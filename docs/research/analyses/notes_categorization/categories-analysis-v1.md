# Notes — categorized clauses (Goal A.5)

Built from the locked v1 [category_dictionary.md](category_dictionary.md) by [categorize.py](categorize.py).

## Group sizes (days with notes)

- crash days: **59**
- lead-up days: **45**
- non-crash days: **582**
- total with notes: **686**

## Per-day category presence rates (proportion of days mentioning the category)

| category | crash | leadup | non-crash | all | ratio crash/all | ratio leadup/all |
|----------|-----:|------:|---------:|----:|---------------:|----------------:|
| belasting_cognitief | 0.03 ⬇ | 0.09 | 0.08 | 0.08 | 0.44x | 1.15x |
| belasting_emotioneel | 0.07 ⬆ | 0.02 | 0.02 | 0.02 | 2.91x | 0.95x |
| belasting_fysiek | 0.07 | 0.13 | 0.10 | 0.10 | 0.68x | 1.35x |
| belasting_gezin | 0.12 ⬇ | 0.22 | 0.20 | 0.20 | 0.60x | 1.12x |
| belasting_sociaal | 0.03 | 0.04 | 0.05 | 0.05 | 0.66x | 0.87x |
| recovery_actie | 0.08 ⬇ | 0.16 | 0.18 | 0.17 | 0.49x | 0.90x |
| symptoom_cognitief | 0.19 ⬆ | 0.00 ⬇ | 0.07 | 0.08 | 2.37x | 0.00x |
| symptoom_emotioneel | 0.00 | 0.00 | 0.00 | 0.00 | 0.00x | 0.00x |
| symptoom_fysiek | 0.92 | 0.53 | 0.65 | 0.67 | 1.37x | 0.80x |
| triggers_extern | 0.05 ⬆ | 0.00 | 0.00 | 0.01 | 8.72x | 0.00x |
| context_neutraal | 0.59 | 0.80 | 0.74 | 0.73 | 0.81x | 1.09x |

Markers: ⬆ = ≥1.5x overall rate (category over-represented), ⬇ = ≤0.66x and base rate > 5% (under-represented).

## Era comparison (the K## kind-of-crash thread, finally with note data)

| category | crash_early | crash_late | shift | leadup_early | leadup_late | shift |
|----------|-----------:|----------:|:-----|------------:|----------:|:-----|
| belasting_cognitief | 0.04 | 0.03 | -0.01 | 0.00 | 0.12 | +0.12 ⬆ |
| belasting_emotioneel | 0.04 | 0.09 | +0.06 | 0.00 | 0.03 | +0.03 |
| belasting_fysiek | 0.04 | 0.09 | +0.06 | 0.08 | 0.16 | +0.08 |
| belasting_gezin | 0.00 | 0.22 | +0.22 ⬆ | 0.15 | 0.25 | +0.10 |
| belasting_sociaal | 0.04 | 0.03 | -0.01 | 0.00 | 0.06 | +0.06 |
| recovery_actie | 0.11 | 0.06 | -0.05 | 0.23 | 0.12 | -0.11 ⬇ |
| symptoom_cognitief | 0.11 | 0.25 | +0.14 ⬆ | 0.00 | 0.00 | +0.00 |
| symptoom_emotioneel | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| symptoom_fysiek | 0.89 | 0.94 | +0.05 | 0.69 | 0.47 | -0.22 ⬇ |
| triggers_extern | 0.07 | 0.03 | -0.04 | 0.00 | 0.00 | +0.00 |
| context_neutraal | 0.52 | 0.66 | +0.14 ⬆ | 0.77 | 0.81 | +0.04 |

Era split at 2023-12-31 (analytical convenience, not a real phase boundary — see synthesis).
Markers: ⬆/⬇ = shift of ±10 percentage points between early and late.

## How to read this

- The first table answers: **which kinds of clauses are over-represented before vs during crashes?** vs the baseline of all notes.
- The second table answers: **has the user's *language about crashes* shifted across years?** Direct K## evidence at the level of subjective experience.
- Both tables use **per-day category presence rates** (a day with the category mentioned in ≥1 clause counts as 1 for that category), not per-clause rates, because the day is the unit of analysis for crash labelling.

## Caveats

- **Note coverage is uneven across years** (18% in 2022 → 71% in 2024 → 44% in 2026). The era-shift table is affected by this: the late era's averages are computed over fewer notes. Significant shifts should still hold up; subtle ones may be noise.
- **Substring matching is imperfect** — "emotioneel" matches both `belasting_emotioneel` (via the phrase "emotioneel") and `symptoom_emotioneel` (some emotional symptoms). Multi-labeling absorbs this fine for category-presence rates but be aware when inspecting individual clauses.
- **Clause segmentation is naïve** — splits on punctuation + conjunctions. A clause like "hoofdpijn en moe" splits into ["hoofdpijn", "moe"], which is fine for category presence; a clause like "slecht geslapen door spanning" stays whole because there's no clause-splitter, which is also fine (both categories fire on the whole clause).
- **`context_neutraal` is the residual.** A high rate of context_neutraal in a group means many clauses in that group didn't match any positive category — could mean the dictionary is missing patterns, or that the group genuinely contains a lot of mundane day-shape content.
