"""
MBWP workflow diagram for Term 3 Lecture 5 (Figure 12).

The three-step Model-Based Wavelet Processing (MBWP) workflow:

  Step 1 — Initial model.
      Load the measured instrument, detector, and source responses; start
      from default Q = 30 and S/N = 20 dB; convolve the components into the
      initial model wavelet W(t).

  Step 2 — Parameter estimation.
      Compute log power spectra of field traces, fit the model log-spectrum
      to the data (spectral slope -> Q, level difference -> S/N), and
      decompose Q and S/N surface-consistently to obtain average values.

  Step 3 — Final operator.
      Rebuild the model wavelet with the estimated Q and S/N, derive the
      residual filter that corrects what spiking deconvolution leaves
      behind, QC the amplitude and phase spectra, and export the operator.

The script is self-contained and writes a single PNG to figures/term03_lec05/.
"""

from pathlib import Path

from graphviz import Digraph

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
OUT_DIR = PROJECT_ROOT / "figures" / "term03_lec05"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "term03_lec05_mbwp_workflow"

# ---------------------------------------------------------------------------
# Colorblind-friendly palette
# ---------------------------------------------------------------------------
CLR_INPUT = "#e0ecf4"     # light blue   — measured / known inputs
CLR_STEP = "#f4f1e6"      # light sand   — workflow step blocks
CLR_PARAM = "#fee8c8"     # light orange — free parameters
CLR_TEXT = "#222222"
CLR_EDGE = "#333333"
CLR_LINK = "#7f8c8d"      # grey         — secondary links
FONT = "Helvetica"

# ---------------------------------------------------------------------------
# Build the diagram
# ---------------------------------------------------------------------------
dot = Digraph(
    name="mbwp_workflow",
    format="png",
    graph_attr={
        "rankdir": "TB",
        "bgcolor": "white",
        "splines": "ortho",
        "size": "8.5,11",         # portrait-ish: suits a lecture-notes page
        "ratio": "auto",
        "dpi": "150",
        "nodesep": "0.5",
        "ranksep": "0.5",
        "fontname": FONT,
        "label": "Model-Based Wavelet Processing (MBWP) — three-step workflow",
        "labelloc": "t",
        "fontsize": "20",
        "fontcolor": CLR_TEXT,
        "pad": "0.3",
    },
    node_attr={
        "fontname": FONT,
        "fontsize": "11",
        "shape": "box",
        "style": "rounded,filled",
        "margin": "0.14,0.08",
        "fontcolor": CLR_TEXT,
    },
    edge_attr={
        "fontname": FONT,
        "fontsize": "10",
        "color": CLR_EDGE,
        "arrowsize": "0.9",
    },
)

# --- Measured / known inputs feeding Step 1 --------------------------------
dot.node(
    "meas",
    "Measured / known responses\nsource signature · detector response · instrument response",
    fillcolor=CLR_INPUT, width="5.2", height="0.8",
)
dot.node(
    "defaults",
    "Default starting parameters\nQ = 30   ·   S/N = 20 dB",
    fillcolor=CLR_PARAM, width="5.2", height="0.8", penwidth="2",
)

# --- Step 1 ----------------------------------------------------------------
dot.node(
    "step1",
    "STEP 1 — Build the initial model\n\n"
    "Convolve the responses into the initial model wavelet W(t)\n"
    "Output: signal and noise model autocorrelations",
    fillcolor=CLR_STEP, width="5.6", height="1.3", penwidth="1.5",
)

# --- Step 2 ----------------------------------------------------------------
dot.node(
    "step2",
    "STEP 2 — Estimate Q and S/N from field data\n\n"
    "Compute log power spectra of field traces\n"
    "Fit model log-spectrum to data  →  spectral slope gives Q, level gives S/N\n"
    "Decompose Q and S/N surface-consistently; average from histograms",
    fillcolor=CLR_STEP, width="5.6", height="1.6", penwidth="1.5",
)

# --- Step 3 ----------------------------------------------------------------
dot.node(
    "step3",
    "STEP 3 — Build the final operator\n\n"
    "Rebuild W(t) with the estimated Q and S/N\n"
    "Residual filter = model wavelet vs. spiking-decon result\n"
    "QC amplitude & phase; taper ends; export production filter",
    fillcolor=CLR_STEP, width="5.6", height="1.6", penwidth="1.5",
)

# --- Flow edges ------------------------------------------------------------
dot.edge("meas", "step1", weight="5")
dot.edge("defaults", "step1", weight="5")
with dot.subgraph() as s:           # inputs share the row above Step 1
    s.attr(rank="same")
    s.node("meas")
    s.node("defaults")

dot.edge("step1", "step2", weight="5")
dot.edge("step2", "step3", weight="5")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
dot.render(str(OUT_PATH), cleanup=True)
print(f"Saved {OUT_PATH}.png")
