# Slide outline — Term 2, Lecture 4: Multiple Attenuation II — Prediction Methods

---


## Slide 1 — Title
- Multiple Attenuation II: Predictive Deconvolution, SRME and Adaptive Subtraction
- Term 2, Lecture 4
- Figure: none

---

## Slide 2 — Learning objectives
- Apply the prediction idea to periodic multiples; explain the offset-dependent failure of predictive decon and the tau-p repair.
- Derive the 1D SRME feedback relation; use its series and iterative forms; explain the surface operator and the wavelet problem.
- Explain the 2D SRME construction: virtual source at the downward reflection point, multiple contribution gather, sum over all DRPs.
- List SRME's data requirements and their production fixes.
- Formulate adaptive subtraction as a Wiener matching filter; choose parameters; decide L1 vs L2.

---

## Slide 3 — From discrimination to prediction
- Session 1's failures share one root: filtering by HOW MULTIPLES MOVE.
- New strategy: PREDICT them from what they are made of.
- A multiple is built from primaries (times add, amplitudes multiply) — the most predictable event in the record.
- No velocity model, no moveout assumption, near offsets welcome.

---

## Slide 4 — Predictive decon recap (Term 1)
- Prediction gap $\alpha$ = water period in samples; prediction-error filter subtracts the periodic train.
- Ideal predictor = shift + scale: primaries untouched, reverberations annihilated.
- Works perfectly on zero-offset / small-offset traces.
- Figure: `term02_lec03_multiple_raypaths.png`

---

## Slide 5 — The flaw: period varies with angle
- Vertical period $\Delta t_0 = 2h_w/v_w$ is measured by vertical rays only.
- Slant path: $\Delta t(\theta) = \Delta t_0 / \cos\theta$ — at far offsets the local period stretches.
- One constant gap cannot match a continuum of periods: the filter is wrong everywhere except one offset.
- Figure: `term02_lec04_period_vs_offset.png`

---

## Slide 6 — The repair: deconvolve in tau-p
- Tau-p organizes data by ray parameter: one angle per family per trace -> period constant along each p-trace.
- The gap is ANALYTIC: $\Delta\tau(p) = \Delta t_0 \sqrt{1 - p^2 v_w^2}$ — computed from water depth, no picking.
- Workflow: slant stack -> per-trace decon with gap(p) -> p-mute -> inverse transform (LS machinery of Session 1).
- Figure: `term02_lec04_taup_decon.png`

---

## Slide 7 — tau-p decon: the fine print
- ACF evidence: far-offset trace = smeared periods; p-trace = clean peaks at the analytic lag.
- Remaining limits: generator must be locally flat (1D); Wiener assumptions apply (stationary, min-phase).
- Cannot predict peg-legs with no short period at all -> need composition, not period.
- Figure: `term02_lec04_taup_decon.png`

---

## Slide 8 — SRME: the 1D building block
- Where does a first-order surface multiple come from? From the primary, twice, glued at the surface.
- $t_{mult} = t_1 + t_2$, $A_{mult} = -A_1 A_2$ -> convolution: $m_1 = -x_0 * x_0$, $m_2 = +x_0 * x_0 * x_0$, ...
- Figure: `term02_lec04_srme_1d_series.png`

---

## Slide 9 — The feedback equation
- The surface is a mirror: each loop convolves the total response with the primaries once more.
- $x = x_0 - x_0 * x$ (feedback diagram; minus = $r_0 = -1$).
- Implicit: $x_0 = x + x_0 * x$. Series: $x_0 = x + x*x + x*x*x + ...$ — removal by AUTO-CONVOLUTION OF THE INPUT.
- Figure: `term02_lec04_srme_1d_series.png`

---

## Slide 10 — Iterative SRME
- Fixed point: $p_0^{(0)} = p$; $p_0^{(i+1)} = p - a * p_0^{(i)} * p$.
- Each iteration strips one more order; converges geometrically ($33\% \to 15\% \to 9\% \to 5\%$).
- Production: 2-3 iterations — most multiple energy is first order.
- Figure: `term02_lec04_srme_iterations.png`

---

## Slide 11 — What happens to the wavelet
- Real data carry a source wavelet: the naive prediction $-p*p$ carries TWO wavelets (squared spectrum).
- Surface operator $a(t) = -[s(t)]^{-1}$ pre-scales every convolution so each order carries one wavelet.
- $s(t)$ never known perfectly; no directivity, no 3D -> adaptive subtraction is ALWAYS the last step.
- Figure: `term02_lec04_srme_wavelet.png`

---

## Slide 12 — 2D: the virtual source picture
- Any multiple splits at its downward reflection point (DRP) into two primary-shaped legs.
- Leg 1: shot-gather trace $P(x_k, x_s)$. Leg 2: receiver-gather trace $P(x_r, x_k)$ — "virtual source" at $x_k$.
- The multiple = time-convolution of the two legs.
- Figure: `term02_lec04_srme_2d_drp.png`

---

## Slide 13 — 2D: sum over all reflection points
- We do not know the DRP -> integrate over the whole surface:
- $M(x_r,x_s;f) = A(f) \int P(x_r,x_k;f) P(x_k,x_s;f) dx_k$ — per frequency a MATRIX PRODUCT $M = A P P$.
- The integrand vs. $x_k$ = multiple contribution gather (MCG); apexes mark the true reflection points.
- Figure: `term02_lec04_srme_2d_drp.png`

---

## Slide 14 — 2D SRME on data
- Prediction matches the actual multiples kinematically (8% in our demo); subtraction recovers the primaries.
- Field data: complex interfering families predicted without human interpretation.
- No subsurface model used ANYWHERE.
- Figure: `term02_lec04_real_srme_predicted.png`

---

## Slide 15 — SRME's bill 1: near offsets
- The prediction integrates over the surface: missing data = missing prediction.
- Near-offset gap: MCG loses its flat short legs -> shallow reverberations under-predicted (worst in shallow water).
- Figure: `term02_lec04_srme_requirements.png`

---

## Slide 16 — SRME's bill 2: regularity, land, internal
- Coarse/irregular shooting -> aliasing and missing matrix columns -> prediction artifacts.
- Fixes: shot interpolation, 5D regularization, reciprocity, near-offset reconstruction (Radon extrapolation).
- Land: ground roll/statics/amplitudes -> preprocess a COPY for prediction; statics dilemma (true surface vs. datum).
- Internal multiples: out of scope (need other machinery).
- Figure: `term02_lec04_real_srme_no_near_offsets.png`

---

## Slide 17 — Adaptive subtraction: the problem
- Predictions are right in KINEMATICS, wrong in DYNAMICS (amplitude, wavelet, directivity, 3D).
- Direct subtraction leaves residuals; one scalar cannot fix a wavelet.
- Universal answer: estimate a short MATCHING FILTER in local windows; subtract the filtered model.
- Figure: `term02_lec04_adaptive_subtraction.png`

---

## Slide 18 — The Wiener matching filter
- Same normal equations as Term 1 decon, new job: $R_{mm} a = r_{dm}$ (Toeplitz, Levinson).
- Worked example: model wrong by x1.4, 6 ms, wrong wavelet -> direct subtraction damages the primary 133%; adaptive 4%.
- The engine of EVERY model-and-subtract method: SRME, surface waves (Term 3), 4D matching.
- Figure: `term02_lec04_adaptive_subtraction.png`

---

## Slide 19 — Parameters and their interaction
- Filter length = how much you trust the model: long enough for the wavelet error, no longer.
- Window size = adaptivity vs. stability: small windows chase primaries; large windows miss lateral variation.
- Two-stage strategy: global inverse-wavelet filter in common-offset; local corrections in shot domain.
- Iterate: predict -> subtract -> re-predict from cleaner data.

---

## Slide 20 — L2 vs L1
- L2 assumes the OUTPUT has minimum energy — exactly wrong where a primary interferes with the multiple.
- The L2 filter compromises at the overlap: leakage AND primary damage (27% in the demo).
- L1 treats interference samples as OUTLIERS: primary survives (1% damage); solved by IRLS — the same re-weighting as high-resolution Radon.
- Figure: `term02_lec04_l1_vs_l2.png`

---

## Slide 21 — The filter-length trap
- Good model: short and long filters both behave.
- Bad model (wrong kinematics): short filter leaves residuals; LONG filter shapes the model into the DATA — primaries eaten.
- Rule: the filter length is a statement about model trust.
- Figure: `term02_lec04_l1_vs_l2.png`

---

## Slide 22 — Adaptive subtraction on field data
- Data, model, adapted subtraction output — the loop closes.
- Toolbox: L2 (fast, robust, crossing-event problems), L1 (interference), curvelets (dip+frequency separation).
- "A processor needs a toolbox approach." (Verschuur)
- Figure: `term02_lec04_real_adaptive_subtraction.png`

---

## Slide 23 — The shallow-water chain
- 30-80 m water: reverberation period shorter than the wavelet (fog) + long-period deeper multiples.
- No single tool cleans both: tau-p decon (fog) + SRME (long-period) + Radon (residuals).
- Production chain (EET 06): swell/bad traces -> decon+deghost -> FK (post-critical) -> pred. decon -> interpolation+near offsets -> SRME -> Radon.
- Figure: `term02_lec04_shallow_water_strategy.png`

---

## Slide 24 — The method map (both sessions)
- Discrimination: moveout/dip; needs velocity model; weak at near offsets; cheap; long-period multiples.
- Prediction: periodicity/composition; no velocity model; near offsets essential (SRME) or handled (tau-p decon); wavelet matters.
- No silver bullet: internal multiples need their own tools; every serious survey combines methods.
- The chain, not the competition: each stage handles the family its physics exploits.

---

## Slide 25 — Summary
- Predictive decon: gap = layer period; period varies with angle -> tau-p decon, gap $= \Delta t_0 \sqrt{1-p^2 v_w^2}$ per trace.
- SRME: $x = x_0 - x_0 x$; series $x_0 = x + x^2 + x^3 + ...$; iteration $p_0^{(i+1)} = p - a p_0^{(i)} p$; 2D: $M = A \int P P dx_k$ per frequency.
- Wavelet: surface operator $a = -1/s$; adaptive subtraction closes the gap.
- SRME needs: near offsets, regularity, wavelet; land needs preprocessing; internal multiples out of scope.
- Adaptive subtraction: Wiener matching in windows; length = model trust; L1 for interference (IRLS).
- Shallow water: the chain. Toolbox approach.

---

## Slide 26 — Comprehension questions
- 75 m water, $v_w$ = 1500: vertical period; period at 30 degrees; which method and gap?
- Why does SRME NEED near offsets while Radon demultiple MUTES them?
- Over-prediction x2 and 5 ms late: what does the matching filter do, which parameters, what if too long?
- Why does L2 damage primaries at interference and L1 not? Name the scheme and its other appearance.
- 200 m near-offset gap over 60 m water: sketch the demultiple chain and each stage's target family.

---

## Slide 27 — References
- Verschuur (2006), EET Chapters 3, 5, 6, 7; Berkhout & Verschuur (1997); Verschuur et al. (1992); Guitton & Verschuur (2004).
- Companion derivation: SRME from the feedback diagram.
- Wiki: srme, multiples, adaptive_subtraction, predictive_deconvolution, wiener_filter.
