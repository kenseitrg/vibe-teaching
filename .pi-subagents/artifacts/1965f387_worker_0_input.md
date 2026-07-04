# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
Revise the layer-replacement figure for Term 1 Lecture 03 using the updated velocity model described by the instructor. The script is `scripts/figures/term01_lec03/plot_layer_replacement.py` and the output PNG is `figures/term01_lec03/term01_lec03_layer_replacement.png`.

## Updated velocity model
- The true interval velocity `v_true(x)` is the sum of:
  - a smooth, long-wavelength variation `v_smooth(x)` that we can recover with velocity analysis, and
  - small, short-wavelength random variations `v_random(x)` that velocity analysis cannot recover.
- The reflector is flat at a constant depth `z0`.
- Suggested parameters (tune as needed):
  - x = 0–5000 m, z0 ≈ 500 m, background velocity v0 ≈ 2000 m/s.
  - Smooth variation: amplitude ±100–150 m/s, wavelength ≈ 1500–2000 m (e.g., a sinusoid or broad Gaussian).
  - Random variation: amplitude ±30–50 m/s, correlation length ≈ 100–200 m.
  - The velocity-analysis estimate should be a close approximation of the smooth part, e.g., `v_int = v_smooth` or a slightly smoothed version of it.

## Workflow to illustrate (same 6-panel layout as before)
1. **Model panel:** show the flat reflector and the interval velocity `v_true(x)` as a color fill in the overburden, with a colorbar labeled "Interval velocity (m/s)". The smooth vs random parts of the velocity should be visible.
2. **Velocity profiles:** plot `v_true`, `v_int` (smooth/recoverable), and the derived replacement velocity `v_rep`.
3. **Raw traveltimes:** `t_obs = 2 * z0 / v_true`. Distorted by both smooth and random velocity variations.
4. **Depth conversion:** `z_est = 0.5 * v_int * t_obs`. Because `v_int` captures the smooth variation but not the random part, `z_est` is almost flat but has small residual wiggles.
5. **Smoothed depth:** `z_smooth = smooth(z_est)` removes the random wiggles, giving a nearly flat geological surface.
6. **Corrected traveltimes:** `t_new = 2 * z_smooth / v_rep`, where `v_rep` is derived from `v_int` (e.g., its mean or a heavily smoothed version).
7. **Statics:** `static = t_obs - t_new`.

## Requirements
- Use only NumPy, Matplotlib, and SciPy (no shared utilities).
- Keep the script self-contained and well-commented.
- Use a colorblind-friendly palette.
- Fix the annotation in the raw-traveltimes panel so the "Push-down" label is near the center of the trough and clearly points to it.
- Target visual ranges: raw traveltime range roughly 80–120 ms; corrected traveltime range < 20 ms; `z_est` within ~10 m of `z0` with visible residual wiggles; `z_smooth` within ~5 m of `z0`.
- Read the current `scripts/figures/term01_lec03/plot_layer_replacement.py`, then overwrite it.
- Run `uv run python scripts/figures/term01_lec03/plot_layer_replacement.py` and confirm the PNG is updated.
- Report the exact file paths and a short summary of the chosen parameters and resulting ranges.

---
**Output:**
Write your findings to exactly this path: /home/amilekhin/Work/RGUNG/vibe-teaching/.pi-subagents/artifacts/outputs/1965f387/inline
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

## Acceptance Contract
Acceptance level: checked
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope

Required evidence: changed-files, tests-added, commands-run, residual-risks, no-staged-files

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```