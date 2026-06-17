# Audit: Descriptive research programme scoping (descriptive-programme)

**Target**: [`docs/research/analyses/descriptive/README.md`](../analyses/descriptive/README.md)
**Target commit**: `8e0fce7`
**Reviewer mode**: Claude (independent methodological auditor; fresh session, doc-only knowledge)
**Audit date**: 2026-06-16

## 1. Headline verdict

**PASS-with-caveats.** The two-strand framing is well-motivated and the Q3.x template covers most operationalisation-prerequisite needs the methodology stack requires, but **three substantive gaps** prevent a clean PASS: (a) **data-quality / sensor-event / calibration-drift discipline is structurally absent** (Dimension 2 — D2.1/D2.2/D2.3/D2.6 all silent, with `garmin_indicators_audit.md` not even indexed in §5); (b) **two existing major descriptive artefacts (`lc_phase_descriptive.md`, `garmin_indicators_audit.md`) are missing from §5** and would already pre-answer ~40% of Q3.x.a + the entire D2.6 row (Dimension 6 fire that propagates back into the programme's own scope); (c) **the subjective↔objective coupling thread and the seasonality / day-of-week / sensitivity-to-cutpoints discipline are absent from Strand A's Q-template** (Dimension 4 D4.5 / D4.9 + Dimension 7 D7.2). The first 3 analyses are sensibly chosen and the integration story is coherent at the trajectory level; the caveats sit at the operationalisation-support template and the §5 index, not at the strand framing.

---

## 2. What fires per dimension

### Dimension 1 — Methodological-prerequisite coverage

| check | status | notes |
|---|---|---|
| **D1.1** ACF / effective E[L] per channel | **covered explicitly** | Q3.x.b at [`descriptive/README.md:60`](../analyses/descriptive/README.md#L60) — names ACF + E[L] under [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md). Clean. |
| **D1.2** Stationarity over the analysis window | **missing** (substantive) | Q3.x.b mentions autocorrelation only; rolling mean/variance, structural-break tests (PELT named-and-rejected in `citalopram_phase_stratification.md` §3 but not re-deployed here), and gradual-drift checks are absent. Stationary-bootstrap CIs assume mild non-stationarity at most; the descriptive layer should verify, not assume. |
| **D1.3** Exchangeability for permutation tests | **covered weakly** | Q3.x.d (phase-stratified distribution) addresses the dominant non-exchangeability axis (phase boundaries on CONFIRMED-citalopram channels), but era × phase × dip-cluster interactions are not surfaced. Minor. |
| **D1.4** Distribution shape | **covered explicitly** | Q3.x.a — mean, median, MAD, quantiles, skewness, heavy-tail flag. The most well-specified item in the Q-template. |
| **D1.5** Base rates per phase × era × eligibility cell | **covered weakly** (substantive) | Q3.x.c does *base rates per phase* but the multi-axis cell (phase × era × eligibility-rule), which is exactly the HA-C4b v1 structural-hole lesson recorded in [`hypothesis_lock_process.md` §5](../methodology/hypothesis_lock_process.md#L315), is not explicit. A drafter could compute per-phase n and still lock an unsatisfiable consolidation × train cell. The §7c discipline binding to lock-process gates §5 catches this *at lock time*, but the descriptive prerequisite should provide the cell directly. |
| **D1.6** Personal-baseline / lagged-baseline window length sufficient | **covered weakly** | §2 Strand A bullet 1 says distributions inform "personal-baseline z-score robustness, §7 anchor calibration" but Q3.x.a-f do not explicitly carry a personal-baseline-window-length check (e.g. "does a 30-day window give a stable MAD for this column"). [CONVENTIONS §3.1](../CONVENTIONS.md#L213) and §3.2 are the binding policy but the descriptive verification of *whether the lagged window is long enough for this column* is missing. Substantive — the HA01b-recomputed correction worked example (§3.2 audit hook fire) is the exact pattern this should pre-empt. |
| **D1.7** Crash-drop sensitivity foundation | **covered explicitly** | Q3.x.f calls out Cohen's d + crash-drop sensitivity per CONVENTIONS §3.4. Clean. |
| **D1.8** Spike-detecting metric availability for acute-load hypotheses | **missing** (substantive) | The 3 CONFIRMED-citalopram channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) are *all daily-aggregate channels*. Per [CONVENTIONS §3.5](../CONVENTIONS.md#L326) and the lived-experience anchor (intense moment in an otherwise calm day triggers a crash), spike-detecting primitives are the analytical bar for sympathetic-arousal mechanisms. None of the first 3 analyses surface spike / peak / count primitives — the README's CONFIRMED-citalopram filter privileges level channels and silently buries the spike-metric question into §3.4 ("HA-touched non-confirmed", spun up on need). HA-C4b's `stress_low_motion_min_count_S60_Mlow` is exactly such a spike-count channel and is named in §3.4 as a candidate; it sits behind the CONFIRMED filter and will not get Strand A coverage unless an HA pre-reg blocks on it. |

**Magnitude**: D1.2 + D1.5 + D1.6 + D1.8 are substantive; D1.3 is minor; D1.1 + D1.4 + D1.7 pass cleanly.

### Dimension 2 — Data-quality + outlier + missingness coverage

| check | status | notes |
|---|---|---|
| **D2.1** Outlier detection (isolated vs persistent) | **missing** (substantive) | Q3.x.a's "heavy-tail flag" partially captures persistent shifts but isolated sensor failures / calibration spikes are not explicitly named. Critical because a single Garmin sync error can introduce a spike that distorts the personal-baseline z-score for ±60 days. |
| **D2.2** Sensor change events catalog | **missing** (minor here; substantive in broader programme) | FR245 has been the device throughout 2021-08-16 → present per [`garmin_exploration/README.md:23`](../analyses/garmin_exploration/README.md#L23) so device-swap is N/A here. But firmware updates, CPAP start (likely shifts HR / BB / stress baseline by physical mechanism), watch-strap-tightness drift over years — none are scoped. Strand B Q4.2 covers citalopram cross-channel; the equivalent "non-pharmacological boundary inventory" is absent. |
| **D2.3** Calibration-drift check (non-mechanism drift contaminating personal-baseline z-score) | **missing** (substantive) | This is the HA01b-recomputed correction worked example projected forward: a slow drift in baseline that the rolling-window-inclusive-of-day baseline absorbs. The v3.2 `_lagged_lcera` columns close it operationally; the descriptive verification that no other channel has the same problem is absent. Q3.x.a-f do not include a slow-trend-check column. |
| **D2.4** Missingness patterns (random vs systematic, contiguous vs intermittent, weekend-vs-weekday) | **covered weakly** | Q4.6 names "missingness patterns that matter for hypothesis design" but is deferred to "later phase, not in first 3" at [`descriptive/README.md:166`](../analyses/descriptive/README.md#L166). For Strand A operationalisation support this is too late — the next HA pre-reg blocks before Q4.6 has run. |
| **D2.5** Coverage analysis: date range per column, sub-window coverage, BB bridge case | **covered weakly** | Q4.6 covers; FIT taxonomy in `garmin_exploration/README.md` covers per-minute; `bb_overnight_gain_proxy.md` covers the 2024-07-08 → 2024-09-17 BB bridge. The §5 index acknowledges the partial coverage. Adequate as long as Q4.6 is not too far back. |
| **D2.6** Known data-quality issues catalog | **missing** (blocking for §5 index, substantive here) | [`garmin_indicators_audit.md`](../methodology/garmin_indicators_audit.md) **exists** and is the project's canonical known-issues catalog (per-column provenance + known caveats inventory). It is **not cited in §5** and not referenced by any Strand A or Strand B question. A drafter who relies on this README will miss it. See D6 below. |
| **D2.7** Garmin extract version tracking | **missing** (minor) | The corpus is built from a 2026 GDPR dump; the README says nothing about which dump version each analysis ran against. Per the project pattern (CSV files emitted into the analysis folder), this is implicit but not formalised. Minor for descriptive but could matter for refresh discipline (§7c). |

**Magnitude**: D2.1 + D2.3 + D2.6 are substantive; D2.2 + D2.4 + D2.7 are minor-to-substantive; D2.5 passes weakly. **Dimension 2 is the weakest dimension of the README.**

### Dimension 3 — Cross-channel structure

| check | status | notes |
|---|---|---|
| **D3.1** Full correlation matrix (Pearson + Spearman) across load-bearing columns | **covered** | Q4.5 + `cross-channel-correlation.md`. The README says "Missing: nothing immediately." Defensible *for the existing 7 anchors*; if a new channel enters the load-bearing list (e.g. `stress_low_motion_min_count_S60_Mlow` post-HA-C4b v3), the card needs extension. Worth noting in the refresh trigger (§7c). |
| **D3.2** Near-identity pair detection threshold + flagging (\|ρ\| ≥ 0.92) | **covered** | Q3.x.e at threshold ρ ≥ 0.9. Threshold differs from [CONVENTIONS §3.3](../CONVENTIONS.md#L266)'s ρ ≥ 0.97 definitional-pair bar and the cross-channel card's ρ ≥ 0.92 near-identity bar; a one-line reconciliation in the Q-template would prevent drafter confusion. Minor. |
| **D3.3** Definitional-pair detection (columns derived from each other) | **covered weakly** | Q3.3.h names `bb_lowest` ↔ `bb_overnight_gain` specifically but doesn't generalise the pattern to "before locking the Strand A on a channel, confirm in `pipeline/03_consolidate/build_unified_dataset.py` whether it shares computation path with any other column" per CONVENTIONS §3.3. Minor. |
| **D3.4** Spurious-correlation flag for time-trended pairs | **missing** (substantive) | The existing cross-channel card is computed on raw primitives "we want the underlying biological correlation, not the lead-up-window correlation" ([cross-channel-correlation.md:28](../analyses/garmin_exploration/cards/cross-channel-correlation.md#L28)). Time-trended pairs (e.g. correlation driven by shared 4-year-recovery trajectory) are not flagged. This is the §3.7 trajectory-detrend audit hook applied at the cross-channel level. The intervention-effects MD §8.2 found two raw-test findings collapsing under detrend; the same risk applies to the cross-channel matrix without a detrended companion. |
| **D3.5** Cross-channel timing analysis | **named as gap, deferred** | Q4.2's "Missing" section explicitly names this ("does the SSRI signal hit stress channels first then BB then RHR") and defers it to "later phase, not in first 3." Honest acknowledgement; the deferral is reasonable given that the 3 first analyses focus on a single channel each. |

**Magnitude**: D3.4 is substantive; D3.2/D3.3/D3.5 are minor or honestly-deferred; D3.1 passes.

### Dimension 4 — General descriptive-research best practice

| check | status | notes |
|---|---|---|
| **D4.1** Univariate before bivariate | **covered implicitly** | Q3.x ordering (distribution shape first → autocorrelation → base rates → bivariate phase-stratified / crash-vs-normal) respects this. No explicit statement, but the ordering is correct. |
| **D4.2** Visualisations before tests | **covered weakly** | §6.1/§6.2 Outputs name `findings.md` but don't mandate plots. The `garmin_exploration/<topic>/README.md` precedent has heavy use of figures; presumably this carries forward but worth saying. Minor. |
| **D4.3** Sensitivity checks for arbitrary cutpoints | **missing** (minor) | Q3.x.f's crash-drop is a sensitivity check; window-length, threshold-cutpoint, and era-boundary-buffer sensitivities are not generalised into the Q-template. CONVENTIONS §3.4/§3.7 + the §5 sanity-check rows in `hypothesis_lock_process.md` carry them at the test layer; surfacing one row in the Q-template would close the gap. |
| **D4.4** Exploratory vs confirmatory positioning + pre-registration / data-peeking risk for downstream HA pre-regs | **covered weakly** (substantive) | §8 "IS NOT a hypothesis pre-reg; descriptive only" is correct as far as it goes. But [CONVENTIONS §4.2-4.3](../CONVENTIONS.md#L573) draws a stricter line: descriptive findings that influence HA pre-reg drafting risk lifting confounder-acknowledgment into analytical-basis (the a-priori-class fire). The §7b lock-process integration ("HA pre-reg §3 cites the relevant Strand A analysis") is the right binding but the risk is not surfaced. A drafter could over-anchor a §7 sanity-check range to Strand A's distribution and call that "anchored to data" when it's really "anchored to a non-pre-registered exploratory pass." A one-paragraph caveat would close this. |
| **D4.5** Heterogeneity / Simpson's-paradox check (pooling-vs-stratified) | **missing** (substantive) | Q3.x.d handles phase × pooled stratification specifically. Other axes that have produced Simpson's-paradox-shaped reversals on this corpus — HA10's train −20.5 pp / validate +16.2 pp directional reversal being the worked example — are not generalised. A "pooled-vs-stratified across the locked axes (phase, era, dip-cluster, season)" check would address this. |
| **D4.6** Survivor / selection bias documentation | **missing** (minor) | The Q-template doesn't enumerate exclusions per analysis (eligibility windows, coverage gates, the Stratum 4 frame). The frame inheritance from `lc_era_temporal_segmentation.md` makes this less acute but the exclusion-count-per-Q row is absent. |
| **D4.7** Reproducibility (versioned data, scripts, seeds, refresh) | **covered weakly** | §6's `run.py` per-analysis output + §7c refresh cadence partially cover this. Seeds, data-version-pinning, and the per-analysis emit-CSV pattern are not formalised. The `garmin_exploration/<topic>/` precedent (run all three scripts in order from the repo root) is the implicit model. Minor for descriptive. |
| **D4.8** Long-run vs short-run pattern separation | **covered weakly** | Q4.1 recovery_arc is multi-year; within-year variation is NOT explicitly distinguished. The headline finding "peak 2023 → trough 2025 → uptick May 2026" is the long-run; the year-internal variation (the "trough 2025" detail) is implied. Minor-substantive — explicit separation in `findings.md` is what readers need. |
| **D4.9** Time-of-year / seasonal + day-of-week effects | **missing** (substantive) | The README is silent on seasonality and DOW effects. Yet the v3 citalopram multi-channel work *used the spring-2025 control to rule out seasonality* ([STOCKTAKE.md:111](../STOCKTAKE.md#L111)); the question "does this channel show a seasonal cycle independent of LC era" is therefore demonstrably load-bearing for the project's inference. Strand A should carry a seasonality + DOW check as a standard companion column. |

**Magnitude**: D4.4 + D4.5 + D4.9 are substantive; D4.2/D4.3/D4.6/D4.7/D4.8 are minor or weakly-covered; D4.1 passes.

### Dimension 5 — Sufficiency for the HA-* pipeline

| check | status | notes |
|---|---|---|
| **D5.1** HA-C4b v1 halt diagnosis: would the planned stack carry a §7-anchor-source distribution for the EXACT column under test? | **covered for first 3 analyses; structurally vulnerable elsewhere** | §6.1 `stress_mean_sleep` does Q3.1.a-f for the exact column — would catch a [15, 60] miss on this channel. But `stress_low_motion_min_count_S60_Mlow` (the actual HA-C4b column) sits in §3.4 "HA-touched non-confirmed, spin up only on need." If a Wiggers HA-C4b v3 / HA10 v2 hits before that Strand A analysis is spun up, the §7-anchor fire reoccurs. §7b says "spin one up first if missing" — that closes it operationally if the discipline holds, but the README would be stronger if §3.4 was promoted to "pending, ordered by HA-* queue" instead of "spin up only when needed". |
| **D5.2** HA07c train/validate divergence reinterpretation | **covered** | §6.1 `stress_mean_sleep` first analysis covers Q3.1.d phase-stratified — the citalopram step as non-rejected confound class is exactly the §5.A/§5.B/§5.C treatment per `citalopram_phase_stratification.md` §6. Strong. |
| **D5.3** HA-P7 §4.5.4 covariate-sensitivity diagnostic generalisation | **missing** (substantive) | HA-P7's §4.5.4 (`gevoelscore_lagged_mean_14d` covariate attenuating crash_count_14d's β) was the load-bearing diagnostic that flipped "recovery-debt mechanism" to "recent-low-gevoelscore proxy". No Strand A Q surfaces "what other channels have a covariate-sensitivity-vs-autocorrelation-confusion risk?" The diagnostic is in the methodology stack but the descriptive layer doesn't pre-empt it for the next HA pre-reg. |
| **D5.4** HA-C3 / HA-C4 Tier 1 Wiggers operationalisation-support mapping | **covered partially** | §3.2 `all_day_stress_avg` is named as HA-C3 candidate. HA-C4's 3-channel stress-decay-triad channels are not enumerated. A drafter would need to read [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) to know which channels HA-C4 touches, then check whether Strand A coverage exists. A mapping table in §6.3 candidates → C3/C4 column list would close this. |
| **D5.5** HA-P6 cohort topology dependency | **covered conditionally** | §6.3 candidate `trajectory/cohort_topology/` names HA-P6 explicitly as trigger. Reasonable; the HA-P6 run is the gating event. |

**Magnitude**: D5.1 carries a residual risk (structurally adequate, queue-dependent); D5.3 + D5.4 are substantive; D5.2 + D5.5 pass.

### Dimension 6 — Existing-work integration

| check | status | notes |
|---|---|---|
| **D6.1** Glob check vs §5 list | **missing entries surfaced** | A glob over `docs/research/methodology/*_descriptive.md` + `docs/research/analyses/garmin_exploration/*` + `_archive/*` surfaces FOUR existing artefacts not in the §5 index: **(a)** [`methodology/lc_phase_descriptive.md`](../methodology/lc_phase_descriptive.md) — per-phase distribution table of ALL key Garmin + subjective signals across pre_corona / corona_infection / lc. This artefact **already pre-answers a large fraction of Q3.x.a** (distribution shape) for the channels listed. Substantive miss. **(b)** [`methodology/garmin_indicators_audit.md`](../methodology/garmin_indicators_audit.md) — the canonical per-column provenance + known-issues catalog. **Directly answers D2.6.** Substantive miss. **(c)** [`methodology/hrv_proxy_via_stress.md`](../methodology/hrv_proxy_via_stress.md) — HRV-proxy validation methodology (sleep-window stress as HRV proxy). Should be cited under any future Strand A on `stress_mean_sleep` since the proxy semantics directly affect distribution interpretation. **(d)** [`_archive/H02b-trajectory-sub-files/`](../analyses/hypotheses/_archive/) — likely contains trajectory descriptive work; verify and decide whether to surface or leave archived. Minor. |
| **D6.2** Question-to-artefact mapping accuracy | **mostly correct** | The mappings that are present are accurate. Specific note: `citalopram_dose_response_stress_mean_sleep.md` is mapped to "A + B; Q3.1.d phase-stratified + Q4.2" — correct. `intervention_effects_descriptive.md` to Q4.2 — correct. |
| **D6.3** Existing artefacts NOT in §5 that the audit found | **see D6.1** | The four-item list under D6.1. Most consequential: `lc_phase_descriptive.md` and `garmin_indicators_audit.md`. |
| **D6.4** Status column accuracy | **mostly accurate** | S01/S02/S02c status as "archived; load-bearing" is correct. `cross-channel-correlation.md` as "active; canonical" matches. `bb_overnight_gain_proxy.md` as "active" matches. One concern: the row for `intervention_effects_descriptive.md` says "active; canonical for the citalopram arc" without flagging that the MD's §1 explicitly says "no segmentation choice is locked" — a reader could misread the row as a sign-off when the MD is still descriptive-only. Minor wording fix. |

**Magnitude**: D6.1 + D6.3 surface a **substantive** miss (`lc_phase_descriptive.md` + `garmin_indicators_audit.md`). The missing entries propagate back into Dimension 2 (D2.6) and Dimension 1 (D1.4 base distribution coverage) — the descriptive programme is partly already done, and the README presents the work as if it isn't.

### Dimension 7 — Coherent multi-year story

| check | status | notes |
|---|---|---|
| **D7.1** Narrative arc segment coverage (pre-LC → LC onset → train → validate → citalopram phases → current) | **covered weakly** for pre-LC + LC onset | Strand B Q4.1 recovery_arc covers train → validate → current cleanly. Pre-LC baseline (2021-08 → 2022-04) and LC onset (2022-04 → 2022-09, pre-gevoelscore) are not explicitly named in §6.2 dependencies. `lc_phase_descriptive.md` (missing from §5) would close this. |
| **D7.2** Subjective ↔ objective coupling | **missing** (substantive) | "When does gevoelscore align with Garmin signal vs diverge" is not a planned Strand A or B question. Gevoelscore appears in §3.4 as "almost every test's outcome side" without a planned Strand A analysis. Given the entire project hinges on the coupling between subjective experience and physiological signal, this is a notable omission. |
| **D7.3** Intervention ↔ response causal-narrative thread (CPAP + Ergotherapie + CPAP + citalopram) | **covered partially** | Q4.2 covers citalopram cross-channel. CPAP, Ergotherapie, Naproxen, Breinvoeding are catalogued in `intervention_effects_descriptive.md` §2 but not named in the README's Strand B questions. The §4.3 boundary-spacing audit hook (CPAP end 2024-04-16 ≡ Citalopram start 2024-04-09, 7-day gap) is structurally unanalyzable at all buffers — a coherent multi-year story should note that some intervention boundaries are forever entangled. |
| **D7.4** Recovery shape characterisation | **covered** | Q4.1 recovery_arc covers the multi-year shape (peak 2023 → trough 2025 → uptick May 2026). Refresh cadence in §7c addresses cadence work. |
| **D7.5** Cohort topology integration into the trajectory | **covered weakly** | Q4.4 is the cohort topology analysis but is a candidate third analysis. The integration of 29 crashes + 79 dips + dip-cluster overlay into the recovery_arc narrative is not explicit — these could live as their own analysis with no cross-link to the recovery arc. |
| **D7.6** Cross-channel narrative for "what does the body do during a crash / during an intervention / during recovery" | **missing** (substantive) | Cross-channel views are channel-grouped (Q4.5 independence) or event-grouped (Q4.2 intervention). The "what does the body do during a crash" narrative is implicit in the cohort topology (Q4.4) but not joined with cross-channel timing. The validate-era "autonomic stillness" finding from HA07d + HA10 ([HA07d result.md:82-100](../analyses/hypotheses/HA07d-sleep-stress-variability/result.md#L82)) is exactly this narrative — it deserves a Strand B home, not just an HA-result entry. |
| **D7.7** Open-questions section: what the descriptive layer will NOT answer | **covered weakly** | §8 "IS NOT" partially serves. No explicit "questions the descriptive layer can't address" list. The intervention-effects MD §2b CPAP-confound paragraph is the worked example of how to do this; the README doesn't carry an equivalent. Minor. |

**Magnitude**: D7.2 + D7.6 are substantive; D7.1 + D7.3 + D7.5 + D7.7 are minor-to-substantive; D7.4 passes.

---

## 3. What does NOT fire (selective)

These are non-trivially-strong coverage items worth naming explicitly.

- **The two-strand split** (`operationalisation_support/` vs `trajectory/`) is well-motivated. The functional distinction between "reusable per-channel artefacts HA pre-regs cite" and "standalone scientific descriptive of the multi-year arc" is the right cut. Plan v2's reframe (research programme, not card-per-group documentation layer) is methodologically sound — column-driven inventory would have driven toward "do all 88" which is unworkable.

- **Q3.x.a-f (the Strand A template)** is well-designed for what it covers. The combination of distribution shape (a) + autocorrelation (b) + base rates (c) + phase-stratified (d) + near-identity (e) + crash-vs-normal (f) is what the methodology stack actually needs to consume. The dimensions missed (D1.2 stationarity, D1.6 lagged-window adequacy, D1.8 spike-metrics) sit alongside this template rather than replacing it.

- **§7b lock-process integration** binds Strand A as a Phase 4 promotion gate. This is the right discipline binding — it closes the HA-C4b v1 §7-anchor calibration miss prospectively. The "spin one up first if missing" clause is the structural fix.

- **The §6.3 third-analysis deferral** is honest. Picking between cohort_topology / all_day_stress_avg / bb_lowest based on HA-P6 + HA-C3 + HA-C4b v2 results is the right kind of dependency to surface, not handwave.

- **The §5 status column** "active / archived / partial" is appropriately granular and lets a reader triage what to consume vs what to extend.

---

## 4. What would strengthen the programme

Concrete recommendations. **Each is a recommendation to the drafting agent, not an edit to the README** — Claude does not edit reviewer-mode artefacts unless authorised, and the user has reserved authorisation for the drafting agent's r2.

### 4a. Index integrity — close Dimension 6 (substantive, fast)

Add to §5 (in priority order, highest first):

1. **`methodology/lc_phase_descriptive.md`** → Strand A, addresses Q3.x.a + Q3.x.c (distribution shape + base rates) across pre_corona / corona_infection / lc for `total_steps`, `moderate_min`, `vigorous_min`, and the other Garmin daily signals already covered. Status: **active**. Cite from `operationalisation_support/stress_mean_sleep/` for any per-phase distribution context. **This pre-answers a substantial fraction of Q3.x.a for many channels.**
2. **`methodology/garmin_indicators_audit.md`** → Strand A, addresses D2.6 (known data-quality issues). Status: **active; canonical**. Cite from every `operationalisation_support/<channel>/` analysis as the known-issues check before any distribution claim.
3. **`methodology/hrv_proxy_via_stress.md`** → Strand A, addresses the HRV-proxy semantics that gate every `stress_mean_sleep` / `stress_*` interpretation. Cite from `operationalisation_support/stress_mean_sleep/` first.
4. **`_archive/H02b-trajectory-sub-files/`** → Strand B, possibly Q4.5 (cross-channel) or Q4.1 (recovery arc). Investigate and either index or note as superseded.

### 4b. Q-template additions — close Dimensions 1, 2, 4

Promote the following from implicit to explicit in the Q3.x-shape template (Strand A) and / or as Strand B questions:

- **Q3.x.g — Stationarity / slow-drift check** (D1.2 + D2.3). Rolling 90-day mean + variance of the channel across the analysis window; flag structural breaks if any. Closes both "is the stationary-bootstrap assumption OK" and "is the personal-baseline z-score drifting".
- **Q3.x.h — Outlier inventory** (D2.1). Distribution-tail outlier count + dates; correlate with calendar events / sync sessions. Catches the sensor-error case Q3.x.a's "heavy-tail flag" can mask.
- **Q3.x.i — Personal-baseline-window-adequacy** (D1.6). For the 30-day rolling baseline (or whatever window the channel uses), demonstrate that the MAD stabilises by day-N (not still falling). Closes the HA01b-recomputed correction worked example prospectively.
- **Q3.x.j — Seasonality + DOW check** (D4.9). Mean / median by month + day-of-week; flag any pattern that exceeds the within-month / within-week SD. Closes the seasonality alibi that v3 dose-response had to rule out manually.
- **Q3.x.k — Covariate-sensitivity vs autocorrelation** (D5.3). For any channel that could appear as a predictor in a rolling-sum / lagged-mean HA test, run the descriptive analogue of HA-P7's §4.5.4 — does adding `gevoelscore_lagged_mean_Nd` attenuate the channel's relationship with `is_crash`? Identifies the "recent-low-gevoelscore proxy" risk before lock.

**New Strand B question — Q4.8 — Subjective ↔ objective coupling** (D7.2). When does `gevoelscore` align with the load-bearing Garmin channels, when does it diverge? This is the central project question and deserves its own home rather than being subsumed under HA-* outcome-side framing.

**New Strand B question — Q4.9 — Crash-day body-state profile** (D7.6). What does the body do during a crash (cross-channel; integrated)? What does it do during the recovery? This is the HA07d "autonomic stillness" finding deserving a Strand B home as a refreshable cross-channel narrative.

### 4c. Strand A queue promotion (Dimension 5)

§3.4 "HA-touched non-confirmed channels" reads as "spin up only when needed" which is operationally fine but **carries the HA-C4b v1 §7-anchor failure risk** for any channel that hits an HA pre-reg without prior Strand A. Promote the §3.4 candidates list to a **pending queue** ordered by HA-* execution queue priority (HA-C3 drafting, HA-C4b v3, HA-P6 result-reading). Each pending item gets a 2-line scope statement so a drafter can spin up in <2h. Specifically:

- `stress_low_motion_min_count_S60_Mlow` — HA-C4b v3 column. Lock §7-anchor source before the v3 test run. Add a §3.4.x mini-spec.
- `bb_overnight_gain` — HA10 v2 reinterpretation candidate. Cross-reference with `bb_overnight_gain_proxy.md`.
- `gevoelscore` — outcome side of nearly every test. The "outcome channel" status is no excuse for skipping its distribution + base-rate analysis.

### 4d. Cross-channel structure extension (Dimension 3)

- Add a **detrended cross-channel-correlation companion** (D3.4) per CONVENTIONS §3.7's spirit: same matrix, but on linearly-detrended-on-window data. Compare to the raw matrix; any pair where \|Δρ\| > 0.10 is a time-trend-driven correlation, not biology.
- Reconcile the threshold language between Q3.x.e (ρ ≥ 0.9), CONVENTIONS §3.3 (ρ ≥ 0.97 definitional pair), and the cross-channel card (ρ ≥ 0.92 near-identity). One sentence in the Q-template stating "ρ ≥ 0.92 near-identity, ρ ≥ 0.97 definitional pair, ρ ≥ 0.9 strong-association flag" prevents drafter confusion.

### 4e. Discipline rows — close Dimension 4

- §7a per-analysis README pattern: add **"Plots before tables"** as a soft convention (closes D4.2).
- §7a: add **"Pre-registered exploratory framing"** — each Strand A analysis surfaces its findings as exploratory; HA pre-regs citing them carry that exploratory tag forward to keep the §7-anchor-anchoring-discipline clean (closes D4.4).
- §7a: add **"Excluded-rows count + reason"** at the head of each analysis (closes D4.6).
- §7a: add **"Seed + corpus snapshot date"** to every `run.py` output header (closes D4.7).
- §7c refresh cadence: add **"after a new column lands in `per_day_master.csv`, audit existing Strand A analyses for near-identity vs the new column"** — closes a slow gap where the cross-channel card grows stale.

### 4f. Trajectory narrative completeness (Dimension 7)

- §6.2 recovery_arc Inputs: add **pre-LC baseline window** (2021-08-16 → 2022-04-03 per `lc_phase_descriptive.md`) as a context dependency. The recovery arc starts from somewhere; that somewhere is pre-LC.
- Add §8 line: **"Questions the descriptive layer will NOT answer"** — list the causal-attribution-questions (intervention vs trajectory disentanglement; cross-confounded boundary pairs per §3.8 boundary-spacing) that the descriptive layer surfaces without resolving. Pre-empts a reader inferring more than the analyses claim.

---

## 5. Verdict

**PASS-with-caveats** — the two-strand framing + Q3.x template + first-3-analyses ordering are methodologically sound, but the index missing `lc_phase_descriptive.md` + `garmin_indicators_audit.md` (Dimension 6), the silent data-quality / sensor-event / calibration-drift discipline (Dimension 2), and the absence of seasonality + Simpson's-paradox + subjective↔objective + covariate-sensitivity checks from the Q-template (Dimensions 4 + 5 + 7) prevent a clean PASS. None of the fires are blocking; all can close with r2 additions to §5 (4a) + Q-template extensions (4b) + a queue promotion in §3.4 (4c).

---

## Methodology

This audit applies a 7-dimension checklist customised for a descriptive-research-programme scoping artefact, drawing on:

- Project-specific audit hooks from [CONVENTIONS §3](../CONVENTIONS.md) (personal-baseline / lagged-baseline / column-duplication / crash-drop sensitivity / spike metrics / named counts / detrend-sensitivity / boundary-spacing / curated-catalog).
- The methodology stack the descriptive layer must support: [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md) (stationary-bootstrap + block-permutation null assumptions), [`citalopram_phase_stratification.md`](../methodology/citalopram_phase_stratification.md) §4 + §6 (per-channel inheritance rules + pre-registration template), [`hypothesis_lock_process.md`](../methodology/hypothesis_lock_process.md) §3.2 step 4 + §3.8 + §5 (lock-blocking gates + sanity checks).
- General descriptive-research best practice (univariate-before-bivariate; viz-before-tests; sensitivity-to-cutpoints; Simpson's-paradox awareness; reproducibility; seasonality / DOW).
- The HA-C4b v1 halt (§7-anchor inherited from definitional cousin → unmedicated median 78 vs locked anchor [15, 60]) + HA-P7 §4.5.4 covariate-sensitivity diagnostic (recovery-debt mechanism collapsing to recent-low-gevoelscore proxy) as worked failure-mode examples.

**Reviewer constraint**: per [CONVENTIONS §1.2](../CONVENTIONS.md#L52), this audit reads + critiques + recommends; it does NOT edit the README being audited. Recommendations in §4 are addressed to the drafting agent for r2.
