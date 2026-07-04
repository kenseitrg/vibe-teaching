# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
Remove the Gauss–Seidel figure (Figure 4) from Lecture 03 materials and clean up all references. Do NOT delete the Gauss–Seidel derivation documents or remove the Gauss–Seidel text/section; only remove the figure file, the script, and references to that figure.

## Files to delete
1. `scripts/figures/term01_lec03/plot_gauss_seidel.py`
2. `figures/term01_lec03/term01_lec03_gauss_seidel.png`

## Markdown references to update

### `lecture_notes/en/term01_lec03_advanced_statics_and_velocity_link.en.md`
- Remove the figure embed and caption around lines 210–212:
  ```markdown
  ![Gauss–Seidel](figures/term01_lec03/term01_lec03_gauss_seidel.png){width=90%}

  **Figure 4.** *Gauss–Seidel iteration for the 4-component model. The algorithm cycles through source, receiver, offset, and CMP classes, updating one class at a time while holding the others fixed.*
  ```
  Keep the surrounding Gauss–Seidel section text (section 3.3).
- Renumber the remaining figures:
  - Old **Figure 5** → **Figure 4** (Long-wavelength statics and velocity bias)
  - Old **Figure 6** → **Figure 5** (Long-wavelength statics shift the whole CMP gather...)
  - Old **Figure 7** → **Figure 6** (Floating datum concept)

### `slides/term01/lec03_advanced_statics_and_velocity_link/slide_outline.md`
- Remove the figure reference line under the `# Gauss–Seidel solution` slide:
  ```markdown
  **Figure:** `figures/term01_lec03/term01_lec03_gauss_seidel.png`
  ```
  Keep the rest of the Gauss–Seidel slide text.

### `wiki/lecture_ready/term01_lec03_advanced_statics_and_velocity_link.md`
- Remove the Gauss–Seidel row from the generated figures table:
  ```markdown
  | Gauss–Seidel iteration | `figures/term01_lec03/term01_lec03_gauss_seidel.png` |
  ```

## Steps
1. Read the three files above to confirm the exact text to remove.
2. Delete the two figure files.
3. Make the edits and renumbering.
4. Verify the files still read correctly (no broken figure references, no orphaned numbering).
5. Report the exact changes made and any remaining references to Gauss–Seidel figures.

---
**Output:**
Write your findings to exactly this path: /home/amilekhin/Work/RGUNG/vibe-teaching/.pi-subagents/artifacts/outputs/f787ef57/inline
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