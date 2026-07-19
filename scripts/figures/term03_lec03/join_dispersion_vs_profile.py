"""Join dispersion curve fit and inverted Vs profile into a single side-by-side figure."""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img_curves = mpimg.imread("slides/raw/inverted_curves.jpg")
img_profile = mpimg.imread("slides/raw/inverted_profile.png")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.imshow(img_curves)
ax1.set_axis_off()
ax1.set_title("(a) Dispersion curve fit", fontsize=12, pad=10)

ax2.imshow(img_profile)
ax2.set_axis_off()
ax2.set_title("(b) Inverted $V_s$ profile", fontsize=12, pad=10)

plt.tight_layout()
plt.savefig("figures/term03_lec03/term03_lec03_inversion_result.png", dpi=150, bbox_inches="tight")
plt.close()
