# Result: post-crash exertion relapse (the "danger window")

**Status**: producer-mode TEST EXECUTION result, layer-1 descriptive-plus-inference
per [CONVENTIONS](../../../CONVENTIONS.md). Reveals the outcome for the LOCKED
pre-registration
[`hypothesis.md`](hypothesis.md) (LOCKED 2026-07-04). This is the single place the
exposure-versus-relapse relationship is computed. Executed 2026-07-04 by Claude
(Opus 4.8) under producer-mode authorization, for the participant-researcher
(repo owner). Test code: [`test.py`](test.py).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress. "exertion" / "strain" = physical / cardiac load only.

> ## VERDICT (pre-reg section 10)
>
> **Cannot resolve.** The one primary statistic (the standardised
> danger-window-vs-matched-baseline relapse-rate difference at matched
> magnitude) is **-1.03** with an event-level block-permutation **95% CI of
> [-8.58, +5.21]**, which spans the null (0). Per the pre-registered section 10,
> a CI that spans the null is read as **"Cannot resolve"** - the pre-committed
> default reading. It is **not** upgraded to "suggestive" or "consistent with."
> The point estimate is if anything slightly negative (danger-window peaks
> relapsed at a marginally LOWER rate than their matched baseline: mean delta =
> **-0.116**), so there is no evidence in the predicted positive direction. The
> descriptive statement is: **danger-window peak cardiac strain did NOT predict
> relapse above the matched baseline in this subject's 24 usable crash windows.**
> No causal mark: this is not "the spike caused / prevented the relapse."

---

## 1. What was tested (faithful to the locked pre-reg)

The single primary test (pre-reg sections 1, 4b, 4d, 5, 6, 8): peak masked
`max_hr_rank_lagged_lcera` x crash arm x 10-day danger window x 4-day relapse
window x matched-baseline contrast. Everything else (the activity-volume
comparison arm, the cumulative-strain secondary, the dip arm, and every
sensitivity band) is secondary / comparison / sensitivity and is NOT promoted to
primary regardless of its result (peak-primacy is irrevocable).

RNG seed (recorded, and set in a `test.py` code comment): **20260704**. Only the
event-level block-permutation null consumes the RNG; the all-eligible-in-caliper
matched-baseline construction has no random draw, so the point estimates,
matched pools, and all sensitivities are seed-independent. Re-running `test.py`
reproduces every number here bit-for-bit (verified across three runs).

## 2. Reproduction check (pre-reg section 4e-2)

The masked PRIMARY exposure is the same lagged-rank algorithm as the as-built
`_lcera` extractor (`analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py`,
`compute_lagged_rank`, `LCERA_START = date(2022, 4, 4)`, window `[d-90, d-30]`,
`MIN_LAGGED_DAYS = 40`, midrank-for-ties), MINUS the crash/dip masking. To prove
this, `test.py` first recomputes the UN-masked rank from the raw `max_hr` column
and compares it to the stored `max_hr_rank_lagged_lcera`:

- Raw source used: the **`max_hr` column in `per_day_master.csv`** (no fallback
  join to `activity_features_daily.csv` was needed).
- n compared: **1432 days**. Correlation **1.000000**. Max abs diff **0.000500**;
  mean abs diff **0.000225**.

The residual max abs diff of 0.0005 is exactly the rounding of the stored column
to 3 decimals. The reproduction is essentially perfect, which proves the masked
recompute is the identical algorithm minus the masking (the only difference is
the pool exclusion of `is_crash` / `is_dip` days).

## 3. Events and coverage (pre-reg sections 3, 4a, 4e)

| Quantity | Value |
|---|---|
| Crash episodes (`crash_episode_id` with >= 1 `is_crash` day) | 29 |
| Crash episodes with a felt-recovery day (`gevoelscore >= 4` in t+1..t+10) | **28 / 29** (crash-014, nadir 2023-11-29, excluded: no felt-recovery day) |
| Dip days (`is_dip`) | 79 |
| Dip days with a felt-recovery day | **79 / 79** |
| **Usable crash events entering the PRIMARY statistic** | **24** |
| Usable dip events (mechanism-control arm) | 76 |

The 28/29 and 79/79 felt-recovery coverage matches the precondition (section 3)
exactly. The reduction from 28 usable crash windows (the pre-reg's anticipated n)
to **24** in the masked primary is a faithful, disclosed consequence of the
locked masking (see Implementation notes, item A). The un-masked sensitivity
retains 26 events.

## 4. The primary result (pre-reg section 6)

- **The one primary statistic** (standardised mean of `delta_i`, where
  `delta_i = (danger-window relapse 0/1) - (mean relapse rate of that peak's
  matched-baseline pool)`): **-1.0287**.
- **Event-level block-permutation 95% CI**: **[-8.5780, +5.2134]**.
- **p-analogue** (upper tail, in the predicted positive direction):
  **0.6608** (observed statistic at the 33.9th percentile of the null).
- **Direction + magnitude**: mean `delta` = **-0.1156**. The danger-window peaks
  relapsed at rate **8 / 24 = 0.333**; their matched-baseline pools relapsed at a
  (pool-size-weighted-per-event) mean rate near **0.45**. So the danger-window
  peaks relapsed slightly LESS than matched baseline, the opposite of the
  predicted positive direction, and well within the null.

Direction + magnitude are reported alongside the p-analogue, never the p alone
(pre-reg section 6). The CI is very wide (spanning roughly -8.6 to +5.2 in
standardised units) because a standardised (t-type) mean over 24 events under a
block-permutation null has heavy tails; this width is the honest reflection of
the design's power at 24 units, not a numerical artefact (the null was
well-behaved: all 10,000 replicates valid, centred near 0, median -0.09).

### 4b. Rank-slope reading (pre-reg section 4c, 6)

The pre-reg calls the primary "equivalently the relapse-rate-monotone-in-peak
rank-slope." Regressing the per-event relapse-excess (`delta_i`) on the peak-rank
magnitude:

- **Rank-slope point**: **+1.3100**. 95% CI **[-3.2358, +3.5429]**. p-analogue
  **0.2067**.

The slope point is positive (higher peak rank associated with more relapse-excess
across the 24 events), but its CI comfortably spans zero, so it too **cannot
resolve**. The standardised-difference statistic (the pre-reg's named primary)
and the rank-slope disagree in sign of the point estimate but agree in verdict:
neither excludes the null. Per the irrevocable primacy rule, the standardised
difference is the verdict; the rank-slope is reported as the companion reading,
not promoted.

## 5. The null (pre-reg section 6): ACF readout + E[L]

- Day-level ACF of the masked `max_hr_rank_lagged_lcera`: **rho(1) = +0.1113**,
  **rho(7) = +0.0843** (weak, short-range autocorrelation).
- Data-driven **E[L]\* = 7.000** (Politis-White / Patton-Politis-White estimator;
  cutoff lag 1). The factor-of-2 override did NOT fire (E[L]* does not deviate
  from 7 by more than 2x), so **E[L] = 7** is used, matching the
  `permutation_null_block_length.md` stationary-block default.
- Transparency note (carried from the pre-reg): the null MD's own literature
  anchor is deferred (the stationary-bootstrap canon is unread in the literature
  folder), so E[L] = 7 rests on first-principles reasoning plus the data-driven
  companion, not on a verified citation.
- Per-replicate mechanic (mirrors the sibling `peri-event-covid/test.py`): each
  of 10,000 replicates block-permutes the danger-window-vs-baseline labels across
  the pooled labelled units under stationary calendar blocks at E[L] = 7, holding
  each unit's relapse outcome and peak magnitude fixed, and recomputes the one
  primary statistic. The 10,000 recomputed values form the reference
  distribution; the observed percentile is the p-analogue and the 2.5/97.5
  percentiles are the CI.

## 6. Matched-baseline pool sizes actually constructed (pre-reg section 4d)

For the 24 usable crash peaks (masked primary arm), the matched-baseline pools
(all LC-era days outside any post-crash danger window meeting all three calipers:
rank-band +/- 0.03, same `recovery_phase`, preceding-3-day gevoelscore mean +/-
1.0) had sizes:

- **min = 0, median = 17, max = 50**. Two peaks had an EMPTY pool (crash-001,
  peak rank 0.964, and crash-002, peak rank 0.618), both early-2022 events whose
  `recovery_phase` stratum plus rank band plus felt-trajectory caliper admitted
  no out-of-window LC-era day. Those two events are excluded from the primary
  statistic (their `delta` is undefined), which is why the primary runs on 24
  usable events of the 26 built. `recovery_phase` was dense (all 1755 rows
  non-null), so it was used as the epoch caliper with no fallback to `lc_phase`.

The precondition predicted pool constructibility (63 days >= 0.95, 116 >= 0.90,
149 >= 0.87 available across bands); the per-peak calipered pools realised here
are smaller (median 17) because each pool is constrained by all three calipers
simultaneously (not just the rank band), which is the intended tight matching.

## 7. Crash-vs-dip formal slope interaction (pre-reg section 7)

- **Crash rank-slope +1.3100** vs **dip rank-slope -0.3858**; slope interaction
  (crash minus dip) = **+1.6959**.
- Crash primary statistic **-1.0287** vs dip primary statistic **+0.4256**.
- **Power asymmetry stated (pre-reg section 7)**: 79 dip windows carry ~2.7x the
  power of 28 crash windows (76 vs 24 usable here). So the crash-vs-dip
  divergence is NOT read as autonomic-window-specificity: the dip arm is SECONDARY
  and is never promoted to primary, and the interaction is base-rate-conditioned
  (each arm's `delta` subtracts that arm's own matched-baseline base rate, so a
  slope difference is a difference in slope, not in level). Neither arm's primary
  statistic excludes the null, and the interaction is reported as a number with
  wide error, not an era or specificity verdict.

## 8. Activity-volume comparison arm (pre-reg sections 2, 4b)

Repeating the primary with peak `eff_exertion_rank_lagged_lcera` (same window,
same peak rule, same matched-baseline construction on the volume rank):

- **Comparison primary statistic -2.3266**, rank-slope **-0.2204**, n_used 26.

The activity-volume arm's primary statistic is also negative and does not exclude
the null. The in-sample confound-test premise (pre-reg section 2, "cardiac cost
not step count") asked: does cardiac strain predict relapse WHERE activity volume
does not? Here **neither** axis predicts relapse above baseline (both point
estimates negative, both CIs span the null on the primary reading), so the
strain-vs-volume divergence does not adjudicate the confound in this sample: there
is no danger-window-vs-baseline effect on either axis to attribute to one
measure over the other. This is reported, not interpreted as confirming or
refuting "cardiac cost not step count."

## 9. Cumulative-strain secondary (pre-reg sections 4b, 9c)

Danger-window aggregate (sum over the danger-window days) of
`hr_area_above_daytime_baseline_waking_lcera` vs the danger-window relapse
indicator, across the 26 events with coverage:

- Cumulative-dose-vs-relapse slope **+0.000003**, correlation **+0.0548** (n=26):
  effectively no association.

**Autonomic-conflation disclosure (pre-reg section 9c, carried verbatim in
substance):** the cumulative-strain secondary
`hr_area_above_daytime_baseline_waking_lcera` sweeps up all-day HR elevation,
INCLUDING the resting autonomic arousal that IS the danger-window state, so it
conflates the exposure with the outcome-adjacent state. That is why `hr_area` is
secondary and `max_hr_rank` (an activity-driven spike) is the cleaner
threshold-crossing sensor. The peak-vs-cumulative contrast does not separate
here (neither predicts relapse), so it does not adjudicate threshold-crossing vs
dose-accumulation in this sample.

## 10. Sensitivities (pre-reg sections 4a, 4e, 4f, 5)

All secondary, none promoted. (`stat` = standardised primary statistic; `slope` =
rank-slope; `n` = usable events.)

| Sensitivity | Result |
|---|---|
| **Danger-window band 7 / 10 / 14** | 7: stat -2.2447, slope +0.0001, n 24. 10 (primary): stat -1.0287, slope +1.3100, n 24. 14: stat -0.6005, slope +0.8994, n 24. |
| **Relapse band 3 / 4 / 5** | 3: stat -0.5292, slope +1.3625, n 24. 4 (primary): stat -1.0287, slope +1.3100, n 24. 5: stat -0.4120, slope +1.1711, n 24. |
| **Masked (primary) vs un-masked (stored)** | masked: stat -1.0287, slope +1.3100, n 24. un-masked: stat -1.0971, slope +0.6825, n 26. |
| **Autonomic-trend exclusion** (drop danger-window days whose autonomic z is rising) | stress-key (`stress_mean_sleep_lagged_lcera_z` rising): stat -1.8763, slope -0.0520, n 23. rhr second-read (`resting_hr_lagged_lcera_z` rising): stat -1.0427, slope +1.0219, n 23. |

Across every band and every exposure variant, the standardised primary statistic
stays negative or near-zero and no reading excludes the null. The verdict is
stable to all pre-registered sensitivities: **Cannot resolve** is not an artefact
of one window / relapse / masking choice. (The autonomic-trend sensitivity ran on
the covered subset; the few danger-window days uncovered by the lagged-z columns
were retained and disclosed, per pre-reg section 4f.)

## 11. Caveats (pre-reg section 9, carried in substance)

**(a) The two-case null-reading (so physical-only scope is not immunity).** Case
(1): a relapse with NO physical / cardiac exposure at all is out of support /
neutral (a possible mental-PEM trigger, the parked R4), NOT counter-evidence.
Case (2): an in-danger-window strain spike that does NOT relapse above the matched
baseline IS disconfirming ("the physically-visible danger-window effect is not
established"). The mental-PEM escape applies ONLY to case (1); it never absorbs a
physical spike that failed to relapse. This test's danger-window peaks were
overwhelmingly high-strain (median peak rank ~0.95) and did NOT relapse above
baseline, which is case (2) territory, so the honest reading is that the
physically-visible danger-window effect is not established here, tempered only by
the wide CI (hence "Cannot resolve," not "Not supported").

**(b) Physical / cardiac scope; mental-PEM invisible.** The exposure is
physical / cardiac strain only. `eff_exertion` and `max_hr_rank` are blind to
cognitive / emotional / orthostatic load, which draws on the same envelope and
can trigger PEM (parked R4). The hypothesis is scoped to the physically-visible
subset.

**(c) The `hr_area` autonomic-conflation disclosure.** See section 9 above:
`hr_area_above_daytime_baseline_waking_lcera` sweeps up all-day HR elevation
including the resting autonomic arousal that IS the danger-window state, so it
conflates the exposure with the outcome-adjacent state. That is why it is
secondary and `max_hr_rank` (an activity-driven spike) is the cleaner
threshold-crossing sensor.

**(d) The reverse-causation felt-lag residual bias.** The felt-recovered gate is
the only available ordering sensor and it is known to LAG the autonomic state, so
a prodromal relapse can suppress activity / HR before the felt-state descends. The
ordering guard (peak strictly precedes the relapse; days that fell back below the
felt-recovery gate are excluded from being a peak) and the autonomic-trend
sensitivity (section 10) mitigate but do not remove this; the residual is a NAMED
directional bias on the CI, not a clean guard. Its direction would, if anything,
suppress a true positive effect (a brewing relapse depresses the very peak strain
that would otherwise be the exposure), so the null-spanning result is not made
more benign by this bias.

**(e) n=1, association not causation.** This is a single-subject observational
test; a supported result would be an association within this subject's danger
windows, never a causal or generalisable claim. The CIs are wide (24 event-level
units). The exposure is self-selected (pacing is not random), so this is a
dose-response question, not a natural experiment.

**(f) Single-pool primacy.** Any over-time / era-split difference (including the
crash-vs-dip interaction and any era pattern in the per-event detail) is a number
with wide error, never an era verdict.

**(g) No causal / interpretive marks on the descriptive layer.** The claim is
"danger-window peak strain did NOT predict relapse above the matched baseline,"
never "the spike caused / prevented the relapse."

## 12. Honest framing

With 24 event-level units, n=1, heavy self-selection of exposure (danger-window
strain is near-ubiquitous by construction, precondition section 3.1), and
E[L] ~ 7 autocorrelation, the design was pre-registered as underpowered for
anything but a large effect, with an estimate-plus-honest-CI as the primary
deliverable and "Cannot resolve" as the pre-committed default reading of a
null-spanning CI. That is the outcome. The point estimate carries no signal in
the predicted direction (mean delta -0.116, standardised statistic -1.03, both
slightly against the hypothesis), so the result constrains the design's own power
and offers no positive evidence for the danger-window mechanism in this subject's
physically-visible strain windows. It is publishable as an honest limit and is
NOT upgraded to "suggestive" or "consistent with."

## 13. Implementation notes / resolved ambiguities

- **A. Masking-induced coverage loss (24 usable, not 28).** The locked masking
  (pre-reg section 4e) excludes `is_crash` / `is_dip` days from the `[d-90, d-30]`
  baseline pool. In the dense late-2023 / early-2024 era (~32 crash+dip days in a
  ~3.5-month span), this drops the masked pool from 60 to 36-38 valid days, below
  the extractor's locked `MIN_LAGGED_DAYS = 40`, so those danger-window days
  become uncovered under the masked primary. Two crash windows (crash-015 nadir
  2024-01-12, crash-016 nadir 2024-01-21) lose ALL danger-window coverage this
  way and drop out, so 26 peaks are built (not 28) and 24 have a non-empty
  matched pool. This is exactly the neighbouring-crash baseline-contamination
  scenario the precondition (section 3.3) foresaw; it is a faithful consequence
  of the locked masking, not a fix or a design change. The un-masked sensitivity
  (section 10) retains 26 events, confirming the delta is purely the masking.

- **B. Ordering guard operationalisation (pre-reg section 4f, crude case).** The
  pre-reg says "exclude as exposure candidates any day already in a descending
  felt-state so a relapse day is never its own exposure." The simplest faithful
  reading was chosen: a danger-window day whose own `gevoelscore` has fallen back
  below the felt-recovery gate (`< 4`, i.e. back into the `<= 3` crash/dip zone)
  is dropped from the peak candidate set. Because a relapse day (a new crash/dip)
  has `gevoelscore <= 3` by definition, this guarantees a relapse day is never
  selected as its own peak, and the relapse is counted strictly AFTER the peak
  (k = 1..window). Logged as an implementation note.

- **C. Deterministic peak selection.** Danger-window days are held as a sorted
  calendar list (not a set) and the peak is `max(rank, then earliest-day)`, so a
  rank tie resolves deterministically to the earliest day and the result is
  seed-independent and reproducible across runs (an initial set-hash-ordered
  version was non-deterministic on the autonomic-trend sensitivity; fixed).

- **D. Cumulative-strain readout.** The cumulative exposure is a per-event
  danger-window SUM, not a single-day peak, so it cannot enter the same
  matched-baseline delta as the peak arms; it is reported as the dependence of the
  danger-window relapse indicator on the cumulative dose (slope + correlation),
  which is the simplest faithful readout of the threshold-crossing-vs-dose-
  accumulation contrast. Disclosed with the section-9c conflation caveat.

- **E. Danger-window day count.** The masked primary danger-window day count for
  window=10 is 237 present rows across the 28 felt-recovered crash windows vs the
  precondition's cited 236 (an off-by-one boundary-presence detail on a coverage
  count, not an outcome); it does not affect any statistic.

- **F. LC-era reference universe.** The matched-baseline reference universe is
  LC-era days (`lc_phase == 'lc'`, exactly where the `_lcera` rank is defined),
  excluding every crash danger-window day at the widest sensitivity band (14) so
  no window day can leak into a baseline pool.

---

*Executed 2026-07-04. Implements the LOCKED pre-registration
[`hypothesis.md`](hypothesis.md) verbatim. Primary exposure: peak masked
`max_hr_rank_lagged_lcera` (r3 cardiac-strain, section 4e masked primary).
Verdict: Cannot resolve (pre-committed default reading of a null-spanning CI).
Cross-refs: methodology MD `../../../methodology/post_crash_exertion_relapse.md`;
descriptive precondition `../../descriptive/post_crash_exertion_relapse/precondition.md`;
sibling null precedent `../peri-event-covid/test.py`;
`../../../methodology/permutation_null_block_length.md`; the `_lcera` extractor
`../../garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py`.*
