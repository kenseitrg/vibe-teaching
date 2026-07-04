"""
Demonstrate how a long-wavelength static biases velocity analysis.

Key physics:
  A long-wavelength static shifts the whole CMP gather uniformly in time,
  so the event remains a perfect hyperbola with the same NMO velocity but
  a wrong zero-offset time:
      t_shifted(x) = sqrt((t0 + dt)^2 + x^2 / V^2)

  Semblance analysis finds the correct velocity if it is allowed to search
  the new t0.  In practice, picking is often tied to an original (wrong) t0
  — for example horizon-consistent picking or a fixed-time panel — and then
  the best-fit velocity at that wrong t0 is biased.

Three panels:
  (a) CMP gather: true hyperbola and static-shifted hyperbola (same V).
  (b) Semblance spectra: true peak (t0, V), shifted peak (t0+dt, V), and
      the biased pick obtained when the search is constrained to the
      original t0.
  (c) t^2 vs x^2: true line, shifted line (same slope = same V), and the
      constrained-fit line (forced through the true intercept) with a
      different slope = biased velocity.

Undergraduate seismic data processing — Term 1 Lecture 03.
"""

import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# Parameters
# =====================================================================
dt = 0.002
t_max = 2.0
t = np.arange(0, t_max, dt)
nt = len(t)

n_offsets = 31
offsets = np.linspace(0, 2500, n_offsets)      # m, include zero
x2 = offsets ** 2

t0_true = 0.40          # true zero-offset time (s)
v_true = 2000.0         # true NMO velocity (m/s)
static_shift = 0.15     # long-wavelength static (s)
t0_shifted = t0_true + static_shift

# =====================================================================
# Traveltime curves — both are perfect hyperbolas
# =====================================================================
t_true = np.sqrt(t0_true**2 + (offsets / v_true)**2)
t_shifted = np.sqrt(t0_shifted**2 + (offsets / v_true)**2)

t2_true = t_true ** 2
t2_shifted = t_shifted ** 2

# =====================================================================
# Synthetic gathers
# =====================================================================
def ricker(f0, tau):
    """Ricker wavelet with peak frequency f0."""
    return (1 - 2 * (np.pi * f0 * tau) ** 2) * np.exp(-(np.pi * f0 * tau) ** 2)


def make_gather(times, offsets, t_vec, f0=25.0):
    """Build a CMP gather with Ricker wavelets along specified arrival times."""
    no = len(offsets)
    nt = len(t_vec)
    gather = np.zeros((nt, no))
    half_width = int(0.12 / dt)   # 120 ms half-width
    for k in range(no):
        idx = np.argmin(np.abs(t_vec - times[k]))
        start = max(0, idx - half_width)
        end = min(nt, idx + half_width)
        tau = t_vec[start:end] - times[k]
        w = ricker(f0, tau)
        gather[start:end, k] = w
    return gather


gather_true = make_gather(t_true, offsets, t, f0=25.0)
gather_shifted = make_gather(t_shifted, offsets, t, f0=25.0)

# =====================================================================
# Semblance velocity spectrum
# =====================================================================
def semblance_spectrum(gather, offsets, t0_range, v_range, dt, half_win=5):
    """Compute semblance over (t0, V) grid."""
    nt0 = len(t0_range)
    nv = len(v_range)
    m = len(offsets)
    semb = np.zeros((nt0, nv))
    for i, t0 in enumerate(t0_range):
        for j, v in enumerate(v_range):
            t_hyper = np.sqrt(t0**2 + (offsets / v)**2)
            stack = np.zeros(half_win * 2 + 1)
            power = np.zeros(half_win * 2 + 1)
            for k in range(m):
                idx = int(round(t_hyper[k] / dt))
                for w in range(-half_win, half_win + 1):
                    s_idx = idx + w
                    if 0 <= s_idx < gather.shape[0]:
                        stack[w + half_win] += gather[s_idx, k]
                        power[w + half_win] += gather[s_idx, k] ** 2
            numerator = np.sum(stack ** 2)
            denominator = m * np.sum(power)
            if denominator > 0:
                semb[i, j] = numerator / denominator
    return semb


t0_range = np.linspace(0.25, 0.80, 300)
v_range = np.linspace(1400, 2600, 300)

semb_true = semblance_spectrum(gather_true, offsets,
                               t0_range, v_range, dt, half_win=4)
semb_shifted = semblance_spectrum(gather_shifted, offsets,
                                  t0_range, v_range, dt, half_win=4)


def peak_rc(semb, t0_range, v_range):
    """Return (t0, V) of maximum semblance."""
    idx = np.unravel_index(np.argmax(semb), semb.shape)
    return t0_range[idx[0]], v_range[idx[1]]


pt0_t, pv_t = peak_rc(semb_true, t0_range, v_range)
pt0_s, pv_s = peak_rc(semb_shifted, t0_range, v_range)

# =====================================================================
# Least-squares fits in t^2 vs x^2
# =====================================================================
coeff_true = np.polyfit(x2, t2_true, 1)
coeff_shifted = np.polyfit(x2, t2_shifted, 1)

v_app_true = np.sqrt(1.0 / coeff_true[0])
v_app_shifted = np.sqrt(1.0 / coeff_shifted[0])
t0_app_true = np.sqrt(coeff_true[1])
t0_app_shifted = np.sqrt(coeff_shifted[1])

# Constrained fit: force the line through the true intercept t0_true^2
# and fit only the slope.  This mimics picking at the wrong t0.
slope_biased = np.sum((t2_shifted - t0_true**2) * x2) / np.sum(x2**2)
v_app_constrained = np.sqrt(1.0 / slope_biased)

# Velocity reported in panel (b) if picking is forced to stay at the
# original t0.  We use the theoretical fixed-t0 least-squares value so
# that panels (b) and (c) are consistent.
v_biased = v_app_constrained

# =====================================================================
# Plot
# =====================================================================
fig = plt.figure(figsize=(15, 4.5))
fig.suptitle('How a long-wavelength static biases velocity analysis',
             fontsize=13, y=1.04)

# ---- (a) CMP gather --------------------------------------------------
ax1 = plt.subplot(1, 3, 1)
# Plot shifted gather as wiggles
for k in range(n_offsets):
    amp = np.max(np.abs(gather_shifted[:, k]))
    norm = gather_shifted[:, k] / amp if amp > 0 else gather_shifted[:, k]
    ax1.plot(offsets[k] + norm * 250, t, 'k-', linewidth=0.5)

# Overlay the two traveltime curves
ax1.plot(offsets, t_true, 'k-', linewidth=2,
         label=f'True hyperbola\n($t_0$={t0_true:.2f} s, V={v_true:.0f} m/s)')
ax1.plot(offsets, t_shifted, 'r-', linewidth=2,
         label=f'Shifted hyperbola\n($t_0$={t0_shifted:.2f} s, V={v_true:.0f} m/s)')

ax1.set_xlabel('Offset (m)')
ax1.set_ylabel('Time (s)')
ax1.set_title('(a) CMP gather with static')
ax1.invert_yaxis()
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-100, 2600)

# ---- (b) Semblance spectra -------------------------------------------
ax2 = plt.subplot(1, 3, 2)

# Background: shifted semblance (now V on x-axis, t0 on y-axis)
im = ax2.imshow(semb_shifted, aspect='auto', origin='lower',
                extent=[v_range[0], v_range[-1],
                        t0_range[0], t0_range[-1]],
                cmap='Greys', interpolation='bilinear')

# Overlay true semblance as blue contours
ct = ax2.contour(v_range, t0_range, semb_true,
                 levels=np.linspace(0.3, 1.0, 8),
                 colors='blue', linewidths=1.2, alpha=0.7)

# Mark peaks
ax2.plot(pv_t, pt0_t, 'b*', markersize=12,
         label=f'True peak\n({pv_t:.0f} m/s, {pt0_t:.2f} s)')
ax2.plot(pv_s, pt0_s, 'r*', markersize=12,
         label=f'Shifted peak\n({pv_s:.0f} m/s, {pt0_s:.2f} s)')

# Show the biased pick when t0 is fixed to the original value
ax2.axvline(x=v_biased, color='purple', linestyle='--', linewidth=1.5)
ax2.axhline(y=t0_true, color='purple', linestyle='--', linewidth=1.5)
ax2.plot(v_biased, t0_true, 'mo', markersize=8,
         label=f'Biased pick (fixed $t_0$={t0_true:.2f} s)\nV={v_biased:.0f} m/s')

ax2.set_xlabel('$V_\\mathrm{nmo}$ (m/s)')
ax2.set_ylabel('$t_0$ (s)')
ax2.set_title('(b) Semblance spectra')
ax2.legend(fontsize=7, loc='lower right')
ax2.invert_yaxis()
ax2.text(0.02, 0.98, 'Greys = shifted\nBlue contours = true',
         transform=ax2.transAxes, fontsize=7, ha='left', va='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# ---- (c) t^2 vs x^2 --------------------------------------------------
ax3 = plt.subplot(1, 3, 3)
ax3.plot(x2, t2_true, 'b.', markersize=4, label='True data')
ax3.plot(x2, t2_shifted, 'r.', markersize=4, label='Shifted data')

x2_fit = np.linspace(0, x2.max(), 100)

# True fit
ax3.plot(x2_fit, coeff_true[0] * x2_fit + coeff_true[1],
         'b-', linewidth=2,
         label=f'True fit: V={v_app_true:.0f} m/s, '
               f'$t_0$={t0_app_true:.2f} s')

# Shifted fit (free t0 and V)
ax3.plot(x2_fit, coeff_shifted[0] * x2_fit + coeff_shifted[1],
         'r-', linewidth=2,
         label=f'Shifted fit: V={v_app_shifted:.0f} m/s, '
               f'$t_0$={t0_app_shifted:.2f} s')

# Constrained fit through true t0^2
ax3.plot(x2_fit, slope_biased * x2_fit + t0_true**2,
         'm-', linewidth=2,
         label=f'Fixed-$t_0$ fit: V={v_app_constrained:.0f} m/s, '
               f'$t_0$={t0_true:.2f} s')

# Annotate the slope difference between true and constrained fits
x_annot = 0.55 * x2.max()
ax3.annotate('', xy=(x_annot, coeff_true[0] * x_annot + coeff_true[1]),
             xytext=(x_annot, slope_biased * x_annot + t0_true**2),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
ax3.text(x_annot * 1.05,
         (coeff_true[0] * x_annot + coeff_true[1]
          + slope_biased * x_annot + t0_true**2) / 2,
         '$\\Delta$ slope\n→ velocity bias',
         fontsize=8, color='purple', va='center')

ax3.set_xlabel('$x^2$ (m$^2$)')
ax3.set_ylabel('$t^2$ (s$^2$)')
ax3.set_title('(c) $t^2$ vs $x^2$')
ax3.legend(fontsize=7)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(-2e5, x2.max() * 1.15)

plt.tight_layout()
plt.savefig('figures/term01_lec03/term01_lec03_statics_velocity_bias.png',
            dpi=150, bbox_inches='tight')
plt.close()

# =====================================================================
# Report
# =====================================================================
print(f"True velocity:                {v_true:.0f} m/s")
print(f"True t0:                      {t0_true:.3f} s")
print(f"Static shift:                 {static_shift*1000:.0f} ms")
print(f"Shifted t0:                   {t0_shifted:.3f} s")
print()
print(f"Free fit to shifted data:     V={v_app_shifted:.0f} m/s, "
      f"t0={t0_app_shifted:.3f} s  (velocity correct, t0 wrong)")
print(f"Fixed-t0 fit to shifted data: V={v_app_constrained:.0f} m/s, "
      f"t0={t0_true:.3f} s  (velocity biased)")
print()
print("Figure saved: figures/term01_lec03/term01_lec03_statics_velocity_bias.png")
