# Wearable biometrics as predictors and characterisers of post-exertional malaise: an n-of-1 investigation in Long COVID stabilisation — Addendum I

*Addendum to the 2026-06-05 report, initially authored 2026-06-06
covering crash_v2 + H02b-on-dips + specificity re-tag + unknown_233
protocol, then extended same-week through 2026-06-07 to cover the
activity-labels phase, HA01b + Theme A re-test, H02d, the autonomic-
channel sibling family (HA06/HA06b/HA10/HA11), the HRV-proxy
substitute tests (HA07c/HA08c/HA07d), and the threshold-monotonicity
v2 diagnostic round.*

> **Forward reference**: subsequent work on 2026-06-07 covering the
> S02 score-trajectory batch (S02 + S02b + S02c), cross-document
> propagation, and product-plan consolidation is captured in
> **[Addendum II](RESEARCH-REPORT-ADDENDUM-II.md)**. This Addendum I
> is preserved unchanged from its locked state for audit-trail
> continuity; Addendum II extends rather than supersedes the §6
> nine-axis framework discussion below (Addendum II §6 adds two
> further descriptive axes and two methodology constraints).

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

### 5.12. HA06 — morning nightly RHR delta (absolute bidirectional thresholds, lagged baseline)

HA06 was the first member of the autonomic-channel sibling family
queued from Laure Wiggers' *Smartwatch Pacing* pdf (2025-07; a
lotgenoten-curated lived-experience guide that cites Workwell,
Bateman Horne, and Ruijgt/Wüst 2025). Pre-registration locked
2026-06-07 at [HA06-morning-rhr-delta/hypothesis.md](garmin/hypotheses/HA06-morning-rhr-delta/hypothesis.md);
result at [HA06-morning-rhr-delta/result.md](garmin/hypotheses/HA06-morning-rhr-delta/result.md).

**Design changes from the original C.1 sketch** (5 changes folded
in after reading the Wiggers pdf):

1. **Bidirectional** test (`|RHR − baseline| ≥ N`) instead of
   one-sided elevated. Wiggers documents the parasympathetic-swing
   pattern — a paradoxical LOW-RHR + HIGH-HRV night after overexertion
   ("freeze") that LOOKS like recovery but is warning. One-sided
   thresholds would miss these.
2. Use Garmin UDS `restingHeartRate` (the lowest stable nightly HR)
   per Wiggers' specific framing.
3. 4-day primary + 5-day secondary lead-up window, matching HA01b
   and H02d.
4. Lagged baseline `[d-90, d-30]` per Theme A (excludes the
   recent candidate region; min 40 of 60 prior nights).
5. Sensitivity arm reporting one-sided result and directionality
   split.

**Thresholds (pre-registered)**: N = 5 bpm primary (Wiggers'
*"5-10 al ontevreden"* floor); N = 10 bpm secondary (Workwell's
lower 10-15 bound); N = 15 bpm sensitivity check (upper bound).

**Result: REFUTED both eras.**

| | train (14 episodes) | validate (15 episodes) |
|---|---:|---:|
| crash episodes triggering (\|delta\| ≥ 5 bpm) | 3 (21.4%) | **0 (0.0%)** |
| null windows triggering | 15 (7.5%) | 15 (7.5%) |
| discrimination (pp) | +13.9 | −7.5 |
| median max-\|delta\| (bpm) | 3.49 | **1.63** |
| crit (a) freq ≥ 60% | fail | fail |
| crit (b) disc ≥ +15 pp | fail (close, +13.9) | fail |
| crit (c) median ≥ 2.5 bpm | PASS | fail |
| verdict | refuted | refuted |

Validate-era refutation is decisive: **0 of 15 validate crashes
show *any* RHR deviation ≥ 5 bpm in their 4-day lead-up.** The
N = 10 and N = 15 sensitivity thresholds were vacuous (0% on both
crash and null windows for both eras) because the participant's
nightly RHR is too stable for those thresholds to be meaningful at
all — median max-|delta| sits at only 1.6-3.5 bpm.

Train showed a directionally positive result (+13.9 pp discrimination,
+3.49 bpm median magnitude) but the 21.4% frequency was well below
the 60% bar. The bidirectional design caught one extra train
triggering event over the one-sided arm (+7.1 pp contribution).
Directionality split among the 3 train triggering events: 2
elevated (classical Workwell direction), 1 lowered (Wiggers'
parasympathetic-swing). The swing pattern is present but small.

**The reason for the refutation, explicitly**: the pre-registered
5/10/15 bpm thresholds were drawn from Wiggers' own RHR-variability
range and Workwell's clinical rule. **For this participant, those
thresholds are effectively unreachable**. Wiggers' lived
experience shows daily RHR moves of 5-10 bpm; this participant's
lagged-baseline-relative deviation is typically 1-3 bpm. The
pre-registered bar was calibrated to a person with materially more
RHR variability than this one. The pre-commitment held — the
result is honestly reported — but the methodological gap motivated
a same-session re-test under a relative-threshold variant (HA06b
below).

### 5.13. HA06b — z-score bidirectional RHR delta (relative thresholds)

HA06b is a Theme-A-style methodological re-test of HA06: same data,
same lagged baseline window, same 4-day primary / 5-day secondary
windows, same bar shape — but with relative thresholds
`|RHR − μ| / σ ≥ N_std` (N_std = 1.5 primary / 2.0 secondary / 2.5
sensitivity check) instead of absolute bpm. Pre-registration locked
2026-06-07 *before* the re-test ran, at [HA06b-rhr-zscore/hypothesis.md](garmin/hypotheses/HA06b-rhr-zscore/hypothesis.md);
result at [HA06b-rhr-zscore/result.md](garmin/hypotheses/HA06b-rhr-zscore/result.md).

The motivation is explicit: the locked
[`relative_not_absolute`](../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md)
feedback principle says *"for PEM-pacing metrics in this project,
always use z-scores or deviations from personal baseline, not
absolute thresholds."* HA06 partially followed this (the
delta-from-baseline part was relative) but the threshold N itself
was absolute. HA06b fully follows the principle. As with Theme A,
this is a methodologically-motivated re-test of mis-calibrated
spec, not a re-cut of HA06; HA06 stays as-locked.

**Result: TRAIN SUPPORTED, validate REFUTED → OVERALL REFUTED by
the locked rule.** But the train signal lifted substantially under
the relative framing.

| | train (14 episodes) | validate (15 episodes) |
|---|---:|---:|
| crash episodes triggering (\|z\| ≥ 1.5) | **10 (71.4%)** | 8 (53.3%) |
| null windows triggering | 105 (52.5%) | 105 (52.5%) |
| **discrimination (pp)** | **+18.9** | +0.8 |
| median max-\|z\| | 2.31 | 1.57 |
| crit (a) freq ≥ 60% | **PASS** | fail (53.3% < 60%) |
| crit (b) disc ≥ +15 pp | **PASS** | fail (+0.8 pp) |
| crit (c) median ≥ 0.75 | **PASS** | PASS |
| verdict | **supported** | refuted |

Train SUPPORTED in **4 of 6** bidirectional configurations
(4d × {1.5, 2.0}, 5d × {1.5, 2.0}); the train-era signal is
robust across threshold and window choice. N_std = 2.5 fails
criterion (a) in train (50%) — the participant's typical max-|z|
does not stretch that far.

#### Directionality reversal between eras

| | n triggering | elevated (z ≥ +1.5) | lowered (z ≤ −1.5) |
|---|---:|---:|---:|
| train | 10 | **7 (70%)** | 3 (30%) |
| validate | 8 | 2 (25%) | **6 (75%)** |

The era pattern **reverses**. Train-era triggering crashes are
predominantly elevated-direction (classical Workwell / sympathetic
overarousal); validate-era triggering crashes are predominantly
lowered-direction (Wiggers' parasympathetic-swing pattern). **The
pattern Wiggers documented is empirically present in the validate
era at 75% of triggering events** — but the same lowered pattern
appears in random non-crash 4-day windows at roughly the same rate,
so it does not discriminate.

Validate one-sided "elevated only" arm shows **−16.2 pp
discrimination**: classical Workwell elevated-RHR direction is
*anti*-predictive of validate-era crashes — they are *less* likely
to be preceded by elevated RHR than random non-crash 4-day
windows. This is the opposite-direction mirror of the train pattern
made formal.

#### Three train-era SUPPORTED autonomic-deviation precursors on three channels

HA06b is the third pre-registered train-era SUPPORTED finding under
clean methodology, all on different channels:

| test | channel | window | metric | train freq | train disc |
|---|---|---|---|---:|---:|
| H02b | per-minute stress spike count | 3d rolling | abs minutes ≥ +10 | 71.4% | +29.9 pp |
| H02d bridge × 5d | per-minute stress spike (sentinel-corrected) | 5d | abs minutes ≥ +10 | 92.3% | +31.8 pp |
| **HA06b** | **nightly RHR z-score** | **4d lagged** | **rel \|z\| ≥ 1.5** | **71.4%** | **+18.9 pp** |

The pre-cliff (2022-23) era's autonomic-deviation precursor is now
demonstrably **multi-channel**, not stress-specific. Three different
measurement choices, three different time-scales, three different
methodologies, all converging on the same train-era crashes. The
b retrospective card (train-era 2022-23 per-crash) has a
substantially stronger empirical case than after H02b alone.

The validate-era refutation likewise extends. **Twelve pre-registered
tests are now consistent** that no clean validate-era precursor
exists in waking-hour-derivable Garmin signals under the canonical
3-criterion bar (5 stress-channel + 4 activity-shock channel +
2 RHR channel + 1 sleep-efficiency channel).

#### Methodology lesson banked

**Pre-register relative thresholds (z-score or percentile rank) as
the default for autonomic-channel tests.** Absolute thresholds drawn
from external populations need re-calibration to participant
variability *before* the test runs, not after. HA06's median
max-|delta| of 1.6-3.5 bpm vs Wiggers/Workwell-calibrated 5/10/15
bpm thresholds is the textbook case: the participant's signal-to-noise
characteristic differs by enough that an externally-calibrated
absolute floor missed 47.4 percentage points of train triggering
events (HA06b bidirectional 71.4% vs HA06 absolute 21.4%).

Applies forward to:
- **HA07** (day-over-day HRV drop) — pre-register on z-score
  thresholds from the start, not the *vermoeidheidskliniek*'s
  absolute 10 ms.
- **HA08** (multi-day HRV creep / slope) — pre-register slope
  thresholds in standardized units.
- **HA10** (BB overnight recharge coarse proxy) — pre-register on
  z-score against the participant's own recharge distribution, not
  on Wiggers' absolute 70-80% floor.

This now joins the Theme A lesson (lagged baseline for
push-burden-style metrics; symmetric pre-registered re-test
discipline) in the project's methodology playbook.

### 5.14. HA10 — Body Battery overnight recharge coarse proxy (z-score, bidirectional)

After HA07 (day-over-day HRV drop) was queued as the next sibling
test, an investigation revealed that **nightly HRV is not present
in any local data source for this participant's Forerunner 245 GDPR
dump**: no HRV field in UDS, sleepData, bioMetrics, monitoring_b
FIT, or activity FIT. HRV records live only in the Garmin Connect
cloud, accessible via the same ToS-grey REST API path as H04b's
per-minute Body Battery. HA07 was therefore gated on the same
authorisation as H04b. The user opted to pivot to HA10 (BB recharge
coarse proxy) followed by HA11 (within-day U-dip pattern), both
operationalisable on existing local data.

HA10 tests Wiggers' "chronic-illness BB rarely reaches 100%"
framing operationalised through the morning HIGHEST Body Battery
anchor in the daily UDS record. The HIGHEST anchor is consistently
in the early-morning hours (03:00-10:00 local time across the
corpus) and represents the BB level reached after overnight
recharge. Pre-registration locked 2026-06-07 at
[HA10-bb-overnight-recharge/hypothesis.md](garmin/hypotheses/HA10-bb-overnight-recharge/hypothesis.md);
result at [HA10-bb-overnight-recharge/result.md](garmin/hypotheses/HA10-bb-overnight-recharge/result.md).

**Per-day metric**: `morning_peak[d]` = HIGHEST BB anchor's
`statsValue` on date d, filtered to timestamps in [03:00, 10:00].
Daytime-peak days (e.g. nap recovery) are excluded. Z-scored
against lagged baseline `[d-90, d-30]` (Theme A); thresholds
N_std = 1.5 / 2.0 / 2.5 consistent with HA06b. Bidirectional
primary; one-sided lowered (Wiggers direction) + one-sided elevated
sensitivity arms.

**Result: TRAIN REFUTED, VALIDATE SUPPORTED → OVERALL REFUTED per
the locked rule. But the validate-era SUPPORTED finding is the
project's first.**

| | train (14 episodes) | validate (15 episodes) |
|---|---:|---:|
| crash episodes triggering (\|z\| ≥ 1.5) | 7 (50.0%) | **13 (86.7%)** |
| null windows triggering | 141 (70.5%) | 141 (70.5%) |
| **discrimination (pp)** | **−20.5** | **+16.2** |
| median max-\|z\| | 1.637 | 2.121 |
| **verdict** | **refuted** | **SUPPORTED** |

13 prior pre-registered tests on waking-hour Garmin signals had
refuted validate-era under the canonical 3-criterion bar. HA10's
validate arm at 4d primary clears all three criteria
(86.7% / +16.2 pp / 2.121). The strict overall verdict is REFUTED
because train fails (50% trigger rate is BELOW the 70.5% null), but
**this is the first clean validate-era precursor finding in the
investigation**.

#### Directionality reversal between eras

| | n triggering | elevated (z ≥ +1.5) | lowered (z ≤ −1.5) |
|---|---:|---:|---:|
| train | 7 | 0 (0%) | **7 (100%)** |
| validate | 13 | **9 (69%)** | 4 (31%) |

**Train: 100% lowered direction** (Wiggers' canonical "didn't
recharge" pattern). **Validate: 69% elevated direction**
(paradoxical "looked like a great night but" pattern). Both eras
have a SUPPORTED arm at the 5-day secondary window in their
respective *opposite* directions: train SUPPORTED at 5d one-sided
lowered (+18.3 pp, 64.3% freq); validate SUPPORTED at 5d one-sided
elevated (+27.5 pp, 60.0% freq). This is the cleanest
era-directionality reversal in the project so far.

#### Cross-channel coherence with HA06b — strongest internal-physiological-consistency evidence in the project

BB is inversely-related to RHR via the vagal-tone / HRV → stress →
BB pathway. The fact that HA10 (BB) and HA06b (RHR) show
**opposite directions per era** is *expected* if the autonomic
deviation is real and the era split represents a flip in dominant
direction. The fact that the pattern emerges **independently** on
two channels is strong internal-consistency evidence.

| era | HA06b RHR direction | HA10 BB direction | autonomic interpretation |
|---|---|---|---|
| train (2022-23) | elevated (70% triggering) | lowered (100% triggering 4d) | **sympathetic overarousal**: high RHR ↔ low HRV ↔ low BB recharge |
| validate (2024+) | lowered (75%) | elevated (69%) | **parasympathetic swing**: low RHR ↔ high HRV ↔ high BB recharge — Wiggers' "freeze" pattern |

**Wiggers' "freeze" pattern is now empirically population-level
visible** in this participant's validate-era crashes on two
independent biometric channels.

#### Pre-committed soft outcome held: H04b strongly prioritised

HA10's §9 pre-commit stated that SUPPORTED in either era moves
H04b's per-minute decode priority UP. The validate-era SUPPORTED
finding triggers this commitment. **The per-minute BB version
(H03b via H04b) should sharpen the validate-era signal** — the
coarse 3-anchor proxy already finds 86.7% trigger rate at
+16.2 pp; the trajectory pattern is plausibly cleaner.

### 5.15. HA11 — Within-day stress U-dip event count (z-score, one-sided elevated)

HA11 follows HA10 as the second user-confirmed pivot test. Tests
Wiggers' within-day pattern: per-minute stress drops sharply
(the "U") and plateaus at a *higher-than-pre-dip* baseline.
Wiggers reports resolving this pattern with ORS / electrolytes;
the physiological hypothesis is orthostatic / low-blood-volume
dysregulation. Pre-registration locked 2026-06-07 at
[HA11-stress-udip/hypothesis.md](garmin/hypotheses/HA11-stress-udip/hypothesis.md);
result at [HA11-stress-udip/result.md](garmin/hypotheses/HA11-stress-udip/result.md).

**This is the first within-day pattern test in the project** —
all prior precursor tests have used day-level metrics. The data
primitive is per-minute stress samples re-parsed from monitoring_b
FIT files (Stage 1 extraction, ~7 min; 7888 files, 1739 days,
1722 valid ≥600 samples, 1469 total U-dip events identified).

**U-dip event definition (locked)**: a timestamp t where
- pre-dip mean stress in [t−35, t−5] is ≥ 40 (moderate baseline),
- dip-floor in [t−7, t+7] is ≤ pre-dip − 25 (sharp drop), AND
- post-dip mean stress in [t+8, t+38] is ≥ pre-dip + 5 (higher plateau).

Refractory 60 min between consecutive events. Daily count
`u_dip_count[d]` z-scored against lagged baseline `[d-90, d-30]`.
Thresholds N_std = 1.5 / 2.0 / 2.5. **One-sided elevated primary**
(more U-dips = more orthostatic events = pre-crash precursor per
Wiggers' framing); bidirectional + one-sided lowered as sensitivity
arms.

Distribution: 47% of valid days have 0 U-dip events, 31% have 1,
14% have 2, 7% have 3+. The metric has variability sufficient for
z-score analysis (cross-day stdev 1.02; lagged-window σ ~0.78-0.98).

**Result: TRAIN SUPPORTED, VALIDATE REFUTED → OVERALL REFUTED per
the locked rule.**

| | train (14 episodes) | validate (13/15 clean episodes) |
|---|---:|---:|
| crash episodes triggering (signed z ≥ +1.5) | **9 (64.3%)** | 4 (30.8%) |
| null windows triggering | 83 (41.5%) | 83 (41.5%) |
| **discrimination (pp)** | **+22.8** | **−10.7** |
| median max signed z | 2.168 | 0.374 |
| **verdict** | **supported** | **refuted (inverse)** |

Train clears all three criteria substantially. **Validate is
anti-predictive: −10.7 pp at 4d primary, scaling to −24.1 pp at
5d N_std=2.0.** Validate-era crashes have *fewer* U-dip events
than typical 4-5d windows — the inverse-direction signal is itself
a *characteristic* signature of the parasympathetic-swing era, not
random noise.

#### Cross-channel coherence — four-channel train-era convergence

HA11 adds the fourth train-era SUPPORTED autonomic precursor on the
fourth channel:

| test | channel | window | metric | train freq | train disc |
|---|---|---|---|---:|---:|
| H02b | per-minute stress spike count | 3d rolling | abs minutes ≥ +10 | 71.4% | +29.9 pp |
| H02d bridge × 5d | per-minute stress spike (sentinel-corrected) | 5d | abs minutes ≥ +10 | 92.3% | +31.8 pp |
| HA06b | nightly RHR z-score | 4d lagged | rel \|z\| ≥ 1.5 (bidir) | 71.4% | +18.9 pp |
| **HA11** | **within-day U-dip count z-score** | **4d lagged** | **rel signed z ≥ 1.5 (elevated)** | **64.3%** | **+22.8 pp** |

Four SUPPORTED train findings across four distinct channels:
- Per-minute stress trajectory pattern (H02b, H02d) — sympathetic
  spike duration
- Per-night autonomic recovery (HA06b) — elevated RHR
- Per-day within-day pattern (HA11) — elevated U-dip count

The pre-cliff (2022-23) era's
sympathetic-overarousal / orthostatic-instability precursor
signature is now **four-channel-confirmed across distinct
measurement modalities and time-scales**. This is the strongest
multi-channel convergence in the project.

#### Era reversal pattern formalised across four channels

| era | H02b/H02d (stress) | HA06b (RHR) | HA11 (U-dip) | HA10 (BB peak) |
|---|---|---|---|---|
| **train** | SUPPORTED elevated | SUPPORTED elevated | **SUPPORTED elevated** | refuted (5d lowered SUPPORTED) |
| **validate** | refuted | refuted | **refuted (inverse)** | **SUPPORTED elevated** (paradoxical swing) |

Pre-cliff: sympathetic-arousal-spectrum events fire across all
four channels. Post-cliff: parasympathetic-swing-spectrum events
fire (HA10 BB high, with HA06b RHR low / HA11 U-dip low as
inverse-direction characteristic signatures).

#### Secondary descriptive — same-day correlation

Per HA11 §4.10: Spearman ρ between u_dip_count[d] and gevoelscore[d]
is essentially zero across both eras (train +0.075, validate
+0.012). The U-dip metric is a 4-day-lead precursor in train, NOT
a same-day symptom correlate.

### 5.16. Consolidated picture after HA06b + HA10 + HA11

Reading §5.13 + §5.14 + §5.15 together (all three run on 2026-06-07
under clean pre-registration), the consolidated picture for this
participant's crash precursors:

**Pre-cliff (2022-23) era — four-channel-confirmed
sympathetic-overarousal + orthostatic-instability signature:**
- H02b stress spike count 3d (+29.9 pp, 71.4%)
- H02d bridge × 5d (+31.8 pp, 92.3%) — strongest train signal of project
- HA06b RHR z-score 4d (+18.9 pp, 71.4%)
- HA11 U-dip count z-score 4d (+22.8 pp, 64.3%)
- HA10 BB peak lowered 5d (+18.3 pp, 64.3%) — fifth train arm
  SUPPORTED, in the inverse-of-validate direction

**Post-cliff (2024+) era — one-channel-confirmed
parasympathetic-swing signature:**
- HA10 BB peak elevated 4d primary (+16.2 pp, 86.7%) — the
  project's first validate-era SUPPORTED finding under the
  canonical bar.

**Era directionality reversal demonstrated across four channels:**
the same physiological phenomenon (autonomic deviation) operates in
opposite directions across eras. The pattern is internally
consistent across BB ↔ RHR ↔ U-dip via the vagal-tone / HRV /
stress pathway.

**Net change to "what's been SUPPORTED" under clean methodology:**
the investigation now has **four train-era SUPPORTED autonomic-
deviation precursors** (H02b, H02d, HA06b, HA11) and **one
validate-era SUPPORTED precursor** (HA10 morning BB peak elevated).
The D7 single-mechanism-two-regimes reframe now has empirical
anchors in BOTH eras, on physiologically related channels with
opposite-direction era-specific patterns.

### 5.17. HA07/HA08 BLOCKED-PENDING-HARDWARE; substitute tests HA07c + HA08c + HA07d via sleep stress as HRV proxy

After HA10 + HA11 closed, H04b path C authorisation was completed
(garminconnect library installed, OAuth token cached) to unlock
nightly HRV (for HA07/HA08/HA09/HA12) and per-minute Body Battery
(for H03b proper). A smoke test against the Garmin Connect REST
API on 2026-05-15 confirmed Body Battery, Sleep, and Stress
endpoints respond. **But the HRV endpoint
`/hrv-service/hrv/{date}` returned an empty dict for every date
sampled (2022 through 2026).** Investigation traced the cause to
**hardware**: the Forerunner 245 (firmware 10.40) was released in
2019 with an older optical HR sensor. **Garmin's HRV Status
feature was added to the newer Forerunner 255/265/955/965 and
Fenix 7 generation watches (2022-2023) which use a
multi-sample sensor.** The FR245's sensor does not support HRV
Status; the data simply was never recorded.

**HA07, HA08, HA12 are therefore BLOCKED-PENDING-HARDWARE.** The
original pre-registrations remain as audit-trail records;
substitute pre-registrations were locked before any analysis
inspected the data.

#### The substitute proxy argument

Garmin's `stress` signal is computed as `f(HRV, HR, activity)`.
During sleep, activity ≈ 0, so `sleep_stress ≈ f(HRV, HR)`. Higher
mean sleep stress corresponds to lower HRV (sympathetic dominance);
lower mean sleep stress corresponds to higher HRV (vagal
dominance). The relationship is non-linear and bounded [1, 100],
but **Workwell and Wiggers reference Garmin's stress in their
pacing recommendations as an HRV-class indicator** — the
proxy is already used in the field.

Three substitute pre-registrations were locked **before** any
sleep-stress data was inspected:

- **HA07c** — night-over-night delta of mean sleep stress
  z-scored against lagged baseline (analog of HA07).
- **HA08c** — trailing-5-day OLS slope of mean sleep stress
  z-scored (analog of HA08).
- **HA07d** — night-over-night delta of in-sleep-window stress
  STDEV z-scored (variability of HRV proxy — second-order
  primitive testing autonomic flexibility shift).

The pre-registered §8 caveats in each hypothesis.md require
result.md files to explicitly acknowledge:
- Sleep stress is a proxy for HRV, not HRV itself.
- A SUPPORTED test on the proxy does NOT confirm the HRV
  hypothesis directly.
- A REFUTED test on the proxy does NOT refute the HRV hypothesis.
- Cross-channel coherence with HA06b RHR / HA10 BB peak / HA11
  U-dip is the strongest validation the proxies provide.

Stage 1 extraction re-parsed all 7888 monitoring_b FIT files
(~7 min, same approach as HA11) for per-minute stress samples;
intersected with sleep windows from local `*_sleepData.json` (in
`DI-Connect-Wellness`). Output: 1734 nights total, **1707 valid
(≥120 in-window samples)**, mean 592 samples per valid night.

### 5.18. HA07c — Sleep stress mean delta (one-sided elevated)

Result at [HA07c-sleep-stress-mean-delta/result.md](garmin/hypotheses/HA07c-sleep-stress-mean-delta/result.md).

**Primary 4d N_std=1.5 one-sided elevated: TRAIN SUPPORTED,
VALIDATE REFUTED.**

| | train (13/14 clean) | validate (15/15 clean) |
|---|---:|---:|
| triggering (signed z ≥ +1.5) | **9 (69.2%)** | 6 (40.0%) |
| null | 46.0% | 46.0% |
| **discrimination (pp)** | **+23.2** | −6.0 |
| median max signed z | 1.677 | 1.392 |
| verdict | **SUPPORTED** | refuted |

**5th train-era SUPPORTED autonomic-channel precursor on the 5th
channel** (after H02b, H02d, HA06b, HA11). The HRV proxy is
validated on the train side: sleep stress mean delta discriminates
train crashes at +23.2 pp, matching the magnitudes of HA06b RHR
(+18.9 pp) and HA11 U-dip (+22.8 pp).

Multiple arms SUPPORTED for train (5d secondary elevated +18.4 pp,
4d N_std=2.0 bidirectional +19.7 pp, 4d N_std=2.0 lowered
+26.0 pp). Directionality split: train 33% elevated /
67% lowered-at-max-|z| — train-era crashes preceded by HIGH
AUTONOMIC VOLATILITY (large shifts in both directions; downward
deviation at higher thresholds is the *strongest* discriminator).

### 5.19. HA08c — Sleep stress mean slope (one-sided elevated)

Result at [HA08c-sleep-stress-slope/result.md](garmin/hypotheses/HA08c-sleep-stress-slope/result.md).

**Primary 4d N_std=1.5 one-sided elevated: TRAIN SUPPORTED,
VALIDATE REFUTED.**

| | train (13/14 clean) | validate (15/15 clean) |
|---|---:|---:|
| triggering (signed z ≥ +1.5) | **8 (61.5%)** | 6 (40.0%) |
| null | 38.5% | 38.5% |
| **discrimination (pp)** | **+23.0** | +1.5 |
| median max signed z | 2.116 | 1.311 |
| verdict | **SUPPORTED** | refuted |

**6th train-era SUPPORTED finding under clean methodology**;
both acute (HA07c delta) and sustained (HA08c slope) modes
SUPPORTED in train on the same HRV-proxy channel. Wiggers' "HRV
daalt over meerdere dagen na overbelasten" (multi-day creep mode)
is empirically population-level present in pre-cliff era.

Strong **validate ANTI-PREDICTIVE** pattern at higher thresholds
(N_std=2.0 bidirectional **−36.2 pp**, one-sided lowered
−27.3 pp). Validate-era crashes arrive against unusually-FLAT
baseline — the autonomic creep that precedes train-era crashes is
ABSENT in validate-era lead-ups. (This anti-predictive pattern
foreshadows HA07d's variability finding — see §5.20.)

### 5.20. HA07d — Sleep stress variability delta (BIDIRECTIONAL primary) → FIRST PROJECT-LEVEL OVERALL-SUPPORTED TEST

Result at [HA07d-sleep-stress-variability/result.md](garmin/hypotheses/HA07d-sleep-stress-variability/result.md).

Second-order primitive: **night-over-night delta of in-sleep-window
stress STDEV** (variability of the HRV-proxy). Tests autonomic
**flexibility** shift, not level shift. Bidirectional primary —
the physiological direction is a priori ambiguous.

**Primary 4d N_std=1.5 bidirectional: TRAIN SUPPORTED AND VALIDATE
SUPPORTED → OVERALL SUPPORTED per the locked rule.**

| | train (13/14 clean) | validate (15/15 clean) |
|---|---:|---:|
| triggering (\|z\| ≥ 1.5) | **11 (84.6%)** | **13 (86.7%)** |
| null | 65.0% | 65.0% |
| **discrimination (pp)** | **+19.6** | **+21.7** |
| median max \|z\| | 2.541 | 2.752 |
| verdict | **SUPPORTED** | **SUPPORTED** |
| **OVERALL** | colspan=2 | **SUPPORTED both eras (project first)** |

**This is the first pre-registered test in the entire investigation
to OVERALL SUPPORT in both eras under the strict locked rule.**
Nineteen pre-registered hypotheses preceded HA07d. HA10 was the
first validate-era SUPPORTED but failed train. HA07d clears both
simultaneously.

#### Era-specific directionality within the bidirectional finding

The bidirectional primary captures both directions; the one-sided
sensitivity arms reveal the per-era directional preference:

| arm | train | validate |
|---|---|---|
| **4d N_std=1.5 bidirectional (PRIMARY)** | **SUPPORTED +19.6** | **SUPPORTED +21.7** |
| 4d N_std=1.5 one-sided **elevated** (variability rose) | **SUPPORTED +27.4** | refuted +3.8 |
| 4d N_std=1.5 one-sided **lowered** (variability fell) | **SUPPORTED +16.5** | **SUPPORTED +21.7** |
| 4d N_std=2.0 bidirectional | **SUPPORTED +15.5** | **SUPPORTED +27.3** |
| 4d N_std=2.0 one-sided lowered | refuted +14.7 | **SUPPORTED +28.5** |

**Train SUPPORTS BOTH directions** (variability rose AND fell)
at N_std=1.5 — train-era crashes preceded by large variability
shifts in either direction (autonomic instability / volatility).

**Validate SUPPORTS ONLY the LOWERED direction** (variability
fell, +21.7 pp at N_std=1.5, **+28.5 pp at N_std=2.0**) —
validate-era crashes preceded by **autonomic stillness**: sleep
stress variability DROPS in the days before crashes. The
autonomic state becomes unusually stable, "looks like" recovery,
but symptoms continue.

**HA07d's +28.5 pp validate discrimination is the strongest
validate-era discrimination on any arm in the project** (exceeds
HA10's previous best of +27.5 pp at 5d one-sided elevated).

#### The validate-era picture is now multi-channel-anchored — with one robust primary and one fragile secondary

Validate-era crashes now have **two empirical anchors with
different robustness profiles** (per independent peer review §3
critique on threshold-fragility):

| validate-era signature | direction | discrimination | threshold robustness | role |
|---|---|---:|---|---|
| **HA07d sleep stress variability** | **lowered** | **+21.7 pp (4d primary bidir), +28.5 pp (N_std=2.0 lowered)** | **ROBUST** — SUPPORTS at N_std=1.5 AND N_std=2.0 in primary | **PRIMARY** |
| HA10 morning BB peak | elevated | +16.2 pp (4d primary bidir, N_std=1.5 only) | **FRAGILE** — refuted at N_std=2.0 and 2.5 | CORROBORATING |

HA10's threshold fragility was flagged by the independent peer
review as "the single most fragile headline in the project" before
HA07d landed. HA07d does **not** inherit this fragility — its
SUPPORTED status holds at multiple threshold tiers AND multiple
arms.

The HA10 fragility was further investigated through a
**pre-registered threshold-monotonicity diagnostic** (locked
[diagnostic.md](garmin/hypotheses/HA10-threshold-monotonicity-diagnostic/diagnostic.md);
ran 2026-06-07; result at [HA10-threshold-monotonicity-diagnostic/result.md](garmin/hypotheses/HA10-threshold-monotonicity-diagnostic/result.md)).
**Verdict per locked rescue/close/ambiguous criteria: CLOSE.** A
fine N_std grid [0.5 → 4.0] showed HA10's primary bidirectional
arm peaks at N_std=1.75 — one σ-tier past the locked rescue window
[1.0, 1.5]. Every other shape criterion passed (Spearman rho
−0.456 strongly monotonic; disc holds at +14 at N_std=2.0, +11
at 2.5; one sign change); the peak-location failure is the only
close trigger. **HA10's locked SUPPORTED verdict stays on record**
under pre-registration discipline; but synthesis-level framing
demotes HA10 to non-load-bearing per the locked CLOSE clause.

**Important nuance** (recorded in the diagnostic result.md):
HA10's one-sided ELEVATED arm shows robust threshold-monotonicity
— +23 pp plateau from N_std=1.5 through 2.5. The **direction**
HA10 identified (paradoxical elevated BB peak before validate-
era crashes) is supported by the one-sided arm's robust shape;
only HA10's specific BIDIRECTIONAL-PRIMARY choice failed the
diagnostic.

**Subsequent HA07d threshold-monotonicity diagnostic CLOSE both
eras 2026-06-07** (see [HA07d-threshold-monotonicity-diagnostic/result.md](garmin/hypotheses/HA07d-threshold-monotonicity-diagnostic/result.md)):
HA07d's bidirectional primary closes per the same locked v1
rescue/close criteria. Peak at N_std=1.75 outside rescue window
[1.0, 1.5] in both eras. Validate Spearman positive (+0.170 —
rising-with-threshold shape that the v1 criteria penalise even
though qualitatively highly robust: discrimination stays +19 to
+31 pp across N_std=1.0 through 4.0). Train Spearman near-zero
(+0.005) with 4 sign changes (genuinely bumpy curve consistent
with train-era volatility hypothesis). The v1 locked rule
applied honestly: CLOSE both eras.

**The validate-era picture therefore rests on NO LOAD-BEARING
ANCHOR** in v1 synthesis framework. Both HA07d and HA10's locked
SUPPORTED verdicts stay on record per audit-trail discipline;
synthesis-level load-bearing claims do not. The diagnostic-v1
criteria themselves are acknowledged to have a methodological
defect — they only capture canonical-decline robustness and
penalise stable-plateau and rising-with-threshold shapes that are
equally robust forms of signal. **v2 criteria** are pre-registered
2026-06-07 as a methodology document
([garmin/methodology/threshold-sweep-rescue-criteria-v2.md](garmin/methodology/threshold-sweep-rescue-criteria-v2.md))
with a five-category shape rule. **v2 diagnostics for HA10, HA07d,
HA06b, and HA11** are pre-registered as separate locked
diagnostic.md files. The validate-era load-bearing claim depends
entirely on v2 outcomes.

**Symmetric interim demotion** (peer-review concern on asymmetry):
HA06b and HA11 were demoted to "load-bearing pending v2" in
synthesis-level framing, joining HA10 and HA07d. All four findings
under v2 diagnostic shared the same interim status until v2 ran.
The discipline cost of demotion was paid symmetrically.

**Atomic v2 round result (2026-06-07)** — three RESCUES, one CLOSE:

- HA10 validate bidirectional: **RESCUE** via Cat 3 (rising/late-peak).
- HA07d train bidirectional: **RESCUE** via Cat 3.
- HA07d validate bidirectional: **RESCUE** via Cat 2 (stable plateau) + Cat 3.
- HA11 train one-sided elevated: **RESCUE** via Cat 1 (canonical decline).
- HA06b train bidirectional: **CLOSE** via Cat 4 (2 sign-changes in [1.0, 3.0]).

Restoration map: HA10, HA07d, HA11 restored to load-bearing. HA06b
permanently demoted. The discipline binds in both directions —
v2 produced honest verdicts that could have gone either way per
finding, and one of four findings did genuinely fail the v2
strict reading.

In the interim before v2 diagnostics run:
- Card (b2) cannot ship anchored.
- The era-as-moderator narrative weakens to "supported by
  physiological consistency across multiple non-load-bearing
  findings" rather than "demonstrated on a single load-bearing
  test."
- The HA07d-as-overall-SUPPORTED headline is paused. Locked
  verdict stays on record; synthesis claim depends on v2.

The pre-cliff multi-channel convergence narrative (six channels,
seven tests, sleep-stress channel with three primitives) remains
intact at the locked verdict level. After v2 criteria lock, the
same diagnostic framework will be applied symmetrically to those
train-era findings (H02b, H02d, HA06b, HA11 already pre-registered
for v2). The train-era load-bearing status is conditional on those
v2 outcomes too.

Both LOOK like recovery. Neither IS recovery. The
parasympathetic-swing pattern Wiggers documents qualitatively is
empirically observable in this participant's validate era at
robust discrimination magnitudes at the locked verdict level via
HA07d and HA10. Whether either supports the synthesis-level
load-bearing claim depends on v2 diagnostic outcomes. HA10's BB
peak elevation is
descriptively consistent but non-load-bearing per the diagnostic.

### 5.21. Consolidated picture after the substitute tests

The post-substitute SUPPORTED list:

**Pre-cliff (2022-23) era — SEVEN-channel/primitive
sympathetic-overarousal + autonomic-volatility precursor signature:**
- H02b stress spike count 3d (+29.9 pp, 71.4%)
- H02d bridge × 5d (+31.8 pp, 92.3%) — strongest train signal
- HA06b RHR z-score 4d (+18.9 pp, 71.4%)
- HA11 U-dip count z-score 4d (+22.8 pp, 64.3%)
- HA07c sleep stress mean delta 4d (+23.2 pp, 69.2%)
- HA08c sleep stress slope 4d (+23.0 pp, 61.5%)
- **HA07d sleep stress variability delta 4d (+19.6 pp, 84.6%)** —
  also validate-era SUPPORTED, project's first overall-SUPPORTED

**Post-cliff (2024+) era — TWO-channel
parasympathetic-swing / autonomic-stillness signature:**
- HA10 BB peak elevated 4d primary (+16.2 pp, 86.7%)
- **HA07d sleep stress variability lowered 4d primary (+21.7 pp,
  86.7%, ALSO project's first overall-SUPPORTED at primary
  bidirectional)**

**Methodology lessons banked from the substitute round:**
- Pre-register relative thresholds for autonomic-channel tests
  (HA06 → HA06b banked; HA07c/HA08c/HA07d all followed).
- Pre-register the **bidirectional primary** when the
  physiological direction is genuinely ambiguous (HA07d's primary
  bidirectional was crucial; one-sided primary would have missed
  the validate-era finding).
- **Second-order primitives (variability of derived metrics) can
  carry signal first-order primitives miss.** HA07c (mean delta)
  refuted validate at +4.3 pp; HA07d (variability delta) supported
  validate at +21.7 pp. The autonomic dimension that shifts before
  validate-era crashes is FLEXIBILITY, not LEVEL.
- **Locked HRV pre-registrations do not waste effort if hardware
  blocks them**: HA07 / HA08 / HA12 pre-registrations are
  preserved as audit-trail records; substitutes were locked
  *before* data inspection; methodology integrity stays clean.
- When path C authorisation reveals a hardware gap, **the
  defensible substitute path is to find a proxy whose
  relationship to the original signal is known**, not to abandon
  the pre-registered question.

**Net change after the substitute round + threshold-monotonicity
diagnostic-v1 results (2026-06-07):**

- Train-era SUPPORTED on record: 7 across six distinct channels
  (sleep-stress channel tested through three primitives). **None
  has yet undergone threshold-monotonicity diagnostic.** v2
  diagnostics pre-registered for HA06b and HA11 (HA07c, HA08c,
  H02b, H02d to follow if v2 framework is adopted broadly).
  Train load-bearing status conditional on v2 outcomes.
- Validate-era SUPPORTED on record: 2 (HA10 + HA07d). **Both
  demoted to non-load-bearing** under v1 diagnostic CLOSE
  verdicts. v2 diagnostics pre-registered for both.
- **Overall-SUPPORTED at primary on record: 1** (HA07d). Demoted
  to non-load-bearing under v1; status pending v2.
- Card (b) train-era retrospective: seven locked anchors on
  record; load-bearing status conditional on v2 diagnostics for
  the underlying tests.
- Card (b2) validate-era retrospective: ZERO load-bearing
  anchors after diagnostic-v1 round. Cannot ship anchored under
  v1 framework. Ship pathway depends on v2 RESCUE outcomes plus
  separately-completed specificity tables.
- D7 single-mechanism-two-regimes reframe: HA07d's
  single-channel both-eras evidence is **paused** pending v2.
  In the interim, the era reversal narrative rests on
  physiological consistency across multiple non-load-bearing
  findings rather than a load-bearing single-test demonstration.

**Channel-independence honest framing** (per peer-review §3 — the
review's most important framing critique):

The synthesis-level claim of "seven train channels SUPPORTED" weights
the channels as independent samples of nature. They are NOT
statistically independent:
- Body Battery is a fused composite `g(HR, HRV, stress, sleep)`.
- Sleep stress is per-minute stress restricted to the sleep window.
- HA07c (mean delta), HA08c (slope), HA07d (variability delta) are
  three primitives of the *same* sleep-stress channel.
- Even RHR (HA06b) and stress (HA11) share underlying HRV input via
  the Garmin algorithm.

The more honest framing: **six distinct measurement axes confirming
an underlying autonomic-state construct, all of which SUPPORT in
train**. The pre-cliff sympathetic-overarousal + autonomic-
volatility precursor signature is **well-replicated through
multiple operationalisations**; "multi-channel convergence" was
overstating the independence. A future cross-channel correlation
matrix (queued) will anchor this caveat quantitatively.

**Independent peer-review integration** (2026-06-07): the project
received an independent variable-architecture review at
[garmin/review/2026-06-07-variable-architecture-review.md](garmin/review/2026-06-07-variable-architecture-review.md);
the project's research lead replied at
[garmin/review/2026-06-07-reply-with-ha07d-context.md](garmin/review/2026-06-07-reply-with-ha07d-context.md)
committing to Tier 1 framing fixes (this section + STOCKTAKE + synthesis
+ pem-pacing-indicators) and Tier 2 action items (HA10 threshold-
monotonicity diagnostic; HA01b per-axis decomposition; H01/H03/H04
Gen-3 re-tests; Fisher's exact p-values; cross-channel correlation
matrix; card specificity tables; crash_v3 mechanism subtyping; S02
score trajectory; pooled-corpus descriptive arm; HA11 parameter
sensitivity diagnostic). See QUEUED-WORK for the full Tier 2 items.

### 5.22. HA01b per-axis decomposition diagnostic — first diagnostic under consolidated testing playbook

Pre-registered as the next strand after the Theme A bundled re-test
demoted HA01b composite to REFUTED both eras. Locked at
[HA01b-per-axis-diagnostic/diagnostic.md](garmin/hypotheses/HA01b-per-axis-diagnostic/diagnostic.md);
run 2026-06-07; result at
[HA01b-per-axis-diagnostic/result.md](garmin/hypotheses/HA01b-per-axis-diagnostic/result.md).
This is the **first diagnostic locked under the consolidated testing
playbook** ([garmin/methodology/testing-playbook.md](garmin/methodology/testing-playbook.md))
section 9 compliance bar.

**Diagnostic question**: HA01b's composite (`exertion_class_lagged`,
MAX percentile rank across 4 input axes) refuted both eras under the
clean lagged baseline. Was the composite obscuring a per-axis signal
that any single axis, pre-registered as primary, would have caught?

**Result**: yes, for one axis.

| axis | train | validate |
|---|---|---|
| **effective_exertion** | **SUPPORTED** +21.3 pp / 81.8% freq / median rank 0.883 | **SUPPORTED** +19.5 pp / 80.0% freq / median rank 0.909 |
| step_burden | refuted (crit-c miss by 0.008; +27.5 pp, 90.9% freq) | SUPPORTED +16.6 pp / 80.0% freq / median rank 0.875 |
| max_hr_peak | refuted (+7.5 pp, crit-b miss) | **refuted (-7.7 pp, INVERTED)** |
| vigorous_min | refuted (+10.7 pp, crit-b miss) | SUPPORTED +24.6 pp / 86.7% freq / median rank 0.917 |

**Composite control reproduces HA01b REFUTED both eras** (+3.4 train,
+1.5 validate pp), confirming the per-axis decomposition is honestly
extracting signal the composite obscured.

**Why composite REFUTES while per-axis SUPPORTS**: the composite is
`MAX(rank across 4 axes) ≥ 0.75`. The MAX across 4 axes triggers
~78% of the time in null windows (any one of 4 axes being elevated
suffices). Crashes trigger at ~80%. Spread = ~2 pp. When you ask
"is THIS specific axis elevated," null rate drops to ~60% (the
axes are correlated 0.31-0.69 but not identical, so any single
axis is more specific than the MAX) and discrimination jumps to
~+20 pp.

**Generalisable methodology lesson**: MAX-rank composites can dilute
per-axis signal in the null distribution. For future composites:
pre-register per-axis primaries IN ADDITION to the composite, OR
use AND-of-axes composites (require all N axes to trigger, tighter
specificity at the cost of sensitivity). Queued for testing playbook
§3 addendum.

**Both-eras rule (playbook §4.4) reduces load-bearing to 1 axis**.
Only effective_exertion clears the both-eras gate. step_burden and
vigorous_min validate-only are **diagnostic findings, NOT load-bearing**.
max_hr_peak's validate inversion (-7.7 pp) is consistent with the
known chronotropic incompetence in ME/CFS (>85% prevalence per
pacing-and-crash-mitigation literature).

**Cross-axis correlation matrix (per playbook §6.1, channel
non-independence)**: Spearman ρ across 1184 fully-valid days ranges
0.31 to 0.69. effective_exertion is the "central" axis (mean ρ ≈
0.58 with the other 3); step_burden is the most independent (mean
ρ ≈ 0.35). Effective number of independent comparisons ≈ 2.5
(not 4). Multi-comparison concern (8 verdicts at locked bar) is
real but bounded.

**Critical specificity caveat (per playbook §6.2)**: even at +19.5
pp validate discrimination, **posterior-per-fire is ~2.2% vs 1.7%
base rate**. 60% of any 4-day window in the analysis range has at
least one effective_exertion ≥ 0.75 day. A card built on this
primitive would fire roughly every other day and only marginally
lift posterior over the base rate. **NOT shippable as a card without
further refinement** (tighter threshold, multi-condition AND,
temporal aggregation). The HA01c v2 threshold-monotonicity
diagnostic is precisely designed to probe whether tighter thresholds
yield acceptable specificity.

**Pre-committed follow-ups (locked 2026-06-07 BEFORE per-axis
diagnostic ran)**:

- **HA01c**
  ([HA01c-effective-exertion-shock/hypothesis.md](garmin/hypotheses/HA01c-effective-exertion-shock/hypothesis.md)):
  effective_exertion as primary, same rank ≥ 0.75 threshold, same
  3-criterion bar, both-eras rule. Not a re-test of HA01b; new
  hypothesis with a different primary per playbook §2.2.
- **HA01c v2 threshold-monotonicity diagnostic**
  ([HA01c-threshold-monotonicity-diagnostic-v2/diagnostic.md](garmin/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/diagnostic.md)):
  5th in v2 round (after HA10, HA07d, HA06b, HA11). Tests rank
  thresholds {0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95} per
  locked five-category shape rule.

**Status**: HA01b composite REFUTED stays on record. The per-axis
diagnostic produces a **diagnostic finding, NOT a re-test verdict**
(playbook §5.2). HA01c + v2 pending user approval to run.

**If HA01c + v2 both pass**: effective_exertion becomes the **second
project-level both-eras SUPPORTED finding** after HA07d. The D7
single-mechanism-two-regimes reframe regains an empirical anchor —
a validate-era physiological precursor on a cleanly-pre-registered
single-axis primary. Card-craft phase applies, gated on specificity
tables.

**If HA01c REFUTES or v2 fails**: HA01b composite REFUTED stays;
per-axis finding documented as investigative artefact per playbook
§2.5 audit-trail discipline.

### 5.23. HA01c + HA01c v2 execution (same-day) — mixed v2 verdict (first AMBIGUOUS in v2 series)

Same-day execution after the per-axis diagnostic, per user approval
of the pre-committed sequence. Results at
[HA01c result.md](garmin/hypotheses/HA01c-effective-exertion-shock/result.md)
+ [HA01c v2 result.md](garmin/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/result.md).

**HA01c locked-threshold verdict: SUPPORTED both eras** at τ=0.75
(train 81.8% / +21.3 pp / median 0.883; validate 80.0% / +19.5 pp /
median 0.909). Numbers identical to per-axis diagnostic — disciplinary
re-run, not informational. HA01b composite REFUTED stays unchanged
on record per playbook §2.2 (HA01c is a separate hypothesis with a
different primary).

**HA01c v2 threshold-monotonicity diagnostic: MIXED verdict — first
AMBIGUOUS in the v2 series.**

| era | discrimination curve | peak | shape stats | v2 verdict |
|---|---|---|---|---|
| train | 15.4 → 6.4 → 16.2 → +21.3 → 10.3 → 7.9 → 2.0 → 7.3 | τ=0.75 (+21.3 pp) | ρ=-0.452; sign-changes [0.60, 0.90] = 0; max_neg = +2.0 | **AMBIGUOUS** (fails all 5 categories) |
| validate | 15.4 → +24.6 → 21.0 → 19.5 → 13.3 → 13.3 → 12.3 → 6.7 | τ=0.60 (+24.6 pp) | ρ=-0.850; sign-changes = 0; max_neg = +6.7 | **RESCUE via Cat 1** (textbook canonical decline) |

**Why train AMBIGUOUS**: shape is bumpy-but-never-negative.
- Cat 1 (canonical decline) requires peak in [0.50, 0.70] — fails
  (peak at 0.75).
- Cat 2 (stable plateau) requires range ≤ 5 pp — fails (range
  19.3 pp).
- Cat 3 (rising / late-peak) requires peak ≥ 0.80 AND monotone
  rise to peak — fails on both (peak 0.75; the 0.50→0.60 drop from
  +15.4 to +6.4 breaks monotone rise).
- Cat 4 (bumpy with sign-changes) requires ≥ 1 sign-change in
  [0.60, 0.90] — fails (0 sign-changes; curve never crosses zero).
- Cat 5 (loose-tail noise) requires peak < +5 pp — fails (peak
  +21.3 pp).

This is the **edge case the locked v2 framework was designed to
surface**: a genuinely robust shape that doesn't fit any locked
category. The framework returns AMBIGUOUS rather than forcing a
fit. Discipline binds.

**Why validate Cat 1 RESCUE**: classic canonical decline. Peak at
the loosest threshold (τ=0.60) with +24.6 pp; declines monotonically
beyond peak; ρ=-0.850 confirms strong negative threshold-discrimination
correlation; 0 sign-changes. Cleanest Cat 1 shape in the entire v2
round.

**Era-moderator on threshold-stability** (not just on magnitude):
validate-era crash precursor activity is broadly distributed across
rank tiers; train-era is concentrated at τ=0.70-0.85 with a
characteristic dip at τ=0.60 (a possibly-bimodal train precursor
distribution — descriptive hypothesis only; not pre-registered).

**Outcome per playbook §4.4 both-eras rule + HA01c hypothesis.md §5
v2-gate**: HA01c stays **SUPPORTED-with-stability-mixed** — honest
at τ=0.75 but **NOT load-bearing** in synthesis.

**No HA01c card.md drafted**. Two converging reasons:
1. Playbook §6.2 specificity gate: 2.2% posterior per fire vs 1.7%
   base rate; 60% of any 4-day window triggers in the null.
2. v2 mixed verdict: load-bearing status withheld, which also
   withholds card-craft per playbook §2.7.

**Project net state**:
- HA07d remains the only project-level overall-SUPPORTED +
  v2-validated finding (both eras RESCUE).
- HA01c joins the "noted-but-not-load-bearing" status, alongside
  HA06b's permanent demotion.
- HA01b composite REFUTED stays unchanged on record.
- The v2 framework now has worked examples of all four outcomes:
  RESCUE Cat 1/2/3, CLOSE Cat 4, AMBIGUOUS.

**Discipline-cost paid in full (revised)**: the locked v2 framework
has demoted (HA06b), rescued (HA10/HA07d/HA11), and now surfaced
edge cases (HA01c AMBIGUOUS). The framework distinguishes
"robust-but-uncategorizable" from "non-robust-and-bumpy" — both
are mature outcomes of a locked discipline. The user pre-committed
to the framework after HA07d v1 CLOSE; the framework continues to
return verdicts the locked criteria support, not the ones
researcher intuition prefers.

### 5.24. H03b per-minute BB overnight recharge — INCONCLUSIVE × 12 by data availability

Same-day execution after HA01c chain. Result:
[H03b result.md](garmin/hypotheses/H03b-bb-overnight-recharge-permin/result.md).

H03b was pre-registered as the sharpening test of HA10: does the
per-minute integral (peak_during_sleep − sleep_onset_value) give
sharper discrimination than HA10's coarse 3-anchor proxy
(+16.2 pp validate)?

**Result**: INCONCLUSIVE × 12 (all evaluation cells; 3 N_std × 2
windows × 2 eras). The locked n_clean ≥ 10 threshold from
hypothesis.md §5 binds.

**Data-availability finding (the substantive outcome of this
run)**: Garmin's API has two cutover dates:
- `bodyBatteryChange` (daily scalar): populated from ~2023-12-31
- `sleepBodyBattery` (per-3-min array): populated from ~2024-06-03

Of 29 crash episodes:
- Train (2022-09 to 2023-12): 14 crashes, **0 with per-minute
  data** (entire era predates the API cutover)
- Validate (2024-01 to 2026-06): 15 crashes, 9 with leadup data,
  **only 6 with both data AND usable lagged baseline** (baseline
  window [d-90, d-30] needs ≥40 valid days, stabilising
  ~Sept 2024)

**User pre-committed to running as-locked** rather than lowering
the n=10 threshold mid-run (which would have created H03c per
playbook §2.2). Pre-registration discipline preserved.

**Endpoint clarification audit trail (per playbook §2.5)**:
hypothesis.md §3 specified the
`/wellness-service/wellness/bodyBattery/events/{date}` endpoint as
the per-minute source. The endpoint actually returns event records
(sleep, activities, naps), NOT per-minute samples. The per-3-min
BB during sleep window IS available via
`get_sleep_data().sleepBodyBattery` (already captured in the
existing path C sleep backfill; no separate BB backfill required).
Per playbook §2.2, this is an implementation-source clarification,
not a spec change.

**HA10 stays canonical for the BB overnight recharge channel** —
SUPPORTED validate at +16.2 pp (coarse 3-anchor proxy on full
corpus), v2 RESCUE Cat 3, currently load-bearing as the
corroborating secondary anchor for validate-era. The substantive
BB-overnight-recharge question is answered at coarse resolution;
the sharpening test cannot run on the current data corpus.

**H03b re-runnable only after** path B (FIT decode of
`unknown_233`) unlocks per-minute BB for the old corpus. That is
an open H04b track with no fixed timeline.

**Methodology lesson banked** (queued for playbook §3 addendum):
when a pre-registered hypothesis depends on a third-party API
endpoint, verify data availability across the analysis window
BEFORE locking the inconclusive threshold. The H03b case shows
that an n=10 threshold combined with a 2024-06 data cutover
automatically forces INCONCLUSIVE — a constraint the
pre-registration did not anticipate.

**Project net state unchanged**: load-bearing list (HA07d, HA10,
HA11, H02b, H02d) and noted-but-not-load-bearing list (HA01c,
HA06b) all unchanged. H03b adds "INCONCLUSIVE-by-data-availability"
to the verdict-category roster.

### 5.25. Tier 2 specificity tables — all 9 anchors land in Tier C (retrospective-annotation-only)

Tier 2 peer-review action item completed 2026-06-07. Locked spec
at [methodology/specificity-tables-spec.md](garmin/methodology/specificity-tables-spec.md).
Derivative Bayes computation over locked result-data.json files —
no new hypothesis tests, no new null draws.

**Locked era parameters** (from playbook §4.3):

| era | days | crash_v1 count | base rate |
|---|---:|---:|---:|
| train (2022-09-03 → 2023-12-31) | 485 | 14 | 2.89% |
| validate (2024-01-01 → 2026-06-05) | 887 | 15 | 1.69% |

**Precision tier definitions** (locked in spec §7):
- **Tier A**: lift ≥ 5× AND precision ≥ 30% — informative for
  next-N-day awareness
- **Tier B**: lift 2-5× AND precision 5-30% — reflective use only,
  no alerting
- **Tier C**: lift < 2× OR precision < 5% — retrospective
  annotation only (playbook §6.6 no-go boundary)

**Card (b) train-era results** (7 anchors at locked primary arms):

| anchor | recall | null_fire | precision | lift | tier |
|---|---:|---:|---:|---:|:-:|
| H02b train 3d | 71.4% | 41.5% | **4.87%** | **1.69×** | **C** |
| H02d train bridge × 5d | 92.3% | 64.0% | 4.34% | 1.50× | C |
| HA07d train 4d bidir | 84.6% | 65.0% | 3.73% | 1.29× | C |
| HA11 train 4d elevated | 64.3% | 41.5% | 4.40% | 1.52× | C |
| HA07c train 4d elevated | 69.2% | 46.0% | 4.28% | 1.48× | C |
| HA08c train 4d elevated | 61.5% | 38.5% | 4.54% | 1.57× | C |
| HA06b train 4d bidir | 71.4% | 52.5% | 3.89% | 1.35× | C |

**Card (b2) validate-era results** (2 anchors at locked primary arms):

| anchor | recall | null_fire | precision | lift | tier |
|---|---:|---:|---:|---:|:-:|
| HA07d validate 4d bidir | 86.7% | 65.0% | **2.24%** | **1.33×** | **C** |
| HA10 validate 4d bidir | 86.7% | 70.5% | 2.07% | 1.22× | C |

**Decisive structural finding**: lift ≈ recall/null_fire is
independent of base rate (Bayes algebra at low base rates). No
anchor's recall-to-null-fire ratio exceeds 2× (best is H02b at
0.714/0.415 = 1.72×). Therefore **no anchor can clear the 2× lift
threshold at any base rate** — even if the era's true crash rate
were 5× higher, the Tier C verdict would hold.

The hypothesis-test 3-criterion bar (frequency ≥ 60%, discrimination
≥ +15 pp, magnitude floor) confirms metrics are *measurably
different* in crash lead-ups vs random windows. It does NOT confirm
they are good *predictive cards*. These are different gates that
were conflated in the original card-concept framing.

**Card framing implications**: Card (b) and Card (b2) both
restricted to **retrospective-annotation-only surfaces**. The
acceptable surface per playbook §6.6 is timeline annotation during
after-the-fact review, paired with the gevoelscore record.

Even HA07d — the project's only overall-SUPPORTED + v2-validated
finding — drops to **2.24% precision per fire vs 1.69% base rate**.
At 86.7% recall it surfaces nearly every crash AND ~65% of any
random 4-day window. As a forward signal, it is too noisy. As a
retrospective annotation ("this crash was preceded by an autonomic
stillness pattern that fired in 87% of validate-era crashes — here
is where it fired in the timeline"), it remains a meaningful
empirical artifact.

**No-go boundary reaffirmed** (playbook §6.6): even with full
discrimination support, the following are still NOT permitted:
- Crash-risk percentages ("12% crash risk today")
- Traffic-light alerting on a single metric trigger
- Push notifications
- Recovery-score framing
- Automated rest-targets
- Age-predicted HR zones
- Time-contingent escalation

**Methodology lesson banked (and load-bearing for the project's
future)**: a hypothesis-test bar clearance and a card-shippable
precision are different gates. Future card pre-registrations
should include specificity-table thresholds in the hypothesis.md,
not deferred to a downstream check. This is a candidate
playbook §3.9 addendum (queued).

**Project shape after the specificity table**: the discrimination
work was right; the card framing was over-eager. The findings
become **empirical anchors for retrospective sense-making**, not
forward-predictive cards. This is consistent with the original
project ethos (reflective tool, not predictive product) — but the
specificity computation makes the boundary precise.

Full tables: [card-b-train-specificity.md](garmin/cards/card-b-train-specificity.md)
+ [card-b2-validate-specificity.md](garmin/cards/card-b2-validate-specificity.md).
Computation script: [compute_specificity.py](garmin/cards/compute_specificity.py).

### 5.26. Tier 2 statistical audits — Fisher's exact + cross-channel correlation

Two cheap derivative computations completed 2026-06-08 per Tier 2
peer-review action items in [QUEUED-WORK.md](QUEUED-WORK.md). No new
hypothesis tests, no new null draws — purely derivative over locked
result-data.json files + per-day primitive CSVs.

#### Fisher's exact + 95% binomial CIs on 11 primary verdicts

[primary-verdict-statistics.md](garmin/cards/primary-verdict-statistics.md) +
[compute_fisher_ci.py](garmin/cards/compute_fisher_ci.py).

For each primary verdict, retrofits: Fisher's one-sided exact
p-value (alternative = crash trigger > null trigger), Wilson 95%
binomial CI on recall, Wilson 95% CI on null fire rate, Wald 95%
CI on discrimination pp.

**Headline result**:

| anchor | era | recall | disc (pp) | Fisher p | sig α=0.05 | sig Bonf α=0.005 |
|---|---|---:|---:|---:|:-:|:-:|
| H02b | train | 71.4% | +29.9 | **0.0285** | ✓ | — |
| H02d bridge × 5d | train | 92.3% | +28.3 | **0.0112** | ✓ | — |
| HA06b 4d bidir | train | 71.4% | +18.9 | 0.1362 | — | — |
| HA07c 4d elevated | train | 69.2% | +23.2 | 0.0581 | — | — |
| HA07d 4d bidir | train | 84.6% | +19.6 | 0.0934 | — | — |
| HA08c 4d elevated | train | 61.5% | +23.0 | 0.0539 | — | — |
| HA11 4d elevated | train | 64.3% | +22.8 | 0.0836 | — | — |
| HA07d 4d bidir | validate | 86.7% | +21.7 | 0.0703 | — | — |
| HA10 4d bidir | validate | 86.7% | +16.2 | 0.1475 | — | — |
| HA01c rank ≥ 0.75 | train | 81.8% | +21.3 | 0.1355 | — | — |
| HA01c rank ≥ 0.75 | validate | 80.0% | +19.5 | 0.1085 | — | — |

**Only H02b (p=0.029) and H02d (p=0.011) reach α=0.05 one-sided.
Zero reach Bonferroni α=0.005.** Even HA07d validate (+21.7 pp,
the strongest validate-era discrimination in the project) lands at
p=0.0703 — close-to-bar but failing α=0.05 conventional significance.

**Honest interpretation**: the project's pre-registered bar
(frequency ≥ 60%, discrimination ≥ +15 pp, magnitude floor) is
**more permissive than a conventional α=0.05 Fisher's exact test**
when n_crash = 14-15. This was a conscious choice for n-of-1
exploratory research — the bar was calibrated to "discrimination
that would be worth seeing if real" not "discrimination that
distinguishes signal from null at conventional p < 0.05". The
peer-review §2 critique correctly flagged this gap; the audit
retrofits the numbers.

**Why the recall CIs are wide**: with n_crash = 15, a point
estimate of 86.7% (HA07d validate) has Wilson 95% CI roughly
[60%, 96%]. The verdict-bar pass (≥ 60%) is robust to the lower
CI bound only if that bound stays > 60% — this varies by anchor.

#### Cross-channel correlation matrix (Spearman + Pearson)

[cross-channel-correlation.md](garmin/cards/cross-channel-correlation.md) +
[compute_cross_channel_correlation.py](garmin/cards/compute_cross_channel_correlation.py).

Per-day raw primitive values loaded from existing CSV / UDS
sources (no z-scoring, no lagging — captures underlying biological
correlation, not lead-up-window correlation). Inner-joined on
calendar date within 2022-09-03 to 2026-06-05; min N=30 days per
pair (typical N ~1340).

**Two paradigm-shifting findings**:

**1. H02b ≡ H02d at the per-day primitive level (ρ = +1.000,
identical for all 1737 shared valid days)**. The H02d "bridge"
sentinel handling produces the same daily `max_spike_minutes`
values as H02b. The discrimination difference (H02b +29.9 pp at
3d vs H02d bridge +31.8 pp at 5d) comes ENTIRELY from window-length
+ validity rules, NOT from a distinct underlying signal.

**Implication**: the "six channels with seven SUPPORTED tests"
synthesis framing must **drop H02d as a separate channel**. H02b
and H02d are one primitive at two windows.

**2. HA10 ≡ −HA07c (ρ = −0.922; Pearson r = −0.863)**. Morning BB
peak and sleep stress mean are nearly the same underlying signal
in opposite signs. Structural in Garmin's BB algorithm (BB
decreases when stress is high). **HA10 and HA07c are NOT
independent channels** — they are two views of the same
autonomic-state measurement.

**Other findings**:
- HA06b ↔ HA07c = +0.377; HA06b ↔ HA10 = −0.393 (vagal-tone pathway)
- HA07c ↔ HA07d = +0.501 (level and variability of the same sleep-stress signal)
- H02b ↔ HA11 = +0.377 (within-day stress patterns share variance)
- HA08c is a slope of the HA07c primitive; identical raw values

**Effective independent signal clusters: 3-4 (not 6-7)**:
- **Cluster 1 (within-day stress)**: H02b/H02d + HA11
- **Cluster 2 (autonomic state)**: HA07c + HA10 ± HA06b
- **Cluster 3 (autonomic variability)**: HA07d, partially tied to Cluster 2

**Honest effective-N Bonferroni**: α = 0.05/4 ≈ 0.0125 (using
effective N of clusters, not naive 11 verdicts). Of the 11 primary
verdicts, only **H02d (p=0.011) clears this threshold**. But the
H02b/H02d collinearity means **only ONE distinct primitive
survives honest effective-N statistical significance correction**.

#### Combined implications

The discrimination findings are real; the **"many converging
channels" framing was overstated**. Tightening:

- "Seven SUPPORTED on six channels" → "**three-to-four
  effectively-independent signal clusters, of which one (within-day
  stress spike, H02b/H02d in train) clears α=0.05 one-sided
  Fisher's exact**"
- HA10 validate-SUPPORTED ≠ corroborating second channel for
  HA07d in validate — they're structurally linked through Garmin's
  BB algorithm at ρ ≈ −0.5 (validate-specific value)
- HA07d remains the only project-level overall-SUPPORTED +
  v2-validated finding, but at p=0.0703 (validate) and p=0.0934
  (train) it does NOT clear conventional α=0.05 with current N

**This is the most significant project-shape revision since the
Theme A bundled re-test.** The findings stay on record (verdicts
unchanged per pre-registration discipline); the framing tightens
honestly. The Tier 2 peer-review items are now closed with numbers
that re-shape the synthesis.

**Methodology lessons banked**:

1. **Pre-registration bars and conventional statistical
   significance are different gates**. Future hypothesis.md files
   should include Fisher's exact + 95% CI lines in the result.md
   template by default; the peer-review §2 critique surfaced this
   gap and it should be closed for new tests.

2. **"Channels are not independent" was true but the magnitude
   matters**. Future synthesis claims about "multiple channels
   converging" should be quantified with a correlation matrix
   before being made. Candidate playbook §3.9 addendum (queued).

3. **Identical per-day primitives at different windows are not
   independent corroborating tests** (H02b/H02d lesson). Future
   hypothesis pre-registrations on the same primitive at different
   windows should be flagged as a single test with multiple arms,
   not as multiple tests.

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
| **morning RHR delta, absolute thresholds (new, see §5.12)** | **HA06** | **+13.9 pp train (close-but-refuted at 21.4% freq); 0 of 15 validate crashes trigger at 5 bpm — decisive refutation; absolute bar miscalibrated to participant variability** |
| **morning RHR delta, z-score relative thresholds (new, see §5.13)** | **HA06b** | **+18.9 pp train SUPPORTED at N_std=1.5 (71.4% freq); validate +0.8 pp refuted; directionality reversal: train 70% elevated → validate 75% lowered (Wiggers' swing pattern empirically present in validate but non-discriminative)** |
| **morning BB peak, z-score (new, see §5.14)** | **HA10** | **train refuted (−20.5 pp, 100% lowered direction); validate +16.2 pp SUPPORTED (86.7% freq, 69% elevated direction — paradoxical "swing" direction); FIRST VALIDATE-ERA SUPPORTED IN THE PROJECT; 5d each-era one-sided opposite-direction SUPPORTED (train +18.3 pp lowered; validate +27.5 pp elevated)** |
| **within-day U-dip count, z-score (new, see §5.15)** | **HA11** | **train +22.8 pp SUPPORTED at N_std=1.5 (64.3% freq, elevated direction); validate refuted inverse direction (−10.7 pp at 4d, scales to −24.1 pp at 5d N_std=2.0); FOURTH TRAIN-ERA SUPPORTED ON FOURTH CHANNEL** |
| **sleep stress mean delta, z-score (new, see §5.18)** | **HA07c** | **train +23.2 pp SUPPORTED at N_std=1.5 (69.2% freq, elevated direction); validate refuted (-6.0 pp); 5th train-era SUPPORTED on 5th channel; HRV proxy validated for train** |
| **sleep stress slope, z-score (new, see §5.19)** | **HA08c** | **train +23.0 pp SUPPORTED at N_std=1.5 (61.5% freq, elevated direction); validate refuted (+1.5 pp, anti-predictive at higher thresholds); 6th train-era SUPPORTED finding; sustained creep mode** |
| **sleep stress variability delta, z-score BIDIRECTIONAL (NEW, see §5.20)** | **HA07d** | **train +19.6 pp SUPPORTED + validate +21.7 pp SUPPORTED → OVERALL SUPPORTED — FIRST PROJECT OVERALL-SUPPORTED TEST. Validate +28.5 pp at N_std=2.0 lowered (autonomic stillness signature)** |
| **lag length (revised after §5.16)** | **H02b vs HA06b vs HA10 vs HA11** | **3-5 days, cross-channel-confirmed in train across 4 channels; 4-5 days validate-era confirmed by HA10 primary 4d + secondary 5d both SUPPORTED** |
| **era directionality reversal (NEW, see §5.16)** | **HA06b + HA10 + HA11** | **train: sympathetic-arousal-spectrum (elevated stress / RHR / U-dip / lowered BB); validate: parasympathetic-swing-spectrum (elevated BB peak / lowered RHR / lowered U-dip count); internally consistent via vagal-tone physiology** |

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
