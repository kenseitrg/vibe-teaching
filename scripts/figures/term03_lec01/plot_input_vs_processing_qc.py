"""
Processing QC flow diagram for Term 3 Lecture 1.

Shows the difference between input-data QC («Входной контроль»)
and processing-stage QC («Контроль на каждом этапе»). Input QC checks
raw data before processing; stage QC checks the result of each major
processing step. The two overlap because some attributes are recomputed
after each stage.

The script is self-contained and writes a single PNG to figures/term03_lec01/.
"""

from pathlib import Path
from graphviz import Digraph

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
OUT_DIR = PROJECT_ROOT / "figures" / "term03_lec01"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "term03_lec01_input_vs_processing_qc"

# ---------------------------------------------------------------------------
# Colorblind-friendly palette
# ---------------------------------------------------------------------------
CLR_PROCESS = "#e8f4f8"   # light blue — processing steps
CLR_INPUT_QC = "#1f4e79"  # dark blue — input-data QC
CLR_STAGE_QC = "#d95f02"  # orange — processing-stage QC
CLR_TEXT = "#333333"
CLR_EDGE = "#555555"

# ---------------------------------------------------------------------------
# Build the diagram
# ---------------------------------------------------------------------------
dot = Digraph(
    name="input_vs_processing_qc",
    format="png",
    graph_attr={
        "rankdir": "TB",
        "bgcolor": "white",
        "splines": "ortho",
        "size": "10,6",
        "ratio": "compress",
        "dpi": "150",
        "nodesep": "0.45",
        "ranksep": "0.45",
        "fontname": "Helvetica",
        "label": "Входной и поэтапный контроль качества обработки",
        "labelloc": "t",
        "fontsize": "24",
        "fontcolor": CLR_TEXT,
    },
    node_attr={
        "fontname": "Helvetica",
        "fontsize": "11",
        "shape": "box",
        "style": "rounded,filled",
        "margin": "0.10,0.05",
        "fontcolor": CLR_TEXT,
    },
    edge_attr={
        "fontname": "Helvetica",
        "fontsize": "10",
        "color": CLR_EDGE,
    },
)

# Processing steps (left column)
process_steps = [
    ("input", "Входные данные\n(сырые сейсмограммы)"),
    ("amp", "Коррекция\nамплитуд"),
    ("decon", "Деконволюция"),
    ("noise", "Подавление\nпомех"),
    ("velocity", "Анализ скоростей\n/ NMO"),
    ("stack", "Суммирование"),
    ("demult", "Подавление\nкратных волн"),
    ("migration", "Миграция"),
]

# QC checkpoints (right column)
qc_steps = [
    ("qc_input", "Входной контроль\nгеометрия, атрибуты,\nпервые вступления", "box"),
    ("qc_amp", "Амплитудные атрибуты\n(спектр)", "diamond"),
    ("qc_decon", "Стабильность импульса\nфаза, привязка", "diamond"),
    ("qc_noise", "Разностной разрез\n+ сохранение сигнала", "diamond"),
    ("qc_velocity", "Плоские ОСТ-годографы\nостаточная кинематика", "diamond"),
    ("qc_stack", "Прослеживаемость горизонтов\nкогерентность", "diamond"),
    ("qc_demult", "Кратные волны на\nспектрах скоростей", "diamond"),
    ("qc_migration", "Кросс-плоты с отбивками\nглубинные карты", "diamond"),
]

# Add processing nodes
for key, label in process_steps:
    dot.node(key, label, fillcolor=CLR_PROCESS, width="2.0", height="0.55", fixedsize="true")

# Add QC nodes (input QC as a dark box, stage QC as orange diamonds)
for key, label, shape in qc_steps:
    dot.node(
        key,
        label,
        fillcolor=CLR_INPUT_QC if key == "qc_input" else CLR_STAGE_QC,
        shape=shape,
        fontcolor="white",
        width="3.4",
        height="1.2",
        fixedsize="true",
    )

# Align each processing step with its QC checkpoint on the same row
for (proc_key, _), (qc_key, _, _) in zip(process_steps, qc_steps):
    with dot.subgraph() as s:
        s.attr(rank="same")
        s.node(proc_key)
        s.node(qc_key)

# Vertical flow of processing steps
for i in range(len(process_steps) - 1):
    dot.edge(process_steps[i][0], process_steps[i + 1][0])

# Vertical flow of QC checkpoints (dotted to keep it secondary)
for i in range(len(qc_steps) - 1):
    dot.edge(qc_steps[i][0], qc_steps[i + 1][0], style="dotted")

# Each processing step is checked by the QC checkpoint at the same level
for proc, qc in zip(process_steps, qc_steps):
    dot.edge(proc[0], qc[0], style="dashed")

# Note at the bottom serving as both legend and overlap explanation
with dot.subgraph() as s:
    s.attr(rank="sink")
    s.node(
        "note",
        "Синий прямоугольник — Входной контроль; оранжевый ромб — Контроль на каждом этапе.\n"
        "Некоторые атрибуты пересчитываются на каждом этапе обработки.",
        shape="note",
        fillcolor="#fffacd",
        style="filled",
        fontsize="10",
        fontcolor=CLR_TEXT,
    )

# Invisible edges to keep the note centered under the two columns
dot.edge("migration", "note", style="invis")
dot.edge("qc_migration", "note", style="invis")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
dot.render(str(OUT_PATH), cleanup=True)
print(f"Saved {OUT_PATH}.png")
