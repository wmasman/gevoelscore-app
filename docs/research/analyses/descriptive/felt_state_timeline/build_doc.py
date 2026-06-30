import json, sys
from datetime import date

OUT = r"C:\Users\GEBRUI~1\AppData\Local\Temp\claude\c--Users-Gebruiker-Documents-gevoelscore-app\6101e860-148b-48cb-b547-c289a83205b0\scratchpad"
TARGET = r"C:\Users\Gebruiker\Documents\gevoelscore-app\docs\research\analyses\descriptive\felt_state_timeline\findings.md"

a = json.load(open(OUT + r"\agg.json"))
felt, crashes, dips = a["felt"], a["crashes"], a["dips"]

def phase(m):
    y, mo = int(m[:4]), int(m[5:7]); d = date(y, mo, 1)
    if d < date(2022, 9, 22): return "3 lc_pre_ergo"
    if d < date(2022, 11, 17): return "4a learning"
    if d < date(2024, 4, 9): return "4b habit"
    return "5 citalopram"

felt_rows = "\n".join(
    "| {} | {:.1f} | {:.1f} | {:.1f} | {} | {} |".format(
        f["month"], f["median"], f["p25"], f["p75"], f["n"], phase(f["month"]))
    for f in felt)
crash_rows = "\n".join(
    "| {} | {} | {} |".format(c["month"], c["n_crash"], c["max_bucket"]) for c in crashes)
dip_rows = "\n".join(
    "| {} | {} | {} |".format(d["month"], d["n_dip_episode"], d["n_dip_day"])
    for d in dips if d["n_dip_episode"] or d["n_dip_day"])

DOC = r"""# Felt-state establishing timeline (R13) -- Layer-1 descriptive

**Request**: R13, the home-page felt-state establishing timeline for the Wiggers site.
**Mode**: producer-mode, Layer-1 **descriptive** only.
**Discipline**: NO causal claims, NO interpretive marks (CONVENTIONS section 4.1). Every figure below is a count or an order statistic of logged data; nothing here is a verdict, a supported/refuted mark, or a trajectory claim.
**Privacy floor**: MONTH-level. No dated raw daily score, no exact crash start date, ships in this artefact.
**As-of-date**: corpus right edge 2026-06-05 (felt-state + crash labels); 2026-06 is a 5-day partial month.

---

## 0. Data availability

| source | file | unit | span | role here |
|---|---|---|---|---|
| Felt-state (gevoelscore) | `$GEVOELSCORE_DATA_PATH/raw/directus_exports/day_entries.json` | daily score 1-10 | 2022-09-03 -> 2026-06-05 (1372 score-days) | per-month median + p25 + p75 |
| Crash + dip labels | `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv` | episode-level (crash_v2 scheme) | 2022-09-03 -> 2026-06-05 | per-month crash count + duration bucket; per-month dip count |
| Era / strata bands | `docs/research/methodology/lc_era_temporal_segmentation.md` s1 | event-anchored | 2021-08 -> present | overlay bands |
| Recovery phase axis | `docs/research/methodology/lc_recovery_phase_axis.md` s2 | 6 phases (1,2,3,4a,4b,5) | 2021-08 -> present | overlay bands (forward spine) |
| Event dates | `wiggers_research_story/site/data/corpus.json` -> `timeline` | month-coarsened already | 2021-08 -> today | overlay markers (read-only) |

**Note on the requested `day_entries.csv`**: the prompt named `$GEVOELSCORE_DATA_PATH/day_entries.csv`. That exact file does not exist. The equivalent gevoelscore daily source is the Directus export `raw/directus_exports/day_entries.json` (1372 rows, columns `id,date,score,note`), the cleaner felt-state source, spanning the identical range as the crash-label file. It was used for the felt-state aggregation. (`gevoelscore_verrijkt.csv` is an older 2026-05-26 snapshot, 1363 rows; not used.)

**crash_v2 scheme provenance** (CONVENTIONS section 3.6): name = `labels_crash_v2`, unit = **episode** (one record per `episode_id` for crashes; dip episodes formed by collapsing `dip_cluster_id` groups + counting isolated dips standalone), file = `processed/crash_labels/labels_crash_v2.csv`. Reconciled totals: **29 crash episodes** (103 crash-days), **79 dip-days = 49 dip episodes** (15 clusters + 34 standalone), 1190 normal-days. These match the request's stated 29 / 79.

---

## 1. Felt-state line -- per-month median + p25 + p75

The range band p25-p75 is **day-to-day spread, not error**. Median = central logged day in the month; p25/p75 = the inter-quartile band of that month's daily scores. Logging starts 2022-09. **Months before 2022-09 are intentionally blank** (the Garmin baseline exists from 2021-08, but felt-state does not -- do NOT backfill).

| month | median | p25 | p75 | n_day | recovery_phase (month-anchor) |
|---|---|---|---|---|---|
__FELT__

`recovery_phase` is the month-anchor (phase of the 1st of the month) per `lc_recovery_phase()` in `lc_recovery_phase_axis.md` s2.1; phase boundaries are mid-month so adjacent months may straddle a boundary. Phases 1 (`pre_illness_healthy`) and 2 (`acute_infection`) precede felt-state logging and have no felt-state row by construction.

**Lived-ceiling data fact** (descriptive, from `corpus.json` -> `scale`, confirmed by the data above): the instrument runs **1-10**, but across the full 1372-day felt-state record the **monthly p75 reaches 6 only once (2025-06)** and no monthly median exceeds 5.0. The realised range is 1-6 against a 1-10 scale. This is a property of the logged data, not a claim about why.

---

## 2. Crashes -- per-month count + duration bucket

Buckets: **short = 2-3 d**, **medium = 4-6 d**, **long = >=7 d** (on `episode_length_days`). `max_bucket` = the longest bucket present that month. Crash months are **coarsened to month** via `episode_start` -- no exact start date ships. Months absent from the table have `n_crash = 0`.

| month | n_crash | max_bucket |
|---|---|---|
__CRASH__

Episode-length bucket totals (across all 29 crash episodes): short 21, medium 4, long 4; max episode length = 14 days (the 2023-11 longest crash, also surfaced in `corpus.json` -> `timeline`).

---

## 3. Dips -- per-month transient-dip count

`n_dip_episode` = dip episodes anchored in that month (cluster -> first dip-day's month; isolated dip -> its own month). `n_dip_day` = raw dip-day count that month, for transparency. Months absent have 0 of both.

Two months (**2023-11, 2026-03**) show `n_dip_episode = 0` but `n_dip_day > 0`: those dip-days belong to a dip cluster whose anchor (first day) falls in the preceding month. Episode counting attributes them to the anchor month by design.

| month | n_dip_episode | n_dip_day |
|---|---|---|
__DIP__

**Per-year dip:crash ratio** (dip episodes : crash episodes, descriptive -- partial years flagged): 2022 = 4:5 (0.8), 2023 = 15:9 (1.7), 2024 = 15:11 (1.4), 2025 = 12:2 (6.0), 2026 = 3:2 (1.5, partial through 06-05). The ratio is a count ratio of two label classes; it carries no causal reading.

---

## 4. Era + phase bands + event dates (overlay)

### 4.1 Data-given strata (`lc_era_temporal_segmentation.md` s1)

| stratum | window | felt-state present? |
|---|---|---|
| 1 pre-corona | 2021-08-16 -> 2022-03-20 | no (Garmin only) |
| 2 acute infection | 2022-03-21 -> 2022-04-03 | no (Garmin only) |
| 3 LC, pre-gevoelscore | 2022-04-04 -> 2022-09-02 | no (Garmin only) |
| 4 LC, with gevoelscore + crash labels | 2022-09-03 -> present | **yes** |

The pre-2022-09 gap is real: keep it visible on the timeline, do not backfill.

### 4.2 Recovery-phase bands (`lc_recovery_phase_axis.md` s2 -- the forward spine)

| # | phase (kebab) | window | felt-state |
|---|---|---|---|
| 1 | `pre_illness_healthy` | 2021-08-16 -> 2022-03-20 | no |
| 2 | `acute_infection` | 2022-03-21 -> 2022-04-03 | no |
| 3 | `lc_pre_ergo` | 2022-04-04 -> 2022-09-21 | partial (last 19 days only) |
| 4a | `pacing_pre_citalopram_learning` | 2022-09-22 -> 2022-11-16 | yes |
| 4b | `pacing_habit_established` | 2022-11-17 -> 2024-04-08 | yes |
| 5 | `citalopram_modulated` | 2024-04-09 -> 2026-06-04 | yes |

(`citalopram_phase` sub-axis nests inside phase 5: buildup 2024-04-09->2024-06-19, consolidation ->2026-03-19, afbouw 2026-03-20->2026-06-05.)

### 4.3 Event markers (`corpus.json` -> `timeline`, already month-coarsened)

| date | kind | label |
|---|---|---|
| 2021-08 | baseline | Garmin first worn; pre-illness baseline begins |
| 2022-04 | onset | COVID infection; Long COVID onset |
| 2022-09 | data | Daily gevoelscore logging begins |
| 2023-11 | crash | Longest crash recorded: 14 days, lowest score 1 |
| 2024-01 | intervention | CPAP begins (sleep-apnoea dx later refuted; since stopped) |
| 2024-04 | intervention | Citalopram (SSRI) buildup begins |
| 2024-06 | intervention | Citalopram reaches 30 mg plateau |
| 2026-03 | intervention | Citalopram taper begins |
| today | now | Still tracking |

`confounds` declared in corpus.json: `medication`, `pacing_practice`.

---

## 5. Proposed export JSON shape

Parallel arrays over a single shared `month` axis (46 entries, 2022-09 -> 2026-06). Crash/dip arrays aligned to the same axis, 0-filled where absent. `lo`/`hi` are p25/p75.

```jsonc
{
  "scale": { "range": "1-10", "realised_max_monthly_p75": 6 },
  "band_label": "day-to-day spread, not error",
  "month":   ["2022-09", "2022-10", "...", "2026-06"],
  "median":  [3.5, 5.0, "...", 4.0],
  "lo":      [3.0, 4.0, "...", 4.0],
  "hi":      [4.0, 5.0, "...", 5.0],
  "n_day":   [28, 31, "...", 5],
  "n_crash": [3, 0, "...", 0],
  "crash_max_bucket": ["long", "", "...", ""],
  "n_dip":   [1, 1, "...", 0],
  "phase_bands": [
    { "phase": "lc_pre_ergo",                    "start": "2022-04", "end": "2022-09", "felt_state": "partial" },
    { "phase": "pacing_pre_citalopram_learning", "start": "2022-09", "end": "2022-11", "felt_state": "yes" },
    { "phase": "pacing_habit_established",        "start": "2022-11", "end": "2024-04", "felt_state": "yes" },
    { "phase": "citalopram_modulated",           "start": "2024-04", "end": "2026-06", "felt_state": "yes" }
  ],
  "events": [ "/* corpus.json timeline, month-coarsened, verbatim */" ]
}
```

The full 46-length numeric arrays are materialised at `scratchpad/export.json` (parallel to `agg.json`) during aggregation; the site build can regenerate them from the spec in section 6 rather than hand-copying.

---

## 6. Aggregation spec (reproducible)

| output | source | group-by | predicate | statistic |
|---|---|---|---|---|
| felt | `day_entries.json` | `date[:7]` (month) | `score is not null` | median, p25, p75 (linear-interp), count |
| crash | `labels_crash_v2.csv` | `episode_start[:7]` | one row per distinct `episode_id` where `label=='crash'` | count; max bucket of `episode_length_days` (<=3 short / 4-6 medium / >=7 long) |
| dip episode | `labels_crash_v2.csv` | anchor month = min(date) of cluster / dip date | rows where `label=='dip'`; collapse by `dip_cluster_id`, isolated dips standalone | count |
| dip day | `labels_crash_v2.csv` | `date[:7]` | rows where `label=='dip'` | count |

---

## 7. Privacy statement

- **Privacy floor = MONTH.** Confirmed: nothing dated below month granularity, and no raw daily gevoelscore value, appears in this artefact. Felt-state ships only as monthly order statistics (median, p25, p75) over n>=5 days per month (the single n=5 month is the 5-day partial 2026-06; all others n>=28).
- **Crashes** are coarsened to month via `episode_start[:7]`; **no exact crash start date** ships. The duration bucket (short/medium/long) ships, not the exact `episode_length_days` (except the 14-day longest-crash fact, already public in `corpus.json` -> `timeline`).
- **Dips** ship as monthly counts only.
- **Event dates** come from `corpus.json`, already month-coarsened at source.
- No note text, no tag content, no individual day is emitted.

---

## 8. Section-3.6 count-triple register (name / unit / file) for every count above

| count | value | name (scheme) | unit | file |
|---|---|---|---|---|
| felt-state logged days | 1372 | day_entries (Directus export) | day | `raw/directus_exports/day_entries.json` |
| months with felt-state | 46 | derived monthly rollup | month | (this artefact) |
| crash episodes | 29 | crash_v2 | episode | `processed/crash_labels/labels_crash_v2.csv` |
| crash-days | 103 | crash_v2 | day | `processed/crash_labels/labels_crash_v2.csv` |
| crash months (n_crash>0) | 20 | crash_v2 (rolled to month) | month | derived |
| dip episodes | 49 | crash_v2 (15 clusters + 34 isolated) | episode | `processed/crash_labels/labels_crash_v2.csv` |
| dip-days | 79 | crash_v2 | day | `processed/crash_labels/labels_crash_v2.csv` |
| dip clusters | 15 | crash_v2 `dip_cluster_id` | cluster | `processed/crash_labels/labels_crash_v2.csv` |
| isolated dips | 34 | crash_v2 (no cluster) | episode | `processed/crash_labels/labels_crash_v2.csv` |
| normal-days | 1190 | crash_v2 | day | `processed/crash_labels/labels_crash_v2.csv` |

---

## 9. External dependency

`corpus.json` (`wiggers_research_story/site/data/corpus.json`) is the external source for the section-4.3 event markers and the lived-ceiling scale note. It is **read-only** here; this artefact was assembled from a snapshot read on 2026-06-30. If the site timeline changes, section 4.3 + the `events` block in the export must be re-synced. The felt-state / crash / dip aggregations have **no** dependency on corpus.json -- they derive entirely from the two data-root files in section 0.
"""

DOC = DOC.replace("__FELT__", felt_rows).replace("__CRASH__", crash_rows).replace("__DIP__", dip_rows)
open(TARGET, "w", encoding="utf-8").write(DOC)
print("written:", TARGET, len(DOC), "chars")
