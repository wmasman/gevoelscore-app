# Garmin indicators audit — provenance + known issues + inventory

**Status**: navigation index, locked 2026-06-11; v3.2 preference clause added 2026-06-12.

## Rule for new analyses (v3.2 lagged baseline)

New analyses on `per_day_master.csv` use the **v3.2 lagged-baseline**
exertion columns (`exertion_class_lagged`, `exertion_rank_composite_lagged`,
`step_rank_lagged`, `eff_exertion_rank_lagged`, `max_hr_rank_lagged`,
`vigorous_min_rank_lagged`, `push_burden_7d_lagged`,
`effective_exertion_slope_28d`). The v3.1 columns (`exertion_class`,
`step_z_30d`, etc.) stay in the master only for reproducibility of
existing HA01b / HA02c results; they are not the default surface for
new work. See § Per-column provenance map and the v3.2 sub-section in
[`severity_spec.md`](../analyses/garmin_exploration/activity-labels/spec/severity_spec.md).

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
| `effective_exertion_min` | `effective_exertion_min` | max(recorded-activity total, passive UDS vigorous + 0.5×moderate); definition in `garmin/activity-labels/definition.md` §3.3 | weighted-passive convention captures unlogged exertion but the 0.5× weight on moderate is a designed convention, not a derived constant. **2022Q3 coverage gap (Layer 2 audit 2026-06-12)**: only 33.7% of `has_garmin_uds=True` days in 2022Q3 have this column populated, vs 100% in 2022Q4 onwards. The 30-day warmup ended ~2021-09-14 so this is a separate post-warmup gap (see `step_z_30d` note for the parallel finding and likely upstream cause). |
| `step_z_30d` | `step_z_30d` | z-score of daily steps vs 30d rolling median + MAD; spec in definition.md §3.3 | inherits the same rolling-baseline issue as push_burden in extreme push periods (less severe for steps than for class because steps are more granular). **2022Q3 coverage gap (Layer 2 audit 2026-06-12)**: only 9.6% of `has_garmin_uds=True` days in 2022Q3 have `step_z_30d` populated, vs 100% in 2022Q4 onwards. The 30-day warmup ended ~2021-09-14 so this is a separate post-warmup gap — likely an upstream `activity_features_daily.csv` extraction discontinuity around Sep-Oct 2022. Worth confirming against the extract script before relying on early-2022Q3 rolling features. |

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

### NOT extracted from raw FIT (latent in dump)

- **HRV (Heart Rate Variability)**: Garmin's nightly HRV summary lives
  in sleep type-49 files. Highly relevant for autonomic-recovery
  signals. Extraction script does not exist.
- **Body Battery**: per-minute energy reserve estimate. Lives in
  monitoring_b. Not extracted.
- **SpO2**: nightly oxygen saturation. Lives in monitoring_b. Not
  extracted.
- **Respiration rate spread**: relates to ANS reactivity. Mentioned as
  H03 candidate in STOCKTAKE but not implemented.
- **Per-minute stress curve**: we extract sleep-window aggregates +
  daily max spike, but the full intra-day stress profile is in the
  FIT files and could support shape-of-day analyses.

When any of these is queued for addition:

1. New extraction script in `pipeline/01_extract/`.
2. New CSV in `data/processed/garmin/` (or external equivalent
   per Phase C reorganisation).
3. New rows in this audit table.
4. New rows in DATA_DICTIONARY.

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
