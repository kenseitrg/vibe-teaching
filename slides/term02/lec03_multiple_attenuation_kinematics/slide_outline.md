# Slide outline — Term 2, Lecture 3: Multiple Attenuation I — Kinematic Methods

---


## Slide 1 — Title
- Multiple Attenuation I: Multiples and Move-Out Discrimination
- Term 2, Lecture 3
- Figure: none

---

## Slide 2 — Learning objectives
- Define primaries vs. multiples; explain why multiples fool imaging and interpretation.
- Name the two fingerprints of every multiple: periodicity and excess moveout — and the method families built on them.
- Classify multiples: surface-related vs. internal; short- vs. long-period — treatment follows the cell.
- Explain the parabolic Radon demultiple workflow incl. least-squares and high-resolution formulations.
- State the four limitations of kinematic methods and why they motivate the prediction family (next lecture).

---

## Slide 3 — Why multiples are the worst noise
- Ground roll is loud but obviously noise; a multiple is a genuine reflection with one extra downward bounce.
- Same wavelet, same frequency band: nothing in a single trace distinguishes it from a primary.
- It stacks at its own velocity, migrates as a reflector, and interprets as geology.
- Figure: `term02_lec03_multiple_raypaths.png`

---

## Slide 4 — The definition, in one line
- Primary: exactly one upward reflection.
- Multiple: at least one extra DOWNWARD reflection — free surface (red circle) or interbed.
- Surface-related definition test: "the multiples that disappear if the surface were removed".
- Everything in this lecture follows from the extra bounce: shallow-strong amplitude, slow-layer kinematics, periodic families.

---

## Slide 5 — The interpretation trap (real data)
- Stacked section riddled with multiples: families of sub-parallel events marching down the section.
- Water-bottom multiples, peg-legs, surface multiples of deeper reflectors — all look like stratigraphy.
- Figure: `term02_lec03_real_stack_multiples.png`

---

## Slide 6 — False structure (synthetic)
- Truth: flat water bottom, one anticline, one flat reflector.
- Recorded: the same plus a FALSE anticline (surface multiple of the real one) and a ladder of fake reflectors.
- Multiples computed with the 1D feedback relation — a preview of SRME (next lecture).
- Figure: `term02_lec03_false_structure.png`

---

## Slide 7 — Migration makes it worse (real data)
- Migration believes every event is a primary and images it: false reflectors, false structure.
- Without demultiple vs. after surface-multiple removal — the elevator pitch for these two lectures.
- Figure: `term02_lec03_real_migration_with_mult.png`

---

## Slide 8 — Fingerprint 1: periodicity
- Water layer = a repeating machine: each round trip adds $\Delta t_w = 2h_w/v_w$ and multiplies amplitude by $R_{bot} R_{surf}$.
- Long-period (separation > wavelet): separate events, "deterministic".
- Short-period (shallow water): reverberation fog, "statistical" — deconvolution territory.
- Figure: `term02_lec03_periodicity.png`

---

## Slide 9 — Times add, amplitudes multiply
- A multiple is BUILT FROM PRIMARIES: combine two primaries and you get their peg-leg.
- $t_{mult} = t_1 + t_2$, $A_{mult} = -A_1 A_2$ — that is convolution.
- Preview: SRME (next lecture) is exactly this observation, taken seriously.

---

## Slide 10 — Fingerprint 2: excess moveout
- Compaction: velocity increases with depth; a same-time multiple spent its whole life in slow shallow layers.
- Lower stacking velocity, more moveout, steeper dip; each order adds another slow lap.
- Differential moveout reaches 150-250 ms at far offsets — several wavelet lengths.
- Figure: `term02_lec03_multiple_moveout.png`

---

## Slide 11 — Secondary behaviors
- Conflicting dips: multiples cross primaries; higher orders dip more.
- Focusing/defocusing from structure in the generating layer — bright spots that look like anomalies.
- Amplitude magnification order by order; interference with primaries.

---

## Slide 12 — The method map
- Family 1 — discrimination (spatial behavior): NMO+stack, FK, Radon. This lecture.
- Family 2 — prediction (periodicity/composition): predictive decon, tau-p decon, SRME + adaptive subtraction. Next lecture.
- Every demultiple method in existence sits in one of these two rows.

---

## Slide 13 — Classification
- Axis 1 — where is the extra downward reflection: free surface vs. interbed (internal).
- Axis 2 — period vs. wavelet length: long-period vs. short-period.
- The axes are independent; the cell decides the treatment.
- (Draw the taxonomy grid on the blackboard: surface vs. internal × long- vs. short-period.)

---

## Slide 14 — Treatment by cell (examples)
- Water-bottom reverberation, 400 m water: surface-related + long-period -> Radon / SRME.
- The same family in 30 m water: surface-related + short-period -> tau-p predictive decon.
- Internal multiples: their own tools entirely (beyond this course).
- Choose by the physics, not by habit.

---

## Slide 15 — The general kinematic recipe
- Transform (after NMO) to a domain where curvature is an axis; separate; mute; transform back.
- Requirement 1: primaries and multiples must actually separate there.
- Requirement 2: the transform must be reversible.
- Every kinematic method fails through one of the two.

---

## Slide 16 — Legacy: stacking is a move-out filter
- NMO at primary velocity + stack: primary aligns and sums; multiple undercorrected, sums destructively.
- Cheapest demultiple that exists — and the weakest: attenuates, does not remove; biased picks; destroys AVO.
- FK demultiple: after NMO the families dip opposite ways -> dip filter. Curved events spread over dips -> leakage.

---

## Slide 17 — Parabolic Radon: the right domain
- After approximate NMO, residual moveout of every event is close to a parabola: $t(x) = t_0 + q x^2$.
- The shift $q x^2$ does not depend on $t$ -> the transform factorizes into small per-frequency matrix problems.
- $L[q,x] = e^{i 2 \pi f q x^2}$ — at 40 Hz: a 69x61 complex matrix. Tiny.

---

## Slide 18 — The adjoint is not an inverse
- Stack along parabolas (adjoint): events smear along the curvature axis; the reconstruction does not reproduce the input.
- Fix: redefine the forward transform as the least-squares inverse of the reverse one.
- $m = (L^H L + \lambda^2 I)^{-1} L^H d$ per frequency slice.
- Figure: `term02_lec03_parabolic_radon_ls.png`

---

## Slide 19 — The Hampson (1986) workflow
- 1) NMO with a velocity between primary and multiple trends.
- 2) Forward LS parabolic Radon. 3) Mute large curvature (multiples live there). 4) Inverse transform, inverse NMO.
- Far offsets clean almost perfectly; near offsets do not (see limitations).
- Figure: `term02_lec03_radon_demultiple.png`

---

## Slide 20 — Radon demultiple on field data
- Input CMP gathers with a strong multiple family; after parabolic Radon demultiple the primaries stand out.
- Production reality: dozens of gathers per second of section, per line, per survey.
- Figure: `term02_lec03_real_radon_input.png`

---

## Slide 21 — From LS to high-resolution
- LS still smears along q: near-null curvatures compromise; families overlap in the panel; the mute leaks.
- Change the prior: smallest ENERGY (L2) -> sparsest model (Cauchy/L1-like).
- $J = ||d - L^T m||^2 + \lambda \sum \ln(1 + m^2/\sigma^2)$ — non-linear, solved by iterative re-weighting (IRLS).
- Full derivation: companion document.

---

## Slide 22 — High-resolution Radon in action
- Same data, same physics: the sparse panel focuses each event into a compact blob (watch the iteration strip).
- Data fit barely changes; separability improves dramatically; alias tolerance as a bonus.
- Demultiple comparison: LS mute leaks; HR mute separates cleanly.
- Figure: `term02_lec03_highres_radon.png`

---

## Slide 23 — Limitation 1: near offsets
- The discrimination signal (differential moveout) is quadratic in offset — it vanishes at $x \to 0$.
- Below ~500 m offset the difference is smaller than the wavelet can express: no filter separates identical things.
- Production answer: hard mute of the near-offset strip -> a data gap -> its own imaging artifacts.

---

## Slide 24 — Limitation 2: velocity inversions
- The method rests on "velocity increases with depth".
- Fast layer over slow sediments (carbonate, permafrost): internal multiples inherit nearly primary-like kinematics.
- After NMO at primary velocities: surface multiple strongly curved (easy); internal multiple almost flat (leaks).
- Figure: `term02_lec03_kinematic_limits.png`

---

## Slide 25 — Limitations 3 and 4: non-hyperbolicity and AVO
- Complex overburden: apex-shifted, multi-arrivals, diffraction tails — no parabola focuses them.
- AVO: a variable-amplitude parabola is a sum of constant ones -> smearing along q; the mute also damages primary AVO.
- Quantitative AVO work demands careful parameter choices — or another method.

---

## Slide 26 — Scorecard
- Strengths: cheap; robust; 2D/3D; excellent at far offsets; no assumptions about the generator.
- Weaknesses: needs a moveout difference (near offsets, inversions); assumes hyperbolas (complex overburden); distorts AVO; leaves a muted gap.
- The setup for Session 2: what if we PREDICT the multiples instead of filtering them?

---

## Slide 27 — Summary
- Multiple = reflection with >= 1 extra downward bounce; carries the same wavelet — the most convincing noise.
- Two fingerprints: periodicity ($\Delta t_w = 2 h_w / v_w$; times add, amplitudes multiply) and excess moveout.
- Classification: surface-related vs. internal; long- vs. short-period; treatment by cell.
- Parabolic Radon: adjoint smears -> LS inverse $(L^H L + \lambda^2 I)^{-1} L^H d$; Hampson workflow; high-res adds sparsity (IRLS).
- Four limitations: near offsets, inversions, non-hyperbolicity, AVO -> prediction family, next lecture.

---

## Slide 28 — Comprehension questions
- Classify three given events by interface and period; pick the treatment for each.
- Water depth 150 m, $v_w$ = 1500 m/s: compute the multiple period and the arrival time of the third order.
- Why does a 0.5 s multiple move out more than a 1.5 s primary reaching 2.5 s? What breaks the argument?
- Why does the adjoint Radon fail requirement 2, and what does the LS inverse change?
- Your demultiple leaves residual multiples at near offsets and the interpreter needs AVO — which limitations, which remedies?

---

## Slide 29 — References
- Verschuur (2006), EET Chapters 1-2; Hampson (1986); Maeland (1998); Herrmann et al. (2000); Trad et al. (2003).
- Companion derivation: high-resolution Radon (LS to sparsity, IRLS).
- Wiki: multiples, radon_transform, normal_moveout.
