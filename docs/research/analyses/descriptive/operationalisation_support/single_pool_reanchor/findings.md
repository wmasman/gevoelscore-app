# Findings - R14 single-pool re-anchor cross-check

**Strand A operationalisation-support analysis** - executes the binding recipe at [`methodology/train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) Sec 5.7 (single-pool re-run cross-check; descriptive, not a re-lock).
**Surface**: full Stratum 4 single pool, 2022-09-03 to 2026-06-05 (n_days=1372; n_crash_episodes=29). Block-permutation null at E[L]=7, B=10,000, seed `20260624`. Stationary bootstrap 95% CI on the discrimination statistic (pp) at the same E[L]. Null sample size n=200 per HA leadup-window-length (legacy seed `20260605` for reference-frame inheritance).
**Discipline binding**: Layer 1 descriptive cross-check per [CONVENTIONS Sec 2.1](../../../../CONVENTIONS.md). Locked HA `result.md` files are UNCHANGED per Sec 5.7 bullets 6-8. Train-vs-validate divergence is a **number, not a narrative** per Sec 5.7 bullet 8. No framework is pre-committed as correct per Sec 5.7 bullet 7. Single-pool verdicts are NOT promoted to SUPPORTED on their own per Sec 5.7 bullet 8; they are descriptive overlays. The HA01b legacy +17.3 pp validate divergence is NOT anchored on per Sec 5.7 bullet 8 (v3.1 rolling-baseline artefact; v3.2 lagged-baseline recomputed is canonical).
---
## 1. Headline
Cross-check evaluated 7 primary HAs + 5 stretch HAs (12 total) for **single-pool primary verdict robustness** to era partition. On the single pool, 12 HAs CONVERGE (single-pool primary verdict matches the locked era-split overall verdict per the HA's own Sec 5 rule); 0 HAs DIVERGE; 0 INCONCLUSIVE.
**The cross-check answers**: "is the primary single-pool verdict robust to era partition?" It does NOT answer "does the effect change over time?" - the single-subject observational design cannot answer that. Per Sec 5.7 bullet 8.
---
## 2. Side-by-side table
One row per HA. Locked-verdict column reads the headline number from the HA's locked `result.md` (NOT modified by this cross-check). Single-pool columns are derived on the full Stratum 4 pool per Sec 5.7 recipe.
| HA | locked verdict (era-split, OVERALL) | locked train disc | locked validate disc | n_single_pool (crash / null) | single-pool disc pp (CI95) | single-pool perm p (E[L]=7) | single-pool verdict | divergence | driver note (descriptive) |
|---|---|---:|---:|---|---:|---:|---|---|---|
| **HA01b-recomputed** | REFUTED both eras | +5.8 | +4.0 | 28 / 200 | +5.1 [-14.7, +13.3] | 0.3689 | NOT-SUPPORTED | CONVERGE (both NOT-SUPPORTED) | locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework. |
| **HA07c** | TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED | +23.2 | -6.0 | 25 / 189 | +10.8 [-22.5, +20.7] | 0.2148 | NOT-SUPPORTED | CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED) | locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples. |
| **HA07d** | BOTH ERAS SUPPORTED -> OVERALL SUPPORTED (only canonical both-eras-SUPPORTED test) | +19.6 | +21.7 | 25 / 189 | +19.7 [-18.1, +17.0] | 0.0291 | SUPPORTED | CONVERGE (both SUPPORTED) | locked era-split and single-pool both SUPPORTED; cross-check confirms SUPPORTED status under single-pool MD2+MD3 framework. |
| **HA08c** | TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED | +23.0 | +1.5 | 25 / 197 | +13.4 [-20.7, +22.3] | 0.1464 | NOT-SUPPORTED | CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED) | locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples. |
| **HA10** | TRAIN REFUTED (-20.5) / VALIDATE SUPPORTED (+16.2) / OVERALL REFUTED; era-directionality reversal (train 100% lowered, validate 69% elevated) | -20.5 | +16.2 | 26 / 199 | +4.1 [-16.5, +16.8] | 0.4328 | NOT-SUPPORTED | CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED) | locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples. |
| **HA11** | TRAIN SUPPORTED / VALIDATE REFUTED (inverse) / OVERALL REFUTED | +22.8 | -10.7 | 24 / 171 | +16.8 [-22.4, +20.4] | 0.0906 | NOT-SUPPORTED | CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED) | locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples. |
| **HA01c** | BOTH ERAS SUPPORTED -> OVERALL SUPPORTED (load-bearing WITHHELD pending v2 threshold-monotonicity diagnostic) | +21.3 | +19.5 | 28 / 200 | +19.6 [-19.6, +19.1] | 0.0290 | SUPPORTED | CONVERGE (both SUPPORTED) | locked era-split and single-pool both SUPPORTED; cross-check confirms SUPPORTED status under single-pool MD2+MD3 framework. |
| **H01** (stretch) | REFUTED both eras | -1.2 | -9.5 | 26 / 121 | -3.1 [-9.4, +10.1] | 0.7820 | NOT-SUPPORTED | CONVERGE (both NOT-SUPPORTED) | locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework. |
| **H02b** (stretch) | TRAIN SUPPORTED / VALIDATE refuted (near-miss) / OVERALL REFUTED | +29.9 | -8.2 | 26 / 200 | +3.5 [-21.2, +21.7] | 0.4458 | NOT-SUPPORTED | CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED) | locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples. |
| **H04** (stretch) | REFUTED both eras (validate near-miss +13.3 pp) | -5.7 | +13.3 | 26 / 121 | +0.5 [-5.8, +9.1] | 0.6280 | NOT-SUPPORTED | CONVERGE (both NOT-SUPPORTED) | locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework. |
| **HA06b** (stretch) | TRAIN SUPPORTED / VALIDATE refuted / OVERALL REFUTED | +18.9 | +0.8 | 26 / 195 | +6.7 [-18.7, +17.9] | 0.3368 | NOT-SUPPORTED | CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED) | locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples. |
| **H03** (stretch) | REFUTED both eras | +0.0 | +0.0 | 26 / 120 | +0.0 [+0.0, +0.0] | 1.0000 | NOT-SUPPORTED | CONVERGE (both NOT-SUPPORTED) | locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework. |

---
## 3. Per-HA narrative notes
Per Sec 5.7 bullet 8 "number, not narrative" discipline: 1-3 sentences per HA, describing the cross-check finding + naming plausible drivers descriptively where divergence is observed. NO causal claims; NO framework-correctness claims.
### 3.x HA01b-recomputed
- **Operand**: frac windows with >=1 day in 4-day leadup at exertion_class_lagged in {heavy, very_heavy}.
- **Locked era-split verdict**: REFUTED both eras (train +5.8 pp, validate +4.0 pp; see [`analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md`](../../../../analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md)).
- **Single-pool**: disc_pp=+5.1, CI95=[-14.7, +13.3], perm p (E[L]=7) = 0.3689; frac_crash=0.821, frac_null=0.770; crit_a=True, crit_b=False, crit_c=True; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE (both NOT-SUPPORTED).
- **Driver (descriptive)**: locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework.

### 3.x HA07c
- **Operand**: max signed z (4d) of night-over-night delta of stress_mean_sleep; lagged baseline [d-90, d-30] trimmed; sigma_floor=2.0.
- **Locked era-split verdict**: TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED (train +23.2 pp, validate -6.0 pp; see [`analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md`](../../../../analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md)).
- **Single-pool**: disc_pp=+10.8, CI95=[-22.5, +20.7], perm p (E[L]=7) = 0.2148; frac_crash=0.600, frac_null=0.492; crit_a=True, crit_b=False, crit_c=True; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED).
- **Driver (descriptive)**: locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples.

### 3.x HA07d
- **Operand**: max |z| (4d, bidirectional) of night-over-night delta of stress_stdev_sleep; lagged baseline; sigma_floor=0.5.
- **Locked era-split verdict**: BOTH ERAS SUPPORTED -> OVERALL SUPPORTED (only canonical both-eras-SUPPORTED test) (train +19.6 pp, validate +21.7 pp; see [`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md)).
- **Single-pool**: disc_pp=+19.7, CI95=[-18.1, +17.0], perm p (E[L]=7) = 0.0291; frac_crash=0.880, frac_null=0.683; crit_a=True, crit_b=True, crit_c=True; verdict (single-pool) = **SUPPORTED**.
- **Divergence**: CONVERGE (both SUPPORTED).
- **Driver (descriptive)**: locked era-split and single-pool both SUPPORTED; cross-check confirms SUPPORTED status under single-pool MD2+MD3 framework.

### 3.x HA08c
- **Operand**: max signed z (4d) of trailing-5d OLS slope of stress_mean_sleep; lagged baseline of slopes; sigma_floor=0.5/day.
- **Locked era-split verdict**: TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED (train +23.0 pp, validate +1.5 pp; see [`analyses/hypotheses/HA08c-sleep-stress-slope/result.md`](../../../../analyses/hypotheses/HA08c-sleep-stress-slope/result.md)).
- **Single-pool**: disc_pp=+13.4, CI95=[-20.7, +22.3], perm p (E[L]=7) = 0.1464; frac_crash=0.560, frac_null=0.426; crit_a=False, crit_b=False, crit_c=True; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED).
- **Driver (descriptive)**: locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples.

### 3.x HA10
- **Operand**: max |z| (4d, bidirectional) of bb_highest (morning BB peak proxy via UDS); lagged baseline; sigma_floor=2.0 BB points.
- **Locked era-split verdict**: TRAIN REFUTED (-20.5) / VALIDATE SUPPORTED (+16.2) / OVERALL REFUTED; era-directionality reversal (train 100% lowered, validate 69% elevated) (train -20.5 pp, validate +16.2 pp; see [`analyses/hypotheses/HA10-bb-overnight-recharge/result.md`](../../../../analyses/hypotheses/HA10-bb-overnight-recharge/result.md)).
- **Single-pool**: disc_pp=+4.1, CI95=[-16.5, +16.8], perm p (E[L]=7) = 0.4328; frac_crash=0.769, frac_null=0.729; crit_a=True, crit_b=False, crit_c=True; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED).
- **Driver (descriptive)**: locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples.

### 3.x HA11
- **Operand**: max signed z (4d) of u_dip_count (per-day count primitive in master); lagged baseline; sigma_floor=0.5 events.
- **Locked era-split verdict**: TRAIN SUPPORTED / VALIDATE REFUTED (inverse) / OVERALL REFUTED (train +22.8 pp, validate -10.7 pp; see [`analyses/hypotheses/HA11-stress-udip/result.md`](../../../../analyses/hypotheses/HA11-stress-udip/result.md)).
- **Single-pool**: disc_pp=+16.8, CI95=[-22.4, +20.4], perm p (E[L]=7) = 0.0906; frac_crash=0.583, frac_null=0.415; crit_a=False, crit_b=True, crit_c=True; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED).
- **Driver (descriptive)**: locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples.

### 3.x HA01c
- **Operand**: frac windows with >=1 day in 4-day leadup at eff_exertion_rank_lagged >= 0.75; median rank on triggering episodes >= 0.875.
- **Locked era-split verdict**: BOTH ERAS SUPPORTED -> OVERALL SUPPORTED (load-bearing WITHHELD pending v2 threshold-monotonicity diagnostic) (train +21.3 pp, validate +19.5 pp; see [`analyses/hypotheses/HA01c-effective-exertion-shock/result.md`](../../../../analyses/hypotheses/HA01c-effective-exertion-shock/result.md)).
- **Single-pool**: disc_pp=+19.6, CI95=[-19.6, +19.1], perm p (E[L]=7) = 0.0290; frac_crash=0.821, frac_null=0.625; crit_a=True, crit_b=True, crit_c=True; verdict (single-pool) = **SUPPORTED**.
- **Divergence**: CONVERGE (both SUPPORTED).
- **Driver (descriptive)**: locked era-split and single-pool both SUPPORTED; cross-check confirms SUPPORTED status under single-pool MD2+MD3 framework.

### 3.x H01 (stretch)
- **Operand**: frac windows with mean RHR (7d leadup) - trimmed baseline >= +3 bpm.
- **Locked era-split verdict**: REFUTED both eras (train -1.2 pp, validate -9.5 pp; see [`analyses/hypotheses/H01-rhr-drift/result.md`](../../../../analyses/hypotheses/H01-rhr-drift/result.md)).
- **Single-pool**: disc_pp=-3.1, CI95=[-9.4, +10.1], perm p (E[L]=7) = 0.7820; frac_crash=0.077, frac_null=0.107; crit_a=False, crit_b=False, crit_c=False; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE (both NOT-SUPPORTED).
- **Driver (descriptive)**: locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework.

### 3.x H02b (stretch)
- **Operand**: frac windows where max(max_spike_minutes - trimmed_baseline) over 3-day leadup >= +10 min.
- **Locked era-split verdict**: TRAIN SUPPORTED / VALIDATE refuted (near-miss) / OVERALL REFUTED (train +29.9 pp, validate -8.2 pp; see [`analyses/hypotheses/H02b-stress-spikes/result.md`](../../../../analyses/hypotheses/H02b-stress-spikes/result.md)).
- **Single-pool**: disc_pp=+3.5, CI95=[-21.2, +21.7], perm p (E[L]=7) = 0.4458; frac_crash=0.500, frac_null=0.465; crit_a=False, crit_b=False, crit_c=True; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED).
- **Driver (descriptive)**: locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples.

### 3.x H04 (stretch)
- **Operand**: frac windows where mean BB net-drain (7d leadup) - baseline <= -5 BB units (bb_net_drain = drained_24h - charged_24h).
- **Locked era-split verdict**: REFUTED both eras (validate near-miss +13.3 pp) (train -5.7 pp, validate +13.3 pp; see [`analyses/hypotheses/H04-body-battery/result.md`](../../../../analyses/hypotheses/H04-body-battery/result.md)).
- **Single-pool**: disc_pp=+0.5, CI95=[-5.8, +9.1], perm p (E[L]=7) = 0.6280; frac_crash=0.038, frac_null=0.033; crit_a=False, crit_b=False, crit_c=False; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE (both NOT-SUPPORTED).
- **Driver (descriptive)**: locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework.

### 3.x HA06b (stretch)
- **Operand**: max |z| (4d, bidirectional) of resting_hr; lagged baseline; sigma_floor=0.5 bpm.
- **Locked era-split verdict**: TRAIN SUPPORTED / VALIDATE refuted / OVERALL REFUTED (train +18.9 pp, validate +0.8 pp; see [`analyses/hypotheses/HA06b-rhr-zscore/result.md`](../../../../analyses/hypotheses/HA06b-rhr-zscore/result.md)).
- **Single-pool**: disc_pp=+6.7, CI95=[-18.7, +17.9], perm p (E[L]=7) = 0.3368; frac_crash=0.615, frac_null=0.549; crit_a=True, crit_b=False, crit_c=True; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED).
- **Driver (descriptive)**: locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples.

### 3.x H03 (stretch)
- **Operand**: frac windows where mean sleep-efficiency (7d leadup) - trimmed baseline <= -0.05 (eff = (deep+light)/(deep+light+awake+unmeasurable)).
- **Locked era-split verdict**: REFUTED both eras (train +0.0 pp, validate +0.0 pp; see [`analyses/hypotheses/H03-sleep-efficiency/result.md`](../../../../analyses/hypotheses/H03-sleep-efficiency/result.md)).
- **Single-pool**: disc_pp=+0.0, CI95=[+0.0, +0.0], perm p (E[L]=7) = 1.0000; frac_crash=0.000, frac_null=0.000; crit_a=False, crit_b=False, crit_c=False; verdict (single-pool) = **NOT-SUPPORTED**.
- **Divergence**: CONVERGE (both NOT-SUPPORTED).
- **Driver (descriptive)**: locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework.

---
## 4. Aggregate cross-check summary
Of the 12 HAs evaluated:

- **12 CONVERGE** (locked overall verdict <-> single-pool verdict).
- **0 DIVERGE**.
- **0 INCONCLUSIVE** on single-pool primitive.

Pattern observations (descriptive only):
- HAs whose locked OVERALL-SUPPORTED verdict reproduces under single-pool: HA07d, HA01c.
- HAs whose locked overall NOT-SUPPORTED status reproduces under single-pool: HA01b-recomputed, H01, H04, H03.
- HAs whose locked split-mixed (one-era SUPPORTED, other-era REFUTED -> OVERALL REFUTED) verdict converges with single-pool NOT-SUPPORTED (direction-cancellation under single-pool plausible per Sec 5.7 bullet 7): HA07c, HA08c, HA10, HA11, H02b, HA06b.

Per Sec 5.7 bullet 8 discipline: these patterns are descriptive only. No conclusion about "the framework that's correct" is asserted. The locked verdicts remain on record as the historical evidence for the era-split framework; the single-pool verdicts surfaced here are descriptive cross-check overlays for the MD2+MD3 framework. **User decides** on any follow-up per Sec 5.7 bullet 7.
---
## 5. Deferred / out-of-scope HAs
Per stocktake Sec 9 + REJECTED.md Appendix:

| HA | reason | reference |
|---|---|---|
| H02 | SUPERSEDED-by-H02b (daily-aggregate stress -> per-minute spike count); cross-check covers via H02b. | [REJECTED.md 2026-06-05](../../../../REJECTED.md) |
| H02d | SUPERSEDED-by-equivalence (H02b == H02d at rho=+1.000 per cross-channel-correlation card). | [REJECTED.md 2026-06-06](../../../../REJECTED.md) |
| H03b | RETIRED - data-resolution limit (INCONCLUSIVE x 12 cells; data does not exist at gated resolution). | [REJECTED.md Appendix](../../../../REJECTED.md) |
| H05 | RETIRED - spec-induced trivial. | [REJECTED.md Appendix](../../../../REJECTED.md) |
| HA01b-per-axis-diagnostic | NOT-RUN in cross-check (DIAGNOSTIC bound to HA01b parent; inheriting cross-check from HA01b-recomputed). | parent: HA01b-recomputed |
| HA06 | SUPERSEDED-by-HA06b (absolute-threshold mis-cal -> z-score). | [REJECTED.md 2026-06-07](../../../../REJECTED.md) |
| HA07 | SUPERSEDED-by-proxy (FR245 HRV hardware-blocked; HA07c proxy). | [REJECTED.md Appendix](../../../../REJECTED.md) |
| HA08 | SUPERSEDED-by-proxy (same FR245 hardware blocker; HA08c proxy). | [REJECTED.md Appendix](../../../../REJECTED.md) |
| S02b | SHELVED-BLOCKED-BY-S02. | [REJECTED.md Appendix](../../../../REJECTED.md) |
| K01 | NOT-APPLICABLE (cross-era contrast - the era split IS the predictor). | [K01 result.md](../../../hypotheses/K01-crash-depth/result.md) |
| K02 | NOT-APPLICABLE (same as K01). | [K02 result.md](../../../hypotheses/K02-crash-duration/result.md) |
| threshold-monotonicity diagnostics (HA01c-v2, HA06b-v2, HA07d, HA07d-v2, HA10, HA10-v2, HA11-v2) | inherit cross-check from parent HA per testing playbook. | parents covered above |

**R14-v2 closed** (2026-06-30): HA01c (effective_exertion rank shock; primary scope) and H03 (sleep_efficiency drop; stretch scope) are now COMPUTED and reported in the Sec 2 table + Sec 3 narrative above; they are no longer deferred. HA06b is covered as stretch. The remaining NOT-BACKSTOPPED HAs from stocktake Sec 5 close in a future R14-v3 session.
---
## 6. Implications for the synthesis_structure_map (descriptive only)
Per Sec 5.7 bullet 7: this cross-check **does not** auto-promote any HA's synthesis-structure-map standing. Reading is user-owned.

Stocktake-style enumeration of HAs whose assumption-cell A8 (`single-pool primary preserved per train_validate_split_fate.md`) is now backstopped by this cross-check (potentially eligible to transition NOT-BACKSTOPPED -> Stage D TRUSTED on A8, pending review of other NOT-BACKSTOPPED cells per stocktake Sec 5):

- **HA01b-recomputed**: A8 cell backstopped by this cross-check (CONVERGE (both NOT-SUPPORTED)).
- **HA07c**: A8 cell backstopped by this cross-check (CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED)).
- **HA07d**: A8 cell backstopped by this cross-check (CONVERGE (both SUPPORTED)).
- **HA08c**: A8 cell backstopped by this cross-check (CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED)).
- **HA10**: A8 cell backstopped by this cross-check (CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED)).
- **HA11**: A8 cell backstopped by this cross-check (CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED)).
- **HA01c**: A8 cell backstopped by this cross-check (CONVERGE (both SUPPORTED)).
- **H01**: A8 cell backstopped by this cross-check (CONVERGE (both NOT-SUPPORTED)).
- **H02b**: A8 cell backstopped by this cross-check (CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED)).
- **H04**: A8 cell backstopped by this cross-check (CONVERGE (both NOT-SUPPORTED)).
- **HA06b**: A8 cell backstopped by this cross-check (CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED)).
- **H03**: A8 cell backstopped by this cross-check (CONVERGE (both NOT-SUPPORTED)).

**Important**: backstopping A8 alone does not move an HA to Stage D TRUSTED; per stocktake Sec 5 most older HAs also carry Shared gap 1 (per-channel ACF / E[L]\* never run on the pre-MD verdicts) + Shared gap 3 (per-cell missingness audit). Those remain to be closed by separate descriptive runs.

Of the 16 HAs that stocktake Sec 3 Shared gap 2 enumerated, this cross-check closes A8 on 12 of them (HA01c + H03 added in the 2026-06-30 R14-v2 extension); remaining 4 (H02, H02d, H03b, HA01b-diag) continue to carry NOT-BACKSTOPPED A8 until a future descriptive backstop arrives via another path. H02 and H02d are SUPERSEDED in the registry (so closure is procedural rather than empirical); H03b is RETIRED per stocktake Sec 9; HA01b-diag inherits from HA01b-recomputed which IS covered. There are no genuinely uncovered HAs remaining in the Shared gap 2 set.
---
## 7. Caveats per CONVENTIONS Sec 4.1 + Sec 4.2
- **Operationalised cross-check, no causal claim** (Sec 4.1). The single-pool numbers characterise the same operand evaluated on a different reference frame; they do NOT claim what causes the divergence or convergence.
- **Layer 1 descriptive** (Sec 2.1). No falsification bar in this cross-check itself; the per-HA verdicts evaluated here are the HAs' own locked bars applied to single-pool numbers. No new inferential commitment.
- **Locked verdicts UNCHANGED** regardless of cross-check outcome per Sec 5.7 bullet 6. The HA `result.md` files remain as historical evidence for the era-split framework. This cross-check produces descriptive overlays; it does NOT re-lock.
- **User-owned decision on any follow-up** per Sec 5.7 bullet 7. New pre-reg / methodology revision / per-HA footnote / R14-v2 scope expansion are separate sessions.
- **Block-permutation null + stationary bootstrap CI** uses E[L]=7 per project default. Per stocktake Sec 5 Shared gap 1, several channels have not had their per-channel data-driven E[L]\* characterised on Stratum 4 (only `stress_mean_sleep` and `stress_low_motion_min_count_S60_Mlow` are landed at the Strand A level). A factor-of-2 deviation from E[L]=7 on a specific channel could shift specific p-values; the discrimination point estimate is less sensitive to this.
- **Cross-check inherits the locked HA's null reference scheme** (200 non-overlapping random windows seeded `20260605`) for per-HA continuity. The new framework's choice of null (block-permutation at E[L]=7) operates on top of the same reference dates; the p-value reported is therefore the new-framework p-value on the same window set.
- **`per_day_master.csv` snapshot at run time**: the per-day master is the single source of truth for the operand re-extraction; HA-specific operand details may differ slightly from the original locked test scripts that read from cached extraction CSVs (e.g. HA01b originally reads from `activity_features_daily.csv`; HA11 originally reads from `udip_counts.csv`). The per_day_master columns are the project's canonical consolidated source per [DATA_DICTIONARY.md](../../../../DATA_DICTIONARY.md); using them in the cross-check is the consistent choice but introduces a small operand-routing difference from the locked tests.
- **No anchoring on the HA01b legacy +17.3 pp validate divergence** per Sec 5.7 bullet 8. The canonical HA01b is the lagged-baseline recomputed version (REFUTED both eras at +5.8 / +4.0 pp), not the v3.1 rolling-baseline artefact.
---
## 8. Verification log
- **R14-v2 extension (2026-06-30)**: HA01c (primary) + H03 (stretch) added to scope under the SAME recipe as the original 10 HAs (full Stratum 4 single pool, n_crash_episodes=29; block-permutation null E[L]=7; B=10,000; null sample seed `20260605`; bootstrap/perm seed `20260624`; N_std primary 1.5; leadup 4 days for HA01c, 7 days for H03). HA01c operand = `eff_exertion_rank_lagged >= 0.75` (the v3.2 _lagged column the locked HA01c test used; per CONVENTIONS §3.2 the `_lagged_lcera` variant is near-identical on the all-LC Stratum 4 pool). H03 operand = 7d-leadup mean sleep-efficiency minus [d-97, d-8] trimmed baseline <= -0.05; efficiency reconstructed from per_day_master `(sleep_deep_min + sleep_light_min) / (deep + light + awake + unmeasurable)` (no `sleep_rem_min` on FR245 per DATA_DICTIONARY.md, so light absorbs REM and the reconstruction is construction-equivalent to the locked test's deep+light+rem). §3.4 crash-drop sensitivity: the single pool inherits the same 29-episode crash_v2 set; no per-episode drop sweep is re-run at the cross-check layer (the locked HA verdicts carry their own sensitivity records).
- **As-of-date**: 2026-06-05 (Stratum 4 right edge for this run).
- **Stratum 4 start**: 2022-09-03.
- **n_days in Stratum 4 master**: 1372.
- **n_crash_episodes in Stratum 4 single pool**: 29.
- **Null sample sizes**: 4d leadup n=200; 7d leadup n=122; 3d leadup n=200.
- **Block length E[L]**: 7 (project default per `permutation_null_block_length.md`).
- **n_bootstrap / n_permutations**: 10,000.
- **Bootstrap + permutation seed**: `20260624` (per handoff Sec 2.4).
- **Null sample seed**: `20260605` (inherited from legacy HA pre-reg pattern; matches the locked HA reference frames).
- **N_std primary**: 1.5 (per locked HA pre-reg primary tier).
- **Leadup days primary**: 4.
- **Inference helpers**: [`analyses/_utils/inference.py`](../../../_utils/inference.py) (`stationary_bootstrap_ci`, `permutation_pvalue`, `compute_data_driven_block_length`).
- **Run timestamp (UTC)**: 2026-06-30T13:30:38.840916Z.
- **Operand-source path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` + `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv`.

**Locked HA `result.md` cross-references** (NOT modified by this cross-check):

- HA01b-recomputed: [`analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md`](../../../../analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md). Lagged-baseline (v3.2) recomputation of HA01b; canonical version per REJECTED.md.
- HA07c: [`analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md`](../../../../analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md). Sleep stress mean delta primitive; HRV-proxy chain.
- HA07d: [`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md). Sleep stress variability (stdev) delta primitive; bidirectional.
- HA08c: [`analyses/hypotheses/HA08c-sleep-stress-slope/result.md`](../../../../analyses/hypotheses/HA08c-sleep-stress-slope/result.md). Trailing-5d OLS slope of sleep stress; one-sided elevated.
- HA10: [`analyses/hypotheses/HA10-bb-overnight-recharge/result.md`](../../../../analyses/hypotheses/HA10-bb-overnight-recharge/result.md). Morning BB peak; bidirectional; only DIRECTIONALITY-REVERSAL test in project.
- HA11: [`analyses/hypotheses/HA11-stress-udip/result.md`](../../../../analyses/hypotheses/HA11-stress-udip/result.md). Within-day U-dip count; one-sided elevated.
- H01: [`analyses/hypotheses/H01-rhr-drift/result.md`](../../../../analyses/hypotheses/H01-rhr-drift/result.md). RHR drift over 7-day leadup at +3 bpm; absolute-threshold spec.
- H02b: [`analyses/hypotheses/H02b-stress-spikes/result.md`](../../../../analyses/hypotheses/H02b-stress-spikes/result.md). Per-minute stress spike count (3-day leadup); +10 min absolute threshold.
- H04: [`analyses/hypotheses/H04-body-battery/result.md`](../../../../analyses/hypotheses/H04-body-battery/result.md). BB net-drain over 7-day leadup at -5 BB units; absolute-threshold spec.
- HA06b: [`analyses/hypotheses/HA06b-rhr-zscore/result.md`](../../../../analyses/hypotheses/HA06b-rhr-zscore/result.md). RHR z-score (4d, bidirectional); permanently demoted to non-load-bearing per v2 diag.
- HA01c: [`analyses/hypotheses/HA01c-effective-exertion-shock/result.md`](../../../../analyses/hypotheses/HA01c-effective-exertion-shock/result.md). Effective-exertion rank shock (>= 0.75 in 4d leadup); SUPPORTED both eras at the locked 3-criterion bar; load-bearing gated on HA01c v2. R14-v2 close.
- H03: [`analyses/hypotheses/H03-sleep-efficiency/result.md`](../../../../analyses/hypotheses/H03-sleep-efficiency/result.md). Sleep-efficiency drop (>= 5pp) over 7d leadup; flat-as-a-board, REFUTED decisively both eras (0.0% trigger). R14-v2 close.

---

*End of findings.*
