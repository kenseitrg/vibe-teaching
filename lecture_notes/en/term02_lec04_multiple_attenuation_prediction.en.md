---
title: "Term 2 Lecture 04 — Multiple Attenuation II: Prediction Methods"
author: Seismic Data Processing Course
---

# Multiple Attenuation II: Predictive Deconvolution, SRME and Adaptive Subtraction

## Why this lecture matters

Session 1 ended with a scorecard full of caveats: move-out methods need a velocity contrast (fail at near offsets and in velocity inversions), assume hyperbolic events (fail under complex overburden) and distort AVO. Every one of those failures has the same root: the methods *discriminate* — they filter the multiples by how they *move*, so they can only work where primaries and multiples move differently.

This lecture changes the strategy completely: instead of filtering, **predict**. A multiple is the most predictable event in the record — it is *built from primaries* (Session 1, Section 2.1: times add, amplitudes multiply). If we can compute what the multiples should look like, we do not need any discrimination at all: we model them and subtract them.

The plan:

1. **Predictive deconvolution** — the prediction idea in its cheapest form, its offset-dependent fatal flaw, and the tau-p repair.
2. **SRME** (surface-related multiple elimination) — the prediction idea taken to its logical, fully data-driven conclusion: the data themselves are the prediction operator. From the 1D feedback diagram to the 2D matrix formulation.
3. **What SRME needs** — near offsets, regularity, the wavelet — and what to do when the survey does not provide them.
4. **Adaptive subtraction** — the engine that makes every model-and-subtract method work: Wiener matching filters in local windows, their parameters, and L1 vs L2.
5. **The shallow-water chain** — how all the tools of both sessions combine in one production flow.

Prerequisites: Session 1; predictive deconvolution and the Wiener filter (Term 1 Lec 06); FK and tau-p (Term 2 Lec 02).

---

## 1. From discrimination to prediction

The two fingerprints of Session 1 were *periodicity* and *excess moveout*. Kinematic methods exploited the second. The prediction family exploits the first — and, in SRME's case, its deeper meaning:

> A multiple is not merely *periodic*. It is **composed of primaries**: every surface multiple is two (or more) primary reflections connected at the surface. Predict the composition, and you have predicted the multiple — without a velocity model, without moveout, valid at all offsets including near offsets.

Two levels of exploiting this:

| Method | What it uses | What it needs |
|---|---|---|
| Predictive deconvolution | periodicity of the reverberation train | period of the generating layer (e.g., water depth) |
| SRME | full primary-composition | the complete dataset (all shots, all offsets) |

---

## 2. Predictive deconvolution, and why it fails at offset

### 2.1 The prediction gap (recall Term 1 Lec 06)

For a trace that contains a reverberating water layer, the prediction-error filter with **prediction gap** $\alpha$ = water period (in samples) predicts each reverberation from the previous one and subtracts it:

$$
f[n] \;=\; \delta[n] - h[n-\alpha],
\qquad \text{PEF output} = \text{trace} - \underbrace{(\text{trace} * h)}_{\text{prediction}}
$$

where $h$ solves the same Wiener normal equations we derived for deconvolution. With $h \approx R_\text{bot}\,\delta$ the ideal predictor is a *shift and a scale* — the filter does almost nothing to non-repeating events (primaries) and annihilates the periodic train. On a zero-offset trace, or a CMP trace at small offset, this works exactly as advertised.

![Figure: `figures/term01_lec06/term01_lec06_predictive_decon.png` — prediction gap and operator, from Term 1.](./figures/term01_lec06/term01_lec06_predictive_decon.png)

*Figure 1: Term 1 recap — the prediction gap $\alpha$ and the prediction operator. Predictive decon removes what repeats with period $\alpha$ and leaves everything else alone.*

### 2.2 The flaw: the period depends on the ray angle

The vertical period $\Delta t_0 = 2h_w/v_w$ is only measured by *vertical* rays. A slant path through the water layer takes longer per round trip:

$$
\Delta t(\theta) \;=\; \frac{\Delta t_0}{\cos\theta},
\qquad \sin\theta = p\,v_w .
$$

At far offsets the ray under a CMP gather is far from vertical: every order of the reverberation family follows its own hyperbola, and the *local* period stretches with offset. One constant gap cannot match a continuum of periods:

![Figure: `figures/term02_lec04/term02_lec04_period_vs_offset.png` — multiple period vs offset, and the tau-p repair.](./figures/term02_lec04/term02_lec04_period_vs_offset.png)

*Figure 2: Left: one water round trip at four emergence angles. Middle: a CMP reverberation train — the local period grows from 133 ms at zero offset to ~170 ms at far offset (annotate the arrows). A single prediction gap is wrong everywhere except one offset. Right: in the tau-p domain each trace holds ONE angle per family, and the intercept-time period is the known analytic function $\Delta\tau(p) = \Delta t_0\sqrt{1-p^2v_w^2}$.*

### 2.3 The repair: deconvolve in tau-p

The fix (Verschuur EET 03; standard production practice) is to transform the gather to the linear Radon (tau-p) domain — where the transform we built in Term 2 Lecture 02 organizes every event by ray parameter — and apply predictive deconvolution **trace by trace**:

- each $p$-trace contains one propagation angle per event family, so the reverberation period along it is *constant*, equal to the analytic $\Delta\tau(p)$;
- the gap for each $p$-trace is *computed from the water depth* — no picking, no data-driven estimation;
- a $p$-mute removes steep traces beyond the reflection family (where the angle assumption breaks and noise lives);
- inverse transform back to $x$-$t$.

![Figure: `figures/term02_lec04/term02_lec04_taup_decon.png` — tau-p predictive deconvolution.](./figures/term02_lec04/term02_lec04_taup_decon.png)

*Figure 3: The tau-p decon workflow. Input gather (reverberating water layer) $\to$ slant-stack tau-p panel (hyperbolas became ellipses; along each $p$-trace the period is constant) $\to$ per-trace predictive decon with the analytic gap + p-mute $\to$ single $p$-traces before/after (the periodic train collapses) $\to$ ACF evidence: the far-offset trace's autocorrelation shows smeared periods, a $p$-trace's ACF shows clean peaks at the known lag. The inverse transform uses the same LS machinery as the Radon demultiple of Session 1.*

### 2.4 The remaining limits — and the bridge to SRME

Tau-p decon fixes the *offset* problem, but two assumptions survive:

1. **The generator is locally flat (1D).** A dipping water bottom, or structure in any multiple-generating layer, means the "period" is not a single number even at fixed angle — it varies laterally along the propagation. The method cannot know the local dip from a $p$-trace alone.
2. **All the Wiener assumptions** (stationarity, minimum phase, white reflectivity, additive noise) still apply — they are inherited from the filter design, not from the multiple physics.

And one more structural limit: predictive deconvolution only ever exploits the *period* of one generating layer. It cannot predict a surface multiple whose two "legs" come from *different, distant* reflectors — a peg-leg with no short period at all. To predict those we must stop thinking in periods and start thinking in *compositions*. That is SRME.

---

## 3. SRME: the data predict the multiples

### 3.1 The 1D building block: times add, amplitudes multiply

Look again at the zero-offset picture of Session 1, now with a question: where does a first-order surface multiple of the water bottom *come from*? Answer: from the water-bottom primary, *twice*. The wave goes down to the seabed, comes back up (that is a primary — recorded), reflects off the free surface ($r_0 = -1$), goes down to the seabed again, comes back (a second primary-shaped leg). The multiple is the two legs glued at the surface reflection point:

$$
t_\text{mult} = t_1 + t_2, \qquad
A_\text{mult} = -\,A_1 \cdot A_2 .
$$

**Travel times add; amplitudes multiply** — that is the definition of *convolution*. A first-order multiple is (minus) the convolution of the primary response with itself; second order convolves three times; and so on:

$$
m_1(t) = -x_0(t)*x_0(t), \quad
m_2(t) = +x_0*x_0*x_0, \quad \dots
$$

![Figure: `figures/term02_lec04/term02_lec04_srme_1d_series.png` — the 1D SRME series.](./figures/term02_lec04/term02_lec04_srme_1d_series.png)

*Figure 4: The series in action on a three-reflector model. Panel 2: the measured data contain primaries plus all the cross-terms (peg-legs at 1.45 s, second orders at 1.85 s, ...). Panel 3: the first removal term $x*x$ — computed from the data alone — is precisely the multiples of order 1+. Panel 4: partial sums converge to the truth (relative residual 56% $\to$ 29% $\to$ 10%). No velocity model anywhere.*

### 3.2 The feedback diagram and its two solutions

The infinite family has a closed description. The measured response $x(t)$ is the multiple-free response $x_0(t)$ plus everything the surface mirror makes out of it — a **feedback system**: each loop through the surface convolves the current total response with $x_0$ once more:

$$
\boxed{\; x(t) \;=\; x_0(t) \;-\; x_0(t)*x(t) \;}
$$

(the minus sign is $r_0 = -1$). Two ways to use it:

- **Implicit (iterative) removal:** rearrange to $x_0 = x + x_0 * x$ — the primaries are the data minus their own multiple prediction — and solve by fixed-point iteration, starting with $x_0^{(0)} = x$:

$$
p_0^{(i+1)} \;=\; p \;-\; a * p_0^{(i)} * p ;
$$

- **Explicit (series) removal:** expand $x_0 = x + x*x + x*x*x + \dots$ (the Neumann series, like $\tfrac{1}{1+a} = 1 - a + a^2 - \dots$ but here with the signs already absorbed) — "multiple removal by auto-convolution and summation of the input".

Both are *fully data-driven*: the operator that predicts the multiples is the data themselves.

![Figure: `figures/term02_lec04/term02_lec04_srme_iterations.png` — iterative SRME convergence.](./figures/term02_lec04/term02_lec04_srme_iterations.png)

*Figure 5: The iterative scheme on a four-reflector model (moderate reflectivities; the iteration converges when the total reflectivity is "small enough"). Each pass strips one more order: residual 33% $\to$ 15% $\to$ 9% $\to$ 5% $\to$ 4% $\to$ 3%. Production runs typically use 2–3 iterations — most multiple energy is first-order.*

### 3.3 What the convolutions do to the wavelet

So far $x_0$ was an impulse response. Real data carry a source wavelet $s(t)$: $p = x_0 * s$. Convolving data with data convolves *wavelets with wavelets*: the naive prediction $-p*p$ carries **two** wavelets — longer in time, squared (therefore narrower) in spectrum — while the actual multiple carries one:

$$
p(t) \;=\; p_0(t) - a(t)*p(t)*p(t), \qquad
a(t) \;=\; -\,[s(t)]^{-1} .
$$

The **surface operator** $a(t)$ — an inverse source signature — must pre-scale every convolution step so each predicted order ends up carrying exactly one wavelet:

![Figure: `figures/term02_lec04/term02_lec04_srme_wavelet.png` — wavelet bookkeeping in SRME.](./figures/term02_lec04/term02_lec04_srme_wavelet.png)

*Figure 6: Top: the wavelet $s$, its self-convolution $s*s$ (what the naive prediction carries — visibly smeared), and the inverse-source operator. Middle: true multiple vs naive prediction vs operator-corrected prediction — the corrected one matches event by event. Bottom: spectra — the naive prediction has lost the high frequencies ($|S|^2$); the operator restores $|S|$.*

Two honest conclusions follow. First: $s(t)$ is never known perfectly, and the operator cannot know source/receiver directivity or 3D effects at all. Second: therefore **no production SRME subtracts its prediction directly** — the last step is always an adaptive match (Section 4). The surface operator gets the prediction *close*; adaptive subtraction closes the gap.

### 3.4 The 2D formulation: one trace at a time, summed over the surface

The 1D picture assumed vertical rays and flat layers. In 2D, take any recorded multiple on trace (source $x_s$, receiver $x_r$) and look at its raypath: it touches the free surface at some **downward reflection point** $x_k$. Cut the raypath there. The two pieces are:

- **leg 1:** a shot-gather trace — source $x_s$, *receiver* $x_k$ (the reflection arrives at the surface point $x_k$): $P(x_k, x_s)$;
- **leg 2:** a *receiver*-gather trace — source $x_k$ acting as a **virtual source**, receiver $x_r$: $P(x_r, x_k)$.

The multiple is the time-convolution of the two leg traces — and since we do not know where the true reflection point is, we sum over *all* surface points:

$$
\boxed{\;
M(x_r, x_s; f) \;=\; A(f) \int P(x_r, x_k; f)\; P(x_k, x_s; f)\; dx_k
\;}
$$

Per frequency slice this is a **matrix multiplication**: $\mathbf{M}(f) = A(f)\,\mathbf{P}(f)\,\mathbf{P}(f)$ — the data matrix times itself. The integrand as a function of $x_k$ is the **multiple contribution gather (MCG)**; its apex sits exactly at the true surface reflection point of each multiple event.

![Figure: `figures/term02_lec04/term02_lec04_srme_2d_drp.png` — the 2D SRME construction.](./figures/term02_lec04/term02_lec04_srme_2d_drp.png)

*Figure 7: The full 2D construction. (1) split the multiple at its DRP — leg 1 is a primary of the shot gather, leg 2 a "primary" from the virtual source; (2) the input shot gather with the water-bottom family and peg-legs; (3) the MCG for the target trace: each event's apex marks its true surface reflection point; (4) the MCG sum (predicted multiple) vs the actual multiples in the data — kinematics match to 8%; (5) model-and-subtract vs the true primaries.*

![Figure: `figures/term02_lec04/term02_lec04_real_srme_predicted.png` — field data: SRME prediction.](./figures/term02_lec04/term02_lec04_real_srme_predicted.png)

![Figure: `figures/term02_lec04/term02_lec04_real_srme_subtracted.png` — field data: after subtraction.](./figures/term02_lec04/term02_lec04_real_srme_subtracted.png)

*Figure 8: The same construction on field data (from the original deck): a shot gather, the SRME-predicted multiples, and the subtraction result. Note how the prediction gets the complex interfering families right — nothing here was interpreted by a human.*

What did SRME need to know? **Nothing about the subsurface.** No velocity model, no reflector geometry, no water depth. The price is paid in *data requirements* instead — the next section.

### 3.5 SRME's bill: near offsets, regularity, and the wavelet

The prediction is an integral over the whole surface. Whatever data are missing from the integral is missing from the prediction:

1. **Near offsets.** The shallow reverberation legs are short and flat; they live in the near-offset traces. Streamer surveys have a 100–250 m near-offset gap — the prediction of shallow water multiples is then too weak, exactly where the problem is worst. Fixes: near-offset reconstruction by Radon extrapolation of NMO-corrected CMPs; reciprocity; the shallow-water chain (Section 5).
2. **Regular, dense sampling.** Coarse shot spacing $\to$ spatial aliasing of the operator $\to$ prediction artifacts; irregular shooting $\to$ missing columns of the matrix. Fixes: shot interpolation, 5D regularization (Term 3 Lec 06 tools — this is *why* interpolation and demultiple are best friends in modern marine processing).
3. **The wavelet and directivity** $\to$ surface operator + adaptive subtraction (already discussed).
4. **Land data.** The raw operator data carry ground roll, statics, amplitude imbalance — unusable as a convolution operator. Production land SRME preprocesses a *copy* of the data (statics, ground-roll filter, amplitude balancing, lateral filtering) used only for prediction, then subtracts from the raw input. And there is a statics dilemma: multiples are generated at the *true* surface (apply no statics), while land data processing wants a datum (apply statics).
5. **Internal multiples.** SRME removes *surface-related* multiples only; interbed multiples need other machinery (beyond this course).

![Figure: `figures/term02_lec04/term02_lec04_srme_requirements.png` — SRME data requirements.](./figures/term02_lec04/term02_lec04_srme_requirements.png)

*Figure 9: Missing data = missing prediction. Row 1: complete data — the MCG is whole, prediction error 8%. Row 2: a 150 m near-offset gap — the MCG loses its flat legs, shallow reverberations are under-predicted. Row 3: every second shot missing — the MCG is decimated, aliasing-type artifacts contaminate the prediction.*

![Figure: `figures/term02_lec04/term02_lec04_real_srme_full.png` — field data: prediction from complete data.](./figures/term02_lec04/term02_lec04_real_srme_full.png)

![Figure: `figures/term02_lec04/term02_lec04_real_srme_no_near_offsets.png` — field data: prediction without near offsets.](./figures/term02_lec04/term02_lec04_real_srme_no_near_offsets.png)

*Figure 10: The same test on field data (from the original deck): prediction from complete data vs prediction when the near offsets are missing — the shallow part of the prediction degrades exactly where shallow-water multiples live.*

---

## 4. Adaptive subtraction: making model-and-subtract work

### 4.1 The problem it solves

Every prediction method ends the same way: we have data $d$ and a multiple model $m$ that is right in **kinematics** (the events are at the correct times, the correct moveout) but wrong in **dynamics** — amplitudes, wavelet phase, directivity, 3D propagation effects. Direct subtraction $d - m$ leaves residuals; a single scalar cannot fix a wavelet. The universal answer is a **matching filter**: estimate a short filter $a(t)$, in local windows, such that $a * m$ fits the multiples in $d$, and subtract the *filtered* model.

The estimation is exactly the Wiener problem of Term 1 Lecture 06 — the same normal equations, a new job:

$$
\min_{a} \sum_n \big( d[n] - (a*m)[n] \big)^2
\qquad\Longrightarrow\qquad
\mathbf{R}_{mm}\,\mathbf{a} \;=\; \mathbf{r}_{dm}
$$

with $\mathbf{R}_{mm}$ the autocorrelation matrix of the model (Toeplitz, solved by Levinson) and $\mathbf{r}_{dm}$ the cross-correlation of data and model, both summed in the local window.

![Figure: `figures/term02_lec04/term02_lec04_adaptive_subtraction.png` — adaptive subtraction workflow and worked example.](./figures/term02_lec04/term02_lec04_adaptive_subtraction.png)

*Figure 11: Left: the workflow — data and multiple model enter, matching filters are estimated in local space-time windows (autocorrelation and cross-correlation per window, Wiener solve), the adapted model is subtracted. Right: a worked example — the model has the wrong amplitude ($\times$1.4), a 6 ms delay and a different wavelet. Direct subtraction damages the primary by 133%; the 11-sample matching filter absorbs amplitude + phase + wavelet error and the primary survives (4% damage).*

### 4.2 The parameters — and how they interact

Adaptive subtraction is parameter-rich, and the parameters are not independent:

- **Filter length.** Long enough to absorb the wavelet error (rule of thumb: the wavelet's length); every sample beyond that is freedom for the filter to fit *signal* instead of noise. With a perfect model, even a long filter is harmless; with an imperfect one, a long filter starts *shaping the model into the data* — primaries included.
- **Window size (time and space).** Small windows adapt to local errors but each filter is estimated from little data — unstable, and worse: inside a small window the filter can chase primaries too. Large windows are stable and safe but cannot follow lateral variations (directivity, amplitude trends). The filter must also be short relative to the window.
- **Two-stage strategy** (standard): first *large* windows to estimate one global inverse-wavelet filter (naturally done in common-offset gathers — one filter per offset); then *small* windows for local amplitude/directivity corrections (naturally in shot domain).
- **Iteration**: model $\to$ subtract $\to$ re-predict from the cleaner data $\to$ subtract (the iterative SRME loop of Figure 5).

### 4.3 L1 vs L2 — the norm is a physical statement

The least-squares filter minimizes output *energy*. That is correct **if the output contains only signal uncorrelated with the model** — then the best fit of the model is the true multiple. But where a *primary overlaps the multiple*, the L2 filter faces a conflict: reducing the residual there means removing primary energy too (the output is "supposed" to be small). The filter compromises — and both suffers: residual multiple leakage *and* primary damage.

The L1 norm, $\sum |e[n]|$ instead of $\sum e[n]^2$, penalizes large residuals *less*: the samples where a primary interferes are treated as **outliers** to tolerate, not errors to eliminate. The filter is then driven by the clean multiple-only samples, and the primary survives the overlap. The cost: the problem becomes non-linear — solved by **iteratively re-weighted least squares** (IRLS: re-solve with weights $1/(|e|+\delta)$, exactly the same machinery as the high-resolution Radon of Session 1 — the pattern "L2 + sparsity/robustness weights" strikes again).

![Figure: `figures/term02_lec04/term02_lec04_l1_vs_l2.png` — L2 vs L1 subtraction and the filter-length trap.](./figures/term02_lec04/term02_lec04_l1_vs_l2.png)

*Figure 12: Top: a primary overlapping a multiple, model nearly right. The L2 filter (one window, long filter) eats 27% of the primary — its compromise at the overlap; the L1 filter keeps it (1% damage). Bottom: the filter-length trap from the original deck: with a good model, short and long filters both behave; with a bad model (wrong kinematics), a short filter leaves residuals while a long filter shapes the bad model into the data and removes primaries. Filter length is a statement about how much you trust your model.*

![Figure: `figures/term02_lec04/term02_lec04_real_adaptive_subtraction.png` — field data: adaptive subtraction.](./figures/term02_lec04/term02_lec04_real_adaptive_subtraction.png)

*Figure 13: Field-data adaptive subtraction (from the original deck): data, multiple model, and the adaptively subtracted output. The same engine closes the loop of every model-and-subtract method in this course — SRME here, surface-wave removal in Term 3.*

**Toolbox summary** (Verschuur's closing table):

| Method | Strengths | Weaknesses |
|---|---|---|
| L2 subtraction | fast, robust, easy | problems at crossing events |
| L1 subtraction | handles interference | slower, non-linear |
| curvelet-domain separation | discriminates by local dip + frequency | assumes no overlap; cost |

"A processor needs a toolbox approach."

---

## 5. The shallow-water chain: everything together

Very shallow water (30–80 m) is the hardest demultiple environment: the water period (40–110 ms) is *shorter than the wavelet* — reverberation fog that no event-based method can see — while deeper surface multiples are ordinary long-period events. No single tool from these two lectures can do both jobs:

![Figure: `figures/term02_lec04/term02_lec04_shallow_water_strategy.png` — the shallow-water demultiple chain.](./figures/term02_lec04/term02_lec04_shallow_water_strategy.png)

*Figure 14: A shallow-water synthetic (h = 50 m) walked through the chain. Stage 0: primaries + short-period fog + one long-period surface multiple. Stage 1: tau-p predictive decon collapses the fog (multiple content 87% $\to$ 47%) but the long-period event survives — it has no short period. Stage 2: SRME-style prediction (with the water-bottom primary muted, per the standard recipe) + windowed adaptive subtraction removes it ($\to$ 39%; the rest is short-period residue around the strong primaries). Bottom: the production chain (after EET 06): swell-noise/bad traces $\to$ wavelet decon + deghosting $\to$ FK filtering of post-critical water-bottom events $\to$ predictive decon (water layer) $\to$ shot interpolation + near-offset reconstruction $\to$ SRME $\to$ Radon for residuals.*

Note what the chain teaches: the tools of Session 1 and Session 2 are not competitors but **stages** — each handles the family of multiples whose physics it exploits, and hands a cleaner dataset to the next.

---

## 6. The method map — closing both sessions

| | Discrimination (Session 1) | Prediction (Session 2) |
|---|---|---|
| Physics | moveout / dip difference | periodicity; primaries compose multiples |
| Velocity model needed | yes (NMO) | no |
| Near offsets | weakest there — muted | essential *input* (SRME) / handled (tau-p decon) |
| Wavelet knowledge | irrelevant | surface operator + adaptive subtraction |
| Data requirements | modest | SRME: complete, dense, regular |
| Typical failures | inversions, non-hyperbolicity, AVO damage | structural generators (tau-p decon), land data + gaps (SRME), model-trust issues (subtraction) |
| Cost | cheap–moderate | moderate (decon) – high (SRME) |
| Removes | long-period multiples with moveout difference | water-layer reverberations (decon); all surface multiples (SRME) |

There is no silver bullet: internal multiples need their own machinery (beyond this course), and every serious survey combines at least two of the tools above — usually Radon *and* SRME *and* a decon somewhere in the chain.

---

## Summary

- **Prediction beats discrimination where physics is adverse**: near offsets, velocity inversions, complex structure. The price: prediction needs either a period (decon) or the whole dataset (SRME).
- **Predictive decon** removes periodic trains with gap $\alpha$ = layer period; the period varies with angle ($\Delta t(\theta) = \Delta t_0/\cos\theta$), so at offset it fails — unless the data are first organized by angle: **tau-p decon**, gap $= \Delta t_0\sqrt{1-p^2v_w^2}$ per trace, p-mute, inverse. Remaining limits: locally flat generator, Wiener assumptions.
- **SRME**: every surface multiple is primaries glued at the surface — times add, amplitudes multiply $\to$ convolution. Feedback relation $x = x_0 - x_0*x$; iterative removal $p_0^{(i+1)} = p - a*p_0^{(i)}*p$; 2D prediction per frequency: $M(x_r,x_s) = A\int P(x_r,x_k)P(x_k,x_s)\,dx_k$ — matrix multiplication, MCG apexes mark the true reflection points. No subsurface model.
- **SRME's bill**: near offsets (Radon reconstruction), regular dense sampling (interpolation/5D), wavelet/directivity (surface operator $a = -1/s$ + adaptive subtraction), land preprocessing, internal multiples out of scope.
- **Adaptive subtraction**: Wiener matching filter in local windows ($\mathbf{R}_{mm}\mathbf{a} = \mathbf{r}_{dm}$); parameters interact — filter length = model trust, window size = adaptivity vs stability, two-stage (global wavelet in common offset, local in shot). **L1 vs L2**: L2 assumes minimum-energy output (fails at interference, ~27% primary damage in our example); L1 treats interference samples as outliers (1% damage), via IRLS — the same re-weighting as high-resolution Radon.
- **The chain**: shallow water = decon (fog) + SRME (long-period) + Radon (residuals); "a processor needs a toolbox approach."

## Comprehension questions

1. Water depth 75 m, $v_w = 1500$ m/s, 40 Hz minimum-phase wavelet. (a) Compute the vertical period. (b) At what offset does a CMP ray under the seabed reach 30° emergence, and what is the reverberation period there? (c) Which method would you choose, and what gap?
2. Explain, in one paragraph each, why (a) SRME needs near offsets while (b) Radon demultiple mutes them. What does each fact follow from?
3. The SRME prediction of a first-order multiple over-predicts amplitudes by a factor 2 and is 5 ms late. Direct subtraction fails. Describe exactly what the adaptive matching filter does, which parameters you would pick, and what could go wrong if the filter is too long.
4. Why does the L2 adaptive filter damage primaries exactly where primaries and multiples interfere, and why does the L1 norm fix this? Name the iterative scheme and the other lecture where you have already met it.
5. Your marine dataset has a 200 m near-offset gap over 60 m of water. Sketch the demultiple chain you would run and which tool removes which multiple family at each stage.

## References and further reading

- Verschuur, D. J. (2006). *Seismic Multiple Removal Techniques: Past, Present and Future* — EAGE EET course. Chapters 3 (Predictive deconvolution), 5 (Principles of SRME), 6 (Practical aspects of SRME), 7 (Adaptive subtraction). `wiki/sources/verschuur_2006_predictive_deconvolution.md`, `wiki/sources/verschuur_2006_eet05_principles_srme.md`, `wiki/sources/verschuur_2006_eet06_practical_srme.md`, `wiki/sources/verschuur_2006_eet07_adaptive_subtraction.md`
- Berkhout, A. J. & Verschuur, D. J. (1997). Estimation of multiple scattering by iterative inversion, Part I: Theoretical considerations. *Geophysics*, 62(5), 1586–1595. (The SRME theory paper.)
- Verschuur, D. J., Berkhout, A. J. & Wapenaar, C. P. A. (1992). Adaptive surface-related multiple elimination. *Geophysics*, 57(9), 1166–1177.
- Guitton, A. & Verschuur, D. J. (2004). Adaptive subtraction of multiples using the L1-norm. *Geophysical Prospecting*, 52, 27–38.
- Hampson, D. (1986) — Session 1's Radon workflow; the inverse-transform machinery shared by both lectures.
- Companion derivation: [SRME from the feedback diagram — series, iteration and the surface operator](../derivations/srme_feedback_derivation.en.md)
- Wiki concepts: [SRME](../../wiki/concepts/srme.md), [Multiples](../../wiki/concepts/multiples.md), [Adaptive subtraction](../../wiki/concepts/adaptive_subtraction.md), [Predictive deconvolution](../../wiki/concepts/predictive_deconvolution.md), [Wiener filter](../../wiki/concepts/wiener_filter.md)
