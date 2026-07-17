# Seismic Data Processing Course — Agent Guide

Teaching materials for an undergraduate course on seismic data processing.
The instructor is the subject-matter expert; the agent is a teaching assistant.

**Key constraint:** Students understand basic signal-processing math and seismic acquisition, but struggle with complicated math and programming. Every material must lower the barrier to understanding.

---

## Commands

All Python scripts run via `uv run python <script.py>`. Never use bare `python` or `python3`.

| Action | Command |
|--------|---------|
| Render notes to PDF | `uv run python scripts/render_lecture.py lecture_notes/en/termXX_lecYY_<topic>.en.md` |
| Build PPTX from outline | `uv run python scripts/build_slides.py slides/.../slide_outline.md -o slides/.../deck.pptx` |
| Lint wiki | `uv run python scripts/lint_wiki.py` |
| Lenient lint | `uv run python scripts/lint_wiki.py --warn-stub` |
| Extract text from paper | `uv run python scripts/extract_source_text.py papers/<topic>/<file> -o wiki/sources/_raw_text` |
| OCR (scanned PDFs) | `uv run python scripts/extract_source_text.py papers/... --ocr --no-mmproj-offload` |
| Install with OCR deps | `uv sync --extra ocr` |
| Run a figure script | `uv run python scripts/figures/termXX_lecYY/plot_<concept>.py` |

---

## File naming & directory layout

```
lecture_notes/
  en/term01_lec01_introduction_to_seismic_processing.en.md  # English
  ru/term01_lec01_introduction_to_seismic_processing.ru.md  # Russian translation
  derivations/wiener_deconvolution_derivation.en.md          # Step-by-step math
scripts/figures/termXX_lecYY/plot_<concept>.py              # Self-contained matplotlib
figures/termXX_lecYY/termXX_lecYY_<concept>.png             # Output PNG
slides/termXX/lecYY_<topic>/slide_outline.md                # Slide plan
slides/termXX/lecYY_<topic>/lecYY_<topic>.pptx              # Generated deck
exercises/termXX_lecYY_<topic>.md                            # Concept checks
wiki/                                                        # Persistent knowledge base
```

**Figure scripts are self-contained.** Import only `numpy`, `scipy`, `matplotlib`. No shared utility modules. Use realistic seismic parameters (velocities 1500–3000 m/s, offsets 0–3000 m, depths 100–1000 m). Default size 10×6 in, 150 DPI, colorblind-friendly palettes.

---

## Known gotchas

- **Lecture 5 covers spectral analysis and frequency filtering.** It sits between Lecture 4 (advanced statics and the velocity-analysis link) and Lecture 6 (single-channel deconvolution). The earlier "no lec05" note was a temporary artefact of the deconvolution split into lec06/lec07.
- **No test framework.** No CI. The wiki linter is the only validation tool.
- **Git ignores everything in `papers/`** (*.pdf, *.pptx, *.docx), the OCR model (`/models/`, `*.gguf`), vendored `tools/llama.cpp/`, PI agent state (`.pi/*`, `.pi-subagents/*`), `.opencode/*`, and generated PDFs. Only Markdown sources and scripts are tracked.

---

## Bilingual workflow

1. Draft and iterate in English.
2. Once approved, translate to Russian in `lecture_notes/ru/`.
3. Keep both synchronized. Figure filenames are identical across languages.
4. For bilingual figures with different labels, use `.en.png` and `.ru.png` suffixes.

---

## Wiki conventions

Every wiki page needs YAML frontmatter:
```yaml
---
title: Page Title
status: draft    # stub | draft | reviewed | lecture-ready
sources:         # list of source page IDs
  - source_page_id
tags: [tag1, tag2]
---
```

After creating/updating any wiki page, update `wiki/index.md` and append to `wiki/log.md`.

---

## Notation glossary

Keep this consistent in figures and notes. Add new symbols here once settled.

| Symbol | Meaning | Russian term |
|--------|---------|--------------|
| $x(t)$ | Recorded seismic trace | сейсмическая трасса |
| $w(t)$ | Embedded seismic wavelet | зарегистрированный сейсмический импульс |
| $r(t)$ | Earth reflectivity series | последовательность коэффициентов отражения |
| $n(t)$ | Additive noise | аддитивный шум |
| $*$ | Convolution operator | оператор свёртки |
| $z$ | Unit-delay operator ($z$-transform) | оператор единичной задержки |
| $W(z)$ | $z$-transform of wavelet $w$ | $z$-преобразование импульса |
| $\varepsilon^2$ | Prewhitening constant | аддитивная константа отбеливания |
| $\phi_{xx}[k]$ | Autocorrelation of $x$ at lag $k$ | автокорреляция $x$ |
| $\phi_{dx}[k]$ | Cross-correlation of $d$ and $x$ | взаимная корреляция $d$ и $x$ |
| $\alpha$ | Prediction gap (samples) | интервал предсказания |
| $s_s(t)$ | Source-location wavelet | импульс источника |
| $r_r(t)$ | Receiver-location wavelet | импульс приёмника |
| $h_h(t)$ | Offset-class wavelet | компонента удаления |
| $c_c(t)$ | CDP-location wavelet | компонента ОСТ |
| $G$ | Surface-consistent design matrix | матрица поверхностно-согласованного решения |
| $f[n]$ | Prediction-error filter (PEF) | фильтр ошибки предсказания (ФОП) |
| $h[k]$ | Prediction filter coefficients | коэффициенты фильтра предсказания |
| $F(z)$ | Z-transform of PEF | $z$-преобразование ФОП |
| $H(z)$ | Z-transform of prediction filter | $z$-преобразование фильтра предсказания |
| $\mathbf{R}$ | Toeplitz autocorrelation matrix | теплицева автокорреляционная матрица |
| $\boldsymbol{\phi}_{dx}$ | Cross-correlation vector | вектор взаимной корреляции |
| $v_i$, $V_\text{int}$ | Interval velocity | интервальная скорость |
| $V_\text{avg}$ | Average velocity (vertical ray) | средняя скорость |
| $V_\text{rms}$ | RMS velocity (straight ray) | среднеквадратичная скорость |
| $V_\text{nmo}$ | NMO velocity | скорость NMO |
| $V_\text{stack}$ | Stacking velocity | скорость суммирования |
| $t_0$ | Zero-offset two-way time | двойное вертикальное время |
| $x$ | Source-receiver offset | удаление источник-приёмник |
| $\Delta t_\text{nmo}$ | NMO correction | кинематическая поправка |
| $S(t_0, V)$ | Semblance | сэмбланс |
| $V_\text{r}$ | Replacement velocity | скорость замещения |
| $\delta t$ | Delay time (refraction statics) | время задержки |
| $h$ | Weathering-layer thickness | мощность выветриванного слоя |
| $s_i$ | Source residual static | остаточная статика источника |
| $r_j$ | Receiver residual static | остаточная статика приёмника |
| $h_k$ | Offset-class residual moveout | остаточная кинематика на заданном удалении |
| $c_l$ | CMP structural term | структурная компонента ОСТ |
| $G$ | Design matrix for surface-consistent statics | матрица поверхностно-согласованных статических поправок |
| $\Delta t_\text{floating}$ | Floating-datum correction | поправка к плавающему уровню |
| $\Delta t_\text{smoothed}$ | Long-wavelength static component | длиннопериодная составляющая статики |
| $V_\text{apparent}$ | Apparent velocity from biased velocity analysis | кажущаяся скорость |
| $R$ | Reflection coefficient at normal incidence | коэффициент отражения |
| $Z$ | Acoustic impedance ($\rho v$) | акустический импеданс |
| $Q$ | Quality factor (inverse of absorption) | добротность |
| $G(t)$ | Amplitude gain function | функция усиления |
| $A_\text{rms}$ | RMS amplitude | среднеквадратичная амплитуда |
| $A_{ij}$ | Measured trace amplitude (source $i$, receiver $j$) | измеренная амплитуда трассы |
| $S_i$ | Source amplitude component in SCAC | амплитудная компонента источника |
| $R_j$ | Receiver amplitude component in SCAC | амплитудная компонента приёмника |
| $G_k$ | CMP/geology amplitude component in SCAC | амплитудная компонента ОСТ/геологии |
| $M_l$ | Offset amplitude component in SCAC | амплитудная компонента удаления |
| $v_\text{near}$ | Near-surface velocity for first-break QC | скорость ВЧР (скорость в верхней части разреза) |
| ВЧР | Near surface / upper part of section | верхняя часть разреза |
| NSM | Near-surface model | модель ВЧР |
| FBP | First-break picking | пикирование первых вступлений |
| Refracted waves | Refracted / head waves | рефрагированные волны |
| $V_R$ | Rayleigh-wave phase velocity | фазовая скорость поверхностной волны |
| $c(f)$ | Frequency-dependent phase velocity | фазовая скорость (зависит от частоты) |
| $U(f)$ | Group velocity | групповая скорость |
| $V_s$ | Shear-wave velocity | скорость поперечной волны |
| $V_p$ | Compressional-wave velocity | скорость продольной волны |
| $\mu$, $\lambda$ | Lamé parameters | параметры Ламе |
| $\rho$ | Density | плотность |
| $k$ | Wavenumber | волновое число |
| $\omega$ | Angular frequency | круговая частота |
| $D(f)$ | Dispersion curve | дисперсионная кривая |
| $n$ | Mode number | номер моды |
| $G(f, c)$, $P(f, c)$ | Dispersion spectrum / FK-MUSIC pseudo-spectrum | спектр дисперсии |
| $\hat{h}[n]$ | Adaptive filter coefficients | коэффициенты адаптивного фильтра |
