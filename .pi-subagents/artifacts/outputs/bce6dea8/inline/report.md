# Layer Replacement Figure — Implementation Summary

## Changes

### `scripts/figures/term01_lec03/plot_layer_replacement.py` — rewritten

**Before (old):** 2×2 grid showing a dipping horizon with a constant-velocity depth conversion. The model used a time-domain push-down anomaly on a dipping background, with a single constant interval velocity (2200 m/s) for everything. The depth smoothing partially corrected the time push-down, but the underlying physics was about distorting a time horizon, not about velocity-model uncertainty.

**After (new):** 3×2 grid showing a physically realistic layer-replacement workflow:

| Panel | Content |
|-------|---------|
| (a) | Flat reflector at 500 m depth + Gaussian low-velocity zone (1800 m/s min, 2200 m/s background) |
| (b) | Three velocity profiles: true (\(v_{\rm true}\)), velocity-analysis estimate (\(v_{\rm int}\)), replacement velocity (\(v_{\rm rep}=2200\)) |
| (c) | Raw traveltimes \(t_{\rm obs}=2z_0/v_{\rm true}\) — 100.9 ms push-down |
| (d) | Depth estimate \(z_{\rm est}=\frac12 v_{\rm int} t_{\rm obs}\) and geologically smoothed \(z_{\rm smooth}\) |
| (e) | Corrected \(t_{\rm new}=2z_{\rm smooth}/v_{\rm rep}\) (26.3 ms range) vs raw \(t_{\rm obs}\) (100.9 ms range) |
| (f) | Static correction \(\Delta t = t_{\rm obs} - t_{\rm new}\) (81.7 ms peak, 0 ms at edges) |

### `figures/term01_lec03/term01_lec03_layer_replacement.png` — regenerated

Replaced the old 4-panel figure (119 KB) with the new 6-panel figure (330 KB).

## Key improvements over old figure

1. **Physically correct model**: flat reflector at constant depth, velocity anomaly causes the time distortion
2. **Separate interval vs replacement velocity**: mimics real workflow where velocity analysis gives smooth estimates and the replacement velocity is the background value
3. **No overcorrection at edges**: static is zero where the true velocity equals the replacement velocity
4. **7-step workflow** (condensed to 6 panels) is clearly traceable from model → statics
5. **Colourblind-friendly palette** (Tol palette variant)

## Assumptions

- The replacement velocity is taken as the background velocity (2200 m/s). In practice this would come from well control or regional knowledge.
- `v_int` is a Gaussian-smoothed version of `v_true` (sigma=10 samples ≈ 333 m). This simulates what velocity analysis can resolve.
- Depth smoothing uses a Gaussian filter with sigma=5 samples ≈ 167 m.

## Numerical validation

| Quantity | Value |
|----------|-------|
| True velocity at center | 1800 m/s |
| True velocity at edges | 2200 m/s |
| v_int (interval estimate) at center | 1894 m/s |
| Raw traveltime range | 100.9 ms |
| Corrected traveltime range | 26.3 ms |
| Improvement factor | 3.8× |
| Static at anomaly center | 81.7 ms |
| Static at edges | 0.0 ms (no overcorrection) |
| z_est depth range | 490.5–525.9 m |
| z_smooth depth range | 492.2–521.1 m |
