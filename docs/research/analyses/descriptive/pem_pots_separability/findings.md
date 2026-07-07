# Findings - PEM vs POTS separability in the watch data (descriptive)

> **Label discipline.** "POTS" here names one of Wiggers' two management threads (the electrolyte-side she takes for the felt within-day stress U-dip), NOT a watch-detectable condition. FR245 is posture-blind, U-dip polarity runs opposite the established POTS HRV signature (vagal withdrawal), and no POTS subtype is trackable to the instrument-bar per [`../../../literature/reviews/pots_operationalisation_wearable_review.md`](../../../literature/reviews/pots_operationalisation_wearable_review.md). See [`../../../methodology/pem_pots_mechanism_framing.md §1.2`](../../../methodology/pem_pots_mechanism_framing.md).

**Descriptive Layer-1 analysis** answering the reframing questions raised
2026-07-07: is the POTS-signature watch pattern separable from the PEM-signature
pattern, when does it appear, do POTS-signature days coincide with lower felt-state,
and can the symptom notes corroborate POTS episodes. Producer-mode, for the
participant-researcher (repo owner), drafted 2026-07-07 by Claude (Opus 4.8).
Reproducible via [`run.py`](run.py).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

**Operationalisation (two descriptive watch SIGNALS, not markers/detectors of a
condition; grounded in Wiggers' own framing; not a diagnosis):**
- the **within-day U-dip signal** = elevated within-day stress **U-dip**
  (`u_dip_count` z vs personal baseline) - the pattern Wiggers manages as if
  orthostatic (electrolytes / ORS), the substrate of HA11. NB: this is Wiggers'
  as-if-orthostatic side, **not a validated POTS marker** (see caveats).
- the **overnight stress-load signal** = elevated overnight stress
  (`stress_mean_sleep` z, the HRV-proxy autonomic load; the load / PEM side), with
  `stress_stdev_sleep` as a secondary read.

Naming note: `PEM` / `POTS` refer to **Wiggers' two management threads** (pacing;
electrolytes), not to conditions the watch detects; any *management* is her lived
practice, not a claim of ours. Both signals: z vs the personal lagged [d-90, d-30]
trimmed baseline (project standard). A "signature day" = signal z >= 1.0 (stated
threshold; the separability read is the threshold-free correlation). Single-pool,
baseline-relative, aggregated. No causal marks per
[CONVENTIONS section 4.1](../../../CONVENTIONS.md); the signals are proxies, the
associations are not mechanism, and we make **no claim that either state worsens if
unmanaged or that management helps**. n_days with both markers computable
= 1090 (of 1372; the [d-90,d-30] baseline needs 40+ prior days, so the earliest
weeks and phase 3 drop out).

---

## 1. Headline

**PEM and POTS are largely distinct in this body's watch data - the two markers
share under 1% of variance and signature-days are mostly one mechanism or the
other.** They are **weakly positively correlated, not independent** (Pearson
r = +0.09, 95% CI [+0.03, +0.15], which excludes zero; Spearman p = 0.047), so the
honest word is "largely distinct," not "unrelated." And they carry felt-state
differently: the **PEM** marker tracks lower gevoelscore (real, and it survives a
crash-drop check); the **POTS** marker does not (a genuine null). The orthostatic
U-dip pattern is the "dysregulated but not necessarily feeling bad" signature
Wiggers warns about ("don't be fooled by good values"); the PEM autonomic load is
the one that coincides with feeling worse. (The "both together = lowest felt-state"
reading was **dropped on review** - it is an artefact of crashes, see section 4.)

---

## 2. Separability - are POTS-days and PEM-days the same days?

| statistic | value |
|---|---:|
| Pearson r (POTS-marker z, PEM-marker z) | **+0.092**, 95% CI **[+0.033, +0.151]** |
| shared variance (r^2) | **0.85%** |
| Spearman r (p) | +0.060 (**p = 0.047**) |
| Pearson r (POTS-marker, PEM-*variability* z) | +0.014 |
| contingency phi (POTS-day x PEM-day) | +0.050 |
| crash-drop sensitivity (r with crash days removed, section 3.4) | +0.072 (delta -0.020, CLEAN) |

Contingency of signature-days: **both 77 / POTS-only 169 / PEM-only 219 /
neither 625**. The correlation is **weak but statistically non-zero** - the 95% CI
excludes zero and Spearman p = 0.047, so the markers are **not independent**; they
are **weakly positively** related. But they share **under 1% of variance** and most
signature-days are one mechanism or the other, so they are **largely distinct** -
the empirical warrant for looking for both separately rather than collapsing them
into one "autonomic dysregulation" signal. The weak positive correlation survives
the crash-drop check (r 0.092 -> 0.072).

---

## 3. When does the POTS signal appear (per recovery phase)?

| phase | id | n_days | POTS-day rate | PEM-day rate | mean POTS z | mean PEM z |
|---|---|---:|---:|---:|---:|---:|
| `pacing_pre_citalopram_learning` | 4a | 6 | 33.3% | 16.7% | -0.13 | -0.47 |
| `pacing_habit_established` | 4b | 500 | **27.0%** | 30.0% | **+0.23** | +0.37 |
| `citalopram_modulated` | 5 | 584 | **18.7%** | 24.8% | **+0.14** | +0.04 |

The POTS (U-dip) signature is **stronger in the pre-citalopram pacing-habit era
(4b) and lower in the citalopram era (5)** - both its day-rate (27% -> 18.7%) and
its mean level fall. This is consistent with HA11 and the participant's lived report
that the POTS picture waxes and wanes as symptoms change. **Important confound (read
inline, not as a footnote):** the only two informative phase cells (4b, 5) straddle
the **2024-04-08/09 boundary, which is exactly citalopram onset** - so this "recedes
over time" read is *not* an independent time-trend; it is the retired era-split in
another guise, and it inherits the R19 discipline (descriptive phase-to-phase
variation, never a verdict). It is reported as a suggestive descriptive pattern, not
a clean temporal decline. Phase 3 (`lc_pre_ergo`) and the earliest days have no
computable baseline and drop out; phase 4a (n=6) is noise.

---

## 4. Are POTS-signature days lower in felt-state?

| group | n | mean gevoelscore | MWU vs neither | crash-days | crash-dropped mean |
|---|---:|---:|---|---:|---:|
| neither | 625 | 4.48 | - | 4.3% | 4.55 |
| **POTS-only** | 169 | **4.57** | p = 0.19 (**null**), d = +0.11 | 3.0% | 4.62 |
| **PEM-only** | 219 | **4.15** | **p < 0.0001, d = -0.40** | 13.2% | 4.39 |
| both | 77 | 4.03 | p = 0.0006, d = -0.54 | **24.7%** | **4.52** |

Two claims survive review; one does not:

- **POTS-signature days are NOT lower** - POTS-only sits at 4.57, marginally *above*
  neither (4.48), and the Mann-Whitney test is a **genuine null** (p = 0.19). The
  orthostatic pattern is "quiet dysregulation" that need not feel bad.
- **PEM-signature days ARE lower** - 4.15 vs neither 4.48, a real effect (MWU
  p < 0.0001, Cohen d = -0.40) that **survives the crash-drop check** (with crash
  days removed the gap narrows but holds, 4.39 vs 4.55). This is the robust
  felt-state finding.
- **"Both together = lowest" is DROPPED on review** - the "both" group is 24.7%
  crash-days (vs 4.3% for neither), and because `is_crash` is defined partly on low
  gevoelscore, its low mean (4.03) is largely **circular**: with crash days removed
  it rises to 4.52, essentially equal to neither. So "both mechanisms = worst felt
  day" is a crash artefact, not a standalone finding.

Magnitudes are small (4.0 to 4.6 on the realised 1-6 range), the markers are
proxies, and these are associations at n=1 wide error, not mechanism.

---

## 5. Can the symptom notes corroborate POTS episodes?

**No.** Across all notes, only **32 clauses** carry any POTS-adjacent keyword (and
most are generic "staan" / "opstaan", not orthostatic-symptom reports), and only
**2 of the 246 POTS-signature days** have any such note. The written record does
not carry orthostatic-symptom vocabulary (dizziness on standing, palpitations,
low-blood-volume, salt/electrolyte), so the notes cannot give extra colour to the
watch-detected POTS moments. This is a **prospective-logging gap** (the same shape
as the household-illness gap): a lightweight orthostatic-symptom tag would let a
future analysis corroborate the watch U-dip against felt orthostatic symptoms.

---

## 6. Caveats per CONVENTIONS section 4.1 + section 4.2

- **Proxy markers, not diagnoses.** "POTS-signature" = the stress U-dip proxy;
  "PEM-signature" = the overnight HRV-proxy load. Neither is a clinical label; a
  true orthostatic read would need positional / standing-HR data this device does
  not provide.
- **The U-dip is not a validated POTS marker** (external literature review,
  [`../../../literature/reviews/pots_operationalisation_wearable_review.md`](../../../literature/reviews/pots_operationalisation_wearable_review.md)):
  POTS is defined by an orthostatic HR delta this posture-blind device cannot form;
  the within-day stress-trough count has no precedent as a POTS marker; and its
  polarity runs *opposite* the population POTS signature (a stress U-dip is a
  transient HRV rise; POTS is HRV withdrawal). The defensible label is "a within-day
  autonomic-variability event the participant manages as if orthostatic," not "a
  POTS marker." This does not affect the separability result (two distinct signals);
  it caps only what the second signal may be *called*.
- **The POTS marker is a thin substrate.** `u_dip_count` is a sparse low count -
  43% of days are zero and the max is 5, so a signature day (z >= 1.0) turns on a
  small integer difference. This is enough for a descriptive *marker* but does not
  warrant "axis" / "family" language on its own; the marker is a low-resolution
  discriminator, flagged as such.
- **Weakly correlated, not independent.** The markers are weakly *positively*
  correlated (r = +0.09, CI excludes zero); "separable" here means "share <1% of
  variance / mostly-different days," not "statistically independent."
- **Descriptive, no causal marks.** Correlations and group means are associations
  at n=1 with wide error; the felt-state gaps are small on the 1-6 scale.
- **Threshold sensitivity.** The signature-day rates use z >= 1.0; the robust
  separability claim is the threshold-free correlation (r ~ 0.09), not the day
  counts. The felt-state group means are more stable than the exact rates.
- **Single-pool; the phase read is descriptive variation, not a verdict** (per the
  R19 discipline). The 4b -> 5 decline coincides with the citalopram-onset boundary
  and is not independent of the medication story.
- **Baseline coverage** drops the earliest weeks + phase 3 (needs 40+ prior days),
  so "when" is read on phases 4a/4b/5 only.

---

## 7. Verification log

- **Markers**: `u_dip_count` (POTS, sigma_floor 0.5), `stress_mean_sleep` (PEM,
  sigma_floor 2.0), `stress_stdev_sleep` (PEM secondary, 0.5); z vs [d-90,d-30]
  trimmed (10/90) mean/std, min 40 prior days.
- **Surface**: Stratum 4 (2022-09-03 to 2026-06-05); n_days both-computable 1090.
- **Separability**: Pearson +0.092 (95% CI [+0.033, +0.151], excludes zero;
  shared variance 0.85%), Spearman +0.060 (p = 0.047), phi +0.050;
  crash-drop-robust (r 0.092 -> 0.072).
- **Felt-state inference**: Mann-Whitney U vs neither -- PEM-only p < 0.0001
  (d = -0.40), POTS-only p = 0.19 (null), both p = 0.0006 (d = -0.54 but crash-driven).
- **Peer review (2026-07-07)**: independent fresh-context review
  (`reviews/pem-pots-reframing-2026-07-07.md`), MAJOR-REVISIONS-NEEDED, folded --
  softened "not correlated" -> "weakly correlated / largely distinct" (CI excludes
  zero); added the missing section-3.4 crash-drop and dropped the crash-driven
  "both = lowest" claim; added the MWU tests; flagged the thin u_dip substrate and
  the citalopram-onset era-confound on the timing read. Numbers reproduced exactly.
- **Notes source**: `processed/notes/notes-categorized-v24-clauses.csv`; POTS
  keyword scan (duizel, staan, opstaan, orthostat, hartklop, bloeddruk, flauw,
  zout, electrolyt, bloedvolume).
- **Operand-source path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`.
- **Machine-readable**: `summary.json` (gitignored per the `docs/research/**/*.json`
  rule).

---

## 8. Cross-references

- **POTS substrate**: `analyses/hypotheses/HA11-stress-udip/result.md` (the U-dip
  crash-discrimination test) + `methodology/stress_low_motion_primitive.md`.
- **PEM substrate**: `analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md`,
  `HA07d-sleep-stress-variability/result.md`.
- **Phase axis**: `methodology/lc_recovery_phase_axis.md`; per-phase levels
  `analyses/descriptive/recovery_phase_signal_backdrop/` (R19).
- **Guide source**: Wiggers handleiding, clean extraction `c:/tmp/wiggers_raw.txt`
  (pdftotext -raw; the orthostatic / U-dip / electrolyte chapters). Catalog
  `docs/research/wiggers_testable_hypotheses.md`.

---

*End of findings.*
