# Descriptive research programme

## Authorship

- **Drafted**: 2026-06-16 by Claude (Opus 4.7), in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked)
- **Authorising user**: user (name redacted for publication-safety per `audit_for_publication.py` discipline)
- **Drafting-session context**: post-STOCKTAKE revival ([`STOCKTAKE.md §3`](../../STOCKTAKE.md#3-descriptive-work--the-structural-gap)) + plan v2 ([`structured-descriptive-analysis-2026-06-16.md`](file:///C:/Users/Gebruiker/.claude/plans/structured-descriptive-analysis-2026-06-16.md), v2 reframe accepted: research programme, not card-per-group documentation layer)
- **Locked design choices** (from plan v2 §9, user-accepted 2026-06-16):
  - Folder name: `descriptive/`
  - Two-strand split: `operationalisation_support/` + `trajectory/`
  - First 3 analyses: `stress_mean_sleep` (Strand A) + `recovery_arc` (Strand B) + a third TBD by HA-P6 result / HA-C3 drafting needs
  - Phase 4 lock-blocking: soft sanity-check first; promote to lock-blocking later
  - S01/S02 migration: leave archived, consolidate into `trajectory/recovery_arc/` from scratch
- **Status**: **LOCKED 2026-06-18 by user acceptance at revision r3 (compressed §3.6 re-audit per acceptability criteria).** Programme scoping artefact, not a falsification-bar pre-reg. **Compression justification**: r3 changes (Strand B operationalisation interview discipline + three-phase recovery_arc reframe) are scope additions, not architectural; no new statistical machinery; no falsification-bar change (descriptive programme has none); first programme-scoping doc so the discipline pattern is itself being established. Further modifications create v2 with v1 archived per the locked-pre-reg discipline. **§3.8 lock-commit gates**: (1) power-calc dispatch N/A — programme scoping doc, no §8 caveats; (2) headline cell N/A — no falsification bar; (3) register-row pointer N/A — descriptive/README is sui generis programme scoping artefact, non-supersession confirmed; (4) re-audit COMPRESSED per §3.6 (justification above). **Next**: Phase 1 execution per §6 unblocked — first analysis [`operationalisation_support/stress_mean_sleep/`](operationalisation_support/) can begin.

### Revision r3 — Strand B operationalisation + three-phase trajectory reframe (2026-06-18)

Two user-driven changes (no audit fire driver; direct user feedback after r2-amended scope review):

- **Strand B operationalisation interview discipline** → new §7b documents the protocol: Claude drafts a question-and-options brief; user picks; locked operationalisation enters the analysis README before script.py is written. Default canonical; compression (skip interview) is documented exception only. §2 Two-strand framing extended with the discipline distinction (Strand A template-driven vs Strand B operationalisation-requires-user). §6.2 recovery_arc updated to name the §7b pre-spin-up requirement. *(Rationale: Strand B questions are open and cross-cutting; multiple defensible operationalisations per choice point; user owns the choice.)*
- **Q4.1 recovery arc reframed as three-phase** (pre-illness healthy → immediate infection/acute → LC trajectory) → §2 Two-strand framing extended with the three-phase paragraph; §4.1 question text extended; §6.2 recovery_arc scope + inputs + outputs + dependencies + effort all updated to reflect the three-phase coverage. *(Rationale: the Garmin corpus covers ~5 years 2021-08-16 → present, with ~13+ months of pre-illness healthy baseline that has never been formally characterised; S01/S02 only used the LC era. Pre-illness data is a stronger comparison than early-LC-as-proxy-for-healthy.)*

§7 numbering also corrected (broken intermediate state with duplicate §7c labels + empty §7d → cleaned to §7a / §7b / §7c / §7d sequential).

Authorship "Locked design choices" bullet about first-3-analyses still holds: §6.2 recovery_arc remains the second analysis; scope is broader but the analysis identity is unchanged.

### Revision r2 — audit closures (2026-06-16)

Audit report at [`docs/research/reviews/descriptive-programme-2026-06-16.md`](../../reviews/descriptive-programme-2026-06-16.md) (fresh-session methodological audit per [`session-descriptive-programme-audit-handoff-2026-06-16.md`](file:///C:/Users/Gebruiker/.claude/plans/session-descriptive-programme-audit-handoff-2026-06-16.md)) returned verdict **PASS-with-caveats** with 7 dimension-level fires (no blocking). All 7 closed in this revision:

- **D1.8 spike-detecting metrics** → new Q3.x.g in Strand A template (spike primitive per channel; CONVENTIONS §3.5) + §6.3 first-3 third-analysis slot revised to `operationalisation_support/stress_low_motion_min_count_S60_Mlow/` (covers CONFIRMED-citalopram channel AND spike primitive simultaneously, replacing the prior cohort_topology / all_day_stress_avg / bb_lowest candidates which remain on the deferred queue per §3).
- **D2.6 known-issues catalog + D2.1 outlier + D2.3 calibration-drift** → new Q3.x.h in Strand A template (outlier detection + calibration-drift check); [`methodology/garmin_indicators_audit.md`](../../methodology/garmin_indicators_audit.md) added to §5 index.
- **D3.4 spurious-correlation flag** → new Q4.5.b in Strand B (detrended-companion correlation matrix for time-trended pairs per CONVENTIONS §3.7).
- **D4.9 seasonality + DOW effects** → new Q4.8 in Strand B (seasonality + day-of-week per channel; explicit confound-class check against v3-dose-response seasonality-alibi rejection logic).
- **D5.3 covariate-sensitivity generalisation** → new Q3.x.i in Strand A template (covariate-sensitivity readiness per HA-P7 §4.5.4 worked example).
- **D6.1 missing existing artefacts** → §5 index extended with [`methodology/lc_phase_descriptive.md`](../../methodology/lc_phase_descriptive.md) (substantially pre-answers Q3.x.a) + [`methodology/garmin_indicators_audit.md`](../../methodology/garmin_indicators_audit.md) (canonical known-issues catalog for Q3.x.h). §6.1 Q3.1.a scope delegated to lc_phase_descriptive.md (refresh + extend if material gaps, rather than redo).
- **D7.2 + D7.6 subjective↔objective coupling + crash-day body-state profile** → new Q4.9 in Strand B (the central project question; gevoelscore-vs-Garmin alignment + crash-day cross-channel body-state profile; currently no home in any artefact).

The original "Locked design choices" bullets above are preserved as audit-trail of the drafting-time decisions. The r2 closure updates one of them (third first-3 analysis: was TBD, now `stress_low_motion_min_count_S60_Mlow`); change documented in this revision entry per the locked-pre-reg revision-log discipline.

---

## 1. What this is

A research programme that does the descriptive analysis every quantitative research needs in order to (a) **choose methodology**, (b) **design operationalisation**, and (c) **gain overall insights in a multi-year trajectory**. Question-driven, not column-driven. Output is analyses (folders with code + writeup), not standardised templates.

Companion to:
- [`STOCKTAKE.md §3`](../../STOCKTAKE.md#3-descriptive-work--the-structural-gap) — the cross-cutting view that named the structural gap this programme closes
- [`methodology/hypothesis_lock_process.md`](../../methodology/hypothesis_lock_process.md) — the HA-* discipline this programme integrates with (Phase 4)
- Existing descriptive artefacts at [`garmin_exploration/`](../garmin_exploration/), `_archive/S01-S02`, and several `methodology/*_descriptive.md` MDs — indexed here, not duplicated

---

## 2. Two strands

### Strand A — Operationalisation support

Reusable per-channel analyses that any HA pre-reg drafting session can cite to make sound methodological + operationalisation choices. Answers, for each channel touched by an HA test:
- What is the column's distribution shape — informs personal-baseline z-score robustness, §7 anchor calibration
- What is the autocorrelation structure — informs block-bootstrap E[L] choice + window-length defensibility
- What are base rates per phase / era / Stratum 4 — informs sample-size feasibility before the falsification bar is locked
- For CONFIRMED-citalopram channels: what's the phase-stratified distribution — informs §5.A/§5.B/§5.C treatment per [`citalopram_phase_stratification.md §6`](../../methodology/citalopram_phase_stratification.md)
- Near-identity check: which other columns is it ρ ≥ 0.9 with — informs CONVENTIONS §3.3 column-duplication discipline

**Folder**: `descriptive/operationalisation_support/<channel>/`

### Strand B — Multi-year trajectory

Standalone scientific descriptive analyses of the corpus's bigger-picture story. Answers cross-cutting questions about the multi-year arc, intervention effects across channels, era boundaries, cohort topology. Output is refreshable as more data accrues.

**Folder**: `descriptive/trajectory/<topic>/`

**Discipline (r3 added 2026-06-18)**: Strand B analyses **require a user operationalisation interview before script.py is written**. Unlike Strand A (per-channel template Q3.x.a-i drives operationalisation deterministically), Strand B questions are open and cross-cutting — every analysis has multiple defensible operationalisations (which channels? which window? which events to overlay? which boundary dates? what counts as "healthy baseline"?). The user owns the operationalisation choice per Strand B analysis; Claude drafts a question-and-options brief, user picks, then script.py is written to the locked operationalisation. See §7c for the protocol.

**Three-phase trajectory framing (r3 added 2026-06-18)**: the Garmin corpus covers ~5 years (2021-08-16 → present) and spans **three distinct epochs** that should be honoured by trajectory analyses:
1. **Pre-illness healthy baseline** (2021-08-16 → COVID infection date) — ~13+ months of healthy Garmin data BEFORE the LC onset. No gevoelscore (that started 2022-09-03). The strongest available "healthy comparison" for everything that follows.
2. **Immediate infection / acute phase** (COVID infection date → onset of sustained illness) — the period of acute infection + early recovery. Operational boundary requires user input (first symptoms vs PCR-confirmed vs sustained symptom onset vs official diagnosis — choices give different windows).
3. **LC trajectory** (Stratum 4: 2022-09-03 → as-of-date) — the multi-year recovery arc. Currently the primary analytic surface per `lc_era_temporal_segmentation.md`; trajectory analyses extend the framing to include phases 1 + 2 above.

Trajectory analyses (Q4.1 recovery arc; Q4.3 era boundaries) should leverage all three phases — pre-illness data is a stronger baseline than early-LC-as-proxy-for-healthy.

---

## 3. Research questions — Strand A (operationalisation-support)

Each question is per-channel. Listed in priority order (highest first):

### 3.1 `stress_mean_sleep` (CONFIRMED-citalopram, +0.43/mg p=0.001)

**Why first**: most-cited channel across HA-* (HA07c, HA07d, HA08c); critical for any HA pre-reg re-interpretation in light of v3 dose-response; HA-C3 / HA-C4 may touch.

**Questions**:
- Q3.1.a — Distribution shape on Stratum 4 (mean, median, MAD, quantiles, skewness, heavy-tail flag)?
- Q3.1.b — Autocorrelation structure (ACF, effective E[L] under [`permutation_null_block_length.md`](../../methodology/permutation_null_block_length.md))?
- Q3.1.c — Base rates per phase (unmedicated / buildup / consolidation / afbouw / post_afbouw) — n per cell + median + dispersion?
- Q3.1.d — Phase-stratified distribution: how much does the citalopram step shift the baseline + dispersion vs natural day-to-day variation?
- Q3.1.e — Near-identity check vs `stress_stdev_sleep`, `all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`?
- Q3.1.f — Crash-day vs normal-day comparison on Stratum 4 (Cohen's d, crash-drop sensitivity per CONVENTIONS §3.4) — re-anchors the HA07c family results in current-corpus form?
- Q3.1.g — Spike-detecting primitive: per-minute or per-window resolution available? Coverage? Relation to the daily-aggregate channel (per CONVENTIONS §3.5 acute-load discipline)? *(r2 closure D1.8)*
- Q3.1.h — Outlier detection (isolated sensor failures + persistent shifts) + calibration-drift check; cross-reference [`methodology/garmin_indicators_audit.md`](../../methodology/garmin_indicators_audit.md) for known issues. *(r2 closure D2.6 + D2.1 + D2.3)*
- Q3.1.i — Covariate-sensitivity readiness: which other channels are reasonable controls for a future HA pre-reg using this channel as predictor (per HA-P7 §4.5.4 worked example, targeting autocorrelation-vs-mechanism disambiguation)? *(r2 closure D5.3)*

**Existing**: partial — [`garmin_exploration/hrv_proxy_validation/`](../garmin_exploration/hrv_proxy_validation/) covers crash-vs-normal at episode + day level. [`methodology/lc_phase_descriptive.md`](../../methodology/lc_phase_descriptive.md) substantially pre-answers Q3.1.a (distribution shape on Stratum 4); planned analysis delegates to it + refreshes if material gaps. [`methodology/garmin_indicators_audit.md`](../../methodology/garmin_indicators_audit.md) carries known data-quality issues for Q3.1.h. Nothing reusable for §7 anchor + phase-stratified + spike + covariate-sensitivity.

**Missing**: Q3.1.b / c / d / e / g / i for sure; Q3.1.a delegated (per r2 closure D6.1); Q3.1.f needs a refresh in operationalisation-support framing; Q3.1.h closure depends on garmin_indicators_audit.md coverage of this channel specifically.

### 3.2 `all_day_stress_avg` (CONFIRMED-citalopram, +0.57/mg p=0.000)

**Why second**: largest citalopram effect; potential HA-C3 input (the non-linear stress → fatigue test).

**Questions**: same Q-shape as Q3.1.a-i, on `all_day_stress_avg` *(r2: template extended a-i per closures D1.8, D2.6, D5.3)*.

**Existing**: minimal — incidental coverage only. [`methodology/lc_phase_descriptive.md`](../../methodology/lc_phase_descriptive.md) may pre-answer Q3.2.a if it covers this channel; verify at spin-up.

**Missing**: nearly everything; Q3.2.a delegates to lc_phase_descriptive.md if coverage exists.

### 3.3 `bb_lowest` (CONFIRMED-citalopram, −1.13/mg p=0.000)

**Why third**: foundational for HA-C4b v2 + HA10 reinterpretation; the BB-floor candidate channel. *(Note: r2 closure D1.8 moved this analysis OUT of the locked first-3 list; it joins the deferred queue per §6. The third first-analysis is now `stress_low_motion_min_count_S60_Mlow` because it covers both CONFIRMED-citalopram AND spike-primitive gaps in one analysis.)*

**Questions**: same Q-shape as Q3.1.a-i, on `bb_lowest` *(r2: template extended a-i)*. **Additional**:
- Q3.3.j — Coverage of the BB-source channel (per-day BB lowest is computable from when?) — informs which date range any HA test on this column can use *(was Q3.3.g pre-r2; renamed to avoid collision with new template letters)*
- Q3.3.k — Relationship to `bb_overnight_gain` (HA10's primary) — near-identity check + descriptive of the gap between these two BB columns *(was Q3.3.h pre-r2; renamed)*

**Existing**: [`methodology/bb_overnight_gain_proxy.md`](../../methodology/bb_overnight_gain_proxy.md) covers Q3.3.k partially. [`methodology/lc_phase_descriptive.md`](../../methodology/lc_phase_descriptive.md) may pre-answer Q3.3.a; verify at spin-up.

**Missing**: most of Q3.3.a-j; Q3.3.k needs extension to bb_lowest specifically.

### 3.4 HA-touched non-confirmed channels

Lower priority — spin up only when an HA pre-reg drafting session needs them. No formal scoping until that point.

Candidates (current HA-* anchors not in the CONFIRMED-citalopram set):
- `bb_overnight_gain` (HA10 primary) — partially covered by `bb_overnight_gain_proxy.md`
- `stress_low_motion_min_count_S60_Mlow` (HA-C4b v2 primary) — partially covered by [`stress_low_motion_viz/`](../garmin_exploration/stress_low_motion_viz/) + [`stress_low_motion_primitive.md`](../../methodology/stress_low_motion_primitive.md)
- `resting_hr` (HA06b primary; weak v3 dose-modulation)
- `exertion_class` + `push_burden_7d` (HA01b/HA01c primaries) — partially covered by [`activity-labels/`](../garmin_exploration/activity-labels/)
- `stress_stdev_sleep` (HA07d primary, the only canonical-SUPPORTED test) — needs a Strand A analysis for the variability story
- `gevoelscore` (almost every test's outcome side)

---

## 4. Research questions — Strand B (multi-year-trajectory)

Each question is cross-cutting. Listed roughly in priority order.

### 4.1 Recovery arc (three-phase: healthy → infection → trajectory)

**Question (r3-extended 2026-06-18)**: What is the **three-phase** shape of the data? (a) **Pre-illness healthy baseline** (2021-08-16 → COVID infection date) — what does healthy look like in the Garmin signals? (b) **Immediate infection / acute phase** (infection → onset of sustained illness) — how do the signals shift during acute infection + early recovery? (c) **LC trajectory** (2022-09-03 → present) — the multi-year recovery arc, inflection points, alignment with documented events (CPAP, Ergotherapie, citalopram phases). The healthy-baseline (a) is a **stronger comparison** than early-LC-as-proxy-for-healthy.

**Existing**: [`_archive/S01-stabilisation-trajectories/`](../hypotheses/_archive/S01-stabilisation-trajectories/) (90d rolling autonomic on LC era only) + [`_archive/S02-score-trajectory/`](../hypotheses/_archive/S02-score-trajectory/) (gevoelscore distribution shift) + [`_archive/S02c-may-2026-divergence/`] (channel divergence). All archived; **all framed only on the LC era** — none of them leveraged the pre-illness healthy baseline.

**Missing**: (i) a non-archived, refreshable home; (ii) a current-corpus refresh (S01/S02 last computed pre-2026-06-13); (iii) **the pre-illness healthy baseline + acute-infection phase extensions** (the r3-added scope — strongest gap, since pre-illness data has never been formally characterised).

**Operationalisation requires user interview (per Strand B discipline §7c)**:
- Which date marks the COVID infection boundary? (first symptoms / PCR-confirmed / sustained onset / official diagnosis — all are defensible)
- Which Garmin channels are in scope for each phase? (some channels may have coverage gaps in different phases)
- How is the acute-infection phase boundary defined? (fixed window vs symptom-driven vs autonomic-signal-driven)
- Which documented events get overlaid? (CPAP, Ergotherapie, citalopram phases — full list to be confirmed)

**Proposed analysis**: `trajectory/recovery_arc/`. Consolidates S01 + S02 + S02c + the new pre-illness + acute-infection extensions into one refreshable three-phase analysis. Headline finding: full arc (healthy → infection → LC trajectory) with documented event overlays + cross-phase channel comparisons. Effort bump from v2-original 4-5h estimate to ~6-8h reflecting the scope extension.

### 4.2 Intervention cross-channel view (the citalopram integrated picture)

**Question**: What's the integrated picture of the citalopram effect across all 6 candidate channels? Where does the SSRI signal land first (stress vs BB vs RHR vs respiration)? Is there a timing relationship?

**Existing**: [`intervention_effects_descriptive.md`](../../methodology/intervention_effects_descriptive.md) + [`citalopram_dose_response_stress_mean_sleep.md`](../../methodology/citalopram_dose_response_stress_mean_sleep.md) + [`citalopram_phase_stratification.md`](../../methodology/citalopram_phase_stratification.md). v3 multi-channel work confirmed 3 + rejected 1.

**Missing**: the **cross-channel timing analysis** — does the SSRI signal hit stress channels first then BB then RHR? And the integrated visualisation that ties the 6-channel picture together for non-specialist readers.

**Proposed analysis** (later phase): `trajectory/intervention_cross_channel/`. Not in the first 3.

### 4.3 Era-boundary descriptive justification

**Question**: pre-LC / train / validate / Stratum 4 are operational; what's the descriptive justification for those boundaries vs alternatives?

**Existing**: [`lc_era_temporal_segmentation.md`](../../methodology/lc_era_temporal_segmentation.md) — definitional; operationalises the boundaries but doesn't go deep on alternative-boundary comparison.

**Missing**: a data-driven case for the current boundaries; explicit alternatives considered + rejected.

**Proposed analysis** (later phase): `trajectory/era_boundaries/`. Not in the first 3.

### 4.4 Cohort topology refresh

**Question**: 29 crashes + 79 dips; what's the dip-cluster overlay; what are the recovery-window distributions; what's the empirical baseline for "normal" between events?

**Existing**: [`crash_episode_descriptive.md`](../../methodology/crash_episode_descriptive.md) + [`crash_episode_prolonged.md`](../../methodology/crash_episode_prolonged.md). Dip-cluster overlay was in archived STOCKTAKE — needs its own home.

**Missing**: the dip-cluster overlay analysis surfaced as its own artefact; refresh of recovery-window distributions (HA-P6 depends on this).

**Proposed analysis** (third-priority if HA-P6 needs it): `trajectory/cohort_topology/`. **Candidate for the "third analysis TBD" slot.**

### 4.5 Cross-channel independence structure

**Q4.5.a — Raw-primitive independence**: What's the effective dimensional rank of the load-bearing signal set? Which channels are independent, which collapse?

**Existing**: [`garmin_exploration/cards/cross-channel-correlation.md`](../garmin_exploration/cards/cross-channel-correlation.md) — this IS the analysis. Found H02b ≡ H02d (ρ=+1.000) + HA10 ≡ −HA07c (ρ=−0.922). Established 3-4 independent clusters from 9 anchors.

**Missing**: nothing immediately for Q4.5.a. The card stays in place. Index it from `_existing_work_index.md`.

**Q4.5.b — Detrended-companion correlation (spurious-correlation flag)** *(r2 closure D3.4)*: For each pair where both channels show a multi-year trajectory (recovery arc), how much of the correlation is within-window co-variation vs shared trajectory? Detrend per [`CONVENTIONS §3.7`](../../CONVENTIONS.md) trajectory-detrend sensitivity discipline; recompute correlations on residuals; flag which "near-identity" pairs collapse to weak within-window correlation under detrend.

**Existing**: nothing direct. The cross-channel-correlation card runs on raw primitives.

**Missing**: a detrended-companion correlation matrix; spurious-correlation flag for time-trended pairs.

### 4.6 Coverage / availability analysis

**Question**: When does which Garmin signal become available? What's the sub-window-resolved coverage for per-minute primitives? What missingness patterns matter for hypothesis design?

**Existing**: [`DATA_DICTIONARY.md`](../../DATA_DICTIONARY.md) documents some; [`garmin_exploration/README.md`](../garmin_exploration/README.md) FIT taxonomy covers per-minute coverage well; [`bb_overnight_gain_proxy.md`](../../methodology/bb_overnight_gain_proxy.md) covers the 2024-07-08 → 2024-09-17 BB bridge.

**Missing**: a coherent coverage-overview analysis that any HA pre-reg can cite for "this column is available from date X with coverage Y%".

**Proposed analysis** (later phase): `trajectory/coverage_overview/`. Not in the first 3.

### 4.7 Notes-categorisation patterns

**Question**: What's the symptom-mention asymmetry profile? When does the user write vs not? How does the categorisation distribution shift across LC eras?

**Existing**: [`symptom_mention_asymmetry.md`](../../methodology/symptom_mention_asymmetry.md) — definitional, not descriptive. [`analyses/notes_categorization/categories-analysis-v1.md` + `-v2.md`](../notes_categorization/) — partial descriptive but bundled with categorisation methodology.

**Missing**: a clean descriptive of mention-rate patterns + write-vs-not patterns; complements rather than duplicates the existing categorisation work.

**Proposed analysis** (later phase): `trajectory/notes_patterns/`. Not in the first 3.

### 4.8 Seasonality + day-of-week effects *(r2 closure D4.9)*

**Question**: Are there time-of-year (seasonality) or weekday-vs-weekend (DOW) patterns per channel? These act as confounders for the recovery-arc analysis and must be ruled out (or controlled for) before attributing inflection points to documented events.

**Existing**: implicit in the v3 multi-channel dose-response work via the spring-2025 control (ruled out a seasonality alibi for `stress_mean_sleep` specifically; β=+0.004/day flat). No systematic per-channel seasonality + DOW analysis exists.

**Missing**: a coherent per-channel seasonality + DOW pattern check on the 3 CONFIRMED-citalopram channels (at minimum) — feeds into the recovery_arc analysis's confound-class disambiguation + extends the v3 spring-2025 control to the other 2 CONFIRMED channels.

**Proposed analysis** (later phase): `trajectory/seasonality_dow/`. Not in the first 3.

### 4.9 Subjective ↔ objective coupling + crash-day body-state profile *(r2 closure D7.2 + D7.6)*

**Question** (the central project question): When does `gevoelscore` align with the 3 CONFIRMED Garmin channels vs diverge? On a crash day, what does the body-state profile combining gevoelscore + cross-channel Garmin patterns look like? Are there pre-crash divergence patterns where Garmin signals one thing and gevoelscore another?

**Existing**: partial — [`garmin_exploration/hrv_proxy_validation/`](../garmin_exploration/hrv_proxy_validation/) covers `stress_mean_sleep` crash-vs-normal at episode + day level. No integrated subjective↔objective coupling analysis across the 3 CONFIRMED channels.

**Missing**: the integrated picture combining gevoelscore + the 3 CONFIRMED Garmin channels into a cross-channel body-state profile per crash day + non-crash baseline. **This is the central project question and currently has no home in any artefact.**

**Proposed analysis** (later phase, high-priority post-MVP): `trajectory/subjective_objective_coupling/`. Not in the first 3 because the 3 Strand A first-analyses build the per-channel substrate this depends on; spin up after at least `stress_mean_sleep` + `stress_low_motion_min_count_S60_Mlow` land.

---

## 5. Index of existing descriptive work

(Phase 2 of the plan — catalog, no content moves. To be expanded into `_existing_work_index.md` after this README is locked.)

| artefact | strand | research question addressed | status |
|---|---|---|---|
| [`_archive/S01-stabilisation-trajectories/`](../hypotheses/_archive/S01-stabilisation-trajectories/) | B | Q4.1 (recovery arc) | archived; load-bearing for `trajectory/recovery_arc/` |
| [`_archive/S02-score-trajectory/`](../hypotheses/_archive/S02-score-trajectory/) | B | Q4.1 (recovery arc, score axis) | archived; load-bearing for `trajectory/recovery_arc/` |
| [`_archive/S02c-may-2026-divergence/`] | B | Q4.1 (recovery arc, late-era divergence) | archived; load-bearing for `trajectory/recovery_arc/` |
| [`garmin_exploration/cards/cross-channel-correlation.md`](../garmin_exploration/cards/cross-channel-correlation.md) | B | Q4.5 (cross-channel independence) | **active; canonical** — leave in place |
| [`garmin_exploration/cards/card-b-train-specificity.md`](../garmin_exploration/cards/card-b-train-specificity.md) + `card-b2-validate-specificity.md` + `primary-verdict-statistics.md` | B | (Tier 2 specificity audit; tangential to descriptive programme) | active; leave in place, indexed |
| [`garmin_exploration/hrv_proxy_validation/`](../garmin_exploration/hrv_proxy_validation/) | A | Q3.1.f (stress_mean_sleep crash-vs-normal) | active; cite from `operationalisation_support/stress_mean_sleep/` |
| [`garmin_exploration/stress_low_motion_viz/`](../garmin_exploration/stress_low_motion_viz/) | A | Q3.4 (stress_low_motion primitive characterisation) | active; cite from `operationalisation_support/stress_low_motion_*` (later) |
| [`garmin_exploration/activity-labels/`](../garmin_exploration/activity-labels/) | A | Q3.4 (exertion_class, push_burden_7d) | active; foundation for any future Strand A on exertion channels |
| [`garmin_exploration/README.md`](../garmin_exploration/README.md) (FIT taxonomy + sub-daily inventory) | A + B | Q4.6 (coverage / availability) | active; leave in place |
| [`intervention_effects_descriptive.md`](../../methodology/intervention_effects_descriptive.md) | B | Q4.2 (intervention cross-channel view, Session C single-channel) | active; canonical for the citalopram arc |
| [`citalopram_dose_response_stress_mean_sleep.md`](../../methodology/citalopram_dose_response_stress_mean_sleep.md) | A + B | Q3.1.d (phase-stratified `stress_mean_sleep`) + Q4.2 | active; canonical |
| [`citalopram_phase_stratification.md`](../../methodology/citalopram_phase_stratification.md) | A | Q3.1.d / Q3.2.d / Q3.3.d (phase-stratified treatment for all 3 CONFIRMED) | active; canonical; §6 binding on new HA pre-regs |
| [`crash_episode_descriptive.md`](../../methodology/crash_episode_descriptive.md) + [`crash_episode_prolonged.md`](../../methodology/crash_episode_prolonged.md) | B | Q4.4 (cohort topology, episode geometry) | active; cite from `trajectory/cohort_topology/` (when spun up) |
| [`lc_era_temporal_segmentation.md`](../../methodology/lc_era_temporal_segmentation.md) | B | Q4.3 (era boundaries) | active; foundation for `trajectory/era_boundaries/` |
| [`lc_phase_descriptive.md`](../../methodology/lc_phase_descriptive.md) *(r2 added per closure D6.1)* | A | Q3.1.a / Q3.2.a / Q3.3.a / Q3.x.a (substantially pre-answers distribution-shape questions on Stratum 4) | active; canonical; planned Strand A analyses delegate Q3.x.a to this MD + refresh if material gaps |
| [`garmin_indicators_audit.md`](../../methodology/garmin_indicators_audit.md) *(r2 added per closure D6.1)* | A | Q3.x.h (outlier detection + calibration-drift + known-issues catalog) | active; canonical known-issues catalog; planned Strand A analyses cross-reference for Q3.x.h |
| [`symptom_mention_asymmetry.md`](../../methodology/symptom_mention_asymmetry.md) | A | Q4.7 (notes patterns; definitional substrate) | active; definitional |
| [`bb_overnight_gain_proxy.md`](../../methodology/bb_overnight_gain_proxy.md) | A | Q3.3.h (bb_lowest vs bb_overnight_gain) | active; cite from `operationalisation_support/bb_lowest/` |
| [`stress_low_motion_primitive.md`](../../methodology/stress_low_motion_primitive.md) | A | Q3.4 (stress_low_motion primitive lock) | active; cite from any future Strand A on that primitive |
| [`lc_recovery_phase_axis.md`](../../methodology/lc_recovery_phase_axis.md) *(LOCKED 2026-06-19 `d47e0d3`)* | A + B | Q3.x.c (per-phase base rates extended on 6-phase axis) + Q4.1 (recovery_arc v2 substrate) + Q4.3 (era boundaries refined) | active; canonical; 3-layer axis (data-given outer + 6-phase LC recovery middle + citalopram dose inner); default for descriptive work, opt-in for HA pre-regs; 4a/4b sub-boundary at 2022-11-17 from §7b user lived-experience |
| [`bout_level_recovery_dynamics.md`](../../methodology/bout_level_recovery_dynamics.md) *(LOCKED 2026-06-21 `c57ff3f`)* | A | Q3.x.g (spike-detecting primitive at bout resolution; CONVENTIONS §3.5 acute-load discipline) | active; canonical; per-bout operand for any Wiggers register row at within-day recovery resolution; narrow-scope lock with C4 + HA11 enabled; framework-validity gate restricted to HA11 v1 reproduction on unmedicated × train × calm-day pool |
| [`bout_level_dose_response_calibration.md`](../../methodology/bout_level_dose_response_calibration.md) *(LOCKED 2026-06-21 `c57ff3f`, sub-MD)* | A | Q3.x.d (per-bout phase-stratified β recalibration) | active; sub-MD of `bout_level_recovery_dynamics`; per-bout β recalibration over citalopram dose mirroring `citalopram_phase_stratification §5.B` at bout resolution; standalone four-input bar at §1.5 |
| [`phase_axis_collapsibility_conventions.md`](../../methodology/phase_axis_collapsibility_conventions.md) *(LOCKED 2026-06-22 `ab356d8`)* | A + B | Q3.x.c + Q4.x phase-stratification governance (HOW phases pool when needed for HA pre-regs + descriptive analyses) | active; canonical; 3-tier collapsibility hierarchy (A 4a+4b→4; B 4+5 with binding §5.A/B/C on CONFIRMED-citalopram; C full Stratum 4) + hard boundary (phase 1 ↔ 2 ↔ LC era NEVER pool); hypothesis-driven only (no data-driven pathway); audit verdict PASS-with-caveats incl. PE.1-4 plan-effectiveness dimension per user 2026-06-22 |
| [`operationalisation_support/stress_mean_sleep/`](operationalisation_support/stress_mean_sleep/) *(LANDED 2026-06-18 `84b9801`)* | A | Q3.1.a-i for `stress_mean_sleep` on Stratum 4 (Phase 1 #1) | active; first Strand A analysis; cross-referenced by HA07c/HA07d/HA08c re-interpretation work; substantive: phase-stratified distribution informs citalopram-confound reading |
| [`trajectory/recovery_arc/`](trajectory/recovery_arc/) *(v2 LANDED 2026-06-22 `8feae6a`; v1 archived at `24dad02`)* | B | Q4.1 (three-phase trajectory: pre-illness healthy → infection/acute → LC trajectory) | active; **v2 adopts the 6-phase axis** from `lc_recovery_phase_axis.md` (LOCKED `d47e0d3`); per-phase per-channel block-bootstrap CIs per §6.6; §7b falsifiability hook on 4a→4b discriminative power (`resting_hr` alone excludes 0); §5.A sub-stratification on phase-5 CONFIRMED-citalopram channels surfaces **afbouw reversal** (citalopram benefit reversible during dose reduction) |
| [`operationalisation_support/stress_low_motion_min_count_S60_Mlow/`](operationalisation_support/stress_low_motion_min_count_S60_Mlow/) *(LANDED 2026-06-22 `4318a77`)* | A | Q3.x.a-i for `stress_low_motion_min_count_S60_Mlow` on Stratum 4 (Phase 1 #3) | active; closes Phase 1 of the descriptive programme; count-primitive adaptations vs continuous-channel template; substantive: phase-shift concentrated at citalopram boundary NOT pacing boundary; E[L]\*=21.1 (longest in Strand A); HA-C4b primary channel |
| [`../../pipeline/02_features/extract_stress_bouts.py`](../../pipeline/02_features/extract_stress_bouts.py) + `per_bout_master.csv` *(LANDED 2026-06-22 `d5b394c`; external dataset)* | A | (cross-cutting infrastructure for bout-level HA pre-regs) | active; **bout-level extractor** per `bout_level_recovery_dynamics.md` LOCKED operand; 4,317 bouts × 1,479 valid days; 5 per-day aggregations emitted into `per_day_master.csv` (`bout_n_fast_recovery_day` + 4 companions per DATA_DICTIONARY §8E); enables HA11-bout-redo framework-validity check + (gated) HA-C4c substantive C4 retest |
| [`analyses/notes_categorization/categories-analysis-v1.md` + `-v2.md`](../notes_categorization/) | B | Q4.7 (notes patterns) | active; cite from `trajectory/notes_patterns/` (when spun up) |

---

## 6. Planned first analyses

After this README is locked, the first three analyses to execute (per plan v2 §11 sequencing):

### 6.1 `operationalisation_support/stress_mean_sleep/` (Strand A, first)

**Scope**: Q3.1.a-i for `stress_mean_sleep` on Stratum 4 *(r2: template extended a-i per closures D1.8, D2.6, D5.3)*. Q3.1.a (distribution shape) delegates to [`methodology/lc_phase_descriptive.md`](../../methodology/lc_phase_descriptive.md) (refresh + extend if material gaps surface) per r2 closure D6.1; Q3.1.h (outlier + calibration-drift) cross-references [`methodology/garmin_indicators_audit.md`](../../methodology/garmin_indicators_audit.md) for known issues per r2 closure D2.6.

**Inputs**: `per_day_master.csv` `stress_mean_sleep` column + `labels_crash_v2.csv` + phase-axis from [`citalopram_phase_stratification.md`](../../methodology/citalopram_phase_stratification.md) + [`lc_phase_descriptive.md`](../../methodology/lc_phase_descriptive.md) for Q3.1.a baseline + [`garmin_indicators_audit.md`](../../methodology/garmin_indicators_audit.md) for Q3.1.h.

**Outputs**:
- `run.py` — descriptive computation script
- `findings.md` — writeup covering: distribution shape delegate-or-extend (Q3.1.a), autocorrelation + E[L]* (Q3.1.b), per-phase base rates (Q3.1.c), phase-stratified distribution (Q3.1.d), near-identity check (Q3.1.e), crash-vs-normal Cohen's d with crash-drop sensitivity (Q3.1.f), spike-primitive availability (Q3.1.g), outlier + calibration-drift (Q3.1.h), covariate-sensitivity readiness (Q3.1.i).

**Dependencies**: none upstream; uses existing per_day_master + labels_crash_v2 + intervention-phase MD + lc_phase_descriptive.md + garmin_indicators_audit.md.

**Why first**: most-cited CONFIRMED-citalopram channel; HA pre-reg drafting on this channel will block on it; HA07c re-interpretation hinges on it.

**Estimated effort**: 2-3 hours.

### 6.2 `trajectory/recovery_arc/` (Strand B, second — three-phase scope per r3 2026-06-18)

**Scope**: Q4.1 (three-phase trajectory: pre-illness healthy baseline → immediate infection/acute → LC trajectory recovery shape, with documented event overlays). Per the r3-extended Q4.1 framing in §2 + §4.1, this analysis now leverages **all ~5 years of Garmin data** (2021-08-16 → present), not just the LC era (2022-09-03 →).

**Pre-spin-up requirement (Strand B discipline per §7b)**: user operationalisation interview MUST happen before script.py. Key choice points to surface in the Q&A brief:
- **COVID infection-date boundary**: which date marks the pre-illness → acute transition (first symptoms / PCR-confirmed / sustained symptom onset / official diagnosis)?
- **Acute-phase endpoint**: how to define the acute → LC transition (fixed window vs symptom-driven vs autonomic-signal-driven)?
- **Channel set per phase**: which Garmin channels are in scope for each phase (some have coverage gaps; e.g. gevoelscore doesn't exist pre-2022-09-03)?
- **Event overlays**: which documented events to overlay (CPAP / Ergotherapie / citalopram phases / other)?

**Inputs**: full `per_day_master.csv` corpus + S01/S02 archived findings as historical reference (note: S01/S02 were both framed only on the LC era, so the pre-illness + acute extensions are net-new) + intervention phase axis + COVID-infection-date + documented events list (both surfaced via the operationalisation interview).

**Outputs**:
- `run.py` — refreshed three-phase analysis on current corpus
- `findings.md` — three-phase story: (a) pre-illness healthy Garmin baseline characterisation (first time formalised), (b) acute-infection phase shifts vs healthy baseline, (c) LC-trajectory recovery shape vs healthy baseline + acute-phase. Headline + event overlays + inflection-point identification + comparison-to-S01/S02-archived for the LC-era sub-finding.

**Dependencies**: S01/S02 archived for reference; current corpus; **locked operationalisation from §7b user interview** (no script.py without it).

**Why second**: load-bearing trajectory story is currently invisible to fresh readers; consolidates scattered work; refreshable as cadence work; pre-illness baseline characterisation is the single largest gap (never formally surfaced).

**Estimated effort**: 6-8 hours (r3 bump from 4-5h; reflects the pre-illness + acute-phase scope extension + user interview round-trip).

### 6.3 `operationalisation_support/stress_low_motion_min_count_S60_Mlow/` (Strand A, third — per r2 closure D1.8)

**Scope**: Q3.x.a-i for `stress_low_motion_min_count_S60_Mlow` on Stratum 4. **Hits two coverage gaps with one analysis**: CONFIRMED-citalopram channel (per audit D5.3) AND spike-detecting primitive (per audit D1.8 + CONVENTIONS §3.5).

**Inputs**: `per_day_master.csv` `stress_low_motion_min_count_S60_Mlow` column + `labels_crash_v2.csv` + phase-axis from [`citalopram_phase_stratification.md`](../../methodology/citalopram_phase_stratification.md) + [`methodology/stress_low_motion_primitive.md`](../../methodology/stress_low_motion_primitive.md) (definitional substrate) + [`garmin_exploration/stress_low_motion_viz/`](../garmin_exploration/stress_low_motion_viz/) (existing primitive characterisation) + [`garmin_indicators_audit.md`](../../methodology/garmin_indicators_audit.md) for Q3.x.h.

**Outputs**: same shape as §6.1 — `run.py` + `findings.md` covering Q3.x.a-i for this channel.

**Dependencies**: `stress_low_motion_primitive.md` must be locked (it is, Session E lock 2026-06-15).

**Why third (not deferred)**: replaces the previously-TBD candidates (`cohort_topology` / `all_day_stress_avg` / `bb_lowest`) because this analysis covers two audit-surfaced gaps (D1.8 spike primitives + D5.3 HA pre-reg covariate-sensitivity readiness for the HA-C4b v2 channel) in one analysis. **The deferred candidates remain on the queue for the fourth slot when HA-P6 / HA-C3 / HA-C4 results land:**
- `trajectory/cohort_topology/` — if HA-P6 result raises questions about dip-cluster overlay or recovery-window distributions. Q4.4.
- `operationalisation_support/all_day_stress_avg/` — if HA-C3 drafting indicates it touches this column. Q3.2.
- `operationalisation_support/bb_lowest/` — if HA-C4b v2 result reading wants a phase-stratified reference for the BB-floor candidate channel. Q3.3.

**Estimated effort**: 2-3 hours.

---

## 7. Discipline

### 7a. Per-analysis README pattern

Each analysis folder's README answers, in plain prose (no rigid template):
- **Research question** — what we're trying to learn
- **Method** — what we did
- **Result** — headline finding(s) + figures/tables
- **Status** — current / refresh-due / superseded
- **Cross-references** — HA pre-regs citing this; related analyses; methodology MDs

Mirrors the existing [`garmin_exploration/<topic>/README.md`](../garmin_exploration/) pattern. No standardised section template forced.

### 7b. Strand B operationalisation interview (r3 added 2026-06-18)

**Strand B analyses require a user operationalisation interview before script.py is written.** The default is canonical; compression (skip interview) is the documented exception, not the rule.

**Why**: Strand A is template-driven (per-channel Q3.x.a-i questions are deterministic; spin up + run). Strand B questions are open and cross-cutting — every analysis has multiple defensible operationalisations:
- Q4.1 recovery arc: which date marks COVID infection? Which channels per phase? Acute-phase boundary definition?
- Q4.2 intervention cross-channel: which boundary (2024-04 buildup / 2026-03 afbouw)? Which channels in scope? Pre/post window length?
- Q4.3 era boundaries: which alternatives to compare against the current Stratum 4?
- Q4.4 cohort topology: dip-cluster proximity rule? Recovery-window length?
- Q4.7 notes patterns: which categorisation slices? Time-series resolution?
- Q4.9 subjective↔objective coupling: which Garmin channel set? Coupling measure?

Different operationalisations yield different findings. The user owns the choice.

**Protocol**:
1. **Claude drafts a question-and-options brief** for the analysis — what the question asks, 2-4 defensible operationalisation options per choice point, the trade-offs of each.
2. **User picks** (or proposes a fourth option). Use the AskUserQuestion tool pattern for the round-trip.
3. **Locked operationalisation goes into the analysis README** before script.py is written (Authorship-block-equivalent record).
4. **script.py implements the locked operationalisation** — no on-the-fly choices.
5. After result lands, descriptive interpretation: any operationalisation-sensitive finding is flagged as such.

**Compression (skip interview)** is acceptable for:
- Pure refresh analyses where the operationalisation is unchanged from a prior locked run (just rerun with new data).
- Mechanically derivative analyses (e.g. extending an existing analysis by one more channel where the per-channel mechanics are already locked).

When compressed, the analysis README must include a one-line `Compression: operationalisation-interview skipped because <reason>` justification.

### 7c. Integration with HA-* discipline (Phase 4 — after ≥3 analyses land)

Amendments to [`hypothesis_lock_process.md`](../../methodology/hypothesis_lock_process.md):
- §3.2 step 4 §3 (Data sources): "cite the relevant Strand A descriptive analysis for each column-cluster used; if none exists, spin one up first"
- §5 sanity-check row: "Are descriptive analyses cited for §3 columns + their distributions referenced for §7 anchor calibration?" (initially soft; promote to lock-blocking once 3+ analyses are landed and the discipline is proven)
- §3.8 (deferred): potential 5th lock-commit confirmation gate

### 7d. Refresh cadence

- **Strand A** analyses refresh when the underlying column's distribution shifts materially (new data alters base rates by > 20%, or new intervention boundary lands). Trigger: HA-* result re-interpretation flag.
- **Strand B** analyses refresh on cadence:
  - `recovery_arc` — quarterly or when an HA-* result shifts the story
  - `intervention_cross_channel` — when a new boundary is investigated or a new channel CONFIRMED/REJECTED
  - `cohort_topology` — when crash_v3 mechanism-subtyping lands OR when N_crashes increases by > 5

---

## 8. What this document IS and IS NOT

**IS**:
- A research-programme scoping artefact for the descriptive layer
- A list of research questions the programme will address, organised by strand
- An index of existing descriptive work (already-done; stays in place)
- A pre-execution declaration of the first 3 analyses to spin up

**IS NOT**:
- A methodology lock (specific statistical choices live in [`methodology/`](../../methodology/) MDs)
- A hypothesis pre-reg (no falsification claim; descriptive only)
- A binding commitment to do all Strand A questions for all channels (only those that surface as needs)
- A replacement for [`STOCKTAKE.md`](../../STOCKTAKE.md) (this is one layer of the cross-cutting view; STOCKTAKE indexes this)

**Out of scope** (deferred):
- Automated descriptive-card regeneration
- Interactive descriptive dashboards
- A formal methodology MD on the descriptive-research discipline (write after first 3 analyses surface what discipline actually works)

---

## 9. Review + acceptance protocol

The user reviews this README before any analysis is spun up. Per the lock-process discipline pattern (reviewer-mode-with-authorization), explicit acceptance = lock signal.

**Acceptance checklist** (user reads + confirms):
1. The two-strand framing is correct (or proposes amendments)
2. The Strand A questions Q3.1.a-f for the 3 CONFIRMED-citalopram channels are the right scope
3. The Strand B questions Q4.1-Q4.7 capture the multi-year-trajectory work that matters (or surfaces additional questions)
4. The existing-work index in §5 is complete (or flags missing artefacts)
5. The first 3 analyses (§6.1 + §6.2 + §6.3-TBD) are the right priorities

**On acceptance**:
- Update Authorship block status to `**Status: LOCKED <date> by user acceptance.**`
- Commit message: `research(descriptive): programme README locked — first 3 analyses authorised`
- Next session: execute §6.1 (`operationalisation_support/stress_mean_sleep/`) per the discipline in §7a

**On revision-recommended**:
- Update README per user feedback
- Re-submit for acceptance (no formal fresh-session re-audit at this level; it's a programme-scoping doc, not a pre-reg with falsification claim)

**Review report (if any)**: lands at `docs/research/reviews/descriptive-programme-2026-06-16.md` if the user runs a fresh-session `/research-review` on this README — optional but available.
