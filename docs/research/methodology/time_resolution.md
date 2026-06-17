# Time-resolution methodology — picking the right scale

*Producer-mode methodology MD. Drafted 2026-06-14. **Framework, not a hypothesis.** Sister to [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) (which segments by stratum, not by scale) and [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md) (an instance at one specific scale). The discipline here is for choosing the time resolution of an analysis from the mechanism it claims to address; it is not itself an analysis at any scale.*

---

## Citation status

This MD runs on first-principles reasoning plus the project's prior conventions. Candidate statistical / methodological references (SCED time-series standards in Daza 2018, WWC 2022, Natesan Batley 2023; wavelet vs nested-window vs frequency-domain in time-series methodology; autonomic / circadian analysis-window conventions) have **not** been read or verified in our literature folder. They are listed in [`queued_work.md`](queued_work.md) as a fetch-and-verify task. Until those refs land, the literature row of the §11 four-input reasoning is honestly downgraded to "deferred". The methodological reasoning stands on its own and does not depend on any specific paper.

---

## 1. What this MD is, what it is not

**Is.** A framework for picking the time-resolution of any given analysis on this corpus. Inventories the scales that actually exist in the data, names how those scales can confound each other, and states the discipline for choosing.

**Is not.** A hypothesis. Not an analysis at any specific scale. Not a corpus-wide commitment to one resolution. Specific hypothesis instances at specific scales already exist — [P6 post-crash 5-day window](../personal_hypotheses.md#p6-post-crash-window--distinctive-autonomic-recovery-shape), [P7 recent-crash-density 14d](../personal_hypotheses.md#p7-recent-crash-density-predicts-elevated-crash-risk), [HA11 within-day stress U-dip](../analyses/hypotheses/HA11-stress-udip/), the [intervention-effects 90d windows](intervention_effects_descriptive.md) — and this MD is what they cite for *why* their scale is what it is.

The four inputs of [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) (best-practices standards, established literature, our own vision on tradeoffs, our research limitations + objectives) are worked through in §11.

---

## 2. The scale inventory

Four scales matter on this corpus. **Per-week is deliberately not on the list**: multi-day window lengths are situational and evidence-based per hypothesis (see §2.3), not a generic "weekly" grain.

### 2.1 Per-minute (raw FIT substrate)

The Garmin `monitoring_b` FIT files store HR, stress, and Body Battery samples at minute cadence (sometimes finer for HR; see §7 sub-minute note). The shared [`Monitoring16Resolver`](../analyses/garmin_exploration/scripts/fit_utils.py) expands `timestamp_16` to real datetimes; everything downstream of that resolver is per-minute or coarser by construction.

**Mechanism this scale is sensitive to.** Within-day autonomic dynamics: stress spikes, HR sustained-elevation runs, Body Battery rise/drain events. Anything where the *shape* across a day matters, not the daily summary.

**Worked example: Body Battery up-and-down in daytime.** From the [lived-experience braindump §"Garmin notes"](../lived_experience_garmin_pacing_2026-06-14.md#garmin-notes): a daytime nap shows as a BB *rise* mid-day; a steeper-than-expected drain triggers the late-afternoon decision check (P4b). Daily aggregates (`bb_highest`, `bb_lowest`, `bb_during_sleep_value`) describe at most one transition each and miss the multi-event story — a day with multiple distinct recoveries is qualitatively different from a day of continuous drain, and that distinction lives at minute resolution.

**What's operationalised at this scale.** [HA11 stress U-dip](../analyses/hypotheses/HA11-stress-udip/) (locked); the Wave 4 HR + stress columns in [§8B of DATA_DICTIONARY](../DATA_DICTIONARY.md) (the operational form of [Wiggers A4](../wiggers_testable_hypotheses.md#a4--sustained-multi-hour-rhr-elevation-marks-real-overexertion) and [C4](../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic)). What's pending: per-minute Body Battery (blocked on H04b path C — see [QUEUED-WORK.md](../QUEUED-WORK.md)), the by-time-of-day stress-rest primitive (P5b).

### 2.2 Per-day (the spine)

`per_day_master.csv` — one row per calendar date, 2021-08-16 → today, ~172 columns. Every per-minute primitive that gets summarised into a daily descriptor lives here; so does every label, every external-record-derived flag, every triage-derived value.

**Mechanism this scale is sensitive to.** Anything where the unit of analysis is structurally one day: the subjective state for that day, the autonomic state attributed to that day (per [nightly_attribution.md](nightly_attribution.md)), the categorical label assigned to that day.

**Worked example: `gevoelscore` is inherently per-day.** The participant logs one score per day. The construct itself is daily-resolved; there is no finer truth about how the day felt. Any analysis that wants to predict or co-vary with the score is per-day-bounded on the outcome side. Crash labels inherit this — `is_crash` is a per-day boolean derived from `gevoelscore ≤ 3 for ≥ 2 consecutive days`; the label cannot exist at finer resolution by construction.

**What's operationalised at this scale.** Most active hypotheses — H01-H05, [HA01b](../REJECTED.md), [P1](../personal_hypotheses.md#p1-sleep-window-stress-is-elevated-on-crash-episodes), [P2](../personal_hypotheses.md#p2-wearable-exertion-axis-signals-are-elevated-in-the-4-day-window-before-crash-episodes), [P6 §primary](../personal_hypotheses.md#p6-post-crash-window--distinctive-autonomic-recovery-shape), [P7 §primary](../personal_hypotheses.md#p7-recent-crash-density-predicts-elevated-crash-risk). The default when no other scale is mechanism-motivated.

### 2.3 Situational multi-day windows

Not a generic "per-week" scale. **A category of choice**: per-hypothesis multi-day window lengths picked from the mechanism's natural timescale and from evidence already accumulated on this corpus. The MD records that this category exists; it does not pre-commit any length.

**Mechanism this scale is sensitive to.** Lead-lag, post-event recovery shape, cumulative-load buildup, recovery debt. Phenomena whose timescale is not one day and not months — typically days to a couple of weeks.

**Worked examples (existing instances).**

- **P2's 4-day pre-crash window** ([REJECTED.md HA01b-recomputed](../REJECTED.md)). Mechanistically anchored to the PEM lead-lag literature; lived experience that push days precede felt crashes by several days.
- **P6's 5-day post-crash window** ([P6](../personal_hypotheses.md#p6-post-crash-window--distinctive-autonomic-recovery-shape)). Mechanistically anchored to the multi-day autonomic re-equilibration tail.
  - **Within-window per-channel sub-timings** (added 2026-06-17 per HA-P6 v3 §9 first-branch propagation #4; source: [HA-P6 v3 result.md](../analyses/hypotheses/HA-P6/result.md) at commit `19d33e4` + audit-trail commit `a980b1c` + reader's notes commit `bbcb478`). Within the 5-day post-crash window, the per-channel recovery-completion-day estimates (median day at which the channel returns within 0.5 SD of the `[t0-90, t0-30]` lagged personal baseline) differ across channels: `resting_hr` and `gevoelscore` at t+1.0; `bb_lowest` / `bb_overnight_gain` / `stress_low_motion_min_count_S60_Mlow` at t+2.0; `stress_mean_sleep` and `all_day_stress_avg` at t+3.0. The 2-day spread between the HR-direct channel (`resting_hr` t+1.0) and the two HRV-derived autonomic-load stress channels (`stress_mean_sleep` / `all_day_stress_avg` at t+3.0) is in the direction Wiggers H5 predicts ([wiggers_testable_hypotheses §H5](../wiggers_testable_hypotheses.md#h5--each-metric-has-a-characteristic-lag-vs-exertion-lags-differ-by-metric): HRV-derived signals have longer characteristic lags than HR). The `gevoelscore` t+1.0 estimate is a per-the-classifier read; the actual median z-trajectory is a relapse-and-recover oscillation per HA-P6 reader's notes Note 1 — for downstream mechanism-matching the relapse pattern is the load-bearing characterisation, not the day-1 crossing. Full per-channel + per-channel × phase tables at [`crash_episode_descriptive.md §8`](crash_episode_descriptive.md). Downstream hypothesis tests with specific mechanism claims should pick the channel whose recovery timing matches the claimed mechanism (per HA-P6 v3 §9 first-branch propagation #4).
- **P7's 14-day recent-crash-density window** ([P7](../personal_hypotheses.md#p7-recent-crash-density-predicts-elevated-crash-risk)). Mechanistically anchored to the typical PEM-recovery tail; sensitivity arms 7d and 30d on either side.
- **push_burden_7d_lagged_lcera** ([DATA_DICTIONARY §6](../DATA_DICTIONARY.md#section-6--garmin-exertion-features-engineered)). Operational instance of cumulative weekly load.

The lengths above (4d, 5d, 7d, 14d) are **not interchangeable**. Each is anchored to the mechanism it operationalises. The MD's discipline (§6) requires every pre-reg using a multi-day window to state mechanism + length + why-not-the-neighbouring-length.

### 2.4 Lagged reference frame

Not an analysis scale per se. A **baseline construction** that addresses the coarse-scale reference question: how do you describe "today's load" against a personal baseline that is itself non-stationary?

The canonical construction on this corpus is the `[d − 90, d − 30]` lagged window — 60 days ending 30 days before the candidate day. Excludes the recent push period from its own reference; widely enough to be statistically meaningful; far enough back not to contaminate by an active episode.

**Mechanism this scale is sensitive to.** Slow pacing-effectiveness drift, baseline-shift around interventions, baseline-shift around era transitions. The construction is itself what handles the months-scale reference question; no separate "per-month analysis" needs to exist alongside it.

**Worked example: the v3.2 lagged baseline.** Operationalised because v3.1's trailing-30d rolling baseline broke during sustained pushes (the baseline drifted up with the pushes — see §3 for the worked confound story). Per [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses), `_lagged_lcera` is the default for PEM-pacing tests, `_lagged` is the default for cross-era trajectory work.

The `_lcera` restriction is a *cross between* this scale and the segmentation framework — the baseline restricts to LC-era days only. It is the place where scale (resolution) and segmentation (stratum) meet. §8 cross-references that explicitly.

---

## 3. When a coarser-scale trend distorts a finer-scale read

The canonical worked story on this corpus.

**Sustained-push period rebases the 30d trailing baseline.** In v3.1 the rolling 30-day baseline included the candidate day. During a multi-week push (a vacation, a stretch of late-2023 reintegration work, a build-up week before the Ardennen weekend), the baseline drifted up with the pushes; a slow grind stopped looking heavy at per-day resolution. HA01b's original v3.1 reading appeared SUPPORTED on the validate era (+17.3 pp) and the per-axis decomposition appeared clean. On the corrected v3.2 lagged baseline (`[d − 90, d − 30]`), HA01b-recomputed reads REFUTED on both eras (+5.8 / +4.0 pp). The "supported" verdict was a baseline-contamination artifact, not a mechanism finding. Tracked in [REJECTED.md](../REJECTED.md) row `HA01b-recomputed`; codified as a rule in [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses).

The structural lesson, scale-generalised: when a per-day analysis uses a rolling reference that overlaps with the candidate window, a slow drift in that reference can erase the finer-scale deviation it was supposed to measure. The fix is not to abandon the finer scale; it is to repair the reference frame (§2.4).

---

## 4. When a finer-scale phenomenon distorts a coarser-scale read

Three independent worked stories on this corpus. Each is a different shape of finer-scale-distorting-coarser; the MD records all three because they motivate different mitigations.

**4.1 Daily mean stress dilutes evening rest-stress spikes.** A 5-minute spike of intense stress in a 24-hour day is dilution-invisible to `averageStressLevel`; lived experience is that exactly that shape (intense moment in an otherwise calm day) can trigger crashes. HA11's locked verdict and P5b's evening-amplification framing both depend on minute-resolution detection. [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages) codifies the rule (spike-detecting metrics over daily averages). The per-day-mean reading understates the relationship; the mitigation is to use a minute-resolution-derived per-day descriptor (e.g. `stress_high_duration_min`, `stress_post_peak_time_to_rest_min`).

**4.2 Crash days inflate cross-scale variance and shift correlations.** Layer 3 audit 2026-06-12 found seven cross-family Spearman correlations shift by ≥ 0.15 when `is_crash == True` rows are dropped: `push_burden_7d_lagged_lcera` × `resting_hr` went +0.091 (full) → +0.426 (crash-dropped). The crash days — a finer-scale phenomenon (specific days) — drive a coarser-scale reading (the LC-frame correlation) that isn't there outside crashes. [CONVENTIONS §3.4](../CONVENTIONS.md#34-crash-drop-sensitivity-row-on-every-layer-4-correlation) codifies the rule (every Layer 4+ correlation reports a crash-drop sensitivity row). The coarser-scale reading without the sensitivity check overstates the relationship.

**4.3 Within-day BB multi-event days are lost in daily aggregates.** A day with a morning nap + an afternoon dip + an evening recovery contains three distinct BB transitions. The daily `bb_highest` describes the peak; `bb_lowest` describes the trough; `bb_during_sleep_value` describes the sleep window. None of them can describe the *count* of distinct recoveries — and a multi-recovery day is qualitatively different from a day of continuous drain. [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages) specifies that per-minute BB is *required* and the count of distinct BB-rise events is meaningful in itself. The per-day-aggregate reading misses the multi-event story; the mitigation is to derive a per-day count-of-events from the minute substrate (pending H04b path C).

---

## 5. The third axis: aggregation choice masquerading as mechanism

A distinct structural confound beyond the coarser ↔ finer pair. When a per-day signal has a multi-day window *baked into its construction*, the aggregation choice can look like a mechanism finding if it isn't made explicit.

**Worked example: `is_crash`.** The crash_v2 label is derived from `gevoelscore ≤ 3 for ≥ 2 consecutive days`. The "2 consecutive days" requirement is a 2-day window aggregation, not a mechanism statement. Any analysis on `is_crash` is implicitly analysing days that lie inside a multi-day window of low scores. If a downstream finding describes "crash days have elevated X", part of what is happening is that low-X days adjacent to low-score days are getting selected by the aggregation. The mechanism claim (X *leads to* crash) is not the same as the construction claim (X *co-occurs with* a 2-day window of low scores); the MD requires every pre-reg to surface the latter when it makes the former.

The pattern generalises. `is_dip` (single-day, 1-day window). `crash_episode_id` (variable-length per-episode aggregation). `push_burden_7d` (7-day count window). `effective_exertion_slope_28d` (28-day OLS). Each has a window baked in; each is a candidate for the aggregation-masquerading confound.

**The discipline.** When a hypothesis uses a derived label or rolling primitive, the pre-reg must state: (i) the window built into the label/primitive, (ii) whether that window is the *same as* the hypothesis's claimed mechanism timescale, (iii) what the corresponding raw-substrate reading would show if the window were removed.

---

## 6. The discipline rule

**Mechanism-driven scale choice.** The mechanism's natural timescale picks the analysis scale. Every pre-reg names: the mechanism's claimed timescale, the analysis scale chosen, and the matching reasoning. Decision procedure, not pre-decision.

Concrete matching on this corpus:

| mechanism's natural timescale | analysis scale | examples |
|---|---|---|
| Within-day autonomic dynamics (stress spikes, sustained HR runs, BB rise/drain events) | per-minute → per-day descriptor | HA11, Wave 4 A4 + C4 cols, P5b (pending), P4a/P4b (pending) |
| Per-day subjective state / per-day label outcome | per-day | P1, P2 (composite at t0), most H-register |
| Lead-lag / post-event recovery / cumulative load (days to ~2 weeks) | situational multi-day window (length from mechanism + evidence) | P2 4d, P6 5d, P7 14d, push_burden_7d |
| Slow pacing-effectiveness drift / baseline shift around interventions / cross-era reference | lagged reference frame (§2.4); not a separate analysis scale | every `_lagged` / `_lagged_lcera` column |

**Multi-scale parallel is allowed as descriptive overlay, not as confirmatory pass.** When a finding is borderline or when a §3 / §4 / §5 confound is suspected, a parallel-scale overlay is added as a descriptive sensitivity row. No per-scale confirmatory claim — that would be a multiplicity inflation and a re-litigation of the primary scale-choice after seeing data. The same shape as the M3 sensitivity overlay in [`lc_era_temporal_segmentation.md §2`](lc_era_temporal_segmentation.md#2-the-methodological-question).

**No corpus-wide commitment to one scale.** This MD does NOT say "use scale X for class Y". Picking a scale is a per-analysis decision, not a corpus-wide rule; the inventory exists so pre-regs can name the scale they pick, not so pre-regs inherit a default.

---

## 7. Revision procedure: when a scale-choice turns out wrong

Two parallel mechanisms.

**Audit trail in REJECTED.md.** When a scale-choice produces a result that later turns out wrong (because the baseline was contaminated, the aggregation hid the mechanism, the resolution was too coarse), the wrong reading stays visible in [REJECTED.md](../REJECTED.md) as a row, the corrected reading is computed at the right scale, and both stay in the audit. The HA01b-recomputed / v3.1 → v3.2 transition is the prototype; do not silently substitute. This is the post-hoc half: the lesson is preserved behind us.

**A pre-flight scale-sanity audit hook (proposed for CONVENTIONS §3).** Before pressing go on a hypothesis, the analyst names: (i) the scale chosen, (ii) the mechanism's natural timescale, (iii) a 1-line check on whether the scale is contaminated by a neighbouring scale (coarser-scale rebase risk, finer-scale aggregation risk, aggregation-masquerading risk). This operationalises the discipline as a pre-flight check, sister to existing §3.1–§3.6 audit hooks. **This MD does not unilaterally add the new hook to CONVENTIONS** (CONVENTIONS is producer-locked + needs its own review); the MD *recommends* the addition and surfaces the recommendation in §10.

The pair is belt-and-suspenders: the lesson lives behind us (audit trail) and ahead of us (pre-flight).

---

## 8. Compose with existing methodology

| existing artefact | how this MD composes with it |
|---|---|
| [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) | Sister MD. Segmentation (which days are comparable) is orthogonal to resolution (time-grain of the analysis). The two meet only in the `_lagged_lcera` construction (§2.4), which is a baseline restricted to a stratum. Cross-reference both ways. |
| [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) | The lagged baseline rule. §2.4 of this MD is the framework-level statement of why §3.2 exists. §3 of this MD is the worked story behind §3.2. |
| [CONVENTIONS §3.4](../CONVENTIONS.md#34-crash-drop-sensitivity-row-on-every-layer-4-correlation) | Crash-drop sensitivity. §4.2 of this MD is the scale-generalised framing of why §3.4 exists. |
| [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages) | Spike-detecting > daily means. §4.1 + §4.3 of this MD generalise the rule from "within-day vs daily" to other scale-pairs. Do not restate §3.5; reference. |
| [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md) | An instance at one scale: the `[d − 30, d + 60]` around-intervention window. The 90-day choice is right for that question because the mechanism (post-intervention baseline equilibration) operates at that timescale; this MD's §6 supports the choice. |
| [`personal_hypotheses.md`](../personal_hypotheses.md) (P6, P7) | Specific multi-day-window instances. P6 (5d post-crash) and P7 (14d recent-crash-density) are the §2.3 worked examples. P6 + P7 each should cite this MD for the scale-choice rationale. |
| [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) | Existing tests operate at different scales (H1 is multi-day, HA11 is within-day, A4 is within-day). Should be cross-referenced as "see scale tag" when they cite this MD. Suggested back-update in §10. |
| [`garmin_pacing_practice.md`](garmin_pacing_practice.md) | Behavioural / operational side of within-day usage. The pacing protocol itself operates at within-day grain (per-minute monitoring → per-day decision). Sister to §2.1 here. |

---

## 9. Open questions / deferred

- **Literature row of §11 four-input reasoning is deferred.** SCED time-series multi-scale standards (Daza 2018, WWC 2022, Natesan Batley 2023), wavelet vs nested-window vs frequency-domain in time-series methodology, autonomic / circadian analysis-window conventions. Queued in [`queued_work.md`](queued_work.md) (entry to add); fetch-and-verify task.
- **Sub-minute scale on this corpus.** `monitoring_b` HR samples occasionally land at seconds cadence, but current extraction aggregates to per-minute via `Monitoring16Resolver`. No current operationalisation; HRV beat-by-beat is hardware-blocked on Forerunner 245 ([DATA_DICTIONARY §7B device caveat](../DATA_DICTIONARY.md#section-7b--garmin-physiological-extras-uds-derived-body-battery-all-day-stress-24h-respiration-24h-spo2)). Sub-minute is on the "available but not used" floor; if a future hypothesis needs it, the door is open.
- **A pre-flight scale-sanity audit hook for CONVENTIONS §3.** Recommended in §7 of this MD; not unilaterally added. Needs a separate pass over CONVENTIONS.
- **Back-update of existing hypothesis pre-regs to name their scale.** Suggested in §10. Not run as part of this session.

---

## 10. Back-pointers needed in downstream artefacts

The MD will likely be cited from:

- **Personal-register hypotheses** ([P6](../personal_hypotheses.md#p6-post-crash-window--distinctive-autonomic-recovery-shape), [P7](../personal_hypotheses.md#p7-recent-crash-density-predicts-elevated-crash-risk), future P8+) — each should name its scale + reason. Currently P6 / P7 do not name "5-day window because PEM-recovery tail" / "14-day window because recent-crash-density mechanism" in those words. Add a "Scale" line to the Operationalisation table of each pre-reg.
- **Wiggers register** ([wiggers_testable_hypotheses.md](../wiggers_testable_hypotheses.md)) — existing tests operate at different scales. H1 is multi-day; HA11 is within-day; A4 is within-day; H3 is multi-day. Suggested back-update: add a "Scale" tag to each hypothesis row.
- **`intervention_effects_descriptive.md`** — the 90-day window choice should be re-grounded in this framework. Suggested back-edit: cross-reference §6 of this MD.
- **CONVENTIONS** — if §7's pre-flight scale-sanity audit hook is accepted, add as §3.7.
- **Future descriptive analyses** — every new methodology MD that names a scale references this one.

Back-pointer list surfaced for user decision; not run as part of this session.

---

## 11. Four-input reasoning

### 5.1 Best-practices standards

- **Mechanism-driven scale selection** is the orthodoxy in time-series methodology: the analysis timescale should match the mechanism's natural timescale, not the data's storage granularity. A within-day stress spike analysed at daily mean loses the spike; a months-scale drift analysed at per-day resolution loses the drift to high-frequency noise. The corollary: when a hypothesis spans multiple timescales (a within-day trigger leading to a multi-day crash leading to a recovery-debt build), the analysis decomposes into a sequence of scale-matched sub-analyses, not a single multi-scale super-analysis.
- **Reference-frame correctness is a distinct discipline.** Lagged baselines, jackknifed baselines, exclusion-window baselines all exist because a rolling reference that includes the candidate day is a confounded reference. This is well-established in trend-detection methodology and is the inheritance behind §2.4.
- **Per-mechanism sensitivity to neighbouring scales.** Time-series methodology generally accepts that a finding at one scale should be checked for contamination from neighbouring scales (coarser-scale drift, finer-scale noise, aggregation-window choice). The checks are descriptive sensitivity; they are not per-scale confirmatory passes.

### 5.2 Established literature

**Deferred** (see Citation status). Candidate references queued in [`queued_work.md`](queued_work.md): SCED multi-scale standards (Daza 2018, WWC 2022, Natesan Batley 2023), wavelet vs nested-window vs frequency-domain decomposition, autonomic / circadian analysis-window conventions. The methodological reasoning above does not depend on any specific paper landing.

### 5.3 Our own vision on tradeoffs

| dimension | committed-to-one-scale | mechanism-driven per-pre-reg (CHOSEN) |
|---|---|---|
| Granularity vs statistical power | committed; n is whatever the chosen scale provides | varies per pre-reg; each hypothesis gets the resolution its mechanism warrants |
| Pre-registrability | high (single scale across hypotheses) | high per pre-reg (each names scale + mechanism explicitly) |
| Adaptive observation | low (corpus-wide commitment) | high (multi-day windows are evidence-based per hypothesis) |
| Autocorrelation handling | uniform; may be wrong for some mechanisms | per-mechanism; e.g. crash analyses use per-episode unit, not per-day |
| Discoverability across scales | low (one scale = one window onto the corpus) | high (different mechanisms surface at different scales) |
| Aligned with [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) (caveats yes, a-priori claims no) | mixed (a corpus-wide scale-commitment is a-priori) | aligned (mechanism-driven choice is a decision procedure, not a pre-decision) |

### 5.4 Our research limitations + objectives

- **n-of-1, observational, multi-source, single subject across 4+ years.** No across-subject replication is available; across-time replication on the same subject is the closest we get. Picking a scale that maximises the within-corpus replication signal (multi-day windows where 29 crash episodes give per-event n; per-day where 1755 rows give per-day n) is the discipline. A scale that gives n ≈ 5 per cell is descriptive only.
- **The data substrate is at two raw resolutions.** `monitoring_b` FIT (per-minute, since 2021-08-16) and `per_day_master.csv` (per-day, since 2021-08-16). Everything else (rolling-7d, 28d slopes, 90d lagged, around-intervention 90d) is *derived* from one of these two substrates. The MD's inventory reflects the substrates plus the canonical derivations; it does not invent scales.
- **Forerunner 245 hardware caveat.** HRV beat-by-beat is sensor-blocked on this device (Elevate V3); the sub-minute floor is not currently reachable for HRV-class analyses. This is a limitation of the floor of §2.1, not of the framework.
- **Objective: faithful descriptive characterisation before any inference.** Per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference). A scale-choice that pre-commits the analysis to a mechanism class it has not described is exactly what §2.1 protects against; the framework here is mechanism-driven *per hypothesis*, not mechanism-class-driven across the corpus.

---

## 12. Cross-references

- [CONVENTIONS §2.1, §2.2, §3.2, §3.4, §3.5, §4.1, §4.2](../CONVENTIONS.md) — discipline gates this MD operates inside.
- [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) — orthogonal axis (segmentation, not resolution).
- [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md) — instance at one scale.
- [`personal_hypotheses.md`](../personal_hypotheses.md) — P6, P7 as situational multi-day-window instances.
- [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) — multi-scale tests.
- [`garmin_pacing_practice.md`](garmin_pacing_practice.md) — within-day operational sibling.
- [`lived_experience_garmin_pacing_2026-06-14.md`](../lived_experience_garmin_pacing_2026-06-14.md) — primary-source prior; the multi-scale dynamics framing motivates this MD.
- [`queued_work.md`](queued_work.md) — literature fetch + back-update list.
- [REJECTED.md](../REJECTED.md) — HA01b-recomputed as the prototype audit-trail entry.

---

*Producer-mode methodology MD. Update when a new scale becomes operationalised on this corpus, when the discipline rule needs a refinement, or when the deferred literature row lands.*
