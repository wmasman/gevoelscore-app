# Descriptive precondition — pre-LC training-load data coverage

**Status**: producer-mode descriptive precondition, a COVERAGE-ONLY
follow-up to R23 (the COVID peri-event check). This artefact
characterises **what Garmin training-activity data exists** for the
pre-LC era and its run-up, expressed **strictly as row-presence /
non-null / session-count facts**. It backs a later exploratory test of
the post-hoc hypothesis that *heavy endurance training in the months
before the 2022-03 COVID infection suppressed the participant's baseline
RHR, complicating the R23 result.* It is Layer-1 descriptive: **no causal
or interpretive marks** per [CONVENTIONS §4.1](../../../CONVENTIONS.md).
Drafted 2026-07-02 by Claude (Opus 4.8) producer-mode descriptive
precondition, for the participant-researcher (repo owner).

> ## COVERAGE-ONLY / NO-OUTCOME-PEEK STATEMENT (binding)
>
> The exploratory test this precondition backs is *whether pre-infection
> training load relates to resting heart rate (RHR)*. That test is only
> credible if the training-vs-RHR relationship is unseen when the design
> locks. This precondition characterises **only**: which training-data
> sources exist, their paths, the training-load metric inventory
> (column/field names), row-presence / non-null day counts and
> logged-activity session counts across the pre-LC era and its run-up,
> the infection-window and week-12 activity counts, and the data
> granularity. It does **NOT** compute, estimate, plot, or infer any
> relationship, trend, contrast, or correlation between training load and
> RHR. **No training-load VALUES were analysed against RHR, no
> training-vs-RHR trend or contrast was computed, and no RHR values
> appear in this document at all.** The training-load-to-RHR relationship
> IS the later test; it runs only after that test's design locks (per
> [`_plan_results_analysis_layer.md`](../../../methodology/_plan_results_analysis_layer.md)
> §3.5 hard rule + [CONVENTIONS §1.2](../../../CONVENTIONS.md)). Every
> number below is a **row-presence / non-null count or a logged-session
> count** — never a load value analysed against an outcome. Named per
> [CONVENTIONS §3.6](../../../CONVENTIONS.md): each count carries its
> scheme, unit, and source.

---

## 1. Era location

The bands are inherited verbatim from the R23 precondition
[`../peri_event_covid/precondition.md`](../peri_event_covid/precondition.md)
and [CONVENTIONS §5](../../../CONVENTIONS.md):

| Band | Dates | Length | `lc_phase` |
|---|---|---|---|
| **Pre-LC (Stratum 1, healthy)** | 2021-08-16 → 2022-03-20 | **217 days** | `pre_corona` |
| Infection window (Stratum 2) | 2022-03-21 → 2022-04-03 | 14 days | `corona_infection` |
| Week-12 illness week | 2022-03-21 → 2022-03-27 | 7 days | (within infection) |

- The pre-LC band's left edge (2021-08-16) is the **GDPR-dump start /
  Stratum-1 start** and is **also the earliest logged training activity
  in the corpus** (see §5 data-quality flag D1). The "run-up" therefore
  coincides with the pre-LC band: no earlier 2021 training season is
  present in this dump.
- The `annotations.yaml` marker for this era records a
  `Training-periode ... voorbereiding Ardennen` and asserts
  *"0 training-activities in week 12"* (the corona-ziek week). That
  presence/count claim is **verified** below (§3, week-12 row).

## 2. Training-data source inventory

Three source files carry personal training-activity data. All resolve
under `GEVOELSCORE_DATA_PATH`
(`C:\Users\Gebruiker\Documents\gevoelscore-data\`).

| # | Source path | Grain | Role |
|---|---|---|---|
| S1 | `processed/garmin/activities.csv` | **session-level** (one row per logged activity, timestamped) | primary training-load record |
| S2 | `processed/garmin/activity_features_daily.csv` | daily-aggregated (one row per calendar day) | daily rollup of S1 + UDS activity fields |
| S3 | `unified/per_day_master.csv` | daily-aggregated (one row per calendar day) | unified corpus; carries UDS/exertion columns folded from S2 |

Provenance (per `raw/garmin/README.md`): S1 is written by
`02_extract_activities.py` (in
`docs/research/analyses/garmin_exploration/`) from
`summarizedActivities.json` + FIT files in the Garmin GDPR dump at
`C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\`.

**Not a source (decoy)**: the top-level `garmin data/` folder is the raw
GDPR dump; its many `AVC_*` / `DI_*` / `ENG_*` subfolders are Garmin
**corporate/service** domains, not personal fitness records. The
personal activity record inside it is `summarizedActivities.json`, which
S1 already extracts. The repo folder `docs/research/garmin/` referenced
in project memory does **not** exist at that path; the live Garmin
research code is under
`docs/research/analyses/garmin_exploration/` and
`docs/research/pipeline/01_extract/`.

## 3. Training-load metric inventory

### 3.1 Session-level metrics — S1 `processed/garmin/activities.csv`

One row per logged activity. Timestamped by `start_date`. Columns:

| Field | Meaning |
|---|---|
| `start_date` | activity date (session timestamp) |
| `activity_type` | walking / cycling / running / breathwork / sailing_v2 / incident_detected |
| `name` | activity label |
| `duration_min`, `moving_duration_min` | elapsed / moving minutes |
| `distance_m` | distance (metres) |
| `avg_hr`, `max_hr`, `min_hr` | session heart rate summary (session-internal; **not** the daily-RHR outcome channel) |
| `aerobic_te`, `anaerobic_te` | Garmin/Firstbeat Training Effect (aerobic, anaerobic) |
| `calories` | activity calories |
| `intensity_min_total`, `moderate_min`, `vigorous_min` | intensity minutes |
| `time_in_zone_4plus_min`, `time_in_zone_0_min` | HR-zone time |
| `elevation_gain_m`, `elevation_loss_m` | elevation |
| `start_stress`, `end_stress`, `difference_stress`, `avg_stress`, `max_stress` | session stress (Garmin GSS; **all null in pre-LC**, see §3.3) |
| `workout_rpe`, `workout_feel` | subjective RPE / feel |

Note: there is **no** single "Garmin training load / TSS" column and
**no** acute:chronic training-load ratio column in S1; the closest
load primitives are `aerobic_te` / `anaerobic_te` (Training Effect) plus
duration / distance / intensity-minutes / zone-4+ time.

### 3.2 Daily-aggregated metrics — S2 `activity_features_daily.csv` / S3 `per_day_master.csv`

Training-relevant daily columns (present in S2; the UDS/exertion subset
is folded into S3):

`n_activities`, `total_activity_min`, `max_activity_min`,
`total_distance_km`, `max_aerobicTE`, `max_anaerobicTE`,
`total_time_zone4plus_min`, `effective_exertion_min`,
`effective_exertion_slope_28d`, `vigorous_min_uds`, `moderate_min_uds`,
`highly_active_sec`, `active_sec`, `max_hr_uds`, `max_avg_hr_uds`,
`total_steps`, `daily_step_goal`, plus the derived exertion-class /
push-burden / rank columns.

In S3 `per_day_master.csv` the folded training columns include
`total_steps`, `total_calories`, `highly_active_sec`, `active_sec`,
`effective_exertion_min`, `effective_exertion_slope_28d`.

### 3.3 Metric-availability flags (presence, not values)

- `avg_stress` / `max_stress` in S1 are **non-null on 0 / 103** pre-LC
  sessions (scheme: non-null session count; unit: sessions; source: S1
  pre-LC band). Session-level stress is unusable in this era.
- `is_vigorous_day` in S2 is **non-null on 0 / 217** pre-LC days
  (all-null flag; unit: days; source: S2 pre-LC band). It is not
  populated for this era.
- `max_aerobicTE` / `max_anaerobicTE` in S2 are non-null only on the
  99 activity-present days (they are undefined on rest days), not all
  217 (see §3.4 table).

### 3.4 Coverage counts

Named per [CONVENTIONS §3.6](../../../CONVENTIONS.md): **scheme = non-null
row/session presence; unit = as stated; source = as stated.**

**A. Session-level presence — S1 `activities.csv`, pre-LC band (217 cal days):**

| Quantity | Count (unit) |
|---|---|
| Logged activity **sessions** in pre-LC band | **103** (sessions) |
| Distinct **calendar days** with >=1 logged activity | **99 / 217** (days; 45.6%) |
| Per-session non-null: `duration_min` | 103 / 103 (sessions) |
| Per-session non-null: `distance_m` | 103 / 103 |
| Per-session non-null: `aerobic_te` | 103 / 103 |
| Per-session non-null: `anaerobic_te` | 103 / 103 |
| Per-session non-null: `calories` | 103 / 103 |
| Per-session non-null: `intensity_min_total` | 103 / 103 |
| Per-session non-null: `time_in_zone_4plus_min` | 103 / 103 |
| Per-session non-null: `moderate_min` | 102 / 103 |
| Per-session non-null: `vigorous_min` | 102 / 103 |
| Per-session non-null: `elevation_gain_m` | 101 / 103 |
| Per-session non-null: `moving_duration_min` | 83 / 103 |
| Per-session non-null: `workout_rpe` | 78 / 103 |
| Per-session non-null: `workout_feel` | 78 / 103 |

Pre-LC session distribution by activity type: running 82, cycling 17,
walking 3, incident_detected 1 (source: S1 pre-LC band). Pre-LC sessions
by month: 2021-08 = 11, 2021-09 = 12, 2021-10 = 15, 2021-11 = 14,
2021-12 = 16, 2022-01 = 15, 2022-02 = 13, 2022-03 = 7 (unit: sessions;
source: S1) — a training presence spanning the full run-up.

**B. Daily-aggregated presence — S2 `activity_features_daily.csv`, pre-LC band:**

| Column | Days with non-null row | Notes |
|---|---|---|
| daily rows present | 217 / 217 | full band |
| `n_activities` | 217 / 217 | zero-filled on rest days |
| `total_activity_min` | 217 / 217 | zero-filled on rest days |
| `total_distance_km` | 217 / 217 | zero-filled on rest days |
| `total_time_zone4plus_min` | 217 / 217 | |
| `effective_exertion_min` | 217 / 217 | |
| `vigorous_min_uds` / `moderate_min_uds` | 217 / 217 | UDS-sourced |
| `total_steps` | 217 / 217 | UDS-sourced |
| `highly_active_sec` / `active_sec` | 217 / 217 | UDS-sourced |
| `max_hr_uds` | 217 / 217 | |
| **days with `n_activities` > 0** | **99 / 217** | matches S1 distinct-day count |
| `max_aerobicTE` / `max_anaerobicTE` | 99 / 217 | non-null only where an activity exists |

The 99 activity-present days in S2 reconcile with the 99 distinct
activity days in S1.

**C. Infection window 2022-03-21 → 2022-04-03 (14 days):**

| Quantity | Count |
|---|---|
| Logged activity sessions (S1) | **1** (session) |
| Date of that session | **2022-04-03** (cycling, 162.2 min per S2 daily rollup) |
| Days 2022-03-21 → 2022-04-02 with any session | 0 |

**D. Week-12 illness week 2022-03-21 → 2022-03-27 (7 days):**

| Quantity | Count |
|---|---|
| Logged activity sessions (S1) | **0** (sessions) |

The annotation claim *"0 training-activities in week 12"* is
**verified**: 0 logged sessions in S1 over 2022-03-21 → 2022-03-27
(scheme: session count; unit: sessions; source: S1). The single
infection-window activity falls on 2022-04-03, outside week 12.

## 4. Granularity

Training data is available at **session level** (S1 `activities.csv`:
one timestamped row per logged activity, with per-session duration,
distance, Training Effect, intensity minutes, zone time, calories). This
is the finer grain preferred for load reconstruction. A
**daily-aggregated** rollup (S2 / S3) is also available for day-level
joins. Both grains cover the full pre-LC band. For the later exploratory
test, **session-level load reconstruction is feasible** for the pre-LC
run-up.

## 5. Data-quality flags (row-presence view only)

- **D1 — left-edge boundary.** The earliest logged activity is
  2021-08-16, the same day the GDPR dump begins. Any 2021 (or earlier)
  training season **before** that date is **absent** from this dump.
  The run-up is left-censored at the pre-LC band start; "months before
  the infection" is covered back to 2021-08-16 only (≈ 7 months of
  run-up), not the full prior training year.
- **D2 — session-stress unusable in era.** `avg_stress` / `max_stress`
  in S1 are null for all 103 pre-LC sessions (§3.3). Session-level GSS
  cannot be used as a per-activity load proxy here.
- **D3 — `is_vigorous_day` not populated.** All-null across the pre-LC
  band (§3.3); use `vigorous_min_uds` / `vigorous_min` instead if a
  vigorous flag is needed downstream.
- **D4 — subjective fields thinner.** `workout_rpe` / `workout_feel`
  present on 78 / 103 sessions; `moving_duration_min` on 83 / 103.
  Objective load metrics (duration, distance, TE, intensity minutes,
  zone-4+) are 100% or near-100% present.
- **D5 — daily zero-fill vs true missing.** Daily columns in S2 are
  zero-filled on rest days (n_activities = 0), so "217/217 non-null"
  reflects presence-with-explicit-zero, not 217 training days. The
  training-present grain is the 99-day / 103-session count.
- **No device-change gap flagged** within the pre-LC band from
  row-presence: activity rows are continuous month-to-month across the
  run-up (§3.4-A monthly distribution shows every month 2021-08 →
  2022-03 populated).

## 6. Open inputs

| # | What is missing | Blocks | Cheapest path | Fallback |
|---|---|---|---|---|
| 1 | User lock on the later exploratory test's design (which load primitive, which window, matched-null construction) | The pre-registration of the training-vs-RHR exploratory test | that test's methodology MD + fresh-session `/research-methodology-review` | — |
| 2 | Decision on load construct: raw per-session (duration / distance / TE / intensity-min) vs a derived rolling training-load / acute:chronic proxy (none exists as a column today; would need construction) | Operationalising "training load" for the test | build a rolling-load column in the pipeline, presence-audited before any outcome join | use daily `effective_exertion_min` + `total_activity_min` as the load axis |
| 3 | Whether left-censoring at 2021-08-16 (D1) is acceptable given "months before" framing | Interpreting a null / positive result | confirm 7-month run-up suffices for the hypothesis | narrow hypothesis to the observable run-up window |

## 7. Cross-references

- [`../peri_event_covid/precondition.md`](../peri_event_covid/precondition.md)
  — the R23 peri-event precondition this follow-up extends (band
  definitions, week-12 annotation, comparator design space).
- `processed/garmin/activities.csv` (S1) — the session-level training
  record; provenance in `raw/garmin/README.md`.
- `processed/garmin/activity_features_daily.csv` (S2) — daily rollup.
- `unified/per_day_master.csv` (S3) — unified corpus daily columns.
- [`docs/research/analyses/garmin_exploration/README.md`](../../garmin_exploration/README.md)
  — Garmin extraction pipeline + file taxonomy.
- [CONVENTIONS.md](../../../CONVENTIONS.md) §1.2 (no outcome peek), §3.6
  (named counts), §4.1 (no interpretive marks), §5 (LC timeline anchor).
