# Figure brief: Term 1 Lecture 1 — Introduction to seismic data processing

## General requirements

- Each script must be **self-contained** (no shared utilities module).
- Use NumPy, SciPy, Matplotlib. Keep code readable and well-commented.
- Output publication-quality PNGs with clear labels, titles, and captions.
- Figure size: prefer 10×6 inches or 8×8 inches when square; DPI 150.
- Save PNGs to `figures/term01_lec01/` using the filename given below.
- Keep scripts in `scripts/figures/term01_lec01/`.
- Follow the course pedagogical rule: **physical/geometric intuition first**.
- Add a short docstring at the top describing what the figure illustrates.
- Use realistic numbers where possible (e.g., velocities ~1500–3000 m/s, offsets ~0–3000 m).
- Bilingual figures are not required unless labels contain a lot of text; keep labels in English for now.

## Figure 1: Exploration workflow

**Script:** `plot_exploration_workflow.py`
**Output:** `figures/term01_lec01/term01_lec01_exploration_workflow.png`

Illustrate seismic processing in the lifecycle of geological exploration (ГРР):
- Study of geology → Field acquisition → Seismic processing → Interpretation → Geological modeling → Drilling → (back to geology).
- Show that seismic data is one input among others (wells, geology, apriori info).
- Use a block-diagram / flowchart style.

## Figure 2: Idealized vs recorded trace

**Script:** `plot_idealized_vs_recorded_trace.py`
**Output:** `figures/term01_lec01/term01_lec01_idealized_vs_recorded_trace.png`

Top panel: idealized reflectivity series (spikes at reflection times).
Middle panel: band-limited wavelet convolved with reflectivity = ideal seismic response.
Bottom panel: recorded trace = ideal response + noise + multiple + acquisition filter effects.
Use a small 1D layered model with 3–4 reflectors. Add labels and annotations.

## Figure 3: Acquisition and propagation effects

**Script:** `plot_distortions_overview.py`
**Output:** `figures/term01_lec01/term01_lec01_distortions_overview.png`

Schematic diagram showing what gets added to the geological signal:
- Left: clean ray paths from source to reflector to receiver.
- Right: additional phenomena — ghost, source/receiver array response, geometric spreading, absorption, multiples, refractions, surface waves, noise.
Use simple ray cartoons and labeled icons. No need for realistic wave equation modeling.

## Figure 4: Kinematic vs dynamic problems

**Script:** `plot_kinematic_vs_dynamic.py`
**Output:** `figures/term01_lec01/term01_lec01_kinematic_vs_dynamic.png`

Two panels:
- Kinematic: a CMP gather with a hyperbolic reflection; show the goal of placing energy at the correct time and space (NMO, statics, migration).
- Dynamic: the same gather with amplitude variations; show the goal of recovering true relative amplitudes (gain, deconvolution, Q, demultiple).
Use simple synthetic gathers. Label axes clearly.

## Figure 5: Four-phase processing flow

**Script:** `plot_processing_flow.py`
**Output:** `figures/term01_lec01/term01_lec01_processing_flow.png`

Flowchart with four main phases:
1. Preprocessing: data loading, geometry assignment, QC, brute stack.
2. Kinematic processing: statics, velocity analysis, NMO.
3. Dynamic processing: noise attenuation, demultiple, deconvolution, amplitude correction, regularization.
4. Imaging: migration, post-migration conditioning.
Show that phases 2 and 3 can iterate. Use boxes and arrows.

## Figure 6: 2D acquisition geometry and fold

**Script:** `plot_2d_acquisition_geometry.py`
**Output:** `figures/term01_lec01/term01_lec01_2d_acquisition_geometry.png`

Illustrate a 2D marine/land end-on geometry:
- Source positions and receiver spread.
- Midpoints between source–receiver pairs.
- Show how moving the source by one shot interval adds new midpoints and builds fold.
- Label: source interval, receiver interval, minimum offset, maximum offset, CMP spacing.
- Include a small fold profile plot below or beside the geometry cartoon.

## Figure 7: CMP gather and stack

**Script:** `plot_cmp_gather_stack.py`
**Output:** `figures/term01_lec01/term01_lec01_cmp_gather_stack.png`

Three panels:
- Left: shot/receiver geometry for one CMP, showing multiple source–receiver pairs with the same midpoint.
- Middle: synthetic CMP gather before NMO (hyperbolic events).
- Right: same gather after NMO correction and stacking; resulting stacked trace.
Use a simple two-layer model. Label primary and multiple if possible.

## Figure 8: Data sorts

**Script:** `plot_data_sorts.py`
**Output:** `figures/term01_lec01/term01_lec01_data_sorts.png`

Four small panels in a 2×2 grid:
- Shot gather (common source): traces from one shot, ordered by receiver.
- Receiver gather (common receiver): traces recorded at one receiver, ordered by shot.
- CMP gather: traces with same midpoint, ordered by offset.
- Common-offset gather: traces with same offset, ordered by midpoint.
Use simple synthetic data (e.g., hyperbolic events). Each panel should clearly show the sorting principle.

## Figure 9: SEG-Y file structure

**Script:** `plot_segy_structure.py`
**Output:** `figures/term01_lec01/term01_lec01_segy_structure.png`

Diagram of SEG-Y file organization:
- Textual file header (3200 bytes).
- Binary file header (400 bytes).
- Optional extended textual headers.
- Data traces: 240-byte trace header + sample data; repeated for each trace.
- Highlight key trace header fields: shot/receiver line and point, X/Y coordinates, offset, CMP number, number of samples, sample interval.
Use a block/stack visualization with byte sizes and field names.
