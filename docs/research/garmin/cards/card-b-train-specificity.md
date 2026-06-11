# Card (b) — train-era retrospective per-crash — specificity / precision / posterior tables

**Locked 2026-06-07** per [specificity-tables-spec.md](../methodology/specificity-tables-spec.md). Derivative computation over locked result-data.json files. Required output before any card.md is drafted (playbook §2.7 + §6.2).

## Era parameters

- **Era**: train (pre-cliff era)
- **Days in window**: 485
- **crash_v1 episodes**: 14
- **Base rate** P(crash on any day) = **2.89%**

## Main table

| anchor | recall | null_fire | disc (pp) | magnitude | **precision** | **lift** | F1 | implication |
|---|---:|---:|---:|---|---:|---:|---:|---|
| H02b train 3d (max contiguous stress >=75 >=5min, delta >=+10 min) | 71.4% | 41.5% | +29.9 | 16.215 (median delta (min)) | **4.87%** | **1.69×** | 0.0911 | Tier C — too broad as forward signal; retrospective annotation only |
| H02d train bridge x 5d (sentinel-corrected spike) | 92.3% | 60.5% | +31.8 | 28.200 (median delta (min)) | **4.34%** | **1.50×** | 0.0829 | Tier C — too broad as forward signal; retrospective annotation only |
| HA07d train 4d N_std=1.5 bidirectional (sleep stress variability) | 84.6% | 65.0% | +19.6 | 2.541 (median |z|) | **3.73%** | **1.29×** | 0.0714 | Tier C — too broad as forward signal; retrospective annotation only |
| HA11 train 4d N_std=1.5 one-sided elevated (U-dip event count) | 64.3% | 41.5% | +22.8 | 2.168 (median signed z) | **4.40%** | **1.52×** | 0.0824 | Tier C — too broad as forward signal; retrospective annotation only |
| HA07c train 4d N_std=1.5 one-sided elevated (sleep stress mean delta) | 69.2% | 46.0% | +23.2 | 1.677 (median signed z) | **4.28%** | **1.48×** | 0.0807 | Tier C — too broad as forward signal; retrospective annotation only |
| HA08c train 4d N_std=1.5 one-sided elevated (sleep stress slope) | 61.5% | 38.5% | +23.0 | 2.116 (median signed z) | **4.54%** | **1.57×** | 0.0845 | Tier C — too broad as forward signal; retrospective annotation only |
| HA06b train 4d N_std=1.5 bidirectional (RHR z-score) | 71.4% | 52.5% | +18.9 | — | **3.89%** | **1.35×** | 0.0737 | Tier C — too broad as forward signal; retrospective annotation only |

## Notes per anchor

- **H02b train 3d (max contiguous stress >=75 >=5min, delta >=+10 min)**: PRIMARY anchor for Card (b) train-era
- **H02d train bridge x 5d (sentinel-corrected spike)**: Corroborating: strongest train-era discrimination (+31.8 pp)
- **HA07d train 4d N_std=1.5 bidirectional (sleep stress variability)**: Cross-era anchor: both-eras SUPPORTED + v2 RESCUE
- **HA11 train 4d N_std=1.5 one-sided elevated (U-dip event count)**: Corroborating: v2 RESCUE Cat 1 canonical decline
- **HA07c train 4d N_std=1.5 one-sided elevated (sleep stress mean delta)**: Corroborating: train SUPPORTED (HRV-proxy)
- **HA08c train 4d N_std=1.5 one-sided elevated (sleep stress slope)**: Corroborating: train SUPPORTED (multi-day creep)
- **HA06b train 4d N_std=1.5 bidirectional (RHR z-score)**: Reported for completeness; PERMANENTLY DEMOTED by v2 Cat 4 CLOSE (not used for card framing)

## Base-rate sensitivity

Precision computed at 0.5×, 1×, 2× the locked base rate (captures uncertainty about whether the era's crash rate is representative).

| anchor | precision @ 1.44% | precision @ 2.89% (locked) | precision @ 5.77% |
|---|---:|---:|---:|
| H02b train 3d (max contiguous stress >=75 >=5min, delta >=+10 min) | 2.46% | **4.87%** | 9.54% |
| H02d train bridge x 5d (sentinel-corrected spike) | 2.19% | **4.34%** | 8.55% |
| HA07d train 4d N_std=1.5 bidirectional (sleep stress variability) | 1.87% | **3.73%** | 7.39% |
| HA11 train 4d N_std=1.5 one-sided elevated (U-dip event count) | 2.22% | **4.40%** | 8.67% |
| HA07c train 4d N_std=1.5 one-sided elevated (sleep stress mean delta) | 2.16% | **4.28%** | 8.44% |
| HA08c train 4d N_std=1.5 one-sided elevated (sleep stress slope) | 2.29% | **4.54%** | 8.92% |
| HA06b train 4d N_std=1.5 bidirectional (RHR z-score) | 1.95% | **3.89%** | 7.69% |

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