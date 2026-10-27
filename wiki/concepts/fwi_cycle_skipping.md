---
title: Cycle skipping in FWI
status: draft
sources:
  - jones2019_fwi_mechanics_tutorial
  - metivier2026_fwi_nonconvexity_review
  - pratt1999_frequency_domain_fwi
  - zhang2015_land_data_fwi
tags: [fwi, nonlinearity, cycle-skipping, local-minima, misfit, frequency-continuation]
---

# Cycle skipping in FWI

**Cycle skipping** (half-cycle skipping) is the failure mode of waveform inversion when the starting model predicts event arrival times with an error exceeding **half the dominant period**. The least-squares misfit then decreases by matching the predicted wavelet to the *wrong cycle* of the observed wavelet, and the optimization converges to a spurious **local minimum**.

## Mechanism

- Seismic wavelets oscillate: the L2 residual $\|d_\text{obs} - d_\text{cal}\|^2$ as a function of a time-shift error is oscillatory, with local minima at shifts ≈ ±1 period even though the global minimum sits at zero shift.
- If the starting-model time error < T/2, downhill paths lead to the global minimum; if > T/2, the nearest local minimum is the wrong-cycle one. Criterion (Pratt 1999): **starting model must predict waveforms within about half a wavelength/period.**
- Lower frequency → longer period T → larger tolerated time error and smoother (less oscillatory) misfit. Half a period at 2 Hz = 250 ms tolerance; at 20 Hz = 25 ms.

## Mitigations (per the Métivier–Brossier taxonomy)

1. **Multiscale / frequency continuation** (Bunks 1995): invert low frequencies first, then add higher batches; time-windowing (early arrivals first) is the same relaxation idea.
2. **Better starting models:** ray tomography, WEMVA/gather flattening, interpretation-guided models.
3. **Misfit replacements** that behave convexly under large time shifts:
   - cross-correlation / traveltime-shift residuals (Luo & Schuster 1991; "adjustive FWI"),
   - adaptive waveform inversion (AWI): matching filter should become a spike (Warner & Guasch),
   - instantaneous phase / dynamic time warping / optimal transport (OT),
   - deconvolution-based residuals.
4. **Extended formulations:** wavefield reconstruction inversion (WRI) / extended source; extended reflectivity (MVA/FWIME/RWI) — add degrees of freedom that let the data be fit with an imperfect model, with convex penalties pulling the extension to zero.
5. **Acquire/encourage low frequencies:** broadband sources (<2–3 Hz) make the criterion easy; essential for subsalt FWI.

## Land specifics

Short offsets + missing low frequencies → diving waves absent/unusable → reflection FWI from gradient starting models is cycle-skipped by construction (Zhang & Dai 2015 Fig. 1); phase-deviation objectives and WEMVA starting models are the standard work-arounds.

## Diagnostic

Compare observed vs modelled shot gathers at the first iterations: if events are shifted by more than half a wiggle, FWI is cycle-skipped; fix the starting model or change the misfit before iterating.
