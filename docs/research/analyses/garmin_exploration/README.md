# Garmin GDPR dump — research notes for gevoelscore correlation

Investigation of the Garmin GDPR export at
`C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\`, with a focus on
finding **sub-daily signal** (HR / stress / respiration spikes) useful for
crash / PEM prediction. Daily averages alone are too coarse: a crash can be
triggered by a single spike of exertion (physical, cognitive, emotional)
that may not move the daily mean.

Date: started 2026-06-05.

## TL;DR — what we have

- **404 workout activities** (2021-08-16 → 2026-04-16) with per-second HR, GPS, cadence — in `summarizedActivities.json` + matching FIT files.
- **~1.733 days (98.8% coverage)** of continuous daily monitoring across 2021-08-16 → 2026-06-03 — the load-bearing dataset for spike analysis. Only meaningful gaps: 2022-07-04 → 2022-07-07 (4 days) and 2022-08-07 → 2022-08-11 (5 days), both likely vacations.
- Per-day, per-minute resolution for **HR, stress (0-100), respiration rate, SpO2 (periodic)**, plus sleep-stage transitions.
- Daily aggregates for body battery (highest/lowest/most-recent + timestamps), all-day stress buckets (low/medium/high duration), VO2max, training load, RHR.
- One undecoded per-minute signal (`unknown_233`, 1.440 records/day) that the wider FIT reverse-engineering community has not yet mapped — see Open question 1.

## File-type taxonomy (whole population: 21.219 FIT files, 0 parse errors)

All from a Garmin Forerunner 245 (serial 3377851255, registered 2021-08-16).

| type             | files | size    | content                                                              |
| ---------------- | ----: | ------: | -------------------------------------------------------------------- |
| `monitoring_b`   | 7.888 |   80 MB | Per-minute HR + stress + respiration + SpO2 across waking day        |
| `49` (sleep)     | 7.881 |   47 MB | Sleep-stage transitions + per-minute sleep-time samples (`unknown_274`) |
| `44` (metrics)   | 4.292 |  1.7 MB | Tiny metrics snapshot — VO2max / fitness-age touch-ups               |
| `41`             |   755 |  0.2 MB | Housekeeping / device telemetry                                      |
| `activity`       |   403 |   27 MB | Workouts with per-second record messages                             |

Files per day average ~12 (Connect rolls over on each watch sync). The 7.888
`monitoring_b` ↔ 7.881 `type-49` pairing is exactly 1:1 except on
edge-of-coverage days — one of each per sync session.

## What's inside one full-day `monitoring_b` file

Decoded from a January 2026 file (50 KB, 24-hour span, 1.440 minutes covered):

| message              | count | what it is                                                       |
| -------------------- | ----: | ---------------------------------------------------------------- |
| `stress_level`       | 1.429 | per-minute stress (0-100) + 3 secondary fields                   |
| `respiration_rate`   | 1.429 | per-minute breaths/min (~0.01 precision)                         |
| `monitoring`         | 1.063 | per-minute HR (bpm) + activity type/intensity/distance           |
| `unknown_233`        | 1.440 | per-minute 4-byte payload — see Open question 1                  |
| `spo2_data`          |   283 | SpO2 readings when periodic mode is on (~one every 5 min)        |
| `event`              |   292 | auto-activity-detect start/duration markers (helpful: catches "you went for a walk" without launching activity)  |
| `monitoring_hr_data` |     2 | resting HR + current-day RHR snapshot                            |
| `monitoring_info`    |     1 | RMR, distance ratios, activity-type ratios                       |

Daily cadence summary (median across 60 stratified-sample files):
- HR samples: ~132/file but up to 1.127 on full-day files
- Stress: ~215 samples/file, up to ~1.429 on full days
- Respiration: same cadence as stress
- All 60 sampled files contain HR, stress, and respiration — feature availability is uniform across the 5-year span.

## What's inside a `type-49` (sleep) file

| message       | count | what it is                                                        |
| ------------- | ----: | ----------------------------------------------------------------- |
| `unknown_274` | 1.418 | Per-minute sleep-time 20-byte payload — likely HRV / RR-interval data |
| `sleep_level` |    44 | Sleep-stage transitions (awake / light / deep / REM)              |
| `unknown_273` |     4 | Sleep window start (tcgoetz guess — fits the timestamp pattern)   |
| `unknown_276` |     1 | Sleep window end (tcgoetz guess)                                  |

The sleep-stage transitions match the per-night summaries in
`DI-Connect-Wellness/*_sleepData.json` — same calendar dates, same
deep/light/REM/awake durations.

## Daily aggregates already structured (no FIT decoding needed)

`DI_CONNECT/DI-Connect-Aggregator/UDSFile_*.json` is the rich one. Per day:

- `bodyBattery.bodyBatteryStatList` — HIGHEST / LOWEST / MOSTRECENT values **with timestamps** (so we know when in the day battery bottomed out, even without the per-minute curve)
- `bodyBattery.chargedValue` / `drainedValue` — total charge gained vs drained over the day
- `allDayStress.aggregatorList` — TOTAL day: averageStressLevel, maxStressLevel, stressIntensityCount, stressOffWristCount, stressTooActiveCount, plus durations bucketed into rest/low/medium/high
- `averageSpo2Value`, `lowestSpo2Value`, `latestSpo2Value` (+ timestamps)
- `respiration` — avg waking / highest / lowest / latest
- `restingHeartRate`, `currentDayRestingHeartRate`, `minHeartRate`, `maxHeartRate`, `minAvgHeartRate`, `maxAvgHeartRate`
- Activity totals: steps, distance, kcal (active/BMR/total), highly-active/active/moderate/vigorous seconds, intensity minutes
- Hydration totals + per-event entries (`HydrationLogFile_*.json`)

This is enough for *day-level* features. The FIT files add the *intra-day distribution*: variance, peaks, time-above-threshold, how clustered the spikes were.

## Practical feature ideas for crash correlation

Per-day features computable from this data, ranked by likely PEM-relevance:

1. **Stress-spike count / duration above threshold** — `stress_level` samples > 75 in a 60-min rolling window. Probably the strongest single intra-day signal.
2. **HR variance and peak frequency** — std-dev of per-minute HR, count of minutes > resting + 30 bpm outside of a logged activity. Catches unrecorded exertion (cleaning, social events, emotional spikes).
3. **Respiration spread** — max - min and 95th percentile of waking respiration rate; rapid breathing without activity is a strong sympathetic-arousal marker.
4. **Body-battery drain rate** — `drainedValue / waking_hours` and time-of-day of LOWEST point. Faster-than-baseline drain on a "rest" day is a candidate crash precursor.
5. **Sleep-stage fragmentation** — count of awake transitions and deep-sleep total from type-49 / sleepData.
6. **SpO2 nocturnal dips** — minutes < 92% from `lowestSpo2Value` + sleep-time SpO2 samples.
7. **Unrecorded activity bursts** — `event` messages with `auto_activity_detect_start_timestamp` outside of any logged workout.

A useful first artefact would be a daily wide table: one row per calendar date, columns = these features, joinable with the gevoelscore daily entry on `calendarDate`.

## Open questions

### 1. What is FIT `mesg_num 233`?

1.440 records per day (exactly one per minute), 4-byte payload (e.g. `(0, 36, 1, 176)`). Values are too noisy minute-to-minute to be body battery directly. Community status as of June 2026:

- Garmin's official FIT SDK does not document it.
- `tcgoetz/Fit` (one of the most thorough reverse-engineering projects) explicitly labels it `unknown_233 = 233` in `fitfile/message_type.py`.
- GoldenCheetah's FIT parser logs and skips it.
- HarryOnline's community Google Sheet of undocumented mesg_nums does not have a mapping for it.
- Multiple Garmin Connect IQ / FIT SDK forum threads ask about 233; none answered.

Hypotheses worth testing:
- **Per-minute body-battery internal state** — values would need delta-decoding to align with the HIGHEST/LOWEST/MOSTRECENT timestamps in the UDS daily file. If the third byte tracks a smooth 0-100 curve once delta-decoded, this is body battery.
- **Per-minute HRV (e.g. SDNN bytes)** — the cadence matches HRV's typical reporting interval; would correlate with `current_day_resting_heart_rate` evolution.
- **Internal stress confidence / smoothing state** — secondary fields used to compute the published `stress_level_value`.

Concrete next step: for one well-instrumented day, plot byte[0..3] across 1.440 minutes alongside the known stress / HR / respiration curves. If any byte tracks a known signal at lag-0, we have a mapping.

### 2. Where do per-minute body-battery samples actually live?

The UDS daily file only has HIGHEST / LOWEST / MOSTRECENT markers. The
Garmin Connect web UI shows a continuous body-battery curve — that data
must be either (a) computed client-side from raw HRV + stress, (b) hidden
in `unknown_233`, or (c) only retrievable via the Connect REST API
(`/wellness-service/wellness/dailyStress/{date}` and
`/wellness-service/wellness/bodyBattery/events/{date}`).

If (c) we'd need an account-authenticated Connect API client; the GDPR
dump alone won't have it. The `garmin-health-data` project (Diego
Scarabelli) is one option, but it's a live-data tool, not a dump parser.

## Scripts and outputs

Everything reproducible from this repo, no cloning needed:

| script | what it produces                                              | output                                  |
| ------ | ------------------------------------------------------------- | --------------------------------------- |
| [scripts/01_classify_fit_files.py](scripts/01_classify_fit_files.py)    | One row per FIT file with type + product + size + `time_created`. Reads zips in place — no need to extract. | [output/fit_files_classified.csv](output/fit_files_classified.csv) (21.219 rows)         |
| [scripts/02_profile_monitoring_density.py](scripts/02_profile_monitoring_density.py) | Stratified sample (60 files per type) decoded with `fitdecode`; per-file message counts, HR cadence, stress/respiration/SpO2 sample density, plus field-presence summary. | [output/monitoring_density_profile.csv](output/monitoring_density_profile.csv) + [output/monitoring_field_presence.txt](output/monitoring_field_presence.txt) |
| [scripts/03_date_coverage.py](scripts/03_date_coverage.py) | Per-day FIT file counts; gap detection.                       | [output/monitoring_coverage.csv](output/monitoring_coverage.csv) (1.754 rows, one per calendar day) |

Run all three in order from the repo root:
```powershell
python docs/research/garmin/scripts/01_classify_fit_files.py
python docs/research/garmin/scripts/02_profile_monitoring_density.py
python docs/research/garmin/scripts/03_date_coverage.py
```

Dependency: `pip install fitdecode` (0.11+; ships with FR245-compatible
profile mappings for the documented fields).

The Garmin dump itself lives **outside** the app repo at
`C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\` and is read
read-only by these scripts — no copies into the app tree.

## Not yet done

- Per-minute timeseries extractor: read every `monitoring_b` file, emit a tall CSV `(timestamp, hr, stress, respiration, spo2)` to seed feature engineering. Probably an `04_extract_timeseries.py`.
- Per-day feature table joined on `calendarDate` against `UDSFile_*.json`.
- Decode `unknown_233`: test the body-battery / HRV hypothesis.
- Look at the workout `activity` files for in-workout HR variability; PEM-relevant if a "normal" workout HR profile suddenly shows post-exertional irregularity.
- Sanity-check sleep-stage transitions against the per-night summary fields in `*_sleepData.json` to confirm we can rely on either source.

## References

Web search trail for `unknown_233` (June 2026):

- [List of Undocumented mesg_num? — Garmin FIT SDK Forum](https://forums.garmin.com/developer/fit-sdk/f/discussion/254469/list-of-undocumented-mesg_num) — `233` mentioned, no answer given.
- [Where can I find definitions for the large proportion of messages types generated by my Garmin devices?](https://forums.garmin.com/developer/fit-sdk/f/discussion/375512/where-can-i-find-definitions-for-the-large-proportion-of-messages-types-generated-by-my-garmin-devices-which-are-not-defined-in-profile-xlxs) — official answer is "many will remain undocumented."
- [HarryOnline — Beyond the SDK: Uncovering Undocumented Garmin FIT File Information](https://www.harryonline.net/blog-en/beyond-the-sdk-uncovering-undocumented-garmin-fit-file-information/14727/) — describes the community Google Sheet and FIT File Viewer; sheet does not include 233.
- [`tcgoetz/Fit` — `fitfile/message_type.py`](https://raw.githubusercontent.com/tcgoetz/Fit/master/fitfile/message_type.py) — explicit `unknown_233 = 233`; tentative `start=273`, `sleep_data=274`, `end=276` for the type-49 file companions.
- [`tcgoetz/GarminDB`](https://github.com/tcgoetz/GarminDB) — production project for FIT + Garmin Connect ingestion, useful as a comparison target.
- [`diegoscarabelli/garmin-health-data`](https://github.com/diegoscarabelli/garmin-health-data) — confirms that per-minute body battery / stress timeseries comes from the Connect REST API, not from FIT files.
- [GoldenCheetah `FitRideFile.cpp`](https://github.com/GoldenCheetah/GoldenCheetah/blob/master/src/FileIO/FitRideFile.cpp) — treats `233` as unknown.
- [`mrihtar/Garmin-FIT` — `FIT.pm`](https://github.com/mrihtar/Garmin-FIT/blob/master/Garmin/FIT.pm) — comprehensive Perl reference; lookup table only documents up to `climb_pro = 317` and does not name 233.
