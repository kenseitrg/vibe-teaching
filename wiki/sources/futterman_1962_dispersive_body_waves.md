---
title: "Futterman (1962) — Dispersive Body Waves"
status: draft
type: paper
source_file: wiki/sources/_raw_text/Walter I. Futterman - Dispersive body waves.txt
language: en
concepts:
  - velocity_dispersion
  - seismic_absorption
  - q_models
tags: [kramers-kronig, causality, velocity-dispersion, absorption, quality-factor, hilbert-transform]
---

# Futterman (1962) — Dispersive Body Waves

*Journal of Geophysical Research*, 67(13), 5279–5291.

## Overview

Futterman's central result: **for a linear medium, absorption of body waves necessarily implies velocity dispersion**, and the dispersion is uniquely determined by the absorption law through a Kramers–Kronig (KK) type integral relation. The relations follow from the principle of causality alone — no specific wave equation or attenuation mechanism is required. The paper resolves an early-1960s controversy: apparent observations of absorption without dispersion (and a strictly linear absorption coefficient α(ω)) were thought to require nonlinear wave theory; Futterman shows they are fully consistent with linearity once causality is enforced.

## Setup

- Plane-wave displacement $u(R,t) = u_0 e^{iKR - i\omega t}$ with complex propagation constant $K = k + i\alpha(\omega)$; $\alpha > 0$ takes energy from the wave.
- Two assumptions: (a) the measured absorption coefficient is strictly linear in frequency over the band of interest; (b) the wave motion is linear (superposition holds).
- Complex index of refraction $n(\omega) = K(\omega)/(\omega/c)$, where $c$ is the nondispersive low-frequency velocity limit.
- **Low-frequency cutoff hypothesis:** for $\omega < \omega_0$ the absorption is negligible and no dispersion exists. The theory later *requires* $\omega_0 \neq 0$ — the cutoff may be arbitrarily small but not zero (otherwise $n$ is unbounded).

## Kramers–Kronig relation

From causality (signal cannot be detected before it can physically arrive) plus the crossing symmetry $K(x) = K^*(-x)$ (a consequence of a real-valued displacement), the dispersive part of the index is an integral over the absorptive part over all frequencies (Cauchy principal value). Futterman exhibits three absorption–dispersion pairs (A1, A2, A3) with different cutoff functions; all three converge to the same asymptotic dispersion for frequencies well above the cutoff:

$$\operatorname{Re} n(x) = 1 - \frac{1}{\pi Q_0} \ln x, \qquad x = \omega/\omega_0$$

This logarithmic law fails for $x > e^{\pi Q_0}$ (astronomically large for $Q_0 \geq 30$); a high-frequency cutoff removes this failure, and the dispersion in the measured range is insensitive to the exact cutoff form.

## Key takeaways

- Quality factor definitions: per-cycle energy loss $Q^{-1} = (2\pi)^{-1}(\Delta W / W)$; for small absorption $Q(\omega) \approx \omega/(2\alpha v_p)$, equivalently $Q \approx k/(2\alpha)$; reduced quality factor $Q_0(\omega) = \omega/(2\alpha c)$ with $\operatorname{Im} n = 1/(2Q_0)$.
- Phase and group velocities for $x > 6$: $v_p \simeq c\,[1 - (\ln\gamma x)/(\pi Q_0)]^{-1}$, $u_g \simeq c\,[1 - (1 + \ln\gamma x)/(\pi Q_0)]^{-1}$ (γ ≈ 1.781, Euler–Mascheroni); asymptotically both $\approx c\,[1 - (\ln x)/(\pi Q_0)]$.
- The **dispersion is unambiguously determined by the absorption** — an absorption–dispersion pair must be consistent (this is the foundation of every causal Q-compensation operator).
- Magnitude: for Pierre shale ($Q_0 \approx 30$) $\Delta v_p/v_p \approx 0.04$, i.e. an ~8% fractional velocity difference relative to the no-dispersion case at 1 Hz; for $Q_0 \approx 300$ (mantle) only ~$10^{-5}$ — dispersion is very hard to measure directly in the earth.
- The cutoff $\omega_0$ has weak influence on results (logarithmic dependence); in practice one may choose it phenomenologically small compared to the lowest measured frequency (e.g., $10^{-8}\,\mathrm{s}^{-1}$).
- Pulse shapes: numerical integration of the dispersive pulse shows delay and distortion growing with distance — the visual consequence of dispersion.

## Relation to lecture notes

Foundation for Term 2 Lecture 01 (Absorption and Q-compensation), Section 3 (causality and velocity dispersion). The step-by-step causality → KK derivation lives in `lecture_notes/derivations/kramers_kronig_dispersion_derivation.en.md`; Futterman's logarithmic dispersion law is the basis of the "Futterman" velocity ratio used in compensation operators and compared against Wang/Kjartansson's power law.

## Related sources

- [Schönleber (2014) — simple KK derivation](schonleber_2014_kk_system_theory.md) — compact system-theory proof of the same relations
- [Kjartansson (1979) — constant Q](kjartansson_1979_constant_q.md) — exact constant-Q alternative without cutoff
- [Wang (2002) — stable inverse Q filtering](wang_2002_stable_inverse_q.md) — practical phase compensation built on a Futterman-type law
