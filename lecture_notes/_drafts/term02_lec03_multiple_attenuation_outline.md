# Draft outline: Multiple Attenuation (two 90-minute sessions)

> Based on the instructor's plan, the raw deck `slides/raw/multiples.pptx` (97 slides, Russian), and the ingested Verschuur EAGE EET chapters (01, 02, 03, 05, 06, 07) in the wiki.
>
> **Numbering confirmed with the instructor (Option A, precedent = term01 lec06/lec07 deconvolution split):**
> - Session 1 → `term02_lec03_multiple_attenuation_kinematics` (nature, classification, kinematic methods)
> - Session 2 → `term02_lec04_multiple_attenuation_prediction` (prediction: tau-p decon, SRME, adaptive subtraction)
>
> **Instructor decisions (2026-10-25):**
> 1. Two lecture numbers (lec03 + lec04).
> 2. High-resolution Radon: objective + iteration demo in the notes; full IRLS only in the derivation doc.
> 3. Shallow-water combined strategy (FK → pred. decon → SRME): full figure + ~5 min in Session 2.
> 4. Figures: mix — self-generated synthetic scripts + key real-data examples carried over from the raw deck (like term02_lec02 `noise_types.png`).

---

## Session 1 — Multiples and move-out discrimination (~90 min)

**Lecture file:** `lecture_notes/en/term02_lec03_multiple_attenuation_kinematics.en.md`
**Prerequisites:** CMP gathers, NMO and stacking velocity (T1L03), FK and tau-p transforms (T2L02), deconvolution basics (T1L06).

### Learning objectives

After this session students can:
1. Define primaries vs. multiples and explain why multiples fool imaging and interpretation.
2. Classify multiples (surface-related vs. internal; short- vs. long-period) and give field examples of each.
3. Name the two exploitable properties (periodicity, moveout difference) and map each demultiple family onto them.
4. Explain the parabolic Radon demultiple workflow incl. the least-squares and high-resolution formulations.
5. State the limitations of move-out methods (near offsets, velocity inversion, non-hyperbolicity, AVO) and say why they motivate prediction methods.

### 1. Why multiples are a problem (10 min)
- Primary = one upward reflection; multiple = at least one extra *downward* reflection (EET 01 definition).
- Same wavelet, same frequency band → looks exactly like a reflection.
- Field motivation: stacked section ruined by water-bottom multiples; migration images multiples as false reflectors / false structure (raw deck slides 1–8, 15–18; EET 01 false-structure example).
- Where they sit in the flow: demultiple is the defining prestack challenge between statics/decon and stack.

### 2. The two fingerprints: periodicity and excess moveout (15 min)
- **Periodicity** (zero-offset view): water-layer reverberation repeats with period Δt = 2h_w/v_w; multiples = primaries with *times added, amplitudes multiplied* (preview of SRME idea).
  - Long-period (separate events, ~>50 ms) vs. short-period (interfering, "statistical").
- **Kinematics**: velocity increases with depth (compaction) → a shallow multiple travels more of its path in slow layers than a same-time deep primary → more moveout, increasing dip per order; conflicting dips with primaries (raw deck 10–13; EET 01).
- Focusing/defocusing from structure in the generator; amplitude magnification per order.
- These two fingerprints = the two method families of the whole lecture.

### 3. Classification (10 min)
- By downward-reflection interface: **surface-related** (free surface / sea surface, r ≈ −1; "would disappear if the surface were removed") vs. **internal (interbed)** (all downward reflections below surface).
- By generator: water-bottom multiples, peg-legs/reverberations, deeper-generator surface multiples, internal multiples.
- By period: short vs. long — and the practical consequence (statistical decon vs. event-based removal).

### 4. Suppression by kinematics (45 min)
#### 4.1 The general recipe (5 min)
- Transform (after NMO) to a domain where curvature/dip is an axis → separate → mute → transform back.
- Two requirements (EET 02): primaries/multiples must separate there; transform must be reversible.
- Legacy end-members: NMO-at-primary + stack (stacking itself is a move-out filter); FK dip filtering after NMO (recall T2L02) — works when moveout difference maps to resolvable dip difference.

#### 4.2 Parabolic Radon demultiple, adjoint and LS (15 min)
- Why parabolas: after NMO with intermediate velocity, residual moveout ≈ q·x² for both primaries and multiples; frequency-domain implementation per f-slice.
- Adjoint (stack along parabolas) smears and is not invertible → least-squares inverse `m = (LᴴL + λ²I)⁻¹Lᴴd`; reconstruction exact, focusing improved.
- Hampson (1986) workflow: NMO between velocities → forward parabolic Radon → mute large q → inverse transform. Mute design; near-offset hard mute.
- Demo figure: CMP with 3 primaries + multiples, Radon panel, mute, result + removed section.

#### 4.3 High-resolution Radon (10 min)
- LS residual smearing → events spread over curvatures → leakage after mute.
- Sparseness constraint (L1 / Cauchy) on the model: `J = ||d − Lm||² + λ·Σ ln(1 + m²/σ²)`; non-linear, solved iteratively (re-weighting; "IRLS" mention).
- Convergence demo: iterations 0→100 focusing the panel; same data, fewer non-zero parameters; bonus: combats aliasing smearing.

#### 4.4 Limitations of kinematic methods (15 min)
- **Near offsets**: moveout difference → 0 as x → 0; need hard mute near offset → gap → artifacts (raw deck 35).
- **Velocity inversion zones**: internal multiples of a fast shallow layer can stack with primary-like velocities (raw deck 38–39; EET 02 model example).
- **Non-hyperbolicity / apex shift** under complex overburden: multiples are *more* non-hyperbolic than primaries (raw deck 40–42).
- **AVO distortion**: constant-amplitude parabola → spike; AVO → curvature smearing → overlap; Radon demultiple is not amplitude-friendly.
- Summary table: advantages (3D-capable, efficient, far offsets) / disadvantages.

### 5. Wrap-up + comprehension questions (10 min)
- Method map: spatial discrimination done; next session = prediction family (decon, SRME) + the subtraction engine.
- 4–5 concept-check questions.

### Figures (Session 1)

| # | Concept | Script |
|---|---------|--------|
| F1 | Raypath anatomy: primary, water-bottom multiple, peg-leg, internal multiple (schematic) | `plot_multiple_raypaths.py` |
| F2 | False structure: stack/migration with vs. without demultiple (synthetic, 3–4 reflectors + strong water bottom) | `plot_false_structure.py` |
| F3 | Zero-offset periodicity: reverberation train with Δt = 2h/v; short- vs long-period vs. wavelet length | `plot_periodicity.py` |
| F4 | CMP moveout fingerprint: primaries + higher-order multiples, increasing dips; Δt_nmo(x) curves | `plot_multiple_moveout.py` |
| F5 | Classification chart (free-surface vs interbed; short vs long period) — schematic 2-panel | `plot_multiple_taxonomy.py` |
| F6 | Adjoint vs LS parabolic Radon: smearing + reconstruction test | `plot_parabolic_radon_ls.py` |
| F7 | Radon demultiple workflow: NMO → Radon → mute → inverse (panels) | `plot_radon_demultiple.py` |
| F8 | High-res Radon: LS vs HR panels + removed/kept sections; (optional iteration strip) | `plot_highres_radon.py` |
| F9 | Limitations montage: near-offset moveout collapse; velocity-inversion model gather; AVO smear | `plot_kinematic_limits.py` |
| F9b | Real-data carry from raw deck: stacked section with multiples (Nordkapp), North Sea CMP Radon demultiple example | copy from `slides/raw/multiples.pptx` |

Reuse from earlier lectures: `term02_lec02_*` (FK/tau-p), `term01_lec03_*` (NMO) — referenced, not regenerated.

### Key equations (Session 1)

1. Water-layer period: Δt_w = 2 h_w / v_w (vertical); angle-dependence deferred to Session 2.
2. Parabolic Radon adjoint: M(q, f) = Σ_x D(x, f) e^{i2πf q x²}
3. LS inverse: m = (LᴴL + λ²I)⁻¹ Lᴴ d  — matrix per frequency slice (small N×N; "easy" inversion, can show explicitly).
4. High-res objective: J = ||d − Lm||²₂ + λ Σ_{τ,q} ln(1 + m²/σ²)  (Cauchy) — state, don't derive; derivation pointer.

---

## Session 2 — Prediction methods: deconvolution, SRME, adaptive subtraction (~90 min)

**Lecture file:** `lecture_notes/en/term02_lec04_multiple_attenuation_prediction.en.md`
**Prerequisites:** Session 1; predictive deconvolution (T1L06); Wiener filter normal equations (T1L06); tau-p transform (T2L02).

### Learning objectives

After this session students can:
1. Apply the prediction idea to periodic multiples; explain why the period varies with offset and why tau-p fixes it.
2. Derive/state the 1D SRME feedback relation and its series and iterative forms; explain the role of the surface operator and the wavelet problem.
3. Explain the 2D SRME construction (virtual source / downward reflection point, multiple contribution gather, sum over all DRPs).
4. List SRME practical requirements (near offsets, regularity, wavelet, land issues) and their fixes.
5. Formulate adaptive subtraction as a Wiener matching filter; choose filter length / window parameters; decide L1 vs L2.

### 1. Recap + prediction idea (5 min)
- Two fingerprints from Session 1; prediction family exploits periodicity: "a primary (or the data) predicts the multiple".

### 2. Predictive deconvolution and its offset problem (15 min)
- Quick recall T1L06: prediction gap α = water-bottom period (in samples); PEF kills periodic part; ideal operator = shift + scale (raw deck 45–48).
- Worked trace: reverberating water layer, autocorrelation shows the periodicity.
- **Limit**: period depends on ray angle → constant gap wrong at far offsets (each multiple family has its own offset-dependent period).
- **Fix**: linear Radon (tau-p) organizes data by ray parameter p; within one p-trace the period is constant → per-p predictive decon, then inverse transform (raw deck 50–56; EET 03).
- **Remaining limit**: assumes the multiple generator is locally flat (1D); struggling with structural generators → need SRME.

### 3. SRME — the data-driven prediction (40 min)
#### 3.1 1D building block (10 min)
- Zero-offset picture: multiple = two primaries connected at the surface reflection point → times add, amplitudes multiply ×r₀(=−1) → convolution (raw deck 59–61; EET 05).
- m₁ = −x₀*x₀; m₂ = +x₀*x₀*x₀; … the multiple family as a **feedback loop**.
- Implicit: x = x₀ − x₀*x ⇒ x₀ = x + x₀*x.
- Series (explicit): x₀ = x + x*x + x*x*x + … (Neumann; note each term = one order of multiples, "auto-convolution of the input").
- Iterative: p₀⁽ⁱ⁺¹⁾ = p − a*p₀⁽ⁱ⁾*p, start p₀⁽⁰⁾ = p — show iteration-by-iteration convergence figure.

#### 3.2 What happens to the wavelet (10 min)
- Ideal operator is an impulse; real source s(t): each convolution adds one wavelet → spectrum ×S(f) per order.
- Surface operator a(t) = −[s(t)]⁻¹ (designature-like); imperfectly known → predicted multiple has wrong wavelet → **must** adapt before subtracting (bridge to §5).
- Convolution bookkeeping demo: predicted vs true multiple on the synthetic 1D example.

#### 3.3 2D formulation (15 min)
- A multiple for (source s, receiver r) splits at its **downward reflection point (DRP)** k into two "primaries" from a **virtual source** at k: shot-gather trace P(x_k, x_s) ⊛ receiver-gather trace P(x_r, x_k).
- All possible k contribute: M(x_r,x_s;f) = ∫ P(x_r,x_k;f) P(x_k,x_s;f) dx_k — per frequency a matrix product; MCG (multiple contribution gather) shows apex at the true DRP (raw deck 65–73; EET 05–06).
- Step-by-step synthetic demo: 2 reflectors, build MCG, sum → predicted multiple trace; predict → subtract → repeat for all traces.
- Iterative SRME in 2D; workhorse position: fully data-driven, no velocity model.

#### 3.4 SRME limitations (5 min, details in §4 examples)
- Needs **near offsets** (prediction integrates over the surface; missing gap → limited-aperture artifacts; shallow water worst).
- Needs **regular, well-sampled data** (coarse shots → aliasing in the operator; land: statics, ground roll, amplitude → special preprocessing copy for prediction only).
- Wavelet/directivity → adaptive subtraction mandatory.
- Land dilemma: multiples generated at the true surface (no statics) vs. data needing statics.
- Std. marine chain: swell noise → decon/deghost → pred. decon → shot interpolation + near-offset reconstruction → SRME → Radon residual (EET 06).

### 4. Adaptive subtraction — making prediction practical (25 min)
- Statement of problem: model right in kinematics, wrong in dynamics; scaling not enough.
- **Wiener matching filter**: minimize Σ(d − a*m)² in local space-time windows → normal equations R_mm·a = r_dm (raw deck 84; T1L06 equations reused verbatim — deliberate reinforcement).
- **Parameters**: filter length (long enough for wavelet errors, short enough to not fit primaries); window size (stability vs. adaptivity); their interaction; two-stage strategy (global wavelet filter in common-offset, local corrections in shot domain).
- **L2 assumption**: minimum-energy output — fails at interference; leakage + primary damage. **L1**: tolerate outlier residuals at crossing events; non-linear (IRLS); demo figure L2 vs L2 with interfering primary (raw deck 87–97).
- Generalization: same engine for surface-wave subtraction (T3), modeled-noise removal, 4D matching.

### 5. Method map + comprehension questions (5 min)
- Final table: discrimination vs. prediction families; when each wins; toolbox approach ("no silver bullet").

### Figures (Session 2)

| # | Concept | Script |
|---|---------|--------|
| F10 | Period vs offset: raypath geometry + periodicity per offset for one multiple family | `plot_period_vs_offset.py` |
| F11 | Tau-p decon workflow: gather → tau-p (period constant per p) → per-p decon → mute → back; + ACF comparison x-t vs tau-p (raw deck 54) | `plot_taup_decon.py` |
| F12 | 1D SRME series: input trace, −p*p term, +p*p*p term, sum → primaries; feedback-diagram inset | `plot_srme_1d_series.py` |
| F13 | Wavelet bookkeeping: impulse vs source-signature operator; predicted vs true multiple; a(t) = −1/s(t) | `plot_srme_wavelet.py` |
| F14 | SRME iteration convergence: p, p₀⁽¹⁾, p₀⁽²⁾, … vs true primaries (1D multi-reflectors) | `plot_srme_iterations.py` |
| F15 | 2D DRP split: raypath cartoon (s→k→r with virtual source at k) + MCG construction + sum = predicted trace | `plot_srme_2d_drp.py` |
| F16 | SRME requirements demo: full data vs missing near offsets vs coarse shots → prediction artifacts | `plot_srme_requirements.py` |
| F17 | Adaptive subtraction workflow diagram (windows, ACF/CCF, filter, subtract) — schematic + worked synthetic | `plot_adaptive_subtraction.py` |
| F18 | L1 vs L2 subtraction on interfering primary+multiple; filter-length sensitivity (short/long filter, good/bad model — raw deck 93–97) | `plot_l1_vs_l2.py` |
| F19 | Shallow-water combined strategy: shallow-water synthetic walked through FK water-layer demultiple → predictive decon → SRME stages (confirmed: full figure + ~5 min) | `plot_shallow_water_strategy.py` |
| F19b | Real-data carries from raw deck: Gulf of Mexico SRME stack before/after/difference; land-data SRME example | copy from `slides/raw/multiples.pptx` |

Reuse: `term01_lec06_predictive_decon.png` (gap/operator recap), `term02_lec02_taup_mapping.png` (tau-p recap).

### Key equations (Session 2)

1. Angle-dependent period in tau-p: for water layer, Δτ(p) = 2 h_w √(1/v_w² − p²) — period constant per p (small derivation in notes, geometrical).
2. 1D SRME: m₁ = −x₀*x₀; x = x₀ − x₀*x; series x₀ = x + x*x + x*x*x + …; iterative p₀⁽ⁱ⁺¹⁾ = p − a*p₀⁽ⁱ⁾*p.
3. Surface operator: a(t) = −[s(t)]⁻¹.
4. 2D SRME: M(x_r,x_s;f) = A(f) ∫ P(x_r,x_k;f) P(x_k,x_s;f) dx_k.
5. Adaptive subtraction: min_a Σ (d − a*m)² ⇒ R_mm a = r_dm; L1 variant min Σ|d − a*m|.

### Derivation documents

- `lecture_notes/derivations/srme_feedback_derivation.en.md` — from the feedback diagram to implicit/series/iterative forms; Neumann-series justification; surface-operator role; convergence in 1D. (Session 2 backbone; keeps main notes light.)
- `lecture_notes/derivations/highres_radon_derivation.en.md` — LS parabolic Radon per frequency slice; from L2 to Cauchy/L1 sparsity; IRLS/iterative scheme. (Session 1 deep-dive.)
- Optional pointers only: tau-p period derivation stays inside the notes (one paragraph + figure).

---

## Exercises (one file per lecture)

- `exercises/term02_lec03_multiple_attenuation_kinematics.md`: classification quiz (name the multiple), period/moveout calculations (h=75 m, v_w=1480 m/s → Δt; order-3 water-bottom multiple zero-offset time), Radon-panel reading exercise, "why does the near-offset mute hurt" short answer.
- `exercises/term02_lec04_multiple_attenuation_prediction.md`: predict tau-p period from p; SRME series term bookkeeping (how many convolutions/wavelets in order-2 term); matching-filter design window reasoning; L1-vs-L2 scenario choice.

## Wiki pages to touch

- Concepts: `multiples` (created), `srme` (created), `adaptive_subtraction` (generalized), `radon_transform` (add demultiple use), `predictive_deconvolution` (add tau-p section link).
- Sources: five EET pages (created) + existing `verschuur_2006_predictive_deconvolution`.
- Lecture-ready pages after delivery.

## Open questions for the instructor — RESOLVED

All four open questions resolved 2026-10-25 (see header). No blockers remain; proceed to notes + figures.
