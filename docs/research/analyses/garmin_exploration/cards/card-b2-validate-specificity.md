# Card (b2) — validate-era retrospective per-crash — specificity / precision / posterior tables

**Locked 2026-06-07** per [specificity-tables-spec.md](../methodology/specificity-tables-spec.md). Derivative computation over locked result-data.json files. Required output before any card.md is drafted (playbook §2.7 + §6.2).

## Era parameters

- **Era**: validate (post-cliff era)
- **Days in window**: 887
- **crash_v1 episodes**: 15
- **Base rate** P(crash on any day) = **1.69%**

## Main table

| anchor | recall | null_fire | disc (pp) | magnitude | **precision** | **lift** | F1 | implication |
|---|---:|---:|---:|---|---:|---:|---:|---|
| HA07d validate 4d N_std=1.5 bidirectional (sleep stress variability) | 86.7% | 65.0% | +21.7 | 2.752 (median |z|) | **2.24%** | **1.33×** | 0.0437 | Tier C — too broad as forward signal; retrospective annotation only |
| HA10 validate 4d N_std=1.5 bidirectional (morning BB peak z) | 86.7% | 70.5% | +16.2 | 2.121 (median |z|) | **2.07%** | **1.22×** | 0.0405 | Tier C — too broad as forward signal; retrospective annotation only |

## Notes per anchor

- **HA07d validate 4d N_std=1.5 bidirectional (sleep stress variability)**: PRIMARY anchor for Card (b2) validate-era; project's only overall-SUPPORTED + v2-validated finding
- **HA10 validate 4d N_std=1.5 bidirectional (morning BB peak z)**: Corroborating: v2 RESCUE Cat 3 rising/late-peak

## Base-rate sensitivity

Precision computed at 0.5×, 1×, 2× the locked base rate (captures uncertainty about whether the era's crash rate is representative).

| anchor | precision @ 0.85% | precision @ 1.69% (locked) | precision @ 3.38% |
|---|---:|---:|---:|
| HA07d validate 4d N_std=1.5 bidirectional (sleep stress variability) | 1.12% | **2.24%** | 4.46% |
| HA10 validate 4d N_std=1.5 bidirectional (morning BB peak z) | 1.04% | **2.07%** | 4.13% |

## Reading guide

- **recall** = P(card fires | crash on day D) — same as the result.md `frac_event` column
- **null_fire** = P(card fires | random day D) — same as `frac_null`
- **precision** = P(crash on day D | card fires on day D) — the Bayes posterior
- **lift** = precision / base_rate — how much firing multiplies the prior
- **F1** = 2 · precision · recall / (precision + recall)

Implication tiers per [spec §7](../methodology/specificity-tables-spec.md):
- **Tier A**: lift ≥ 5× AND precision ≥ 30% — informative for next-N-day awareness
- **Tier B**: lift 2-5× AND precision 5-30% — reflective use only, no alerting
- **Tier C**: lift < 2× OR precision < 5% — retrospective annotation only

Tier C is the playbook §6.6 no-go boundary: no crash-risk %, traffic lights, push notifications, or automated targets regardless of recall/discrimination magnitude.