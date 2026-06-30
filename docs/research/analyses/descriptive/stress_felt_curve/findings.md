# Descriptive: binned stress -> felt-state curve (R22)

**Purpose**: a clean, higher-resolution binned `all_day_stress_avg` -> `gevoelscore`
curve for the Wiggers site `/workings/not-a-straight-line` page, replacing the
provisional 5-quintile version. **Descriptive ONLY** -- no p-values, no verdict.
The PARTIAL/REJECTED test verdicts live in the HA-C3p / HA-C3 v2 scorecard, NOT
here. This document is the shipped *shape*; the inference is elsewhere.

Drafted 2026-06-30 by Claude (Opus 4.8, 1M context) in producer-mode under user
authorisation. Source cell: the HA-C3p headline pool (this re-bins the same
substrate at higher resolution; bin-means at the coarse quintile level reconcile
to the locked HA-C3p result.md: 3.82 / 4.14 / 4.27 / 4.29 / 4.02).

---

## 1. The slice (date-free, for the caption)

**Cell**: the **medication-free window** -- the Long COVID era *before* citalopram
was started. In the project stratification this is the **unmedicated phase of
Citalopram Stratum 4** (`citalopram_phase == "unmedicated"`, plasma dose = 0 mg).

**Why this cell**: `all_day_stress_avg` is a CONFIRMED dose-modulated channel
(+0.57 stress-points per mg of plasma citalopram, per
`citalopram_dose_response_stress_mean_sleep.md` section 5.6.1). Pooling
medicated and unmedicated days would slide the whole stress axis right under the
drug and contaminate the shape. Restricting to the medication-free window gives a
curve that is clean of the citalopram dose-shift -- the stress axis means the
same thing at every point on it.

**Date-free caption phrasing** (suggested): *"medication-free stretch of the
illness, before the antidepressant was started, so the stress scale reads the
same all the way along."*

**Pool provenance**: LC era start through the last unmedicated day; first 21
device-baseline days excluded; the April-2024 onboarding cluster excluded; days
require a valid `gevoelscore` and `all_day_stress_avg` in [0,100]. This reproduces
the HA-C3p primary pool exactly: **n = 581** (matches HA-C3p result.md section 2).

---

## 2. Bin scheme

**10 equal-N bands (deciles) of `all_day_stress_avg`.** Each band holds ~58 days
(581 / 10; the lowest band carries the +1 remainder, n = 59). Equal-N is preferred
over equal-width so every point on the curve rests on the same sample size and the
spread band is comparable band-to-band. Band edges are data-driven decile cut
points of the observed stress distribution in this cell (stress range 20 - 69).

- `lo` / `hi` in the table below and in the shipped JSON = **p25 / p75** (the
  inter-quartile spread of `gevoelscore` within the band). This is the
  **noise-envelope band** and it is the load-bearing visual: the band-to-band
  shifts in the mean are tenths of a point, while the within-band IQR is a full
  1-2 points wide. **Show the spread band prominently.**
- A secondary **95% CI of the mean** column is reported for completeness (normal
  approximation, `mean +/- 1.96 * SE`). It is NOT the shipped `lo/hi`.

---

## 3. Binned table -- full pool (crashes KEPT; primary)

| band | stress range | x_center | n | mean gevoelscore | p25 (lo) | p75 (hi) | 95% CI of mean |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | 20 - 28 | 25.93 | 59 | 3.847 | 3.0 | 5.0 | [3.556, 4.139] |
| 2 | 28 - 30 | 29.21 | 58 | 4.241 | 4.0 | 5.0 | [4.041, 4.442] |
| 3 | 30 - 32 | 31.09 | 58 | 4.276 | 4.0 | 5.0 | [4.061, 4.490] |
| 4 | 32 - 33 | 32.43 | 58 | 4.276 | 4.0 | 5.0 | [4.051, 4.501] |
| 5 | 33 - 34 | 33.64 | 58 | 4.207 | 4.0 | 5.0 | [3.982, 4.432] |
| 6 | 34 - 36 | 34.69 | 58 | 4.259 | 4.0 | 5.0 | [4.068, 4.449] |
| 7 | 36 - 37 | 36.26 | 58 | 4.362 | 4.0 | 5.0 | [4.177, 4.547] |
| 8 | 37 - 39 | 37.93 | 58 | 4.155 | 4.0 | 5.0 | [3.952, 4.359] |
| 9 | 39 - 42 | 40.02 | 58 | 4.086 | 4.0 | 5.0 | [3.849, 4.324] |
| 10 | 42 - 69 | 46.72 | 58 | 3.690 | 3.0 | 5.0 | [3.369, 4.010] |

**Reading (descriptive)**: the mean climbs from ~3.85 at the lowest-stress band to
a broad plateau-peak around stress 30 - 37 (means ~4.21 - 4.36), then eases back
down to ~3.69 in the highest-stress band. A gentle inverted-U / threshold hump,
not a straight line. **Every adjacent-band gap is tenths of a point and sits
inside the p25 - p75 spread band** -- the IQR is 1 - 2 points wide at every band
while the mean wanders by ~0.1 - 0.4. The spread band is the honest visual: the
hump is real in the means but small against the day-to-day scatter.

**Fitted straight line (real least-squares, full pool)**:

    fit_line = { x0: 20.0, y0: 4.413, x1: 69.0, y1: 3.506 }   (slope -0.0185, intercept 4.783)

This is the actual OLS line through the 581 raw daily points -- "what a straight
line sees": a faint overall downward tilt that completely misses the rise-then-fall
hump the binned curve shows. That mismatch is the whole point of the page.

---

## 4. Crash-drop sensitivity (CONVENTIONS section 3.4)

Re-binned with `is_crash` days removed (n drops 581 -> 503; 78 crash days
removed), equal-N deciles recomputed on the no-crash distribution:

| band | stress range | n | mean (no-crash) | p25 | p75 |
|---|---|---:|---:|---:|---:|
| 1 | 20 - 28 | 51 | 4.235 | 4.0 | 5.0 |
| 2 | 28 - 30 | 51 | 4.255 | 4.0 | 5.0 |
| 3 | 30 - 32 | 51 | 4.412 | 4.0 | 5.0 |
| 4 | 32 - 33 | 50 | 4.480 | 4.0 | 5.0 |
| 5 | 33 - 34 | 50 | 4.380 | 4.0 | 5.0 |
| 6 | 34 - 35 | 50 | 4.360 | 4.0 | 5.0 |
| 7 | 35 - 36 | 50 | 4.380 | 4.0 | 5.0 |
| 8 | 37 - 38 | 50 | 4.300 | 4.0 | 5.0 |
| 9 | 38 - 40 | 50 | 4.440 | 4.0 | 5.0 |
| 10 | 40 - 58 | 50 | 4.400 | 4.0 | 5.0 |

`fit_line (no-crash) = { x0: 20.0, y0: 4.235, x1: 58.0, y1: 4.577 }` (slope **+0.009**).

**The crash-drop sensitivity CHANGES the shape.** With crashes kept, the high-stress
end droops to 3.69 and the OLS slope is negative (-0.0185); with crashes removed,
the high-stress droop largely disappears (top band rises to ~4.40) and the OLS
slope flips to slightly positive (+0.009). **Mechanism**: of the 10 days with
stress > 50, **8 are crash days**; above stress 45, 13 of 25 days are crashes.
The downturn of the full-pool curve at the high-stress end is substantially
*carried by crash days landing in the top stress band*. This is consistent with
the HA-C3p locked crash-drop FLAG (second-difference S = -0.196 full -> -0.033
no-crash, sign-boundary flag). The rise from low to mid stress is present in both;
only the high-stress fall-off is crash-dependent.

**Shipping note for the site**: the shipped `curve` series is the **full pool
(crashes kept)** -- it is the participant actual lived distribution. The no-crash
row is a sensitivity disclosure, not a replacement series. If the page makes any
claim about the *downturn at high stress*, it must carry the crash caveat, because
that part of the shape is crash-driven.

---

## 5. Optional smooth (LOESS, full pool)

Tricube-weighted local-linear LOESS (frac = 0.5) over the full pool, **capped at
stress <= 50** -- above 50 there are only 10 days (8 of them crashes) so the smooth
there is a sparse-data edge artefact and is NOT plotted:

    smooth = [
      {x:20.00,y:3.391},{x:22.04,y:3.562},{x:24.08,y:3.718},{x:26.12,y:3.879},
      {x:28.17,y:4.071},{x:30.21,y:4.194},{x:32.25,y:4.261},{x:34.29,y:4.285},
      {x:36.33,y:4.276},{x:38.38,y:4.194},{x:40.42,y:4.098},{x:42.46,y:3.949},
      {x:44.50,y:3.837},{x:46.54,y:3.690},{x:48.58,y:3.517}
    ]

The smooth peaks at ~4.285 around stress 34 and falls away on both sides -- the
same inverted-U the bands show, drawn as a continuous line.

---

## 6. Shipped JSON -- shape-not-linear.json `curve` object

    {
      "cell": "medication_free_unmedicated_stratum4",
      "cell_caption": "medication-free stretch of the illness, before the antidepressant was started, so the stress scale reads the same all the way along",
      "bin_scheme": "10 equal-N deciles of all_day_stress_avg; ~58 days per band; lo/hi = p25/p75 IQR spread band",
      "predictor": "all_day_stress_avg",
      "outcome": "gevoelscore",
      "n": 581,
      "bins": [
        { "x_label": "20-28", "x_center": 25.93, "n": 59, "mean": 3.847, "lo": 3.0, "hi": 5.0 },
        { "x_label": "28-30", "x_center": 29.21, "n": 58, "mean": 4.241, "lo": 4.0, "hi": 5.0 },
        { "x_label": "30-32", "x_center": 31.09, "n": 58, "mean": 4.276, "lo": 4.0, "hi": 5.0 },
        { "x_label": "32-33", "x_center": 32.43, "n": 58, "mean": 4.276, "lo": 4.0, "hi": 5.0 },
        { "x_label": "33-34", "x_center": 33.64, "n": 58, "mean": 4.207, "lo": 4.0, "hi": 5.0 },
        { "x_label": "34-36", "x_center": 34.69, "n": 58, "mean": 4.259, "lo": 4.0, "hi": 5.0 },
        { "x_label": "36-37", "x_center": 36.26, "n": 58, "mean": 4.362, "lo": 4.0, "hi": 5.0 },
        { "x_label": "37-39", "x_center": 37.93, "n": 58, "mean": 4.155, "lo": 4.0, "hi": 5.0 },
        { "x_label": "39-42", "x_center": 40.02, "n": 58, "mean": 4.086, "lo": 4.0, "hi": 5.0 },
        { "x_label": "42-69", "x_center": 46.72, "n": 58, "mean": 3.690, "lo": 3.0, "hi": 5.0 }
      ],
      "fit_line": { "x0": 20.0, "y0": 4.413, "x1": 69.0, "y1": 3.506 },
      "smooth": [
        { "x": 20.00, "y": 3.391 }, { "x": 22.04, "y": 3.562 }, { "x": 24.08, "y": 3.718 },
        { "x": 26.12, "y": 3.879 }, { "x": 28.17, "y": 4.071 }, { "x": 30.21, "y": 4.194 },
        { "x": 32.25, "y": 4.261 }, { "x": 34.29, "y": 4.285 }, { "x": 36.33, "y": 4.276 },
        { "x": 38.38, "y": 4.194 }, { "x": 40.42, "y": 4.098 }, { "x": 42.46, "y": 3.949 },
        { "x": 44.50, "y": 3.837 }, { "x": 46.54, "y": 3.690 }, { "x": 48.58, "y": 3.517 }
      ],
      "note": "Descriptive shape only; no test verdict. lo/hi are the p25-p75 spread band (the noise envelope) and are wider than the band-to-band shifts in the mean, which is the point. The high-stress downturn (band 10 and the smooth tail) is crash-driven: of 10 days with stress>50, 8 are crashes; with crash days removed the downturn flattens and the OLS slope flips slightly positive. Smooth is capped at stress<=50 (sparse beyond)."
    }

The site owns `shape-not-linear.json`; this is the proposed `curve` object to drop
in. This document does NOT touch the site repo or any locked result.md.

---

## 7. Privacy statement

This artefact reports **aggregated band-level statistics only**: per-band n,
mean, median, p25/p75, and a CI of the mean, over bands of >= 58 days each. No
dated daily values, no raw per-day (date, stress, gevoelscore) rows, and no
individually identifiable day are exposed. The fit line is the OLS endpoint pair
derived from the pooled fit, not a list of points. The minimum band size (58) is
well above any small-cell disclosure threshold. Date-free framing is used
throughout per the caption guidance in section 1.

---

## 8. Count-triple (CONVENTIONS section 3.6)

- **Days in cell (primary, crashes kept)**: **n = 581** (matches HA-C3p result.md
  section 2 unmedicated pool).
- **Days after crash-drop**: **n = 503** (78 `is_crash` days removed).
- **Bands**: **10 equal-N deciles**, ~58 days each (band 1 = 59, bands 2-10 = 58).

Named exclusions reaching the n = 581 figure: LC-era start floor, first 21
device-baseline days, April-2024 onboarding cluster, medicated days (all
post-2024-04-08 unmedicated-window cutoff), and rows missing `gevoelscore` or
`all_day_stress_avg`. Stress range in cell: 20 - 69. Gevoelscore median: 4.0.

---

## 9. Reproducibility

- Pool + binning logic replicates `docs/research/analyses/hypotheses/HA-C3p/test.py`
  day-validity gate (`day_passes_gate`, `find_device_baseline_cutoff`) exactly;
  coarse-quintile bin-means reconcile to the locked HA-C3p result (3.82 / 4.14 /
  4.27 / 4.29 / 4.02).
- Source: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`.
- Columns used: `date`, `gevoelscore`, `all_day_stress_avg`, `is_crash`,
  `has_garmin_uds`.
- Equal-N deciles by sorted-index split; OLS via `numpy.linalg.lstsq`; LOESS
  tricube local-linear, frac = 0.5.
- Descriptive only: no permutation null, no p-value, no verdict computed or shipped.
