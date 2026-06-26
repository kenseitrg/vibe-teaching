"""
Assemble a side-by-side comparison figure from the real-data examples in
slides/raw/: trace-by-trace deconvolution vs. surface-consistent deconvolution.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def main():
    left = mpimg.imread("slides/raw/trace_by_trace_decon.png")
    right = mpimg.imread("slides/raw/surface_consistent_decon.png")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

    for ax, img, title in [
        (axes[0], left, "Trace-by-trace deconvolution"),
        (axes[1], right, "Surface-consistent deconvolution"),
    ]:
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(title, fontsize=12, fontweight="bold", pad=10)

    fig.tight_layout()
    out = "figures/term01_lec07/term01_lec07_surface_consistent_example.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
