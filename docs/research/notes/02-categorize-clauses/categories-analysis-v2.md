# Notes — categorized clauses v2 (3-layer model)

Built from locked [category_dictionary_v2.md](category_dictionary_v2.md) by [categorize_v2.py](categorize_v2.py).
Each clause now has: categories (layer 1), symptom_states (layer 2 via negation+severity modifiers), polarity (layer 3).

## Group sizes

- crash days: **59** (early 27, late 32)
- lead-up days: **45** (early 13, late 32)
- non-crash days: **582**
- total with notes: **686**

## Polarity at the clause-level: dominant polarity per day

How often does each group end up with a positive- vs negative-dominant day?

| group | day positive-dominant | day negative-dominant |
|-------|---------------------:|---------------------:|
| crash (n=59) | 0.32 | 0.07 |
| lead-up (n=45) | 0.27 | 0.09 |
| non-crash (n=582) | 0.41 | 0.03 |
| all (n=686) | 0.40 | 0.04 |

Era breakdown (crash + lead-up only):

| group | day positive-dom | day negative-dom |
|-------|----------------:|----------------:|
| crash early (n=27) | 0.11 | 0.00 |
| crash late (n=32) | 0.50 | 0.12 |
| lead-up early (n=13) | 0.31 | 0.08 |
| lead-up late (n=32) | 0.25 | 0.09 |

## Category rates with polarity split

For each category: presence (any clause), positive-polarity presence, negative-polarity presence.
`crash_p`/`crash_n` = % of crash days where this category appears in a positive / negative clause.

| category | crash | crash_p | crash_n | leadup | leadup_p | leadup_n | non-crash |
|----------|-----:|-------:|-------:|------:|--------:|--------:|---------:|
| belasting_cognitief | 0.03 | 0.00 | 0.00 | 0.09 | 0.00 | 0.00 | 0.08 |
| belasting_emotioneel | 0.07 | 0.00 | 0.00 | 0.07 | 0.00 | 0.00 | 0.04 |
| belasting_fysiek | 0.07 | 0.00 | 0.00 | 0.16 | 0.00 | 0.00 | 0.12 |
| belasting_gezin | 0.12 | 0.02 | 0.00 | 0.22 | 0.00 | 0.02 | 0.20 |
| belasting_sociaal | 0.03 | 0.00 | 0.00 | 0.04 | 0.00 | 0.00 | 0.05 |
| recovery_actie | 0.10 | 0.00 | 0.00 | 0.18 | 0.04 | 0.00 | 0.19 |
| symptoom_cognitief | 0.19 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.06 |
| symptoom_emotioneel | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| symptoom_fysiek | 0.92 | 0.19 | 0.03 | 0.53 | 0.16 | 0.07 | 0.68 |
| triggers_extern | 0.05 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Era comparison: crash-day polarity-split shifts

Looking at categories where polarity changes the story between early-era and late-era crashes.

| category | early_p | late_p | shift_p | early_n | late_n | shift_n |
|----------|--------:|------:|:-------|--------:|------:|:-------|
| belasting_cognitief | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| belasting_emotioneel | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| belasting_fysiek | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| belasting_gezin | 0.00 | 0.03 | +0.03 | 0.00 | 0.00 | +0.00 |
| belasting_sociaal | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| recovery_actie | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| symptoom_cognitief | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| symptoom_emotioneel | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| symptoom_fysiek | 0.11 | 0.25 | +0.14 ⬆ | 0.00 | 0.06 | +0.06 |
| triggers_extern | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |

## symptoom_fysiek state breakdown (the new view of the v1 92% finding)

v1 said "92% of crash days mention symptoom_fysiek" — but conflated 'geen hoofdpijn' with 'hoofdpijn'.
v2 separates by state (absent / mild / present / severe). The day's symptom_fysiek state is the worst observed across its clauses.

| group | absent | mild | present | severe | total mentioned |
|-------|------:|----:|-------:|------:|--------------:|
| crash (n=59) | 0.03 | 0.00 | 0.75 | 0.14 | 0.92 |
| lead-up (n=45) | 0.02 | 0.00 | 0.44 | 0.07 | 0.53 |
| non-crash (n=582) | 0.02 | 0.02 | 0.56 | 0.07 | 0.68 |
| all (n=686) | 0.02 | 0.02 | 0.57 | 0.08 | 0.69 |

## Era comparison: symptoom_fysiek state shifts on crash days

| state | early | late | shift |
|-------|-----:|----:|:-----|
| absent | 0.04 | 0.03 | -0.01 |
| mild | 0.00 | 0.00 | +0.00 |
| present | 0.81 | 0.69 | -0.13 ⬇ |
| severe | 0.04 | 0.22 | +0.18 ⬆ |

## How v2 changes the picture (informal)

Compare to v1's [categories-analysis.md](categories-analysis.md):

- **Polarity gives lead-up days a signal v1 missed.** Lead-up days were 80% context_neutraal in v1 — those clauses now have polarity even without a category match ("matig" → negative; "redelijk" → positive).
- **`symptoom_fysiek` on crashes is no longer 92% blindly**. Now broken into absent / mild / present / severe — the 92% becomes a more useful distribution.
- **`belasting_emotioneel` and `belasting_gezin` get polarity-split** so we can see whether they're recovery-supportive (positive) or load-additive (negative) in each group.
- **Era comparison gains polarity dimension** — for each category we can ask not just "did rate shift" but "did *positive* presence shift differently from *negative* presence?"
