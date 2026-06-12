# Garmin indicators audit — provenance + known issues + inventory

**Status**: navigation index, locked 2026-06-11; v3.2 preference clause added 2026-06-12.

## Rule for new analyses (v3.2 lagged baseline)

New analyses on `per_day_master.csv` use the **v3.2 lagged-baseline**
exertion columns. Two variants exist (added 2026-06-12):

- **`_lagged_lcera`** (LC-era-only baseline, restricted to dates >=
  `LC_ERA_START = 2022-04-04`): **use for PEM-pacing analyses**
  (Wiggers H1, H3, H5, B4, D5). The baseline reflects the user's
  LC-era normal, so today's rank measures load relative to current
  capacity. Avoids the all-era variant's mis-ranking of early-LC days
  whose lagged window still reaches into pre-LC healthy days.
- **`_lagged`** (all-era baseline, no date restriction): use for
  trajectory characterisation, cross-era comparison, and "how have I
  changed from pre-LC capacity" questions.

Default v3.2 columns for new analyses:
`exertion_class_lagged[_lcera]`, `exertion_rank_composite_lagged[_lcera]`,
4 per-axis ranks `_lagged[_lcera]`, 4 per-axis classes `_lagged[_lcera]`,
`push_burden_7d_lagged[_lcera]`, plus `effective_exertion_slope_28d`
(shared, no LC-era variant — see DATA_DICTIONARY.md §6).

The v3.1 columns (`exertion_class`, `step_z_30d`, etc.) stay in the
master only for reproducibility of existing HA01b / HA02c results;
they are not the default surface for new work. See § Per-column
provenance map and the v3.2 sub-section in
[`severity_spec.md`](../analyses/garmin_exploration/activity-labels/spec/severity_spec.md).
The LC-era boundary `lc_phase` column is in §0 of the dictionary —
gate on `lc_phase == "lc"` to scope to LC-era days; on
`lc_phase == "pre_corona"` for healthy-baseline characterisation;
exclude `lc_phase == "corona_infection"` from both. Per-phase
distributions of Garmin + subjective signals are documented in
[`lc_phase_descriptive.md`](lc_phase_descriptive.md) (regenerate from
`c:/tmp/lc_phase_descriptive.py` after any master rebuild).

This document serves three purposes:

1. **Navigation**: for every Garmin-derived column in
   [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md), point to the
   primary definition / spec / extraction code so a fresh researcher
   can trace it without searching.
2. **Known issues**: catalogue methodological caveats per indicator
   (e.g. push_burden's rolling-baseline contamination) so they're
   surfaced before the column is used in an analysis.
3. **Inventory**: list Garmin signals that are *available* in the
   GDPR dump but not currently in `per_day_master.csv` — these are
   the forward-looking expansion candidates.

This is a navigation doc, not a re-derivation. Every indicator already
has its own documentation at the point of production; the audit
catalogs where to look.

---

## Audit principle

> Each Garmin-derived column in `per_day_master.csv` must trace back
> to a documented derivation. If the chain raw → script → output is
> not findable from this document, the column doesn't belong in the
> master.

Failure modes the audit prevents:

- Filters or transforms applied "because it's what the prior code did"
  without checking whether the upstream data needs them
  (e.g. the 30-130 bpm RHR sanity filter that proved a no-op).
- Indicators with known methodological issues used in analyses
  without flagging them
  (e.g. `push_burden_7d` rolling-baseline contamination).
- Inventory blind spots: signals available in the GDPR dump that
  could enrich analyses but aren't currently extracted.

---

## Per-column provenance map

For each column in `per_day_master.csv` sourced from Garmin, the table
points to the primary documentation. Click through for the algorithm /
spec / locked decisions.

### From `daily_uds.csv` (Garmin's UDS pre-computed aggregates)

| master column | upstream column | derivation home | known issues |
|---|---|---|---|
| `total_steps` | `total_steps` | passthrough from Garmin UDS JSON via [`garmin/activity-labels/scripts/01_extract_daily_uds.py`](../garmin/activity-labels/scripts/01_extract_daily_uds.py); column definition in [`garmin/activity-labels/definition.md`](../garmin/activity-labels/definition.md) §3.2 | — |
| `moderate_min` | `moderate_min` | passthrough; passive UDS intensity-minutes (not activity-recorded — catches unlogged exertion) | UDS algorithm undocumented by Garmin; sensitivity to wear-pattern unknown |
| `vigorous_min` | `vigorous_min` | passthrough | same |
| `total_calories` | `active_kcal` | passthrough (active calories only, not BMR) | the column-name mismatch (master uses `total_calories`, source uses `active_kcal`) is intentional but slightly misleading — see DATA_DICTIONARY note |
| `resting_hr` | `resting_hr` | passthrough; Garmin's algorithmic RHR computed from sleep periods + day-low windows | **the 30-130 bpm sanity filter previously applied is a no-op for this user** (data range observed: 47-65 bpm, 0 outliers in 1731 days). Filter removed 2026-06-11. The RHR depends on sleep-data quality; days with poor sleep coverage may give jittery values; downstream analyses should consider robust rolling means rather than single-day values for trajectory work. |
| `min_hr` | `min_hr` | passthrough | depends on wear pattern (off-wrist gaps can artificially raise min). Observed range 31-72 bpm; 5 days at or below 40 bpm (0.29% of 1733 obs), 43 days at or below 45 bpm. The sub-40 days are 2022-01-13, 2022-01-17, 2022-02-28, 2024-09-30, 2024-11-29 — co-occurring with the `Training-periode (hardlopen + fietsen)` event_label (first three) and the `Citalopram-traject (umbrella)` event_label (last two). No sanity filter applied. For trajectory work prefer rolling minima over single-day values. (Audit added 2026-06-12 per Layer 1 review.) |
| `max_hr` | `max_hr` | passthrough | depends on whether activity was recorded (activities push max_hr; passive days are lower) |
| `max_avg_hr_uds` | `max_avg_hr` | passthrough; "max-of-averages" UDS metric (NOT a daily mean) | misleading without context — the column name in the master makes the UDS provenance explicit; downstream analyses should NOT treat as daily mean HR |

### From `activity_features_daily.csv` (custom feature engineering)

| master column | upstream column | derivation home | known issues |
|---|---|---|---|
| `exertion_class` | `exertion_class` | 4-axis percentile-rank composite; locked v3.1 spec at [`garmin/activity-labels/spec/severity_spec.md`](../garmin/activity-labels/spec/severity_spec.md); script [`garmin/activity-labels/scripts/04_classify_exertion.py`](../garmin/activity-labels/scripts/04_classify_exertion.py) | sensitive to rolling-baseline contamination during sustained pushes (the 30d rolling baseline includes the pushes themselves); v3.2 lagged variant in the same spec exists but the master uses v3.1 |
| ~~`push_burden_7d`~~ DROPPED 2026-06-11 | (upstream `push_burden_7d`) | spec at [`garmin/activity-labels/spec/severity_spec.md`](../garmin/activity-labels/spec/severity_spec.md) | **Held back from the master.** Known methodological issue (rolling-baseline contamination — the 30d baseline includes the pushes themselves; sustained creep rebases into its own reference). A v3.2 lagged-baseline variant `push_burden_7d_lagged` exists upstream (script [`11_compute_lagged_baseline.py`](../garmin/activity-labels/scripts/11_compute_lagged_baseline.py)) and is the documented fix. Neither is currently in the master: same discipline as `stabilisation_period` — we don't surface a known-broken metric, nor pre-commit to its replacement before descriptive analysis motivates the choice. When descriptive work surfaces the need, the lagged variant can be added cleanly. |
| `effective_exertion_min` | `effective_exertion_min` | max(recorded-activity total, passive UDS vigorous + 0.5×moderate); definition in `garmin/activity-labels/definition.md` §3.3 | weighted-passive convention captures unlogged exertion but the 0.5× weight on moderate is a designed convention, not a derived constant. **2022Q3 coverage gap resolved (re-extract 2026-06-12)**: now 100% fill from 2021Q3 onwards (extended `ANALYSIS_START` from 2022-09-03 to 2021-08-16 in `03_compute_daily_features.py` line 26). Pre-LC baseline now accessible. |
| `step_z_30d` | `step_z_30d` | z-score of daily steps vs 30d rolling median + MAD; spec in definition.md §3.3 | inherits the same rolling-baseline issue as push_burden in extreme push periods (less severe for steps than for class because steps are more granular). **2022Q3 coverage gap resolved (re-extract 2026-06-12)**: now 100% fill from 2021Q4 onwards (after 20-day warmup window). v3.1 rolling-baseline values for **2022-09-23 → 2022-10-22 shifted** because the baseline now includes pre-LC training-period days — strict HA01b/HA02c bit-identical reproducibility breaks for those 30 days only; qualitative results expected stable. |

### From `sleep_stress_nightly.csv` (custom-extracted from FIT)

| master column | upstream column | derivation home | known issues |
|---|---|---|---|
| `sleep_start_gmt` | `sleep_start_gmt` | from `sleepData.json` sleep window | — |
| `sleep_end_gmt` | `sleep_end_gmt` | from `sleepData.json` | — |
| `stress_mean_sleep` | `stress_mean` | mean of monitoring_b stress samples within sleep window; script [`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`](../garmin/scripts/sleep_stress_extract/extract_sleep_stress.py); MIN_SAMPLES_PER_NIGHT=120 (~6h at 3-min cadence) | nights with <120 samples → `sleep_valid_flag=False` → `stress_mean_sleep=NaN`. Watch-off nights silently drop. |
| `stress_stdev_sleep` | `stress_stdev` | stdev of same samples | same caveat |
| `sleep_valid_flag` | `valid` | True iff n_samples ≥ 120 | the threshold is conservative; lower-quality nights may still carry signal but the script discards them |

### From `daily_max_spike.csv` (custom-extracted from FIT)

| master column | upstream column | derivation home | known issues |
|---|---|---|---|
| `max_spike_minutes` | `max_spike_minutes` | longest contiguous run of stress ≥ 75 lasting ≥ 5 min, with ≤ 3-min gaps allowed; script [`garmin/hypotheses/H02b-stress-spikes/extract_daily_max_spike.py`](../garmin/hypotheses/H02b-stress-spikes/extract_daily_max_spike.py) | days with < 60 samples are flagged invalid; the 75 threshold + 5-min duration is locked but other variants exist (`daily_max_spike_v2.csv` for the uncensored version in `H02d-stress-spikes-uncensored/`) |

### From `labels_crash_v2.csv` (derived from gevoelscore)

| master column | upstream column | derivation home | known issues |
|---|---|---|---|
| `is_crash` | `label == "crash"` | tier-1 classification: score ≤ 3 for ≥2 consecutive days, 3-day merge rule; locked spec at [`garmin/hypotheses/crash_v2-definition/definition.md`](../garmin/hypotheses/crash_v2-definition/definition.md) | identical to crash_v1; tied to the pre-registered train/validate era split (boundary 2023-12-31) |
| `is_dip` | `label == "dip"` | tier-2: single isolated day with score ≤ 3, both neighbors ≥ 4 | distinct from `is_sub_threshold_dip` which is user-confirmed via Q2 review — these are research-derived |
| `crash_episode_id` | `episode_id` | groups multi-day crashes | empty when not in an episode |

---

## Documents-of-record (read these before using a column)

For deeper detail than the table above, the canonical source-of-truth
documents (in repo) are:

1. **`garmin/README.md`** — Garmin dump landscape (21k FIT files; file-type
   taxonomy; open questions like FIT mesg_num 233).
2. **`garmin/activity-labels/definition.md`** — feature definitions for
   daily_uds, activities, and activity_features_daily.
3. **`garmin/activity-labels/spec/severity_spec.md`** — exertion_class
   v3.1 (locked) + v3.2 lagged-baseline extension.
4. **`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`**
   (header) — sleep-stress extraction algorithm, sample-count gates.
5. **`garmin/hypotheses/H02b-stress-spikes/extract_daily_max_spike.py`**
   (header) — spike definition (threshold 75, ≥ 5 min, ≤ 3-min gap).
6. **`garmin/hypotheses/crash_v2-definition/definition.md`** — locked
   crash + dip classification, 2026-06-06.
7. **`garmin/hypotheses/registry.md`** — index of all H##/HA##/K##/S##
   hypothesis cards + train/validate era split.
8. **`garmin/methodology/testing-playbook.md`** — testing discipline
   (pre-registration, held-out validation).

These documents are the source-of-truth for their respective
indicators. **This audit document never duplicates their content** —
it points to them. When they change, this audit's tables remain valid
because they point to the moving target by file path.

---

## Inventory: available-but-not-extracted (forward-looking)

Signals present in the Garmin GDPR dump but NOT currently surfaced in
`per_day_master.csv`. Adding any of these requires a new extraction
script and a corresponding DATA_DICTIONARY entry. Listed here so a
future researcher knows what's possible.

### In `daily_uds.csv`, available but unused

- `total_distance_m` — daily distance (steps × stride). Largely
  redundant with `total_steps` for this user (no significant cycling
  outside recorded activities).

*(Propagated to master in Wave 2 2026-06-12: `daily_step_goal`,
`highly_active_sec`, `active_sec`, `is_vigorous_day`. See
[`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) §4.)*

### In `activity_features_daily.csv`, available but unused

The full feature table has **~40 columns** beyond what the master
surfaces. Remaining unused groups (after Wave 2 propagation):

- **Per-activity richness**: `max_aerobicTE`, `max_anaerobicTE`,
  `total_distance_km`, `avg_workoutRpe`, `avg_workoutFeel`. Per-activity
  resolution; if needed build a separate per-activity table rather than
  collapsing to per-day.
- **Raw rank columns (v3.1)**: `step_rank_30d`,
  `effective_exertion_rank_30d`, `max_hr_rank_30d`,
  `vigorous_min_rank_30d`. The v3.2 lagged ranks are now in the master
  and are the default; raw v3.1 ranks remain unused unless an
  HA01b-style reproduction explicitly requires them.

*(Propagated to master in Wave 2 2026-06-12: all 4 per-axis classes
v3.1 + all 4 per-axis classes v3.2 lagged + `above_baseline_streak`.
Lagged ranks composite + push_burden + slope landed in the v3.2
commit 02018e0. See [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) §6.)*

### HRV — hardware blocked (Forerunner 245 / Elevate V3)

Nightly HRV Status is a feature of the Elevate V4 sensor (Forerunner
265, 955, 965, fēnix 7, Epix 2, Venu 2+). The Forerunner 245 used
across the entire 2021-08-16 → today dump carries the older Elevate
V3 sensor and **does not produce nightly HRV at all** —  not
extracted, not raw, not derivable from any other Garmin field.

Confirmation:
- Pre-flight inventory script
  (`$DATA/scratch/preflight_hrv_inventory.py`, throwaway diagnostic,
  not committed) opened 3 sleep type-49 FIT files spanning 2021-08-16
  → 2026-06-03; zero field-name hits on `hrv`, `rmssd`, `rr_interval`,
  `stress_hrv`. The data-bearing messages are `unknown_273` /
  `unknown_274` / `unknown_276` — undocumented by Garmin; community
  has not decoded them (per Garmin Forums threads "Sleep and
  monitoring files: unknown messages" and "List of Undocumented
  mesg_num", checked 2026-06-12).
- The fr245's HRV record-setting (`Settings → Physiological Metrics
  → Log HRV`) only captures **per-activity** beat-to-beat RR
  intervals — and only when an external HR chest strap is paired
  (wrist OHR is not clean enough). Not nightly. Not aggregated to
  per-day. Not the signal Wiggers B1-B5 / H1-H5 reference.

Wiggers consequence: **B1-B5 and the HRV-dependent parts of H1, H2,
H3, H4, H5 are hardware-blocked on this dataset.** Only a device
upgrade would unblock forward, and only for new data from the upgrade
date onward.

The 8 partially-decoded fields visible in the unknown messages
(`unknown_0` ... `unknown_253`) are presumably sleep-stage timing data
that Garmin Connect uses internally to render the sleep timeline.
Reverse-engineering them is not a productive use of effort: even if
fully decoded, they would not yield HRV (the sensor doesn't produce
it).

### NOT extracted from raw FIT (latent in dump, but not currently surfaced)

- **Per-activity HRV (RR intervals)**: only present if the user wore
  a chest strap and enabled `Log HRV` on the watch. Worth a one-off
  check whether the activity FIT files have an `hrv` message before
  declaring it absent.
- **Garmin sleep score** (single 0-100 number): not in `sleepData.json`
  on this device; possibly computed cloud-side only. Wiggers F3 remains
  blocked until verified absent in FIT layer too.
- **Body Battery per-minute curve**: the 7 stat points from UDS
  cover daily extremes + sleep-start/end; the per-minute curve in
  monitoring_b would enable shape-of-day BB-slope analyses. Wave 4
  candidate, not built.

*(Extracted to master in Wave 4 2026-06-12 from `monitoring_b` FIT
files: 8 columns operationalising Wiggers A4 (sustained HR elevation)
and C4 (stress decay after peak). Source: `pipeline/01_extract/
garmin_intraday_hr_stress.py` using `Monitoring16Resolver` for
`timestamp_16` rollover. Per-minute intraday stress curve and HR
samples — previously listed here as latent — are now collapsed to
daily summary columns in §8B of DATA_DICTIONARY. The full per-minute
curves are intentionally NOT propagated to the master (column
explosion); the daily summaries cover the Wiggers A4/C4 questions
without it.)*

*(Extracted to master in Wave 3 2026-06-12 via JSON-side propagation —
**no FIT parsing needed**: Body Battery (8 cols), all-day stress
(5 cols), 24h / waking respiration (3 cols), 24h SpO2 (2 cols), sleep
stages (4 cols), sleep-window respiration (3 cols), sleep-window
SpO2 (2 cols) — total 27 columns. Sources:
`pipeline/01_extract/garmin_uds_extras.py` reads UDS JSON,
`pipeline/01_extract/garmin_sleep_extras.py` reads sleepData.json.
See [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) §7 + §7B.
Respiration / Body Battery / SpO2 — previously listed here as latent
— are now first-class master columns. Body Battery in particular
turned out to live in the UDS JSON as the `bodyBattery` object with
charged / drained / 7-element stat list — not in monitoring_b as the
earlier audit entry assumed.)*

When a future signal is queued for addition:

1. Pre-flight in `$DATA/scratch/` (throwaway) to confirm the field
   exists with a real name on this device.
2. Extraction script in `pipeline/01_extract/`.
3. CSV output in `$DATA/processed/garmin/`.
4. Propagation in `pipeline/03_consolidate/build_unified_dataset.py`.
5. Audit row in this document.
6. Column rows in DATA_DICTIONARY.

---

## Audit findings applied 2026-06-11

This audit identified two findings that flow back into the master
build:

1. **30-130 bpm RHR sanity filter removed.** Filter inherited from
   `build_timeline.py`; data range observed in 1731 daily_uds rows
   was 47-65 bpm with 0 outliers. Filter never fired. Removed from
   `pipeline/03_consolidate/build_unified_dataset.py` and the
   DATA_DICTIONARY's old "30-130 filter applied" note replaced with a
   pointer to this document.

2. **`push_burden_7d` dropped from the master.** The column was being
   surfaced from upstream despite the known rolling-baseline
   contamination. Removed from
   `pipeline/03_consolidate/build_unified_dataset.py`. The v3.2 lagged
   variant `push_burden_7d_lagged` is also held back: per the same
   discipline applied to `stabilisation_period`, the master does not
   carry indicators with known issues or unvalidated replacements.
   When descriptive analysis on the master motivates a push-burden
   construct, the lagged variant is the documented fix to add.

No other indicator was changed by this audit pass — all other
upstream-documented columns pass through cleanly.

---

## Cross-references

- [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) — per-column data
  dictionary; the audit table here is the provenance subset for
  Garmin-derived columns.
- [`methodology.md`](methodology.md) — broader research methodology.
- [`nightly_attribution.md`](nightly_attribution.md) — wake-up date
  convention; applies to `resting_hr` and the entire sleep-stress
  family.
- [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md) —
  presence-conditioned semantics for the note-derived columns
  (orthogonal to Garmin but shares the discipline of
  explicit-decision-before-use).
