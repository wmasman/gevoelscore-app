# Push-crash pipeline handoff (context + state)

**Status**: PM / continuity artefact (2026-07-04), underscore-prefix planning
convention. Consolidates the conversation-level context behind the
post-crash-exertion-relapse ("push-crash danger window") test, so a future
session can pick up the pipeline cold. **NOT part of the fresh-session review
set**: the pre-reg reviewer reviews the pre-reg + methodology MD + precondition
cold (doc-only) to preserve independence, and should NOT read this handoff (it
carries the drafting rationale). This is for the PM / test-runner / continuity.

## 1. What this test is (one paragraph)

After a crash, the felt-state rebounds in ~2-3 days but the autonomic system
settles over ~2 weeks (the R9 dissociation, Radin 2021). During that mismatch
(the **danger window**: felt-recovered, `gevoelscore >= 4`, but autonomically
unsettled, within nadir+10) the PEM threshold, a cardiac/HR threshold (VT1), is
transiently lowered, so a single supra-threshold **peak cardiac-strain spike**
is more likely to trip a **relapse** (new crash/dip within ~4 days) than the
same-magnitude spike at baseline. Primary exposure: peak single-day
`max_hr_rank_lagged_lcera`. n=1, 28 usable crash windows.

## 2. Provenance (how we got here)

R23 (COVID peri-event, MOVED) left one friction point: resting_hr did not move
on the raw scale, only after detrend. That prompted the long-run RHR /
deconditioning thread (driver ledger, decomposition: deconditioning does not
dominate but the LC residual is suggestive-not-established). Along the way R9
characterised the post-crash recovery curves (felt-fast / autonomic-slow) and
the crash-vs-dip autonomic contrast; HA-P6 found a distinctive post-crash
autonomic recovery signature (4/7 channels vs matched controls); HA-P7 found no
recovery-debt compounding. The user then proposed the push-crash hypothesis:
the danger-window mechanism. That is this test.

## 3. The design decisions and WHY (the rationale behind the MD's four-input tags)

The locked design is in `post_crash_exertion_relapse.md` (r3). The
non-obvious rationale, which took discussion to settle:

- **Exertion = physical/cardiac, not mental.** The wearable is blind to
  cognitive/emotional/orthostatic load (the mental-PEM the step-counter misses;
  parked R4). Scope is stated; a relapse with no physical exposure is
  out-of-support, not counter-evidence.
- **Threshold-crossing, NOT sustained over-doing.** An early draft used a
  "sustained >=3 days" exposure. The user corrected it: PEM's evidenced
  mechanism is single-bout threshold suppression (2-day CPET; VT1-as-PEM-
  threshold); the cumulative/dose-accumulation model is clinical-inference-only
  and never physiologically measured (`push crash research.md`). So the primary
  is a single PEAK spike; cumulative is a secondary competing arm (novel: no
  study has pitted the two against each other).
- **Baseline is lagged + era-local (`_lcera`), not fixed, not naive-rolling.**
  PEM is a spike relative to CURRENT capacity, and the envelope shrank sharply
  over the LC era (the deconditioning finding: ~15kg / VO2Max 52->37). A fixed
  baseline mis-scales; a naive rolling one rebases into the ramp (CONVENTIONS
  §3.2). The [d-90,d-30] window self-cleans against the INDEX crash but can
  straddle a NEIGHBOURING crash in the dense 2023-24 era -> mask crash/dip days
  from the baseline.
- **Primary exposure = cardiac strain (`max_hr_rank`), not activity volume
  (`eff_exertion`).** An external critique (Founder&City 700k-day wearable
  analysis) showed step count / activity volume measures "how much someone
  walks, not how they walk" (PEM cases need ~50% more cardiac work for identical
  walks). This bites hardest here: the PEM threshold is a cardiac threshold,
  lowered in the danger window, so it is crossed at LOWER activity volume -- an
  activity-volume exposure under-detects exactly the threshold-crossings that
  matter. The two axes diverge (danger-window rho +0.42), so `eff_exertion` is
  kept as a COMPARISON arm and the strain-vs-volume divergence is the in-sample
  test of the confound. `hr_area` (the HR integral) is the cumulative-strain
  secondary, NOT the primary, because it sweeps up the danger-window autonomic
  arousal (conflation); a peak-HR SPIKE is activity-driven and cleaner.
- **The exposure is CONTINUOUS (peak dose-response), not binary.** The
  precondition found a binary ">=1 day >=0.75" is degenerate (86% exposed, no
  contrast) -- the pacing-confound is inverted (exposure is ubiquitous, not
  censored). The continuous peak (median 0.95, gradient 0.50-1.00) restores
  contrast and dodges HA01c's threshold-monotonicity trap.
- **The null is a CONSTRUCTED matched baseline, event-level.** The methodology
  review's load-bearing catch: "more likely than baseline" needs a constructed
  baseline. It is equal-magnitude peak-strain days OUTSIDE any danger window,
  matched on strain-rank band + LC-era epoch + comparable felt-state trajectory
  (RTM control). The permutation is EVENT-LEVEL (28 units, not ~1700 days) with
  an ACF readout + E[L]* companion.
- **Crash-vs-dip is a formal slope interaction**, base-rate-conditioned, with
  the 2.7x power asymmetry (79 dips vs 28 crashes) stated, so specificity is not
  confounded with power.
- **Reverse-causation is irreducible.** The felt-recovered gate is the only
  ordering sensor and it LAGS the autonomic state (by the design's own premise),
  so a prodromal relapse can suppress activity before the felt-state descends.
  Named as a directional bias; an autonomic-trend exclusion sensitivity is
  added.

## 4. Data facts that matter (for the test-runner)

- Surface: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05).
- Events: 29 crash episodes (`crash_episode_id` + `is_crash`; nadir =
  min-gevoelscore day), 79 dips (`is_dip`, transient single days). 28 crashes
  have a felt-recovery day; coverage 100% on the strain columns in the windows.
- PRIMARY `max_hr_rank_lagged_lcera` (cov 235/236 in windows; peak median 0.95);
  COMPARISON `eff_exertion_rank_lagged_lcera`; CUMULATIVE `hr_area_above_daytime_baseline_waking_lcera`.
  Column-name gotchas: it is `eff_exertion_...` (abbreviated), not
  `effective_exertion_...`. The `_lcera` variants restrict the lagged baseline
  to LC-era days.
- `eff_exertion_min` ~= intensity minutes (rho 0.985); steps are a distinct axis
  (rho ~0.49); cardiac strain vs activity volume rho ~0.42-0.54 (distinct).
- Weight + VO2Max live in the Garmin dump `userBioMetrics.json` (weight is a
  NESTED object; see [[reference_garmin_weight_vo2max_biometrics]]).

## 5. The honest posture (pre-committed)

28 event-units, n=1, heavy autocorrelation, pacing self-selection ->
**underpowered for anything but a large effect. The primary deliverable is an
estimate with an honest CI, and "cannot resolve" (a null-spanning CI) is the
pre-committed default reading, publishable as an honest limit.** Do not upgrade
a wide CI to "suggestive."

## 6. Pipeline state + next steps

1. DONE: operationalisation aligned; descriptive precondition; methodology MD
   r3; fresh-session methodology review (ACCEPT-WITH-MINOR-REVISIONS, absorbed).
2. IN PROGRESS: pre-registration draft (`hypotheses/post-crash-exertion-relapse/hypothesis.md`),
   reviewer-mode-with-authorization, fresh session.
3. NEXT: fresh-session review of the pre-reg (DIFFERENT session from the draft;
   per [[feedback_pre_reg_writer_role]]) -- and because r3 changed the primary
   exposure, the review must re-confirm the exposure choice cold.
4. THEN: lock the pre-reg (audit-gated commit) BEFORE writing/running test.py.
5. THEN: the test (the only place the outcome is revealed) -> result.md ->
   fresh-session review -> Stage-T translation for the site if it lands.

## 7. Cross-references

- Methodology MD `post_crash_exertion_relapse.md`; precondition
  `../analyses/descriptive/post_crash_exertion_relapse/precondition.md`;
  methodology review `../reviews/methodology-post_crash_exertion_relapse-2026-07-03.md`.
- HA01c (inherited comparison operand), HA-P6 / HA-P7, R9 peri-event-recovery.
- Literature: `push crash research.md`, `pacing-and-crash-mitigation.md`,
  `reviews/pem_recovery_trajectory_review.md`; the external Founder&City
  step-count-confound analysis.
- CONVENTIONS §2.2 / §3.2 / §3.5 / §3.6; `permutation_null_block_length.md`.
