---
title: "Yilmaz (2001) — Seismic Data Analysis §6.3: Slant-Stack Transformation (RU translation)"
status: draft
source_type: textbook chapter
authors: "Öz Yilmaz"
year: 2001
source_file: papers/textbooks/Yilmaz - Seismic Data Analysis_2.pdf (pp. 325–353, Russian translation)
lectures:
  - term02_lec02
  - term02_lec03
related_concepts:
  - radon_transform
  - fk_transform
  - rho_filter
  - aliasing
tags: [slant-stack, tau-p, plane-wave-decomposition, rho-filter, aliasing, dip-filter, interpolation, textbook]
---

# Yilmaz (2001) §6.3 — Slant-Stack Transformation

*Seismic Data Analysis*, Vol. 2, Section 6.3 (Russian translation in the library; extracted PDF pages 325–353; §6.4 "velocity-stack transformation" starts p. 354 and is not extracted).

## Main message

The classical encyclopedic treatment of the slant-stack (τ-p) transform: the physical basis (plane-wave decomposition via Snell's-law ray parameter), the forward/inverse pair, the **rho filter**, the exact relation between the f-k and τ-p domains, the behavior of aliased events, practical choice of p-sampling parameters, dip filtering in the slant-stack domain, τ-p interpolation, and periodicity of multiples in τ-p.

## Key content

### Plane-wave decomposition physics (§6.3 intro)
- Slant stacking is justified by the horizontally layered earth assumption: the ray parameter `p = sinθ/v` is conserved along a ray (Snell), so a τ-p trace is a genuine **plane-wave response** at emergence angle θ, not just a dip sum.
- Plane waves can be synthesized physically with delayed sources (Fig. 6.3-3/4) or by reciprocity with moving receivers — historical motivation from the plane-wave shooting era.

### Forward and inverse transforms (Claerbout, 1978)
- Forward: LMO with trial `p`, then sum over offset:
  `τ = t − px`,  `S(p, τ) = Σₓ P(x, τ + px)`  (eqs. 6-4a,b)
- Inverse: inverse LMO and sum over p (adjoint, eqs. 6-5a,b).
- **Rho filtering:** for proper amplitude recovery, the amplitude spectrum of each slant-stack trace is multiplied by |f| before the inverse transform. Equivalent to differentiating the wavefield before summation; the same operator appears in the integral formulation of Kirchhoff migration (§4.1). (Same ramp as tomography's λ-filter.)
- Treitel et al. (1982) distinguish the **conventional** slant stack (exact plane-wave decomposition for line sources) from the **proper** slant stack (point sources — needs a 3D amplitude correction operator before summation); the two are kinematically equivalent, differing only in amplitudes.

### Event mapping and the f-k ↔ τ-p relation (Figs. 6.3-9, 6.3-13)
- A hyperbola is mapped point-by-point through its **tangents**: each summation line touches the hyperbola in a Fresnel-zone neighborhood (tangent point B → point B′ in τ-p). The apex maps to (t₀, p=0).
- A linear event in t-x → a **point** in τ-p; and back: a linear event in τ-p → a point in t-x.
- 1D Fourier transform of the τ-p traces over τ gives the **ω-p spectrum**; a radial line in f-k corresponds to a vertical line in ω-p (`kₓ = p·f`, eq. 6-7 as printed with the frequency factor implied). The f-p plane is used in channel-wave analysis (§F.1).

### Aliasing behavior (Fig. 6.3-14)
- Spatial aliasing shows as **wraparound** in the f-k plane (inadequate spatial sampling of the linear event).
- Subtlety: the aliased portion of an event maps onto **the same p trace** as the unaliased portion — the aliased frequencies (e.g. 21–42 Hz in the example) do **not** appear on negative-p traces as one might expect. Tau-p does not automatically un-mix aliased energy.

### Practical p-parameter selection (Fig. 6.3-18) — the experimental matrix
- Baseline that reconstructs exactly: number of p values `np = nx` (number of traces), `p_min = 0`, `p_max` = steepest dip present in the data.
- **Too coarse Δp** (`np = nx/2`): reconstructed gather shows coherent noise (artifact A).
- **Oversampling in p** (`np = 2nx`): neither hurts nor helps — no gain beyond the information content.
- **Too wide p range** (`p_max` beyond data dips): the empty steep p traces are fed by the shortened effective aperture of the shallow-tangent sums and produce artifact B; empty p-trace regions should be excluded (or damped) before the inverse transform.

### Applications shown
- **Dip filtering**, including **time-variant** dip filtering (different mute per time window) in the slant-stack domain.
- **Interpolation** of missing traces by transforming to τ-p and inverse transforming onto a finer x grid (Fig. 6.3-16) — the "smart interpolator".
- **Multiple suppression**: water-layer multiples are periodic on τ-p traces but not on offset traces → predictive deconvolution works better in τ-p (Figs. 6.3-22…6.3-25; Treitel et al. 1982) — material for the multiples lecture.

## Relation to lecture notes

- Term 2 Lecture 02: Sections 5–8 follow this development — slant-stack construction, tangent/envelope mapping of hyperbolas, rho filter, f-k ↔ f-p relation, Δp and aperture artifacts, τ-p mutes. The aliased-event subtlety (aliased energy stays on the same p trace) refines Section 6.1.
- Term 2 Lecture 03 (multiples): τ-p periodicity of water-layer multiples and τ-p deconvolution.

## Related concepts

- [Radon transform](../concepts/radon_transform.md)
- [FK transform](../concepts/fk_transform.md)
- [Rho filter](../concepts/rho_filter.md)
- [Aliasing](../concepts/aliasing.md)

## Related sources

- [Margrave (2006)](margrave_2006_methods_of_seismic_data_processing.md) — same material as course notes with the projection-slice-theorem derivation.
- [Gower (2003)](gower_2003_intouch_taup.md) — production τ-p noise + demultiple workflow.
