"""
Processing flow diagram for Term 1 Lecture 03.

Shows the sequence of kinematic and static corrections from raw shot records to
a zero-offset stack section, with migration deferred to Term 2/3.

The script is self-contained and writes a single PNG to figures/term01_lec03/.
"""

from graphviz import Digraph

# ---------------------------------------------------------------------------
# Build the flow diagram
# ---------------------------------------------------------------------------
dot = Digraph(
    name="processing_flow",
    format="png",
    graph_attr={
        "rankdir": "TB",
        "bgcolor": "white",
        "splines": "ortho",
        "size": "3.5,5.5",
        "ratio": "compress",
        "dpi": "200",
    },
    node_attr={
        "shape": "box",
        "style": "rounded,filled",
        "fillcolor": "#f0f4f8",
        "fontname": "Helvetica",
        "fontsize": "10",
        "height": "0.35",
        "width": "2.0",
    },
    edge_attr={"fontname": "Helvetica", "fontsize": "9"},
)

nodes = [
    "Raw shot records",
    "Sort to CMP\ngathers",
    "Static corrections",
    "NMO correction\n(needs velocity)",
    "Mute",
    "Stack",
    "Zero-offset section",
    "Migration\n(Term 2/3)",
]

for node in nodes:
    dot.node(node)

for i in range(len(nodes) - 1):
    dot.edge(nodes[i], nodes[i + 1])

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
output_path = "figures/term01_lec03/term01_lec03_processing_flow"
dot.render(output_path, cleanup=True)
print(f"Saved {output_path}.png")
