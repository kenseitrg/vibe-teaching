---
title: "Term 2 Lecture 02 — Linear Noise Attenuation: FK and Tau-P"
author: Seismic Data Processing Course
---

# Linear Noise Attenuation: FK and Tau-P

## Why this lecture matters

Every processor has seen a raw shot gather from a land survey: a few faint hyperbolas underneath a thick, slow, low-frequency fog of ground roll, plus some crisp straight-line arrivals cutting across everything. The reflections and the noise live at the **same times** and in **overlapping frequency bands**, so nothing we learned in Term 1 Lecture 5 (frequency filtering) can separate them. What *does* separate them is a property we have been measuring all along but never used as a filter axis: **apparent velocity** — the dip of an event across the gather.

To filter by dip we need a domain where dip is visible: the **frequency–wavenumber (FK) domain** and the **linear Radon (tau–p) domain**. These two domains are the workhorses of coherent-noise attenuation, and — as we will prove — they are the *same transform* written in two coordinate systems. Between them sits the single most important practical obstacle in the whole subject: **spatial aliasing**, the reason steep noise on routinely sampled data masquerades as signal and defeats naive dip filters.

We will look at:

1. Noise taxonomy: random vs coherent, and the coherent linear-noise family this lecture targets.
2. The FK spectrum: how it is built, why a dip is a radial line ($p = k/f$), and why reflections form fans.
3. Spatial aliasing: the spatial Nyquist, the alias frequency $f_\text{alias} = V_\text{app}/(2\Delta x)$, and why it breaks noise attenuation.
4. FK filter types: k-cut, dip fan, narrow dip-reject, polygonal masks — plus tapers, low-frequency protection, and QC discipline.
5. The linear Radon transform: slant stacking, how events map, and why reflections become **ellipses** $\tau(p) = t_0\sqrt{1-p^2V^2}$.
6. Aliasing and filtering in tau-p.
7. The exact connection between FK and tau-p (the Fourier slice theorem) and the equivalence of filters in the two domains.
8. The inverse Radon transform: why summing back is not enough, the **rho filter**, and a teaser for least-squares transforms.

One synthetic shot gather — reflections plus ground roll plus an air blast — will follow us through the whole lecture, so that by the end you have seen the same data in every domain, filtered in two of them, and put back together.

---

## 1. Noise types: coherent vs random

### 1.1 What counts as noise

Noise is any recorded energy that is not the signal for the *current* objective. The definition is deliberately relative: a surface wave is noise for reflection processing, but it is the *signal* for near-surface shear-velocity studies (Term 3 Lecture 03 will treat it as a treasure). In this lecture, "signal" means reflection energy and "noise" means everything else on the gather.

The first split every processor must make:

| | **Random noise** | **Coherent noise** |
|---|---|---|
| Behavior trace-to-trace | Unpredictable | Predictable, modelable |
| Examples | Wind, cultural activity, swell, instrument noise, spiking | Ground roll, air blast, guided waves, side scatter, multiples |
| Why it can be removed | It does not correlate from trace to trace | It follows a *model* — a traveltime law, a dip, a periodicity |
| Removal principle | Stack, predict-and-subtract (Term 3 Lec 04) | Separate by kinematics (dip, moveout) or dynamics (amplitude, frequency), or model and subtract |

**Random noise** cannot be predicted from trace to trace, so suppression exploits exactly that: stacking averages it down; prediction filters cannot reproduce it and subtract it. Those tools belong to Term 3.

**Coherent noise** is the opposite: it is *predictable*. Ground roll arrives along a straight line in the shot gather with an apparent velocity of 250–500 m/s. An air blast crosses the record at roughly the speed of sound. A multiple repeats the shape of the water bottom. Because each of these obeys a model, we can hope to separate them from reflections — *if* we can find a domain in which the model predicts something different from the reflections. That domain is the subject of this lecture.

### 1.2 The coherent-noise families

- **Source-generated linear noise** — ground roll (the Rayleigh-wave train: slow, low-frequency, high amplitude), the air blast, and guided waves trapped in near-surface layers. On a shot gather these appear as straight-line events fanning out from the source. This family is the subject of this lecture.
- **Side-scattered energy** — waves scattered from near-surface heterogeneities (karst, fault zones, infrastructure): linear events with scattered apparent velocities, often crossing the reflections at steep angles. Same treatment as above.
- **Multiples** — predictable by periodicity and by their moveout. They deserve their own lecture (Term 2 Lecture 03), where the tau-p domain we build today returns as the main stage.
- **The first-break zone** — direct and refracted arrivals near the top of the record. Usually handled by muting, not filtering; but the same dip ideas apply.

Real gathers mix all of these with the random background (Figure 1).

### 1.3 Why transforms, and where this sits in the flow

The lecture often references one synthetic example: three reflection hyperbolas, a ground-roll cone, an air blast and random background noise. The reflections (hyperbolas) and the noise (straight lines) overlap completely in time, and their amplitude spectra overlap in frequency: ground roll dominates 5–25 Hz, but so does much of the reflection energy. No 1-D filter can separate them, because a 1-D filter treats every trace independently and never looks *across* traces.

The one property that separates them is geometric: **dip**. Reflections are flat to moderately dipping; ground roll and air blast are steep. Dip is a spatial property, so we need a transform that looks across traces: a two-dimensional transform in which dip becomes an axis or a ray direction. This lecture builds two: the FK transform, where a dip is a *radial direction*, and the tau-p transform, where a dip is an *axis*.

In the processing flow, linear-noise attenuation sits early: on prestack gathers (shot or receiver domain, often also CMP) after amplitude recovery and statics, and before detailed velocity analysis, demultiple and stack. Cleaner gathers give better deconvolution design windows, more reliable velocity picks, and a better stack. Like most noise tools it is applied *before* the steps that assume the data are mostly signal.

![Figure: `slides/raw/noise_types.png` — the four noise families, from the original deck.](../../slides/raw/noise_types.png)

*Figure 1: From the original deck: the four noise families on real records — random noise, coherent linear noise, multiples, and the first-break zone. Random noise never repeats from trace to trace; everything else follows a model — a dip, a velocity, a periodicity — and that is precisely what makes it separable from reflections.*

---

## 2. The FK spectrum

### 2.1 From one trace to a whole gather

Recall Term 1 Lecture 5: the 1-D Fourier transform decomposed a single trace into frequencies, $d(t) \rightarrow D(f)$. Now we have a gather $d(t, x)$ — a function of time *and* offset. Apply the Fourier transform in time (each trace separately), then apply it again in space (across traces, at each frequency). The result is the **2-D Fourier transform**, the FK spectrum:

$$
D(f, k) = \iint d(t, x)\, e^{-2\pi i (f t - k x)}\, dt\, dx
$$

The new axis is the **wavenumber** $k$: spatial frequency, cycles per meter. Where frequency counts oscillations per second along a trace, wavenumber counts oscillations per meter *across* the gather. Two unit systems are in common use, and you will meet both in software and in papers:

- $k$ in **cycles/m** — the physical unit, natural when offsets are in meters;
- $k$ in **cycles/trace** — the processing unit, in which the meaningful limits are simply $\pm 0.5$ (you will see why in Section 3).

They are related by $k\,[\text{cycles/trace}] = k\,[\text{cycles/m}] \times \Delta x$.

A useful mental image, worth keeping for the rest of the course: the FK transform decomposes the gather into **plane waves**. Each point $(f, k)$ of the spectrum is one plane-wave component — one temporal frequency travelling at one spatial oscillation rate.

### 2.2 Building intuition: one plane wave

Take the simplest event that exists across traces: a **linear event** — a plane wave arriving at the surface. It is a wavelet $s$ stretched along a straight line, written compactly as

$$
d(t, x) = s(t - p x),
$$

where $p = dt/dx$ is the **slope**: the delay added per meter of offset. Slope is the inverse of apparent velocity, $V_\text{app} = 1/p$ — the speed at which the event sweeps across the surface array.

How does this event appear in FK:

1. **Transform over time.** At each offset the wavelet has the same spectrum $S(f)$; only its arrival delay differs. At a single frequency $f$, the complex amplitude across offsets is a **sinusoid in $x$**: each trace is delayed by $p x$ seconds, i.e. rotated in phase by $f \cdot p x$ cycles. One frequency, one spatial sinusoid.
2. **Transform over space.** A sinusoid in $x$ has a single wavenumber — and the delay law tells us which one: $k = p f$.

So a linear event occupies a **line through the origin**, with slope fixed by the event's dip:

$$
\boxed{\; p = \frac{dt}{dx} = \frac{k}{f}, \qquad V_\text{app} = \frac{1}{p} = \frac{f}{k} \;}
$$

Three consequences you should internalize:

- **Slope is a ratio.** A 20 Hz component at $k = 0.010$ cycles/m and a 40 Hz component at $k = 0.020$ cycles/m are the *same dip* ($p = 0.5$ ms/m, $V_\text{app} = 2000$ m/s). Doubling $f$ and doubling $k$ changes nothing about the event's direction — only about its pitch. This is why the FK picture of a dip is a ray from the origin, not a point.
- **Horizontal and vertical trade places.** A horizontal event in $(x, t)$ has $p = 0$, so all its energy sits on the $f$-axis ($k = 0$): vertical in FK. A very steep event hugs the $k$-axis: nearly horizontal in FK.
- **All events of one apparent velocity share one radial line**, no matter their arrival times or wavelets — they differ only in phase along that line.

![Figure: `figures/term02_lec02/term02_lec02_fk_plane_wave.png` — construction of the FK spectrum for plane waves.](./figures/term02_lec02/term02_lec02_fk_plane_wave.png)

*Figure 2: Plane waves in t-x and in FK, at $\Delta x = 12.5$ m. Left: three linear events — two gentle, reflection-like dips ($p = 0.25$ and $0.50$ ms/m) and one steep, air-blast-like dip ($p = 1.5$ ms/m; $V_\text{app} = 667$ m/s). Right: the FK amplitude spectrum. The two gentle events are single clean radial lines $k = pf$ through the origin, well inside the panel; steeper dip → larger $|k|$ at the same $f$. The steep event's line reaches the $k = +0.5$ cyc/trace edge at $f_\text{alias} = 26.7$ Hz and wraps around to $k = -0.5$: above $f_\text{alias}$ its energy re-enters the spectrum from the opposite edge, masquerading as an apparent dip of the opposite sign — spatial aliasing, Section 3's subject.*

### 2.3 Reflections and linear noise in FK

A reflection hyperbola is not a straight line — but any *piece* of it nearly is. Zoom into a window of offsets and the hyperbola is a quasi-linear segment with the local slope of that window: flat near the source, steepening with offset toward the straight-line asymptote of slope $1/V$. (In Term 1 we made this precise without saying so: the tangent to the hyperbola at offset $x$ has slope $p = x / V^2 t(x)$.)

So think of a reflection as a **continuum of linear segments**, one per tangent. Each tangent segment maps to its own radial line in FK. The family of tangents, from the flat near-offset slopes up to the steep far-offset ones (the asymptote $1/V$), sweeps out a **fan** — approximately a triangular region between the lines $k = p_\text{near} f$ and $k = p_\text{far} f$ (Figure 3). Deeper reflections (larger $t_0$, larger $V$) have flatter fans: their steepest tangent slope, the asymptote $1/V$, is smaller.

The linear noise, meanwhile, is honest about what it is: ground roll at 300 m/s is a single radial line $k = f/300$ — steep, and since ground roll is low-frequency, its energy hugs the low-$f$ part of that line: a **low-frequency, high-$|k|$ wedge**. The air blast at 600 m/s is a slightly gentler line. The amplitude at a point $(f, k)$ has a clean meaning: *the energy at frequency $f$ travelling at dip $k/f$*.

Now the central difficulty of the subject is visible in one picture: the steep side of the reflection fan and the ground-roll wedge **overlap**. At low frequencies and steep dips, signal and noise occupy the same FK cells. A dip filter can remove the wedge only up to where the reflections are not; below that, surgery must be partial. And there is a second problem hiding in Figure 3, at the left and right edges of the spectrum — the wrapped skirts of the ground-roll wedge. That is spatial aliasing, and it is important enough to deserve its own section.

![Figure: `figures/term02_lec02/term02_lec02_fk_reflection_fan.png` — reflections as tangent fans in FK.](./figures/term02_lec02/term02_lec02_fk_reflection_fan.png)

*Figure 3: The running gather and its FK amplitude spectrum. Left: three offset windows on the shallow reflection with their local tangent dips — flat near the source ($p = 0.04$ ms/m), steepening with offset ($0.17$, $0.27$ ms/m) toward the asymptote $1/V$. Right: each colored segment maps to the color-matched radial line $k = pf$; together the tangents sweep out the reflection fan between the $f$-axis ($p \approx 0$) and the steep far-offset edge ($p_{\max}$, dashed white; its mirror on the negative-$k$ side comes from the real-valued data). The ground roll is the steep low-frequency wedge wrapping around the $\pm k_N$ spectrum edges — Section 3 explains it.*

---

## 3. Spatial aliasing

### 3.1 The spatial Nyquist

Term 1 Lecture 5 established the sampling theorem in time: sample a signal at interval $\Delta t$, and only frequencies below the Nyquist $f_N = 1/(2\Delta t)$ are representable; anything above **folds back** into the band, disguising itself as a lower frequency. Field systems apply analog anti-alias filters *before* digitization, so properly recorded seismic data are essentially never aliased in time.

Spatial sampling gets no such rescue. There is no "analog filter in space" before the wavefield is sampled by a receiver array: the geophones are where they are, at spacing $\Delta x$, and that is that. The spatial Nyquist wavenumber is

$$
\boxed{\; k_N = \frac{1}{2 \Delta x} \;\; = 0.5 \ \text{cycles/trace} \;}
$$

Any event component that requires $|k| > k_N$ folds back into $[-k_N, +k_N]$, exactly as an over-Nyquist frequency folds in time.

Now apply this to an event with apparent velocity $V_\text{app}$. Its components satisfy $k = f / V_\text{app}$ — the faster the event, the gentler the line. Aliasing begins when $k$ crosses $k_N$:

$$
\frac{f}{V_\text{app}} > \frac{1}{2\Delta x}
\qquad\Longleftrightarrow\qquad
\boxed{\; f_\text{alias} = \frac{V_\text{app}}{2\, \Delta x} \;}
$$

A steep event delayed by $\Delta t$ per trace looks "smooth" only while that delay is under half a period, $\Delta t < T/2 = 1/(2f)$; since $\Delta t = \Delta x / V_\text{app}$, the same formula follows. **Slow events alias first**: the steeper the dip, the lower the frequency at which the folding starts.

### 3.2 Worked numbers — why land data are in trouble

Plug the running example's numbers in, with $\Delta x = 25$ m:

- **Ground roll, $V_\text{app} = 300$ m/s:** $f_\text{alias} = 300 / (2 \times 25) = \mathbf{6\ Hz}$. The ground-roll band  can reach up to 25 Hz — *the entire event is aliased almost from its first cycle*. Its high-frequency part does not sit on the steep line $k = f/300$; it wraps repeatedly around the $\pm k_N$ edges and re-enters the spectrum at moderate, reflection-like dips. 
- **The same ground roll at $\Delta x = 12.5$ m:** $f_\text{alias} = 12$ Hz. Halving the trace spacing doubles $k_N$; now the lower half of the band is clean.
- **A reflection, $V_\text{app} = 2500$ m/s:** $f_\text{alias} = 2500/(2\times25) = 50$ Hz. Reflections are safely unaliased across the whole useful band — the survey was *designed* for the reflections. Nobody designed it for the noise.

![Figure: `figures/term02_lec02/term02_lec02_spatial_aliasing.png` — spatial aliasing of a steep linear event.](./figures/term02_lec02/term02_lec02_spatial_aliasing.png)

*Figure 4: The example ground roll ($V_\text{app} = 300$ m/s, band 6–25 Hz) at two trace spacings. Left, $\Delta x = 4$ m: $f_\text{alias} = 37.5$ Hz lies above the band — the design rule $\Delta x < V_\text{app}/(2 f_\text{max})$ of Section 3.3 is satisfied, nothing wraps, and in FK the energy is one clean radial line $k = f/V$ (white). Right, $\Delta x = 25$ m: $f_\text{alias} = 6$ Hz (Section 3.2's worked number) — the whole band wraps, and in FK the energy forms a sawtooth of parallel red segments crossing the entire k range, right through the dips where reflections live; in t-x the per-trace delay (83 ms ≈ one period at 14 Hz) flips the apparent dip trace-to-trace — shown in the zoom inset.*

### 3.3 Why aliasing breaks noise attenuation — and what to do

Once ground-roll energy has wrapped, it sits at $(f, k)$ points that reflections also occupy. It is **indistinguishable from signal dips** — not because our filter is bad, but because the recorded numbers genuinely are the same. A dip filter now faces a dilemma: remove the wrapped noise and amputate the reflection dips with it, or spare the reflections and keep the noise. This is why aliased coherent noise is the classic *acquisition* failure that processing inherits.

The remedies, in order of preference:

1. **Do not acquire the aliasing** — receiver spacing small enough that the *noise*, not the signal, is unaliased: $f_\text{alias} > f_\text{max}(V_\text{noise})$ requires $\Delta x < V_\text{noise} / (2 f_\text{max})$; e.g. 300 m/s at 25 Hz forces $\Delta x < 6$ m. Costly, which is why it is often not done.
2. **Interpolate before filtering** — densify the data (de-alias it) in processing, then dip-filter. Interpolation in the FK/Radon world is a Term 3 Lecture 06 topic; the tau-p "smart interpolator" of Section 5 is a hint of it.
3. **Cut the wrapped energy with a k-filter** (Section 4): if the wrapped noise lands at $|k|$ beyond the reflection fan, a wavenumber cut removes it cheaply.
4. **Use tools that tolerate aliasing** — sparsity-based and prediction-based methods (Term 3 Lecture 04).

---

## 4. FK filters

### 4.1 The general recipe

FK filtering is Term 1 Lecture 5's frequency filtering with one more dimension:

1. forward 2-D FFT of the gather (or a window of it);
2. multiply the FK spectrum by a designed **amplitude mask** — 1 in pass zones, 0 in reject zones, smooth in between;
3. inverse FFT back to t-x.

The design logic comes straight from Section 2: to filter **dips** you pass or reject radial **sectors**; to filter **frequencies**, horizontal **bands**; and any combination of the two is an arbitrary **polygon** in the $(f, k)$ plane. Four standard masks cover nearly all practical needs.

### 4.2 The four standard masks

**1. The k-filter (anti-alias cut).** Zero the spectrum beyond a wavenumber limit, $|k| > k_\text{cut} \le k_N$ — the spatial twin of a temporal low-pass filter. Two uses: before **decimation** (dropping or interpolating traces to a coarser grid, you must first remove the wavenumbers the new grid cannot carry), and as the cheap cure for wrapped noise: if aliased ground roll has folded to $|k|$ outside the reflection fan, a k-cut removes it without touching signal dips.

**2. The dip filter (velocity filter).** Pass a fan of slopes $|p| < p_\text{max}$, reject outside it. The mask boundaries are radial lines through the origin; the reject wedge takes away ground roll and air blast while the reflection fan passes. The *workhorse* of linear-noise attenuation — and the filter most betrayed by aliasing (Section 3.3).

**3. The narrow dip-reject.** The surgical version: reject a narrow cone around one slope, e.g. $p \approx 1/350$ s/m for the air blast. Minimal signal damage, but only when the noise occupies a slope range the signal does not visit.

**4. The polygonal filter.** An arbitrary polygon lets you combine dips and frequencies: reject the ground-roll wedge *below 30 Hz only*; keep a low-frequency protection corridor; carve the reflection fan out of the reject zone. This is the form production software actually exposes.

Every mask needs **tapers**: abrupt 0/1 boundaries in FK ring in t-x — the 2-D Gibbs effect from Term 1 Lecture 5, now wrapping around all four edges of the gather. Soft transitions over a few percent of the axes are cheap insurance.

![Figure: `figures/term02_lec02/term02_lec02_fk_filter_types.png` — the four standard FK filter masks.](./figures/term02_lec02/term02_lec02_fk_filter_types.png)

*Figure 5: The four standard masks in the (f, k) plane of the running example ($\Delta x = 25$ m, so $k_N = 0.5$ cyc/trace). Blue = pass, red = reject, cosine-tapered in between; dashed guides mark each mask's design boundaries — the $k_\text{cut}$ of the anti-alias cut, the 0.45–0.60 ms/m slope limits of the dip fan, the air-blast slope of the narrow reject, and, on the polygonal mask, the 30 Hz top of the reject wedge and its low-frequency protection corridor around $k = 0$: at very low frequencies the cut spares the region near zero wavenumber instead of pinching to the origin. Notice also how little of the panel the air-blast cone occupies: above $f_\text{alias} = V/(2\Delta x) = 12$ Hz that slope is aliased and wraps to other apparent dips (Section 3), so the surgical reject only sees its low-frequency foot.*

### 4.3 Low-frequency protection and the QC discipline

A naive dip-reject fan through the origin has a side effect: it removes **all low-frequency energy inside the noise cone**, including the low frequencies of the reflections — precisely the band that broadband processing (Term 3 Lecture 05) fights to preserve. Production masks therefore soften the fan: the reject wedge may start above a frequency floor, widen gradually, or leave a protected corridor along the $f$-axis. The design rule: *reject the noise's (dip, frequency) combination, not the noise's dip at every frequency.*

Quality control is not optional, and it is the same in every domain of this lecture:

- Always inspect **before / after / difference** panels — in t-x *and* in the transform domain.
- The difference panel is your noise model. It must look like the noise you meant to remove: linear events, the right dips and frequencies. Reflection arcs in the difference mean your mask ate signal — fix the mask, not the data.
- Where amplitude fidelity matters (AVO, 4D), prefer **model-and-subtract** over zero-out: transform, *keep only the noise* (reject the signal), transform back — you now have a noise model in t-x — and subtract it from the input. Any residual mismatch leaves a small error instead of a zeroed hole; adaptive subtraction (Term 3 Lecture 03) polishes this further. 

![Figure: `figures/term02_lec02/term02_lec02_fk_filter_application.png` — dip-fan FK filter applied to the running gather.](./figures/term02_lec02/term02_lec02_fk_filter_application.png)

*Figure 6: The dip-pass fan applied to the running gather — the QC triplet in action. Top: input, output, and difference in t-x; bottom: the FK spectra of exactly these three panels, with the applied fan edge overlaid (dashed). The difference is the noise model: ground roll and air blast, nothing reflection-shaped. In FK, the output keeps the reflection fan inside the dashed boundary while the difference collects the steep energy outside it.*

---

## 5. Linear Radon transform — the tau-p domain

### 5.1 Slant stacking: summing along dips

The FK transform made dip a *direction*. The Radon transform makes it an *axis*. The **linear Radon transform** — the **slant stack** — is one line of mathematics:

$$
\boxed{\; u(\tau, p) = \sum_{j} d(\tau + p\, x_j,\; x_j) \;}
$$

Read it as an operation: pick a trial slope $p$; shift trace $j$ earlier by $p x_j$ (a linear moveout, LMO, with velocity $1/p$); sum all shifted traces. Energy that actually travelled at slope $p$ lines up flat after the shift and **sums constructively**; everything else smears. The result is one output trace, indexed by intercept time $\tau$, living at this $p$. Repeat for a range of $p$ values (positive and negative) and you have the **tau-p panel** $u(\tau, p)$: a gather reorganized from "one trace per offset" to "one trace per dip".

The coordinates have clean physical meanings. The $p$ axis is slowness — the ray parameter of a plane wave, conserved through a layered earth by Snell's law (a tau-p trace is a genuine *plane-wave response*; this is why tau-p gathers are also called plane-wave gathers). The $\tau$ axis is the intercept time at zero offset. Sign convention, as in the original deck: an event whose arrival time grows with offset has $p > 0$.

The idea is old and multinational: Radon's 1917 mathematics, Rieber's 1936 "controlled directional sensitivity" — delayed analog recordings summed into steered traces — and the CDR (*controlled directional reception*) method developed extensively in the USSR. A slant stack is Rieber's steering, done digitally for all steering angles at once.

### 5.2 How events map

Take a linear event with slope $p_0$ and intercept $\tau_0$. When the trial $p$ equals $p_0$, the event is flattened by the LMO and the sum piles all its energy at $\tau = \tau_0$; at any other $p$ it is misaligned and averages toward zero. Hence the first mapping law:

$$
\text{linear event } (\tau_0, p_0) \text{ in t-x} \;\longrightarrow\; \textbf{one point } (\tau_0, p_0) \text{ in tau-p.}
$$

Refinements that matter in practice:

- Several linear events **with the same slope** but different intercepts all focus onto the **same p-trace** — at different $\tau$. A p-trace is "all energy that ever crossed the array at this dip".
- Compare with FK, where the same event lives on an entire radial line. Tau-p **focuses** linear events: fewer non-zero samples, i.e. a *sparser* representation. This is the first appearance of a key idea: choose the transform in which your data is sparse.
- The inverse mapping also holds: a linear event in tau-p maps to a point in t-x. The transform treats lines symmetrically in both directions.

![Figure: `figures/term02_lec02/term02_lec02_taup_mapping.png` — slant-stack construction and event mapping.](./figures/term02_lec02/term02_lec02_taup_mapping.png)

*Figure 7: Slant stacking three linear events. For each trial $p$, traces are shifted by $p x$ and summed. When the trial slope matches an event, the sum spikes (constructive stacking); otherwise the event smears. Each event ends as a focused point on its own p-trace at its intercept time.*

### 5.3 Why reflections become ellipses

A reflection hyperbola is not one slope — it is a *family* of slopes, one per tangent. So run the argument of §5.2 not on the hyperbola but on each tangent segment: the tangent with slope $p$ focuses at intercept $\tau(p) = t - p x$, where $x$ is the tangent point. The tau-p image of the hyperbola is the locus of all its tangents — the **envelope**. Find it with two lines of algebra (differentiate $t(x) = \sqrt{t_0^2 + x^2/V^2}$):

$$
p = \frac{dt}{dx} = \frac{x}{V^2 t(x)} \quad\Rightarrow\quad x = p V^2 t .
$$

Substitute into the hyperbola equation $t^2 = t_0^2 + x^2/V^2$:

$$
t^2 \left(1 - p^2 V^2\right) = t_0^2
\quad\Rightarrow\quad
\boxed{\; \tau(p) = t - p x = t_0 \sqrt{1 - p^2 V^2}, \qquad |p| \le \frac{1}{V} \;}
$$

— an **ellipse** with apex at $(t_0, p=0)$ that closes on the $\tau = 0$ axis at $p = \pm 1/V$ (Figure 8). The deep reflections never reach large $|p|$; the steepest tangent any reflection offers is its asymptote $1/V$.

![Figure: `figures/term02_lec02/term02_lec02_taup_ellipse.png` — the reflection ellipse in tau-p.](./figures/term02_lec02/term02_lec02_taup_ellipse.png)

*Figure 8: A hyperbola (left) maps to an ellipse in tau-p (right). Tangent lines of the hyperbola, drawn at several offsets, each focus to a point on the ellipse: slope $p$ on the horizontal axis, intercept $\tau(p)$ on the vertical. The ellipse closes at $p = \pm 1/V$ — but a finite cable offers tangent points only up to $|p| = x_\text{max}/(V^2 t_\text{max}) \approx 0.31$ ms/m, so the image fades before the closing point.*

Everything we need for noise separation is now on one panel:

- **Linear noise focuses to points at fixed large $|p|$** (ground roll at $1/300$ s/m $\approx 3.3$ ms/m; air blast at $\approx 1.7$ ms/m), typically low $\tau$, broad in amplitude.
- **Reflections live inside their ellipses**, which close by $|p| = 1/V_\text{min} \approx 0.33$–$0.45$ ms/m for our  velocities.
- Between the reflection closing points and the noise points there is, when velocities are favorable, a **no-man's-land that only random noise occupies** — the mute zone of Section 6. When the noise cone overlaps the ellipses' steep flanks, surgery must again be partial — the same overlap caveat as in FK, because (Section 7) the two domains are one.

Two remarks for the curious. The ellipse is the linear-transform version of a general fact: each Radon variant maps events it does not match into envelopes — Bickel (2000) and Maeland (1998) derive the corresponding envelope curves for the hyperbolic and parabolic transforms, where a hyperbola maps to another hyperbola-like arc or focuses to a point when transform and event match. 

---

## 6. Aliasing and filtering in tau-p

### 6.1 Aliasing and artifacts in tau-p

The slant stack looks immune to aliasing — it sums in t-x, no FFT across traces anywhere. Two separate effects say otherwise.

**First: p-aliasing.** At a fixed frequency $f$, each offset contributes a phase $e^{2\pi i f p x}$ to the sum; as $p$ varies, this phase twists faster for far offsets. Sampling the $p$ axis too coarsely aliases this twist, just like sampling a sinusoid in time. The anti-alias condition involves the largest offset and the highest frequency:

$$
\Delta p \;\le\; \frac{1}{2\, x_\text{max}\, f_\text{max}}
\qquad\text{(rule of thumb: } \Delta p \approx \frac{\Delta k_x}{f_\text{max}} = \frac{1}{f_\text{max}\, L} \text{ over aperture } L\text{)}
$$

For example: $x_\text{max} = 1475$ m, $f_\text{max} = 100$ Hz gives $\Delta p \lesssim 3.4\ \mu$s/m. Over a typical noise-dip range of $\pm 4$ ms/m that is some 2400 p-values — far more than the 60 traces we started with. The tau-p panel is (and should be) an **oversampled** representation; undersampling it in $p$ produces periodic replica artifacts. 

**Second: finite aperture.** The sum runs over a finite cable, not an infinite line. Truncation in $x$ is convolution in $p$: every focused point acquires side lobes smeared along the $p$ direction, and events near the aperture edges (shallow tangent points at far offsets, in particular) suffer most. The practical symptoms are recognizable once you have seen them once (Figure 9):

- spurious energy at **opposite-sign $p$** — steep noise leaking to the wrong side of the panel;
- energy at **very large $\tau$**, beyond any real event — steep summation lines crossing many traces of edge-parallel energy;
- for wrapped (t-x-aliased) input events, a subtlety worth knowing: the aliased frequencies of a linear event **stay on the same p-trace** as the unaliased ones — they do *not* appear at negative $p$ as intuition might suggest (Yilmaz §6.3 demonstrates this). Tau-p does not un-mix aliased energy; it merely relocates it.

**Cheap fix:** a temporal **low-pass filter** (before or after the transform) removes the high-frequency components that violate the $\Delta p$ condition — at the cost of bandwidth, exactly like an anti-alias filter in time. **Proper fix:** sample $p$ finely enough, choose the $p$ range to cover only the dips present in the data (empty steep p-traces only add aperture artifacts), and taper the aperture edges before transforming. Yilmaz's parameter experiments are the classical reference: $n_p$ of the order of the trace count is a safe baseline; oversampling $p$ beyond that neither hurts nor helps; too coarse $\Delta p$ or too wide a $p_\text{max}$ injects coherent artifacts into the reconstruction.

![Figure: `figures/term02_lec02/term02_lec02_taup_aliasing.png` — aliasing artifacts in tau-p.](./figures/term02_lec02/term02_lec02_taup_aliasing.png)

*Figure 9: The input gather (left). Transformed with too-coarse p-sampling ($\Delta p$ = 0.4 ms/m, middle): artifacts appear as coherent energy at opposite-sign p and very large $\tau$, and the whole panel is weaker — leaked away by the undersampled transform. With adequate $\Delta p$ and a low-pass filter (right), the panel shows what it should: three reflection ellipses (dashed) and the focused linear-noise points at $p = 1/V$. Both tau-p panels share one dB scale (reference: the clean panel's maximum; only the two noise foci clip at the top).*

### 6.2 Filtering in tau-p

With a clean panel, filtering is the same recipe as ever — design a mute, apply, transform back (the inverse is Section 8):

- **p-mute:** zero the region beyond the reflection ellipses' closing points ($|p| > 1/V_\text{min}$, generously tapered) — removes focused linear noise wholesale;
- **$\tau$-p windows:** combine the p-mute with a time floor (e.g. spare the shallow part of the panel), or mute only a dip band containing a specific noise train;
- **taper every edge** — the same Gibbs logic as FK, and production practice is explicit about it: the case study in the references used 200 ms tapers and *no sharp corners* on its tau-p mutes, because hard edges ring when transformed back to t-x.

QC is identical to Section 4.3 — before / after / **difference** panels; the difference must be the linear noise (Figure 10). Figure 10 stages both outcomes deliberately: the air blast is low-frequency enough to be unaliased at this $\Delta x$ (its bandwidth ends exactly at $V_\text{ab}/(2\,\Delta x)$, the aliasing threshold), so it focuses entirely at $p = 1/V_\text{ab}$ and the mute removes it completely; the ground roll is aliased, and its wrapped 10–16 Hz components stack inside the keep zone — $p = 1/V_\text{gr} - 1/(f\,\Delta x)$ lands at $|p| < 0.6$ ms/m — leaving residuals in the result. Dip filtering needs unaliased (or low-pass-filtered) input: the same lesson as Section 6.1. And the same strategic choice exists: mute the noise and inverse-transform the *signal* (zero-out), or mute the signal and inverse-transform the *noise* as a model to subtract — the amplitude-preserving route described in Section 4.3.

When to choose tau-p over FK? They are one transform in two coordinate systems (next section), so the separation power is the same in principle. In practice: FK masks are natural when the noise's full $(f, k)$ shape matters (frequency-selective wedges, wrapped-energy surgery); tau-p mutes are natural when the decision is a pure dip decision, independent of frequency — and they generalize (parabolic, hyperbolic variants) where FK does not. 

![Figure: `figures/term02_lec02/term02_lec02_taup_mute.png` — tau-p mute application.](./figures/term02_lec02/term02_lec02_taup_mute.png)

*Figure 10: Tau-p mute on the running gather, with the air blast made unaliased (6 Hz dominant: its bandwidth ends at $V_\text{ab}/(2\Delta x)$, the aliasing threshold; the ground roll stays aliased). The input gather (left); its tau-p panel with the mute zone beyond the ellipses (second); after mute and inverse transform, in t-x (third); the difference = the removed noise (right). The unaliased air blast vanishes completely — all of its energy lands at $p = 1/V$, inside the mute. The aliased ground roll leaves residuals: its wrapped 10–16 Hz components stack inside the keep zone $|p| < 0.6$ ms/m.*

---

## 7. FK and tau-p: one transform, two coordinate systems

Here is the pay-off of the whole lecture: nothing new is needed to connect the two domains — one substitution does it.

Take the tau-p panel and Fourier transform it **along $\tau$ only**, at each $p$. Call the result the **f–p spectrum** $U(f, p)$. Now compute it from the definition of the slant stack (substitute $t = \tau + p x$ and swap the order of integration):

$$
U(f, p) = \int u(\tau, p)\, e^{-2\pi i f \tau}\, d\tau
= \iint d(x, t)\, e^{-2\pi i f (t - p x)}\, dt\, dx
= \boxed{\; D\!\left(f,\; k = p f\right) \;}
$$

The 1-D Fourier transform over $\tau$ of the slant stack at slope $p$ equals the FK spectrum evaluated **along the radial line $k = p f$**. This is the **Fourier slice theorem** (the mathematics behind medical tomography, among other things). Its consequences:

- **FK and f–p are the same spectrum in different coordinates.** Rectangular $(f, k)$ versus "polar" $(f, p)$: a radial fan through the origin of FK is a *horizontal band* of $p$-values in f–p (Figure 11). The radial-line picture (FK) and the focused-point picture (tau-p) are two snapshots of this one object: a point in tau-p spreads into the line $k = pf$ once you Fourier-transform over $\tau$.
- **Filters translate across domains.** A dip-reject fan in FK is a p-band reject in f–p, and approximately a p-mute in tau-p ("approximately" because the f–p version can be made frequency-dependent, while a tau-p mute cannot — the mute applies to all frequencies of the p-trace at once).
- **There is an amplitude price.** The coordinate change $(f, k) \to (f, p)$ with $k = pf$ is not area-preserving: cell areas scale with $f$, so spectra in the two coordinate systems differ by a factor of frequency. That factor — the ramp $|f|$ — is precisely the **rho filter** that the inverse Radon transform will demand in the next section. 

| operation in t-x | FK version | f–p version | tau-p version |
|---|---|---|---|
| reject dips $\|p\| > p_\text{max}$ | fan reject | reject $\|p\| > p_\text{max}$ (horizontal band) | p-mute beyond $p_\text{max}$ |
| keep a frequency band | horizontal band | horizontal band (same $f$ axis) | *not expressible as a mute* — per-frequency only in f–p/FK |
| remove one noise velocity | narrow radial cone | narrow vertical p-stripe | spike mute on one p-trace |

![Figure: `slides/raw/ft_taup.png` — the FK ↔ f–p connection, from the original deck.](../../slides/raw/ft_taup.png)

*Figure 11: From the original deck: the same spectrum in two coordinate systems. In FK, a linear event is a region of constant slope — energy along the radial line $k = pf$; in tau-p it is a point on the trace of that $p$. Fourier-transforming the tau-p panel over $\tau$ gives the f–p spectrum, and FK ↔ f–p is then nothing but the coordinate change $k = pf$: radial fans in FK become horizontal $p$-bands in f–p, and a point in tau-p is the line $k = pf$ seen from the other axis.*

---

## 8. Inverse Radon and the rho filter

### 8.1 Why you cannot just "sum back"

We have been casually writing "inverse transform" since Section 6. Time to look at it. The natural candidate is the **adjoint** — run the slant stack backwards, summing the p-traces along the same lines:

$$
d_\text{adj}(t, x) = \sum_j u(t - p_j x,\, p_j)\, \Delta p .
$$

For the discrete, finite-aperture, finite-p data of the real world, the adjoint is **not** the inverse. Round-trip a gather through slant stack and adjoint and you get a recognizable but **smeared, low-frequency-flavored** copy: amplitudes decay, wavelets stretch, side lobes trail the events (Figure 12, top row). The deck's demonstration is worth reproducing mentally: a clean linear event goes to tau-p and back; the reconstruction is duller than the input, with broadened, asymmetric wavelets.

This is a familiar moral from deconvolution (Term 1): **the transpose of a forward operator is almost never its inverse.** The 2-D DFT pair is the lucky exception — forward and backward DFT are exact inverses, which is why FK filtering (Section 4) needed no such discussion. The discrete tau-p pair is genuinely incomplete: no set of discrete p-values covers the $(f, k)$ grid uniformly, so the round trip always loses something.

### 8.2 The rho filter

What exactly does the adjoint lack? Go back to Section 7: the exact inverse requires *reassembling* the FK spectrum from radial slices, and the change of variables $k = pf$ brings $dk = f\,dp$ — a factor of frequency that the plain adjoint does not apply. Doing the algebra properly gives the **filtered back projection** formula:

$$
d(t, x) = \alpha(t) \ast \sum_j u(t - p_j x,\, p_j)\, \Delta p,
\qquad \alpha(f) = |f|
$$

— the adjoint slant stack **followed by a convolution whose frequency response is the ramp $|f|$**. This convolution is the **rho filter** ($\rho$-filter).

In practice: before the inverse transform, multiply the amplitude spectrum of **each p-trace** by $|f|$ — cheap, stable, standard. A light Gaussian taper of the ramp toward Nyquist keeps interpolation noise in the top octave from being boosted along with the signal. The result (Figure 12, right column): in t-x the wavelets regain bandwidth and symmetry, and in the tau-p view — where the input's events are focused points on an empty background, so the adjoint's $1/|f|$ smear cannot hide along event lines — the points come back, and the $\tau$-slice spikes recover their height. Production implementations apply the rho filter as a built-in part of the inverse tau-p.

What the rho filter does **not** fix: the smearing *along p* caused by finite aperture and coarse $\Delta p$ — events remain slightly defocused and side-lobed in the p direction. Two remedies exist, both pointing beyond this lecture: a **p-direction deconvolution** that compensates the finite array length (Zhou & Greenhalgh 1994), or treating the whole transform as an **inversion** problem.

### 8.3 Teaser: least-squares and high-resolution Radon

The clean way to invert is the way we learned in Term 1 for deconvolution: set up **least squares**. Treat the slant stack as a forward operator $R$ (per frequency, a matrix between the $x$-traces and the $p$-traces) and solve for the tau-p panel that best reproduces the data:

$$
\min_\phi \lVert R\,\phi - d \rVert^2
\quad\Longrightarrow\quad
\phi = (R R^*)^{-1} R\, d ,
$$

The LS panel reconstructs with far fewer artifacts than the adjoint, because the inversion explicitly undoes the operator's smearing — and with a sparsity constraint on $\phi$ it becomes the **high-resolution Radon transform**, which focuses reflections and noise into tight, separable blobs. This is the door to several Term 3 topics: Radon interpolation of missing traces (the "smart interpolator" of Section 5, made rigorous), de-aliased Radon on irregularly sampled data, and the general principle of *sparsity in a transform domain* that underlies modern noise attenuation. For poorly sampled data the plain transform is actively dangerous — see Marfurt et al. (1996), "Pitfalls of using conventional Radon transforms on poorly sampled data". We will build the LS machinery in Term 3 Lecture 06.

![Figure: `figures/term02_lec02/term02_lec02_inverse_radon_rho.png` — inverse Radon with and without the rho filter.](./figures/term02_lec02/term02_lec02_inverse_radon_rho.png)

*Figure 12: The rho filter, seen in both domains. Top row: the t-x round trip — input; adjoint only (events smeared, low-frequency-flavored); adjoint with the rho filter ($|f|$ ramp, Gaussian-tapered toward Nyquist, applied per p-trace before the inverse). Middle row: the same three datasets in tau-p (the round trips forward-transformed back): the input's events are focused points; the adjoint-only round trip smears them along $\tau$; the rho filter restores them. Bottom: a $\tau$ = 0.55 s slice across p on a common amplitude scale — without rho the spikes lose height and broaden; with rho the input slice is recovered.*

---

## Summary

- Noise splits into **random** (uncorrelated trace-to-trace; stack/predict) and **coherent** (modelable; separate by kinematics or dynamics). This lecture's target: **linear coherent noise** — ground roll, air blast, guided waves, side scatter — separated from reflections by **apparent velocity (dip)**.
- **FK** = 2-D Fourier transform; a plane wave $s(t - px)$ lives on the radial line $k = pf$: $p = k/f$, $V_\text{app} = f/k$. Reflections are locally linear → **fans** between their near-offset and asymptotic dips. Ground roll: steep, low-frequency wedge. Overlap of wedge and fan is the intrinsic difficulty.
- **Spatial aliasing**: $k_N = 1/(2\Delta x)$; an event aliases above $f_\text{alias} = V_\text{app}/(2\Delta x)$. Surveys are sampled for signal, so the *slow noise aliases first* (300 m/s at 25 m → 6 Hz!). Wrapped noise sits at reflection dips and defeats dip filters. Check FK panels of raw shots before promising attenuation; then denser sampling, de-aliasing interpolation, k-cuts, or aliasing-tolerant methods.
- **FK filters**: 2-D mask × spectrum. k-cut (anti-alias), dip fan, narrow dip-reject, polygonal. Taper everything (2-D Gibbs); protect the low frequencies inside the noise cone; QC with before/after/**difference**; prefer model-and-subtract where amplitudes matter.
- **Tau-p** = slant stack: linear event → **point** at $(\tau_0, p_0)$; hyperbola → **ellipse** $\tau(p) = t_0\sqrt{1-p^2V^2}$, $|p| \le 1/V$. Noise focuses at large $|p|$ beyond the ellipses → p-mutes. Artifacts from coarse $\Delta p$ (condition $\Delta p \le 1/(2 x_\text{max} f_\text{max})$) and finite aperture; symptoms: opposite-sign p, huge $\tau$.
- **FK and f–p are one spectrum in two coordinates** (slice theorem $U(f,p) = D(f, pf)$): fan $\leftrightarrow$ p-band $\leftrightarrow$ mute, with an amplitude price — the $|f|$ ramp.
- **Inverse Radon** = adjoint + **rho filter** (per-trace $|f|$ ramp; the tomography/Kirchhoff ramp). The adjoint alone smears. Remaining p-smearing → p-deconvolution or **least-squares / high-resolution Radon** (Term 3).

## Comprehension questions

1. Classify as coherent or random: ground roll, swell noise, air blast, a water-layer multiple, side scatter from a shallow fault. Which of these does this lecture address, and by which property?
2. A linear event shows 4 ms of moveout per trace with $\Delta x = 25$ m. Compute $V_\text{app}$, $p$, and $k$ at 30 Hz — in cycles/m and in cycles/trace. Is the event spatially aliased at this frequency? At which frequency does it start to be?
3. Why can a dip filter not remove aliased ground roll, and why is that as much an *acquisition* failure as a processing one? Give two processing-side remedies and their costs.
4. Explain, in geometric terms, why a hyperbola maps to an ellipse in tau-p while a linear event maps to a point. Compute the $p$-extent of the ellipse for a reflection with $t_0 = 2$ s and $V = 2500$ m/s.
5. State the Fourier slice theorem and use it to explain why a dip-reject fan in FK corresponds to a horizontal band in f–p and to a p-mute in tau-p. Where does the $|f|$ factor come from, and which filter of this lecture is it?

## References and further reading

- Margrave, G. F. (2006). *Methods of Seismic Data Processing* (Geophysics 557 lecture notes), University of Calgary, §§2-53–2-76. `wiki/sources/margrave_2006_methods_of_seismic_data_processing.md`
- Yilmaz, Ö. (2001). *Seismic Data Analysis*, Vol. 2, §6.3 (slant-stack transformation). `wiki/sources/yilmaz_2001_seismic_data_analysis_taup.md`
- Taner, M. T., Koehler, F., Alhilali, K. A. & Sherwood, R. D. (1990). Aliasing in the tau-p transform and the removal of spatially aliased coherent noise. *Geophysics*, 55(9), 1496–1503.
- Zhou, B. & Greenhalgh, S. A. (1994). Linear and parabolic $\tau$-p transforms revisited. *Geophysics*, 59(7), 1133–1149. `wiki/sources/zhou_greenhalgh_1994_linear_parabolic_taup.md`
- Bickel, S. H. (2000). Focusing aspects of the hyperbolic Radon transform. *Geophysics*, 65(2), 652–655. `wiki/sources/bickel_2000_hyperbolic_radon_focusing.md`
- Maeland, E. (1998). Focusing aspects of the parabolic Radon transform. *Geophysics*, 63(5), 1708–1715. `wiki/sources/maeland_1998_parabolic_radon.md`
- Treitel, S., Gutowski, P. R. & Wagner, D. E. (1982). Plane-wave decomposition of seismograms. *Geophysics*, 47(10), 1375–1401.
- Marfurt, K. J., Schneider, R. V. & Mueller, M. C. (1996). Pitfalls of using conventional Radon transforms on poorly sampled data. *Geophysics*, 61(5), 1467–1482.
- Gower, R. (2003). Optimising tau-p for noise & multiple suppression: a North Sea example. WesternGeco inTouch. `wiki/sources/gower_2003_intouch_taup.md`
- CGG ODT02 *De-noise* course, Parts 3–4 (K-filter; linear noise removal / tau-p). `wiki/sources/cgg_odt02_denoise.md`
- Companion derivation: [FK–tau-p connection and the rho filter](../derivations/fk_taup_connection_and_rho_filter_derivation.en.md)
