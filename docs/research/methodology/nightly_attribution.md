# Nightly attribution — the wake-up-date convention

**Status**: locked 2026-06-11.

This document defines **how data that crosses midnight is dated** in
the unified `per_day_master.csv`. The rule is short; the rationale
matters because cross-modal joins (sleep × score × Garmin daytime
metrics × work log) all depend on being attributed consistently.

---

## The rule

> Every metric describes the state of the user on date X. For data
> that crosses midnight (overnight sleep, nocturnal HR, sleep-onset
> stress), **`date X = the wake-up date`** (= Garmin's `calendarDate`
> field on the sleep record).

The wake-up date is the date the user opened their eyes on. A sleep
session 22:00 Aug 2 → 07:00 Aug 3 is attributed to `date = 2026-08-03`.

---

## Why this convention

Four reasons, in priority order.

### 1. Aligns with how the gevoelscore is given

The user logs `gevoelscore` on date X for date X. The night before
informed how they felt; the daytime activities of X informed how they
felt; both belong to X. Pairing the score with the night-of and the
daytime-of on the same row makes them directly comparable in joined
analyses. Splitting the night across the calendar boundary would
require every downstream analysis to compensate.

### 2. Garmin uses it natively

`sleepData.json.calendarDate` from the Garmin Connect export is
already the wake-up date. The sleep extraction script
(`pipeline/01_extract/garmin_sleep_stress.py`) reads this field as the
attribution date — no transform needed. Following Garmin's convention
prevents off-by-one errors when re-importing data.

### 3. Avoids dual-counting

A single night cannot be in two rows of `per_day_master.csv`. The
wake-up rule disambiguates definitively. The fall-asleep rule would
have the same property but would diverge from Garmin's calendarDate.

### 4. Matches the bedrijfsarts / AD-rapport convention

Doctor visits and work-incapacity assessments describe the day the
user presented. The user presents in the morning of date X. The night
that preceded the presentation informs the state observed.

---

## Documented exceptions

### Daytime naps

A nap of ≥ 30 minutes during 10:00-20:00 is not captured in the
sleep-stress channel (Garmin tags it as a separate sleep session, not
the night session). Naps surface in note categorisation as
`recovery_actie` clauses ("middagdutje", "middag geslapen") which
belong to the date of the note (= the date of the nap). No conflict
with the wake-up rule.

### Activity that crosses midnight

Rare in this corpus (the user does not regularly do late-evening
activity). When it occurs (e.g. an evening run ending 00:30), Garmin
attributes the activity to its start-time date. The pipeline follows
Garmin. This means a 23:30-00:30 run on the night of Aug 2 → Aug 3
contributes activity minutes to Aug 2 in `daily_uds.csv`, even though
the sleep that follows is attributed to Aug 3. This is correct: the
activity affected the user on Aug 2; the night that followed informs
Aug 3.

### No-sleep nights

Very rare. When the user does not sleep (or Garmin records no sleep
session), `sleep_valid_flag = False` on the wake-up date. The
sleep-derived columns (`stress_mean_sleep`, etc.) are `NaN`. The rule
still defines the attribution: the missing night is attributed to the
day it would have ended.

### Jetlag / multi-timezone nights

Not currently in the corpus. Revisit this section if a long
intercontinental trip appears in the data — the rule may need a
local-clock vs UTC clarification.

---

## Operationalisation

In `per_day_master.csv`:

- **`daily_uds.csv → resting_hr`**: Garmin already attributes this to
  the wake-up date. Pipeline merges on `date` directly.
- **`sleep_stress_nightly.csv → date`**: column already follows
  `calendarDate` (wake-up date). Pipeline merges on `date` directly.
- **`sleep_start_gmt`, `sleep_end_gmt`**: timestamps stored as-is for
  reference, but the row's `date` is the wake-up date.
- **All activity columns** (`total_steps`, `moderate_min`, etc.):
  daytime-attributed by Garmin; no rule applies. Pipeline merges on
  `date` directly.

The build script does NOT perform any date shifting. The rule's
practical effect is that **every source CSV must already be in
wake-up-date convention before it reaches the consolidate stage**.
This is true today for all four Garmin sources.

---

## What this rule does NOT change

- Notes (`day_entries.note`) are written about the day of the note —
  end-of-day reflection. The note's date is the wake-up date already
  (the user is awake when writing). No transform.
- Per-day intensity loads describe the cog/phy/emo intensity of the
  day named in the `date` column — the user assigned them
  retrospectively to that specific day. No nightly component.
- PwC work hours describe the workday — no nightly component.

---

## Cross-references

- [`methodology.md`](methodology.md) — the broader research methodology.
- [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) — every sleep-derived
  column entry links here.
- [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md) —
  sister document for note-derived columns; orthogonal concern but
  shares the discipline of explicit-decision-before-join.
