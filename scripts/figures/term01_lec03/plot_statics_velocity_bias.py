"""
Demonstrate how a long-wavelength static shift biases velocity analysis.

Key physics:
  A static Δt shifts the entire trace uniformly:
    t_shifted(x) = sqrt(t0^2 + x^2/V^2) + Δt
  This is NOT exactly hyperbolic. Fitting t^2 = t0'^2 + x^2/V_app^2
  to the shifted times yields a biased velocity V_app ≠ V_true.

Three panels:
  (a) CMP gather with true hyperbola and constant-shifted hyperbola.
  (b) Semblance spectra for both cases — the shifted peak lies at a
      different (t0, V) because the shifted data is not perfectly hyperbolic.
  (c) t² vs x² plot showing different slopes (→ different apparent velocity).

Undergraduate seismic data processing — Term 1 Lecture 03.
"""

import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# Parameters
# =====================================================================
dt = 0.002
t_max = 2.5
t = np.arange(0, t_max, dt)
nt = len(t)

n_offsets = 31
offsets = np.linspace(0, 2500, n_offsets)      # m, include zero for clarity
x2 = offsets ** 2

t0_true = 0.4           # zero-offset time (s)
v_true = 2000.0         # true NMO velocity (m/s)
static_shift = 0.1      # long-wavelength static (s)

# =====================================================================
# Traveltime curves — physically correct
# =====================================================================
t_true = np.sqrt(t0_true**2 + (offsets / v_true)**2)

# The static adds a constant time to the true arrival time.
# Squaring does NOT yield a perfect hyperbola.
t_shifted_linear = t_true + static_shift
# For consistency with the standard velocity-analysis model we examine
# t² vs x².  For the shifted data:
t2_shifted = t_shifted_linear ** 2
t2_true = t_true ** 2

# =====================================================================
# Semblance velocity spectrum — for the shifted gather
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

# Create the shifted gather (one event with static applied)
gather_shifted = make_gather(t_shifted_linear, offsets, t, f0=25.0)

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

t0_range = np.linspace(0.2, 1.0, 300)
v_range = np.linspace(1400, 2600, 300)

semb_shifted = semblance_spectrum(gather_shifted, offsets,
                                  t0_range, v_range, dt, half_win=4)

# True data semblance for comparison (pure hyperbola)
gather_true = make_gather(t_true, offsets, t, f0=25.0)
semb_true = semblance_spectrum(gather_true, offsets,
                               t0_range, v_range, dt, half_win=4)

# Peak locations
def peak_rc(semb, t0_range, v_range):
    """Return (t0, V) of maximum semblance."""
    idx = np.unravel_index(np.argmax(semb), semb.shape)
    return t0_range[idx[0]], v_range[idx[1]]

pt0_t, pv_t = peak_rc(semb_true, t0_range, v_range)
pt0_s, pv_s = peak_rc(semb_shifted, t0_range, v_range)

# =====================================================================
# Least-squares fit of t² = a + b·x²  (b = 1/V_app²)
# =====================================================================
coeff_true = np.polyfit(x2, t2_true, 1)
coeff_shifted = np.polyfit(x2, t2_shifted, 1)

v_app_true = np.sqrt(1.0 / coeff_true[0])
v_app_shifted = np.sqrt(1.0 / coeff_shifted[0])
t0_app_true = np.sqrt(coeff_true[1])
t0_app_shifted = np.sqrt(coeff_shifted[1])

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
    if amp > 0:
        norm = gather_shifted[:, k] / amp
    else:
        norm = gather_shifted[:, k]
    ax1.plot(offsets[k] + norm * 250, t, 'k-', linewidth=0.5)

# Overlay the two traveltime curves
ax1.plot(offsets, t_true, 'k-', linewidth=2, label='True hyperbola')
ax1.plot(offsets, t_shifted_linear, 'r-', linewidth=2,
         label=f'Shifted (static +{static_shift*1000:.0f} ms)')

ax1.set_xlabel('Offset (m)')
ax1.set_ylabel('Time (s)')
ax1.set_title('(a) CMP gather with static')
ax1.invert_yaxis()
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-100, 2600)

# ---- (b) Semblance spectra -------------------------------------------
ax2 = plt.subplot(1, 3, 2)
# Background: shifted semblance
im = ax2.imshow(semb_shifted.T, aspect='auto', origin='lower',
                 extent=[t0_range[0], t0_range[-1],
                         v_range[0], v_range[-1]],
                 cmap='Greys', interpolation='bilinear')
# Overlay true semblance as contours
ct = ax2.contour(t0_range, v_range, semb_true.T,
                  levels=np.linspace(0.3, 1.0, 8),
                  colors='blue', linewidths=1.2, alpha=0.7)

# Mark peaks
ax2.plot(pt0_t, pv_t, 'b*', markersize=12,
         label=f'True peak\n({pt0_t:.2f} s, {pv_t:.0f} m/s)')
ax2.plot(pt0_s, pv_s, 'r*', markersize=12,
         label=f'Shifted peak\n({pt0_s:.2f} s, {pv_s:.0f} m/s)')

ax2.set_xlabel('$t_0$ (s)')
ax2.set_ylabel('$V_\\mathrm{nmo}$ (m/s)')
ax2.set_title('(b) Semblance spectra')
ax2.legend(fontsize=7, loc='upper left')
ax2.text(0.98, 0.02, 'Greys = shifted\nBlue contours = true',
         transform=ax2.transAxes, fontsize=7, ha='right', va='bottom',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# ---- (c) t² vs x² ----------------------------------------------------
ax3 = plt.subplot(1, 3, 3)
ax3.plot(x2, t2_true, 'b.', markersize=4, label='True data')
ax3.plot(x2, t2_shifted, 'r.', markersize=4, label='Shifted data')

x2_fit = np.linspace(0, x2.max(), 100)
# True fit
ax3.plot(x2_fit, coeff_true[0] * x2_fit + coeff_true[1],
         'b-', linewidth=2,
         label=f'True fit: 1/V²={coeff_true[0]:.3e}\n'
               f'  V_app={v_app_true:.0f} m/s')
# Shifted fit
ax3.plot(x2_fit, coeff_shifted[0] * x2_fit + coeff_shifted[1],
         'r-', linewidth=2,
         label=f'Shifted fit: 1/V²={coeff_shifted[0]:.3e}\n'
               f'  V_app={v_app_shifted:.0f} m/s')
# Annotate the slope difference
ax3.annotate('', xy=(3.5e6, coeff_true[0]*3.5e6+coeff_true[1]),
             xytext=(3.5e6, coeff_shifted[0]*3.5e6+coeff_shifted[1]),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=2),
             fontsize=9)
ax3.text(3.6e6, (coeff_true[0]+coeff_shifted[0])/2*3.5e6
         + (coeff_true[1]+coeff_shifted[1])/2,
         f'$\\Delta$ slope\n→ bias',
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
print(f"True velocity:            {v_true:.0f} m/s")
print(f"True t0:                  {t0_true:.3f} s")
print(f"Static shift:             {static_shift*1000:.0f} ms")
print()
print(f"Shifted data fitted V_app: {v_app_shifted:.0f} m/s  "
      f"(bias = {v_app_shifted - v_true:+.0f} m/s, "
      f"{((v_app_shifted-v_true)/v_true)*100:+.1f}%)")
print(f"Shifted data fitted t0_app: {t0_app_shifted:.3f} s  "
      f"(bias = {t0_app_shifted - t0_true:+.3f} s)")
print()
print("Figure saved: figures/term01_lec03/term01_lec03_statics_velocity_bias.png")
