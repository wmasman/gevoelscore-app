# Wearable biometrics as predictors and characterisers of post-exertional malaise: an n-of-1 investigation in Long COVID stabilisation — Addendum I

*Addendum to the 2026-06-05 report, covering work between 2026-06-06 and 2026-06-06. Authored 2026-06-06.*

This addendum extends the original report ([RESEARCH-REPORT.md](RESEARCH-REPORT.md)) with three pieces of work completed after the original cut-off: (a) the locking of a revised operational crash definition (crash_v2) that introduces a sub-threshold dip tier, (b) a re-run of the per-minute stress-spike test (H02b) against this new dip tier, and (c) a re-tagging of the H02b specificity check using crash_v2 labels. A fourth strand — a literature review and detailed protocol for decoding the undocumented Garmin FIT message `unknown_233` to obtain per-minute Body Battery — is summarised here and lives in full in [.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md).

---

## Abstract

The original report (§5) noted that crash_v1, the operational crash definition, mixed mechanisms: 4 of 14 train-era and 10 of 15 validate-era crashes showed no stress-spike precursor, and the H02b specificity check found 32 of 83 false-positive null windows contained a sub-threshold score-3 day that crash_v1 excluded. A refined crash definition was identified as the most promising next step.

This addendum reports the result of that step. **crash_v2** adds a tier-2 `dip` category (single days with `score ≤ 3` whose neighbours score ≥ 4) alongside the unchanged tier-1 `crash` category. A pre-registered slow-recovery filter for tier-1 was empirically removed after the data showed that all 29 crash_v1 episodes already satisfied it — a positive validation of crash_v1's acute condition as a PEM-shape detector.

Applying crash_v2 yielded 29 crashes (identical to crash_v1) and 79 isolated dips, with a striking era distribution: train era 14 crashes / 26 dips (dip:crash = 1.9×); validate era 15 crashes / 53 dips (dip:crash = 3.5×). The dip:crash ratio nearly doubles between eras, consistent with the seven-axis "kind of crash changed" theory developed in the original report. Visual inspection of the labelled timeline surfaced a further phenomenon: dips cluster in time, forming multi-day rough patches (4-3-4-3-4 patterns) that the single-day classification splits into separate events. A descriptive cluster overlay was added — 15 clusters covering 45 of 79 dips (57%), with 10 of the 15 clusters falling in the validate era.

H02b re-run against dips showed a positive but weak spike-precursor signal in both train (+9.1 pp discrimination) and validate (+5.2 pp), failing the strict ≥+15 pp bar but passing the magnitude criterion (median delta +9.3 min train, +7.8 min validate). Crashes show a ~3× stronger train-era signal than dips (+29.9 pp vs +9.1 pp), sharpening the original H02b finding: the spike precursor is specifically a multi-day-crash phenomenon, not a generic bad-day marker. In the validate era, crash and dip discrimination magnitudes have converged, suggesting the residual crashes have lost their distinctive physiological signature relative to dips.

Re-tagging the original H02b specificity check with crash_v2 labels explained 32 of the 83 false-positive spike windows (39%): 20 contain a v2 dip (24%) and 12 contain a crash-adjacent day inside a recovery shadow (14%). The remaining 51 (61%) are spike events that did not precipitate any sub-threshold day — consistent with the original report's framing of the spike as "necessary but not sufficient", now quantified more sharply.

A literature and forum sweep confirmed that the undocumented FIT message `unknown_233` — believed to encode per-minute Body Battery — has not been publicly decoded. A two-path protocol (Garmin Connect REST API for ground-truth labels; FIT decode for durability and offline replay) is pre-registered for the next phase; the API path acknowledges grey-area Terms-of-Service concerns for personal-use access.

A parallel strand of work built a per-day activity-feature layer using personal-baseline-relative percentile-rank metrics (PEM-envelope framing, not athletic-training framing) across four exertion axes. Sensitivity-tested across 13 parameter alternates; the `exertion_class` single-day shock metric is ROBUST while the `push_burden_class` binning was SENSITIVE and was deprecated in favour of the raw `push_burden_7d` count. The first round of pre-registered tests (HA01 + HA02 + HA05 with a 3-day lead-up window) all REFUTED. Re-tested with a 4-day lead-up window motivated by the participant's experiential PEM lag framing ("trigger day, immediate day after still ok, crash sets in day 2 or 3"), **HA01b initially showed +17.3 pp discrimination for validate-era crashes against the rolling 30-day baseline** and was reported as the first SUPPORTED validate-era precursor of the investigation.

**A bundled re-test on a methodologically cleaner lagged 30-90-day baseline (Theme A fix; see §5.9) subsequently refuted this finding.** HA01b-recomputed on the lagged baseline shows only +4.0 pp validate-era discrimination (-13.3 pp delta vs the original rolling result), and the bundled HA02c push-burden test was also refuted (+0.7 pp validate). The original +17.3 pp was substantially a rolling-baseline construction artifact. The honest position after the bundled re-test: **no validate-era physiological precursor has been demonstrated on the cleanest available baseline construction.** The "kind of crash changed" theory's "longer trigger lag" extension softens accordingly; what remains is the train-era H02b stress-spike precursor and the absence of a validate-era counterpart in any waking-hour Garmin metric tested so far. The pre-committed honesty discipline (re-test bundled, bar held at the original level, audit trail dated *before* the rerun ran) functioned as designed, surfacing the artifact in the same session that produced the original claim.

---

## 1. crash_v2 — design and result

### 1.1. Motivation

The original report's §5 ("Discussion: Cross-hypothesis integration") identified two weaknesses in crash_v1 that limited downstream analyses:

1. **Mechanism mixing inside crash_v1.** H02b found that 4 of 14 train-era and 10 of 15 validate-era crash episodes showed no stress-spike precursor. The original report posited that crash_v1 might collapse two distinct mechanisms — sympathetic-overload crashes (with precursor) and a residual subtype without one — into the same label, diluting any precursor signal.
2. **Sub-threshold events outside crash_v1.** The specificity check (H02b §6) found that 32 of 83 false-positive null windows (39%) contained at least one day with score = 3 that crash_v1's strict 2-consecutive-day rule excluded. Some of these were genuine bad days the operational definition treated as noise.

A refined crash_v2 was proposed to address both: separate "real PEM" from "functional bad day" by adding a sub-threshold tier and (initially) requiring a slow-recovery tail to qualify as the strict tier-1 crash.

### 1.2. Pre-registered design

The crash_v2 pre-registration (see [docs/research/garmin/hypotheses/crash_v2-definition/definition.md](garmin/hypotheses/crash_v2-definition/definition.md)) defined two tiers:

- **Tier 1 `crash`** — score ≤ 3 for ≥ 2 consecutive days (identical to crash_v1's acute condition), merged within 3 days, **and** a slow-recovery filter requiring the median score in the 7 days following episode-end to be ≤ 5.
- **Tier 2 `dip`** — a single day with score ≤ 3 whose immediate neighbours both score ≥ 4. Days inside a crash episode or its 7-day recovery shadow are excluded.

A separate `vague_low` tier (score-4-day clusters) was considered and explicitly rejected as overcomplication; score-4 days were rolled into the `normal` category.

Predicted counts before any data inspection: crash 18–25 (down from crash_v1's 29 due to the slow-recovery filter), dip 50–120.

### 1.3. Empirical result

First-pass application yielded **29 crashes and 79 dips**. The crash count was outside the predicted range — flagged by the pre-registration's §4 sanity check.

Inspection of per-episode tail medians revealed why: **every one of the 29 crash_v1 episodes has tail_median ∈ {4.0, 5.0}**. Not a single episode bounced back fast enough to be demoted to dip. The slow-recovery filter was a no-op on this dataset.

This is itself a positive finding. crash_v1's acute condition (score ≤ 3 for ≥ 2 consecutive days) **already only catches PEM-shape events** — episodes are uniformly followed by a multi-day rough tail, none recover within the seven-day window to the participant's typical functional zone (score ≥ 6). The slow-recovery filter was therefore removed from the locked spec (the rationale and the empirical evidence are preserved in §2.1 of the definition file), and tier-1 crash was set to be exactly crash_v1.

The simplified crash_v2 spec accepted on 2026-06-06:

| label | count, 2022-09-03 → 2026-06-05 |
|---|---:|
| `crash` episodes | 29 (= crash_v1; positively validated) |
| `dip` events | 79 (within original 50–120 prediction) |
| `normal` days | majority (~91% of 1,372 days) |

A timeline visualisation ([timeline_v1_v2.png](garmin/hypotheses/crash_v2-definition/timeline_v1_v2.png)) was generated as a visual sanity check; all 29 crashes and 79 dips were confirmed by manual inspection to land on the appropriate score patterns.

### 1.4. Era distribution

The crash_v2 labels expose an era pattern the original report's frequency analysis hinted at but could not formally surface, because crash_v1 alone provided no analytical handle on sub-threshold events:

| era | crashes | dips | dip:crash ratio |
|---|---:|---:|---:|
| 2022-09-03 → 2023-12-31 (train) | 14 | 26 | 1.9 |
| 2024-01-01 → 2026-06-05 (validate) | 15 | 53 | 3.5 |

The dip:crash ratio nearly doubles between eras. The participant has not just fewer sustained crashes but disproportionately more transient single-day rough patches. This is consistent with the original report's "stabilisation pendulum settling" framing (§4): the residual events are not just smaller in magnitude but topologically different — shorter, more isolated, more often surrounded by functional days. The dip tier formalises a category of event the original report could only describe qualitatively.

### 1.5. Dip clusters — multi-day rough patches

Visual inspection of the timeline plot ([timeline_v1_v2.png](garmin/hypotheses/crash_v2-definition/timeline_v1_v2.png)) surfaced a phenomenon the single-day dip framing does not capture: **dips cluster in time**. Patterns such as score 4-3-4-3-4 over a week — three single-day dips alternating with single-day partial recoveries — read experientially as one extended rough patch but classify as three independent events under the per-day spec.

A descriptive cluster overlay was added to `crash_v2` (definition.md §2.3a) without changing the per-day labels. A **dip cluster** is a transitive chain of two or more isolated dips, where each consecutive pair sits within 7 days of each other. Initial application:

| metric | value |
|---|---:|
| Total isolated dips | 79 |
| Dips inside a cluster (size ≥ 2) | 45 (57%) |
| Dips remaining singleton | 34 (43%) |
| Total clusters | 15 |
| Largest cluster (dipcluster-007) | 9 dips across 34 days (2024-03-14 → 2024-04-16) |
| Most recent cluster (dipcluster-015) | 5 dips across 21 days (2026-02-11 → 2026-03-03) |

Era distribution of clusters: 5 in train (covering 13 dips), 10 in validate (covering 32 dips). The cluster pattern is concentrated in the validate era, reinforcing the broader "kind of crash changed" narrative: rough patches in the residual era are protracted and intermittent rather than sustained-low like the train-era crashes.

The cluster overlay is intentionally a descriptive layer rather than a third tier. Downstream analyses can choose to treat each dip independently (the existing H02b-on-dips test does this) or collapse cluster members into single multi-day events (e.g. for future "rough patch duration" analysis). This preserves backward-compatibility with the analyses already run while making the multi-day-rough-patch phenomenon analytically tractable.

---

## 2. H02b on dips — does the spike precursor fire before isolated bad days?

### 2.1. Question and design

Having defined the dip tier, the natural test is whether dips share the spike-precursor signature that H02b documented for crashes. If yes, the precursor is a generic "bad day" marker; if no, it is specifically a multi-day-crash phenomenon.

The test ([docs/research/garmin/hypotheses/crash_v2-definition/scripts/h02b_on_dips.py](garmin/hypotheses/crash_v2-definition/scripts/h02b_on_dips.py)) mirrors the original H02b metric exactly — lead-up max stress spike duration vs 90-day trimmed baseline — and uses the same null sample seed for direct comparability. The only difference is the reference event: 79 single-day dips instead of 29 crash episodes.

### 2.2. Result

Both windows formally refuted by the same strict bar that applied to H02b crashes:

| | crashes (H02b orig) | dips (this work) |
|---|---:|---:|
| Train discrimination (pp) | **+29.9** | +9.1 |
| Train median delta (min) | +16.2 | +9.3 |
| Train lower-quartile delta (min) | +6.8 | +4.7 |
| Train verdict | **SUPPORTED** | refuted |
| Validate discrimination (pp) | −8.2 | +5.2 |
| Validate median delta (min) | +6.7 | +7.8 |
| Validate lower-quartile delta (min) | −0.4 | +2.6 |
| Validate verdict | refuted | refuted |

Three readings of this table are productive:

**(a) Dips have a real but weak precursor signal.** In both windows the median delta is positive and at or above +5 minutes; criterion C (magnitude) passes both windows. The lower quartile is positive in both windows. The signal is in the data, just not strong enough to clear the criterion-A frequency bar or criterion-B discrimination bar.

**(b) Crashes show a ~3× stronger train-era signal than dips.** Discrimination ratio +29.9 pp / +9.1 pp = 3.3×. The spike-precursor finding from the original report is now sharper: not "any bad day has a precursor" but specifically "multi-day crashes have a strong precursor; isolated dips have a weaker one."

**(c) The dip tier is heterogeneous.** The top dips by delta show clear "almost-crash" signatures — 2024-03-30 had an 88-minute lead-up spike (delta +77.6 min vs baseline); 2024-07-11 had +59.5 min; 2026-02-11 had +56.7 min — alongside other dips with flat baselines. The dip tier mixes two subtypes: "almost-crashes" with strong physiological precursors that didn't extend to two days, and "mood-only" dips with no precursor. The aggregate weak signal is the average of these. A sub-tiered dip_v2 would likely surface a clean separation, though this is deferred to future work.

### 2.3. Convergence in the validate era

The most theoretically interesting comparison is the validate-era convergence:

| validate-era metric | crashes (H02b orig) | dips (this work) |
|---|---:|---:|
| discrimination (pp) | −8.2 | +5.2 |
| median delta (min) | +6.7 | +7.8 |

Crash and dip median deltas are essentially equal (+6.7 vs +7.8). Crash discrimination is actually slightly worse than dip discrimination in this era. The "kind of crash changed" theory predicted exactly this: as stabilisation progressed, the distinctive physiological signature of multi-day crashes faded toward the (always weak) signature of isolated bad days. The dip tier didn't change; the crash tier collapsed toward it.

This converts the original report's H02b-trajectory finding (smooth 12-month decay of crash-precursor discrimination from +31.8 pp in mid-2023 to near zero by mid-2024) from a within-class decay into a between-class convergence. Read together: residual crashes look like dips now, in their physiological precursor profile.

---

## 3. Specificity re-tag — what crash_v2 explains

### 3.1. Method

The original H02b specificity check (report §6) found that 83 of 200 null windows (42%) fired the +10-minute spike criterion — "false positives" from a predictor's standpoint. Of these, 32 were tagged `near_miss` (at least one day in the 3-day lead-up or reference day had score = 3, a sub-threshold dip crash_v1 excluded).

With crash_v2 labels available, the natural re-tag is to check, for each false-positive window, whether any day in the window now carries a v2 `dip` label. The re-tag script ([retag_specificity.py](garmin/hypotheses/crash_v2-definition/scripts/retag_specificity.py)) reproduces the same null sample (seed `20260605`) and cross-tabulates the original `near_miss` tag against the new `v2_dip_in_window` tag.

### 3.2. Result

|                     | v2_dip=True | v2_dip=False | total |
|---                  |---:|---:|---:|
| **near_miss=True**  | 20 | 12 | 32 |
| **near_miss=False** |  0 | 51 | 51 |
| **total**           | 20 | 63 | 83 |

The four cells decompose the 83 false positives as follows:

- **20 (24%)** — near_miss and v2_dip. The score-3 day in the window is now formally a v2 dip. crash_v2 turns these "false positives" into real sub-threshold signal that crash_v1 was blind to.
- **12 (14%)** — near_miss without v2_dip. The score-3 day is part of a multi-day crash episode (tier-1) or in a crash's 7-day recovery shadow. These were always real signal but outside the 3-day lead-up window we tested.
- **51 (61%)** — neither near_miss nor v2_dip. The spike fired but no sub-threshold event followed. Three sub-possibilities: tolerated precursors (high stress moments the participant weathered without crashing), activity-induced spikes (the original check found 15 of these; some overlap likely), or stress-signal noise.
- **0 (0%)** — v2_dip without near_miss. Sanity check passed: every v2 dip in a window contains a score-3 day by construction, so near_miss always fires when v2_dip fires.

Combined explanatory rate: **crash_v2 turns 39% (32 of 83) of the original spike "false positives" into real sub-threshold signal.** The original report's interpretation of the spike as "necessary but not sufficient" remains correct in spirit but is sharpened in proportion: ~24% of spike fires correspond to dips, another ~14% to crash-adjacent days, leaving ~61% genuinely above the threshold of action.

---

## 4. unknown_233 decoding — protocol locked

### 4.1. Why this matters

The original report's §7 "Future work" identified per-minute Body Battery (BB) as the most promising untested signal for residual-crash precursor detection, motivated by (a) the ME/CFS literature's consistent finding of "unrefreshing sleep" (a parasympathetic-recharge failure) and (b) the participant's own framing that BB-rise occurrence counts during the day are themselves meaningful. The original Garmin GDPR data dump contains 3 daily BB anchor points (HIGHEST/LOWEST/MOSTRECENT with timestamps) but the per-minute curve that Garmin Connect displays — and which the watch's firmware clearly knows — is hidden in the FIT files in an undocumented message: `unknown_233`, 1,440 records per day, 4-byte payload.

### 4.2. Literature and forum sweep

A focused search across the Garmin developer forums, the FIT-SDK community, GitHub repositories of FIT parsers (`tcgoetz/Fit`, `polyvertex/fitdecode`, `GoldenCheetah/GoldenCheetah`), HarryOnline's community-maintained spreadsheet of undocumented FIT messages, and the ANT developers' forum confirmed that **no public decode of `unknown_233` exists**. The community knows it is there (HarryOnline's sheet lists `mesg_233?` in the "activity" category with a question mark), uses FIT File Viewer to inspect it, and at least one analyst (`dtransposed/kipchoge.py`) whitelists `unknown_233` in fitdecode but strips the unknown fields downstream. A successful decode would be a small but real contribution to the broader community.

Independently, the community-maintained `cyberjunky/python-garminconnect` library exposes a Garmin Connect internal endpoint (`/wellness-service/wellness/bodyBattery/events/{date}`) that returns per-minute BB events for authenticated users. A second project (`sirredbeard/garmin-data-export`) uses this path to claim per-minute BB export, indicating the endpoint is currently functional.

### 4.3. Two-path protocol

A pre-registered protocol covers both paths in parallel, with the API path providing labels for the FIT-decode path. The protocol is locked at [.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md) and an H04b artefact folder is provisioned at [docs/research/garmin/hypotheses/H04b-decode-unknown-233/](garmin/hypotheses/H04b-decode-unknown-233/) (currently empty pending notes-quality work and crash_v2 follow-ups).

Path C (Garmin Connect REST API): authenticate via `python-garminconnect`, pull per-minute BB for a stratified 90-day sample across the 5-year corpus. Provides supervised labels for path B.

Path B (FIT decode): treat the API-derived per-minute BB as labels, test ~12 candidate byte encodings (`b3 = BB direct`, `b2:b3 as scaled int16`, byte-delta variants, off-wrist flag in `b1`, etc.) against the labels. Lock the winning decoder against a pre-registered 180-day holdout. Three "what if nothing works" fallbacks specified: joint-channel regression, state-buffer reframing, raw-stream feature mining.

A grey-area Terms-of-Service concern was identified for Path C (Garmin's general Terms of Use prohibit automated scraping; the internal endpoints are not covered by any documented personal-use API agreement; risk of account suspension is theoretical but nonzero). The participant has accepted the risk for personal-use, own-data analysis with a light footprint (one login, ~90-day pull, then idle). A fallback to UDS daily anchors as sole ground truth is provisioned if the API path becomes unavailable.

### 4.4. Downstream implications

A working decode of `unknown_233` unblocks at least three previously-deferred hypotheses:

- **H03b — overnight Body Battery recharge as a marker of unrefreshing sleep.** Replaces the original report's H03 (sleep efficiency, refuted) and its planned H03b (sharper sleep metrics) with a physiologically sharper measurement: how much BB was actually recovered overnight. Hypothesis: overnight BB recharge is depressed before and during crash periods.
- **H02d — extended lead-up window (7–10 days) for BB-decline precursors.** Complements H02b's stress-spike precursor with a slower-moving BB-drain pattern.
- **A refined crash_v3** that could incorporate biometric corroboration as part of the operational definition (after sufficient cross-validation to avoid circularity).

---

## 5. Activity-labels phase + HA01b — first validate-era precursor

A separate strand of work, parallel to the crash_v2 phase, built a per-day activity-feature layer to test whether exertion patterns predict crashes or dips. The work yielded an iteration history worth recounting (v1 absolute → v2 z-score → v3 percentile-rank → v3.1 deprecating push_burden_class binning), and produced **the first SUPPORTED validate-era precursor** of the entire investigation.

### 5.1. PEM-envelope framing principle (locked)

During spec design the participant articulated a principle that influenced the entire design: **for PEM-pacing metrics, work with deviations from personal baseline, not absolutes**. Every person has their own baseline; PEM is induced by shocks (single-day deviation) or sustained push (multi-day elevation). Athletic training thresholds (e.g. "30 min vigorous = heavy") bake in fitness norms that don't generalise to PEM populations or even adapt within one participant as their envelope shifts. The principle was saved to feedback memory for future work.

This shifted the spec from v1 (absolute thresholds for 3 of 4 axes) to v3 (percentile rank within personal 30-day rolling baseline). The rank-based approach handles zero-heavy distributions robustly (a particular failure mode of z-scores when the personal baseline is mostly zero) and gives uniform thresholds (0.5/0.75/0.85/0.95) that generalise across participants — the personalisation happens in the baseline computation.

### 5.2. Feature layer built

The locked v3.1 spec produces, per day across 2022-09-03 → 2026-06-05:

- **Raw signals**: `total_steps`, `effective_exertion_min` (UDS vigorous + 0.5 × moderate, or recorded duration if higher), `max_hr_uds`, `vigorous_min_uds`, plus passive `moderate_min_uds`, `highly_active_sec`, recorded-activity HR zones, and sparse self-report fields.
- **Percentile ranks against personal 30-day baseline**: `step_rank_30d`, `effective_exertion_rank_30d`, `max_hr_rank_30d`, `vigorous_min_rank_30d`.
- **Single-day exertion class**: `exertion_class` ∈ {none, light, moderate, heavy, very_heavy}, the max class across the four rank axes.
- **Push burden** (sustained-push detector): `push_burden_7d` = count of days in last 7 with effective_exertion_rank_30d ≥ 0.75. Range 0-7.
- **Above-baseline streak**: consecutive days above median.

An important empirical finding from the data audit: **the UDS daily passive intensity-minutes channel is the unified exertion-load measure** — empirically (verified on 191 days with recorded activity) `UDS vigorous_min ≥ Σ recorded vigorous_min` in 100% of cases, with a mean overshoot of ~2.7 min. So a single UDS channel captures both deliberate workouts and unrecorded exertion (cleaning, gardening, social events) without double-counting. This sidesteps a recurring H02b caveat about unrecorded exertion leaking into stress samples.

Distribution under v3.1:
- exertion_class: 26.5% none, 23.6% light, 15.5% moderate, 17.4% heavy, 17.1% very_heavy
- push_burden_7d: 17% rest weeks (0 push days), 30% with 1, 26% with 2, 18% with 3, 9% with 4+, 2% with 5+

### 5.3. Sensitivity test (script 07)

Before any crash-vs-activity analysis, the v3 spec was sensitivity-tested across 13 parameter alternates (baseline window 14-60d, push window 5-14d, push threshold 0.65-0.85, class cutoffs softer/stricter). Locked pre-test verdict rule: ROBUST if Jaccard ≥ 0.7 vs reference across all alternates; SENSITIVE if any < 0.5.

Key findings:
- **`exertion_class` heavy+very_heavy is ROBUST** across all four dimensions (min Jaccard 0.78).
- **Spearman rank correlation 0.957-0.985** across baseline windows — the underlying ranking is extremely stable. The choice of class boundaries is what introduces sensitivity, not the ranking itself.
- **`push_burden_class very_heavy` binning is SENSITIVE** — Jaccard 0.04-0.32 across push_window and push_threshold variations. The integer threshold (≥5 in a 7-day window) was brittle at the distribution tail.

The sensitivity test caught the brittleness *before* any downstream test ran on it. **The class binning was deprecated**; downstream tests use the raw `push_burden_7d` count directly. The underlying metric is stable; the artificial threshold was the problem. This is exactly the kind of methodological discipline the test was designed to enforce.

### 5.4. HA01 + HA02 + HA05 (3-day window) — all REFUTED

The first round of pre-registered tests used the same 3-day lead-up window as H02b for direct comparability:

| test | metric | train | validate |
|---|---|---|---|
| HA01 (single-day shock) | n_shock_days in [D-3, D-2, D-1] | +0.7 pp (refuted) | +11.5 pp (refuted) |
| HA02 (push burden) | max push_burden_7d in lead-up | −1.5 pp (refuted) | 0.0 pp (refuted) |
| HA05 (crash vs dip ratio) | discrimination ratio | crashes weaker than dips (ratio 0.08x) | n/a |

The HA01 result was particularly striking: with 34% of days as heavy or very_heavy, random 3-day windows have ~68% chance of containing at least one such day. Crash lead-ups had ~69%. Essentially no discrimination.

The HA05 surprise: **dips showed more activity-shock signal than crashes** at the 3-day window (+9.3 vs +0.7 pp train). Echoed the H02b-on-dips finding that dips contain a heterogeneous mix of subtypes, some of which are exertion-related.

### 5.5. HA01b + HA02b + HA05b (4-day window) — HA01b validate SUPPORTED

The participant's experiential PEM lag framing — "trigger day, the immediate day after is still ok, the crash sets in on the second or third day, and may worsen for 1-2 more" — motivated a wider lead-up window. The 3-day test missed triggers occurring 4 days back. Pre-registered as a new test (same bar) with `[D-4, D-3, D-2, D-1]` window.

This is theory-driven not post-hoc rescue — the same pattern as H02 → H02b being motivated by "intense moments trigger crashes."

| test | metric | train | validate |
|---|---|---|---|
| **HA01b (4-day shock)** | n_shock_days in [D-4..D-1] | +8.6 pp (refuted, N=13 underpowered) | **+17.3 pp SUPPORTED ✓** |
| HA02b (4-day push burden) | max push_burden_7d in lead-up | −6.0 pp (refuted) | +2.2 pp (refuted) |
| HA05b (crash vs dip ratio) | discrimination ratio | crashes 1.57x stronger than dips | n/a |

**HA01b for validate-era crashes clears all three pre-registered criteria**: 93.3% of validate crashes have heavy/very_heavy exertion in the 4-day lead-up (vs 76% null), discrimination +17.3 pp (clearing the +15 pp bar), and the magnitude criteria (median 2 shock days, lower quartile 1).

This is the **first SUPPORTED validate-era precursor** across the entire investigation. All H01-H05 + H02b were either train-only-supported or refuted-both; HA01b is the first to clear the validate bar.

### 5.6. Interpretation

The original report concluded "for residual crashes, the daily-aggregate biometric channel is closed." That conclusion was based on 3-day lead-up windows across H01-H04 and H02b. **HA01b reopens it: the channel is open at the 4-day lag**.

The "kind of crash changed" theory gains a new dimension: the change may not be "no precursor" but **"longer lag."** Train-era H02b had a strong 3-day stress-spike precursor; validate-era HA01b has a strong 4-day activity-shock precursor. Two different precursor mechanisms at two different lags across two different eras — but both empirically supported.

A plausible explanation: as the participant has stabilised, the body's response to exertion has slowed. The 3-day lag of the train era reflected an under-recovered system where exertion produced rapid sympathetic-arousal-driven crashes; the 4-day lag of the validate era reflects a better-paced system where exertion still triggers crashes but through a longer-developing mechanism. This is consistent with the pacing literature's "energy envelope" framing — staying within the envelope produces no crashes; brief excursions outside it produce delayed PEM with individual-variable lag.

HA02b's null result (push burden does not predict crashes at either window) is also informative: **the mechanism is acute shock, not sustained push**, at least at this resolution. The "push-crash" narrative the pacing literature emphasises may be more about cumulative energy debt at finer-than-daily timescales, or about cognitive/emotional load not captured by activity metrics.

### 5.7. Exploratory lag profile + per-axis decomposition

After HA01b's positive result, a post-hoc lag profile was computed sweeping the lead-up window from 2 to 7 days. The signal traces a clean curve: weak at 2-3 days, strong at 4-5 days, declining past 6.

| window | train crash disc | validate crash disc |
|---:|---:|---:|
| 2d | +8.5 pp | +0.3 pp |
| 3d (HA01) | +0.7 pp | +11.5 pp |
| 4d (HA01b SUPPORTED) | +8.6 pp | +17.3 pp |
| 5d | +15.3 pp | +23.0 pp |
| 6d | +6.3 pp | +14.0 pp |
| 7d | −2.2 pp | +5.5 pp |

The empirical peak sits at 5 days for both windows (train +15.3 pp would clear the bar; validate +23.0 pp clears comfortably). **This is an exploratory finding, not a pre-registered SUPPORTED test.** Selecting "the window that gave the strongest signal" post-hoc is exactly the kind of analysis-flexibility that pre-registration discipline aims to prevent. We withhold the "SUPPORTED" verdict at 5-day; a pre-registered HA01c with the 5-day window on genuinely new data (additional participants, extended time window) would be the right confirmation path.

The descriptive characterisation remains useful: **the empirical PEM lag distribution for this person peaks around 5 days**, with meaningful signal in the 4-6 day window. Any retrospective card should reference this lag range — the original 3-day window common in PEM literature is too short for this person's residual crashes.

A per-axis decomposition at the 4-day window identifies the dominant driver:

| axis | train disc | validate disc |
|---|---:|---:|
| **A — effective_exertion_min** | **+32.4 pp** | **+17.4 pp** |
| B — total_steps | +22.0 pp | +15.3 pp |
| C — max_hr peak | +4.5 pp | +12.9 pp |
| D — vigorous_min | +0.8 pp | +17.4 pp |

The UDS-derived `effective_exertion_min` (passive intensity-minutes + recorded duration) is the dominant single-axis signal. Single-axis discrimination on train (+32.4 pp) is *stronger than the multi-axis composite* (+8.6 pp) — because the composite's max() rule mixes in less-informative axes that dilute the signal. The "exertion-minutes" channel alone is the cleanest precursor; the multi-axis composite is more PEM-safe (catches more day types) at the cost of precision. This too is exploratory and informs future spec choices (whether to use composite vs single-axis in production card logic).

### 5.8. Implications for feature design

The b2 retrospective card concept gains empirical grounding:
> "Looking back at your crash starting [date]: 3 of the 4 days before it had exertion classified as heavy or very_heavy. What was happening then?"

Fires on ~93% of validate-era crashes. The PPV is modest (76% null baseline means many heavy-exertion days don't precede crashes), so this is **not** a predictive feature — it's a retrospective surface. Paired with card (b) (the H02b spike retrospective for train-era crashes), the two cards together cover both eras with distinct empirical precursors.

Lag range to reference in card copy: 4-6 days (exploratory peak at 5). Don't claim the 5-day window is statistically confirmed; do let the lag range inform the card's "we looked at the X days before this crash" framing.

A new motivation also surfaces for dip subtyping: HA01 at 3-day showed dips with stronger activity-shock signal than crashes (+9.3 vs +0.7 pp). The dip tier likely separates an "exertion-triggered" subtype from a "mood-only" subtype. A dip_v2 split using HA01-style flagging may surface this; deferred until after H04b unlocks BB as a corroborating signal.

### 5.9. Theme A bundled re-test — honest accountancy on the validate-era precursor

After the original HA01b SUPPORTED finding was reported, a methodological critique surfaced: the 30-day rolling baseline used to compute `effective_exertion_rank_30d` includes the recent candidate region in its reference frame. A sustained creep rebases itself into its own baseline, so push burden's discriminative power is least where the risk is highest, and HA01b's rank-based shock detector inherits the same contamination at a different timescale. The full diagnosis lives in [activity-labels/spec/severity_spec.md §Lagged baseline (v3.2)](garmin/activity-labels/spec/severity_spec.md).

Two complementary fixes were locked on 2026-06-06, *before* any rerun ran:

- **A.1 (lagged baseline)**: each rank axis recomputed against days `[d-90, d-30]` — a 60-day window ending 30 days ago that excludes the recent candidate region. Push burden's reference frame no longer overlaps with the very window it is being asked to evaluate.
- **A.2 (trend slope)**: OLS slope of `log(1 + effective_exertion_min)` over the trailing 28 days, surfacing the creeping-floor pattern as a first-class metric rather than letting it absorb into the baseline.

A bundled re-test was pre-registered on the new lagged baseline:
- **HA02c** — push burden on lagged baseline → crash (the original HA02 hypothesis, now on a clean reference frame)
- **HA01b-recomputed** — the original HA01b hypothesis, same 4-day lead-up window, recomputed against the lagged ranks

The pre-committed SUPPORTED bar was *the same as the original* (frequency ≥ 60%, discrimination ≥ +15 pp). Re-testing only the refuted hypothesis while keeping the supported one as-is would be selective rescue and violate symmetric re-test discipline — both tests therefore ran on the same reference frame, evaluated together, with the audit trail recording A.1's motivation *before* any rerun result existed (the anchor against motivated rescue).

The result: both hypotheses refuted on the lagged baseline.

| test | window | rolling (original) | lagged (recomputed) | delta | verdict |
|---|---|---:|---:|---:|---|
| HA01b validate crash | 4-day | **+17.3 pp (SUPPORTED)** | +4.0 pp | -13.3 pp | REFUTED |
| HA01b train crash | 4-day | +8.6 pp | +5.8 pp | -2.8 pp | REFUTED |
| HA02b/c validate crash | 4-day | -7.4 pp | +0.7 pp | +8.1 pp | REFUTED |
| HA02b/c train crash | 4-day | -2.0 pp | -18.7 pp | -16.7 pp | REFUTED |

A sample caveat: 3 of 14 train crashes fell inside the 90-day lagged-rank boundary at corpus start and were dropped from the train-side test (the validate side has all 15 crashes clean). The verdict is not rescued by the dropped train crashes — even validate alone is refuted.

The honest interpretation: the original **+17.3 pp validate-era HA01b finding was substantially a rolling-baseline construction artifact.** What HA01b was probably catching is *short-window relative heaviness* ("today's exertion exceeds the immediate recent past") rather than *long-window relative heaviness against a stable envelope reference*. These are physiologically different constructs. The short-window pattern may still be real and useful for pacing — but it is not the cumulative-erosion / sustainable-floor construct push burden was meant to operationalise, and it does not survive the symmetric pre-registered re-test on a clean baseline.

HA02c is genuinely refuted on both baselines: push burden is not a precursor for this person on either reference frame. Theme A improves push burden's measurement-theoretic standing but does not resurrect it as a predictor.

Three implications:

1. **The "kind of crash changed" theory's "longer trigger lag" extension does not hold up.** §5.6's claim that train-era H02b at 3-day stress-spike pairs with validate-era HA01b at 4-day activity-shock is partly an artifact of the rolling baseline; on a clean baseline, the validate-era counterpart vanishes. The §5.8 "card concept (b2)" empirical anchor is gone. The two-mechanism / two-lag story softens to: train-era crashes had a precursor (H02b); validate-era crashes do not have a measurable precursor in any waking-hour Garmin metric tested so far.
2. **The single-mechanism-two-regimes reframe becomes harder to support.** If validate-era crashes have no measurable physiological precursor, the "same threshold, different dominant pathway" reading needs new empirical anchors. The most defensible position now is: validate-era crashes look like dips physiologically, and we have not yet found a signal that distinguishes them from random non-crash windows.
3. **Morning resting-HR delta (a candidate H06-shape test, gated on its own pre-registration) becomes more important, not less.** It is the only remaining waking-hour-adjacent candidate for a validate-era precursor, and unlike the rank-based shock detectors it operates on a physiological quantity (overnight autonomic recharge) with strong external evidence in the pacing literature (Workwell, Bateman Horne). If a morning-RHR-delta test also fails to fire on validate-era crashes, the honest position becomes that validate-era crashes are precursor-invisible in everything Garmin captures from waking-hour signals — and the next direction shifts to overnight recovery (gated on H04b unlocking per-minute Body Battery).

The methodological lesson banked: when a baseline-relative metric posts an unusually strong validate-era result against a long literature of negative findings, default to skepticism and pre-register a clean-baseline re-test before the result enters synthesis. The pre-commitment is what kept the audit trail clean.

### 5.10. H02d — stress-spike re-test under sentinel + window corrections

Independently of the Theme A re-test, a parallel methodological re-evaluation of the stress channel (H02d) ran on 2026-06-06 — pre-registered at [H02d-stress-spikes-uncensored/hypothesis.md](garmin/hypotheses/H02d-stress-spikes-uncensored/hypothesis.md), result at [H02d-stress-spikes-uncensored/result.md](garmin/hypotheses/H02d-stress-spikes-uncensored/result.md). H02d addressed two operationalisation gaps in H02b that were both biased *against* finding signal in the validate era:

1. **Sentinel collapse.** Garmin emits stress = −1 / −2 in two physically distinct cases (watch off-wrist vs watch on-wrist during "too active" moments — the HRV-stress algorithm censoring extreme arousal). H02b dropped both. An 8-file stratified calibration ([calibrate_sentinel_hr_result.md](garmin/hypotheses/H02b-stress-spikes/calibrate_sentinel_hr_result.md)) showed 100% of sentinels have an HR sample within ±60s; sentinels even have *better* HR coverage than valid stress samples — confirming "too active" is the dominant cause and "off-wrist" is rare. H02d's primary arm imputes "too active" as ≥75 for spike continuity; a bridge-only sensitivity arm runs alongside.
2. **Lead-up window.** H02b used `[D−3, D−1]` for cross-comparability with H02; the post-H02b lag profile peaks at 5 days. H02d uses 4-day primary (matching HA01b) and 5-day secondary.

**Result: H02d refuted overall** by the locked rule, but with two distinct findings under the refutation:

- **Sentinel imputation made the metric over-sensitive.** ~159 "too active" samples/day on average — flat-imputing all of them as ≥75 was too generous; both crash and null hit ~85% above the +10-min threshold. The censored-arousal idea is not killed, but the specific "treat ALL too_active as 75-stress" operationalisation is; an H02e candidate is queued to filter by HR magnitude (impute only when nearby HR ≥ ~100 bpm).
- **Window extension confirmed the lag profile cleanly in train.** Bridge arm (= H02b censoring logic) shows smooth monotonic train discrimination 3d → 4d → 5d: **+29.9 → +27.6 → +31.8 pp.** Bridge × 5d at **+31.8 pp is the strongest train-era single-channel signal of the entire project**, surpassing H02b's +29.9 pp. Train bridge × 5d clears all three criteria; train bridge × 4d clears them too. Both are train-SUPPORTED in isolation, overall-REFUTED by the validate fail.
- **Validate refuted in all four arms** (imputed × {4d, 5d}, bridge × {4d, 5d}). Validate discrimination ranges from −8.7 pp (imputed_4d) to +9.0 pp (bridge_4d); none clear +15 pp. **Five tests on the stress channel are now consistent on validate refutation** (H02 daily-avg, H02b 3d, H02d × 4 arms).

### 5.11. Where this leaves the conclusion

Reading §5.9 (Theme A activity-shock re-test) and §5.10 (H02d stress-spike re-test) together — both run on 2026-06-06, methodologically independent, both pre-registered with their methodological corrections motivated *before* the reruns ran — the consolidated picture for validate-era precursors on waking-hour Garmin signals:

- **Activity-shock channel** (HA01b family): the +17.3 pp original was a rolling-baseline artifact; refuted at +4.0 pp on lagged.
- **Stress-spike channel** (H02 / H02b / H02d): refuted in validate across five tests including H02d's methodological corrections (sentinel handling + wider window).
- **Push burden** (HA02 / HA02c): refuted on both baselines.
- **No waking-hour Garmin metric has demonstrated a validate-era precursor under methodologically clean pre-registration.**

Two convergent positives also emerge:

- **The 4-5 day lag is cross-channel confirmed.** H02d bridge train monotonic 3d → 4d → 5d (+29.9 → +27.6 → +31.8) and HA01b's lag profile (peak at 5d validate +23.0 pp on rolling) both point at the same lag. Independent of which channel survives a clean re-test, the empirical lag for this person centres at ~5 days, not 3.
- **Train-era stress-spike precursor is robust and gets stronger under correct windowing.** H02b train (+29.9 pp at 3d) is now joined by H02d bridge train (+31.8 pp at 5d) as the strongest train-era single-channel signals of the project. The pre-cliff stress-spike precursor is well-replicated; H02d's bridge × 5d per-episode table is the cleanest illustration of "an intense moment in an otherwise calm day can trigger a crash" for the 2022-23 era.

**Net change to "what's been SUPPORTED":** the investigation now has **two train-era SUPPORTED precursors** (H02b 3d; H02d bridge × 5d), both overall-REFUTED by their validate fails; **zero overall-SUPPORTED precursors** under clean methodology (HA01b's original SUPPORTED status withdrawn per Theme A). The implication for HA06 sharpens: it is the only remaining waking-hour candidate, and unlike the stress and activity channels it operates on a physiological quantity (overnight autonomic recharge) where validate-era convergence with train-era residue would be the strongest pre-registerable empirical stake for the D7 single-mechanism-two-regimes reframe.

## 6. Discussion — sharpened "kind of crash changed" narrative

Integrating these new findings with the original report's seven-axis framework, the "kind of crash changed" theory now has **nine directional findings on independent axes** and one cross-class convergence finding:

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | yes → no |
| stress precursor (spike count) | H02b | strong yes → weaker |
| crash depth (score nadir) | K01 | late shallower (no score-1) |
| crash duration (span) | K02 | late shorter (long-tail 5→1) |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late mixed-day +39 pp |
| lead-up language | notes v2 | late less warning, more cognitive |
| **dip:crash ratio (new)** | **crash_v2** | **1.9× → 3.5×** |
| **dip cluster concentration (new)** | **crash_v2 cluster overlay** | **5 clusters / 13 dips train → 10 clusters / 32 dips validate** |
| **crash precursor vs dip precursor (new)** | **H02b on dips** | **3× ratio in train → 1× in validate** |
| **activity shock at 3-day lag (new)** | **HA01 3-day** | **+0.7 pp train (refuted), +11.5 pp validate (refuted)** |
| **activity shock at 4-day lag, rolling baseline (new)** | **HA01b 4-day rolling** | **+8.6 pp train (refuted, N=13), +17.3 pp validate (originally SUPPORTED — see footnote)** |
| **activity shock at 4-day lag, lagged baseline (new, see §5.9)** | **HA01b-recomputed + HA02c** | **+5.8 pp train, +4.0 pp validate — REFUTED on cleanest baseline; the +17.3 pp was largely a rolling-baseline artifact** |
| **lag length (revised after §5.9)** | **H02b vs HA01b-recomputed** | **3 days (train, stress) → no measurable validate-era precursor on cleanest baseline** |

The dip-tier finding extends the theory in a way the original report could not: residual events are not just smaller versions of the original crashes; they are increasingly transient single-day events, with the multi-day crashes themselves having lost their distinctive physiological signature relative to dips. The participant's residual eventscape is dominated by isolated bad days that the original crash_v1 framework treated as noise.

This has direct implications for the gevoelscore app's planned features:

- **The stabilisation-arc card** (original report §6, Tier 1a) is reinforced. The dip-tier formalises an additional axis of recovery characterisation: not just "fewer crashes, shorter, shallower" but "events are increasingly transient and isolated."
- **The per-crash retrospective card** (original report §6, Tier 1b) extends naturally to dips. A retrospective card framed for a single bad day — "your stress was elevated for 30 minutes on the day before this dip" — would fire on the ~24% of dips with strong precursors. Honest framing distinguishes these from the ~76% without.
- **A possible dip-subtyping feature** (new). The "almost-crash" subtype within the dip tier — identified by strong physiological precursor — may merit its own retrospective surface, distinct from "mood-only" dips. This depends on a dip_v2 split that the current work flags but does not implement.

---

## 7. Methodology notes

Two methodology-discipline observations carried forward from the original report's §6:

**The §4 sanity-flag worked.** The pre-registered prediction of "18–25 crashes" was wrong (actual: 29). The empirical 0-demotion finding refuted the prediction and the slow-recovery filter was removed before any downstream analysis ran. The original report's call to "pre-register on both median and mean" (K01 / K02 lesson) and "do a small dry-run before locking a spec" (H03 / H05 lesson) was honoured here in a different form: the sanity-flag served as the dry-run equivalent for a definition rather than a metric.

**Spec-tied-to-data discipline.** The recovery filter was preserved as text in the definition.md as a documented hypothesis that the data refuted, not silently removed. Future re-runs on expanded datasets that surface fast-bounce 2-day lows should re-introduce the filter as `crash_v3` (a separately versioned, separately re-applied definition) rather than silently revising v2. This is consistent with the original report's "honest verdict categories" requirement.

A new methodology observation: **the visual sanity-check on classification labels matters.** A multi-row timeline plot ([timeline_v1_v2.png](garmin/hypotheses/crash_v2-definition/timeline_v1_v2.png)) caught no errors, but the act of inspection itself adds confidence that no algorithmic edge case mis-classified events. For multi-label classification work on time series, a visual layer should be standard alongside per-class counts and per-day labels.

---

## 8. Next steps

The original report identified five next-step directions (§7). Updates:

1. **crash_v2 (now complete).** No further work on the definition; downstream analyses pending.
2. **Dictionary v3 — polarity negation handling.** Unchanged status (deferred).
3. **H02b sensitivity grid (H02c).** Unchanged status (deferred).
4. **H03b — sharper sleep metrics.** Superseded by H03b-via-BB-recharge (gated on H04b success).
5. **HRV-on-rest channel investigation.** Subsumed under H04b path B's joint-channel regression fallback.

New strands queued:
- **Notes label-quality work** (participant-requested). To precede any v3 notes categorisation across crash, dip, and normal day-types.
- **H04b execution.** Folder structure and protocol locked; execution gated on notes label-quality work completing.
- **Dip subtyping (dip_v2).** Identifying the "almost-crash" vs "mood-only" subtypes by physiological precursor. Deferred to after H04b unlocks per-minute BB as a candidate corroborating signal.
- **Cluster-based analyses.** With 15 dip clusters now identified, "rough patch duration" and "rough patch precursor" become testable concepts. Cluster spans range from 3 to 34 days. The longest cluster (2024-03-14 → 2024-04-16, 9 dips) coincides with a period worth retrospective inspection of context (notes, calendar) — a candidate exercise for the eventual notes label-quality work.
- **A retrospective per-dip card concept**, conditional on dip_v2 surfacing a defensible split.
- **A retrospective rough-patch card concept**, building on the cluster overlay: "between 14 March and 16 April you had 9 dips clustered together — what was happening that month?"

---

## 9. Acknowledgement of limitations

This addendum compounds the original report's n-of-1 limitation: one participant's data, one Forerunner 245's firmware-versioned algorithms, one 3.7-year window straddling a stabilisation transition the participant's own recovery shaped. No claims are made about ME/CFS or Long COVID at the population level; no claims are made about the generalisability of crash_v2 to other patients. The work is descriptive of one trajectory, and even within that trajectory, this addendum's findings (particularly the "dips are heterogeneous" reading and the validate-era crash-dip convergence) lean on small N: 29 crashes and 79 dips across the full corpus, with finer slices supporting era splits and subtype hints.

The crash_v2 definition is locked at this revision. Future re-runs on expanded data (additional participants in future research, extended time windows) may require a `crash_v3` revision — the slow-recovery filter, in particular, could fire on patient populations whose acute condition is less reliably PEM-shape than this participant's appears to be.

---

*Addendum locked 2026-06-06. Original report at [RESEARCH-REPORT.md](RESEARCH-REPORT.md). Next phase work tracked in [docs/research/garmin/hypotheses/](garmin/hypotheses/) and [.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md).*
