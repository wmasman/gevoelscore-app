# `trajectory/recovery_arc/` — Multi-year recovery shape across three phases

## v2 status — refreshed 2026-06-22 on locked 6-phase axis

v2 adopts the 6-phase LC recovery axis from
[`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md)
(LOCKED `d47e0d3` 2026-06-19) replacing v1's 4-phase data-given axis. Adds
block-bootstrap CIs per `§6.6`, honors the `§5.4` tight-n caveat for sub-phase
4a (56 days), and adds the `§7b` falsifiability hook test as a Layer 1
sensitivity arm. v1 (commit `24dad02`) stands as historical record;
substantive v1 findings (autonomic-load family acute-spike pattern,
recovery-family coverage-dominated trajectory, cardiovascular acute-DIP,
6/7 factor-of-2 E[L]\* flag) carry forward + decompose at v2 per-phase
resolution. See [`findings.md`](findings.md) for v2 headlines.

The §7b operationalisation interview answers from v1 carry forward verbatim
(2026-06-18 user-locked); no new interview required for v2.

---

## Authorship

- **Drafted**: 2026-06-18 by Claude (Opus 4.7), in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked)
- **Authorising user**: user (name redacted for publication-safety per `audit_for_publication.py` discipline)
- **Drafting-session context**: Phase 1 second analysis of the descriptive research programme. Strand B operationalisation interview completed 2026-06-18 per [`../../README.md` §7b](../../README.md#7b-strand-b-operationalisation-interview-r3-added-2026-06-18) protocol; user-locked framings on 4 choice points; concrete dates resolved from canonical methodology MDs ([`lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) + [`intervention_effects_descriptive.md`](../../../../methodology/intervention_effects_descriptive.md) + [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md)).
- **User-locked operationalisation** (from §7b interview):
  - **COVID infection-date boundary**: *first symptoms* (per user: "first symptoms = PCR-positive home test date; within 1-2 days of infection") = **2022-03-21**
  - **Acute-phase endpoint**: *symptom-driven* (clinical / lived-experience LC-onset event, "Monday after Fietsweekend Ardennen" per [`lc_era_temporal_segmentation.md §3`](../../../../methodology/lc_era_temporal_segmentation.md)) = **2022-04-04**
  - **Channel set**: *7-channel HA-P6 set* (cross-test consistency; extends HA-P6 per-channel post-crash trajectories back into pre-illness + acute phases)
  - **Event overlays**: *Intervention + medical* (COVID infection, Ergotherapie start + end, CPAP start + **end**, citalopram phases through afbouw start — user explicit reminders to include CPAP end AND to mark post-afbouw out-of-scope since the corpus ends 2026-06-04, no post-afbouw data yet)
- **Status**: **operationalisation locked; awaits fresh-agent execution.** See [handoff brief](file:///C:/Users/Gebruiker/.claude/plans/session-descriptive-recovery-arc-handoff-2026-06-18.md).

---

## Research question

Per [descriptive/README §4.1](../../README.md#41-recovery-arc-three-phase-healthy--infection--trajectory) (three-phase reframe added r3 2026-06-18):

**What is the three-phase shape of the data?**

- **(a) Pre-illness healthy baseline** (2021-08-16 → 2022-03-20) — what does healthy look like in the Garmin signals? *(~7 months of pre-illness Garmin data; never formally characterised; the single largest gap this analysis closes.)*
- **(b) Acute infection / early recovery** (2022-03-21 → 2022-04-03) — how do the signals shift during acute infection? *(14 days; short; usable as a labelled acute-infection contrast for Garmin-only signals.)*
- **(c) LC trajectory** (2022-04-04 → present, ~4+ years) — multi-year recovery arc, inflection points, alignment with documented events.

The healthy baseline (a) is a **stronger comparison** than early-LC-as-proxy-for-healthy. Existing trajectory work (archived S01 + S02) was framed only on the LC era; this analysis extends the framing to include phases (a) and (b).

---

## Locked operationalisation

### 1. Date boundaries (per [`lc_era_temporal_segmentation.md §3`](../../../../methodology/lc_era_temporal_segmentation.md))

| phase | window | duration | data scope |
|---|---|---|---|
| Pre-illness healthy baseline | 2021-08-16 → 2022-03-20 | ~217 days | Garmin only |
| Acute infection | 2022-03-21 → 2022-04-03 | 14 days | Garmin only |
| LC, pre-gevoelscore | 2022-04-04 → 2022-09-02 | ~152 days | Garmin only |
| LC with gevoelscore (Stratum 4) | 2022-09-03 → as-of-date | ~1380+ days (ongoing) | Garmin + gevoelscore + crash labels |

### 2. 7-channel set (locked from [HA-P6 §4.1 v3](../../../hypotheses/HA-P6/hypothesis.md))

| channel | dose-response status | family | per-phase coverage notes |
|---|---|---|---|
| `stress_mean_sleep` | CONFIRMED dose-modulated (β=+0.43/mg) | autonomic-load | full coverage all phases |
| `all_day_stress_avg` | CONFIRMED dose-modulated (β=+0.57/mg; strongest) | autonomic-load | full coverage all phases |
| `bb_lowest` | CONFIRMED dose-modulated (β=−1.13/mg) | recovery | full coverage all phases |
| `bb_overnight_gain` | partial (no buildup data) | recovery | **NaN before 2024-09-18**; only available in late-LC trajectory; pre-illness + acute + early-LC + early-buildup all NaN |
| `resting_hr` | weak (consistent direction, near-significance) | cardiovascular | full coverage all phases |
| `gevoelscore` | outcome-channel ([`intervention_effects §3b`](../../../../methodology/intervention_effects_descriptive.md#3b-outcome-channel-contamination-check-gevoelscore)) | felt-state | **only from 2022-09-03**; absent in pre-illness + acute + LC-pre-gevoelscore phases |
| `stress_low_motion_min_count_S60_Mlow` | indirectly dose-modulated (raw stress threshold) | autonomic-load (concurrence) | full coverage all phases (1722 valid days per [`stress_low_motion_primitive.md`](../../../../methodology/stress_low_motion_primitive.md)) |

### 3. Event overlays (locked: Intervention + medical; user explicit reminder to include CPAP end)

| event | date | source |
|---|---|---|
| **COVID infection** (first symptoms = home PCR positive) | 2022-03-21 | [`lc_era_temporal_segmentation.md §3`](../../../../methodology/lc_era_temporal_segmentation.md) |
| **Ergotherapie Rouschop start** | 2022-09-22 | [`intervention_effects_descriptive.md §3`](../../../../methodology/intervention_effects_descriptive.md) |
| **Ergotherapie Rouschop end** (~13-week estimate) | 2022-12-22 | [`intervention_effects_descriptive.md §3`](../../../../methodology/intervention_effects_descriptive.md) (end-date is approximate; findings around end-boundary carry lower weight per the MD) |
| **CPAP-interventie start** | 2024-01-10 | [`intervention_effects_descriptive.md §3`](../../../../methodology/intervention_effects_descriptive.md) |
| **CPAP-interventie end** | 2024-04-16 | [`intervention_effects_descriptive.md §3`](../../../../methodology/intervention_effects_descriptive.md) (refined 2026-06-14 from 2024-04-17 → 2024-04-16; the test-apparaat night itself) |
| **Citalopram buildup start** | 2024-04-09 | [`citalopram_phase_stratification.md §3`](../../../../methodology/citalopram_phase_stratification.md) |
| **Citalopram buildup → consolidation** | 2024-06-20 | [`citalopram_phase_stratification.md §3`](../../../../methodology/citalopram_phase_stratification.md) |
| **Citalopram consolidation → afbouw** | 2026-03-20 | [`citalopram_phase_stratification.md §3`](../../../../methodology/citalopram_phase_stratification.md) |

**Post-afbouw out-of-scope caveat** (user-flagged 2026-06-18): per [`citalopram_phase_stratification.md §3`](../../../../methodology/citalopram_phase_stratification.md) the post-afbouw phase starts 2026-06-05; per [STOCKTAKE §1](../../../../STOCKTAKE.md#1-the-corpus) the Garmin coverage ends 2026-06-04. **The dataset ends inside the afbouw phase — no post-afbouw data yet.** The afbouw phase has ~76 days of data (2026-03-20 → 2026-06-04). No event marker for post-afbouw start; the right edge of the trajectory plot is the data-cut at 2026-06-04.

**Boundary-collision caveat** (per [`intervention_effects_descriptive.md §2b`](../../../../methodology/intervention_effects_descriptive.md#2b-structural-caveat--the-2024-04-boundary-collision)): the 2024-04 cluster has **Citalopram buildup start (2024-04-09) and CPAP end (2024-04-16) only 7 days apart**. Both events get separate timeline markers; their effects are confounded in the data. For recovery_arc the events are shown but their independent contributions are not testable in this descriptive design (per intervention_effects §8.3 deferred to ITS in a future analysis).

### 4. Statistical framework

- **Per-channel × per-phase**: median + IQR computed on the full phase window; 30-day rolling median trajectory across the whole 2021-08-16 → as-of-date corpus with event-overlay markers
- **Block-bootstrap 95% CIs**: at E[L]=7 default per [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (per-channel data-driven E[L]* companion + factor-of-2 deviation flag — same discipline as HA-P6 v3 § 4.8.1, simplified for descriptive use)
- **Cross-phase comparison**: descriptive only — NO inferential test (Layer 1 descriptive per CONVENTIONS §2.1); CI-overlap pattern surfaced per channel
- **Detrend sensitivity per [CONVENTIONS §3.7](../../../../CONVENTIONS.md) binding**: per channel, rolling 90-day detrend → recompute phase-by-phase trajectory; report "survives detrend?" per channel × phase cell (mirrors HA-P6's §3.7 column structure)

### 5. Output format

- `findings.md` — per-channel trajectory characterisation (one section per channel, all phases) + cross-phase comparison narrative + event-overlay reading + cross-channel pattern synthesis (closing paragraph reading: what does the body do across the 5-year arc?)
- `run.py` — descriptive computation script (uses `_utils/frame.py::load_master` + `_utils/inference.py::stationary_bootstrap_ci` + `compute_data_driven_block_length`)
- `plots/` — per-channel trajectory PNGs (7 channels × multi-year x-axis) with event-overlay vertical lines + phase-region shading
- `summary.json` — machine-readable per-channel × per-phase statistics (median / IQR / CI95 / detrend-survives flag / E[L]*)

---

## Method

Per the locked operationalisation above. The analysis loads `per_day_master.csv` from `$GEVOELSCORE_DATA_PATH`, filters to the 7 channels, computes per-phase descriptive statistics (median, IQR, rolling 30-day trajectory, CI95 at E[L]=7 + per-channel E[L]*), generates per-channel trajectory plots with event overlays at the 9 documented dates, and emits a `findings.md` with the per-channel × per-phase narrative + cross-phase pattern reading + closing synthesis.

**Strand B discipline reminders** (per [`descriptive/README §7b`](../../README.md#7b-strand-b-operationalisation-interview-r3-added-2026-06-18)):
- script.py implements the locked operationalisation — **no on-the-fly choices**
- Any post-execution finding sensitive to a different operationalisation choice is **flagged as such** in `findings.md`
- This is **Layer 1 descriptive** per CONVENTIONS §2.1 — NO causal claims; NO SUPPORTED bar; report what the data shows + which phase × channel patterns surface

---

## Cross-references

- [`../../README.md`](../../README.md) §4.1 (research question source — three-phase reframe r3 2026-06-18) + §6.2 (analysis scope) + §7b (operationalisation interview protocol)
- [`../../../../methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) §3 (canonical 4-phase date boundaries)
- [`../../../../methodology/intervention_effects_descriptive.md`](../../../../methodology/intervention_effects_descriptive.md) §3 (CPAP + Ergotherapie + Citalopram event dates) + §2b (2024-04 boundary-collision caveat)
- [`../../../../methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) §3 (citalopram phase boundaries)
- [`../../../hypotheses/HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) §4.1 (locked 7-channel set; this analysis extends HA-P6's per-channel post-crash trajectory back into pre-illness + acute phases)
- [`../../../../methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (block-length policy)
- [`../../../hypotheses/_archive/S01-stabilisation-trajectories/`](../../../hypotheses/_archive/S01-stabilisation-trajectories/) + [`S02-score-trajectory/`](../../../hypotheses/_archive/S02-score-trajectory/) — historical LC-era-only trajectory work; this analysis extends to three phases (does NOT supersede — S01/S02 stay archived; the multi-year-arc narrative is consolidated here for ongoing refresh)

---

## Status — next step

**Drafted operationalisation locked.** Fresh-agent execution handoff at [`session-descriptive-recovery-arc-handoff-2026-06-18.md`](file:///C:/Users/Gebruiker/.claude/plans/session-descriptive-recovery-arc-handoff-2026-06-18.md). When result lands (`findings.md` + plots + summary.json), the analysis is current; refresh cadence per [descriptive/README §7d](../../README.md#7d-refresh-cadence) — quarterly or when an HA-* result shifts the story.
