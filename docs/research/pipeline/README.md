# pipeline/ — all transformation code

The pipeline is split by stage so a reader can trace raw → processed →
consolidated → visualized without searching across folders.

```
01_extract/    raw external → processed external
02_label/      manual triage + categorisation + derived labels
03_consolidate/  multi-source per-day join (the master)
04_visualize/  rendering + plots
_archive/      superseded scripts
```

Every script resolves data paths against `$GEVOELSCORE_DATA_PATH` (see
the root [README.md](../README.md) §2).

---

## Stage flow

```
$DATA/raw/ + Garmin GDPR dump
    ↓
[01_extract/] Garmin extractors (UDS, sleep stress, max spike),
             PwC parser, Directus exporters, notes-candidate extractor
    ↓
$DATA/processed/{garmin,notes,pwc,...}/
    ↓
[02_label/] categorize_v2 + apply_v23/v24 patches → v24 categorisation
             build_per_day_intensity + merge → per_day_intensity
             classify_triage_notes + process_triage_actions → triage events
             dispatch_dossier_actions + dispatch_gap_actions → dispatched
             prepare_*_review.py → review CSVs for user triage
             crash_v2 + sub_threshold_dips
    ↓
$DATA/processed/manual_triage/ + crash_labels/
    ↓
[03_consolidate/] merge_calendar_triage + merge_notes_triage →
                  annotations.yaml
                  cross_validate_with_intensity → reintegration_gaps
                  find_umbrella_candidates → umbrella_candidates
                  audit_annotations → audit report
                  build_unified_dataset → per_day_master.csv (THE goal)
    ↓
$DATA/unified/per_day_master.csv
    ↓
[04_visualize/] build_timeline → timeline.png
```

---

## Critical script: `03_consolidate/build_unified_dataset.py`

The single canonical script that produces the master dataset. It:

1. Reads every per-source CSV at `$DATA/processed/*/`.
2. Reads `annotations.yaml` and `day_entries.json` at `$DATA/raw/directus_exports/`.
3. LEFT-JOINs them on `date` over the full calendar range
   (2021-08-16 → last gevoelscore date).
4. Applies the wake-up-date convention for sleep columns
   (see [methodology/nightly_attribution.md](../methodology/nightly_attribution.md)).
5. Writes `$DATA/unified/per_day_master.csv` + the columnar copy.
6. Idempotent: rerunning produces a byte-identical file given identical
   inputs.

Spec: [DATA_DICTIONARY.md](../DATA_DICTIONARY.md).

---

## When you add a new source

1. New extractor script in `01_extract/`.
2. New processed CSV at `$DATA/processed/<source>/`.
3. New row in [DATA_DICTIONARY.md](../DATA_DICTIONARY.md) (column class,
   source, units, missingness).
4. New methodology entry if there's a derivation rule (e.g.
   nightly-attribution-style).
5. Update `03_consolidate/build_unified_dataset.py` to LEFT-JOIN the
   new column.
6. Re-run + spot-check 5 dates.

For Garmin signals specifically, the audit doc
[methodology/garmin_indicators_audit.md](../methodology/garmin_indicators_audit.md)
contains an "available-but-not-extracted" inventory of latent FIT
signals (HRV, Body Battery, SpO2, respiration, per-minute stress)
worth considering.
