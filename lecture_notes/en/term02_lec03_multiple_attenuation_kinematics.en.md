---
title: "Term 2 Lecture 03 — Multiple Attenuation I: Kinematic Methods"
author: Seismic Data Processing Course
---

# Multiple Attenuation I: Multiples, Their Fingerprints, and Move-Out Discrimination

## Why this lecture matters

Of all the noise types in seismic processing, multiples are the most dangerous. Ground roll (Term 2 Lecture 02) is loud but *obviously* noise: slow, low-frequency, steeply dipping. A multiple is none of these things. It is a genuine reflection — same wavelet, same frequency band, same general behavior — that has simply reflected one extra time on its way to the receiver. Nothing in a single trace tells you it apart from the "real" reflections. Stack it, migrate it, interpret it, and it will happily become a fake reflector, a fake anticline, a fake reservoir.

Multiples deserve (and get) a full pair of lectures. This first one builds the mental model:

1. **What multiples are** and why they fool imaging and interpretation.
2. **The two fingerprints** every multiple leaves: *periodicity* and *excess moveout*. Every demultiple method in existence exploits one of them (Verschuur's taxonomy).
3. **Classification**: surface-related vs. internal; short-period vs. long-period — and why the classification decides the treatment.
4. **Move-out discrimination**: the whole family of kinematic filters, from NMO-plus-stack, through FK, to the least-squares and high-resolution parabolic Radon transforms — workhorse of production demultiple.
5. **Where kinematic methods break**: near offsets, velocity inversions, non-hyperbolic moveout, AVO. These limitations are not footnotes; they are the reason Session 2 (predictive deconvolution, SRME, adaptive subtraction) exists.

Prerequisites: CMP gathers, NMO and stacking velocities (Term 1 Lec 03), FK and tau-p transforms (Term 2 Lec 02), deconvolution basics (Term 1 Lec 06).

---

## 1. What a multiple is, and why it is a problem

### 1.1 One definition, no exceptions

A **primary** reflection has exactly one upward reflection in the subsurface: source → reflector → receiver. A **multiple** has *at least one additional downward reflection* somewhere along its path — at the earth's free surface (for marine data, the sea surface; reflection coefficient $\approx -1$, a nearly perfect mirror) or at an interface *inside* the subsurface.

That is the entire definition, and everything in these two lectures follows from it:

- the extra reflection happens at a *shallow, strong* boundary → the multiple's amplitude can rival a primary's;
- the extra path segments are traveled in *shallow, slow* layers → the multiple's kinematics differ from a primary's at the same arrival time;
- the extra path repeats the same layers → arrivals come in *periodic families*.

![Figure: `figures/term02_lec03/term02_lec03_multiple_raypaths.png` — raypath anatomy of primaries and multiples.](./figures/term02_lec03/term02_lec03_multiple_raypaths.png)

*Figure 1: Anatomy. A primary has one upward reflection (left). A water-bottom multiple bounces off the sea surface — the red circle marks the downward reflection, the defining feature of a multiple (second panel). A peg-leg combines two different reflectors (third). An internal multiple does all its extra bouncing below the surface (right). All four events arrive at the same receiver with the same wavelet — no single trace can tell them apart.*

### 1.2 Why they fool the processing chain

Consider what each processing step "believes":

- **Stacking** believes events with hyperbolic moveout at the picked velocity. A multiple *has* hyperbolic moveout — at a lower velocity. If the velocity analysis is contaminated (multiples are strong, coherent events that produce their own semblance maxima!), the stack stacks the multiples too.
- **Migration** believes every event is a primary and images it accordingly: a multiple becomes a reflector at a location where none exists.
- **Interpretation** believes the image. False reflectors, false pinch-outs, false structures.

![Figure: `figures/term02_lec03/term02_lec03_real_stack_multiples.png` — stacked section with multiples (Nordkapp area).](./figures/term02_lec03/term02_lec03_real_stack_multiples.png)

*Figure 2: A stacked section riddled with multiples (Nordkapp area, courtesy ExxonMobil, from the original deck). Note the families of sub-parallel events — water-bottom multiples and their peg-legs marching down the section at regular intervals. Everything here looks like a perfectly plausible sedimentary sequence.*

Our synthetic example makes the interpretation trap explicit:

![Figure: `figures/term02_lec03/term02_lec03_false_structure.png` — false structure created by multiples.](./figures/term02_lec03/term02_lec03_false_structure.png)

*Figure 3: False structure, built honestly. Left: the multiple-free section ("the truth") — flat water bottom, one anticline, one flat reflector. Middle: only the surface multiples (computed with the 1D feedback relation — a preview of SRME). Right: what we record. The anticline generates a **false anticline** deeper in the section (the surface multiple of the real one — note the doubled structure), and the water bottom generates a ladder of fake flat reflectors. Without independent knowledge, which anticline would you drill?*

On real data the effect is not hypothetical:

![Figure: `figures/term02_lec03/term02_lec03_real_migration_with_mult.png` — migrated image with multiples.](./figures/term02_lec03/term02_lec03_real_migration_with_mult.png)

![Figure: `figures/term02_lec03/term02_lec03_real_migration_demult.png` — same image after surface-related multiple removal.](./figures/term02_lec03/term02_lec03_real_migration_demult.png)

*Figure 4: Prestack depth migration of a synthetic dataset (from the original deck): without demultiple (top) the multiples paint false reflectors across the whole section; after removal of surface-related multiples (bottom) the true image emerges. This pair of pictures is the elevator pitch for the next two lectures.*

### 1.3 Where demultiple sits in the flow

Demultiple is a *prestack* problem: once stacked or migrated, primaries and multiples share the same zero-offset time and no offset axis remains to separate them. In a typical marine sequence it sits after amplitude recovery, (de)convolution and initial velocity analysis, and before detailed velocity analysis and final stack — cleaner gathers give better picks, and better picks give a better demultiple. In practice the loop is iterated.

---

## 2. The two fingerprints

Every multiple removal method exploits one of exactly two properties. This taxonomy (due to Verschuur) organizes everything — including next lecture's methods.

### 2.1 Fingerprint 1: periodicity

Take the simplest repeating machine in seismic exploration: a water layer of thickness $h_w$ over the seabed. A wave trapped between sea surface and seabed reverberates: every round trip adds the same delay and multiplies the amplitude by the same factor,

$$
\Delta t_w \;=\; \frac{2\,h_w}{v_w}, \qquad
\text{gain per round trip} \;=\; R_\text{bot}\,R_\text{surf} \;\approx\; -R_\text{bot}.
$$

With $h_w = 300$ m and $v_w = 1480$ m/s: $\Delta t_w = 0.405$ s; with $R_\text{bot} = 0.4$, $R_\text{surf} = -1$, each order of reverberation is 40% as strong as the previous one. The result is a strictly periodic, geometrically decaying train of events:

![Figure: `figures/term02_lec03/term02_lec03_periodicity.png` — periodicity of water-layer reverberations.](./figures/term02_lec03/term02_lec03_periodicity.png)

*Figure 5: Periodicity. Left: the zero-offset trace — a periodic train with $\Delta t_w = 2 h_w/v_w = 405$ ms, each order damped by $R_\text{bot} R_\text{surf}$. Right: the same physics in shallow water (30 m): the period (40 ms) is shorter than the wavelet — the reverberations merge into "fog" (a short-period multiple) that interferes with everything beneath.*

The deeper observation — which becomes SRME next lecture — is that a multiple is *built from primaries*: combine the primary from the water bottom with the primary from the deep reflector and you get their peg-leg. **Travel times add; amplitudes multiply.** In the language of signal processing: convolution.

### 2.2 Fingerprint 2: excess moveout

Why should a multiple move out *more* than a primary arriving at the same zero-offset time? Because of compaction: velocity generally increases with depth. A primary reaching time $t$ has traveled to the depth where rocks are fast. A surface multiple reaching the same time $t$ spent its entire life bouncing in the *shallow, slow* part of the section — the only place where there was time to bounce.

$$
\text{shallow generator} \;\Longrightarrow\; \text{low average velocity} \;\Longrightarrow\; \text{large } \Delta t_\text{nmo}(x) \;\Longrightarrow\; \text{steep dip, low stacking velocity}.
$$

And each extra order adds another lap in the slow layers — the moveout grows order by order:

![Figure: `figures/term02_lec03/term02_lec03_multiple_moveout.png` — moveout fingerprint in a CMP gather.](./figures/term02_lec03/term02_lec03_multiple_moveout.png)

*Figure 6: The moveout fingerprint. Left: a CMP gather with two primaries and the water-bottom multiple family (synthetic but realistic velocities). Multiples are delayed progressively at far offset — each order steeper than the last. Right: differential moveout relative to the deep primary. At far offsets the separation reaches 150–250 ms — several wavelet lengths. At zero offset, by construction, it is zero: keep that thought for Section 4.5.*

### 2.3 Secondary behaviors

Two more recognizable habits, both visible on field data (original deck; Verschuur EET 01):

- **Conflicting dips.** Multiples cross primaries and each other; higher orders have progressively larger dips — on a stacked section they form fans.
- **Focusing and defocusing.** If the multiple-generating interface has structure (dipping seabed, fault scarp), the multiple family images that structure — sometimes focusing energy into bright spots ("migration smiles") that look exactly like reservoir anomalies.

### 2.4 The method map

| Family | Fingerprint exploited | Members |
|---|---|---|
| **Discrimination** (spatial behavior) | moveout / dip difference | NMO+stack, FK demultiple, Radon demultiple (this lecture) |
| **Prediction** (periodicity/predictability) | periodicity; "built from primaries" | predictive deconvolution, tau-p decon, SRME, adaptive subtraction (next lecture) |

---

## 3. Classification

Two independent axes matter, because each one decides which treatment applies.

### 3.1 Axis 1: where the downward reflection happens

- **Surface-related multiples** — at least one downward reflection at the free surface. The operational definition (Verschuur): *the multiples that would disappear if the earth's surface were removed.* Includes:
  - *water-bottom multiples* (the $\underbrace{S \to \text{WB} \to \text{surf}}_\text{lap} \to \text{WB} \to R$ family),
  - *peg-legs / reverberations* of the first layer,
  - *surface multiples of deeper reflectors* ($S \to A \to \text{surf} \to A \to R$, $S \to A \to \text{surf} \to B \to R$, …).
- **Internal (interbed) multiples** — all downward reflections below the surface. Named by their *shallowest* downward reflection. Weaker (intrabed reflectivities are small) but treacherous: they are the hardest to remove and this course treats them only at the level of "why they are hard".

### 3.2 Axis 2: the period

- **Long-period multiples** (separation $\gtrsim$ 50 ms, comfortably more than a wavelet): they appear as *separate events* — "deterministic", individually removable by move-out methods or predictable as events (SRME).
- **Short-period multiples** (separation $\lesssim$ wavelet length): they interfere with primaries and with each other; their net effect is that of a *transmission filter* — a "statistical" phenomenon. Treatment: (predictive) deconvolution, not event picking.

The two axes are independent: a water-bottom reverberation in 400 m of water is surface-related *and* long-period (→ Radon/SRME); the same reverberation in 30 m of water is surface-related *and* short-period (→ tau-p predictive deconvolution). Choose the treatment by the cell, not by habit.

---

## 4. Suppression by kinematics: move-out discrimination

### 4.1 The general recipe

All kinematic methods are one idea in different coordinates:

> Transform the gather (usually after NMO) into a domain where *moveout is an axis*; the primaries and multiples then occupy different regions of that axis; separate them there; transform back.

Any implementation of this recipe must satisfy **two requirements** (Verschuur):

1. primaries and multiples must actually *separate* in the chosen domain;
2. the transform must be *reversible* — otherwise you cannot go back without damage.

We will watch both requirements closely, because each kinematic method fails through one of them.

### 4.2 The legacy end-members: stacking and FK

**Stacking is a move-out filter.** Apply NMO at the *primary* velocity and stack: the primary aligns and sums constructively; the multiple — undercorrected, arriving progressively later at far offsets — sums destructively. Stacking velocity analysis *is* multiple discrimination, and it is the cheapest demultiple that exists. It is also the weakest: a stack attenuates rather than removes (typically 10–20 dB at best, depending on fold and moveout difference), it damages multiple-contaminated velocity picks, and it destroys the prestack data (AVO) that we now want to preserve.

**FK demultiple** (recall Term 2 Lec 02): after NMO at a velocity between primary and multiple, the two families have opposite dips (primaries curve up if overcorrected, multiples curve down). A 2-D dip filter — reject the downgoing fan — then separates them. It works, and it is cheap; but the events are *curved* (residual moveout is not a straight line), so they spread over a range of dips, the filter is hard to design, and overlap near the mute zone leaks. The lesson learned in production: for *curved* events you want a transform whose axis is *curvature*, not dip.

### 4.3 Parabolic Radon: the right domain

After an NMO correction with *any* reasonable velocity $V_\text{nmo}$, the residual moveout of an event in a CMP gather is well approximated by a parabola:

$$
t(x) \;\approx\; t_0 + q\,x^2,
$$

where $q$ (units s/m², in practice quoted as the residual moveout at maximum offset) is small and negative for overcorrected primaries, positive for undercorrected multiples. This is empirical but robust — hyperbolas minus hyperbolas are near-parabolas over typical offset ranges (Hampson, 1986).

The **parabolic Radon transform** maps the gather $d(t, x)$ to a panel $m(\tau, q)$ by stacking along parabolas — and because the shift $q x^2$ does not depend on $t$, the transform can be computed *per frequency slice*, as we now formalize.

**Adjoint (stack along parabolas).** For one temporal frequency $f$,

$$
m(q, f) \;=\; \sum_{j} d(x_j, f)\, e^{\,i 2\pi f q x_j^2}
\qquad\Longleftrightarrow\qquad
\mathbf{m} = \mathbf{L}^{\mathsf H}\, \mathbf{d},
$$

where $\mathbf{L}[q, x] = e^{\,i2\pi f q x^2}$ is a small complex matrix — one row per curvature, one column per offset. At 40 Hz with 61 offsets and 69 curvatures, $\mathbf{L}$ is 69$\times$61: tiny.

**The catch: the adjoint is not an inverse.** Stack along parabolas, and each event smears along the $q$ axis (a parabola at an off-grid curvature is approximated by a band of grid parabolas); transform back with the reverse stack, and the reconstruction does not match the input. Requirement 2 fails. The fix — and the single most useful idea of this section — is to *redefine the forward transform as the least-squares inverse of the reverse one*:

$$
\boxed{\;\mathbf{m}_\text{ls} \;=\; \left(\mathbf{L}^{\mathsf H}\mathbf{L} + \lambda^2 \mathbf{I}\right)^{-1} \mathbf{L}^{\mathsf H}\, \mathbf{d}\;}
$$

(the stabilization $\lambda^2 \mathbf{I}$ — or equivalently truncation of small eigenvalues — tames the near-singular directions where parabolas of different $q$ are indistinguishable). Now the round trip reconstructs the input, and the panel *focuses*:

![Figure: `figures/term02_lec03/term02_lec03_parabolic_radon_ls.png` — adjoint vs least-squares parabolic Radon.](./figures/term02_lec03/term02_lec03_parabolic_radon_ls.png)

*Figure 7: Adjoint vs LS. Top: the adjoint panel smears each event across many curvatures, and its reconstruction misses 100%+ of the data energy — the pair (stack, reverse stack) is not an inverse pair. Bottom: the LS panel focuses each event into a compact blob around its true residual moveout, and the reconstruction residual is a few percent. Both panels describe the same data; only the bottom one is a faithful representation.*

This is the same "adjoint $\neq$ inverse" lesson as the rho filter in Term 2 Lec 02 — but solved by explicit matrix inversion rather than a spectral ramp, because here the operator is small enough to invert per frequency.

### 4.4 The Hampson workflow, and high-resolution Radon

The production recipe (Hampson, 1986):

1. NMO-correct the CMP gather with a velocity *between* the primary and multiple trends;
2. forward (LS) parabolic Radon transform;
3. **mute** the large-curvature region (multiples live there);
4. inverse transform, apply the inverse NMO → primaries.

![Figure: `figures/term02_lec03/term02_lec03_radon_demultiple.png` — the Hampson (1986) demultiple workflow.](./figures/term02_lec03/term02_lec03_radon_demultiple.png)

*Figure 8: The workflow, end to end, on our synthetic gather: input → NMO at 2300 m/s → LS parabolic Radon panel with the mute (|residual| > 50 ms zeroed; red) → inverse transform and NMO back. Far offsets are cleaned almost perfectly; near offsets are not — see Section 4.5.*

![Figure: `figures/term02_lec03/term02_lec03_real_radon_input.png` — North Sea CMP gathers before Radon demultiple.](./figures/term02_lec03/term02_lec03_real_radon_input.png)

![Figure: `figures/term02_lec03/term02_lec03_real_radon_output.png` — North Sea CMP gathers after Radon demultiple.](./figures/term02_lec03/term02_lec03_real_radon_output.png)

*Figure 9: The same workflow on field data (North Sea, courtesy Equinor; from the original deck). Input CMP gathers with a strong multiple family; after parabolic Radon demultiple the primaries stand out. Production reality: dozens of gathers per second of section, per line, per survey.*

**From LS to high-resolution.** The LS panel still smears each event *along the q axis* — the event is a wavelet (not a delta) in time and, worse, the parabola family is nearly linearly dependent, so the LS solution compromises. When primaries and multiples are close in curvature, the smeared tails overlap, and the mute leaks multiples into the output (and clips primary tails).

The **high-resolution Radon transform** fixes this by changing what we ask for. Instead of the smallest-energy model (the L2 norm, which prefers many small coefficients), we ask for the *sparsest* model that still explains the data — an L1-like (Cauchy) penalty on the Radon coefficients:

$$
\boxed{\;
J(\mathbf{m}) \;=\; \underbrace{\left\|\mathbf{d} - \mathbf{L}^{\mathsf T}\mathbf{m}\right\|_2^2}_{\text{fit the data}}
\;+\;
\lambda \sum_{\tau,\,q} \ln\!\left(1 + \frac{m_{\tau,q}^2}{\sigma^2}\right)
\;\rightarrow\; \min_{\mathbf{m}}
\;}
$$

The Cauchy term penalizes *many* coefficients more than a few *large* ones: exactly what a panel of isolated events wants. The problem becomes non-linear; it is solved iteratively by re-weighting — each iteration solves an LS system whose damping is *inversely* proportional to the current coefficient size (large coefficients are left alone; small ones are crushed). The full derivation and the re-weighting scheme are written out in the companion derivation document; what matters in class is the behavior:

![Figure: `figures/term02_lec03/term02_lec03_highres_radon.png` — high-resolution parabolic Radon.](./figures/term02_lec03/term02_lec03_highres_radon.png)

*Figure 10: High-resolution Radon. Top: the iteration — starting from the smeared LS panel (iteration 0), each re-weighted solve concentrates energy; by iteration ~8–12 the panel is a set of compact blobs. The data fit barely changes (a few percent): we gave up almost nothing in fidelity and gained a lot in separability. Bottom: demultiple by the same mute in both panels — the LS mute leaks (residual multiple in the output), the HR mute separates cleanly. The last panel shows the difference of the two outputs at its own amplitude scale: the leaked residue that sparseness removed.*

A bonus of the sparse panel: events that *alias* (steep events on coarse offset sampling) also focus instead of smearing, so high-resolution Radon is more forgiving of sampling than its LS parent.

### 4.5 The four limitations

Move-out discrimination is cheap, robust, 3D-capable — and bounded by its assumptions. Four failures matter in practice (Figure 11):

**(1) Near offsets.** The discrimination signal — differential moveout — is *quadratic* in offset: it vanishes at $x \to 0$. Below roughly 500 m offset the difference between a multiple and a primary is smaller than the wavelet can express. No transform, however clever, separates identical things. Production answer: a hard mute of the near-offset strip after Radon demultiple — which throws away data, leaves a near-offset gap, and creates its own imaging problems.

**(2) Velocity inversions.** The whole method rests on "velocity increases with depth". Where it does not — fast carbonate or permafrost over slower sediments, salt flanks — the velocity ordering of primaries and multiples collapses. Internal multiples of the inversion zone are the worst: they can move out *almost exactly like primaries* and leak through every kinematic filter.

**(3) Non-hyperbolic moveout.** Complex overburden (faults, salt, diffractors) produces events that are not hyperbolas — apex-shifted, multi-arrivals, diffraction tails. A parabola (or hyperbola) transform does not focus them to a point; they smear in *any* Radon domain. Multiples are *more* non-hyperbolic than primaries (their path samples the overburden twice).

**(4) AVO.** A constant-amplitude parabola maps to a compact blob. An amplitude-versus-offset-varying parabola is a *sum* of constant ones — it smears along the curvature axis. Consequences in both directions: AVO smearing blurs the separation (leakage), and the mute itself damages primary AVO. If your goal is quantitative AVO, Radon demultiple parameters must be chosen with care — or the method changed.

![Figure: `figures/term02_lec03/term02_lec03_kinematic_limits.png` — limitations of kinematic demultiple.](./figures/term02_lec03/term02_lec03_kinematic_limits.png)

*Figure 11: The four limitations. (a) Differential moveout dies quadratically at near offsets — below ~500 m the events are indistinguishable; (b) a velocity-inversion model: after NMO at primary velocities, the surface multiple is strongly curved (easy) but the internal multiple of the slow layer is nearly flat (leaks through); (c) in the Radon panel a constant-amplitude event focuses, an AVO-carrying event smears along q.*

### 4.6 Scorecard

| | Move-out methods (FK / Radon family) |
|---|---|
| **Physics needed** | a velocity model good enough for NMO — and that is all |
| **Strengths** | cheap; robust; 2D and 3D; excellent at far offsets; no assumptions about the multiple generator |
| **Weaknesses** | needs a moveout *difference* (fails: near offsets, velocity inversions); assumes hyperbolic/parabolic events (fails: complex overburden); distorts AVO; removal leaves a muted near-offset gap |

The scorecard's last line is the setup for Session 2: what if, instead of *filtering multiples by how they move*, we *predict them from periodicity* — no velocity model, no moveout assumptions, near offsets welcome?

---

## Summary

- A **multiple** = reflection with $\geq 1$ extra *downward* reflection (free surface → surface-related; intrabed → internal). It carries the same wavelet as a primary — the most convincing noise in seismic data; it stacks, migrates and interprets as false structure.
- Two **fingerprints**: **periodicity** (water-layer round trips: $\Delta t_w = 2h_w/v_w$; times add, amplitudes multiply → a multiple is built from primaries) and **excess moveout** (multiples live in slow shallow layers → lower stacking velocity, steeper dip, growing with order).
- **Classification**: surface-related vs. internal (where is the downward reflection); long- vs. short-period (separation vs. wavelet length). Treatment follows the cell: long-period → Radon/SRME; short-period → deconvolution.
- **Kinematic demultiple recipe**: transform to a domain where curvature is an axis, separate, transform back. Requirements: separability + reversibility.
- **Parabolic Radon**: after NMO, residual moveout $\approx$ $q x^2$; per-frequency operator $\mathbf{L}[q,x] = e^{i2\pi f q x^2}$; the adjoint smears — use the **LS inverse** $(\mathbf{L}^{\mathsf H}\mathbf{L}+\lambda^2\mathbf{I})^{-1}\mathbf{L}^{\mathsf H}$; mute large $q$; transform back (Hampson 1986).
- **High-resolution Radon**: replace the L2 model norm with a sparseness (Cauchy/L1) norm, solved by iterative re-weighting; focused panels → no mute leakage, alias tolerance.
- **Four limitations**: near offsets (no moveout difference — hard mute), velocity inversions (internal multiples move like primaries), non-hyperbolicity (no focus in any Radon domain), AVO (smearing + damage). Motivation for prediction methods: Session 2.

## Comprehension questions

1. Classify each event: (a) source → seabed → sea surface → seabed → receiver; (b) source → 1.2 km reflector → seabed (downward) → 1.8 km reflector → receiver; (c) a 55 Hz-period reverberation in a 25 m water layer. Surface-related or internal? Long- or short-period? Which treatment applies?
2. Water depth 150 m, $v_w = 1500$ m/s. Compute the water-bottom multiple period. At what zero-offset time does the third-order water-bottom multiple appear if the seabed two-way time is that same period? Would you classify the family as long- or short-period with a 40 Hz dominant-frequency wavelet?
3. Explain why a multiple generated at 0.5 s has more moveout than a primary arriving at 1.5 s, even though they both reach 2.5 s at zero offset. What geological circumstance breaks this argument?
4. Why does stacking along parabolas (the adjoint Radon) fail requirement 2 (reversibility), and what exactly does the least-squares inverse change about that? Why do we solve the LS system *per frequency slice* rather than once for the whole gather?
5. Your Radon demultiple leaves residual multiples at near offsets and your interpreter needs AVO at 1.2–2.0 s. Which two limitations of Section 4.5 are you hitting, and what are your options (name at least one method from next lecture that addresses each)?

## References and further reading

- Verschuur, D. J. (2006). *Seismic Multiple Removal Techniques: Past, Present and Future* — EAGE EET course, Chapter 1 (What's the problem?) and Chapter 2 (Move-out discrimination). `wiki/sources/verschuur_2006_eet01_multiples_problem.md`, `wiki/sources/verschuur_2006_eet02_moveout_discrimination.md`
- Hampson, D. (1986). Inverse velocity stacking for multiple elimination. *SEG Expanded Abstracts*, 44–47. (The parabolic Radon demultiple workflow.)
- Maeland, E. (1998). Focusing aspects of the parabolic Radon transform. *Geophysics*, 63(5), 1708–1715. `wiki/sources/maeland_1998_parabolic_radon.md`
- Herrmann, P., Mojesky, T., Magesan, M. & Hugonnet, P. (2000). De-aliased, high-resolution Radon transforms. *SEG Expanded Abstracts*. (LS vs. high-resolution comparison.)
- Trad, D. (2002). Interpolation and multiple attenuation with the high-resolution Radon transform. `wiki/sources/trad2002_radon_interpolation.md`
- Companion derivation: [High-resolution Radon transform — from least squares to sparsity](../derivations/highres_radon_derivation.en.md)
- Wiki concepts: [Multiples](../../wiki/concepts/multiples.md), [Radon transform](../../wiki/concepts/radon_transform.md), [Normal moveout](../../wiki/concepts/normal_moveout.md)
