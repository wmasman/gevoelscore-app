# Findings - R19 recovery-phase signal backdrop (each signal along the lived phases)

**Descriptive Layer-1 backdrop** for site request **R19** ("each primary signal
read along the recovery-phase axis"). Producer-mode, for the participant-researcher
(repo owner), drafted 2026-07-06 by Claude (Opus 4.8). Reproducible via
[`run.py`](run.py).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

**What this is**: the per-phase **shape** of each scorecard signal across the lived
recovery phases - per-phase median levels plus per-phase crash counts, as a
**backdrop to read against, not a set of verdicts**. Per the framing locked with
the participant-researcher (2026-07-06), this is the **level + crash-count** read;
per-phase **discrimination is declined-with-reason** (section 4). Boundaries are
lived-experience (M1), never data-tuned; a quiet phase is not a refutation; no
causal marks per [CONVENTIONS section 4.1](../../../CONVENTIONS.md). Robust central
tendency (median + p25/p75) per section 3.1; named counts per section 3.6.

**Axis**: the `recovery_phase` column of `per_day_master.csv` per
[`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md)
section 2. Within Stratum 4 (2022-09-03 to 2026-06-05, n_days=1372,
n_crash_episodes=29) crashes fall in four phases; phases 1-2 (pre_illness_healthy,
acute_infection) are pre-corpus Garmin-only and carry no crashes.

---

## 1. The per-phase crash backdrop

| phase | id | days | crashes | crash base rate | discrimination computable (n_crashes >= 10)? |
|---|---|---:|---:|---:|---|
| `lc_pre_ergo` | 3 | 19 | 2 | 10.5% (2 / 19) | no - **honest-limit** |
| `pacing_pre_citalopram_learning` | 4a | 56 | 1 | 1.8% (1 / 56) | no - **honest-limit** |
| `pacing_habit_established` | 4b | 509 | 15 | 2.9% (15 / 509) | yes |
| `citalopram_modulated` | 5 | 788 | 11 | 1.4% (11 / 788) | yes |
| **pooled (Stratum 4)** | - | 1372 | 29 | **2.1% (29 / 1372)** | (single-pool; R14) |

Reading discipline:

- **Only phases 4b and 5 carry enough crashes to read a rate at all.** Phase 3's
  10.5% is 2 crashes in a 19-day tail (the corpus opens mid-phase-3) and phase 4a's
  1.8% is a single crash; both are noise, not a phase signal.
- **Descriptively**, among the two readable phases, crashes were somewhat more
  frequent per-day in the pre-citalopram pacing-habit phase (4b, 2.9%) than in the
  citalopram era (5, 1.4%), with the pooled rate (2.1%) in between. This is a raw
  count ratio on small numbers, **not a verdict**, and the 4b-to-5 boundary is the
  citalopram-onset boundary - see section 4.

---

## 2. Per-signal per-phase level backdrop

Median [p25, p75] of each scorecard signal's channel, per phase (numeric signals);
fraction of days at a heavy / very-heavy exertion class for HA01b. `n` is the
per-phase count of non-null channel-days (presence-conditioned; it varies slightly
by channel through missingness). Crash counts repeated for reading against.

| signal | channel | phase 3 (n_cr 2) | phase 4a (n_cr 1) | phase 4b (n_cr 15) | phase 5 (n_cr 11) | across-phase shape |
|---|---|---|---|---|---|---|
| **HA07d** | `stress_stdev_sleep` | 8.24 [6.99, 9.23] | 7.77 [6.76, 9.11] | 8.14 [6.53, 9.88] | **6.63** [5.82, 8.16] | steps **down** in phase 5 |
| **HA07c** | `stress_mean_sleep` | 17.2 [14.7, 19.0] | 20.0 [18.1, 22.9] | 19.5 [16.7, 22.9] | 18.9 [16.3, 22.0] | up from the phase-3 tail, then flat ~19-20 |
| **H02b** | `max_spike_minutes` | 14 [7, 17] | 10 [6, 16] | 10 [6, 18] | **8** [0, 14] | declines across phases |
| **HA11** | `u_dip_count` | 1 [0, 1.5] | 1 [0, 2] | 1 [0, 2] | **0** [0, 1] | median drops to 0 in phase 5 |
| **HA10** | `bb_highest` | 85 [80, 94] | 76 [69, 82] | 78 [66, 87] | 81 [71, 89] | dips at phase-4 onset, recovers |
| **HA06b** | `resting_hr` | 50 [50, 51] | 53 [52, 54] | 56 [55, 57] | 57 [55, 59] | **monotone rise** 50 -> 57 |
| **HA01b** | `exertion_class_lagged` (frac heavy+) | 0.32 | 0.41 | 0.36 | 0.36 | roughly flat ~0.36 |

---

## 3. Reading the shapes (descriptive; attribution belongs to other analyses)

These are raw per-phase levels. Two of the shapes have obvious owners elsewhere,
and R19 deliberately **describes without attributing**:

- **Resting HR rises monotonically across the phases (50 -> 53 -> 56 -> 57).** This
  is the single most confounder-exposed shape: the slow drivers (weight, the
  deconditioning tail, aging) all co-trend with LC duration, so a level gap between
  early and late phases is part lived-phase and part slow drift. **Attribution is
  R30's** (net-of-slow-confounders re-read); the RHR confounder decomposition
  ([`analyses/longrun_rhr_trend/findings.md`](../../longrun_rhr_trend/findings.md))
  already establishes that the static level partition is not cleanly identifiable.
  R19 only reports the raw rise.
- **The stress-family channels step down in the citalopram era (phase 5):**
  sleep-stress variability 8.1 -> 6.6, per-minute spike-minutes 10 -> 8, U-dip
  median 1 -> 0. Phase 5 **is** the citalopram-modulated phase, and citalopram is
  the CONFIRMED down-driver on the stress channels
  ([`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md)
  section 2). So a large part of the phase-5 stress shape is the medication effect
  that **R20** already characterised on the discrimination side; R19 does not
  re-attribute it.
- **Body-battery ceiling and exertion** move little across phases (bb_highest dips
  at the phase-4 onset then recovers; heavy-exertion fraction is flat ~0.36).
- **Felt-state (`gevoelscore`) needs no confounder note** and is not a scorecard
  signal; it is the clean self-report axis and is handled by the recovery-arc
  descriptive substrate, not here.

Nothing in this section is a causal claim: "resting HR sat higher in the later
phases in this body", never "the later phase raised it".

---

## 4. Why per-phase discrimination is declined-with-reason

R19 could, in principle, re-run each signal's crash-discrimination operand
**within** each phase. It does not, and the reason is itself an honest finding:

1. **Only two phases can carry a discrimination number.** The operand needs
   n_crashes >= 10; phases 3 (2 crashes) and 4a (1 crash) are hopelessly
   under-powered. Only 4b (15) and 5 (11) qualify - and even those give CIs so wide
   they cannot support a verdict.
2. **Those two phases straddle the retired era-split.** The 4b-to-5 boundary
   (2024-04-09) is exactly the citalopram-onset boundary. A per-phase discrimination
   read therefore collapses to a "pre-citalopram vs citalopram-era" contrast - the
   very medication era-split that R14 retired in favour of **single-pool primacy**,
   and that R20 has already characterised on the driver side. Splitting it back out
   under the name "recovery phase" would resurrect a verdict the project
   deliberately demoted to a descriptive overlay.
3. **So per-phase discrimination adds nothing independent.** The single-pool
   verdicts (R14) are the discrimination read; the medication contrast is R20's.
   The lived-phase axis gives an honest **level and frequency backdrop** (sections
   1-2), not a second, thinner set of discrimination verdicts.

This is the register's own instruction made concrete: "the lines life drew are a
backdrop to read against, not a new set of verdicts."

---

## 5. Caveats per CONVENTIONS section 4.1 + section 4.2

- **Descriptive Layer-1, no causal marks.** Per-phase levels and counts only; no
  attribution of any phase difference to any cause (that is R20 for medication, R30
  for slow confounders).
- **Phase-to-phase differences are variation, not error and not verdicts.** The
  spread across phases is the lived trajectory's shape; wide within-phase p25/p75
  bands and tiny crash counts in phases 3/4a mean most cells are honest-limit.
- **Boundaries are lived-experience (M1), never data-tuned** per
  `lc_recovery_phase_axis.md`. A quiet phase is not a refutation.
- **Presence-conditioned coverage**: per-channel `n` is non-null channel-days, which
  differ slightly from phase day-totals through missingness (for example
  `stress_stdev_sleep` covers 500 of 509 phase-4b days).
- **The phase-5 stress shapes are partly medication** (CONFIRMED citalopram
  down-driver) and the resting-HR rise is partly slow drift; both are flagged to
  their owning analyses rather than read as lived-phase signal here.
- **n=1 throughout; single-pool primacy.** Any phase difference is a number with
  wide error, never a verdict.

---

## 6. Verification log

- **Surface**: Stratum 4 single pool, 2022-09-03 to 2026-06-05, n_days=1372,
  n_crash_episodes=29. Axis = `recovery_phase` column
  (`lc_recovery_phase_axis.md` section 2).
- **Per-phase day counts**: 3 -> 19, 4a -> 56, 4b -> 509, 5 -> 788 (sum 1372).
- **Per-phase crash counts**: 3 -> 2, 4a -> 1, 4b -> 15, 5 -> 11 (sum 29).
- **Level statistic**: median + p25/p75 of the non-null channel per phase
  (robust central tendency, CONVENTIONS section 3.1); HA01b reported as fraction of
  days at heavy / very_heavy `exertion_class_lagged`.
- **Discrimination-computable flag**: n_crashes >= 10 (the `evaluate_ha` bar); true
  for 4b, 5 only.
- **Operand-source path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`
  + `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv`.
- **Machine-readable**: `summary.json` (gitignored per the `docs/research/**/*.json`
  rule).

---

## 7. Cross-references

- **Axis**: [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md)
  section 2 (the five/six lived phases + boundaries).
- **Discrimination verdicts (the single-pool read this backdrop points to)**:
  [`analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../operationalisation_support/single_pool_reanchor/findings.md)
  (R14).
- **Medication attribution for the phase-5 stress shapes**:
  [`analyses/descriptive/operationalisation_support/driver_netting_overlay/findings.md`](../operationalisation_support/driver_netting_overlay/findings.md)
  (R20) + `methodology/citalopram_phase_stratification.md`.
- **Slow-confounder attribution for the resting-HR rise (R30, downstream)**:
  [`analyses/longrun_rhr_trend/findings.md`](../../longrun_rhr_trend/findings.md).
- **Site register R19** (this deliverable); R14 / R20 / R28 / R30. External repo
  `wiggers_research_story`, `docs/research-requests.md`.

---

*End of findings.*
