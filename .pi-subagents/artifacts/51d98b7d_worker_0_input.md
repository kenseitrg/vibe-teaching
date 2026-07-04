# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
Make one more focused refinement to the layer-replacement figure script so that the random velocity component behaves exactly as the instructor described: short-wavelength, zero-mean, and destroyed by smoothing the depth horizon.

## Current issue
In the current draft, the random velocity component still contains some long-wavelength energy, so the depth estimate `z_est` has a broad trend (not just small wiggles). The instructor wants:
- the smooth velocity variation to be recovered by velocity analysis,
- the remaining random variations to be small and short-wavelength,
- these random variations to be removed by smoothing the depth horizon, so `z_est` is *almost flat* and `z_smooth` is very close to the true flat reflector.

## Refinements to make
1. **Zero-mean, short-wavelength random component.** Generate `v_random` so that:
   - it has zero mean (subtract the mean after smoothing),
   - its correlation length is short (e.g., ~75–125 m),
   - it has no long-wavelength trend (high-pass it by subtracting a heavily smoothed version, e.g., `v_random -= gaussian_filter1d(v_random, sigma=30)` or similar).
   - its amplitude is small (e.g., std ~20–25 m/s, so the orange `v_true` line shows only fine wiggles around the purple `v_int` line).
2. **Keep `v_int = v_smooth`**, so velocity analysis exactly recovers the smooth part.
3. **Tune depth smoothing.** After depth conversion with `v_int`, `z_est` should be almost flat: RMS deviation from `z0` should be small (a few metres), with visible but small residual wiggles. Then smooth `z_est` to get `z_smooth`, which should be very close to flat (RMS deviation < ~2 m).
4. **Corrected times.** `t_new = 2 * z_smooth / v_rep` should still be much flatter than `t_obs` (target corrected range < 15 ms; raw range ~80–120 ms).
5. **Fix the annotation in panel (c).** Place the annotation text near the trough with a clear arrow; avoid the bottom-right corner.
6. **Keep the 6-panel layout, the velocity color fill in the model panel, the colorblind-friendly palette, and the self-contained script structure.**

## Steps
1. Read `scripts/figures/term01_lec03/plot_layer_replacement.py`.
2. Edit the model-generation and smoothing parts to meet the targets above. Tweak `dv_gauss`, `sigma_gauss`, random amplitude, and smoothing sigmas as needed.
3. Run `uv run python scripts/figures/term01_lec03/plot_layer_replacement.py` and confirm the PNG is updated.
4. Report the final diagnostics printed by the script, especially:
   - `v_random std`,
   - `t_obs range`, `t_new range`,
   - `z_est RMS deviation from z0`, `z_smooth RMS deviation from z0`,
   - `static range`.

If the numbers are not close to the targets, iterate once more before reporting.

---
**Output:**
Write your findings to exactly this path: /home/amilekhin/Work/RGUNG/vibe-teaching/.pi-subagents/artifacts/outputs/51d98b7d/inline
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