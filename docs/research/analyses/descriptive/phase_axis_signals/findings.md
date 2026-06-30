# Findings -- R19 phase-axis signal shapes (scorecard backdrop)

**Strand A operationalisation-support analysis** -- re-aggregates the SAME single-pool re-anchor operands ([`operationalisation_support/single_pool_reanchor/`](../operationalisation_support/single_pool_reanchor/findings.md)) along the **lived recovery-phase axis** ([`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md)). Produces, per scorecard signal, its **descriptive shape across the five lived phases** (ids 1, 2, 3, 4a, 4b, 5). This is the scorecard site's NEW backdrop that **replaces "early vs late"**.

**Surface**: full Stratum-4 single pool, 2022-09-03 to 2026-06-05 (n_days=1372; n_crash_episodes=29). Crash episodes assigned to a phase by the `recovery_phase` of their `episode_start` (verified identical to the helper `lc_recovery_phase()` for all in-frame crashes). Per-phase discrimination = (per-phase crash trigger-fraction minus **whole-pool** null trigger-fraction) x 100, in pp. Stationary-bootstrap 95% CI on the per-phase discrimination at E[L]=7, B=10,000, seed `20260624`. Whole-pool null window set inherited from the single-pool re-anchor (legacy seed `20260605`).

**Discipline binding (R19)**: Layer 1 descriptive per [CONVENTIONS Sec 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). This is a **described shape with WIDE error**, explicitly **NOT a per-phase verdict**, NOT a split, NOT a causal claim. Phase boundaries are **lived-experience M1** ([`lc_recovery_phase_axis.md sec 3`](../../../methodology/lc_recovery_phase_axis.md)), **never data-tuned**; a quiet phase is **NOT a refutation** ([CONVENTIONS sec 4.2](../../../CONVENTIONS.md#42-caveats-vs-a-priori)). The 29 crashes spread across ~6 phases -> **most cells are honest-limit** (n too small for any inferential read). Every low-n cell is flagged. The band shown is **phase-to-phase variation, not error.**

---

## 1. Headline (descriptive only)

The 29 single-pool crash episodes are NOT evenly spread across the lived axis. By construction the single pool starts 2022-09-03, so **phases 1 + 2 carry zero crashes** and **phase 3 (`lc_pre_ergo`) holds only its post-2022-09-03 tail (2 crashes)**. The mass of crashes sits in the two long pre-/post-citalopram phases: **4b `pacing_habit_established` (15 crashes)** and **5 `citalopram_modulated` (11 crashes)**, with **4a `pacing_pre_citalopram_learning` holding 1**.

Consequently, of the **7 signals x 6 phases = 42 cells**, only **14 are populated at all** and only **13 carry a computed discrimination + CI**; of those 13, **just 9 clear the n>=10 honest-limit bar** (the 4b and 5 cells on six signals, minus HA11 phase-5 which drops to n=9 after operand-missingness). **30 of 42 cells are honest-limit** (n=0 by construction, n too small, or operand not computable in the early pool). See section 4.

**Phase-shape readings (descriptive, wide-error, NOT verdicts):** the only two phases with a readable shape on most signals are 4b and 5. Across the readable cells, the signals whose phase-4b -> phase-5 shape is most **non-flat** descriptively are **H02b** (max-stress-spike): +13.5 pp in 4b vs **-10.1 pp** in 5 (a sign change), and **HA11** (within-day U-dip count): +25.1 pp in 4b vs +2.9 pp in 5 (a large narrowing). **HA07c**, **HA07d** and **HA10** instead read **higher in phase 5 than 4b** (HA07c +7.9 -> +14.4 pp; HA07d +17.5 -> +22.7 pp; HA10 +0.5 -> +9.0 pp). **HA06b** and **HA01b** are nearly flat across 4b/5. **All of these "shapes" sit inside CIs that overlap zero and overlap each other** -- they are described shapes, not differences. See the honest-limit note in section 5 before reading any of them as real.

---

## 2. Per-signal x per-phase table

One block per scorecard signal. Columns: phase id + name, `disc_pp` (per-phase crash-frac minus whole-pool null-frac, in pp), 95% CI on disc_pp (stationary bootstrap, E[L]=7), `n_crashes` (episodes assigned to phase), `n_clean` (episodes with computable operand -- the section 3.6 count-triple is `{n_crashes_in_phase, n_clean, n_null_pool}`), and the honest-limit flag.

Whole-pool null fraction (the common backdrop each phase is read against) is stated per signal. `n_null_pool` is the whole-Stratum-4 null window count for that signal's leadup length.

> **Reading rule**: `--` means **not computable** (no crashes in phase, or the operand's lagged baseline / leadup needs prior days that do not exist that early in the pool). It is **NOT a zero and NOT a refutation.**

### H02b -- max(max_spike_minutes - baseline) over 3d leadup >= +10 min
null frac = 0.465; n_null_pool = 200; single-pool disc = +3.5 pp (n_clean=26)

| id | phase | disc_pp | CI95 | n_crashes | n_clean | honest-limit |
|---|---|---:|---|---:|---:|:--|
| 1 | pre_illness_healthy | -- | -- | 0 | 0 | YES (no crashes; pre-pool) |
| 2 | acute_infection | -- | -- | 0 | 0 | YES (no crashes; pre-pool) |
| 3 | lc_pre_ergo | -- | -- | 2 | 0 | YES (operand not computable in early pool) |
| 4a | pacing_pre_citalopram_learning | -- | -- | 1 | 0 | YES (operand not computable) |
| 4b | pacing_habit_established | +13.5 | [-27.0, +28.3] | 15 | 15 | no (n>=10; CI spans 0) |
| 5 | citalopram_modulated | -10.1 | [-30.8, +32.2] | 11 | 11 | no (n>=10; CI spans 0) |

### HA06b -- max abs-z (4d) of resting_hr; lagged baseline; sigma_floor=0.5 bpm
null frac = 0.549; n_null_pool = 195; single-pool disc = +6.7 pp (n_clean=26)

| id | phase | disc_pp | CI95 | n_crashes | n_clean | honest-limit |
|---|---|---:|---|---:|---:|:--|
| 1 | pre_illness_healthy | -- | -- | 0 | 0 | YES |
| 2 | acute_infection | -- | -- | 0 | 0 | YES |
| 3 | lc_pre_ergo | -- | -- | 2 | 0 | YES (operand not computable) |
| 4a | pacing_pre_citalopram_learning | -- | -- | 1 | 0 | YES |
| 4b | pacing_habit_established | +5.1 | [-25.1, +24.1] | 15 | 15 | no (CI spans 0) |
| 5 | citalopram_modulated | +8.8 | [-28.1, +28.0] | 11 | 11 | no (CI spans 0) |

### HA07c -- max signed z (4d) of n/n delta of stress_mean_sleep; sigma_floor=2.0
null frac = 0.492; n_null_pool = 189; single-pool disc = +10.8 pp (n_clean=25)

| id | phase | disc_pp | CI95 | n_crashes | n_clean | honest-limit |
|---|---|---:|---|---:|---:|:--|
| 1 | pre_illness_healthy | -- | -- | 0 | 0 | YES |
| 2 | acute_infection | -- | -- | 0 | 0 | YES |
| 3 | lc_pre_ergo | -- | -- | 2 | 0 | YES (operand not computable) |
| 4a | pacing_pre_citalopram_learning | -- | -- | 1 | 0 | YES |
| 4b | pacing_habit_established | +7.9 | [-27.2, +26.5] | 15 | 14 | no (CI spans 0) |
| 5 | citalopram_modulated | +14.4 | [-30.4, +29.9] | 11 | 11 | no (CI spans 0) |

### HA07d -- max abs-z (4d) of n/n delta of stress_stdev_sleep; sigma_floor=0.5
null frac = 0.683; n_null_pool = 189; single-pool disc = +19.7 pp (n_clean=25)

| id | phase | disc_pp | CI95 | n_crashes | n_clean | honest-limit |
|---|---|---:|---|---:|---:|:--|
| 1 | pre_illness_healthy | -- | -- | 0 | 0 | YES |
| 2 | acute_infection | -- | -- | 0 | 0 | YES |
| 3 | lc_pre_ergo | -- | -- | 2 | 0 | YES (operand not computable) |
| 4a | pacing_pre_citalopram_learning | -- | -- | 1 | 0 | YES |
| 4b | pacing_habit_established | +17.5 | [-23.0, +22.5] | 15 | 14 | no (CI spans 0) |
| 5 | citalopram_modulated | +22.7 | [-26.5, +24.2] | 11 | 11 | no (CI spans 0) |

### HA10 -- max abs-z (4d) of bb_highest; lagged baseline; sigma_floor=2.0 BB
null frac = 0.729; n_null_pool = 199; single-pool disc = +4.1 pp (n_clean=26)

| id | phase | disc_pp | CI95 | n_crashes | n_clean | honest-limit |
|---|---|---:|---|---:|---:|:--|
| 1 | pre_illness_healthy | -- | -- | 0 | 0 | YES |
| 2 | acute_infection | -- | -- | 0 | 0 | YES |
| 3 | lc_pre_ergo | -- | -- | 2 | 0 | YES (operand not computable) |
| 4a | pacing_pre_citalopram_learning | -- | -- | 1 | 0 | YES |
| 4b | pacing_habit_established | +0.5 | [-21.0, +21.5] | 15 | 15 | no (CI spans 0) |
| 5 | citalopram_modulated | +9.0 | [-24.9, +24.6] | 11 | 11 | no (CI spans 0) |

### HA11 -- max signed z (4d) of u_dip_count; lagged baseline; sigma_floor=0.5 events
null frac = 0.415; n_null_pool = 171; single-pool disc = +16.8 pp (n_clean=24)

| id | phase | disc_pp | CI95 | n_crashes | n_clean | honest-limit |
|---|---|---:|---|---:|---:|:--|
| 1 | pre_illness_healthy | -- | -- | 0 | 0 | YES |
| 2 | acute_infection | -- | -- | 0 | 0 | YES |
| 3 | lc_pre_ergo | -- | -- | 2 | 0 | YES (operand not computable) |
| 4a | pacing_pre_citalopram_learning | -- | -- | 1 | 0 | YES |
| 4b | pacing_habit_established | +25.1 | [-27.0, +25.7] | 15 | 15 | no (CI spans 0) |
| 5 | citalopram_modulated | +2.9 | [-31.6, +28.1] | 11 | 9 | **YES (n_clean=9 < 10)** |

### HA01b -- frac windows with >=1 heavy/very_heavy exertion day in 4d leadup
null frac = 0.770; n_null_pool = 200; single-pool disc = +5.1 pp (n_clean=28)

| id | phase | disc_pp | CI95 | n_crashes | n_clean | honest-limit |
|---|---|---:|---|---:|---:|:--|
| 1 | pre_illness_healthy | -- | -- | 0 | 0 | YES |
| 2 | acute_infection | -- | -- | 0 | 0 | YES |
| 3 | lc_pre_ergo | +23.0 | [-80.0, +27.5] | 2 | 1 | **YES (n_clean=1; CI meaningless)** |
| 4a | pacing_pre_citalopram_learning | +23.0 | [-80.0, +27.5] | 1 | 1 | **YES (n_clean=1; CI meaningless)** |
| 4b | pacing_habit_established | +3.0 | [-20.7, +17.3] | 15 | 15 | no (CI spans 0) |
| 5 | citalopram_modulated | +4.8 | [-24.5, +21.0] | 11 | 11 | no (CI spans 0) |

> HA01b is the only signal where phases 3 + 4a are computable at all (it needs only an `exertion_class_lagged` label on a single leadup day, not a 90-day lagged baseline). At n_clean=1 the CI is a degenerate artefact ([-80, +27.5] is one episode against the whole null) -- **read it as "one episode, no error estimate possible", not as a phase signal.**

---

## 3. Proposed export shape (scorecard backdrop)

Per the deliverable spec: `{signal, phases:[{id, disc_pp_or_level, ci, n_crashes}], note}`. JSON-shaped export below (values rounded to 1 dp; `null` = not computable; `honest_limit` carried per phase so the scorecard can render small-n cells distinctly, e.g. greyed / "insufficient data" rather than a number):

```json
[
  {"signal": "H02b",  "null_frac": 0.465, "note": "non-flat 4b->5 (sign change, wide CI)",
   "phases": [
     {"id":"1","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"2","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"3","disc_pp":null,"ci":null,"n_crashes":2,"honest_limit":true},
     {"id":"4a","disc_pp":null,"ci":null,"n_crashes":1,"honest_limit":true},
     {"id":"4b","disc_pp":13.5,"ci":[-27.0,28.3],"n_crashes":15,"honest_limit":false},
     {"id":"5","disc_pp":-10.1,"ci":[-30.8,32.2],"n_crashes":11,"honest_limit":false}]},
  {"signal": "HA06b", "null_frac": 0.549, "note": "near-flat 4b/5",
   "phases": [
     {"id":"1","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"2","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"3","disc_pp":null,"ci":null,"n_crashes":2,"honest_limit":true},
     {"id":"4a","disc_pp":null,"ci":null,"n_crashes":1,"honest_limit":true},
     {"id":"4b","disc_pp":5.1,"ci":[-25.1,24.1],"n_crashes":15,"honest_limit":false},
     {"id":"5","disc_pp":8.8,"ci":[-28.1,28.0],"n_crashes":11,"honest_limit":false}]},
  {"signal": "HA07c", "null_frac": 0.492, "note": "rises 4b->5 (wide CI)",
   "phases": [
     {"id":"1","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"2","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"3","disc_pp":null,"ci":null,"n_crashes":2,"honest_limit":true},
     {"id":"4a","disc_pp":null,"ci":null,"n_crashes":1,"honest_limit":true},
     {"id":"4b","disc_pp":7.9,"ci":[-27.2,26.5],"n_crashes":15,"honest_limit":false},
     {"id":"5","disc_pp":14.4,"ci":[-30.4,29.9],"n_crashes":11,"honest_limit":false}]},
  {"signal": "HA07d", "null_frac": 0.683, "note": "rises 4b->5; highest single-pool signal (wide CI)",
   "phases": [
     {"id":"1","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"2","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"3","disc_pp":null,"ci":null,"n_crashes":2,"honest_limit":true},
     {"id":"4a","disc_pp":null,"ci":null,"n_crashes":1,"honest_limit":true},
     {"id":"4b","disc_pp":17.5,"ci":[-23.0,22.5],"n_crashes":15,"honest_limit":false},
     {"id":"5","disc_pp":22.7,"ci":[-26.5,24.2],"n_crashes":11,"honest_limit":false}]},
  {"signal": "HA10",  "null_frac": 0.729, "note": "near-flat 4b, rises 5 (wide CI)",
   "phases": [
     {"id":"1","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"2","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"3","disc_pp":null,"ci":null,"n_crashes":2,"honest_limit":true},
     {"id":"4a","disc_pp":null,"ci":null,"n_crashes":1,"honest_limit":true},
     {"id":"4b","disc_pp":0.5,"ci":[-21.0,21.5],"n_crashes":15,"honest_limit":false},
     {"id":"5","disc_pp":9.0,"ci":[-24.9,24.6],"n_crashes":11,"honest_limit":false}]},
  {"signal": "HA11",  "null_frac": 0.415, "note": "non-flat 4b->5 (large narrowing); phase-5 n_clean=9 honest-limit",
   "phases": [
     {"id":"1","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"2","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"3","disc_pp":null,"ci":null,"n_crashes":2,"honest_limit":true},
     {"id":"4a","disc_pp":null,"ci":null,"n_crashes":1,"honest_limit":true},
     {"id":"4b","disc_pp":25.1,"ci":[-27.0,25.7],"n_crashes":15,"honest_limit":false},
     {"id":"5","disc_pp":2.9,"ci":[-31.6,28.1],"n_crashes":11,"honest_limit":true}]},
  {"signal": "HA01b", "null_frac": 0.770, "note": "near-flat 4b/5; 3+4a are n=1 artefacts",
   "phases": [
     {"id":"1","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"2","disc_pp":null,"ci":null,"n_crashes":0,"honest_limit":true},
     {"id":"3","disc_pp":23.0,"ci":[-80.0,27.5],"n_crashes":2,"honest_limit":true},
     {"id":"4a","disc_pp":23.0,"ci":[-80.0,27.5],"n_crashes":1,"honest_limit":true},
     {"id":"4b","disc_pp":3.0,"ci":[-20.7,17.3],"n_crashes":15,"honest_limit":false},
     {"id":"5","disc_pp":4.8,"ci":[-24.5,21.0],"n_crashes":11,"honest_limit":false}]}
]
```

`disc_pp_or_level` here is `disc_pp` (per-phase crash trigger-fraction minus whole-pool null fraction). The scorecard SHOULD render `honest_limit:true` cells as "insufficient data in this phase", not as a number or a colour-coded effect.

---

## 4. The cell-readability ledger (section 3.6 count discipline)

Per the binding ask: **per-phase n_crashes reported for every cell, and every low-n cell flagged.**

| | phase 1 | phase 2 | phase 3 | phase 4a | phase 4b | phase 5 |
|---|---:|---:|---:|---:|---:|---:|
| **n_crashes (episodes)** | 0 | 0 | 2 | 1 | 15 | 11 |
| **readable cells (n_clean>=10)** | 0/7 | 0/7 | 0/7 | 0/7 | **7/7** | **6/7** |
| **honest-limit cells** | 7/7 | 7/7 | 7/7 | 7/7 | 0/7 | 1/7 (HA11) |

- Phases **1 + 2** carry **zero crashes by construction**: the single pool starts 2022-09-03 (Stratum-4 start), which is inside phase 3. These rows exist only to keep the axis complete; they are **not evidence of anything**.
- Phase **3 (`lc_pre_ergo`)** holds 2 crashes but they fall in the **first ~3 weeks of the pool**, before the 90-day lagged baseline window can fill, so all z-score / delta / slope signals are `--`. Only HA01b (label-only operand) computes, at n=1.
- Phase **4a** holds **1 crash** -- below any honest read for every signal; HA01b's single computable cell is a degenerate artefact.
- Phases **4b + 5** are the only phases with a readable shape, and even there **every CI spans 0**.

**Net: of 42 (signal x phase) cells, 13 carry a number; 9 are above the n>=10 honest-limit bar; 30 are honest-limit (n=0, n too small, or operand not computable).**

---

## 5. Prominent honest-limit note (binding)

> **This is a described shape with WIDE error, NOT a per-phase verdict.**
>
> 1. **Small-n is the dominant fact.** 29 crashes across 6 phases means most phase cells have too few crashes to estimate anything. Only phases **4b (15)** and **5 (11)** are readable; **4a (1)** and **3 (2, mostly uncomputable)** are not; **1 + 2 (0)** are empty by construction of the single pool. The scorecard MUST surface this, not paper over it.
> 2. **Every readable CI overlaps zero and the phases overlap each other.** No phase-to-phase difference here is statistically distinguishable. The disc_pp point estimates describe a *shape*; the bands are *phase-to-phase variation under small n*, not measurement error and not effect size.
> 3. **A quiet phase is NOT a refutation** ([CONVENTIONS sec 4.2](../../../CONVENTIONS.md#42-caveats-vs-a-priori)). Phase 4a reading `--` does not mean the signal is absent in pacing-learning; it means there was 1 crash and no statistical window. Phases 1-3 reading `--`/empty reflects the single-pool start date and baseline-fill requirement, nothing physiological.
> 4. **Boundaries are lived-experience M1, never data-tuned** ([`lc_recovery_phase_axis.md sec 3, sec 5.1 carve-out`](../../../methodology/lc_recovery_phase_axis.md)). They were NOT chosen to make any signal look better across phases. The 4a/4b boundary (2022-11-17) is an 8-week-post-ergotherapie habit-formation anchor, fixed before this aggregation.
> 5. **No verdict, no split, no causal claim.** This artefact does not promote, refute, or stratify any HA. The single-pool re-anchor verdicts ([`single_pool_reanchor/findings.md`](../operationalisation_support/single_pool_reanchor/findings.md)) are unchanged; this is a descriptive overlay on the SAME operands.
> 6. **Long-memory caveat inherited.** Per [`lc_recovery_phase_axis.md sec 5.4 + sec 6.6`](../../../methodology/lc_recovery_phase_axis.md), several scorecard channels fire the factor-of-2 E[L]* flag on long phases; the E[L]=7 block used here may under-cover the 4b + 5 CIs (which are already wide). Treat the bands as **lower bounds on uncertainty**, if anything.
> 7. **Non-flat shapes are descriptive curiosities, not findings.** H02b (sign change 4b->5), HA11 (large narrowing 4b->5), and the HA07c/HA07d/HA10 rise into phase 5 are *visible* in the point estimates but *not distinguishable* given the CIs. Citalopram-confirmed channels (HA07c/HA07d on stress, plus stress-derived signals) carry the additional [`citalopram_phase_stratification sec 5`](../../../methodology/citalopram_phase_stratification.md) confounder note for phase 5 -- the phase-5 rise is NOT attributable to recovery-phase vs medication without a section 5.A/5.B treatment, which this descriptive backdrop does not apply.

---

## 6. Privacy statement

This artefact is **publication-safe by construction**: it reports only **aggregated discrimination statistics, bootstrap CIs, and episode counts per phase**. No dated values, no per-day scores, no crash dates, no calendar-anchored individual observations are emitted. Phase boundaries are documented in the already-published [`lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) as lived-experience anchors (no dated data values). Per-phase n_crashes are small-integer counts, which the honest-limit framing already foregrounds. Run before any push through [`pipeline/audit_for_publication.py`](../../../pipeline/audit_for_publication.py) per project discipline.

---

## 7. Verification log

- **As-of-date**: 2026-06-05 (Stratum-4 right edge, inherited from the single-pool re-anchor).
- **Stratum-4 start**: 2022-09-03. **n_days in pool**: 1372. **n_crash_episodes**: 29.
- **Phase assignment**: by `episode_start` via `lc_recovery_phase()` ([`lc_recovery_phase_axis.md sec 2.1`](../../../methodology/lc_recovery_phase_axis.md)); cross-checked **identical** to `per_day_master.recovery_phase` for all in-frame crashes.
- **Per-phase crash counts**: 1:0 / 2:0 / 3:2 / 4a:1 / 4b:15 / 5:11 (sum=29).
- **Discrimination**: per-phase crash trigger-fraction minus **whole-pool** null trigger-fraction, x100 (pp). Null pool is the whole-Stratum-4 single-pool null set (NOT re-sampled per phase -- a per-phase null would collapse n catastrophically and is not the ask).
- **CI**: stationary bootstrap 95% on disc_pp, E[L]=7, B=10,000, seed `20260624`; inference helpers [`analyses/_utils/inference.py`](../../_utils/inference.py).
- **Null window seed**: `20260605` (inherited). **Leadups**: H02b 3d; all others 4d.
- **Operands**: re-used verbatim from [`single_pool_reanchor/run.py`](../operationalisation_support/single_pool_reanchor/run.py) (imported as a module; no operand re-implementation). Single-pool whole-pool disc per signal reproduced as a sanity row in each table header and matches the re-anchor findings (H02b +3.5, HA06b +6.7, HA07c +10.8, HA07d +19.7, HA10 +4.1, HA11 +16.8, HA01b +5.1).
- **Operand-source path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` + `processed/crash_labels/labels_crash_v2.csv` (resolved via the re-anchor's default-path fallback; env var empty at run time).
- **Phase-id territory note**: phase ids only are used here; the Q4.3 [`era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md) is the R27-territory backstop for phase-boundary convergence and is **not** consumed for any boundary decision in this artefact.

---

*Drafted by Claude (Opus 4.8) in producer-mode (R19) under user authorisation. Layer 1 descriptive backdrop for the scorecard site replacing "early vs late". No push / git / audit performed in this session. Locked result.md files untouched.*
