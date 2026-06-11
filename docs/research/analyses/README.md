# analyses/ — past + ongoing analyses

Each subfolder holds the **code + methodology MDs** for an analysis
thread. The **result data** (CSVs, JSONs, PNGs that contain personal
info) lives at `$GEVOELSCORE_DATA_PATH/analyses/`, not in the repo.

```
hypotheses/         pre-registered hypothesis cards (H01-HA11, K, S series)
garmin_exploration/  FIT taxonomy, activity-labels spec, methodology
notes_categorization/  categories-analysis v1 + v2 narratives
reviews/             review-workflow instruction docs
_archive/            superseded analyses
```

---

## hypotheses/ — pre-registered hypothesis cards

Each `H##` / `HA##` / `K##` / `S##` / `crash_v2-definition` folder has
the same shape:

- `hypothesis.md` — pre-registration: question, predicted outcome,
  test design, discrimination threshold
- `scripts/` (sometimes) — the test code
- `result-*.md` — verdict summary

The result data files live externally at
`$GEVOELSCORE_DATA_PATH/analyses/hypotheses/<same-folder-name>/`.

Master index: [garmin_exploration/registry.md](garmin_exploration/registry.md).
Cross-cutting verdicts: [garmin_exploration/synthesis.md](garmin_exploration/synthesis.md).

Train/validate era split:
- `train`: 2022-09-03 → 2023-12-31 (14 crash episodes)
- `validate`: 2024-01-01 → today (15 crash episodes)

This boundary was pre-registered before the validate-era data came
in, so it generalises honestly. See
[../methodology/methodology.md](../methodology/methodology.md) for
the broader methodological context.

---

## garmin_exploration/

Garmin GDPR dump landscape, FIT file taxonomy (21k files), per-message
inventory, activity-labels feature definitions, exertion classification
spec (v3.1 locked).

Key docs:

- `README.md` — Garmin dump landscape, file-type counts
- `activity-labels/definition.md` — daily_uds + activities + activity_features
- `activity-labels/spec/severity_spec.md` — exertion_class v3.1 + v3.2 lagged
- `methodology/testing-playbook.md` — pre-registration + held-out validation

These are the source-of-truth docs that
[../methodology/garmin_indicators_audit.md](../methodology/garmin_indicators_audit.md)
points to.

---

## notes_categorization/

Narrative analyses of the v1 → v2 categorisation chain. The locked
dictionary lives in [../methodology/symptom_categorization_v24.md](../methodology/symptom_categorization_v24.md);
this folder is for **analytic write-ups** about category distributions
and findings.

---

## reviews/

Instruction documents for human-in-the-loop review workflows:

- PwC dossier triage
- Reintegration gaps review
- PwC reintegration reconstruction narrative

The associated CSVs (filled review files) live at
`$GEVOELSCORE_DATA_PATH/reviews/`, not in the repo.

---

## When you start a new analysis

1. New subfolder here with `README.md` and (if applicable)
   `hypothesis.md`.
2. Code lives in the subfolder.
3. Result data goes to `$GEVOELSCORE_DATA_PATH/analyses/<folder>/`.
4. Verdict summary back to the subfolder as a `.md`.
5. Cross-reference from the root [README.md](../README.md) §7 if it's
   load-bearing.
