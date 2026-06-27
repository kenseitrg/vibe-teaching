#!/usr/bin/env python3
"""
Figure: SEG-Y file structure diagram.

Shows the physical organisation of a standard SEG-Y file as a vertical
stack of blocks:

  1. Textual file header   –  3200 bytes (EBCDIC card images)
  2. Binary file header    –   400 bytes (sample format, number of
                              samples, sample interval, etc.)
  3. Extended textual hdr  –  3200 bytes each (optional, one or more)
  4. Data traces           –  each with a 240-byte trace header followed
                              by trace sample data

An exploded detail on the right side highlights key trace-header fields
(shot/receiver line and point, X/Y coordinates, offset, CMP number,
number of samples, sample interval) that students commonly need to locate
when working with real SEG-Y files.

Pedagogical intention: give students a clear mental picture of how
metadata and trace data are physically laid out inside a SEG-Y file,
the most widely used format in exploration seismology.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path


# ---------------------------------------------------------------------------
# Colour palette  —  dark / saturated blocks so white text is clearly legible
# ---------------------------------------------------------------------------
C_TEXT      = "#1A3C6E"   # dark navy blue   – textual file header
C_BINARY    = "#1B6B3F"   # dark green       – binary file header
C_EXTENDED  = "#4A1A7A"   # dark violet      – extended textual header
C_TRACE_HDR = "#B84A0F"   # burnt orange     – trace header
C_TRACE_DAT = "#B81C24"   # crimson red      – trace data
C_DETAIL_BG = "#F9F6F0"   # warm beige       – detail box background
C_FIELD_ODD = "#FCEED9"   # light orange     – alternating row in detail table
C_FIELD_EVN = "#FFF8EE"   # lighter          – alternating row
C_HEAD_ROW  = "#B84A0F"   # burnt orange     – table header row
C_HIGHLIGHT = "#FFE4B5"   # moccasin         – highlighted rows
C_CAPTION   = "#666666"   # caption text (dark grey)
C_TITLE     = "#222222"   # title text
C_SUBTITLE  = "#555555"   # subtitle text


# ---------------------------------------------------------------------------
# Helper: draw a labelled block with optional size label
# ---------------------------------------------------------------------------
def draw_block(ax, x, y, w, h, color, name, size_str="",
               name_fs=9, size_fs=7, text_color="white",
               edgecolor="white", linewidth=1.5):
    """Rounded rectangle with name and optional byte-size label.

    *x*, *y* are the **bottom-left** corner in data coordinates (= inches).
    A subtle drop shadow and a light border improve readability.
    """
    # Shadow
    shadow = mpatches.FancyBboxPatch(
        (x + 1.2, y - 1.2), w, h,
        boxstyle="round,pad=4",
        facecolor="#CCCCCC", edgecolor="none", alpha=0.15, zorder=1,
    )
    ax.add_patch(shadow)

    # Main box
    box = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=4",
        facecolor=color, edgecolor=edgecolor,
        linewidth=linewidth, zorder=2,
    )
    ax.add_patch(box)

    # Name label
    ax.text(
        x + w / 2, y + h / 2 + (4 if size_str else 0),
        name, ha="center", va="center",
        fontsize=name_fs, fontweight="bold", color=text_color, zorder=3,
    )

    # Byte-size sublabel
    if size_str:
        ax.text(
            x + w / 2, y + h / 2 - 10,
            size_str, ha="center", va="top",
            fontsize=size_fs, color=text_color,
            alpha=0.90, fontstyle="italic", zorder=3,
        )


def draw_detail_header_row(ax, x_left, y_top, w, h, label_left, label_right,
                           fontsize=7.5, text_color="white"):
    """Draw a full-width coloured header row for the detail table."""
    rect = plt.Rectangle(
        (x_left, y_top - h), w, h,
        facecolor=C_HEAD_ROW, edgecolor="#333333", linewidth=0.6, zorder=3,
    )
    ax.add_patch(rect)
    ax.text(
        x_left + 6, y_top - h / 2,
        label_left, ha="left", va="center",
        fontsize=fontsize, fontweight="bold", color=text_color, zorder=4,
    )
    ax.text(
        x_left + w - 6, y_top - h / 2,
        label_right, ha="right", va="center",
        fontsize=fontsize, fontweight="bold", color=text_color, zorder=4,
    )
    return y_top - h


def draw_detail_row(ax, x_left, y_top, w, h,
                    byte_col, field_col, desc_col="",
                    fontsize=7, is_odd=True, highlight=False):
    """Draw one row in the trace-header detail table."""

    if highlight:
        bg = C_HIGHLIGHT
    else:
        bg = C_FIELD_ODD if is_odd else C_FIELD_EVN

    rect = plt.Rectangle(
        (x_left, y_top - h), w, h,
        facecolor=bg, edgecolor="#CCBBAA", linewidth=0.4, zorder=3,
    )
    ax.add_patch(rect)

    x_b = x_left + 6
    x_f = x_left + 68
    x_d = x_left + 155

    ax.text(x_b, y_top - h / 2, byte_col, ha="left", va="center",
            fontsize=fontsize, fontweight="bold", color="#222222", zorder=4)
    ax.text(x_f, y_top - h / 2, field_col, ha="left", va="center",
            fontsize=fontsize, fontweight="bold", color="#111111", zorder=4)
    if desc_col:
        ax.text(x_d, y_top - h / 2, desc_col, ha="left", va="center",
                fontsize=fontsize - 0.5, color="#444444", zorder=4)

    return y_top - h


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # ---- Figure dimensions (inches) --------------------------------------
    FIG_W = 10.5
    FIG_H = 8.0

    # Column positions
    LEFT_X  = 0.7          # left edge of main structure blocks
    STACK_W = 3.5          # width of each main stack block

    RIGHT_X = 5.5          # left edge of detail panel
    DET_W   = 4.4          # width of detail panel

    TOP_GAP = 1.10         # space at top for title
    BOT_GAP = 0.85         # space at bottom for caption

    # ---- Build figure and axes -------------------------------------------
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, FIG_H))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis("off")

    # ======================================================================
    # LEFT COLUMN — Main file structure stack
    # ======================================================================

    # Heights proportional to byte sizes (with minimum readability)
    H_TEXT    = 1.10      # 3200 bytes
    H_BIN     = 0.45      # 400 bytes
    H_EXT     = 1.00      # 3200 bytes
    H_TR_HDR  = 0.35      # 240 bytes
    H_TR_DAT1 = 0.75      # trace data (varies, ~1000-8000 bytes)
    H_TR_DAT2 = 0.75      # second trace data
    H_TR_DAT3 = 0.50      # third trace data (partial for visual balance)

    GAP_SM = 0.10         # small gap between blocks in the stack
    GAP_MD = 0.20         # medium gap

    # Total height of the stack
    y_start = FIG_H - TOP_GAP - H_TEXT

    # ---- 1. Textual File Header ------------------------------------------
    y = y_start
    draw_block(ax, LEFT_X, y, STACK_W, H_TEXT, C_TEXT,
               "Textual File Header", "3200 bytes (EBCDIC)",
               name_fs=9, size_fs=7)
    y -= H_TEXT + GAP_SM

    # ---- 2. Binary File Header -------------------------------------------
    draw_block(ax, LEFT_X, y, STACK_W, H_BIN, C_BINARY,
               "Binary File Header", "400 bytes",
               name_fs=8.5, size_fs=7)
    y -= H_BIN + GAP_SM

    # ---- 3. Extended Textual Headers (optional) --------------------------
    draw_block(ax, LEFT_X, y, STACK_W, H_EXT, C_EXTENDED,
               "Extended Textual Header(s)", "3200 bytes each, optional",
               name_fs=8.5, size_fs=7)
    y -= H_EXT + GAP_SM

    # Optional ellipsis to indicate "one or more"
    ax.plot(
        [LEFT_X + 0.32, LEFT_X + STACK_W - 0.32],
        [y + 0.06, y + 0.06],
        color="#888888", linewidth=2, marker="o", markersize=3,
        linestyle="", zorder=3,
    )
    ax.text(
        LEFT_X + STACK_W / 2, y - 0.04,
        "(1 or more extended headers if present)", ha="center", va="top",
        fontsize=6.5, fontstyle="italic", color="#777777", zorder=3,
    )
    y -= GAP_MD + 0.12

    # ---- 4. Data traces --------------------------------------------------
    # Draw a bracket-ish label on the left
    ax.text(
        LEFT_X - 0.35, y - (3 * H_TR_HDR + 3 * H_TR_DAT1 + 2 * GAP_SM) / 2,
        "Data\nTraces", ha="center", va="center",
        fontsize=8, fontweight="bold", color="#444444", zorder=3,
        rotation=0,
    )

    # Trace 1
    draw_block(ax, LEFT_X, y, STACK_W * 0.35, H_TR_HDR, C_TRACE_HDR,
               "Trace Header", "240 B", name_fs=7.5, size_fs=6)
    x_data = LEFT_X + STACK_W * 0.35 + GAP_SM
    draw_block(ax, x_data, y, STACK_W * 0.65 - GAP_SM, H_TR_HDR, C_TRACE_DAT,
               "Trace Data", "Nsam × IB", name_fs=7.5, size_fs=6)
    # "Trace 1" label to the right
    ax.text(
        x_data + STACK_W * 0.65 - GAP_SM + 0.10, y + H_TR_HDR / 2,
        "Trace 1", ha="left", va="center",
        fontsize=7, fontstyle="italic", color="#888888", zorder=3,
    )
    y -= H_TR_HDR + GAP_SM

    # Trace 2
    draw_block(ax, LEFT_X, y, STACK_W * 0.35, H_TR_HDR, C_TRACE_HDR,
               "Trace Header", "240 B", name_fs=7.5, size_fs=6)
    draw_block(ax, x_data, y, STACK_W * 0.65 - GAP_SM, H_TR_HDR, C_TRACE_DAT,
               "Trace Data", "Nsam × IB", name_fs=7.5, size_fs=6)
    ax.text(
        x_data + STACK_W * 0.65 - GAP_SM + 0.10, y + H_TR_HDR / 2,
        "Trace 2", ha="left", va="center",
        fontsize=7, fontstyle="italic", color="#888888", zorder=3,
    )
    y -= H_TR_HDR + GAP_SM

    # Trace 3
    draw_block(ax, LEFT_X, y, STACK_W * 0.35, H_TR_HDR, C_TRACE_HDR,
               "Trace Header", "240 B", name_fs=7.5, size_fs=6)
    draw_block(ax, x_data, y, STACK_W * 0.65 - GAP_SM, H_TR_HDR, C_TRACE_DAT,
               "Trace Data", "Nsam × IB", name_fs=7.5, size_fs=6)
    ax.text(
        x_data + STACK_W * 0.65 - GAP_SM + 0.10, y + H_TR_HDR / 2,
        "Trace 3", ha="left", va="center",
        fontsize=7, fontstyle="italic", color="#888888", zorder=3,
    )
    y -= H_TR_HDR + GAP_SM

    # Ellipsis for "more traces"
    ax.plot(
        [LEFT_X + STACK_W * 0.35 / 2, x_data + STACK_W * 0.65 * 0.5],
        [y + 0.02, y + 0.02],
        color="#888888", linewidth=2, marker="o", markersize=3,
        linestyle="", zorder=3,
    )
    ax.text(
        LEFT_X + STACK_W / 2, y - 0.10,
        "... (many traces, up to 10\u2075 or more)", ha="center", va="top",
        fontsize=6.5, fontstyle="italic", color="#777777", zorder=3,
    )

    # ---- Connector: arrow from Trace Header to detail panel --------------
    y_trace1_header = y_start - H_TEXT - H_BIN - GAP_SM - H_EXT - GAP_SM - 0.12
    arrow_y = y_trace1_header - H_TR_HDR / 2

    ax.annotate(
        "", xy=(RIGHT_X, arrow_y), xytext=(LEFT_X + STACK_W * 0.35 + GAP_SM, arrow_y),
        arrowprops=dict(
            arrowstyle="->", color="#B84A0F", lw=1.8,
            connectionstyle="arc3,rad=0.05",
        ),
        zorder=5,
    )

    # ======================================================================
    # RIGHT COLUMN — Trace Header Detail Panel
    # ======================================================================

    # Panel background
    det_y_top = y_start  # align top with main stack
    panel_bg_color = "#FFFFFF"
    panel = mpatches.FancyBboxPatch(
        (RIGHT_X, det_y_top - 4.0), DET_W, 4.0,
        boxstyle="round,pad=6",
        facecolor=panel_bg_color, edgecolor="#BBBBBB", linewidth=1.2, zorder=2,
    )
    ax.add_patch(panel)

    # Panel title
    ax.text(
        RIGHT_X + DET_W / 2, det_y_top - 0.08,
        "Trace Header Detail (240 bytes)",
        ha="center", va="top", fontsize=9, fontweight="bold",
        color="#222222", zorder=4,
    )

    # Subtitle
    ax.text(
        RIGHT_X + DET_W / 2, det_y_top - 0.30,
        "Key fields commonly used in processing",
        ha="center", va="top", fontsize=7, fontstyle="italic",
        color="#666666", zorder=4,
    )

    # ---- Table of trace header fields ----
    # Column layout within the detail box
    x_tbl = RIGHT_X + 0.15
    tbl_w = DET_W - 0.30
    row_h = 0.26
    header_h = 0.28

    y_row = det_y_top - 0.60

    # Header row
    y_row = draw_detail_header_row(
        ax, x_tbl, y_row, tbl_w, header_h,
        "Bytes", "Field", fontsize=7.5,
    )

    # Field rows: (bytes, field, description, highlight)
    fields = [
        ("1–4",     "Trace seq. (in line)",      "Trace sequence number within line",         False),
        ("5–8",     "Trace seq. (in file)",       "Trace sequence number in SEG-Y file",       False),
        ("9–12",    "Original field rec. #",      "Original field record number",              False),
        ("13–16",   "Trace in field record",      "Trace number within original field record", False),
        ("17–20",   "Shot (source) point #",      "Energy source point number",               True),
        ("21–24",   "CMP / CDP ensemble #",       "Common midpoint / CDP ensemble number",    True),
        ("25–28",   "Trace in CMP ensemble",      "Trace number within CDP ensemble",          False),
        ("29–36",   "(Identification codes)",     "Trace ID, sum, data use flags",            False),
        ("37–40",   "Offset",                     "Distance source \u2192 receiver (m)",        True),
        ("41–76",   "(Elevation / static data)",  "Elevations, statics, scalars",             False),
        ("77–80",   "Source X coordinate",        "X coordinate of source position",           True),
        ("81–84",   "Source Y coordinate",        "Y coordinate of source position",           True),
        ("85–88",   "Receiver X coordinate",       "X coordinate of receiver (group)",         True),
        ("89–92",   "Receiver Y coordinate",       "Y coordinate of receiver (group)",         True),
        ("93–128",  "(Reserved / additional)",    "Coord units, velocities, delays, etc.",     False),
        ("129–130", "Number of samples",           "Samples per trace (Nsam)",                  True),
        ("131–132", "Sample interval (\u03bcs)",  "Sample rate in microseconds",               True),
        ("133–184", "(Additional header)",        "Mute, gain, year, day, etc.",               False),
        ("185–188", "Receiver line number",        "Line number of receiver station",           True),
        ("189–192", "Receiver point number",       "Point number of receiver station",          True),
        ("193–196", "Source line number",          "Line number of source location",            True),
        ("197–200", "Source point number",         "Point number of source location",           True),
        ("201–240", "(Reserved / tail)",          "Mute, gain, year, day, etc.",               False),
    ]

    odd_row = True
    for byte_col, field_col, desc_col, highlight in fields:
        if y_row - row_h < det_y_top - 4.0 + 0.20:
            # Too low, stop drawing
            break
        y_row = draw_detail_row(
            ax, x_tbl, y_row, tbl_w, row_h,
            byte_col, field_col, desc_col,
            fontsize=6.8, is_odd=odd_row, highlight=highlight,
        )
        odd_row = not odd_row

    # ---- Legend for highlight meaning ----
    legend_y = y_row - 0.20
    legend_bg = plt.Rectangle(
        (x_tbl, legend_y - 0.18), tbl_w, 0.20,
        facecolor=C_HIGHLIGHT, edgecolor="#B84A0F", linewidth=0.8,
        linestyle="--", zorder=3,
    )
    ax.add_patch(legend_bg)
    ax.text(
        x_tbl + tbl_w / 2, legend_y - 0.08,
        "  Highlighted rows = fields most often needed by processors",
        ha="center", va="center", fontsize=6.5,
        fontstyle="italic", color="#555555", zorder=4,
    )

    # ======================================================================
    # TITLE
    # ======================================================================
    fig.text(
        0.5, 0.98,
        "SEG-Y File Organisation",
        ha="center", va="top", fontsize=14, fontweight="bold",
        color=C_TITLE,
    )
    fig.text(
        0.5, 0.945,
        "Most common format in exploration seismology \u2014 every byte matters",
        ha="center", va="top", fontsize=8.5, fontstyle="italic",
        color=C_SUBTITLE,
    )

    # ======================================================================
    # CAPTION
    # ======================================================================
    cap_lines = (
        "The SEG-Y file begins with two fixed-length headers, optional extended textual headers, "
        "then a sequence of data traces.\n"
        "Each trace has a 240-byte header holding location, time, and identification metadata, "
        "followed by trace samples (typically\n"
        "IEEE float, 4 bytes each).  Processors routinely read trace-header fields such as offset, "
        "CMP number, source/receiver\n"
        "coordinates, and sample rate to set up geometry and processing parameters."
    )
    fig.text(
        0.5, 0.02,
        cap_lines,
        ha="center", va="bottom", fontsize=7,
        color=C_CAPTION, linespacing=1.35,
    )

    # ======================================================================
    # SAVE
    # ======================================================================
    out_dir = Path("figures/term01_lec01")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "term01_lec01_segy_structure.png"
    fig.savefig(out_path, dpi=150, facecolor="#FFFFFF")
    plt.close(fig)
    print(f"Saved: {out_path}   ({FIG_W:.1f}\u2033 × {FIG_H:.1f}\u2033)")


if __name__ == "__main__":
    main()
