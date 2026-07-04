# Layer Replacement Figure — Revision Summary

## Task
Revised `scripts/figures/term01_lec03/plot_layer_replacement.py` to use a velocity model with
smooth (recoverable) + random (unrecoverable) components, per instructor's specification.

## Chosen parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `v0` | 2000 m/s | Background velocity |
| `dv_gauss` | -160 m/s | Gaussian low-velocity anomaly amplitude |
| `sigma_gauss` | 800 m | Gaussian anomaly width |
| `v_smooth` | Gaussian + 40*sin(2πx/3500) | Recoverable smooth trend |
| `v_random` | ±35 m/s, correlation ~125 m | Short-wavelength noise (unrecoverable) |
| `v_int` | = v_smooth | Velocity analysis recovers smooth part |
| `v_rep` | 1945 m/s | Mean of v_int (replacement velocity) |
| `z_smooth sigma` | 25 (~625 m correlation) | Aggressive geological smoothing |

## Resulting ranges

| Quantity | Value | Target | Status |
|----------|-------|--------|--------|
| `t_obs` range | 108.6 ms | 80–120 ms | ✅ |
| `t_new` range | 10.7 ms | < 20 ms | ✅ |
| `z_est` RMS | 9.5 m | ~10 m | ✅ |
| `z_smooth` RMS | 4.7 m | < 5 m | ✅ |
| Static range | 98.0 ms | — | — |

## Files changed
- `scripts/figures/term01_lec03/plot_layer_replacement.py` — rewritten
- `figures/term01_lec03/term01_lec03_layer_replacement.png` — regenerated (717 KB)

## Validation
Script runs cleanly with no warnings or errors.

## Residual risks
- The 6-panel layout uses a tight grid; at small display sizes the subplot labels may be hard to read.
- Panel (d) y-limits are ±30 m around z0 to show wiggles — if data changes significantly, limits may need adjustment.
- The `coolwarm` colormap is colourblind-friendly but diverges: cold (blue) = low velocity, warm (red) = high velocity.
