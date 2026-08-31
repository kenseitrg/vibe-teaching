---
title: Amundsen & Zhou (2013) — Low-frequency seismic deghosting
type: paper
year: 2013
authors: Lasse Amundsen, Hongbo Zhou
source_file: papers/marine/amundsen2013.pdf
status: reviewed
tags: [deghosting, marine, broadband, low-frequency, green-theorem, trace-by-trace]
---

# Amundsen & Zhou (2013) — Low-frequency seismic deghosting

## Source

- **Authors:** Lasse Amundsen (Statoil/NTNU), Hongbo Zhou (Statoil)
- **Title:** Low-frequency seismic deghosting
- **Journal:** Geophysics, 78(2), WA15–WA20
- **Year:** 2013
- **DOI:** 10.1190/GEO2012-0276.1
- **File:** `papers/marine/amundsen2013.pdf`

## Main message

A trace-by-trace low-frequency deghosting method can restore the low-frequency content of seismic pressure data suppressed by source and receiver ghosts. The deghosted field is computed as the sum of the pressure field and its scaled temporally integrated and differentiated fields, effective up to approximately half the second notch frequency.

## Key points

1. **Ghost notch frequencies:** $f_n = \frac{nc}{2z}$ for $n = 0, 1, 2, ...$, where $c$ is sound speed in water (~1500 m/s) and $z$ is source or receiver depth. The first notch is always at 0 Hz.

2. **Ghost function in frequency-wavenumber domain:**
   $$G(k_x, k_y, k, z) = 1 - r_0 \exp(2ik_z z)$$
   where $k_z = \sqrt{k^2 - k_x^2 - k_y^2}$ is the vertical wavenumber, $k = \omega/c$ is the wavenumber, and $r_0 \approx 1$ is the sea-surface reflection coefficient.

3. **For vertically traveling plane waves** ($k_x = k_y = 0$):
   $$G(k, z) = 1 - \exp(2ikz)$$
   with amplitude spectrum $|G| = 2\sin(kz)$.

4. **Ideal deghosting:** multiply by $1/G(k_x, k_y, k, z)$, but this is unstable near notch frequencies where S/N is low.

5. **Low-frequency approximation:** neglect horizontal derivative operators (trace-by-trace approximation):
   $$F(k, z) \approx 1 - \frac{1}{2} + \frac{ikz}{2} - \frac{1}{2}\left(\frac{1}{ikz} - \frac{ikz}{3}\right)$$
   
   Simplified to:
   $$F(k, z) \approx \frac{1}{2}\left[1 + i\cot(kz)\right]$$

6. **Time-domain implementation:** the low-frequency deghosted pressure field is:
   $$U^{DG}(t, z) \approx U(t, z) + \frac{1}{2} + \frac{c}{2z}\int_0^t U(t', z)dt' + \frac{z}{6c}\frac{\partial U(t, z)}{\partial t}$$
   
   The deghosted field = pressure + scaled time integral + scaled time derivative.

7. **Effective bandwidth:** deghosts data up to approximately half the second notch frequency. For depth $z = 10$ m, second notch at 150 Hz, effective up to ~75 Hz.

8. **Limitations:**
   - Low-frequency side limited by S/N ratio.
   - Trace-by-trace approximation neglects angle-dependent effects.
   - Works best for conventional streamer data where S/N is acceptable at low frequencies.

9. **Receiver-side vs source-side deghosting:**
   - Receiver-side: applied in common-shot domain.
   - Source-side: applied in common-receiver domain.
   - Both can be combined with dual-sensor (PZ) methods.

10. **Applications:** particularly useful for data beneath complex overburdens (basalt, salt, chalk) where low frequencies are critical for imaging and inversion.

## Key equations

**Ghost notch frequency:**
$$f_n = \frac{nc}{2z}, \quad n = 0, 1, 2, ...$$

**Ghost function (vertical incidence):**
$$G(k, z) = 1 - \exp(2ikz)$$

**Low-frequency deghosting filter:**
$$F(k, z) \approx \frac{1}{2}\left[1 + i\cot(kz)\right]$$

**Time-domain deghosting:**
$$U^{DG}(t, z) \approx U(t, z) + \frac{1}{2} + \frac{c}{2z}\int_0^t U(t', z)dt' + \frac{z}{6c}\frac{\partial U(t, z)}{\partial t}$$

## Practical implications

- **Simple to implement:** trace-by-trace operation, no spatial sampling requirements.
- **Restores low frequencies:** improves S/N at frequencies below the second notch.
- **Works with legacy data:** applicable to conventional streamer data, not just dual-sensor or variable-depth acquisitions.
- **Complementary to other methods:** can be combined with PZ deghosting, sparse deghosting, or variable-depth streamer processing.
- **QC:** check amplitude spectra before/after; low-frequency content should be enhanced, notches filled.

## Implications for teaching

- Provides a clear mathematical derivation of the ghost function and deghosting filter.
- Shows how a complex frequency-domain operation can be approximated as simple time-domain operations (integration + differentiation).
- Demonstrates the trade-off between accuracy (full f-k deghosting) and practicality (trace-by-trace approximation).
- Good example of how physical understanding (ghost physics) leads to practical processing solutions.

## Concepts informed

- [Marine deghosting](../concepts/marine_deghosting.md)
- [Broadband seismic](../concepts/broadband_seismic.md)

## Related sources

- [Ghosh (2000)](ghosh_2000_ghost_deconvolution.md) — frequency-domain deghosting approach
- [Li et al. (2020)](li_et_al_2020_sparse_deghosting.md) — sparse deghosting method
- [CGG ODT04 Part 2](cgg_odt04_deconvolution_part2_signature.md) — bootstrap deghosting (tau-p domain)

## Quotes / memorable lines

> "The low-frequency deghosted pressure field is therefore the sum of the pressure field and its scaled temporally integrated and temporally differentiated fields."

> "The technique works with conventional streamer acquisition and so also enables deghosting of legacy data."

> "The low-frequency deghosting technique can be appropriate to apply to the part of seismic data that have penetrated and reflected beneath complex and attenuating overburdens such as basalt, salt, and chalk."
