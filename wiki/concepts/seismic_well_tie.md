---
title: Seismic well tie
status: draft
sources:
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
  - yilmaz_2001_seismic_data_analysis_deconvolution
  - white_1997_accuracy_of_well_ties
  - walden_white_1998_seismic_wavelet_estimation
  - carvajal_2023_well_tie_tutorial
tags: [well-tie, synthetic-seismogram, wavelet, reflectivity, phase, correlation, QC, Roy-White, time-depth]
---

# Seismic well tie

A seismic well tie links the depth domain of well logs to the time domain of seismic data. It is the main instrument of interpretation-supervised processing (ИСО / WDS) because it compares what the well says the earth should look like with what the seismic data actually show.

## What is needed

- A **sonic log** (interval velocity versus depth) to convert depth to two-way time.
- A **density log** to compute acoustic impedance.
- Optional: a **checkshot survey** to calibrate the time-depth relationship independently of the sonic log.
- A seismic trace or small window of traces at the well location.
- An estimated wavelet.

## Building the synthetic seismogram

1. **Compute acoustic impedance** from velocity and density:

$$
Z(t) = \rho(t) \, v(t)
$$

2. **Compute the normal-incidence reflection coefficient series**:

$$
R(t) = \frac{Z(t+\Delta t) - Z(t)}{Z(t+\Delta t) + Z(t)}
$$

3. **Estimate a wavelet** from the seismic data or from a deterministic model.
4. **Convolve** the reflectivity series with the wavelet to obtain the synthetic seismogram:

$$
s(t) = w(t) * R(t)
$$

5. **Compare** the synthetic with the seismic trace at the well location and estimate the time shift, phase rotation, and correlation coefficient.

## Time-depth conversion

The sonic log gives interval velocity $v(z)$ in depth. Two-way time is obtained by integrating slowness:

$$
t(z) = 2 \int_0^z \frac{d\zeta}{v(\zeta)}
$$

Checkshots provide independent time-depth pairs and are used to correct the sonic log for drift, cycle skipping, or errors in the borehole trajectory.

## Deterministic vs statistical wavelet

- **Deterministic wavelet:** derived from the known source signature, ghost, bubble, instrument response, and propagation effects. It requires accurate knowledge of the acquisition system.
- **Statistical wavelet:** estimated from the seismic data itself, often by assuming a minimum-phase wavelet and a white reflectivity.

### The Roy-White method

The Roy-White method is a statistical approach (White, 1980; Walden and White, 1984, 1998) that balances two competing requirements:

- A **short wavelet** is smooth and less likely to fit noise, but it may not capture the true phase.
- A **wide bandwidth** gives a more reliable phase estimate, but it requires a longer wavelet and may be unstable if the signal-to-noise ratio is poor.

White (1997) emphasizes that the user should look for a compact wavelet with a high, stable correlation coefficient rather than maximizing correlation at all costs, and that the analysis bandwidth should be well below the data bandwidth (typically the ratio of wavelet length to data segment duration should be < 0.5). Walden and White (1998) formulate the estimation in the frequency domain using multiple coherence to correct for noise in both the input reflectivity and the output seismic trace.

## Sources

- [White (1997) — The accuracy of well ties](../sources/white_1997_accuracy_of_well_ties.md)
- [Walden & White (1998) — Seismic wavelet estimation](../sources/walden_white_1998_seismic_wavelet_estimation.md)
- [Carvajal et al. (2023) — Well tie tutorial](../sources/carvajal_2023_well_tie_tutorial.md)

## Metrics of a good tie

- **Correlation coefficient** between synthetic and seismic. High values (typically above 0.7) indicate a good match.
- **Time shift:** the vertical shift needed to align the synthetic with the seismic. It often reveals errors in the velocity model or checkshot calibration.
- **Phase rotation:** the residual phase difference between the seismic wavelet and the synthetic. After proper deconvolution the wavelet should be near zero phase.
- **Wavelet shape and bandwidth:** a compact, stable wavelet is more useful than a long, noisy one.
- **Misfit analysis:** a time- or frequency-varying misfit can reveal residual multiples, tuning effects, or incorrect Q-compensation.

## Common pitfalls

- **Cycle skipping.** A strong reflection can be misaligned by one or more periods if the initial time shift is wrong.
- **Phase ambiguity.** Without well control, the seismic phase can be rotated by 180° without changing the correlation if the reflectivity is symmetric.
- **Wavelet non-stationarity.** A single wavelet may not be valid across the whole trace if Q or processing has changed the wavelet with time.
- **Log quality.** Bad sonic or density log intervals, washouts, or mis-tied depth scales produce wrong reflectivity.
- **Over-optimization.** Maximizing correlation can force the wavelet to fit noise or multiples rather than the true signal.

## Uses in processing QC

- Validate velocity models and time-depth conversion.
- Check that deconvolution and Q-compensation have produced a sensible wavelet.
- Detect multiples or other coherent noise that corrupt the match.
- Provide a wavelet for subsequent inversion or reservoir characterization.
- Establish the phase of the seismic data (zero-phase, minimum-phase, or mixed).

## Related concepts

- [Seismic wavelet](seismic_wavelet.md)
- [Deterministic deconvolution](deterministic_deconvolution.md)
- [Statistical deconvolution](statistical_deconvolution.md)
- [Seismic velocities](seismic_velocities.md)
- [Seismic processing QC](seismic_processing_qc.md)
- [Surface-consistent amplitude correction](surface_consistent_amplitude.md)
- [AVO analysis](avo_analysis.md)
