---
title: Broadband seismic
status: draft
tags: [broadband, bandwidth, resolution, octaves, deghosting, low-frequency]
related_sources:
  - monk_2020_broadband_seismic
  - amundsen_zhou_2013_deghosting
  - li_et_al_2020_sparse_deghosting
  - cgg_odt04_deconvolution_part2_signature
---

# Broadband Seismic

## Definition

Broadband seismic data refers to seismic recordings with significantly extended frequency bandwidth compared to conventional data. Modern broadband acquisition and processing aim for **6+ octaves** of usable bandwidth (e.g., 1–64 Hz or 3–192 Hz), compared to the typical 2–3 octaves (e.g., 10–60 Hz) of conventional streamer data.

## Key Concepts

### Bandwidth and Resolution

The temporal resolution of seismic data is controlled by the **wavelet lobe width**, which is inversely proportional to the bandwidth:

$$L_w \propto \frac{2}{f_{\max} - f_{\min}}$$

where $f_{\max}$ and $f_{\min}$ are the upper and lower frequency limits.

**Critical insight:** Resolution depends on the **average frequency** (bandwidth), not just the maximum frequency. A wavelet with 10–100 Hz bandwidth has better resolution than one with 50–100 Hz bandwidth, even though both have the same $f_{\max}$.

### Octaves

Bandwidth is measured in **octaves** (factors of 2 in frequency):
- 1 octave: 10–20 Hz or 20–40 Hz
- 2 octaves: 10–40 Hz
- 3 octaves: 10–80 Hz
- 6 octaves: 1–64 Hz or 3–192 Hz

Each octave doubles the frequency range. More octaves = better resolution and improved wavelet shape (lower side lobes).

### Wavelet Isolation

Low frequencies control **wavelet isolation** (side lobe amplitude). With sufficient low-frequency content (6+ octaves), the wavelet becomes sharp and impulsive with minimal side lobes, making it easier to:
- Resolve thin beds
- Track events across faults
- Identify subtle impedance variations
- Improve AVO and inversion accuracy

### Ghost Notches

In conventional marine streamer data, the **receiver ghost** creates spectral notches at frequencies:

$$f_n = \frac{n \cdot v_w}{2d}, \quad n = 1, 2, 3, \dots$$

where:
- $v_w$ = water velocity (~1500 m/s)
- $d$ = receiver depth (typically 6–10 m)
- $n$ = notch number

For a 6 m depth, the first notch is at 125 Hz, the second at 250 Hz, etc. The **zero-frequency notch** ($n = 0$) means all low frequencies below the first notch are lost.

### Deghosting

**Deghosting** is the process of removing the effect of source and receiver ghosts to recover the lost bandwidth. Modern deghosting methods include:

1. **Classical 1D designature** — deterministic inverse filter (vertical ray assumption only)
2. **Bootstrap deghosting** — inverse problem in tau-p domain (accounts for angle-dependent ghost delays)
3. **Dual-sensor (PZ) deghosting** — combines pressure (hydrophone) and particle velocity (geophone) data
4. **Variable-depth streamer** — towed at varying depths to create notch diversity (e.g., CGG BroadSeis)
5. **Sparse deghosting** — sparsity-constrained inversion in frequency-slowness domain
6. **Low-frequency deghosting** — trace-by-trace operator using integrated/differentiated pressure field

## Benefits of Broadband Data

### For Interpretation
- **Sharper wavelets** with minimal side lobes → better event resolution
- **Low-frequency texture** → subtle impedance variations become visible
- **Improved fault tracking** → low frequencies highlight impedance contrasts across faults
- **Better well ties** → broader bandwidth improves synthetic seismogram matching

### For Inversion and AVO
- **Extended low frequencies** → reduced dependence on initial model (only 0–3 Hz gap instead of 0–10 Hz)
- **More consistent AVO behavior** → ghost removal provides cleaner amplitude vs. offset response
- **Improved impedance inversion** → broader bandwidth yields more accurate and quantitative results

### For Deep Imaging
- **Low frequencies penetrate better** → less affected by absorption in complex overburdens (salt, basalt, chalk)
- **Improved imaging beneath absorptive layers** → better signal-to-noise at depth

## Marine Broadband Techniques

### Dual-Sensor Streamers
- **GeoStreamer® (PGS)** — combines hydrophones and geophones
- **Sentinel® (Sercel)** — similar dual-sensor concept
- **IsoMetrix (Schlumberger)** — multi-component measurement (hydrophones + accelerometers)

These systems exploit the polarity difference between pressure and particle velocity for ghosts:
- Hydrophone: ghost has opposite polarity to primary
- Geophone: ghost has same polarity as primary
- Summing the two cancels the ghost

### Variable-Depth Streamers
- **BroadSeis™ (CGG)** — streamer towed at varying depths (e.g., 6–10 m)
- Different depths create different ghost notch frequencies
- Processing combines data from all depths to fill in the notches
- Achieves true broadband (6+ octaves)

## Land Broadband Challenges

Achieving marine-style broadband on land is more difficult due to:

1. **Source limitations**
   - Vibroseis: limited low-frequency output (typically >3 Hz)
   - Dynamite: generates more low frequencies but environmental/safety concerns

2. **Receiver limitations**
   - Geophones have resonance frequency (~10 Hz) that attenuates low frequencies
   - Poor coupling in dry/loose near-surface reduces low-frequency response

3. **Near-surface effects**
   - Strong absorption in weathering layer
   - Scattering and attenuation in complex near-surface

**Recent developments** show that broadband land data (6 octaves) is achievable with:
- Better source-receiver coupling
- Low-frequency geophones or accelerometers
- Careful near-surface characterization and statics
- Advanced processing (Q-compensation, inverse filtering)

## Practical Considerations

### Validation
The only reliable way to validate broadband claims is **well tie**:
- Compare seismic bandwidth to well-derived synthetic seismogram
- Check that extended frequencies are in phase with true reflectivity
- Beware of "apparent" bandwidth increase without actual information content

### QC Metrics
- **Octave count** — how many octaves of usable bandwidth?
- **Notch depth** — are ghost notches filled after deghosting?
- **Side lobe level** — are wavelet side lobes suppressed?
- **Well tie quality** — does the broadband data improve the tie?

### Processing Workflow (Marine)
Typical broadband processing sequence:
1. **De-bubble** — remove source bubble oscillation
2. **Designature** — compress source signature (zero-phase or spiking)
3. **Deghost** — remove source and receiver ghosts
4. **Q-compensation** — correct for absorption losses
5. **Predictive deconvolution** — compress wavelet and attenuate multiples
6. **Migration** — image the subsurface

## Related Concepts

- [Marine deghosting](marine_deghosting.md) — detailed discussion of deghosting methods
- [Source signature and designature](source_signature_designature.md) — source wavelet components
- [Seismic wavelet](seismic_wavelet.md) — wavelet properties and effects
- [Predictive deconvolution](predictive_deconvolution.md) — wavelet compression

## Sources

- [Monk (2020)](../sources/monk_2020_broadband_seismic.md) — comprehensive overview of broadband concepts and marine techniques
- [Amundsen & Zhou (2013)](../sources/amundsen_zhou_2013_deghosting.md) — low-frequency deghosting method
- [Li et al. (2020)](../sources/li_et_al_2020_sparse_deghosting.md) — sparse deghosting and denoising
- [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md) — designature and deghosting workflows
