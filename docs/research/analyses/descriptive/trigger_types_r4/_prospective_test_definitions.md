# Prospective test definitions (option-preserving freeze) -- R4 trigger / phenotype

**Status**: producer-mode **DEFINITIONS FREEZE**, underscore-prefix planning
artefact. This is **NOT a locked pre-registration** and confers no verdict. Its
only job is to **timestamp the intended definitions** of two future tests, designed
from the exploratory work on the current 29 crashes, so that a later confirmatory
run on crashes occurring **after this date** can demonstrably claim its definitions
were not tuned to that future data. The full discipline (methodology MD ->
fresh-session pre-registration -> independent review -> lock) still applies before
any test is run. Frozen 2026-07-06 by Claude (Opus 4.8), producer-mode, for the
participant-researcher (repo owner).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

## Why this exists (the prospective logic)

The R4 exploratory work already **saw** the retrospective relationships in these 29
crashes (the emotional-load concordance, the crash-specificity, the phenotype
tendency). Under no-outcome-peek + single-pool primacy, those relationships
**cannot be re-tested on the same data** -- that would be circular. The legitimate
pattern is: **design the test from the exploration, confirm it on data not yet
seen.** Two non-circular confirmation routes exist: (1) **prospective** -- evaluate
on crashes after a lock date; (2) **external validator** -- predict an outcome not
used to define the exposure. Both require the definitions to predate the evaluation
data. This document freezes those definitions cheaply, without committing the full
multi-session pre-reg pipeline now (the tests are low-power and their payoff is
years out, since crashes now accrue slowly). If the prospective program is never
pursued, this file is a harmless record of intent.

## Test A -- emotional-trigger test (prospective)

- **Claim (prior-given, so confirmatory, CONVENTIONS section 4.3)**: emotional load
  in the pre-onset run-up raises the probability of a crash relative to a matched
  baseline. The direction is Wiggers' (emotional stress triggers PEM), not our peek.
- **Exposure (locked intent)**: peak `emo_load` (the 1-3 manual-triage intensity)
  in the pre-onset run-up `[start-5 .. start-1]`, as an **ordinal dose-response**
  (0/1/2/3), not a post-hoc-picked binary threshold.
- **Outcome**: a new crash within a locked forward window (primary 4 days;
  3/4/5 sensitivity), from `is_crash` / `crash_episode_id`.
- **Constructed matched baseline**: equal-magnitude emotional-load days OUTSIDE any
  crash run-up, matched on LC-era / recovery-phase epoch and a comparable
  felt-state trajectory (mirrors the push-crash matched-baseline construction).
- **Era handling**: prospective evaluation is within the current medication era, so
  the retrospective era-confound (the signal concentrated in `citalopram_modulated`)
  is dissolved by construction.
- **Null / inference**: event-level block-permutation, direction + magnitude + CI,
  "cannot resolve" the pre-committed default for a null-spanning CI. Underpowered at
  small n is expected and disclosed.
- **Scope**: physical / emotional / cognitive load are self-reported; a crash with
  no logged load is out-of-support, not counter-evidence.

## Test B -- crash-phenotype validation (prospective OR external validator)

- **Phenotype definition (the convergence rule, locked intent)**: a crash is
  labelled only when all THREE independently-measured axes agree:
  1. **trigger** -- dominant pre-onset load type (`emo_load` vs `phy_load` max over
     `[start-5 .. start-1]`, tie / sub-threshold -> none);
  2. **fingerprint** -- acute-window `[nadir-1 .. +1]` autonomic loudness =
     `mean(stress_mean_sleep_z, all_day_stress_avg_z, resting_hr_z) - bb_lowest_z`,
     split at the pooled-crash median (quiet vs loud);
  3. **content** -- de-identified note-tag lean, interpersonal / cognitive
     (`belasting_gezin + sociaal + emotioneel + symptoom_cognitief`) vs
     physical-illness (`sub_keel_resp + sub_koorts + sub_spier + triggers_extern`)
     over `[nadir-2 .. +2]`.
  -> **convergent-quiet (emotional)** = emo trigger AND quiet AND interpersonal;
  **convergent-loud (physical/illness)** = phy trigger AND loud AND physical-illness;
  everything else = **unclear** (expected to be the majority, a first-class label).
- **Why it cannot be tested on current data**: the rule was found here and its axes
  are correlated by selection, so the same-data bucket counts are description, not a
  p-value.
- **Confirmation route 1 (prospective)**: freeze this definition; classify crashes
  after the lock date; the phenotype either recurs at a stable rate or dissolves.
- **Confirmation route 2 (external validator)**: predict an outcome NOT used to
  define the phenotype -- e.g. recovery-trajectory shape, recurrence spacing, or
  differential response to a pacing vs emotion-regulation strategy.
- **Not for Test A**: the fingerprint is outcome-adjacent to a trigger claim, so it
  must NOT enter Test A's exposure definition.

## What is deliberately NOT locked here (deferred to the full pre-reg)

Threshold sensitivities, the exact permutation block length, power / precision
statements, the final matched-baseline calipers, and the multiplicity plan are all
**deferred to the real methodology MD + fresh-session pre-registration**, which is
required before either test is run. This freeze fixes only the load-bearing
definitions (exposure, outcome, phenotype axes) whose timestamp the prospective
validity depends on.

## Cross-references

- Exploratory basis: [`crash_phenotypes_exploratory.md`](crash_phenotypes_exploratory.md),
  [`analysis.md`](analysis.md), [`precondition.md`](precondition.md).
- Queued tests: [`../../../methodology/queued_work.md`](../../../methodology/queued_work.md)
  Q26 (phenotype-validation), Q21 (R4); household-illness logging Q27.
- Method precedents: the push-crash matched-baseline + event-level null
  ([`../../hypotheses/post-crash-exertion-relapse/hypothesis.md`](../../hypotheses/post-crash-exertion-relapse/hypothesis.md)).
- CONVENTIONS section 1 (producer vs reviewer), 3.5 (no-outcome-peek), 4.3
  (prior-driven = confirmatory).
