# OCR-based text extraction

This project can extract text from scanned PDFs that do not have a selectable text layer (for example, the Hatton and Margrave textbooks). The OCR pipeline uses the **Baidu/Unlimited-OCR** vision-language model in its quantized GGUF form, served locally via **llama.cpp**.

## What the pipeline does

1. Renders the requested PDF pages to PNG images at a configurable DPI.
2. Starts a local `llama-server` process running the Unlimited-OCR GGUF model.
3. Sends each page image to the OpenAI-compatible `/v1/chat/completions` endpoint.
4. Collects the recognized text, optionally strips bounding-box markers, and writes a single `.txt` file with per-page markers.

## One-time setup

### 1. Build llama.cpp from the DeepSeek-OCR support branch

Unlimited-OCR is based on the DeepSeek-OCR architecture and requires a llama.cpp build that supports it. At the time of writing, the required changes are in PR #24975 (which includes the V-cache fix for correct tables/layout).

```bash
# Clone the branch
git clone https://github.com/ggml-org/llama.cpp tools/llama.cpp
cd tools/llama.cpp
git fetch origin pull/24975/head:pr24975
git checkout pr24975

# Build with CUDA (recommended)
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON
cmake --build build -j --target llama-server

# Verify
ls build/bin/llama-server
```

For a CPU-only build, omit `-DGGML_CUDA=ON`.

### 2. Download the quantized model and vision projector

```bash
uv run hf download sahilchachra/Unlimited-OCR-GGUF \
    --include "Unlimited-OCR-Q4_K_M.gguf" \
    --include "mmproj-Unlimited-OCR-F16.gguf" \
    --local-dir models/unlimited-ocr
```

This downloads about **2.6 GB** (1.8 GB text model + 0.8 GB vision projector). The `Q4_K_M` quantization is the recommended default balance between size and quality.

### 3. Install the OCR Python dependencies

```bash
uv sync --extra ocr
```

This installs `huggingface-hub` and `requests` used by the wrapper. `PyMuPDF` is already a core dependency.

## Usage

### Direct OCR script

```bash
# Whole PDF
uv run python scripts/extract_source_text_ocr.py papers/textbooks/Methods.pdf

# Page range only
uv run python scripts/extract_source_text_ocr.py papers/textbooks/Methods.pdf --pages 10-20

# On a GPU with limited VRAM (e.g., 6 GB RTX 3060), keep the vision projector on CPU
uv run python scripts/extract_source_text_ocr.py papers/textbooks/Methods.pdf --no-mmproj-offload
```

Output is written to `wiki/sources/_raw_text/<stem>.txt` by default. You can change it with `-o`.

### Via the existing extractor

The main `extract_source_text.py` script has an `--ocr` flag that routes PDFs through the OCR pipeline:

```bash
uv run python scripts/extract_source_text.py papers/textbooks/Methods.pdf --ocr --no-mmproj-offload
uv run python scripts/extract_source_text.py papers/textbooks/Methods.pdf --ocr --pages 10-20
```

PPT/PPTX files are still handled by the regular extractor.

## Tuning options

| Flag | Default | Purpose |
|------|---------|---------|
| `--dpi` | 200 | Rendering resolution for PDF pages. Higher values improve small-font accuracy but increase GPU memory use and inference time. |
| `--n-predict` | 4096 | Maximum tokens per page. Increase for very dense pages. |
| `--prompt` | `document parsing.` | The model prompt. `document parsing.` gives layout-aware output (good for text + figures). |
| `--strip-grounding` | on | Removes bounding-box markers like `text [x1,y1,x2,y2]`. Pass `--no-strip-grounding` to keep the raw model output. |
| `--no-mmproj-offload` | off | Keeps the vision projector on the CPU; often necessary on 6 GB GPUs. |
| `--chat-template-file` | `tools/unlimited_ocr_chat_template.jinja` | Custom Jinja template used to format the request. The default template includes the `<\|User\|>` / `<\|Assistant\|>` tokens the model expects. |

## Common issues

- **Out-of-memory on GPU**: The vision projector is the biggest consumer of VRAM. Use `--no-mmproj-offload` to run it on the CPU. On a 6 GB RTX 3060 this is usually required.
- **Server does not become ready**: Check `log/llama_server.log` for the exact error. Common causes are a missing `llama-server` binary, missing model files, or an unsupported CUDA architecture.
- **Repetitive or hallucinated output**: Title pages and pages with very large fonts or mostly figures can confuse the model. Try a content-rich page first, and ensure the custom chat template is being used (the default built-in `deepseek-ocr` template is intended for CLI use, not the server).

## License

Unlimited-OCR and the GGUF conversions are MIT-licensed. The upstream `llama.cpp` is also permissively licensed. This wrapper code is part of the course-materials project and follows the same license terms as the rest of the repository.
