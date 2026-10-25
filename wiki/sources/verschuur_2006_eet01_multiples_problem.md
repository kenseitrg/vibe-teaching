---
title: Verschuur (2006) — EAGE EET 01, Multiples: What's the Problem?
type: course slides
year: 2006
author: Eric Verschuur
source_file: papers/multiples/EAGE EET 01 - Whats the Problem.pdf
status: reviewed
tags: [multiples, classification, interpretation, surface-related, internal]
---

# Verschuur (2006) — EAGE EET 01, Multiples: What's the Problem?

## Source

- **Author:** Eric Verschuur (Delft University of Technology)
- **Title:** Seismic Multiple Removal Techniques: Past, Present and Future — Chapter 1: Multiples … what's the problem?
- **Year:** 2006
- **Type:** EAGE Education Course slides
- **File:** `papers/multiples/EAGE EET 01 - Whats the Problem.pdf`

## Main message

Multiples are reflections with at least one *downward* reflection (a primary has exactly one upward reflection). They look like primaries — same wavelet, same frequency band — and therefore contaminate imaging and interpretation. Every removal method exploits one of only two discriminating properties: **spatial behavior** (moveout/dip difference) or **periodicity/predictability**.

## Key points

1. **Definition:** primary = one upward reflection; multiple = at least one downward reflection. Surface-related multiples are those that would disappear if the earth's surface were removed.
2. **Classification by interface:** interface-related multiples are named by their *shallowest* downward reflection: surface-related vs. (water-)bottom-related internal multiples.
3. **Classification by type:** first-layer multiples, first-layer peg-legs/reverberations, other surface multiples, internal multiples.
4. **Classification by period:**
   - *Long-period* (roughly > 50 ms): multiples appear as separate events; "deterministic", predictable and removable.
   - *Short-period*: separation much smaller than the wavelet length; interfere with primaries and act as an effective transmission effect ("statistical").
5. **Recognizable characteristics:** periodic repetition of events; increasing dips for higher-order multiples (conflicting dips with primaries); focusing/defocusing from structure in the multiple-generating layer; amplitude magnification for higher orders; interference with primaries.
6. **Impact:** prestack migration of data with multiples produces false reflectors/false structure (field example: Middle East data with false structure from multiples).
7. **Method taxonomy (foundation for the whole course):**
   - difference in spatial behavior (move-out discrimination; dip filtering after stack/migration),
   - periodicity/predictability (predictive deconvolution — strict 1D periodicity; wave-equation based prediction: model-driven or data-driven, i.e. SRME).

## Implications for teaching

- Perfect opening chapter for the demultiple lecture: definition, classification (surface vs internal; short vs long period), and the two-family method taxonomy that organizes everything that follows.
- The "false structure" examples motivate *why* demultiple matters for interpretation, not just for cosmetic stack quality.

## Concepts informed

- [Multiples](../concepts/multiples.md)
- [SRME](../concepts/srme.md)
- [Seismic noise](../concepts/seismic_noise.md)

## Quotes / memorable lines

> "Surface-related multiples are those multiples that will disappear if the earth's surface is removed."

> "A multiple removal method either exploits a difference in spatial behaviour, or exploits periodicity and predictability — you need a primary to predict a multiple."
