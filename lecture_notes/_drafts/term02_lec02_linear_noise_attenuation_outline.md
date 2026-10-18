# Term 2 Lecture 02 — Linear Noise Attenuation (FK and Tau-P): Lecture Outline

## Overview

**Duration:** 90 minutes
**Topic:** Coherent linear noise (ground roll, air blast, guided waves) and the two transform domains designed to remove it: the frequency–wavenumber (FK) domain and the linear Radon (tau–p) domain. Spatial aliasing as the central practical obstacle. Filter types in both domains, the exact connection between the two transforms, and the inverse Radon problem with the rho filter.
**Prerequisites:**
- Term 1 Lecture 05 (1D Fourier transform, Nyquist frequency, temporal aliasing, filter types and tapers)
- Term 1 Lecture 04 (NMO, RMS velocity — needed for the reflection ellipse in tau-p)
- Term 1 Lecture 06 (deconvolution — only for positioning noise attenuation in the flow)
**Slide deck base:** `slides/raw/fk_taup.pptx` (RU, 34 slides, image-rich; covers all planned topics)
**Downstream consumers:** Term 3 Lecture 04 (noise attenuation algorithms — assumes FK, tau-p, dip filtering), Term 3 Lecture 03 (surface waves — FK fan mention), Term 3 Lecture 06 (regularization/interpolation — LS/high-resolution Radon teaser lives here)

**Pedagogical device:** one synthetic shot gather (reflections + ground roll cone + air blast + random background) is followed through the whole lecture: built in Section 1, transformed to FK in Section 2, aliased in Section 3, filtered in Section 4, transformed to tau-p in Section 5, muted in Section 6, and reconstructed in Section 8. Figure scripts share the same parameters so students recognize the same data everywhere. Each script remains self-contained (per project rules).

---

## Section 1: Noise taxonomy — coherent vs random (8 min)

### 1.1 What counts as noise (3 min)
- Definition: noise = recorded energy that is not the signal for the *current* objective (a surface wave is signal for MASW, noise for reflection processing — foreshadows Term 3 Lec 03)
- **Random noise:** unpredictable trace-to-trace (wind, cultural activity, swell, instrument noise). Suppression exploits lack of correlation: stacking, prediction filtering → mostly Term 3 Lec 04
- **Coherent noise:** predictable / modelable from trace to trace. Suppression exploits a *model*: separate by kinematics (apparent velocity / dip) or dynamics (amplitude, frequency), or model and subtract

### 1.2 The coherent-noise families (3 min)
- Source-generated **linear noise**: ground roll (Rayleigh), air blast, guided/refracted cones — the subject of this lecture
- **Side-scattered** energy: near-surface heterogeneities → linear events with scattered slopes
- **Multiples**: predictable by periodicity/moveout — separate lecture (Term 2 lecture 3)
- The first-break zone on shot gathers — mostly muted, not filtered
- Raw deck slide 2 (four noise examples) as real-data illustration

### 1.3 Why transforms, and where in the flow (2 min)
- In t-x these events overlap in time and frequency; their distinguishing property is **apparent velocity (dip)** — a *spatial* property. We need a domain where dip is an axis: FK and tau-p
- Typical position: prestack (shot or CMP domain) after amplitude recovery and statics, before detailed velocity analysis / demultiple; cleaner gathers → better decon design windows, velocity picks, and stacks
- **Figure 1:** raw deck slide 2 image (`slides/raw/noise_types.png`): the four noise families on real records; the synthetic running example is defined in text (§1.3 table) and first shown in Figure 3

---

## Section 2: The FK spectrum (15 min)

### 2.1 From 1D to 2D Fourier transform (4 min)
- Recall Term 1 Lec 05: temporal DFT of one trace → f axis. FK = temporal FT *then* spatial FT across traces → (f, k) plane
- 2D transform pair (statement, no derivation):
  $$D(f, k) = \iint d(t, x)\, e^{-i 2\pi (f t + k x)}\, dt\, dx$$
- Reading the axes: f in Hz; k in cycles/m (or cycles/trace on regular gathers — both conventions appear in software; raw deck uses cycles/trace)

### 2.2 Building intuition: one plane wave (5 min)
- Step-by-step construction (raw deck slides 3–6): a linear event $d(t,x) = s(t - p x)$; Fourier over t → per-frequency complex traces; at one frequency, the event is a **sinusoid in x**; its spatial frequency is the wavenumber k
- Worked numbers from the deck: f = 20 Hz, k = 0.08 → slope; k = 0.16 at the same f → twice the slope; f = 30 Hz with k = 0.24 → *same* slope → slope depends on the ratio, not on f or k alone
- The slope relation (derive inline, 3 lines):
  $$\boxed{\; p = \frac{dt}{dx} = \frac{k}{f}, \qquad V_\text{app} = \frac{1}{p} = \frac{f}{k} \;}$$
- A linear event of slope p → **radial line k = p·f through the origin** of the FK plane; steeper dip → wider fan
- **Figure 2:** plane waves in t-x → radial lines in FK: two unaliased events (clean k = p·f lines) + one steep aliased event wrapping at ±k_N, f_alias annotated (mirrors deck slides 3–7)

### 2.3 Reflections and linear noise in FK (6 min)
- A reflection hyperbola is **locally linear**: over a limited offset window it is a quasi-linear segment with window-dependent slope (near offsets → steep; far offsets → flat; raw deck slides 8–10)
- Each tangent segment → energy along its radial line → the family of tangents fills a **fan-shaped (roughly triangular) region** from the flat near-offset slopes to the steep far-offset ones (asymptote 1/V) (deck slide 11)
- Intensity at a point (f, k) = energy at frequency f propagating at dip k/f
- Ground roll: slow (250–500 m/s), low-frequency (5–30 Hz) → a **low-f, high-|k| cone** that overlaps the reflection fan's steep side — this overlap is the whole difficulty
- **Figure 3:** running gather + FK spectrum; near/mid/far offset windows with their local dips, each color-matched to its radial line in FK; fan edge and wrapped ground-roll wedge annotated (mirrors deck slides 8–11)

---

## Section 3: Spatial aliasing (12 min)

### 3.1 Spatial Nyquist (4 min)
- Term 1 Lec 5 recap: sampling a sinusoid at Δt aliases frequencies above $f_N = 1/(2\Delta t)$ — nothing about the *time* sampling changes here
- Spatial sampling at trace spacing Δx: highest representable wavenumber
  $$\boxed{\; k_N = \frac{1}{2 \Delta x} \;\; \left(= 0.5 \text{ cycles/trace}\right) \;}$$
- An event with apparent velocity $V_\text{app}$ needs $k = f / V_\text{app}$; it aliases when $f/V_\text{app} > 1/(2\Delta x)$:
  $$\boxed{\; f_\text{alias} = \frac{V_\text{app}}{2\, \Delta x} \;}$$
  (same algebra as the deck's T/2 = 1/(2·f_alias), dt per trace = 1/(2·f_alias))

### 3.2 Worked numbers — why land data are in trouble (3 min)
- Ground roll $V_\text{app} = 300$ m/s, Δx = 25 m → $f_\text{alias}$ = **6 Hz**: the entire ground-roll band is aliased
- Same ground roll with Δx = 12.5 m → 12 Hz: halving Δx doubles $k_N$ (deck slides 16–17)
- Reflection $V_\text{app} = 2500$ m/s, Δx = 25 m → 50 Hz: reflections are safe where the survey was designed for them — but the *noise* was not designed for
- **Figure 4:** the running example's ground roll (300 m/s) unaliased at $\Delta x$ = 4 m (f_alias = 37.5 Hz above the band: one clean radial line) vs fully aliased at 25 m (f_alias = 6 Hz: sawtooth wrap across k); t-x zoom inset shows the per-trace dip flip (mirrors deck slides 12–15)

### 3.3 Why aliasing breaks noise attenuation (5 min)
- Aliased ground roll appears at *reflection-like* dips → a dip filter cannot remove it without removing signal; the wrapped energy is indistinguishable from steep signal dips at the same (f, k)
- Remedies: (a) never let aliased noise in — denser receiver spacing (cost!), (b) k-domain anti-alias cut (Section 4), (c) de-aliasing by interpolation before filtering (Term 3 Lec 06 teaser), (d) methods that tolerate aliasing (Term 3 Lec 04 teaser)
- Message: **spatial aliasing is a design and QC issue first, a filtering issue second** — check FK panels of raw shots before promising any noise attenuation

---

## Section 4: FK filter types (12 min)

### 4.1 The general recipe (2 min)
- Forward 2D FFT → multiply by a designed amplitude mask → inverse FFT → back to t-x; exact 2D analog of Term 1 Lec 05 frequency filtering, now with a 2D mask
- Design rule from Section 2: to pass/reject dips, pass/reject **radial sectors**; to pass/reject frequencies, horizontal bands; combinations → polygons

### 4.2 The four standard masks (6 min)
1. **K-filter (anti-alias cut):** zero |k| > k_N (or a chosen fraction) — the spatial analog of the temporal low-pass; use before decimation/trace dropping; also the cheap fix when noise is aliased: cut the wrapped energy with the *signal* dips preserved
2. **Dip filter (velocity filter):** pass a fan of slopes (e.g. keep |p| < p_max) — remove steep linear noise while passing the reflection fan
3. **Dip-reject / narrow slope band:** remove a narrow cone at the noise's slope (e.g. the air blast at one apparent velocity) — surgical, minimal signal damage
4. **Polygonal filter:** arbitrary polygon in (f, k) — combine a dip fan with frequency limits; the practical general form in real software (e.g. reject the ground-roll cone only below 30 Hz, keep everything else)
- All masks need **tapers** (soft edges) — Gibbs ringing recap from Term 1 Lec 05; 2D ringing is uglier: it wraps around the frame

### 4.3 Low-frequency protection and QC (4 min)
- Problem (deck slides 19–20): a naive dip-reject fan through the origin removes the noise cone *and* the low-frequency energy inside it — the low frequencies we now fight to preserve (broadband processing, Term 3 Lec 05)
- Variants: fan that starts above a floor frequency, low-frequency "protection" zone with relaxed slopes, amplitude-preserving soft fans
- QC discipline: always inspect **before / after / difference** panels and their FK spectra — the difference must look like the noise model (linear events), not like reflections; amplitude-preserving workflows prefer *model-and-subtract* over *zero-out* (adaptive subtraction is Term 3 Lec 03)
- **Figure 5:** mask gallery (k-cut, dip-pass fan, dip-reject band, polygonal, low-f-protected fan) with design guides (mirrors deck slides 16–18)
- **Figure 6:** dip-fan application to the running gather: before/after/difference in t-x and FK (mirrors deck slides 19–20)

---

## Section 5: Linear Radon transform — the tau-p domain (15 min)

### 5.1 Slant stack: summing along dips (5 min)
- Definition (forward linear Radon):
  $$\boxed{\; u(\tau, p) = \sum_{j} d(\tau + p\, x_j,\; x_j) \;}$$
- For each trial slope p, shift each trace by p·x and sum → one **p-trace** indexed by intercept time τ; the full transform repeats for a range of p (positive p = arrival time grows with offset; deck slide 24 convention)
- Physical meaning: τ = intercept at zero offset, p = slowness (1/V_app) — the same slope we read in FK, but now it is an **axis**, not a ray direction

### 5.2 How events map (5 min)
- Linear event with slope $p_0$, intercept $τ_0$ → **a single point** at $(τ_0, p_0)$: all its energy sums in phase only there (deck slide 23)
- Several linear events with the same slope but different intercepts → **one p-trace**, focused at different τ (deck slide 24)
- Contrast with FK (where a linear event is a radial *line*): tau-p **focuses** linear events to points → sparser representation → easier surgical removal; this is the "sparse transform" idea that Term 3 Lect 04/06 generalize

### 5.3 Why reflections become ellipses (5 min)
- A hyperbola $t(x) = \sqrt{t_0^2 + x^2/V^2}$ is the envelope of its tangent lines; each tangent segment is a linear event with slope p(x) and intercept τ(x) = t − p x
- Inline geometric derivation (half page, no calculus beyond d/dx = 0): tangency condition gives the tangent family; envelope result
  $$\boxed{\; \tau(p) = t_0 \sqrt{1 - p^2 V^2}, \qquad |p| \le \frac{1}{V} \;}$$
  an **ellipse** with apex (t_0 at p = 0) closing at τ = 0, p = ±1/V (deck slides 25–26)
- Reading it: the reflection's dip range [−1/V, +1/V] is set by the NMO/RMS velocity → deep/fast reflections → narrow tall ellipses; slow shallow reflectors → wide flat ones
- Why this is good for noise separation: linear noise focuses at *constant large |p|* beyond the reflection ellipses' closing points → a **p-mute region** exists where only noise lives (when velocities differ enough — same overlap caveat as FK)
- **Figure 7:** slant-stack construction on three linear events → points (mirrors deck slides 22–24)
- **Figure 8:** hyperbola → ellipse: tangent-line construction, annotated ellipse formula, p-extent ±1/V (mirrors deck slides 25–26)

---

## Section 6: Aliasing and filtering in tau-p (10 min)

### 6.1 Tau-p aliasing and artifacts (5 min)
- The slant stack is a **discrete sum over finite, sampled offsets** → artifacts with two causes:
  1. **p-sampling too coarse:** anti-alias condition $\Delta p \le 1 / (2\, x_\max\, f_\max)$; violated → aliased replicas
  2. **finite offset aperture + discrete traces:** truncation smears energy along p
- Symptoms (deck slide 27): spurious energy at **opposite-sign p** and **very large τ** — easy to recognize once you know the signature
- Cheap fix (deck slide 28): temporal **low-pass filter** before/after the transform kills the aliased high-f component; proper fix: adequate Δp + aperture-aware parameters
- **Figure 9:** tau-p of the running gather with too-large Δp → artifacts; same with adequate Δp / after LPF (mirrors deck slides 27–28)

### 6.2 Filtering in tau-p (5 min)
- Same recipe as FK: design a mute in (τ, p), apply, inverse transform (the inverse is Section 8)
- Typical mute: reject high-|p| region beyond the reflection ellipses' closing points, often combined with a τ-dependent floor; tapers along mute edges as in FK
- QC: before / after / **difference** panels (deck slide 29); difference must show linear noise, not hyperbolas
- Practice note: tau-p mutes are the tool of choice when noise and signal slopes differ but overlap in frequency; FK fan filters are the tool when the whole (f, k) shape matters; they are one transform in two coordinate systems — Section 7
- **Figure 10:** tau-p mute applied to the running gather: before / after / difference in both t-x and tau-p (mirrors deck slide 29)

---

## Section 7: FK and tau-p are the same transform in different coordinates (6 min)

- Take the tau-p panel and Fourier transform **along τ only** → the **f–p domain** (frequency, ray parameter)
- **Fourier slice theorem** (statement + one-line argument, full derivation in the derivation document): the 1D Fourier transform over τ of the slant stack at slope p equals the FK spectrum evaluated **along the radial line k = p·f**:
  $$\boxed{\; U(f, p) = D(f,\, k = p f) \;}$$
- Consequences:
  - FK and f–p spectra are the **same object in different coordinates** (deck slide 30): radial fans ↔ horizontal p-bands; the FK radial-line picture and the tau-p point picture are the two faces of this statement (a point in tau-p spreads into a line k = p·f after FT over τ)
  - A dip-reject fan in FK ≡ a p-band reject in f–p ≡ a p-mute in tau-p (approximately — per-frequency in f–p, all-frequencies in tau-p)
  - There is an amplitude price: the coordinate change is not area-preserving → a |f| factor appears → exactly the rho filter of Section 8
- Filtering-equivalence table (FK fan ↔ f–p band ↔ tau-p mute) — the mental map students should leave with
- **Figure 11:** raw deck slide 30 image (`slides/raw/ft_taup.png`): linear events as constant-slope regions in FK and points in tau-p; FT over τ → f–p; FK ↔ f–p as a pure coordinate change (mirrors deck slide 30)

---

## Section 8: Inverse Radon and the rho filter (7 min)

### 8.1 Why the inverse is not just "sum back" (3 min)
- The natural inverse is the **adjoint** (inverse slant stack): $d(t, x) = \int u(t - p x, p)\, dp$ — sum the p-traces back along the same lines
- For discrete, finite-aperture data the adjoint ≠ inverse: output is a **smeared, low-frequency-biased** version of the input; amplitude and waveform distorted (deck slides 31–33, including the t = 0.2 s slice comparison)
- Same lesson as deconvolution (Term 1): a forward operator's transpose is almost never its inverse

### 8.2 The rho filter (2 min)
- In the frequency domain the correct inverse multiplies each trace of the adjoint result by a **ramp $|\,f\,|$** (the $\rho$-filter — the exact same ramp as in tomography, where it is called the lambda filter)
- Result (deck slide 34): waveforms restored, sections focused — the standard *cheap* inverse: adjoint + rho filter; derivation (via the slice theorem of Section 7) in the derivation document
- What it does *not* fix: p-resolution limits from finite aperture and coarse Δp — the smearing that remains is operator-dependent

### 8.3 Teaser: least-squares and high-resolution Radon (2 min)
- Treat Radon as an inversion: find the sparsest tau-p panel whose forward transform reproduces the data → **least-squares / high-resolution Radon** (conjugate gradients, sparsity constraints; Trad, Ulrych & Sacchi)
- Fixes both artifacts and resolution; also the door to interpolation of missing traces and de-aliasing
- Covered in Term 3 Lecture 06 (regularization and interpolation) — the |f| ramp, sparsity, and "trust the low frequencies" ideas all return
- **Figure 12:** rho filter demo on a four-event gather: t-x round trip (adjoint vs adjoint + rho) and the same datasets viewed in tau-p, with a $\tau$-slice comparison (mirrors deck slides 31–34)

---

## Section 9: Summary and comprehension questions (5 min)

- Noise splits into random (uncorrelated) and coherent (modelable); linear coherent noise is separated by **apparent velocity**
- FK: 2D Fourier; slope p = k/f; linear events → radial lines, reflections → fans; ground roll → low-f/high-k cone
- Spatial aliasing: $k_N = 1/(2\Delta x)$, $f_\text{alias} = V_\text{app}/(2\Delta x)$; aliased noise hides at signal dips — check FK panels of raw shots first
- FK masks: k-cut (anti-alias), dip fan, narrow dip-reject, polygonal; taper everything; QC with difference panels; protect low frequencies
- Tau-p: slant stack; linear events → points; hyperbolas → ellipses $\tau(p) = t_0\sqrt{1 - p^2 V^2}$; artifacts at opposite-sign p / large τ; mute + inverse
- FK and f–p are one spectrum in two coordinates (k = p·f); fan ≡ band ≡ mute
- Inverse Radon = adjoint + rho filter (ramp |f|); true inverse needs least squares (Term 3)

Comprehension questions (in notes + exercises file):
1. Classify as coherent or random: ground roll, swell noise, air blast, water-layer multiple, side scatter from a shallow fault. Which does this lecture address, and by what property?
2. A linear event shows 4 ms of moveout per trace with Δx = 25 m. Compute V_app, p, and k at 30 Hz (cycles/m and cycles/trace). Is it spatially aliased at this frequency?
3. Why can't a dip filter remove aliased ground roll, and why is that an *acquisition* problem as much as a processing one? Give two processing-side remedies.
4. Why do reflections map to ellipses in tau-p while linear noise maps to points? Compute the p-extent of the ellipse for a reflection with t_0 = 2 s and V = 2500 m/s, and sketch where linear noise at 400 m/s would sit relative to it.
5. State the FK ↔ f–p connection. Why does a dip-reject fan in FK correspond to a horizontal band in f–p, and where does the |f| factor come from?
6. What goes wrong if you invert a slant stack by simple adjoint summation? What does the rho filter fix, and what does it leave unfixed?

---

## Figures plan

| # | Concept | Script | Mirrors deck |
|---|---------|--------|--------------|
| 1 | Noise taxonomy: the four families on real records | reuse `slides/raw/noise_types.png` | slide 2 |
| 2 | FK construction: plane waves → p = k/f radial lines; two unaliased + one aliased (wrap-around preview) | `plot_fk_plane_wave.py` | slides 3–7 |
| 3 | Reflections as local segments → FK fan; near/mid/far windows color-matched to their radial lines | `plot_fk_reflection_fan.py` | slides 8–11 |
| 4 | Spatial aliasing: ground roll unaliased at $\Delta x$ = 4 m vs sawtooth wrap at 25 m; dip-flip zoom inset; wrap guides | `plot_spatial_aliasing.py` | slides 12–15 |
| 5 | FK filter masks (k-cut, dip fan, narrow reject, polygonal, low-f protection) with design guides | `plot_fk_filter_types.py` | slides 16–18 |
| 6 | FK filter application: before / after / difference in t-x and FK, fan edge overlaid | `plot_fk_filter_application.py` | slides 19–20 |
| 7 | Slant stack construction; linear events → points in tau-p | `plot_taup_mapping.py` | slides 22–24 |
| 8 | Hyperbola → ellipse: tangent construction, τ(p) = t₀√(1−p²V²) | `plot_taup_ellipse.py` | slides 25–26 |
| 9 | Tau-p aliasing artifacts (coarse Δp) + LPF remedy | `plot_taup_aliasing.py` | slides 27–28 |
| 10 | Tau-p mute: before / after / difference | `plot_taup_mute.py` | slide 29 |
| 11 | FK vs f–p: same spectrum, k = p·f coordinate change; fan ≡ band | reuse `slides/raw/ft_taup.png` | slide 30 |
| 12 | Inverse Radon: adjoint vs adjoint + rho in t-x and tau-p; $\tau$-slice comparison | `plot_inverse_radon_rho.py` | slides 31–34 |

All scripts share the running-example parameters (60 traces, Δx = 25 m, dt = 4 ms; reflections at t₀ = 0.8/1.4/2.0 s with V = 2200/2600/3000 m/s; ground roll V = 300 m/s, 6–25 Hz; air blast V = 600 m/s) so the same gather is recognizable across figures. Candidates for merging if 11 scripts is too many: 6+7 (event mapping) and 8+9 (tau-p artifacts + mute).

Real-data images to reuse from the raw deck: noise examples (slide 2), the t-x/FK pairs (slides 8–11), FK filter results (slides 19–20), tau-p mute result (slide 29), the FK↔f–p connection (slide 30, `ft_taup.png`), inverse Radon slices (slides 31–34).

## Key equations

1. 2D Fourier transform pair (statement only)
2. Plane wave $d(t,x) = s(t - p x)$ → FK support on the line $k = p f$; slope relation $p = k/f$, $V_\text{app} = f/k$ — inline 3-line derivation
3. Spatial Nyquist $k_N = 1/(2\Delta x)$; alias frequency $f_\text{alias} = V_\text{app}/(2\Delta x)$ — inline
4. Slant stack $u(\tau, p) = \sum_j d(\tau + p x_j, x_j)$ and adjoint inverse $d(t,x) = \int u(t - p x, p)\, dp$ — definition
5. Reflection ellipse $\tau(p) = t_0\sqrt{1 - p^2 V^2}$, $|p| \le 1/V$ — inline geometric derivation (tangent/envelope, half page)
6. Fourier slice theorem $U(f, p) = D(f, pf)$ — statement inline, proof in derivation doc
7. Rho filter: per-trace frequency-domain ramp $|f|$ in the inverse — statement inline, proof in derivation doc

## Derivation documents

1. `fk_taup_connection_and_rho_filter_derivation.en.md` — one document covering: (a) slant stack in the frequency domain → Fourier slice theorem $U(f,p) = D(f, pf)$; (b) why the exact inverse acquires the $|f|$ ramp (rho filter); (c) the tau-p anti-alias condition $\Delta p \le 1/(2 x_\max f_\max)$. All three come from the same frequency-domain calculation, so one coherent derivation is better than three fragments.

The ellipse mapping (item 5) stays inline in the lecture notes — it is geometric and accessible (instructor decision pending; see questions below).

## Wiki updates

New concept pages: `fk_transform.md` (2D Fourier, slope relation, event geometry), `spatial_aliasing.md` (or expand existing `aliasing.md`), `fk_filtering.md` (mask types, low-f protection, QC), `linear_radon.md` (slant stack, event mapping, aliasing) or expand `radon_transform.md`, `rho_filter.md`.
Update: `seismic_noise.md` (taxonomy), `radon_transform.md` (cross-links), `frequency_filtering.md` (2D extension cross-link).
New source page: instructor deck `fk_taup.pptx` as `instructor_fk_taup_deck.md`.

## Notation to add to glossary (AGENTS.md)

| Symbol | Meaning | Russian term |
|--------|---------|--------------|
| $k_N$ | Spatial Nyquist wavenumber, $1/(2\Delta x)$ | пространственная частота Найквиста |
| $\Delta x$ | Trace spacing (spatial sampling interval) | шаг между трассами |
| $f_\text{alias}$ | Spatial alias (onset) frequency | частота начала пространственного аляйсинга |
| — | Slant stack (linear Radon sum) | наклонное суммирование (слант-стек) |
| — | Dip / velocity filter | фильтр наклонов (скоростной фильтр) |
| — | Fan filter | веерный фильтр |
| — | Polygonal FK filter | полигонный FK-фильтр |
| — | f–p domain | область частота–лучевой параметр |
| — | Fourier slice theorem | теорема о центральном сечении |
| $\rho$-filter | Ramp filter $\lvert f \rvert$ in inverse Radon | ро-фильтр |
| — | Coherent noise | когерентные помехи |
| — | Air blast / air wave | воздушная волна |
| — | Guided waves | направляемые волны |
| — | Side-scattered noise | помехи бокового рассеяния |
