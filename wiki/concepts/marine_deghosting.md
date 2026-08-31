---
title: Marine deghosting
status: draft
tags: [deghosting, ghost, notch, marine, streamer, broadband, upgoing, downgoing]
related_sources:
  - cgg_odt04_deconvolution_part1_wavelet
  - cgg_odt04_deconvolution_part2_signature
  - amundsen_zhou_2013_deghosting
  - li_et_al_2020_sparse_deghosting
  - ghosh_2000_ghost_deconvolution
  - lindsey_1960_ghost_elimination
  - monk_2020_broadband_seismic
---

# Marine Deghosting

## Definition

**Deghosting** is the process of removing the effect of source and receiver ghosts from marine seismic data. Ghosts are near-surface multiples caused by reflection of seismic energy at the sea surface (water-air interface). They create spectral notches that limit the usable bandwidth and degrade resolution.

Deghosting is equivalent to **wavefield separation**: decomposing the recorded wavefield into upgoing (primary) and downgoing (ghost) components, then keeping only the upgoing wavefield.

## Ghost Physics

### Source Ghost

When the airgun array fires, energy propagates in all directions. The upgoing energy reflects off the sea surface and travels back down, arriving after the direct downgoing wavelet.

**Delay time:**
$$\Delta t_s = \frac{2d_s}{v_w}$$

where:
- $d_s$ = source depth (typically 5–8 m)
- $v_w$ = water velocity (~1500 m/s)

**Polarity:** The sea-surface reflection coefficient is $R \approx -1$ (pressure release boundary), so the source ghost has **opposite polarity** to the primary.

### Receiver Ghost

The upgoing primary energy reflects off the sea surface and travels back down, arriving at the receiver after the primary.

**Delay time:**
$$\Delta t_r = \frac{2d_r}{v_w}$$

where:
- $d_r$ = receiver depth (typically 6–10 m for conventional streamers)

**Polarity:** Again, $R \approx -1$, so the receiver ghost has opposite polarity to the primary.

### Ghost Notch Frequencies

The interference between primary and ghost creates **notches** in the amplitude spectrum at frequencies:

$$f_n = \frac{n \cdot v_w}{2d}, \quad n = 0, 1, 2, 3, \dots$$

For a receiver at 6 m depth:
- $n = 0$: $f_0 = 0$ Hz (DC notch — all low frequencies lost)
- $n = 1$: $f_1 = 125$ Hz
- $n = 2$: $f_2 = 250$ Hz
- etc.

**Key insight:** The zero-frequency notch means that **all frequencies below the first non-zero notch are severely attenuated**. For a 6 m streamer, this means frequencies below ~125 Hz are degraded, which is why conventional data lacks low-frequency content.

### Angle Dependence

The ghost delay depends on the ray angle $\theta$ (measured from vertical):

$$\Delta t(\theta) = \frac{2d \cos\theta}{v_w}$$

At non-zero offset, the ray path is oblique, so $\cos\theta < 1$ and the delay is shorter. This means:
- The notch frequency **increases with offset**
- A 1D (vertical) deghosting operator will **not work at all offsets**
- Modern deghosting methods must account for angle-dependent ghost delays

### Ghost Filter in Frequency Domain

The ghost effect can be modeled as a filter in the frequency-wavenumber domain:

$$G(k_x, k_y, k, z) = 1 - R_0 \exp(2i k_z z)$$

where:
- $k_x, k_y$ = horizontal wavenumbers
- $k = \omega/c$ = wavenumber
- $k_z = \sqrt{k^2 - k_x^2 - k_y^2}$ = vertical wavenumber
- $z$ = receiver depth
- $R_0 \approx 1$ = sea-surface reflection coefficient

For vertical incidence ($k_x = k_y = 0$):

$$G(k, z) = 1 - \exp(2ikz)$$

The amplitude spectrum is:

$$|G| = 2|\sin(kz)|$$

The zeros of the sine function correspond to the notch frequencies.

## Deghosting Methods

### 1. Classical 1D Designature

**Approach:** Design a deterministic inverse filter from the modeled ghost operator, assuming vertical ray paths.

**Method:**
1. Model the ghost filter $G(f)$ for a given depth
2. Compute the inverse filter $1/G(f)$
3. Apply pre-whitening to stabilize the inversion at notches
4. Apply the filter to the data

**Limitations:**
- Assumes vertical incidence only
- Fails at non-zero offset (ghost delay varies with angle)
- Amplifies noise at notch frequencies
- Rarely used alone in modern processing

**Status:** Mostly for QC and understanding; not suitable for production data.

### 2. Bootstrap Deghosting (Tau-P Domain)

**Approach:** Transform data to tau-p (intercept time – ray parameter) domain, where the ghost becomes a simple time shift that can be inverted.

**Method:**
1. Forward tau-p transform: $d(t, x) \to D(\tau, p)$
2. In tau-p, the ghost is a time shift: $D(\tau, p) = U(\tau, p) - U(\tau - \Delta t(p), p)$
3. Solve the inverse problem: estimate $U(\tau, p)$ from $D(\tau, p)$
4. Inverse tau-p transform: $U(\tau, p) \to u(t, x)$

**Advantages:**
- Accounts for angle-dependent ghost delays (each ray parameter $p$ has its own $\Delta t$)
- Can handle variable cable depth (with modifications)
- Can be combined with demultiple (water-layer reverberations)
- Robust and stable

**Limitations:**
- Computationally expensive (inverse problem)
- Requires accurate velocity model and cable depth
- Tau-p transform assumes laterally homogeneous medium

**References:**
- [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md) — detailed workflow
- [Amundsen (1993)](../sources/amundsen_zhou_2013_deghosting.md) — Green's theorem approach

### 3. Dual-Sensor (PZ) Deghosting

**Approach:** Record both pressure (hydrophone) and particle velocity (geophone) data. Exploit the polarity difference between ghosts in the two sensors.

**Physics:**
- Hydrophone (pressure sensor): ghost has **opposite polarity** to primary
- Geophone (velocity sensor): ghost has **same polarity** as primary

**Method:**
1. Record $P(t)$ (pressure) and $V(t)$ (particle velocity)
2. Scale and sum: $U(t) = P(t) + \alpha V(t)$
3. The scaling factor $\alpha$ is chosen so that ghosts cancel:
   - Primary in $P$: $+p(t)$
   - Ghost in $P$: $-p(t - \Delta t)$
   - Primary in $V$: $+v(t)$
   - Ghost in $V$: $+v(t - \Delta t)$
   - Sum: $U(t) = [p(t) + \alpha v(t)] - [p(t - \Delta t) - \alpha v(t - \Delta t)]$
   - If $\alpha$ is chosen correctly, the ghost terms cancel

**Advantages:**
- Simple, robust, and effective
- No inverse problem needed
- Works for all offsets (no angle-dependence issue)
- Can recover frequencies below the first notch

**Limitations:**
- Requires dual-sensor acquisition (GeoStreamer, Sentinel, etc.)
- Geophone data has lower S/N at low frequencies (flow noise, vibration noise)
- Summing is typically done only above ~10 Hz; below that, other methods are needed

**Commercial systems:**
- **GeoStreamer® (PGS)** — hydrophones + geophones
- **Sentinel® (Sercel)** — similar dual-sensor concept
- **IsoMetrix (Schlumberger)** — multi-component (hydrophones + accelerometers)

### 4. Variable-Depth Streamer

**Approach:** Tow the streamer at varying depths (e.g., 6–10 m) so that different cable segments have different ghost notch frequencies. Processing combines data from all depths to fill in the notches.

**Physics:**
- Different depths → different $\Delta t$ → different notch frequencies
- "Notch diversity" allows reconstruction of the full bandwidth

**Method:**
1. Record data at varying depths along the cable
2. For each depth segment, model the ghost operator
3. Invert for the ghost-free wavefield using all depths
4. Combine to produce broadband output

**Advantages:**
- Achieves true broadband (6+ octaves)
- Recovers low frequencies (below the conventional notch)
- No dual-sensor hardware needed

**Limitations:**
- Requires specialized acquisition (variable-depth cable control)
- Processing is more complex
- Cable depth must be accurately measured

**Commercial systems:**
- **BroadSeis™ (CGG)** — variable-depth streamer (6–10 m)

### 5. Sparse Deghosting

**Approach:** Use sparsity constraints in the frequency-slowness domain to separate upgoing and downgoing wavefields.

**Method:**
1. Transform data to frequency-slowness domain: $d(t, x) \to D(f, p)$
2. Model the ghost effect as a linear operator: $D = G \cdot U$
3. Solve the inverse problem with sparsity constraint:
   $$\min_U \|D - G \cdot U\|_2^2 + \lambda \|U\|_1$$
4. Use fast iterative shrinkage-thresholding algorithm (FISTA)

**Advantages:**
- Simultaneous deghosting and denoising
- Robust to noise
- Can handle complex ghost models

**Limitations:**
- Computationally expensive
- Requires careful parameter tuning (sparsity weight $\lambda$)

**References:**
- [Li et al. (2020)](../sources/li_et_al_2020_sparse_deghosting.md) — detailed method

### 6. Low-Frequency Deghosting (Amundsen & Zhou, 2013)

**Approach:** Trace-by-trace operator that recovers low frequencies using the integrated and differentiated pressure field.

**Method:**
1. Compute the time integral of the pressure field: $\int P(t) dt$
2. Compute the time derivative of the pressure field: $\frac{dP(t)}{dt}$
3. Combine with appropriate scaling:
   $$U_{\text{deghosted}}(t) = P(t) + \alpha \int P(t) dt + \beta \frac{dP(t)}{dt}$$
4. The scaling factors $\alpha$ and $\beta$ are chosen to cancel the ghost at low frequencies

**Advantages:**
- Simple, fast, and effective for low frequencies
- Works with conventional streamer data (no special hardware)
- Can recover frequencies below the first notch

**Limitations:**
- Only recovers low frequencies (not full deghosting)
- Does not fill all notches (higher-frequency notches remain)
- Best used as a complement to other deghosting methods

**References:**
- [Amundsen & Zhou (2013)](../sources/amundsen_zhou_2013_deghosting.md) — detailed method and theory

## Deghosting Workflow

### Typical Marine Processing Sequence

1. **De-bubble** — remove source bubble oscillation
2. **Designature** — compress source signature (zero-phase or spiking)
3. **Deghost** — remove source and receiver ghosts
4. **Q-compensation** — correct for absorption losses
5. **Predictive deconvolution** — compress wavelet and attenuate multiples
6. **Migration** — image the subsurface

### QC Metrics

After deghosting, check:
- **Amplitude spectra** — are ghost notches filled?
- **Low-frequency content** — are frequencies below the conventional notch recovered?
- **Side lobe level** — are wavelet side lobes suppressed?
- **Well tie** — does the broadband data improve the tie to well data?

## Practical Considerations

### Choice of Method

- **Conventional streamer (fixed depth):** Bootstrap or sparse deghosting
- **Dual-sensor streamer:** PZ deghosting (simple and robust)
- **Variable-depth streamer:** Variable-depth deghosting (BroadSeis)
- **Legacy data:** Low-frequency deghosting (trace-by-trace, no special acquisition)

### Trade-offs

- **More aggressive deghosting** → more bandwidth recovered, but may amplify noise
- **Conservative deghosting** → less bandwidth, but better S/N
- **Dual-sensor** → robust but requires special hardware
- **Bootstrap/sparse** → flexible but computationally expensive

### Integration with Demultiple

Ghosts are a type of multiple (near-surface multiples). Deghosting can be integrated with demultiple:
- **Bootstrap deghosting** can be extended to remove water-layer reverberations
- **SRME (Surface-Related Multiple Elimination)** can be applied after deghosting
- **Joint deghosting-demultiple** — solve for both simultaneously

## Related Concepts

- [Broadband seismic](broadband_seismic.md) — overview of broadband concepts and benefits
- [Source signature and designature](source_signature_designature.md) — source wavelet components
- [Seismic wavelet](seismic_wavelet.md) — wavelet properties and effects
- [Predictive deconvolution](predictive_deconvolution.md) — wavelet compression and demultiple

## Sources

- [CGG ODT04 Part 1](../sources/cgg_odt04_deconvolution_part1_wavelet.md) — ghost physics and wavelet components
- [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md) — designature and deghosting workflows
- [Amundsen & Zhou (2013)](../sources/amundsen_zhou_2013_deghosting.md) — low-frequency deghosting method
- [Li et al. (2020)](../sources/li_et_al_2020_sparse_deghosting.md) — sparse deghosting and denoising
- [Ghosh (2000)](../sources/ghosh_2000_ghost_deconvolution.md) — ghost filter theory
- [Lindsey (1960)](../sources/lindsey_1960_ghost_elimination.md) — early ghost elimination methods
- [Monk (2020)](../sources/monk_2020_broadband_seismic.md) — broadband acquisition and processing overview
