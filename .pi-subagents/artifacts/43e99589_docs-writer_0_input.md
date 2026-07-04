# Task for docs-writer

Translate the English Lecture 02 notes into Russian and save them as lecture_notes/ru/term01_lec02_kinematics_and_field_statics.ru.md. Read /home/amilekhin/Work/RGUNG/vibe-teaching/AGENTS.md first for project conventions, then read /home/amilekhin/Work/RGUNG/vibe-teaching/lecture_notes/en/term01_lec02_kinematics_and_field_statics.en.md. Preserve all Markdown formatting, LaTeX math ($...$ and $$...$$), figure references (keep the same PNG paths), and code blocks. Translate all prose, captions, headings, and list items into Russian. Use the shared notation glossary from AGENTS.md for technical terms (e.g., stacking velocity, NMO, static correction, replacement velocity). Keep the existing figure numbering. Do not change the figures or their paths. Write the Russian file to the specified ru path.

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