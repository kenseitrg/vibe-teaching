"""Figure: Multiples create false structure on the stacked section.

A zero-offset synthetic section (approximating a stack) over:
  - a flat, reflective water bottom at 0.4 s,
  - a gentle anticline (real target) at ~1.3 s,
  - a flat reflector at ~1.8 s.

Surface multiples are generated with the 1D feedback relation per trace
(x = x0 - x0*x0 + x0*x0*x0, a preview of SRME). The multiple family of
the anticline re-appears at greater times as a *false* anticline, and
water-bottom multiples imitate flat reflectors at 0.8, 1.2, ... s.

What to notice: without prior knowledge you cannot tell which anticline
is real. Interpreters have drilled false structures of exactly this kind.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 4.0
NX, DX = 201, 25.0
H_WATER, V_WATER = 300.0, 1480.0


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


nt = int(TMAX / DT)
t = np.arange(nt) * DT
x = (np.arange(NX) - NX / 2) * DX
wav = ricker(28, 45, DT)

# --- reflectivity per trace ----------------------------------------------------
t_wb = 2 * H_WATER / V_WATER
t_flat = 1.8
# anticline: lateral two-way time, apex (minimum time) at the centre
t_anti = 1.3 + 0.25 * (x / 1000.0) ** 2

R_wb, R_anti, R_flat = 0.45, 0.28, 0.20

prim = np.zeros((nt, NX))       # multiple-free section
for j in range(NX):
    for t0, R in ((t_wb, R_wb), (t_anti[j], R_anti), (t_flat, R_flat)):
        i0 = int(round(t0 / DT))
        prim[i0:i0 + len(wav), j] += R * wav

# --- add surface multiples via the 1D feedback relation ------------------------
# convolve each trace with itself in the frequency domain
def with_multiples(trace):
    X0 = np.fft.rfft(trace)
    conv1 = np.fft.irfft(X0 * X0, n=nt)
    conv2 = np.fft.irfft(X0 * X0 * X0, n=nt)
    return trace - conv1 + conv2

data = np.apply_along_axis(with_multiples, 0, prim)
data /= np.abs(data).max()
prim /= np.abs(prim).max()

# --- plot ----------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 7), sharex=True, sharey=True)
v = np.percentile(np.abs(data), 99.5)

for ax, sec, title in zip(
        axes,
        (prim, data - prim, data),
        ("Multiple-free section\n('the truth')",
         "Surface multiples only\n(what demultiple must remove)",
         "Recorded section with multiples\n('what we see')")):
    ax.imshow(sec, extent=[x[0], x[-1], TMAX, 0], aspect="auto", cmap="gray",
              vmin=-v, vmax=v)
    ax.set_xlabel("Midpoint (m)")
    ax.set_title(title, fontsize=11)

axes[0].set_ylabel("Two-way time (s)")

# annotate events on the recorded section
axr = axes[2]
axr.annotate("water bottom", (x[0] + 150, 0.48), fontsize=9, color="royalblue")
axr.annotate("WB multiple x2\n(false reflector)", (x[0] + 150, 0.92), fontsize=9,
             color="crimson")
axr.annotate("WB multiple x3", (x[0] + 150, 1.32), fontsize=9, color="crimson")
axr.annotate("REAL anticline", xy=(0, 1.30), xytext=(x[0] + 500, 1.62),
             fontsize=9, color="royalblue",
             arrowprops=dict(arrowstyle="->", color="royalblue"))
axr.annotate("FALSE anticline\n(multiple of the real one)", xy=(0, 2.60),
             xytext=(x[0] + 700, 2.95), fontsize=9, color="crimson",
             arrowprops=dict(arrowstyle="->", color="crimson"))
axr.annotate("flat reflector +\nWB reverberations", (x[-1] - 1400, 2.1), fontsize=9,
             color="crimson", ha="left")

fig.suptitle("Multiples mimic reflectivity: every event on the right panel is a "
             "plausible-looking reflection", fontsize=13)
fig.text(0.5, 0.02,
         "Middle panel = right minus left, computed with the 1D feedback relation "
         "x = x0 - x0*x0 + x0*x0*x0 (SRME preview, Session 2).\nNote the doubled "
         "apparent structure: the false anticline is the surface multiple of the "
         "real one — this is how multiples fool interpretation.",
         ha="center", fontsize=10, color="0.25")
fig.tight_layout(rect=(0, 0.05, 1, 0.93))
fig.savefig("figures/term02_lec03/term02_lec03_false_structure.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_false_structure.png")
