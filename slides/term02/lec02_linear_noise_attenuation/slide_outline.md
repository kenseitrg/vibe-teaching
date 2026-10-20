# Slide outline — Term 2, Lecture 2: Linear Noise Attenuation — FK and Tau-P

---


## Slide 1 — Title
- Linear Noise Attenuation: FK and Tau-P
- Term 2, Lecture 2
- Figure: none

---

## Slide 2 — Learning objectives
- Classify noise into random and coherent; name the linear-noise family this lecture targets.
- Read the FK spectrum: a dip is a radial line $p = k/f$; reflections form fans, ground roll a low-frequency wedge.
- Predict spatial aliasing: $k_N = 1/(2\Delta x)$, $f_\text{alias} = V_\text{app}/(2\Delta x)$ — and explain why it defeats dip filters.
- Design the four standard FK masks (k-cut, dip fan, narrow dip-reject, polygonal) with tapers and low-frequency protection.
- Explain the slant stack: linear events focus to points, hyperbolas to ellipses $\tau(p) = t_0\,(1 - p²V²)^{1/2}$.
- Connect FK and tau-p through the Fourier slice theorem; know the rho filter and why the adjoint alone fails.
- QC every attenuation step with before / after / difference panels.

---

## Slide 3 — Why this lecture matters
- Every raw land shot gather: faint hyperbolas under a low-frequency fog of ground roll, plus crisp straight-line air blasts.
- Signal and noise share the same times and overlapping frequency bands — 1-D filtering (Term 1, Lecture 5) cannot separate them.
- The property that does separate them: apparent velocity — the dip of an event across the gather.
- Two domains make dip visible: FK (dip = radial direction) and tau-p (dip = an axis).
- One practical obstacle rules them all: spatial aliasing.

---

## Slide 4 — Random vs coherent noise
- Random: unpredictable trace-to-trace (wind, swell, instrument noise); removed by stacking and prediction.
- Coherent: follows a model — a traveltime law, a dip, a periodicity; removed by separation or model-and-subtract.
- Noise is relative to the objective: a surface wave is noise for reflection processing but the signal for near-surface $V_s$ studies (Term 3, Lecture 3).
- This lecture: "signal" = reflection energy; "noise" = everything else on the gather.

---

## Slide 5 — The coherent-noise families
- Source-generated linear noise: ground roll (slow, low-frequency, high-amplitude Rayleigh train), air blast, guided waves — straight lines fanning from the source. Today's targets.
- Side-scattered energy: linear events from near-surface heterogeneities (karst, faults) at steep angles.
- Multiples: predictable by periodicity — Term 2, Lecture 3.
- First breaks: direct and refracted arrivals — usually muted, not filtered.
- Figure: `term02_lec02_noise_types.png`

---

## Slide 6 — Why transforms, and where in the flow
- Reflections (hyperbolas) and linear noise overlap completely in time and frequency; only dip separates them.
- Dip is spatial → we need transforms that look across traces: FK and the linear Radon (tau-p).
- Position in the flow: early — after amplitude recovery and statics, before detailed velocity analysis, demultiple, stack.
- Cleaner gathers → better decon windows, more reliable velocity picks, better stack.

---

## Slide 7 — The FK spectrum
- Apply the Fourier transform in time (per trace), then in space (across traces): the 2-D Fourier transform.
- New axis: wavenumber $k$ — spatial frequency, cycles per meter (or cycles/trace; limits $\pm 0.5$).
- Mental image: the FK transform decomposes the gather into plane waves.
- Each point $(f, k)$ = one plane-wave component: one temporal frequency at one spatial oscillation rate.

---

## Slide 8 — One plane wave: from t-x to FK
- Linear event (plane wave): $d(t, x) = s(t - px)$; slope $p = dt/dx$, apparent velocity $V_\text{app} = 1/p$.
- Transform over time: at one frequency $f$, complex amplitudes form a sinusoid in $x$ (phase rotates by $f \cdot px$ per trace).
- Transform over space: a sinusoid has one wavenumber — $k = pf$.
- A linear event occupies a radial line through the origin in FK.
- Figure: `term02_lec02_fk_plane_wave.png`

---

## Slide 9 — Dip in FK: three rules
- $p = k/f$ and $V_\text{app} = f/k$: slope is a ratio — 20 Hz at $k = 0.01$ cyc/m and 40 Hz at $0.02$ cyc/m are the same dip.
- Horizontal and vertical trade places: flat events ($p = 0$) sit on the $f$-axis; steep events hug the $k$-axis.
- All events of one apparent velocity share one radial line — arrival times and wavelets only change phase along it.

---

## Slide 10 — Reflections in FK are fans
- A hyperbola is not a line — but every window of it nearly is: tangent slope $p = x/V^2 t(x)$.
- A reflection = a continuum of tangent segments → each maps to its own radial line.
- The family of tangents sweeps a fan between $k = p_\text{near} f$ and the asymptote $k = f/V$.
- Deeper reflectors (larger $t_0$, $V$) → flatter fans.
- Figure: `term02_lec02_fk_reflection_fan.png`

---

## Slide 11 — Ground roll in FK, and the overlap problem
- Ground roll at 300 m/s: one steep radial line $k = f/300$; low-frequency → a low-f, high-$|k|$ wedge.
- Air blast at ~600 m/s: a slightly gentler line.
- Amplitude at $(f, k)$ = energy at frequency $f$ travelling at dip $k/f$.
- The central difficulty in one picture: the steep side of the reflection fan and the noise wedge overlap — at low f and steep dips, signal and noise share FK cells.

---

## Slide 12 — Spatial aliasing: the spatial Nyquist
- In time, anti-alias filters act before digitization — recorded data are (almost) never aliased in time.
- No "analog filter in space": the geophones are where they are, at spacing $\Delta x$.
- Spatial Nyquist wavenumber: $k_N = 1/(2\Delta x) = 0.5$ cycles/trace.
- Any component with $|k| > k_N$ folds back into $[-k_N, +k_N]$.

---

## Slide 13 — The alias frequency
- An event with apparent velocity $V_\text{app}$ has $k = f/V_\text{app}$; aliasing starts when $k$ crosses $k_N$:
- $f_\text{alias} = V_\text{app} / (2\Delta x)$ — the folding frequency.
- Same statement per trace: the delay $\Delta x/V_\text{app}$ is "smooth" only while under half a period.
- Slow events alias first: the steeper the dip, the lower the folding frequency.

---

## Slide 14 — Worked numbers: land data in trouble
- Ground roll 300 m/s at $\Delta x = 25$ m: $f_\text{alias} = 6$ Hz — the whole 25 Hz band is aliased almost from its first cycle.
- Wrapped energy leaves the steep line and re-enters at moderate, reflection-like dips.
- Same roll at $\Delta x = 12.5$ m: $f_\text{alias} = 12$ Hz — halving $\Delta x$ doubles $k_N$.
- A reflection at 2500 m/s: $f_\text{alias} = 50$ Hz — safe. The survey was designed for signal; nobody designed it for noise.
- Figure: `term02_lec02_spatial_aliasing.png`

---

## Slide 15 — Why aliasing breaks noise attenuation
- Wrapped ground roll sits at $(f, k)$ points reflections also occupy — indistinguishable from signal dips.
- Dilemma: remove the noise and amputate reflection dips, or spare reflections and keep the noise.
- Aliased coherent noise = the classic acquisition failure that processing inherits.
- Remedies, in order: (1) acquire finer ($\Delta x < V_\text{noise}/2f_\text{max}$); (2) interpolate (de-alias) before filtering; (3) k-cut the wrapped energy; (4) aliasing-tolerant methods (Term 3).

---

## Slide 16 — FK filtering: the recipe
- FK filtering = Term-1 frequency filtering + one dimension:
- Forward 2-D FFT → multiply by a designed amplitude mask → inverse FFT.
- Filter dips → radial sectors; filter frequencies → horizontal bands; combinations → arbitrary polygons.
- Four standard masks cover nearly all practical needs.

---

## Slide 17 — The four standard masks
- k-filter (anti-alias cut): zero $|k| > k_\text{cut}$ — before decimation; cheap cure for wrapped noise outside the fan.
- Dip (velocity) filter: pass $|p| < p_\text{max}$ — the workhorse, and the filter most betrayed by aliasing.
- Narrow dip-reject: surgical cone around one slope (e.g. the air blast) — only where signal never visits.
- Polygonal filter: combine dips and frequencies — what production software actually exposes.
- Figure: `term02_lec02_fk_filter_types.png`

---

## Slide 18 — Tapers and low-frequency protection
- Abrupt 0/1 mask boundaries ring in t-x (2-D Gibbs effect) — taper every edge.
- A naive fan through the origin removes all low frequencies inside the noise cone — the band broadband processing fights to preserve.
- Soften the wedge: start above a frequency floor, widen gradually, keep a protected corridor along $f$.
- Rule: reject the noise's (dip, frequency) combination, not its dip at every frequency.

---

## Slide 19 — QC discipline
- Always inspect before / after / difference — in t-x and in the transform domain.
- The difference is your noise model: linear events, right dips and frequencies; reflection arcs mean the mask ate signal.
- Where amplitudes matter (AVO, 4D): prefer model-and-subtract — keep only the noise, transform back, subtract; adaptive subtraction polishes it further.
- Figure: `term02_lec02_fk_filter_application.png`

---

## Slide 20 — The linear Radon transform: slant stack
- $u(\tau, p) = \sum_j d(\tau + p x_j, x_j)$: pick a trial slope, apply LMO($1/p$), sum all traces.
- Energy at that slope lines up flat → sums constructively; everything else smears.
- Result: a gather reorganized from "one trace per offset" to "one trace per dip" — indexed by intercept time $\tau$.
- $p$ = ray parameter (slowness), conserved by Snell's law → tau-p traces are genuine plane-wave responses.
- Pedigree: Radon 1917; Rieber 1936; the Soviet РНП method — digital steering for all angles at once.

---

## Slide 21 — How events map: linear → point
- Trial $p = p_0$: the event flattens and all energy piles at $\tau = \tau_0$ — a point.
- Several events with the same slope → the same p-trace at different $\tau$: "all energy that crossed the array at this dip."
- Compare FK: the same event lives on an entire radial line — tau-p focuses, i.e. a sparser representation.
- First appearance of the key idea: choose the transform in which your data are sparse.
- Figure: `term02_lec02_taup_mapping.png`

---

## Slide 22 — Reflections become ellipses
- A hyperbola is a family of tangents; the tangent at slope $p$ focuses at $\tau(p) = t - px$.
- The tau-p image = the envelope of all tangents:
- $\tau(p) = t_0\,(1 - p²V²)^{1/2}$, $|p| \leq 1/V$ — an ellipse closing at $p = \pm 1/V$.
- Deepest reflection offer: its asymptote $1/V$ — reflections never reach large $|p|$.
- Figure: `term02_lec02_taup_ellipse.png`

---

## Slide 23 — Separation on one panel
- Linear noise: points at fixed large $|p|$ (ground roll ≈ 3.3 ms/m, air blast ≈ 1.7 ms/m), low $\tau$.
- Reflections: inside their ellipses, closing by $|p| = 1/V_\text{min}$.
- Between them (velocities permitting): a no-man's-land of random noise only — the mute zone.
- When the noise cone overlaps the ellipses' steep flanks, surgery is partial — same overlap caveat as FK.

---

## Slide 24 — Aliasing in tau-p: p-aliasing
- The slant stack sums in t-x — no FFT across traces — but is not immune.
- At fixed $f$, each offset contributes phase $e^{2\pi i f p x}$; coarse $\Delta p$ aliases the twist.
- Anti-alias condition: $\Delta p \leq 1/(2 x_\text{max} f_\text{max})$ — e.g. 1475 m & 100 Hz → $\Delta p \leq 3.4$ μs/m → ~2400 p-values.
- The tau-p panel is (and should be) oversampled; low-pass filtering is the cheap fix, fine $p$ the proper one.

---

## Slide 25 — Finite-aperture artifacts
- Truncation in $x$ = convolution in $p$: focused points grow side lobes smeared along $p$.
- Symptoms (recognize once, see forever): energy at opposite-sign $p$; energy at very large $\tau$.
- Subtlety: t-x-aliased frequencies of a linear event stay on the same p-trace — tau-p relocates aliased energy, does not un-mix it.
- Figure: `term02_lec02_taup_aliasing.png`

---

## Slide 26 — Filtering in tau-p
- p-mute: zero beyond the ellipses' closing points ($|p| > 1/V_\text{min}$, generously tapered).
- τ-p windows: add a time floor or mute only one dip band.
- Taper every edge: hard corners ring when transformed back — production uses ~200 ms tapers, no sharp corners.
- Same strategic choice as FK: zero-out the noise, or model-and-subtract for amplitude fidelity.
- When to prefer tau-p: pure dip decisions, frequency-independent — and generalizations (parabolic, hyperbolic) FK cannot offer.

---

## Slide 27 — Tau-p mute on the running example
- Air blast (unaliased here): focuses entirely at $p = 1/V_\text{ab}$ → mute removes it completely.
- Ground roll (aliased): wrapped 10–16 Hz components stack inside the keep zone ($|p| < 0.6$ ms/m) → residuals.
- Lesson: dip filtering needs unaliased (or low-pass-filtered) input.
- QC as always: before / after / difference.
- Figure: `term02_lec02_taup_mute.png`

---

## Slide 28 — FK and tau-p: one transform, two coordinates
- Fourier-transform the tau-p panel over $\tau$ only → the f-p spectrum $U(f, p)$.
- From the slant-stack definition: $U(f, p) = D(f, pf)$ — the Fourier slice theorem (the math of CT tomography).
- The 1-D transform over $\tau$ at slope $p$ = the FK spectrum along the radial line $k = pf$.
- Radial fan in FK ↔ horizontal p-band in f-p; a point in tau-p is the line $k = pf$ seen from the other axis.
- Figure: `term02_lec02_ft_taup_connection.png`

---

## Slide 29 — The dictionary between domains
- Reject $|p| > p_\text{max}$: fan reject (FK) ↔ p-band reject (f-p) ↔ p-mute (tau-p).
- Keep a frequency band: FK/f-p band ↔ not expressible as a tau-p mute (mute hits all frequencies at once).
- Remove one noise velocity: narrow radial cone ↔ narrow p-stripe ↔ spike mute on one p-trace.
- There is an amplitude price: the change $(f, k) \to (f, p)$ brings $dk = f\,dp$ — spectra differ by a factor $f$.

---

## Slide 30 — Inverse Radon: why "sum back" fails
- Natural candidate: the adjoint — spread each p-trace along its line and sum: $d_\text{adj}(t,x) = \sum_j u(t - p_j x, p_j) \Delta p$.
- Round trip (forward + adjoint) = a recognizable but smeared, low-frequency-flavored copy: amplitudes decay, wavelets stretch, side lobes trail.
- Per frequency the round trip multiplies every spectrum by $1/|f|$.
- Moral from deconvolution: the transpose of an operator is almost never its inverse.

---

## Slide 31 — The rho filter
- Exact inverse (filtered back projection): adjoint slant stack followed by convolution with the rho filter — amplitude response $\alpha(f) = |f|$, a zero-phase ramp.
- In practice: multiply each p-trace's amplitude spectrum by the ramp $|f|$ (tapered toward Nyquist) before the inverse transform.
- Result: wavelets regain bandwidth and symmetry; tau-p foci recover their height.
- What rho does not fix: p-smearing from finite aperture and coarse $\Delta p$ → p-deconvolution or least squares.
- Figure: `term02_lec02_inverse_radon_rho.png`

---

## Slide 32 — Teaser: least-squares and high-resolution Radon
- Set up least squares: solve for the tau-p panel that best reproduces the data, $\phi = (RR^*)^{-1} R d$.
- Inversion undoes the operator's smearing → far fewer artifacts than the adjoint.
- With a sparsity constraint: the high-resolution Radon transform — reflections and noise become tight, separable blobs.
- Door to Term 3: Radon interpolation, de-aliased Radon, sparsity-based attenuation.
- Poorly sampled data: plain transforms are dangerous (Marfurt et al. 1996).

---

## Slide 33 — Summary
- Noise: random (stack/predict) vs coherent (separate by kinematics or dynamics); today's target — linear coherent noise, separated by apparent velocity.
- FK: plane wave → radial line $k = pf$; reflections → fans; ground roll → steep low-f wedge; overlap is the intrinsic difficulty.
- Spatial aliasing: $f_\text{alias} = V_\text{app}/(2\Delta x)$; slow noise aliases first (300 m/s @ 25 m → 6 Hz); wrapped noise defeats dip filters.
- FK filters: k-cut, dip fan, narrow reject, polygonal — taper everything, protect low frequencies, QC with differences.
- Tau-p: slant stack; linear → point, hyperbola → ellipse; noise focuses beyond the ellipses → p-mutes; artifacts from coarse $\Delta p$ and finite aperture.
- FK ↔ f-p: one spectrum, two coordinates (slice theorem); amplitude price = the $|f|$ ramp.
- Inverse Radon = adjoint + rho filter; remaining p-smearing → LS / high-resolution Radon (Term 3).

---

## Slide 34 — Comprehension questions
- Classify as coherent or random: ground roll, swell noise, air blast, water-layer multiple, side scatter from a shallow fault. Which does this lecture address, and by which property?
- A linear event shows 4 ms moveout per trace at $\Delta x = 25$ m. Compute $V_\text{app}$, $p$, $k$ at 30 Hz (cyc/m and cyc/trace). Aliased? From which frequency?
- Why can a dip filter not remove aliased ground roll — and why is that an acquisition failure? Two processing-side remedies and their costs.
- Geometrically: why does a hyperbola map to an ellipse in tau-p while a line maps to a point? Compute the p-extent for $t_0 = 2$ s, $V = 2500$ m/s.
- State the Fourier slice theorem; use it to explain fan ↔ p-band ↔ p-mute. Where does $|f|$ come from — and which filter of this lecture is it?
