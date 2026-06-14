# Session B - Annotations triage (2026-06-14)

Walked the lived-experience braindump ([lived_experience_garmin_pacing_2026-06-14.md](../lived_experience_garmin_pacing_2026-06-14.md)) against `hand_curated_spans.yaml` / `annotations.yaml` per the handoff brief.

## Pre-session: handoff contradiction flagged

The handoff brief said to edit `annotations.yaml` directly. The merge pipeline (`pipeline/03_consolidate/merge_calendar_triage.py`) regenerates `annotations.yaml` from scratch on every run, reading hand-curated entries from `hand_curated_spans.yaml`. Direct edits to `annotations.yaml` will silently disappear on next regenerate.

Decision: edit `hand_curated_spans.yaml` (the persistent source). Mirror the prior session's 2026-06-14 edits that landed only in `annotations.yaml` so they survive next merge.

## §4 candidate-event triage results

| # | event | status | notes |
|---|---|---|---|
| 1 | Earlier running attempts (pre-LC) | OUT-OF-SCOPE-DATA-PIPELINE | Training-periode 2021-08-16 -> 2022-03-22 covers Garmin-tracked period. User wants pre-2021 running sessions extracted from raw Garmin activity data (with per-event stats: duration, intensity) and fed into a labeling pipeline. This is a data-pipeline task, not interview triage. Logged in §"Follow-ups" below. |
| 2 | LC-onset "sweat it out" exertion phase | DECLINED-NARRATIVE-ONLY | Inherently interpretive state-phase; no factual-shape reformulation is available. Discrete events (Ardennen, Zuna apr+jun 2022) already present individually. The braindump narrative remains the canonical record; this will never become a structured annotation. |
| 3 | PwC re-integration | ALREADY-PRESENT | `PwC reintegratie 2023 (umbrella)` 2023-03-06 -> 2023-11-28 + 8 individual visits. |
| 4 | PwC work-stop | ALREADY-PRESENT | `Werk-transitie (afbouw + afscheid)` umbrella 2024-04-01 -> 2024-07-18 + `Spullen inleveren` 2024-06-27 + `Afscheid op kantoor, Mark 60` 2024-07-18. |
| 5 | WIA aanvraag / traject | DECLINED-UMBRELLA | Discrete events present (`Voorbespreken WIA-aanvraag` 2024-01-29, `wia aanvraag doen` 2024-01-29, `gesprek verzekeringsarts UWV` 2024-05-13, `Robinius belt` 2024-07-04, `Robius wia belt` 2025). User: discrete coverage sufficient; no umbrella. |
| 6 | Stabilisation period | DECLINED-NARRATIVE-ONLY | Inherently interpretive state-phase; no factual-shape reformulation is available. The braindump narrative remains the canonical record; this will never become a structured annotation. |
| 7 | Sailing weeks (multi-day) | NOT-APPLICABLE | Many single-day sailing entries exist; user: day-level coverage is fine. |
| 8 | Efteling trips | ALREADY-PRESENT | Two entries: `naar de efteling` 2023-09-13 + Efteling-in-wheelchair ~2024-12. User: those two are all of them. |
| 9 | TVO platform pre-launch | ALREADY-PRESENT | `TVO/TVOO project` umbrella 2025-06 -> 2026-05 + `Liefde voor Leren congres en officiële lancering TvO` 2026-02-12 + ~25 individual TVO events. |
| 10 | Partner-away periods | ALREADY-PRESENT | ~10 discrete partner-away entries (Bonaire trips, Curaçao, weekends). User: coverage looks complete. |

## Edits applied (mirror, not new content)

Three edits to `hand_curated_spans.yaml` to mirror prior 2026-06-14 changes that previously only landed in `annotations.yaml`:

1. **CPAP-interventie end date refined**: `2024-02-28` -> `2024-04-17`. Note expanded with 2024-04-16 apneu-test reference and source tag.
2. **Citalopram phase-transition marker added (2024-06-20)**: "buildup -> consolidation (30mg plateau reached)". Boundary used by `intervention_effects_descriptive` script.
3. **Citalopram phase-transition marker added (2026-03-20)**: "consolidation -> scale-down (afbouw begins)". Boundary used by `intervention_effects_descriptive` script.

All three were already present in `annotations.yaml` from the prior session; this session moves them upstream into the persistent source so they survive the next `merge_calendar_triage.py` run.

No interpretive-mark entries were added. No new event content was created in this session.

## Follow-ups (for future sessions)

- ~~**Pre-2021 running data extraction**~~ — RESOLVED in this session. There is no pre-2021 Garmin data (the earliest activity in `activities.csv` is 2021-08-16, the day the Garmin was bought). What was previously framed as "earlier running attempts pre-LC" is actually the existing `Training-periode` umbrella; the umbrella was too coarse to surface each session, but the per-session data was always available. See §"Garmin per-session activity markers" below for the resolution.
- ~~**Sweat-it-out phase (§4 #2)** and **Stabilisation period (§4 #6)**~~ — RESOLVED 2026-06-14 as DECLINED-NARRATIVE-ONLY. These remain narrative content in [lived_experience_garmin_pacing_2026-06-14.md](../lived_experience_garmin_pacing_2026-06-14.md) and will not be structured into annotations.yaml. No further work needed; do not re-propose as deferrals in future triage sessions.

## Garmin per-session activity markers (added this session)

`merge_calendar_triage.py` now reads `processed/garmin/activities.csv` and emits one single-day marker per session for the activity types running, cycling, walking, breathwork. Sailing_v2 and incident_detected are skipped per user request.

**Counts**: 401 markers added (running 86, cycling 42, walking 268, breathwork 5). Date range 2021-08-16 → 2025-03-04.

**Label format**: `<Type>, <duration>min[, <distance>km][, HR avg/max <avg>/<max>]`. Example: `Running, 38min, 6.2km, HR avg/max 144/166`.

**Category mapping** (default; consistent with prior manual entries):

| activity_type | category |
|---|---|
| running | high_intensity |
| cycling | high_intensity |
| walking | levensgebeurtenis |
| breathwork | interventie |

**Note field**: `name: <garmin activity name>; source: garmin_activities_csv`. The `source: garmin_activities_csv` tag is the provenance anchor for these markers.

**Files touched**:
- `docs/research/pipeline/03_consolidate/merge_calendar_triage.py` — added `GARMIN_ACTIVITIES_CSV` path, `ACTIVITY_TYPES_TO_LABEL` map, `_opt_float()` helper, `read_garmin_activities()` function, wire-up in `main()`.
- `$GEVOELSCORE_DATA_PATH/raw/directus_exports/annotations.yaml` — regenerated. Total markers 405 (was 4: 4 hand-curated + 401 derived). Spans unchanged at 506.

**Distance unit note** (documented in the function docstring): `activities.csv` has a column named `distance_m`, but values are actually in centimetres — the Garmin Connect API returns distance in cm and `02_extract_activities.py` preserves it verbatim. The function divides by 100,000 to get km. Verified against typical pace and speed for the four activity types.

**Possible follow-ups**:
- The merge produces some near-trivial markers (e.g. `Cycling, 2min, 1.0km`) — likely Garmin sessions accidentally left running. A `min_duration_min` threshold could filter these out if they're visual noise. Not implemented this session.
- Manual `"running"`-labelled high_intensity entries in `triage_notes_classified` (e.g. 2023-07-04) now co-exist with the Garmin-derived `Running, …` markers on the same dates. The manual entries carry user-perceived load values; the Garmin markers carry objective stats. No dedup applied; they're treated as complementary.
- `workout_rpe` and `workout_feel` columns in `activities.csv` carry user-entered subjective values; not encoded into the marker label or note this session.

## Audit before push

This summary file lives in the repo and is subject to `pipeline/audit_for_publication.py` before the next git push (per `feedback_audit_before_push`). The file contains no raw user text and should pass cleanly.

**Audit status at session close**: 1 pre-existing name hit in `docs/research/wiggers_testable_hypotheses.md:453` (a Wiggers literature-citation author name) — NOT introduced by this session. Needs resolution (allowlist or initials) before the next push. The merge_calendar_triage.py edits and this summary file do not introduce any new name hits.


## Open questions / loose ends

- Should the prior session's direct-edits-to-annotations.yaml pattern be discontinued and the methodology MD (§4) updated to make `hand_curated_spans.yaml` the canonical edit target explicitly? Currently methodology §9 still references HAND_CURATED_* lists in the merge script; the file-based mechanism is documented in `hand_curated_spans.yaml`'s own header but not in methodology.md.

## Audit before push

This summary file lives in the repo and is subject to `pipeline/audit_for_publication.py` before the next git push (per `feedback_audit_before_push`). The file contains no raw user text and should pass cleanly; the audit is the gate either way.
