#!/usr/bin/env python3
"""
OCR-based text extraction for scanned PDFs using the Unlimited-OCR GGUF model.

This script is designed to handle PDFs that have no selectable text layer (e.g.
scanned textbooks). It converts each requested page to an image, starts a local
llama-server running the quantized Unlimited-OCR model, and sends the images to
the OpenAI-compatible chat completions endpoint. The resulting text is written
to a single .txt file with per-page markers.

Setup required before first use:
    1. Build llama.cpp from the DeepSeek-OCR support branch (PR #24975) with
       CUDA enabled, so that llama-server is available.
    2. Download the GGUF model and the vision projector:

           uv run hf download sahilchachra/Unlimited-OCR-GGUF \
               --include "Unlimited-OCR-Q4_K_M.gguf" \
               --include "mmproj-Unlimited-OCR-F16.gguf" \
               --local-dir models/unlimited-ocr

    3. Install the optional OCR dependencies:

           uv sync --extra ocr

Typical usage:

    uv run python scripts/extract_source_text_ocr.py papers/textbooks/Hatton.pdf
    uv run python scripts/extract_source_text_ocr.py papers/textbooks/Hatton.pdf --pages 10-20

The server can be kept running between calls with --keep-server, which is useful
when OCRing many short documents back-to-back.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import re

import requests

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None  # type: ignore[assignment]


DEFAULT_SERVER_URL = "http://127.0.0.1:8080"
DEFAULT_SERVER_BIN = Path("tools/llama.cpp/build/bin/llama-server")
DEFAULT_MODEL_DIR = Path("models/unlimited-ocr")
DEFAULT_PROMPT = "document parsing."
DEFAULT_CHAT_TEMPLATE = None
DEFAULT_CHAT_TEMPLATE_FILE = Path("tools/unlimited_ocr_chat_template.jinja")
DEFAULT_CTX_SIZE = 8192
DEFAULT_N_PREDICT = 4096
DEFAULT_DPI = 200
DEFAULT_TEMP = 0.0
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080
SERVER_READY_TIMEOUT = 180  # seconds
REQUEST_TIMEOUT = 600
MAX_RETRIES = 3


def _require_deps() -> None:
    if fitz is None:
        raise RuntimeError(
            "PyMuPDF is required. Install it with: uv add pymupdf"
        )
    try:
        import requests  # noqa: F401
    except ImportError:  # pragma: no cover
        raise RuntimeError(
            "requests is required. Install OCR extras with: uv sync --extra ocr"
        )


def _parse_page_range(page_range: str | None, max_pages: int) -> tuple[int, int]:
    if not page_range:
        return 0, max_pages
    if "-" in page_range:
        start_str, end_str = page_range.split("-", 1)
        start = max(0, int(start_str.strip()) - 1)
        end = min(max_pages, int(end_str.strip()))
        return start, end
    page = int(page_range.strip()) - 1
    return max(0, page), min(max_pages, page + 1)


def pdf_pages_to_images(
    pdf_path: Path, *, dpi: int, page_range: str | None
) -> list[tuple[int, str]]:
    """Render selected PDF pages to temporary PNG files."""
    doc = fitz.open(pdf_path)
    start, end = _parse_page_range(page_range, len(doc))
    tmp_dir = Path(tempfile.mkdtemp(prefix="ocr_"))
    images: list[tuple[int, str]] = []
    mat = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    for i in range(start, end):
        page = doc.load_page(i)
        out_path = tmp_dir / f"page_{i + 1:04d}.png"
        page.get_pixmap(matrix=mat, alpha=False).save(str(out_path))
        images.append((i + 1, str(out_path)))
    doc.close()
    return images


def server_ready(url: str) -> bool:
    """Probe common llama.cpp server health endpoints."""
    for endpoint in (f"{url}/health", f"{url}/healthz", f"{url}/v1/models"):
        try:
            response = requests.get(endpoint, timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
    return False


def start_server(args: argparse.Namespace) -> subprocess.Popen | None:
    """Start llama-server if it is not already running."""
    if server_ready(args.server_url):
        print(f"Reusing existing server at {args.server_url}", file=sys.stderr)
        return None

    server_bin = Path(args.server_bin).resolve()
    if not server_bin.exists():
        raise RuntimeError(
            f"llama-server not found: {server_bin}\n"
            "Build llama.cpp from the DeepSeek-OCR support branch (PR #24975) "
            "and pass --server-bin."
        )

    model_dir = Path(args.model_dir)
    model = model_dir / args.quant
    mmproj = model_dir / args.mmproj
    for path in (model, mmproj):
        if not path.exists():
            raise RuntimeError(
                f"Model file not found: {path}\n"
                "Download it with:\n"
                "  uv run hf download sahilchachra/Unlimited-OCR-GGUF "
                f'--include "{path.name}" --local-dir {model_dir}'
            )

    cmd = [
        str(server_bin),
        "-m",
        str(model),
        "--mmproj",
        str(mmproj),
    ]
    if args.chat_template:
        cmd.extend(["--chat-template", args.chat_template])
    elif args.chat_template_file:
        cmd.extend(["--chat-template-file", args.chat_template_file])
    cmd.extend([
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--ctx-size",
        str(args.ctx_size),
        "--n-predict",
        str(args.n_predict),
        "--temperature",
        str(args.temperature),
        "--parallel",
        "1",
    ])
    if args.gpu_layers is not None:
        cmd.extend(["--n-gpu-layers", str(args.gpu_layers)])
    if not args.mmproj_offload:
        cmd.append("--no-mmproj-offload")

    log_path = Path(args.server_log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_file = log_path.open("w", encoding="utf-8")

    env = os.environ.copy()
    if args.cuda_visible_devices is not None:
        env["CUDA_VISIBLE_DEVICES"] = args.cuda_visible_devices

    print(f"Starting llama-server ...", file=sys.stderr)
    print(f"  {' '.join(cmd)}", file=sys.stderr)
    process = subprocess.Popen(
        cmd, stdout=log_file, stderr=subprocess.STDOUT, env=env
    )
    process._log_file = log_file  # type: ignore[attr-defined]

    deadline = time.time() + SERVER_READY_TIMEOUT
    while time.time() < deadline:
        if process.poll() is not None:
            log_file.flush()
            raise RuntimeError(
                f"llama-server exited early (code {process.returncode}). "
                f"See {log_path}"
            )
        if server_ready(args.server_url):
            print(f"Server ready at {args.server_url}", file=sys.stderr)
            return process
        time.sleep(2)

    stop_server(process)
    raise RuntimeError(
        f"llama-server did not become ready within {SERVER_READY_TIMEOUT}s. "
        f"See {log_path}"
    )


def stop_server(process: subprocess.Popen | None) -> None:
    if process is None:
        return
    try:
        process.terminate()
        process.wait(timeout=10)
    except Exception:
        process.kill()
        process.wait()
    finally:
        if hasattr(process, "_log_file"):
            process._log_file.close()  # type: ignore[attr-defined]


def strip_grounding_markers(text: str) -> str:
    """Remove common grounding/bounding-box markers from OCR output.

    Handles patterns like:
      - word [x1, y1, x2, y2] ...
      - image_caption [x1, y1, x2, y2] ...
      - page_number [x1, y1, x2, y2] ...
      - markdown/table tags emitted by the model (<|td|>, <|tr|>, etc.)
      - [|Non-Text|] / [Non-Text] placeholders
    """
    # Remove any "word [numbers]" prefixes (also handles table tags if present).
    text = re.sub(r"\b\w+\s*\[[\d\s,]+\]\s*", "", text)
    # Remove standalone table/row/cell tags and other grounding tags.
    text = re.sub(r"<\|/?(?:td|tr|det|ref|grounding)[^>]*\|>", "", text)
    # Remove [Non-Text] placeholders.
    text = re.sub(r"\[\|?[^\]]*Non-Text[^\]]*\]", "", text, flags=re.IGNORECASE)
    # Remove any remaining grounding tags.
    text = re.sub(r"<\|/?[^>]+\|>", "", text)
    # Drop lines that are now empty or only whitespace.
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def _encode_image(image_path: str) -> dict:
    ext = Path(image_path).suffix.lower()
    mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}}


def ocr_image(
    image_path: str,
    *,
    server_url: str,
    prompt: str,
    temperature: float,
    max_tokens: int,
) -> str:
    payload = {
        "model": "Unlimited-OCR",
        "messages": [
            {
                "role": "user",
                "content": [
                    _encode_image(image_path),
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                f"{server_url}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            return str(data["choices"][0]["message"]["content"])
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            print(
                f"  OCR request failed ({exc}), retry {attempt}/{MAX_RETRIES}",
                file=sys.stderr,
            )
            time.sleep(2 * attempt)

    raise RuntimeError(
        f"Failed to OCR {image_path} after {MAX_RETRIES} attempts: {last_error}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OCR text extraction from scanned PDFs using Unlimited-OCR GGUF.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", help="PDF file to OCR")
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory (default: wiki/sources/_raw_text)",
    )
    parser.add_argument(
        "--pages", help="Page range, e.g. '10-20' or '5'"
    )
    parser.add_argument(
        "--dpi", type=int, default=DEFAULT_DPI, help="DPI for page rendering"
    )
    parser.add_argument(
        "--server-bin",
        default=str(DEFAULT_SERVER_BIN),
        help="Path to the llama-server binary",
    )
    parser.add_argument(
        "--server-url",
        default=DEFAULT_SERVER_URL,
        help="Base URL of a running llama-server (if not starting one)",
    )
    parser.add_argument(
        "--model-dir",
        default=str(DEFAULT_MODEL_DIR),
        help="Directory containing the GGUF and mmproj files",
    )
    parser.add_argument(
        "--quant",
        default="Unlimited-OCR-Q4_K_M.gguf",
        help="GGUF quantization filename",
    )
    parser.add_argument(
        "--mmproj",
        default="mmproj-Unlimited-OCR-F16.gguf",
        help="Vision projector filename",
    )
    parser.add_argument(
        "--chat-template-file",
        default=str(DEFAULT_CHAT_TEMPLATE_FILE),
        help="Path to a custom Jinja chat template file for llama-server",
    )
    parser.add_argument(
        "--chat-template",
        default=DEFAULT_CHAT_TEMPLATE,
        help="Built-in chat template name (overrides --chat-template-file if set)",
    )
    parser.add_argument(
        "--ctx-size", type=int, default=DEFAULT_CTX_SIZE, help="Context size"
    )
    parser.add_argument(
        "--n-predict",
        type=int,
        default=DEFAULT_N_PREDICT,
        help="Maximum tokens to predict per page",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_TEMP,
        help="Sampling temperature (0 = deterministic)",
    )
    parser.add_argument(
        "--prompt", default=DEFAULT_PROMPT, help="OCR prompt sent to the model"
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host for the local server"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port for the local server"
    )
    parser.add_argument(
        "--no-server-start",
        action="store_true",
        help="Do not start a server; assume one is already running at --server-url",
    )
    parser.add_argument(
        "--keep-server",
        action="store_true",
        help="Keep the server running after extraction finishes",
    )
    parser.add_argument(
        "--cuda-visible-devices",
        default="0",
        help="CUDA_VISIBLE_DEVICES value for the server process",
    )
    parser.add_argument(
        "--gpu-layers",
        type=int,
        default=None,
        help="Number of model layers to offload to GPU (default: llama.cpp default)",
    )
    parser.add_argument(
        "--no-mmproj-offload",
        dest="mmproj_offload",
        action="store_false",
        default=True,
        help="Do not offload the vision projector to the GPU",
    )
    parser.add_argument(
        "--server-log",
        default="log/llama_server.log",
        help="Path to write the server stdout/stderr log",
    )
    parser.add_argument(
        "--strip-grounding",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Remove bounding-box markers from the model output (default: True)",
    )
    args = parser.parse_args()

    _require_deps()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    output_dir = Path(args.output) if args.output else Path("wiki/sources/_raw_text")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{input_path.stem}.txt"

    server_process = None
    if not args.no_server_start:
        server_process = start_server(args)

    try:
        images = pdf_pages_to_images(
            input_path, dpi=args.dpi, page_range=args.pages
        )
        print(
            f"OCRing {len(images)} page(s) from {input_path.name} ...",
            file=sys.stderr,
        )

        pages: list[str] = []
        for page_num, image_path in images:
            print(f"  Page {page_num} ...", file=sys.stderr)
            text = ocr_image(
                image_path,
                server_url=args.server_url,
                prompt=args.prompt,
                temperature=args.temperature,
                max_tokens=args.n_predict,
            )
            if args.strip_grounding:
                text = strip_grounding_markers(text)
            pages.append(f"--- Page {page_num} ---\n{text.strip()}")

        output_file.write_text("\n\n".join(pages), encoding="utf-8")
        print(f"Saved: {output_file}", file=sys.stderr)
    finally:
        if not args.keep_server:
            stop_server(server_process)


if __name__ == "__main__":
    main()
