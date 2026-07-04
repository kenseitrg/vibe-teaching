# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
Create a self-contained Python script that regenerates Figure 1 (layer replacement) for `lecture_notes/en/term01_lec03_advanced_statics_and_velocity_link.en.md`.

### Goal
Replace the current script `scripts/figures/term01_lec03/plot_layer_replacement.py` and the PNG `figures/term01_lec03/term01_lec03_layer_replacement.png` with a clearer, pedagogically focused figure that shows the layer-replacement workflow with a **laterally varying interval velocity** and a **flat shallow reflector**.

### Physical story to tell (in this order)
1. **Model:** a single flat reflector at constant depth, and an interval velocity that varies laterally with a near-surface anomaly (e.g., a Gaussian low-velocity zone). Show both the reflector and the velocity.
2. **Raw traveltimes:** compute the two-way traveltime `t_obs(x) = 2*z0 / v_true(x)`. They must not be flat — the velocity variations show up as time distortions.
3. **Depth conversion with a smooth velocity:** create a smooth velocity estimate `v_smooth(x)` that mimics what velocity analysis would give (it cannot recover all short-wavelength anomalies). Convert the raw times to depth: `z_est(x) = 0.5 * v_smooth(x) * t_obs(x)`. The depth reflector is almost flat but still has residual wiggles.
4. **Smooth the depth:** apply a gentle smoother to `z_est(x)` to get `z_smooth(x)`. This represents the geological constraint that the reflector should be smooth.
5. **New velocity:** use `v_smooth(x)` as the replacement/new velocity derived from the velocity analysis. (You may also compute a derived replacement velocity `v_new(x) = 2*z_smooth(x)/t_obs(x)` and display it for comparison, but the corrected times should use the smooth replacement velocity.)
6. **New traveltimes:** compute the corrected two-way times by converting the smoothed depth back to time with the replacement velocity: `t_new(x) = 2*z_smooth(x) / v_smooth(x)`. These should be much flatter than the raw `t_obs(x)`.
7. **Statics:** show the static correction as the difference: `static(x) = t_obs(x) - t_new(x)`.

### Implementation details
- Use NumPy and Matplotlib only (no shared utilities).
- Choose realistic numbers: e.g., CMP line 0–5000 m, reflector depth ~500 m, velocity baseline ~2000 m/s with a ±300–400 m/s anomaly.
- Save the output to `figures/term01_lec03/term01_lec03_layer_replacement.png` at 150 dpi.
- Make the figure clear and not crowded. Suggested layout: 6 panels in a 2×3 grid or 3×2 grid, each panel showing one step of the workflow with clear axis labels and short titles. Use a colorblind-friendly palette.
- Include a short caption/comment block in the script summarizing the workflow.
- Read the existing lecture notes section 1.3 and the existing `scripts/figures/term01_lec03/plot_layer_replacement.py` to match the style and file paths.
- After writing the script, run it with `uv run python scripts/figures/term01_lec03/plot_layer_replacement.py` and confirm the PNG is produced.

### Deliverables
1. The updated script `scripts/figures/term01_lec03/plot_layer_replacement.py`.
2. The generated PNG `figures/term01_lec03/term01_lec03_layer_replacement.png`.
3. A concise summary of what the figure shows and any assumptions you made.

---
**Output:**
Write your findings to exactly this path: /home/amilekhin/Work/RGUNG/vibe-teaching/.pi-subagents/artifacts/outputs/bce6dea8/inline
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