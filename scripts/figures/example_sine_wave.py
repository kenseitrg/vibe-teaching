#!/usr/bin/env python3
"""
Generate a simple example sine wave figure for testing lecture-note rendering.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def main():
    t = np.linspace(0, 1, 500)
    y = np.sin(2 * np.pi * 5 * t)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(t, y)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Example sine wave")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    out = Path("figures/example_sine_wave.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
