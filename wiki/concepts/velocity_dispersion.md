---
title: Velocity dispersion from absorption (Kramers–Kronig)
status: draft
sources:
  - futterman_1962_dispersive_body_waves
  - schonleber_2014_kk_system_theory
  - kjartansson_1979_constant_q
tags: [velocity-dispersion, kramers-kronig, causality, hilbert-transform, phase-velocity]
---

# Velocity dispersion from absorption (Kramers–Kronig relations)

**Velocity dispersion** — phase velocity depending on frequency — is not an optional companion of absorption: for a *linear causal* medium, absorption **necessarily implies** dispersion, with the two linked uniquely by the Kramers–Kronig (KK) relations. In a causal, attenuating earth, high frequencies travel slightly *faster* than low frequencies.

## Why absorption without dispersion is impossible

A filter that attenuates high frequencies but delays no frequency (zero phase at all frequencies) has a symmetric impulse response that begins before $t = 0$ — an acausal system. Physical wave propagation cannot respond before the input arrives; therefore the attenuation spectrum $\alpha(\omega)$ and the phase spectrum must be connected.

## Kramers–Kronig relations

For any linear time-invariant causal system with frequency response $H(\omega)$, real and imaginary parts form a Hilbert-transform pair (Cauchy principal values):

$$\operatorname{Re}H(\omega) = \frac{1}{\pi}\,\mathrm{P}\!\int \frac{\operatorname{Im}H(\omega')}{\omega'-\omega}\,d\omega', \qquad \operatorname{Im}H(\omega) = -\frac{1}{\pi}\,\mathrm{P}\!\int \frac{\operatorname{Re}H(\omega')}{\omega'-\omega}\,d\omega'$$

Applied to the seismic propagation constant, the absorption law fixes the dispersion law. Full step-by-step derivation (causality → analyticity → KK → seismic application) in `lecture_notes/derivations/kramers_kronig_dispersion_derivation.en.md`.

## Futterman's dispersion law

Futterman (1962): with absorption linear in frequency above a low-frequency cutoff $\omega_0$ (nearly constant Q), the asymptotic dispersion for $\omega \gg \omega_0$ is logarithmic:

$$\frac{v(\omega)}{c} \approx 1 + \frac{1}{\pi Q}\ln\frac{\omega}{\omega_0}$$

- The cutoff $\omega_0$ must be nonzero (arbitrarily small) for the theory to stay physical; results depend on it only logarithmically (weakly).
- Magnitude for seismic parameters: a few percent velocity change across the seismic band for Q ≈ 30–100 — small but consequential: tens of milliseconds of traveltime difference at 2–3 s, visible in well ties, 4D and velocity analysis.

## Kjartansson's exact constant-Q law

$$\frac{v(\omega)}{v_r} = \Big(\frac{\omega}{\omega_r}\Big)^{\gamma}, \qquad \gamma = \frac{1}{\pi}\arctan\frac{1}{Q} \approx \frac{1}{\pi Q}$$

Since $x^{\gamma} \approx 1 + \gamma\ln x$ for small $\gamma$, the power law and Futterman's logarithmic law are nearly identical over seismic bands for Q ≥ 30 — the two "velocity ratio" options met in Q-compensation software.

## Consequences

- Wavelet distortion: the low-frequency tail lags behind — the deeper the reflector, the more the wavelet stretches and its peak is delayed
- Velocity-analysis bias: picked velocities correspond to the dominant frequency content of the data; absorption shifts them (apparent velocity)
- Dispersion correction is a pure phase operation and is unconditionally stable — the reliable half of [inverse Q filtering](inverse_q_filtering.md)

## Relation to lecture notes

Term 2 Lecture 01, Section 3; derivation document `kramers_kronig_dispersion_derivation.en.md`.

## Related concepts

- [Seismic absorption](seismic_absorption.md)
- [Models of Q](q_models.md)
- [Inverse Q filtering](inverse_q_filtering.md)
- [Seismic velocities](seismic_velocities.md)
