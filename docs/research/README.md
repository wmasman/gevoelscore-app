# Long COVID PEM research — repo orientation

**Last reorg**: 2026-06-11. Browse-then-read overview that gets a fresh
researcher productive in ~5 minutes.

This folder holds the **methodology, code, and analyses** for a long
COVID PEM (post-exertional malaise) self-research project. The
**personal data lives outside the repo** — see Section 2 for how to
configure access.

---

## 1. What this research is

A single participant has tracked their state daily since 2022-09-03
(`gevoelscore` 1-10), kept a Garmin GDPR dump (FIT files + UDS JSON,
2021-08-16 → present, 98.8% coverage), accumulated calendar events and
day-notes, and during a 18-month PwC reintegration kept a daily work
log + a formal medical dossier. The corpus supports two distinct uses:

- **Quantitative / statistical**: gevoelscore + per-day intensity
  vectors + Garmin biometrics + objective work-incapacity record →
  trajectory analysis, hypothesis tests, descriptive correlations.
- **Qualitative / sensemaking**: day-notes (~686 written days),
  calendar events, episode umbrellas, medical records → story-level
  interpretation around specific dates or patterns.

The methodological principle: **descriptive analysis on the unified
corpus comes before any hypothesis test** (see
[methodology/methodology.md](methodology/methodology.md) §3a-§3b).

---

## 2. Setting up your local environment

### External data folder

All personal data lives outside the repo at the path defined by
`GEVOELSCORE_DATA_PATH`:

```
$GEVOELSCORE_DATA_PATH/
├── raw/                    original GDPR exports + PDFs + Excel
│   ├── pwc/                PwC dossier PDFs + reintegratie_willem.xlsx
│   ├── garmin/             Garmin GDPR dump (FIT files + UDS JSON)
│   └── directus_exports/   day_entries.json, annotations.yaml
├── processed/              intermediate single-source per-day CSVs
│   ├── garmin/             daily_uds, activity_features, sleep_stress, daily_max_spike
│   ├── notes/              v24 categorisation (clause-level + per-day rollup)
│   ├── crash_labels/       labels_crash_v2 + sub_threshold_dips
│   ├── manual_triage/      per_day_intensity + triage_events
│   └── pwc/                reintegration_hours + dossier events
├── unified/                THE goal artefact
│   └── per_day_master.csv  one row per calendar date, ~88 columns
├── reviews/                triage / review CSVs containing raw text
└── analyses/               hypothesis result data (CSVs/JSONs/PNGs)
```

Configure your access:

```bash
cp .env.example .env
# Edit .env to point GEVOELSCORE_DATA_PATH at your local copy
```

All `pipeline/` scripts read this env var. The folder is gitignored;
the repo cannot reach it directly.

---

## 3. Folder map (in this repo)

```
docs/research/
├── README.md               (this file)
├── DATA_DICTIONARY.md      column-by-column schema for per_day_master.csv
├── RESEARCH-REPORT*.md     phase reports (H01-H05, crash_v2 addendum, etc.)
├── QUEUED-WORK.md          deferred research items + audit log
├── wiggers_*.md            independent-advisor exchanges
├── _archive/               superseded top-level synthesis snapshots (e.g. STOCKTAKE.md, archived 2026-06-13)
├── literature/ (top-level .md files — see §5)
│
├── methodology/            binding rules for analysts
│   ├── methodology.md      research methodology (load scale, triage rules,
│   │                       work-vs-state lens, presence-conditioned framing)
│   ├── queued_work.md      Q1 (HA-pre-reg), Q2 (hidden-dip), Q3 (umbrella),
│   │                       Q5 (cross-validation lens)
│   ├── nightly_attribution.md     wake-up date convention
│   ├── symptom_mention_asymmetry.md  v24 = presence-conditioned positive
│   │                                  evidence (not prevalence panel)
│   ├── garmin_indicators_audit.md  Garmin per-column provenance + issues
│   ├── symptom_categorization_v24.md  the v2.x category dictionary
│   └── symptom_categorization_quality_review.md  inter-coder review process
│
├── pipeline/               all transformation code
│   ├── 01_extract/         raw external → processed external
│   ├── 02_label/           manual triage + categorisation (build_per_day_intensity,
│   │                        categorize_v2, apply_v23/v24, dispatch_actions, etc.)
│   ├── 03_consolidate/     multi-source per-day join
│   │   ├── build_unified_dataset.py  PRIMARY: produces per_day_master.csv
│   │   ├── merge_calendar_triage.py / merge_notes_triage.py
│   │   ├── cross_validate_with_intensity.py
│   │   ├── find_umbrella_candidates.py / audit_annotations.py
│   │   └── analyze_event_crash_correlation.py
│   ├── 04_visualize/       build_timeline.py (multi-row PNG)
│   └── _archive/           v1 superseded scripts
│
├── analyses/               past + ongoing analyses
│   ├── hypotheses/         H01-H05, HA01-HA11, K01-K02, S01-S02, crash_v2-definition
│   │                       Each folder: hypothesis.md + scripts; result data is
│   │                       in $GEVOELSCORE_DATA_PATH/analyses/hypotheses/
│   ├── garmin_exploration/  FIT taxonomy + scripts + activity-labels spec
│   ├── notes_categorization/  categories-analysis v1 + v2
│   ├── reviews/            review instructions (PwC dossier, reintegration gaps)
│   └── _archive/
│
└── notes/02-categorize-clauses/  gitignored v2 dictionary + verification + prompts
```

---

## 4. How to reproduce the unified dataset

```bash
# 1. Verify env
cat .env  # GEVOELSCORE_DATA_PATH should point to your data folder

# 2. Run the consolidate stage
python docs/research/pipeline/03_consolidate/build_unified_dataset.py

# Output: $GEVOELSCORE_DATA_PATH/unified/per_day_master.csv
# Expected: 1755 rows × 88 columns (as of 2026-06-11)
```

If the script complains about missing source CSVs, your
`$GEVOELSCORE_DATA_PATH/processed/` is incomplete — extract them by
running the upstream scripts in `pipeline/01_extract/` and
`pipeline/02_label/`, or restore from your data folder backup.

---

## 5. Top-level literature reviews

The four `.md` files at this folder's root are **third-party academic
reviews** kept in the repo as reading-material context. They are not
personal data:

- `literature study on pem.md` — peer-reviewed PEM-types review
- `pacing and gaded therapy literature.md` — practitioner pacing
- `push crash research.md` — threshold-dynamics review
- `pacing-and-crash-mitigation.md` — older pacing + mitigation review
- `pais-pem-literature-review.md`
- `ui-ux-patterns-from-visible-welltory.md`
- `import-feature-sketch.md`

These should likely move to a `literature/` subfolder for tidiness
(Phase E follow-up).

---

## 6. Privacy boundary

The repo is intended to be **publishable to a public Git remote**.
Hard rule:

> No personal data leaks via the repo. Personal data = raw notes text,
> free-text triage with names, PwC PDFs, the day_entries export, the
> unified master dataset (it inherits raw text), any processed file
> with raw clause text or person names.
>
> Permitted: code, regex patterns, dictionary phrases, methodology,
> aggregate counts, abstract labels, README files, data dictionaries.

Enforcement:

- All data files live at `$GEVOELSCORE_DATA_PATH/` — outside the repo.
- `.gitignore` excludes `*.csv`, `*.json`, `*.yaml`, `*.png`, `*.txt`,
  `*.xlsx`, `*.pdf`, `*.fit` under `docs/research/`.
- `.env` is gitignored; `.env.example` is committed.

When in doubt about whether something is safe to commit, the
methodology test is: does the file contain raw user-written text,
person names, or medical-document content? If yes → external.

---

## 7. Key cross-references

- [CONVENTIONS.md](CONVENTIONS.md) — how we work on research in this
  folder: role split (producer vs reviewer), discipline gates,
  pre-flight audit hooks, project-wide anchors. Read this before
  proposing an analysis or hypothesis test.
- [reviews/README.md](reviews/README.md) — the 4-layer peer-review
  checklist for HA results and synthesis docs, anchored in SCRIBE
  2016, CENT 2015, STROBE 2007, Daza 2018, WWC 2022 SCED, and the
  Natesan Batley 2023 systematic review. Building our own review
  standards (adapted for observational n=1 time-series, where no
  existing checklist cleanly maps) is itself part of the project's
  research-discipline methodology.
- [literature/methodology/](literature/methodology/) — local PDFs
  and index of the methodology standards the review checklist
  inherits from.
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — every column in
  per_day_master.csv with source + dtype + missingness + variable
  class (daily_computed vs presence_conditioned_positive_evidence)
- [methodology/methodology.md](methodology/methodology.md) — research
  methodology (sources, load scale, triage rules, interpretive lenses)
- [methodology/symptom_mention_asymmetry.md](methodology/symptom_mention_asymmetry.md)
  — the binding rule for note-derived columns (do NOT use rate of
  mention as prevalence)
- [methodology/nightly_attribution.md](methodology/nightly_attribution.md)
  — the binding rule for sleep + RHR dating
- [methodology/garmin_indicators_audit.md](methodology/garmin_indicators_audit.md)
  — per-column Garmin provenance + known issues
- [methodology/queued_work.md](methodology/queued_work.md) — what's
  next + what was decided
- [REJECTED.md](REJECTED.md) — project-scope audit trail of
  rejected / blocked / superseded hypotheses; one row per rejection
  added at the time of rejection

---

## 8. Working with this corpus

The research-discipline principle ([feedback_descriptive_before_inference](
../../README.md) memory): **no hypothesis testing before all labeling,
descriptive analysis, and multi-source consolidation are done.** As of
2026-06-11 the labeling layer is complete (v2.4 categorisation, four
years of per-day intensity triage), the unified master is built, and
the next phase is descriptive analysis on the per_day_master spine.

The unified master is the foundation — every analysis should start
from it rather than from individual processed CSVs. If a column you
need is not in the dictionary, treat it as a signal that either (a) it
needs to be added (with a documented derivation) or (b) the analysis
question should be reframed around what is in the schema.
