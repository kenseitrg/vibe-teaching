---
title: "Zhang & Dai (2015) — Land Data FWI: Methods and Strategies (SPE-177571-MS)"
status: draft
type: paper
source_file: wiki/sources/_raw_text/zhang2015.txt
language: en
concepts:
  - full_waveform_inversion
  - fwi_cycle_skipping
tags: [fwi, land, cycle-skipping, reflection-fwi, wemva, bp2004, inner-mongolia]
---

# Zhang & Dai (2015) — Land Data FWI: Methods and Strategies

SPE-177571-MS, ABU DHABI INTERNATIONAL PETROLEUM EXHIBITION AND CONFERENCE, 2015. BGP/CNPC.

## Overview

A methods-and-strategies paper on making reflection FWI work on land data where offsets are short and low frequencies are missing (diving waves unusable). Reviews why conventional FWI fails there (cycle skipping of reflected events), and builds a practical chain: wave-equation migration velocity analysis (WEMVA)-derived starting models, **dynamic-formation-phase-deviation (DFPD) FWI** — a phase-based objective tolerant to cycle skipping — and reflection-slope FWI for high-resolution updates.

## Key takeaways

- **Cycle skipping on land:** with a 1D-gradient starting model and reflection data only, modelled events can arrive a full period late/early — conventional L2 (and even phase-only) FWI then updates in the wrong direction (their Fig. 1 shows the oscillatory wrong-direction update vs. the coherent DFPD update).
- **Strategies:** (1) build starting models with WEMVA (flattening image gathers — a model-extension idea); (2) use cycle-skip-tolerant objectives (DFPD over 3–8 Hz); (3) resolution demonstrated on the BP 2004 benchmark: FWI recovers small anomalies that ray tomography cannot (their Fig. 7).
- **Field example (Inner Mongolia):** FWI-updated model improves the migration image relative to the WEMVA starting model.

## Relation to lecture notes

Term 3 Lecture 07 §2 (cycle-skipping work-arounds; Fig. 1 reused) and §3 (resolution on BP 2004, Fig. 7 reused).

## Related sources

- [Wang et al. (2020)](wang2020_land_fwi_challenges.md) — CGG land FWI strategies.
- [Métivier & Brossier review](metivier2026_fwi_nonconvexity_review.md) — taxonomy in which WEMVA-like methods appear as model extensions.
