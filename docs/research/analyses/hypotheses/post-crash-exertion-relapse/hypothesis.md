# Post-crash exertion relapse (the "danger window"), does a supra-threshold peak cardiac-strain spike in the felt-recovered-but-autonomically-unsettled window trip a relapse more than the same spike at baseline?

**Pre-registration written 2026-07-04, before any relapse count or any
exposure-versus-relapse relationship has been computed or inspected. Locked.
Any subsequent change to the claim, the primary exposure, the danger-window
definition, the matched-baseline construction, the null, the relapse window, or
the primary test creates a v2.**

This pre-registration is the inferential test that the post-crash-exertion
"danger window" mechanism produces. After a crash, the felt-state rebounds in
~2-3 days but the autonomic system settles over ~2 weeks (R9; autonomic is the
slowest channel). During that mismatch, felt-recovered but autonomically
unsettled, the PEM threshold (a cardiac / HR threshold, VT1-class) is
transiently lowered, so a single supra-threshold cardiac-strain spike is more
likely to trip a relapse than the same-magnitude spike at baseline. *Feeling
fine is not the same as being recovered.*

This pre-reg faithfully implements the locked methodology design
[`../../../methodology/post_crash_exertion_relapse.md`](../../../methodology/post_crash_exertion_relapse.md)
(status DESIGN PROPOSED r3; decisions a to g, the constructed null f-i/ii/iii,
the crash-vs-dip slope interaction f-iv, the power/multiplicity section 4, the
confounds section 5, and the falsification framing section 6). r2 absorbed the
fresh-session methodology review
[`../../../reviews/methodology-post_crash_exertion_relapse-2026-07-03.md`](../../../reviews/methodology-post_crash_exertion_relapse-2026-07-03.md)
(ACCEPT-WITH-MINOR-REVISIONS; its three MAJORs, the RTM/base-rate reference, the
event-level null + power/multiplicity, and the crash-vs-dip interaction, are
closed here as constructions rather than intentions). r3 swapped the primary
exposure to a cardiac-strain measure to answer the documented step-count /
activity-volume confound. It is backed by the descriptive precondition
[`../../descriptive/post_crash_exertion_relapse/precondition.md`](../../descriptive/post_crash_exertion_relapse/precondition.md),
whose numbers (coverage + exposure distribution only) are cited below and are
NOT recomputed here.

> ## NO-OUTCOME-PEEK LOCK (binding)
>
> This is a pre-registered inferential test. The pre-registration is credible
> only if the outcome, whether post-crash danger-window exertion actually
> predicts relapse, is **unseen** when this document locks.
>
> **What HAS been seen, and is fixed here (predictor-only):**
> - The event location: **29 crash episodes and 79 dip days on Stratum 4**
>   (`per_day_master.csv`, `is_crash` / `is_dip` / `crash_episode_id`,
>   2022-09-03 to 2026-06-05; nadir = min-`gevoelscore` day per episode).
> - Felt-recovery coverage (row presence of a `gevoelscore >= 4` day in
>   t+1..t+10): **28 / 29** crashes, **79 / 79** dips.
> - Primary-exposure coverage in the danger windows: `max_hr_rank_lagged_lcera`
>   present **235 / 236** crash danger-window days; `eff_exertion_rank_lagged_lcera`
>   **236 / 236** crash and **790 / 790** dip danger-window days.
> - The primary-exposure (predictor) distribution: crash danger-window peak
>   `max_hr_rank_lagged_lcera` median **0.95** (p25 0.87, p75 0.98, min 0.50,
>   max 1.00); the activity-volume comparison peak `eff_exertion_rank_lagged_lcera`
>   median **0.93** (crash) and **0.92** (dip), spanning comparable ranges.
> - The exposure-axis divergence that is the confound-test premise:
>   danger-window day-level **rho(max_hr_rank, eff_exertion) = +0.42** (n=235
>   days) -- a predictor-versus-predictor rank correlation, never an outcome.
> - The comparison design: danger-window peaks vs a constructed matched-baseline
>   reference set of equal-magnitude peak-strain days outside any post-crash
>   danger window.
>
> **What has NOT been seen, and MUST stay unseen until this locks:**
> any relapse count (marginal or conditional), any relapse rate, any
> dose-response, any test statistic, any danger-window-vs-baseline contrast, in
> the crash arm, the dip arm, or any comparison set. No test has been run; no
> `test.py` has been written or executed; no `result.md` exists. **Every number
> above is a coverage / non-null count or a predictor (exposure) distribution,
> never an outcome and never an exposure-versus-relapse relationship.** The
> exposure-versus-relapse contrast IS the test; it runs only after this pre-reg
> locks and is reviewed fresh in another session (per
> [CONVENTIONS §1.2 / §3.5](../../../CONVENTIONS.md)).

## Authorship

| Field | Value |
|---|---|
| Drafted by | Claude (Opus 4.8) under reviewer-mode-with-authorization, for the participant-researcher (repo owner) |
| Date | 2026-07-04 |
| Mode | Reviewer-mode pre-registration (per CONVENTIONS §1.2). Drafted from the locked producer-mode methodology MD (r3), fresh-session peer-reviewed 2026-07-04 (ACCEPT-WITH-MINOR-REVISIONS; r3 exposure re-confirmed cold; revisions absorbed, see lock log). |
| Discipline | No-outcome-peek LOCK (above), no interpretive marks on the descriptive layer (§4.1), stress = Garmin GSS not mental stress (below). |

---

## 1. Claim

After a crash, during the **danger window** (felt-state recovered,
`gevoelscore >= 4`, but autonomic not yet settled, from the felt-recovery day
through nadir+10), a single **supra-threshold peak cardiac-strain spike** is
more likely to trip a **relapse** (a new crash or dip within ~4 days) than the
**same-magnitude peak-strain spike at baseline**.

- **Primary exposure**: the **peak single-day** `max_hr_rank_lagged_lcera` in
  the danger window (peak HR relative to current LC-era capacity, the max single
  day), read as a **continuous dose-response** with a **pre-locked link
  function** (§4c).
- **Counterfactual ("vs matched baseline")**: the relapse rate of danger-window
  peaks is contrasted against a **constructed matched-baseline reference set**
  of equal-magnitude peak-strain days that fall **outside any post-crash danger
  window** (§4d). The hypothesis is "more likely than *the same spike at
  baseline*," so the baseline is a constructed matched comparison, not an
  adjective.
- **Predicted direction**: a **positive dose-response**, higher danger-window
  peak cardiac strain predicts higher relapse likelihood *relative to the
  matched-baseline reference at the same peak-strain magnitude*.

The **single primary test** is: **peak cardiac strain
(`max_hr_rank_lagged_lcera`) x crash arm x 10-day danger window x 4-day relapse
window x matched-baseline contrast** (§8). Everything else, the activity-volume
comparison arm, the cumulative-strain arm, the dip arm, and every sensitivity
band, is explicitly secondary and is **not promoted to primary if it wins**
(peak-primacy is irrevocable).

**Guardrail.** Throughout this document, "stress" means **Garmin's stress score
(GSS), an HRV-derived measure**, NOT mental or emotional stress. "Exertion" /
"strain" means **physical** activity / cardiac load, NOT cognitive, emotional,
or orthostatic load (decision g).

## 2. Why we think this

The direction is **prior-given, so this is confirmatory, not data-fishing**
(CONVENTIONS §4.3; all three §4.3 questions answered yes: lived pacing
experience that pre-dates the analysis, published single-bout support, and a
mechanistic argument independent of any data look). Three independent legs:

- **PEM's cardiac-threshold-crossing literature.** PEM's evidenced mechanism is
  single-bout **cardiac** threshold suppression: the 2-day-CPET
  threshold-suppression paradigm (Workwell / Keller / Lien / Thomas), VT1 as the
  PEM threshold, ~24h HRV suppression after a single crossing. So the faithful
  threshold-crossing exposure is **peak cardiac output relative to current
  capacity**, not activity volume (per
  [`../../../literature/push crash research.md`](../../../literature/push%20crash%20research.md),
  [`../../../literature/pacing-and-crash-mitigation.md`](../../../literature/pacing-and-crash-mitigation.md)).
  The literature explicitly flags the dose-accumulation "total load" model as
  appearing only in clinical-consensus and patient-guidance language, untested
  against the single-bout model; the cumulative-strain arm (§3, §4b) is
  therefore a genuinely novel (though n=1, un-generalisable) contrast on a
  question the literature leaves open.
- **The danger-window dissociation.** The felt-state rebounds in ~2-3 days while
  the autonomic system settles over ~2 weeks (~12.7d in Moore 2023; RHR ~79d in
  Radin; R9 + the peri-event recovery card + `pem_recovery_trajectory_review.md`).
  During that felt-fast / autonomic-slow mismatch the PEM threshold is
  transiently lowered, so the same physical spike lands harder than it would at
  a settled baseline. Crashes carry this distinctive post-crash autonomic
  signature (HA-P6: 4/7 channels distinguishable from matched controls; R9);
  dips do NOT (flat overnight stress), which is exactly why dips are the
  mechanism control (§7).
- **The cardiac-cost-not-step-count confound.** Step count / activity volume
  measures "how much someone walks, not how they walk" (Founder&City 700k-day
  wearable analysis: PEM cases needed ~50% more cardiac work for identical
  walks; the recommended measure is the "cardiac cost of movement," not volume).
  The confound applies within-person here: cardiac cost per unit activity rises
  as capacity falls (deconditioning plus the low-capacity danger window), so an
  activity-volume exposure under-detects exactly the low-volume cardiac
  threshold-crossings that matter most in the danger window. The two axes
  genuinely diverge in the danger windows (day-level rho(max_hr_rank,
  eff_exertion) = +0.42; they disagree on ~58% of the rank-variance;
  precondition §3.4), so the **strain-vs-volume divergence is itself an in-sample
  test of the confound**: if cardiac strain predicts relapse where volume does
  not, "cardiac cost not step count" is confirmed n=1.

Per CONVENTIONS §4.3, the pre-registration protects the **outcome** (unseen
until lock), not the **direction** (which is prior-given by the literature and
the mechanism).

## 3. Data sources

- **Per-day series**: `per_day_master.csv`, the LC-era **Stratum-4** surface (LC
  with gevoelscore + crash labels, 2022-09-03 to 2026-06-05).
- **Trigger events**: `crash_episode_id` + `is_crash` (crashes, primary arm);
  `is_dip` (dips, mechanism-control arm). Nadir t0 = the min-`gevoelscore` day
  per episode. Named per CONVENTIONS §3.6: *29 crash episodes and 79 dip days on
  Stratum 4 (`per_day_master.csv`, `is_crash` / `is_dip` / `crash_episode_id`,
  2022-09-03 to 2026-06-05)*.
- **Felt-state gate**: `gevoelscore` (the ground-truth daily felt-state; the
  danger window opens at the first `gevoelscore >= 4` day in t+1..t+10).
- **Primary exposure**: `max_hr_rank_lagged_lcera` (peak HR relative to current
  LC-era capacity; peak single-day rank in the danger window). Lagged,
  era-local baseline `[d-90, d-30]`, LC-era days only, per CONVENTIONS §3.2.
- **Comparison-arm exposure**: `eff_exertion_rank_lagged_lcera` (activity-volume,
  the HA01c operand; UDS passive intensity-minutes + recorded activity duration,
  percentile-ranked against the lagged era-local window). Lagged, era-local.
- **Cumulative-strain secondary exposure**:
  `hr_area_above_daytime_baseline_waking_lcera` (the cardiac-load integral, the
  dose-accumulation competitor). Lagged, era-local.
- **Outcome (the TEST, not read here)**: a new crash OR dip within ~4 days of
  the peak-strain day, from the same `is_crash` / `is_dip` labels (a different
  data source from the HR / activity exposures, per confound 5).

**Inherited operand disclosure.** The comparison-arm exposure
`eff_exertion_rank_lagged_lcera` is the HA01c operand
([`../HA01c-effective-exertion-shock/hypothesis.md`](../HA01c-effective-exertion-shock/hypothesis.md),
SUPPORTED, load-bearing status withheld pending its v2 threshold-monotonicity
diagnostic). This test does not inherit HA01c's `>= 0.75` binary threshold: the
precondition's degenerate-binary finding (§4c below) mandates a **continuous
peak** for both the primary and the comparison arm, which also sidesteps HA01c's
threshold-monotonicity trap.

## 4. Measurement protocol (locking the constructions the methodology MD names as open)

### 4a. The danger window (locked; 7/10/14 sensitivity)

- **Felt-recovery gate**: `gevoelscore >= 4` (back into the normal 4-5 band, out
  of the `<= 3` crash/dip zone; the felt-state clusters at 4-5, p25 = 4). The
  danger window **opens** at the first day in t+1..t+10 with `gevoelscore >= 4`.
- **Danger window (primary)**: from the felt-recovery day **through nadir+10**.
  This is inside the ~2-week autonomic-settle window and captures the mismatch
  without reaching the next ordinary baseline.
- **Sensitivity band**: **7 / 10 / 14** days. A longer window trades power for
  dilution; all three are reported, 10 is the locked primary.
- **Coverage (predictor-only, cited)**: felt-recovery reached in **28 / 29**
  crash windows and **79 / 79** dip windows (precondition §3); the one excluded
  crash has no felt-recovery day. The primary contrast runs on the **28 usable
  crash windows**.

### 4b. The exposures (locked primacy)

- **PRIMARY (threshold-crossing)**: the **peak single-day
  `max_hr_rank_lagged_lcera`** in the danger window, continuous. Peak =
  the **max over daily rank** within the window (not a top-k average, not a
  transform of rank; the "peak single-day" wording of the precondition is the
  locked definition). Coverage 235 / 236 crash danger-window days; peak median
  0.95, a continuous 0.50-1.00 gradient (a binary `>= 0.75` flag is degenerate
  at 24/28 = 86%, so the continuous peak is used; §4c).
- **COMPARISON ARM (activity-volume)**: the peak single-day
  `eff_exertion_rank_lagged_lcera`, continuous, same window and same peak rule.
  The strain-vs-volume divergence (rho = +0.42) is the in-sample test of the
  cardiac-cost-not-volume confound.
- **CUMULATIVE-STRAIN SECONDARY (dose-accumulation)**: the danger-window
  aggregate of `hr_area_above_daytime_baseline_waking_lcera` (the cardiac-load
  integral), pitting threshold-crossing against dose-accumulation. **The
  conflation is disclosed** (§9): `hr_area` sweeps up all-day HR elevation
  including the resting autonomic arousal that IS the danger-window state, so it
  conflates exposure with the outcome-adjacent state; a peak-HR spike is
  activity-driven and cleaner. `hr_area` is therefore secondary only. (Note: the
  demotion is **scope-specific** to the danger-window estimand, where the
  integral conflates with the autonomic state being estimated; it does NOT
  override CONVENTIONS §3.3's general preference for `hr_area` as the
  magnitude x duration integral when a cumulative-burden hypothesis does want an
  integral.)

All three exposures use the lagged era-local `[d-90, d-30]` LC-era baseline per
CONVENTIONS §3.2.

### 4c. The dose-response link function (locked; no post-hoc substitution)

The primary readout is a **relapse-rate monotone in the peak rank**, reported as
a **rank-slope / rank-correlation with a CI** (the danger-window-vs-matched-
baseline contrast enters as the reference level, §4d + §6). This link is
**fixed here, before any outcome look**; **no alternative functional form
(logistic, spline, top-k, or a rank transform) will be substituted post-hoc.**
This closes the continuous-dose-response degree of freedom the methodology
review flags (finding 3): the degenerate-binary problem was *cutoff* freedom;
the continuous move must not trade it for *functional-form* freedom. The peak
definition is locked to the max single-day rank (§4b). The precondition's
degenerate-binary finding is load-bearing: a binary "`>= 1` day `>= 0.75`" flags
24/28 crash windows (86% exposed, only 4 unexposed = no usable contrast group),
which **rules out a binary exposure and mandates the continuous peak** (§3.1 of
the precondition).

### 4d. The constructed matched-baseline reference set (locked)

The hypothesis is "more likely than *the same spike at baseline*," so the
baseline is a **constructed matched comparison**, not a within-window
dose-response alone. The reference set is **equal-magnitude peak-strain days
that fall OUTSIDE any post-crash danger window**, matched on:

1. **peak-strain-rank band** (the `max_hr_rank_lagged_lcera` magnitude, so the
   contrast is same-spike-vs-same-spike);
2. **LC-era / deconditioning epoch** (the exertion envelope demonstrably shrank
   across the LC era, ~15 kg / VO2Max 52->37, so a spike must be compared within
   a comparable-capacity epoch, not across the ramp);
3. **a comparable felt-state trajectory** (so regression-to-the-mean is
   controlled; relapse is common after any low day, so the reference conditions
   on a comparable felt-state path, not just a comparable peak).

**Matching operationalisation (locked, pre-outcome, review finding 3):** (i)
**rank-band caliper** = peak `max_hr_rank_lagged_lcera` within +/- 0.03 of the
danger-window peak; (ii) **epoch** = same LC-era recovery-phase stratum; (iii)
**felt-state-trajectory caliper** = the baseline day's own preceding 3-day
`gevoelscore` mean within +/- 1.0 point of the danger-window peak day's, so the
reference is matched on where the felt-state sits AND its recent slope (not just
the peak). **Matching ratio** = all-eligible-in-caliper (every out-of-window
day meeting all three calipers enters the reference for that peak; no random
1:1 draw, so there is no seed-dependent forking path). **Pool constructibility
(predictor-only):** out-of-window LC-era days at the peaks' rank bands number
**63 at >= 0.95, 116 at >= 0.90, 149 at >= 0.87** (28 peaks to match, median
peak 0.95), so the reference is constructible; it thins at the very top
(32 days >= 0.98), which is disclosed as a variance limit at the high-rank end.

The **PRIMARY test is the relapse rate of danger-window peaks vs matched
baseline peaks** at the same peak-strain magnitude (§6, §8). A within-window
dose-response is secondary. This is the methodology review's single most
consequential fix (finding 4a): without the constructed baseline, "more likely
than at baseline" has no baseline.

### 4e. Crash/dip baseline masking (locked; un-masked sensitivity)

The lagged `[d-90, d-30]` baseline self-cleans against the **index** crash (it
closes at least 20 days before the index nadir; window arithmetic in the
methodology review finding 5). It does NOT fully clean against **neighbouring**
crashes in the dense 2023-24 era (~10 crashes/yr, ~30-40 days apart), where the
60-day window can straddle a previous crash and deflate the reference (inflating
the index day's rank). **Resolved branch (review finding 6c, pre-outcome
fact-check):** the `_lagged_lcera` extractor (`analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py`,
`compute_lagged_rank`) ranks today against ALL days in [d-90, d-30] and does
**NOT** exclude crash/dip days (its only exclusion is the pre-LCERA
`min_window_date`). Therefore **crash/dip-day masking is applied in `test.py`
as the locked primary**, and the un-masked as-built `_lagged_lcera` column is
the single named sensitivity. Zero post-lock discretion.

### 4f. The reverse-causation ordering guard + the autonomic-trend sensitivity (locked)

Two layers, plus a named residual bias:

- **Ordering guard (crude case)**: the peak **strictly precedes** the relapse,
  and days already in a **descending felt-state** are excluded, so a relapse day
  is never counted as its own exposure.
- **Autonomic-trend exclusion sensitivity (subtle case; locked column, review
  finding 6b)**: the felt-recovered gate is the only available *ordering*
  sensor, and by the design's own premise the felt-state **lags** the autonomic
  state, so a felt-based exclusion is the wrong sensor for a brewing relapse (a
  prodromal relapse can suppress activity/HR *before* the felt-state visibly
  descends). A **definite (not conditional) sensitivity excludes danger-window
  days whose autonomic trend is already adverse**, keyed to
  **`stress_mean_sleep_lagged_lcera_z` rising** (the R9 overnight-stress
  signature; danger-window-conditional coverage **228 / 233 days = 98%**), with
  **`resting_hr_lagged_lcera_z` rising** (coverage 209 / 233 = 90%) as a second
  read. The sensitivity runs on the covered subset; the few uncovered
  danger-window days are disclosed. (The ~78-82% whole-corpus fill of these
  lagged-z variants does NOT apply in the danger windows, which are LC-era
  gevoelscore days where the columns are dense.)
- **Named directional bias**: any residual is stated as an **irreducible,
  named directional bias on the CI** (the design cannot fully remove it; the
  felt gate is known to lag). This is not a clean guard, it is a disclosed
  limitation (§9).

## 5. The outcome + relapse window

- **Outcome (relapse)**: a **new crash OR dip within 4 days** of the peak-strain
  day (delayed-onset PEM; onset is 12-72h+). The 4-day window is the locked
  primary.
- **Sensitivity band**: **3 / 4 / 5** days. Outcome-*coverage* per window length
  (row presence only, not outcome values) is reported in the precondition; the
  outcome **values** stay unseen until the test runs.
- The relapse is read from the same `is_crash` / `is_dip` labels (a different
  data source from the HR / activity exposures, so exposure and outcome are
  independent measurements, confound 5).

## 6. The null / inference (constructed)

Implementing the methodology MD's constructed null (f-i / f-ii) exactly:

- **The primary contrast** is the **danger-window-vs-matched-baseline** relapse
  rate at equal peak-strain magnitude (§4d), read as the rank-slope / relapse-
  rate-monotone-in-peak with a CI (§4c).
- **The null is EVENT-LEVEL, a 28-unit block-permutation.** With 28 usable crash
  windows the relevant n is **28 events, not ~1700 days**. The permutation
  **block-permutes the event-level danger-window vs matched-baseline labels**
  (not day-level rows), so the autocorrelation within a window is respected by
  construction and the effective n is not inflated to the day count.
- **ACF readout + E[L] justification.** The pre-reg reports **(a) the day-level
  ACF of `max_hr_rank_lagged_lcera`** to justify the E[L] = 7 stationary-block
  default per
  [`../../../methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)
  **or trigger that MD's override**, and **(b) a data-driven E[L]\* companion
  with a factor-of-2 flag** (if the data-driven E[L]\* deviates by more than 2x
  from 7, the override fires and E[L]\* is used). Transparency note: the null
  MD's own literature anchor is **deferred** (the stationary-bootstrap canon is
  unread in the literature folder), so E[L] = 7 rests on first-principles
  reasoning plus the data-driven companion, not on a verified citation.
- **Per-replicate mechanic (locked, review finding 6d; mirrors the sibling
  peri-event-covid pre-reg precedent).** Each of **>= 10,000 replicates**
  block-permutes the **28 event-level labels** (each usable crash's
  danger-window peak vs its matched-baseline set) under stationary blocks at
  **E[L] = 7** (or the data-driven E[L]* the ACF readout justifies; if E[L]*
  deviates > 2x from 7 the override fires and E[L]* is used), holding the
  peak-strain magnitudes fixed and only permuting which unit is labelled
  danger-window vs baseline; it recomputes **the one primary statistic** (the
  relapse-rate-monotone-in-peak rank-slope, equivalently the standardised
  danger-window-vs-baseline difference at matched magnitude) under that permuted
  labelling; the >= 10,000 recomputed values form the reference distribution.
  The observed statistic's percentile in that distribution is the p-analogue,
  and the 2.5/97.5 percentiles of the same distribution give the CI. This drives
  post-lock null discretion to zero.
- The effect size (the standardised danger-window-vs-baseline difference and the
  rank-slope) comes from that **same** block-permutation machinery, so one null
  model serves both the p-analogue and the CI. Direction + magnitude are always
  reported alongside any p-analogue, never the p alone.

## 7. Crash-vs-dip as a formal slope interaction

Implementing decision f-iv exactly. The crash-vs-dip contrast is a **formal
slope interaction** (does the peak-strain-relapse slope **differ** between
crashes and dips), NOT two eyeballed side-by-side verdicts.

- **Base-rate conditioning**: a dip is a milder event with a different relapse
  base rate, so "weaker after dips" must be a **slope** difference, not a
  **level** difference; the interaction conditions on the base-rate difference.
- **Power asymmetry stated**: **79 dip windows carry ~2.7x the power of 28 crash
  windows.** So an effect-on-crashes / null-on-dips (or the reverse) is NOT read
  as autonomic-window-specificity without accounting for power: the
  better-powered dip arm failing while the underpowered crash arm shows an effect
  is exactly what noise plus a small true effect can produce.
- **Comparable support confirmed (predictor-only)**: the dip danger-window peak
  `eff_exertion_rank_lagged_lcera` (median 0.92, p25 0.83, p75 0.97) is
  near-identical to the crash-window peak (median 0.93), so the two arms' slopes
  are compared over overlapping exposure ranges (precondition §3.2). The
  autonomic-window-specificity read is: premature strain raises relapse after a
  *crash* (autonomic signature present) but not after a *dip* (flat overnight
  stress), evidenced as a **slope** difference with base-rate conditioning.

The dip arm is a **secondary** falsification lever, not promoted to primary
(§8).

## 8. Pre-registered verdict + power / precision / multiplicity

- **The single primary test** (irrevocable): **peak cardiac strain
  (`max_hr_rank_lagged_lcera`) x crash arm x 10-day danger window x 4-day relapse
  window x matched-baseline contrast** (§1, §4b, §4d, §5, §6). Its CI is the
  verdict.
- **Everything else is explicitly secondary / comparison / sensitivity, and is
  NOT promoted to primary if it wins** (peak-primacy is irrevocable): the
  activity-volume comparison arm (`eff_exertion`), the cumulative-strain
  secondary (`hr_area`), the dip arm, and the 3/4/5-day + 7/10/14-day +
  masked/un-masked-baseline + autonomic-trend sensitivities. The
  cumulative-strain arm is reported as a mechanism-adjudication contrast
  regardless of which of peak/cumulative separates better; a cumulative-wins
  result is a genuinely novel (n=1, un-generalisable) data point on the open
  threshold-crossing-vs-dose-accumulation question, but it does **not** become
  the primary verdict.
- **Power / precision (a pre-registered expectation, not a post-hoc
  consolation).** With **28 event-level units**, a continuous dose-response,
  n=1, and E[L] ~ 7 autocorrelation, the design is **underpowered for anything
  but a large effect.** The **primary deliverable is an estimate with an honest
  CI, not a reject/accept verdict.** **"Cannot resolve" is the pre-committed
  default reading of a CI that spans the null**; a wide CI is never upgraded to
  "suggestive" or "consistent with." Effective independent looks ~3-4
  (`permutation_null_block_length.md` §4) must not be silently spent, which is
  why the single primary test is named and the rest is labelled secondary.
- **Single-pool primacy** (preserved verbatim from the methodology MD, decision
  f [P]): any over-time difference is a number with wide error, never an era
  verdict.

## 9. Caveats result.md must carry

`result.md` must explicitly acknowledge all of the following:

- **(a) The two-case null-reading (so physical-only scope is not immunity).**
  Case (1): a relapse with **no physical/cardiac exposure at all** is **out of
  support / neutral** (a possible mental-PEM trigger, the parked R4), NOT
  counter-evidence. Case (2): an **in-danger-window strain spike that does NOT
  relapse above the matched baseline IS disconfirming** ("the physically-visible
  danger-window effect is not established"). The mental-PEM escape applies ONLY
  to case (1); it must never absorb a physical spike that failed to relapse.
- **(b) Physical / cardiac scope; mental-PEM invisible.** The exposure is
  physical/cardiac strain only. `eff_exertion` and `max_hr_rank` are blind to
  cognitive / emotional / orthostatic load, which draws on the same envelope and
  can trigger PEM (parked R4). The hypothesis is scoped to the
  physically-visible subset.
- **(c) The `hr_area` autonomic-conflation disclosure.** The cumulative-strain
  secondary `hr_area_above_daytime_baseline_waking_lcera` sweeps up all-day HR
  elevation, including the resting autonomic arousal that IS the danger-window
  state, so it conflates the exposure with the outcome-adjacent state. That is
  why `hr_area` is secondary and `max_hr_rank` (an activity-driven spike) is the
  cleaner threshold-crossing sensor.
- **(d) The reverse-causation felt-lag residual bias.** The felt-recovered gate
  is the only available ordering sensor and it is known to **lag** the autonomic
  state, so a prodromal relapse can suppress activity/HR before the felt-state
  descends. The autonomic-trend sensitivity (§4f) mitigates but does not remove
  this; the residual is a **named directional bias on the CI**, not a clean
  guard.
- **(e) n=1, association not causation.** This is a single-subject observational
  test; a supported result is an association within this subject's danger
  windows, never a causal or generalisable claim. CIs are wide (28 units).
- **(f) Single-pool primacy.** Any over-time / era-split difference is a number
  with wide error, never an era verdict.
- **(g) No causal / interpretive marks on the descriptive layer (§4.1).** The
  claim is "danger-window peak strain did / did not predict relapse above the
  matched baseline," never "the spike caused the relapse."

## 10. What we do with each outcome

- **Supported** -> danger-window peak cardiac strain relapses **more than
  matched-baseline peaks** (beyond the event-level null), AND the crash-vs-dip
  slope interaction shows autonomic-window-specificity. Report the rank-slope /
  relapse-rate contrast and its CI plainly. The strain-vs-volume contrast
  adjudicates "cardiac cost not step count"; the peak-vs-cumulative contrast
  adjudicates threshold-crossing vs dose-accumulation. Reach is bounded to this
  subject, physical/cardiac scope, and these 28 crash windows.
- **Not supported** -> no danger-window-vs-baseline difference, or no
  interaction, or an in-danger-window strain spike that does not relapse above
  baseline (case 2 of §9a). Reported as "**the physically-visible danger-window
  effect is not established**." The mental-PEM escape (§9a case 1) does NOT
  rescue this.
- **Cannot resolve** -> a CI that spans the null. This is the **pre-committed
  default reading** and the honest modal outcome given self-selected exposure +
  n=1 + physical-only scope + 28 units. It is **publishable** and is never
  upgraded to "suggestive." It constrains the design's own power, not the
  mechanism.

---

*Pre-registration locked 2026-07-04 before any relapse count or any
exposure-versus-relapse relationship was computed or inspected. Faithfully
implements the locked methodology
[`../../../methodology/post_crash_exertion_relapse.md`](../../../methodology/post_crash_exertion_relapse.md)
(DESIGN PROPOSED r3: decisions a to g, the constructed null f-i/ii/iii, the
crash-vs-dip slope interaction f-iv, the power/multiplicity section 4, the
confounds section 5, the falsification framing section 6) and its descriptive
precondition
[`../../descriptive/post_crash_exertion_relapse/precondition.md`](../../descriptive/post_crash_exertion_relapse/precondition.md).
Primary exposure: peak `max_hr_rank_lagged_lcera` (r3 cardiac-strain swap).*

*Lock log: fresh-session peer review
[`../../../reviews/hypothesis-post-crash-exertion-relapse-2026-07-04.md`](../../../reviews/hypothesis-post-crash-exertion-relapse-2026-07-04.md)
returned ACCEPT-WITH-MINOR-REVISIONS, NO-OUTCOME-PEEK HELD, r3 EXPOSURE
RE-CONFIRMED YES, 0 BLOCKING / 0 MAJOR. The five pre-outcome, no-peek-safe
tightenings are absorbed 2026-07-04: (c) the `_lcera` masking resolved to a
definite branch by a pre-outcome extractor fact-check (§4e); (d) the
per-replicate null mechanic spelled out (§6); (b) the autonomic-trend
sensitivity made a definite commitment on named columns with real
danger-window coverage (§4f); the matched-baseline felt-state caliper +
matching ratio + pool sizes operationalised (§4d); the `hr_area` §3.3 scope note
added (§4b). None changed the claim, exposure, window, or primary test, so no
v2. **LOCKED 2026-07-04.** Any change creates a v2. `test.py` and `result.md`
may now be written and run.*

*Cross-refs: methodology MD + methodology review (above); the descriptive
precondition; HA01c (the inherited activity-volume comparison operand +
threshold-monotonicity caveat); HA-P6 / HA-P7 (crash autonomic signature); the
R9 peri-event-recovery card. Literature: `push crash research.md`,
`pacing-and-crash-mitigation.md`, `reviews/pem_recovery_trajectory_review.md`,
the Founder&City 700k-day wearable step-count-confound analysis. CONVENTIONS
§1.2 (reviewer mode), §3.2 (lagged-lcera), §3.5 (no-peek), §3.6 (named counts),
§4.3 (prior-driven = confirmatory); `permutation_null_block_length.md`.*
