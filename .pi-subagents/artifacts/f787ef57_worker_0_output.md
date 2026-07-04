## Task: Remove Gauss–Seidel figure (Figure 4) from Lecture 03

### Deleted files
- `scripts/figures/term01_lec03/plot_gauss_seidel.py`
- `figures/term01_lec03/term01_lec03_gauss_seidel.png`

### Edited files
1. **`lecture_notes/en/term01_lec03_advanced_statics_and_velocity_link.en.md`**
   - Removed the figure embed `![Gauss–Seidel](...)` and its caption at the end of §3.3.
   - Renumbered remaining figures: old Fig 5→Fig 4, old Fig 6→Fig 5, old Fig 7→Fig 6.
   - Gauss–Seidel section text (equations, derivation link) kept intact per instructions.

2. **`slides/term01/lec03_advanced_statics_and_velocity_link/slide_outline.md`**
   - Removed the `**Figure:** ...gauss_seidel.png` line under the Gauss–Seidel slide.
   - Slide text (equations, prose) kept intact.

3. **`wiki/lecture_ready/term01_lec03_advanced_statics_and_velocity_link.md`**
   - Removed the Gauss–Seidel row from the generated-figures table.

### Not modified (per scope)
- Gauss–Seidel derivation documents (`lecture_notes/derivations/gauss_seidel_residual_statics_derivation.*.md`)
- All Gauss–Seidel prose/sections in all files
- Russian lecture notes (not yet created)

### Residual reference (not in scope)
- `lecture_notes/_drafts/term01_lec03_advanced_statics_and_velocity_link_outline.md` still lists the figure in a planning table. This is a draft planning document, not a published material; not modified to stay within scope.

### Verification
- No remaining `gauss_seidel.png` references in the three edited files.
- Figure numbers are sequential (4, 5, 6) in the lecture notes.
- Figure files confirmed deleted (shell `ls` returns error).