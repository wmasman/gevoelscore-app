# Findings - PEM vs POTS separability in the watch data (descriptive)

**Descriptive Layer-1 analysis** answering the reframing questions raised
2026-07-07: is the POTS-signature watch pattern separable from the PEM-signature
pattern, when does it appear, do POTS-signature days coincide with lower felt-state,
and can the symptom notes corroborate POTS episodes. Producer-mode, for the
participant-researcher (repo owner), drafted 2026-07-07 by Claude (Opus 4.8).
Reproducible via [`run.py`](run.py).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

**Operationalisation (PROXY markers, grounded in Wiggers' own framing; not a
diagnosis):**
- **POTS-signature marker** = elevated within-day stress **U-dip** (`u_dip_count`
  z vs personal baseline) - the orthostatic / blood-volume pattern Wiggers ties to
  ORS / electrolytes, and the one relatively-specific orthostatic watch-signal on
  this corpus (the substrate of HA11).
- **PEM-signature marker** = elevated overnight stress (`stress_mean_sleep` z, the
  HRV-proxy autonomic load), with `stress_stdev_sleep` as a secondary read.

Both z vs the personal lagged [d-90, d-30] trimmed baseline (project standard). A
"signature day" = marker z >= 1.0 (stated threshold; the separability read is the
threshold-free correlation). Single-pool, baseline-relative, aggregated. No causal
marks per [CONVENTIONS section 4.1](../../../CONVENTIONS.md); the markers are
proxies and the associations are not mechanism. n_days with both markers computable
= 1090 (of 1372; the [d-90,d-30] baseline needs 40+ prior days, so the earliest
weeks and phase 3 drop out).

---

## 1. Headline

**PEM and POTS are separable in this body's watch data - they are essentially
independent day-markers, not the same signal twice.** And the two carry felt-state
differently: the **PEM** marker tracks lower gevoelscore, the **POTS** marker does
not. The orthostatic U-dip pattern is the "dysregulated but not necessarily feeling
bad" signature Wiggers warns about ("don't be fooled by good values"); the PEM
autonomic load is the one that coincides with feeling worse, and the two together
mark the lowest felt-state.

---

## 2. Separability - are POTS-days and PEM-days the same days?

| statistic | value |
|---|---:|
| Pearson r (POTS-marker z, PEM-marker z) | **+0.092** |
| Spearman r | +0.060 |
| Pearson r (POTS-marker, PEM-*variability* z) | +0.014 |
| contingency phi (POTS-day x PEM-day) | +0.050 |

Contingency of signature-days: **both 77 / POTS-only 169 / PEM-only 219 /
neither 625**. The two markers share almost no variance (r ~ 0.09), and most
signature-days are one mechanism or the other, not both. **They are distinguishable,
not heavily correlated** - which is the empirical warrant for looking for both
separately rather than collapsing them into one "autonomic dysregulation" axis.

---

## 3. When does the POTS signal appear (per recovery phase)?

| phase | id | n_days | POTS-day rate | PEM-day rate | mean POTS z | mean PEM z |
|---|---|---:|---:|---:|---:|---:|
| `pacing_pre_citalopram_learning` | 4a | 6 | 33.3% | 16.7% | -0.13 | -0.47 |
| `pacing_habit_established` | 4b | 500 | **27.0%** | 30.0% | **+0.23** | +0.37 |
| `citalopram_modulated` | 5 | 584 | **18.7%** | 24.8% | **+0.14** | +0.04 |

The POTS (U-dip) signature is **stronger in the pre-citalopram pacing-habit era
(4b) and recedes into the citalopram era (5)** - both its day-rate (27% -> 18.7%)
and its mean level fall. This matches HA11 (U-dip crash-discrimination SUPPORTED in
the early era, receding later) and the participant's lived report that the POTS
picture waxes and wanes as symptoms change. Phase 3 (`lc_pre_ergo`) and the earliest
days have no computable baseline and drop out; phase 4a (n=6) is noise.

---

## 4. Are POTS-signature days lower in felt-state?

| group | n | mean gevoelscore |
|---|---:|---:|
| neither | 625 | 4.48 |
| **POTS-only** | 169 | **4.57** |
| **PEM-only** | 219 | **4.15** |
| **both** | 77 | **4.03** |
| any POTS | 246 | 4.40 |
| any PEM | 296 | 4.12 |

**No - POTS-only days are not lower; if anything marginally higher than neither
(4.57 vs 4.48).** It is the **PEM** marker that tracks lower felt-state (PEM-only
4.15), and the **lowest** felt-state is when both co-occur (4.03). The direction is
consistent and interpretable - the orthostatic pattern is the "quiet dysregulation"
that need not feel bad, the PEM load is what coincides with feeling worse - but the
magnitudes are **small** (4.0 to 4.6 on the realised 1-6 felt-state range), the
markers are proxies, and this is an association at wide error, not a mechanism.

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
- **Separability**: Pearson +0.092, Spearman +0.060, phi +0.050.
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
