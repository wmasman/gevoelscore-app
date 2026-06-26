# `trajectory/notes_patterns/` -- Q4.7 note-categorisation patterns

## What this analysis answers

**Q4.7 per [`descriptive/README.md`](../../README.md) section 4.7**: What's the symptom-mention asymmetry profile? When does the user write vs not? How does the categorisation distribution shift across LC eras?

**Tier 3 deferred topic 2 of 2** (Q4.8 seasonality_dow is the other; landed at `e4db6cc` 2026-06-26). **The FINAL Strand B topic before the `/research-interpret` skill pivot**.

---

## BINDING methodological discipline

[`methodology/symptom_mention_asymmetry.md`](../../../../methodology/symptom_mention_asymmetry.md) LOCKED 2026-06-11 is LOAD-BEARING for every framing decision in this analysis:

- v24 cat_* columns are **presence_conditioned_positive_evidence**. A mention is high-specificity positive evidence; **absence of mention is NOT evidence of absence** (5 distinct causes per asymmetry MD section 2; only one is 'symptom absent').
- v24 CANNOT do prevalence trajectories (mention-rate is confounded with note-writing-rate).
- v24 CAN do **stratify-by-content** + **conditional-on-note share** (the user-locked framing here).
- `has_note` IS daily_computed -- its trajectory IS clean.

---

## User-LOCKED operationalisation (per Strand B section 7c interview 2026-06-26; do NOT iterate)

1. **Scope = ALL v24 categorical columns** (per data dictionary section 9 + section 10): 5 belasting + 3 symptoom + 3 state_symptoom + 4 ancillary (medicatie, recovery_actie, triggers_extern, neutral_forward_looking_flag) + day_dominant_polarity + n_clauses + has_note (the daily_computed gating flag).
2. **Write-rate dimensions = ALL**: per-recovery-phase + per-citalopram-phase + per-DOW (Q4.8 sister) + per-month (Q4.8 sister) + has_note <-> gevoelscore correlation.
3. **Stratifications = ALL**: per-recovery-phase + per-citalopram-phase + per-event-class (crash vs dip vs normal per Q4.4) + per-Q4.3-boundary +/-30d (6 strong boundaries: rp1-rp5 + cp3).
4. **Trajectory framing = conditional-on-note share ONLY** (cleanest per the asymmetry discipline). **Absolute mention-rate trajectories are EXCLUDED**.

---

## Method (12-stage architecture; 2 analytic layers)

**Layer A -- write-rate (daily_computed; trajectory-clean per asymmetry MD section 3)**:

- **Stage 1** (data prep): load `per_day_master.csv`; restrict to 2022-09-03 -> 2026-06-04; identify recovery_phase + citalopram_phase + month + DOW per row.
- **Stage 2** (write-rate per-recovery-phase): per phase, P(has_note=True) + n_days + n_notes.
- **Stage 3** (write-rate per-citalopram-phase): same shape on 5-phase citalopram axis.
- **Stage 4** (write-rate per-DOW): 7-DOW table + chi2 2x7 + weekday-vs-weekend chi2 2x2 (**SISTER TO Q4.8 Stage 4** on Garmin channels).
- **Stage 5** (write-rate per-month): 12-month table + chi2 2x12 (**SISTER TO Q4.8 Stage 3**).
- **Stage 6** (has_note <-> gevoelscore correlation): score-bin contingency + Spearman rho on `has_score=True` shared-coverage rows. **In the same family as Q4.6 MCAR diagnostic**.

**Layer B -- within-note share (presence_conditioned; conditional-on-note ONLY per user lock 4)**:

- **Stage 7** (per-cluster within-note share, per-recovery-phase): filter `has_note=True`; per (cluster, phase) cell compute mean(cluster_count / n_clauses). Categorical state_symptoom + day_dominant_polarity + boolean neutral_forward_looking_flag get separate distributions.
- **Stage 8** (per-cluster within-note share, per-citalopram-phase): same shape, 5-phase citalopram axis.
- **Stage 9** (per-cluster within-note share, per-event-class): stratify by `is_crash` + `is_dip` + `normal` per Q4.4. **Q4.4 sister + asymmetry MD's worked example**.
- **Stage 10** (per-cluster within-note share, per-Q4.3-boundary +/-30d): for each of the 6 strong Q4.3 boundaries (rp1-rp5 + cp3), compute pre vs post share table within +/-30d window.

**Layer C -- output + emit**:

- **Stage 11** (output artefacts): 5 PNG plots.
- **Stage 12** (programmatic emit): [`findings.md`](findings.md) + this README + [`summary.json`](summary.json) (gitignored).

---

## Discipline guards

- **Layer 1 descriptive per CONVENTIONS section 2.1**: NO causal claims; NO `SUPPORTED` bar; NO `REFUTED` mark.
- **Per CONVENTIONS section 4.2 caveat-class**: Layer-B findings reported as `share-of-clauses on cluster X is Y conditional-on-note in phase Z` -- NEVER `cluster X is more prevalent in phase Z`. The 5-cause-of-absence rule is invoked at every Layer-B reading.
- **NO absolute mention-rate trajectories** (user-locked choice 4: conditional-on-note share only; absolute mention-rate is EXCLUDED per asymmetry MD section 3).
- **NO claim that absence-of-mention is absence-of-symptom** (asymmetry MD section 2: 5 causes).
- **NO HA verdict promotion** (cross-corroboration only; HA-C4b v3 section 8 queued primitive substrate ONLY, NO promotion to that primitive's MD).
- **ASCII-only stdout; no em-dashes; no emojis** per project convention.
- **f-string discipline**: no nested double-quotes inside expressions (pre-3.12 compatibility); use format() or extract-to-variable.

---

## How to run

```
# Requires GEVOELSCORE_DATA_PATH env var pointing to gevoelscore-data root
python docs/research/analyses/descriptive/trajectory/notes_patterns/run.py
```

Outputs (all but [`run.py`](run.py) + [`README.md`](README.md) + [`findings.md`](findings.md) gitignored). Computed on `per_day_master.csv` as-of-date `2026-06-04` over the 2022-09-03 -> 2026-06-04 window (Stratum 4): 1371 day-level rows; 685 has_note=True rows (50.0%).

- `summary.json` -- machine-readable per-stage statistics
- `plots/write_rate_per_phase.png` -- Layer A: recovery + citalopram phase bars
- `plots/write_rate_dow_month.png` -- Layer A: DOW + month grids
- `plots/conditional_share_heatmap.png` -- Layer B: cluster x recovery/citalopram phases
- `plots/per_event_class_table.png` -- Layer B: cluster x crash/dip/normal
- `plots/per_boundary_pre_post.png` -- Layer B: cluster x boundary delta (post - pre)

---

## Status

**LANDED 2026-06-26**. Tier 3 deferred-topic 2 of 2 closed. **Strand B 8 of 8 CLOSED**. Foundation in place for `/research-interpret` skill pivot per user's earlier sequencing.

