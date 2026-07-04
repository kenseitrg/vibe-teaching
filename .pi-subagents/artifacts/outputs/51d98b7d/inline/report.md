# Layer-replacement figure refinement — acceptance report

## Changes made

**File:** `scripts/figures/term01_lec03/plot_layer_replacement.py`

### 1. Random velocity component — zero-mean, short-wavelength, high-pass filtered
- Reduced base smoothing kernel from `sigma=5` to `sigma=3` (correlation length ~75 m instead of ~125 m)
- Added high-pass filter: subtract `gaussian_filter1d(v_random, sigma=30)` to remove any residual long-wavelength trend
- Force exact zero mean: `v_random = v_random - np.mean(v_random)`
- Reduced amplitude from 35 m/s to 22 m/s (smaller wiggles, more realistic)

### 2. v_int = v_smooth exactly
- Velocity analysis recovers the smooth component with no contamination from random variations

### 3. Depth conversion and smoothing
- `z_est = 0.5 * v_int * t_obs = z0 * v_smooth / (v_smooth + v_random)` — smooth velocity component cancels out, leaving only small random wiggles (RMS 5.7 m)
- `z_smooth = gaussian_filter1d(z_est, sigma=25)` — strong smoothing removes random wiggles (RMS 1.0 m, very close to flat)
- Reduced y-limits on panel (d) from ±30 m to ±10 m to highlight the small residual variations

### 4. Annotation in panel (c) — refined
- Replaced single annotation with two annotations:
  - "Anomaly creates push-down anomaly" pointing to the main trough
  - "Random wiggles from short-wavelength velocity variations" pointing to a representative wiggle
- Both placed more carefully to avoid clutter

## Diagnostics

```
v_random     std:   22.0 m/s    ✓ small amplitude, short-wavelength
v_int        = v_smooth        ✓ velocity analysis recovers smooth part
t_obs        range: 90.6 ms    ✓ large raw range
t_new        range:  3.2 ms    ✓ much flatter than raw (target < 15 ms)
z_est        RMS:    5.7 m     ✓ almost flat (random component only)
z_smooth     RMS:    1.0 m     ✓ very close to true depth
static       range: 89.6 ms    ✓ matches t_obs range (push-down removed)
```

## Validation

The figure was regenerated with `uv run python scripts/figures/term01_lec03/plot_layer_replacement.py` and the PNG was updated at `figures/term01_lec03/term01_lec03_layer_replacement.png` (758 KB, updated timestamp).
