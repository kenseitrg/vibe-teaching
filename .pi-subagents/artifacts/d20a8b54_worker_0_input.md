# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
Revise the layer-replacement figure script based on the review below. The script is `scripts/figures/term01_lec03/plot_layer_replacement.py` and the output PNG is `figures/term01_lec03/term01_lec03_layer_replacement.png`.

## Issues to fix
1. **Show the velocity variation in the model panel.** Panel (a) should display the interval velocity in the overburden (e.g., with `pcolormesh`/`imshow` using a color map) so the link between the flat reflector and the velocity anomaly is visible. Include a colorbar labeled "Interval velocity (m/s)" and keep the reflector as a clear black line.
2. **Tune the smooth velocity estimate so the depth estimate is "almost flat" but still needs smoothing.** The smooth velocity `v_int` should be visibly smoother than the true velocity `v_true` and miss enough short-wavelength anomaly that `z_est` has small residual wiggles (within ~5–10 m of the true depth), but after smoothing the depth `z_est` → `z_smooth` the surface should be very close to flat. Target: raw traveltime range ~80–100 ms, corrected traveltime range < 20 ms, `z_est` range < ~15 m, `z_smooth` range < ~5 m.
3. **Derive the replacement velocity from the smooth velocity estimate.** Instead of hardcoding `v_rep = v0`, define it from `v_int` (e.g., `v_rep = np.mean(v_int)` or a heavily smoothed version of `v_int`). Document this choice in the script comments.
4. **Fix the annotation in panel (c).** Move the "Push-down from low-velocity zone" annotation so it sits near the center of the trough with a clear arrow, avoiding overlap with the curve or the panel edge.
5. **Keep the 6-panel workflow layout, colorblind-friendly palette, and clear labels.** Do not introduce shared utility modules.

## Mathematical workflow to preserve
- `t_obs(x) = 2 * z0 / v_true(x)`
- `z_est(x) = 0.5 * v_int(x) * t_obs(x)`
- `z_smooth(x) = smooth(z_est)`
- `t_new(x) = 2 * z_smooth(x) / v_rep`
- `static(x) = t_obs(x) - t_new(x)`

## Steps
1. Read the current `scripts/figures/term01_lec03/plot_layer_replacement.py`.
2. Edit the script to implement the revisions above.
3. Run `uv run python scripts/figures/term01_lec03/plot_layer_replacement.py` and confirm the PNG is created/overwritten.
4. Report the exact file paths and a short summary of the chosen parameters (anomaly amplitude/width, smoothing sigmas, derived replacement velocity) and the resulting ranges for raw times, corrected times, and depths.

If you need to adjust the model parameters to meet the targets, do so and explain the choices.

---
**Output:**
Write your findings to exactly this path: /home/amilekhin/Work/RGUNG/vibe-teaching/.pi-subagents/artifacts/outputs/d20a8b54/inline
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