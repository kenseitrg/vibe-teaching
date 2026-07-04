# Task for docs-writer

Translate the English derivation 'Delay-time derivation for refraction statics' into Russian and save it as lecture_notes/derivations/refraction_delay_time_linear_system.ru.md. Read /home/amilekhin/Work/RGUNG/vibe-teaching/AGENTS.md first, then read /home/amilekhin/Work/RGUNG/vibe-teaching/lecture_notes/derivations/refraction_delay_time_linear_system.en.md. Preserve all Markdown formatting, LaTeX math, and section structure. Translate all prose and headings into Russian, maintaining the technical notation and terminology from the AGENTS.md glossary.

## Acceptance Contract
Acceptance level: attested
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return a concise result and residual risks when applicable

Required evidence: manual-notes, residual-risks

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