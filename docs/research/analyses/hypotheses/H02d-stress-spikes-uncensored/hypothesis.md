# H02d — Stress spikes with uncensored sentinels and wider lead-up

**Pre-registration written 2026-06-06, before any data was inspected for
this test.** Locked. Any subsequent change creates an H02e.

H02d is **not** a re-cut of H02b. H02b stays as-locked (already run,
train-supported / validate near-miss). H02d is a new test on the same
underlying data that addresses two operationalisation gaps surfaced
2026-06-06 (see registry §4 entry for H02d). If H02b refutes but H02d
supports, the spike framing was correct; censoring and window were
the bug.

## 1. Claim

In the **4 days** before a `crash_v1` episode, at least one day contains
a **longer-than-baseline sustained intense stress spike**, measured at
per-minute resolution from the raw monitoring_b FIT samples, **with
"too active" sentinel runs treated as ≥ 75 by imputation** for spike
continuity and duration. The lead-up's max-spike-duration is
*discriminative* against randomly-sampled non-crash 4-day windows.

The two changes from H02b:
- **Sentinel handling.** Garmin emits stress = -1 / -2 in two physically
  different cases: watch off-wrist (no signal) and watch on-wrist
  during high-arousal moments (HRV-stress algorithm refuses to
  compute). H02b dropped both. H02d distinguishes them by HR-sample
  presence and treats the "too active" subset as ≥ 75 stress.
- **Lead-up window.** H02b used 3 days, inherited from H02 for
  comparability. The post-H02b lag profile
  ([../../activity-labels/output/lag_profile_report.md](../../activity-labels/output/lag_profile_report.md))
  showed this user's empirical lag peaks at 5 days (+23.0 pp validate
  disc for HA01 at 5d vs +11.5 pp at 3d). H02d uses **4 days as
  primary** (matching HA01b's pre-registered window — the disciplined
  choice that already passed for HA01b, not the post-hoc 5d peak) and
  **5 days as a pre-committed secondary** evaluated alongside.

## 2. Why we think this

- **H02b train-supported / validate near-miss** ([../H02b-stress-spikes/](../H02b-stress-spikes/))
  suggests the spike metric is in the right family. The validate
  near-miss could reflect (a) the metric being too noisy for the
  cliff-era residual crashes, (b) censoring removing the most severe
  events, or (c) the 3-day window missing precursor activity at D−4
  or D−5. H02d addresses (b) and (c) simultaneously.
- **The censoring direction is wrong for H02b's purpose.** "Too active"
  sentinels are *exactly* the censored extreme-arousal moments H02b is
  designed to catch. A 30-minute panic episode that crosses into
  "too active" mid-spike either gets split or erased by the H02b
  filter (`val < 1 or val > 100`), depending on the sentinel block's
  duration vs. the 3-minute gap rule. Bias is consistently *against*
  the signal.
- **Calibration ([calibrate_sentinel_hr_result.md](../H02b-stress-spikes/calibrate_sentinel_hr_result.md)),
  8 stratified monitoring_b files**:
  - 220 sentinel samples observed (187 with value −2, 33 with value −1)
  - **100% of sentinels have an HR sample within ±60 s** (92.7% within
    ±30 s) — sentinels happen when the watch is actively recording HR.
  - Sentinels have *better* HR coverage than valid stress samples
    (96.2% within ±60 s for valid). Consistent with "too active" being
    the dominant sentinel cause and "watch off-wrist" being rare.
  - HR cadence ≈ 60 s median.
- **The lag profile is settled**. HA01b found +17.3 pp validate disc
  at 4 days, with +23.0 pp at 5 days (the latter post-hoc). 4 days is
  pre-registered and validated; 5 days is the empirical peak. Testing
  both gives us a cross-modality replication check (is the activity
  signal's lag also the stress signal's lag?).

## 3. Data sources

- **Crash labels**: `crash_v1` per registry §2 (unchanged from
  H01–H05, H02b).
- **Per-minute stress**: `stress_level` messages from each
  `monitoring_b` FIT file, decoded with `fitdecode`. Fields:
  `stress_level_time`, `stress_level_value` (typed int, range
  observed: −2, −1, 1–100; values 0 and > 100 also dropped for
  forward compatibility). Multiple files per day merged on timestamp,
  deduped (keeping max value on rare collisions).
- **Per-minute HR**: `heart_rate` field in `monitoring` messages,
  with timestamp resolved from `monitoring_info.timestamp` plus
  rolling `timestamp_16` (lower 16 bits of FIT-epoch seconds, with
  rollover handling and rolling-reference update on each resolve;
  validated against probe at [probe_monitoring_frame.py](../H02b-stress-spikes/probe_monitoring_frame.py)).
- **Daily aggregator** (`stressTooActiveCount`): reported as a
  diagnostic in `result.md` only. Not used in falsification.
- **Activity sessions** (separate FIT files, already parsed for
  [../../activity-labels/](../../activity-labels/)): reported as a
  diagnostic in `result.md` (what fraction of "too active" minutes
  overlap a recorded session). Not used in falsification.
- **Analysis window**: 2022-09-03 → 2026-06-05.
- **Train / validate split**: train 2022-09-03 → 2023-12-31 (14
  episodes); validate 2024-01-01 → 2026-06-05 (15 episodes). Same as
  H01–H04 and H02b.

## 4. Measurement protocol

### 4.1 Per-sample classification

For each stress sample at timestamp `t`:

1. If `stress_level_value` ∈ [1, 100]: **valid**, value as recorded.
2. Else (value ∈ {−2, −1, 0, > 100}): **sentinel**. Look for any
   HR sample within `±60 s` of `t`:
   - HR sample exists in window → label `too_active`. For spike logic,
     treat as if `stress_level_value = 75` (the threshold; lowest value
     that still qualifies for spike membership).
   - No HR sample in window → label `off_wrist`. Sample is skipped:
     does not contribute to spike duration, does not terminate a
     spike, does not extend the gap rule (treated as if the sample
     never existed).

`±60 s` is locked from the calibration: 100% of sentinels in the
8-file stratified sample have HR within this window; 30 s would lose
≈ 7% to false off-wrist classification; > 60 s gains nothing.

### 4.2 Daily max-spike-duration

For each calendar date with monitoring_b data:

1. Collect classified samples per §4.1, sorted by timestamp,
   deduped on timestamp (keeping max value on collisions; sentinels
   keep the most-restrictive label, i.e. `too_active` > `off_wrist`).
2. Walk the timeline. A "spike" is a contiguous run of samples where:
   - all members have either `value ≥ 75` (valid) or `label = too_active`
     (imputed ≥ 75), AND
   - gaps between consecutive members are ≤ 3 minutes (`off_wrist`
     samples in between are skipped — they neither break the spike
     nor count toward the gap rule), AND
   - total duration (last member's timestamp − first member's
     timestamp) is ≥ 5 minutes.
3. Day's `max_spike_minutes` = duration of the longest qualifying
   spike, or 0 if none.
4. Days with fewer than 60 *valid-or-too_active* samples are flagged
   `low-coverage` and excluded from baseline computation.

### 4.3 Sensitivity arm (bridge-only)

Run the same protocol with one change: `too_active` sentinels count
toward **continuity** (still bridge gaps as in §4.2) but do **not**
count toward **duration** (a spike's duration is measured only over
its valid-≥75 members). This is the conservative arm. Reported
alongside the primary; **the primary verdict governs**. Sensitivity
arm result is informative for honest accounting: if primary supports
but sensitivity refutes, sentinel imputation is doing the work and we
say so.

### 4.4 Per-episode profile

For each crash episode dated `D`:

1. **Primary lead-up window** = `[D − 4, D − 1]` (4 days).
   **Secondary lead-up window** = `[D − 5, D − 1]` (5 days).
2. **Primary baseline window** = `[D − 94, D − 5]` (90 days ending
   4 days before the episode).
   **Secondary baseline window** = `[D − 95, D − 6]`.
3. **Lead-up max-spike** = max of `max_spike_minutes` across the
   lead-up days (per window).
4. **Baseline mean max-spike** = trimmed mean (10/90) of
   `max_spike_minutes` across valid days in the baseline window
   (per window).
5. **`delta_spike`** = lead-up max-spike − baseline mean max-spike
   (per window).

### 4.5 Null sample

200 randomly-selected non-overlapping windows from the analysis
window, each disjoint from any crash episode's lead-up. Same seed
`20260605` as H02 / H02b. One null sample for the 4-day window and
one for the 5-day window (different by length; same draw process).

## 5. Pre-registered falsification criterion

Identical to H02b's bar — direct comparability with the H02b verdict
is the whole point. Evaluated **independently** for the primary
(4-day) and secondary (5-day) windows. The **primary window
determines the overall verdict.** The secondary window is reported
alongside and informs follow-up choices but does not change the
verdict.

Within each window, the hypothesis is **supported** if and only if
**all three** hold in **both** the train window and the validate
window independently:

a. **Frequency**: at least **60%** of crash episodes have
   `delta_spike ≥ 10 minutes`.

b. **Discrimination**: the crash-episode frequency from (a) is at
   least **15 percentage points higher** than the null-sample
   frequency of windows with `delta_spike ≥ 10 minutes`.

c. **Magnitude**: the median `delta_spike` across crash episodes is
   at least **+5 minutes**, and the lower quartile is at least **0
   minutes**.

Any one of (a), (b), (c) failing in either train or validate of the
primary (4-day) window → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions → **inconclusive**.

The sensitivity arm (§4.3) and the secondary 5-day window are
reported with the same a/b/c numbers but do not move the verdict
label. They inform what we do next.

## 6. Exclusion rules

- **Episode requires ≥ 3 valid stress days out of 4** in the primary
  lead-up (and ≥ 4 out of 5 in the secondary). Slightly less strict
  than H02b's "2 of 3" because the windows are wider.
- **Episode requires ≥ 30 valid days out of 90** in baseline (each
  window separately, since the baselines are shifted).
- **Days with fewer than 60 valid-or-too_active stress samples** are
  excluded from both baseline and lead-up.
- **Episodes whose lead-up overlaps another crash episode's days**
  excluded from primary, reported separately.

## 7. Expected effect size if hypothesis is true

Rough sanity-checks for `result.md`:

- 70–85% of crash episodes have `delta_spike ≥ 10 min` (slightly
  above H02b's 70–80% expectation, because we now catch the censored
  events).
- Null sample rate: 25–40% (random 4-day window naturally includes
  more candidate stressful days than a 3-day window; the wider
  window inflates both crash and null rates).
- Median `delta_spike`: 10–25 minutes.
- If crash rate ≥ 95% and null rate ≥ 90% → metric is over-inflated
  by the wider window; flag.

## 8. Caveats `result.md` must explicitly acknowledge

- **Garmin's stress algorithm is opaque** and changes between firmware
  versions (FR245 7.x → 10.4 across the window). H02b's same caveat.
- **Sentinel codes (-1 vs -2) not semantically distinguished.** We
  classify by HR-presence, not by code value. Possible that the two
  codes carry different physiological meaning we haven't decoded.
- **±60 s tolerance is locked from an 8-file calibration**, not from
  the full 1.733-day dataset. If full-dataset HR cadence is materially
  different in some sub-window (e.g. firmware change altered HR
  sampling), the tolerance may be under- or over-fitted there. Sample
  was stratified across the timeline to minimise this risk.
- **Wider lead-up window inflates both crash and null discrimination
  numerators.** The +15 pp criterion was set for H02b's 3-day window;
  by holding it identical at 4 days and 5 days we make H02d *harder
  to pass* on discrimination (the null naturally rises more than the
  crash signal does). This is intentional — we'd rather under-claim
  than over-claim.
- **Activity-overlap not in the verdict.** If "too active" sentinels
  largely overlap formally-recorded workouts, the hypothesis is
  testing "workout intensity" rather than the user's experiential
  "intense moment in an otherwise calm day." Reported as a
  diagnostic, not gating.
- **`crash_v1` mixes mechanisms.** Same caveat as H02b. Some episodes
  may show big deltas, others zero. Per-episode breakdown in
  `result.md`.
- **Multi-comparison.** H02d is the 7th pre-registered hypothesis in
  this batch (H01–H05, H02b, H02d), plus the HA01–HA05 / HA01b–HA05b
  activity-labels family. The held-out validate window is the
  primary defence; we note this in `result.md`.
- **Same-day overlap with HA01b.** HA01b found activity-shock at
  4 days. If H02d supports at 4 days, the two precursors may be the
  same physical event (heavy activity day) seen through two channels.
  Cross-reference: for each crash episode supported by both, report
  whether the H02d spike day is also the HA01b shock day.

## 9. What we do with each outcome

- **Supported in both windows** (primary 4d, both train + validate) →
  **first pre-registered SUPPORTED stress precursor of the project**
  (validate-era). Compare against H02b's verdict to decide what
  *fraction* of the gain came from the sentinel fix vs. the wider
  window. Then `card.md`: forensic-companion card pointing at "around
  [date] there was an X-minute spike on day Y. What was happening?"
- **Refuted in both windows** → the spike framing genuinely doesn't
  capture the validate-era residual crashes, even with censoring
  fixed and window widened. Closes the "stress-spike" branch of the
  investigation. Strong evidence that residual 2025+ crashes are
  *not* sympathetic-spike-precipitated.
- **Primary refuted, secondary (5d) supported** → the 5d lag matters
  more than we said. Document as suggestive (post-hoc-flavoured) and
  pre-register an H02e specifically at 5d on the next batch with
  fresh data discipline.
- **Train-supported, validate refuted** (same shape as H02b's
  current verdict) → the recovery cliff genuinely changed the
  precursor structure for spike-driven crashes. Combined with H02b,
  strong evidence the pre-cliff stress-precursor pattern is real and
  no longer applies.
- **Primary supports but sensitivity arm refutes** → sentinel
  imputation is carrying the verdict. Honest accounting: report as
  "supported under imputation"; consider H02e with a more
  conservative imputation rule (e.g. require activity-session
  overlap for imputation).
- **Inconclusive** → unlikely given coverage, but if HR-timestamp
  resolution or FIT-parse issues bring usable episodes below 10/window,
  debug and re-run.

---

*Pre-registration locked 2026-06-06. Next: implement `extract_daily_max_spike_v2.py`
(adds sentinel classification + HR-cross-reference) and `test.py`
(parallel evaluation at 4d primary / 5d secondary, sensitivity arm
running alongside primary).*
