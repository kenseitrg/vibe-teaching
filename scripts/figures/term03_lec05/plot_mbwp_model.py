"""
MBWP model diagram for Term 3 Lecture 5 (Figure 11).

A *physical* view of the recorded seismic trace: the diagram follows the
actual journey of the wave from the source to the recording system, top to
bottom,

    Source -> Earth absorption -> Reflectivity -> (+ noise) ->
        Detector -> Instrument -> Recorded trace.

Alongside each physical stage we attach the corresponding Model-Based
Wavelet Processing (MBWP) component — the measured or modeled signature that
MBWP uses to describe that stage:

    source signature S(t)  -> Source
    effective absorption   -> Earth absorption      (free parameter Q)
    S/N level              -> added noise           (free parameter)
    detector response D(t) -> Detector
    instrument response I(t)-> Instrument

The random noise n(t), scaled by the S/N level, joins the reflected signal at
the (+) junction; the combined wavelet + noise then passes through the
detector and instrument responses to form the recorded trace x(t). Convolution
is denoted by "*".

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
OUT_PATH = OUT_DIR / "term03_lec05_mbwp_model"

# ---------------------------------------------------------------------------
# Colorblind-friendly palette
# ---------------------------------------------------------------------------
CLR_STAGE = "#e8edf2"     # light grey-blue — physical wave stages
CLR_RESULT = "#1f4e79"    # dark blue       — recorded trace
CLR_COMP = "#fee8c8"      # light orange    — MBWP model components
CLR_NOISE = "#fde0dd"     # light pink      — random noise
CLR_WAVELET = "#377eb8"   # blue            — convolution links / accents
CLR_TEXT = "#222222"
CLR_EDGE = "#333333"
CLR_LINK = "#7f8c8d"      # grey            — model-component links
FONT = "Helvetica"

# ---------------------------------------------------------------------------
# Build the diagram
# ---------------------------------------------------------------------------
dot = Digraph(
    name="mbwp_model",
    format="png",
    graph_attr={
        "rankdir": "TB",
        "bgcolor": "white",
        "splines": "ortho",
        "size": "7.5,9.5",        # portrait-ish: suits a lecture-notes page
        "ratio": "auto",
        "dpi": "150",
        "nodesep": "0.5",
        "ranksep": "0.42",
        "fontname": FONT,
        "label": "Model-Based Wavelet Processing (MBWP) — physical wave-path model",
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
        "margin": "0.12,0.06",
        "fontcolor": CLR_TEXT,
    },
    edge_attr={
        "fontname": FONT,
        "fontsize": "10",
        "color": CLR_EDGE,
        "arrowsize": "0.8",
    },
)

# --- Main physical wave path (central column, top -> bottom) ---------------
stages = [
    ("source", "Source\n(vibroseis · dynamite · airgun)"),
    ("absorp", "Earth absorption"),
    ("refl", "Reflectivity\nr(t)"),
    ("detector", "Detector\n(geophone / hydrophone)"),
    ("instrument", "Instrument\n(recording filters)"),
]
for key, label in stages:
    dot.node(key, label, fillcolor=CLR_STAGE, width="2.5", height="0.7")

# Summing junction where noise joins the reflected signal.
dot.node(
    "add", "+", shape="circle", width="0.5", height="0.5",
    style="filled", fillcolor="white", fontsize="20", penwidth="1.5",
)
# Recorded trace — the output.
dot.node(
    "trace", "Recorded trace\nx(t)", fillcolor=CLR_RESULT,
    fontcolor="white", width="2.5", height="0.7", penwidth="1",
)

# Main path edges (weighted so this column stays the backbone).
for src, dst in [
    ("source", "absorp"),
    ("absorp", "refl"),
    ("refl", "add"),
    ("add", "detector"),
    ("detector", "instrument"),
    ("instrument", "trace"),
]:
    dot.edge(src, dst, weight="5")

# --- Added noise (joins from the right at the (+) junction) ----------------
dot.node("sn", "S/N level\n(free parameter)", fillcolor=CLR_COMP, width="1.8", height="0.7", penwidth="2.5")
dot.node("noise", "Random noise\nn(t)", fillcolor=CLR_NOISE, width="1.8", height="0.7")
dot.edge("noise", "sn")
dot.edge("sn", "add")
with dot.subgraph() as s:      # keep the noise pair on one row
    s.attr(rank="same")
    s.node("noise")
    s.node("sn")

# --- MBWP model components (side annotations, linked to their stage) -------
components = [
    ("src_sig", "Source signature S(t)\nKlauder / derivative /\nfar-field signature", "source", "1"),
    ("q_comp", "Effective Q\n(free parameter)\nQ_eff ≈ 15–50", "absorp", "2.5"),
    ("d_comp", "Detector response D(t)\nmeasured: tap test /\nspecifications", "detector", "1"),
    ("i_comp", "Instrument response I(t)\nmeasured: pulse test", "instrument", "1"),
]
for key, label, _stage, pen in components:
    dot.node(key, label, fillcolor=CLR_COMP, width="2.2", height="0.85", penwidth=pen)

# Dashed grey links tie each component to the physical stage it describes.
for key, _label, stage, _pen in components:
    dot.edge(key, stage, style="dashed", color=CLR_LINK, arrowhead="none", constraint="false")

# S/N is itself the noise component — link it to the summing junction too.
dot.edge("sn", "add", style="dashed", color=CLR_LINK, arrowhead="none", constraint="false")

# Align each component with its physical stage on the same row.
for _key, _label, stage, _pen in components:
    comp = _key
    with dot.subgraph() as s:
        s.attr(rank="same")
        s.node(stage)
        s.node(comp)

# --- Legend ----------------------------------------------------------------
legend_lines = [
    "Grey — physical stages of the recorded wave (top → bottom).",
    "Orange — MBWP model components linked to their stage; bold outline = free parameters (Q, S/N).",
    "Random noise n(t) is scaled by the S/N level and added to the reflected signal at the (+) junction.",
    "Each stage acts by convolution; together the components form the model wavelet W(t) = S(t) * Q(t) * D(t) * I(t).",
]
with dot.subgraph() as s:
    s.attr(rank="sink")
    s.node(
        "legend",
        "\n".join(legend_lines),
        shape="note",
        fillcolor="#fffacd",
        style="filled",
        fontsize="10",
        fontcolor=CLR_TEXT,
        width="6.6",
    )
dot.edge("instrument", "legend", style="invis")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
dot.render(str(OUT_PATH), cleanup=True)
print(f"Saved {OUT_PATH}.png")
