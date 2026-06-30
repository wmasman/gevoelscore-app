# Chart-exports (R1) — beat-2 chart data assembly, single-pool primary

**Producer-mode export artefact.** Assembled 2026-06-30 for Wiggers-site request R1
(replace beat-2 chart placeholders with real aggregated data). Derivative assembly
over already-locked single-pool numbers and already-shipped descriptive cards — **no
new null draws, no new hypothesis tests, no re-lock, no audit, no git, no write into
the site repo, no touch of any locked `result.md`.** Read-only on all sources.

**Scope.** The 5 beat-2 charts named in
`wiggers_research_story/site/assets/ASSETS-NEEDED.md:12-18`:
parasympathetic-swing (HA10), walls-of-orange (H02b trajectory), hrv-decline (HA07d),
exertion-lead-up (HA01b/HA01c), crash-frequency (R13 / K01-K02).

---

## 0. The single-pool reframe this export obeys (do not strip on re-use)

The 2-era "decay / swing / decline OVER TIME" framing is **RETIRED as primary** per the
single-pool re-anchor handoff §F/§G, executed at
`docs/research/analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md:5,8-9`.
Consequences this export enforces:

1. **No manufactured time-decay curves.** Three of the five charts are conceived as
   temporal-decay narratives (walls-of-orange **decay**, parasympathetic-**swing** over
   eras, hrv-**decline** over time). The single-subject observational design **cannot
   answer "does the effect change over time?"** (`findings.md:9`). For these we DROP the
   per-era / per-year decay shape and propose a single-pool baseline-relative aggregate.
   Where the chart's very concept dissolves under single-pool, it is FLAGGED for an
   editorial decision (§6), not back-filled with invented data.
2. **Era contrast = a number, never a per-era verdict.** Where an era overlay is shown
   at all, it ships as a single disc_pp number + CI, per `findings.md:5` ("number, not
   a narrative") — never a train-SUPPORTED / validate-REFUTED storyline.
3. **Baseline-relative, aggregated only.** No dated raw points; every value is a
   corpus-level proportion, a z-vs-baseline band, or a monthly/yearly count.
4. **Honesty about nulls.** Where a chart can only honestly show "no clean over-time
   shape," the export says so. Of the 7 scorecard signals, only HA07d and HA01c are
   single-pool SUPPORTED; the other five are single-pool NOT-SUPPORTED
   (`findings.md:15-26`). HA01b (exertion-lead-up) is single-pool **NOT-SUPPORTED**.

---

## 1. Source inventory (file:line)

- Single-pool per-signal disc_pp + CI + n + frac_crash/frac_null + verdict:
  `single_pool_reanchor/findings.md:15-26` (HA01b :15, HA10 :19, HA07d :17, HA01c :21,
  H02b :23); pool n's `findings.md:187` (n_days=1372, n_crash_episodes=29).
- Per-signal usability metrics (sensitivity / specificity / PPV / lift / CI / tier):
  `garmin_exploration/cards/trust-panel-export.md:79-85`.
- Stress→felt curve (R22, descriptive, not over-time): `stress_felt_curve/findings.md`
  (not a beat-2 chart, but the project's worked example of "show the shape, not the
  line"; cited for the reframe pattern only).
- Crash-frequency per month / per year (R13, already aggregated):
  `felt_state_timeline/findings.md:90-113` (monthly crash counts + buckets),
  `:113` (bucket totals: short 21, medium 4, long 4; max 14 days), `:166`
  (per-year denominators), `:23` (29 crash episodes / 103 crash-days / 49 dip episodes).
- Site placeholder shapes (read-only, for JSON-shape matching only):
  `site/data/charts/walls-of-orange.json`, `site/data/charts/felt-state-timeline.json`.

---

## 2. Chart 1 — crash-frequency (CLEAN single-pool / over-time legitimate)

**Status: ASSEMBLABLE, clean.** This is the one legitimate over-time chart: a Layer-1
**descriptive trajectory** of a count, not an inferred effect-decay. R13 already
aggregates it.

**Source numbers** (`felt_state_timeline/findings.md:90-113`, rolled to year — the
monthly table summed by `episode_start[:4]`; per-year denominators cross-checked against
`findings.md:166`):

| year | n_crash | note |
|---|---:|---|
| 2022 | 5 | partial (logging starts 2022-09) |
| 2023 | 9 | |
| 2024 | 11 | |
| 2025 | 2 | |
| 2026 | 2 | partial (through 06-05) |

Total = 29 crash episodes (`findings.md:23`). Bucket totals across all 29:
short 21, medium 4, long 4; longest = 14 days (the 2023-11 crash, already public in
`corpus.json` → timeline) (`findings.md:113`).

**Proposed JSON** (`data/charts/crash-frequency.json`; matches ASSETS-NEEDED "crashes
per year 2022-2026, depth/duration optional"):

```json
{
  "unit": "crash_episodes",
  "years": ["2022", "2023", "2024", "2025", "2026"],
  "n_crash": [5, 9, 11, 2, 2],
  "partial_years": ["2022", "2026"],
  "duration_buckets_total": { "short_2_3d": 21, "medium_4_6d": 4, "long_7plus_d": 4 },
  "longest_crash_days": 14,
  "note": "Descriptive count trajectory, not an effect-decay. 2022 partial (logging starts 2022-09); 2026 partial (through 06-05). Sustained crashes thin out 2024->2025; transient dips do not (see R13 dip:crash ratio 0.8->6.0). No causal reading; medication + pacing are declared confounds (corpus.json)."
}
```

**Single-pool reframe note:** none needed — this chart was never an effect-decay chart.
It is a raw count over time, which the design *can* legitimately show. The honest caveat
is the **partial-year** flag on 2022 and 2026 and the **confound** declaration
(citalopram buildup starts 2024-04, taper 2026-03), so the 2024→2025 thinning is *not*
narrated as "the signal faded" — it is a count change with declared confounds
(`findings.md:166,210`).

---

## 3. Chart 2 — exertion-lead-up (ASSEMBLABLE, reframed to single-pool, honest null)

ASSETS-NEEDED asks for "crash share with heavy exertion in 4-day lead-up, **by era**"
(HA01b). The **by-era** framing is exactly what the reframe retires. Reframed to
single-pool.

**Source numbers:**
- HA01b single-pool: disc_pp = **+5.1 pp**, CI95 **[-14.7, +13.3]**, perm-p 0.3689,
  frac_crash 0.821, frac_null 0.770, verdict **NOT-SUPPORTED**
  (`findings.md:15`, narrative `:32-36`).
- HA01b usability: sensitivity 82.1% [64-92]%, specificity 23.0% [18-29]%, PPV 2.25%,
  lift 1.06×, Tier C (`trust-panel-export.md:83`).
- HA01c (effective-exertion rank shock, the single-pool SUPPORTED sibling): disc_pp
  **+19.6 pp**, CI95 **[-19.6, +19.1]**, perm-p 0.0290, frac_crash 0.821,
  frac_null 0.625, verdict **SUPPORTED** — but **Tier-C PPV** (~2.x%) and load-bearing
  status WITHHELD pending the v2 threshold-monotonicity diagnostic
  (`findings.md:21,73-78`).

**Proposed JSON** (`data/charts/exertion-lead-up.json`) — a single baseline-relative
share pair (crash lead-ups vs ordinary days), NOT a per-era pair:

```json
{
  "unit": "share_of_windows",
  "framing": "single_pool",
  "primary_signal": "HA01b_exertion_class_heavy_in_4d_leadup",
  "crash_leadup_share": 0.821,
  "ordinary_day_share": 0.770,
  "discrimination_pp": 5.1,
  "discrimination_ci95": [-14.7, 13.3],
  "verdict": "NOT-SUPPORTED",
  "sibling_supported_signal": {
    "name": "HA01c_effective_exertion_rank_shock",
    "crash_leadup_share": 0.821,
    "ordinary_day_share": 0.625,
    "discrimination_pp": 19.6,
    "discrimination_ci95": [-19.6, 19.1],
    "verdict": "SUPPORTED",
    "caveat": "Tier-C PPV (~2%); load-bearing status WITHHELD pending v2 threshold-monotonicity diagnostic"
  },
  "note": "Single-pool, not per-era. HA01b (the asset's named signal) is NOT-SUPPORTED: heavy exertion shows up in ~82% of crash lead-ups but also ~77% of ordinary days, so the gap (+5.1 pp) is inside its own CI. The reframed honest read is its single-pool-SUPPORTED sibling HA01c (rank-shock framing, gap +19.6 pp) — but that is Tier-C and the CI still straddles zero, so even the supported version is not a forecast."
}
```

**Single-pool reframe note:** the **by-era** split is dropped; both shares are
single-pool. The original asset concept ("does heavy exertion lead crashes?") survives,
but the honest answer for the *named* signal (HA01b) is a **null** — the gap is real in
the point estimate but inside the CI. If the page wants a non-null lead-up signal it
must switch to HA01c and carry the Tier-C + WITHHELD caveat. Either way: no per-era
verdict, and the CI must be shown (it crosses zero).

---

## 4. Chart 3 — parasympathetic-swing (DROP the swing-over-time; FLAG)

ASSETS-NEEDED asks for "overnight-recovery z vs baseline, t-6..t0, **early vs late**"
(HA10) — i.e. two curves, one per era, telling a "the swing changed over the eras"
story. The reframe **retires** the per-era swing narrative, and HA10 is the project's
**only directionality-reversal** test (train REFUTED -20.5 / validate SUPPORTED +16.2 →
OVERALL REFUTED), so the `early` vs `late` two-curve shape is precisely the artefact the
reframe says not to manufacture (`findings.md:19,59-64`).

**Source numbers (single-pool):** HA10 disc_pp = **+4.1 pp**, CI95 **[-16.5, +16.8]**,
perm-p 0.4328, frac_crash 0.769, frac_null 0.729, verdict **NOT-SUPPORTED**
(`findings.md:19,59-64`). Usability: sensitivity 76.9%, specificity 27.1%, PPV 2.23%,
lift 1.05×, Tier C (`trust-panel-export.md:84`).

**What can be assembled honestly:** NOT the requested `{labels, early[], late[]}`
t-6..t0 dual curve. The per-timestep z-vs-baseline trajectory (t-6..t0) is **not present
in any assembled source** — `findings.md` carries only the windowed discrimination
scalar (`disc_pp`), not a 7-point lead-up profile. Manufacturing a 7-point early/late
swing from a single scalar would be fabrication.

**Proposed JSON** (`data/charts/parasympathetic-swing.json`) — single-pool scalar +
honest null, NOT a dual t-6..t0 curve:

```json
{
  "unit": "pp",
  "framing": "single_pool",
  "signal": "HA10_morning_body_battery_peak_z",
  "discrimination_pp": 4.1,
  "discrimination_ci95": [-16.5, 16.8],
  "crash_leadup_share": 0.769,
  "ordinary_day_share": 0.729,
  "verdict": "NOT-SUPPORTED",
  "era_overlay_retired": true,
  "note": "The 'early vs late swing' two-curve shape is RETIRED. HA10 was the project's only directionality-reversal test (train and validate pointed opposite ways), which under single-pool collapses to a null (+4.1 pp, CI crosses zero). There is no clean over-time swing to draw. No t-6..t0 per-step profile exists in the assembled sources."
}
```

**FLAG (editorial):** see §6 F1. The asset's data shape (`{labels, early, late}`) cannot
be honored without either (a) an editorial decision to replace the dual-curve visual with
a single null-with-CI chip, or (b) a FRESH per-timestep lead-up extraction (t-6..t0
overnight-recovery z), which is acquire-work, not assembly.

---

## 5. Chart 4 — hrv-decline (DROP the decline-over-time; reframe to single-pool z-band)

ASSETS-NEEDED asks for "multi-day sleep-stress-variability z vs baseline" (HA07d), with
the claim title "hrv-**decline**" implying an over-time downward trajectory. HA07d is the
**stpro-est** signal in the set (single-pool **SUPPORTED**), so unlike charts 3/4 there
IS a real positive result to show — but it is a **windowed discrimination**, not a
decline-over-eras, and the "decline over time" framing must be dropped.

**Source numbers (single-pool):** HA07d disc_pp = **+19.7 pp**, CI95 **[-18.1, +17.0]**,
perm-p 0.0291, frac_crash 0.880, frac_null 0.683, verdict **SUPPORTED**
(`findings.md:17,45-50`). Usability: sensitivity 88.0% [70-96]%, specificity 31.7%
[26-39]%, PPV 2.71% [2.17%], PPV band [1.99-3.27]%, lift 1.28×, Tier C
(`trust-panel-export.md:79`). It is the ONLY single-pool SUPPORTED scorecard signal
(`trust-panel-export.md:36-41`).

**Proposed JSON** (`data/charts/hrv-decline.json`) — single-pool z-vs-baseline
discrimination band, reframed away from "decline over time":

```json
{
  "unit": "pp",
  "framing": "single_pool",
  "signal": "HA07d_sleep_stress_variability_z_bidirectional",
  "construct_note": "sleep-stress-variability is the HRV-proxy chain (FR245 HRV hardware-blocked; stress stdev delta is the proxy)",
  "discrimination_pp": 19.7,
  "discrimination_ci95": [-18.1, 17.0],
  "crash_leadup_share": 0.880,
  "ordinary_day_share": 0.683,
  "verdict": "SUPPORTED",
  "ppv_at_base_2_11pct": 2.71,
  "lift": 1.28,
  "tier": "C",
  "note": "Reframed: NOT a decline-over-time curve. This is the single-pool windowed discrimination of overnight stress-variability (the HRV proxy) in crash lead-ups vs ordinary days. It is the project's strongest signal and the only single-pool SUPPORTED one (+19.7 pp), yet still Tier C: PPV ~2.7%, so when it fires a crash follows ~1 time in 37. A real but weak signal, not an alarm. The point estimate CI straddles zero on disc_pp even though the permutation p is 0.029 (wide-CI honesty at n=29)."
}
```

**Single-pool reframe note:** "hrv-**decline**" as an over-time downslope is dropped;
replaced by a single-pool discrimination band. The honest framing pairs the SUPPORTED
verdict with the Tier-C PPV so the reader does not over-read the green mark.
**Naming flag:** "HRV" is a proxy (sleep-stress-variability); FR245 HRV is
hardware-blocked (`trust-panel-export.md` construct + `findings.md:202`). Editorial should
decide whether the public chart keeps the word "HRV" or uses "overnight stress steadiness"
to avoid implying a direct HRV measurement. See §6 F3.

---

## 6. Chart 5 — walls-of-orange (DROP per-year decay; FLAG hardest)

This is the chart whose **placeholder actively encodes the retired narrative.** The
current `site/data/charts/walls-of-orange.json` ships
`discrimination_pp: [24.0, 31.8, 12.0, 1.5, -3.0]` across years 2022-2026 — a fabricated
"held early, faded toward zero" per-year decay curve (its own `_comment` says
PLACEHOLDER). That **per-year decay is exactly the concept the single-pool reframe
retires.** There is no per-year discrimination series in any assembled source, and the
single-subject design cannot answer "did the effect change over time" (`findings.md:9`).

**Source numbers (single-pool, H02b):** disc_pp = **+3.5 pp**, CI95 **[-21.2, +21.7]**,
perm-p 0.4458, frac_crash 0.500, frac_null 0.465, verdict **NOT-SUPPORTED**
(`findings.md:23,87-92`). Usability: sensitivity 50.0%, specificity 53.5%, PPV 2.27%,
lift 1.07×, Tier C (`trust-panel-export.md:85`). The retired era split (overlay number
only, NOT a verdict): locked train +29.9 pp / validate -8.2 pp → OVERALL REFUTED
(`findings.md:23,89`) — this is the source of the placeholder's "+31.8 peak then decay"
shape, and it is **retired**.

**Proposed JSON** (`data/charts/walls-of-orange.json`) — REPLACE the decay array with a
single-pool scalar + the era contrast as ONE number, not a per-year series:

```json
{
  "unit": "pp",
  "framing": "single_pool",
  "signal": "H02b_per_minute_stress_spike_count_3d",
  "discrimination_pp": 3.5,
  "discrimination_ci95": [-21.2, 21.7],
  "crash_leadup_share": 0.500,
  "ordinary_day_share": 0.465,
  "verdict": "NOT-SUPPORTED",
  "era_overlay_number_only": { "train_disc_pp": 29.9, "validate_disc_pp": -8.2, "as": "number_not_verdict_retired" },
  "per_year_decay_retired": true,
  "note": "The per-year decay curve is RETIRED and was a placeholder. Single-pool H02b is NOT-SUPPORTED: stress spikes show up in ~50% of crash lead-ups and ~46% of ordinary days (+3.5 pp, CI crosses zero). The train/validate contrast (+29.9 vs -8.2) ships ONLY as two overlay numbers, never as a 'held early, faded' story. The single-subject design cannot answer whether the effect changed over time (findings.md:9)."
}
```

**FLAG (editorial, hardest):** see §6 F2. The whole "walls of orange held early then
faded" beat-2 narrative is a **per-era decay story** that the single-pool reframe
retires. The chart concept needs an editorial rethink: either (a) re-cast the page around
the single-pool null ("the spike signal does not separate crash lead-ups from ordinary
days when you pool the whole illness"), or (b) keep the era contrast strictly as a
two-number overlay with no decay-line and no time axis. Do NOT keep the 5-point per-year
decay array.

---

## 6b. FLAG register (charts needing an editorial decision under single-pool)

| flag | chart | why it needs a rethink | honest fallback (assemblable now) |
|---|---|---|---|
| **F1** | parasympathetic-swing (HA10) | Asset wants `{labels, early[], late[]}` t-6..t0 dual swing. Per-era swing retired; HA10 is single-pool NULL and was the only directionality-reversal test. No per-timestep profile exists in sources. | Single null chip: disc +4.1 pp, CI [-16.5,16.8], NOT-SUPPORTED. A real t-6..t0 curve needs FRESH extraction. |
| **F2** | walls-of-orange (H02b) | Placeholder ships a fabricated per-year decay `[24,31.8,12,1.5,-3]`. Per-year decay is the retired narrative; single-pool H02b is NULL. | Single-pool scalar (+3.5, NOT-SUPPORTED) + era contrast as two overlay numbers only. Drop the time axis / decay line. |
| **F3** | hrv-decline (HA07d) | "HRV decline over time" — two issues: (a) over-time decline retired; (b) "HRV" is a proxy, FR245 HRV is hardware-blocked. | Single-pool z-band, SUPPORTED but Tier-C PPV 2.71%. Editorial decides whether to keep the word "HRV" or relabel "overnight stress steadiness." |

Charts 1 (crash-frequency) and 3 (exertion-lead-up) do **not** carry an editorial FLAG:
chart 1 is a legitimate descriptive count-over-time, and chart 3 is a clean single-pool
share pair (with the honest HA01b-null / HA01c-supported choice surfaced in-data).

---

## 7. What is missing (not assemblable; would need FRESH computation)

1. **Per-timestep lead-up profiles (t-6..t0)** for parasympathetic-swing (and any
   "multi-day z vs baseline" line for hrv-decline drawn as a trajectory rather than a
   scalar). `findings.md` carries only the windowed scalar disc_pp per signal, not a
   7-point per-day-before profile. A real lead-up curve is an **acquire-task**, not
   assembly. Do not fabricate from the scalar.
2. **Per-year discrimination series** for walls-of-orange. Does not exist; the
   single-subject design cannot produce a defensible per-year effect series
   (`findings.md:9`). The retired locked train/validate numbers are the only era
   contrast available, and only as two numbers.
3. **PPV / lift confidence intervals** if any chip publishes a CI on a derived metric —
   §2's PPV band is a Wilson-corner approximation; a defensible PPV CI is FRESH work
   (`trust-panel-export.md:184-192`).
4. **Depth axis (K01/K02)** for crash-frequency "depth optional." K01/K02 are
   NOT-APPLICABLE under single-pool (the era split IS their predictor;
   `findings.md:144-145`), so a depth-over-time series is not assemblable here; only the
   duration buckets (§2) ship.

---

## 8. Privacy statement

This export is **aggregated and contains no dated daily values, no per-day records, no
raw physiological readings, no note text, and no tag content.** Every number is a
corpus-level proportion (a frac_crash, a frac_null, a discrimination pp, a recall, a
specificity), an arithmetic function of those (PPV, lift), or a monthly/yearly count of
episodes. The only disclosed counts are cohort-level n's (n_days=1372,
n_crash_episodes=29) and per-signal denominators (n_crash 24-28, n_null 171-200,
`trust-panel-export.md:167-176`). Crash-frequency ships at YEAR granularity (months were
already month-floored in R13; here further rolled to year); the single 14-day
longest-crash duration fact is already public in the site's `corpus.json` → timeline. No
date, no timestamp, no individual crash episode, and no individual signal reading is
exported. Consistent with the presence-conditioned / no-prevalence-claim discipline
(`research_line_limitations.md`): the base rate is this subject's own crash frequency,
not a population prevalence claim.

---

## 9. Section-3.6 count-triple register (name / unit / file)

| count | value | name (scheme) | unit | file |
|---|---:|---|---|---|
| crash episodes (total) | 29 | crash_v2 | episode | `processed/crash_labels/labels_crash_v2.csv` |
| crash-days | 103 | crash_v2 | day | `processed/crash_labels/labels_crash_v2.csv` |
| crashes 2022 (partial) | 5 | crash_v2 (rolled to year) | episode | derived from `felt_state_timeline/findings.md:90-113` |
| crashes 2023 | 9 | crash_v2 (rolled to year) | episode | derived |
| crashes 2024 | 11 | crash_v2 (rolled to year) | episode | derived |
| crashes 2025 | 2 | crash_v2 (rolled to year) | episode | derived |
| crashes 2026 (partial) | 2 | crash_v2 (rolled to year) | episode | derived |
| crash duration buckets | short 21 / medium 4 / long 4 | crash_v2 `episode_length_days` | episode | `findings.md:113` |
| single-pool days | 1372 | Stratum-4 single pool | day | `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (`findings.md:187`) |
| single-pool crash episodes | 29 | crash_v2 (single pool) | episode | `findings.md:187` |
| per-signal null windows | 171-200 | legacy HA null reference set | window | `findings.md:15-26,187` |
| per-signal crash windows | 24-28 | legacy HA crash window set | window | `findings.md:15-26` |

---

## 10. Source citations (file:line)

- Single-pool disc_pp + CI + frac + verdict per signal:
  `docs/research/analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md:15`
  (HA01b), `:17` (HA07d), `:19` (HA10), `:21` (HA01c), `:23` (H02b); pool n's `:187`;
  reframe discipline `:5,8-9`.
- Usability metrics (sensitivity/specificity/PPV/lift/tier):
  `docs/research/analyses/garmin_exploration/cards/trust-panel-export.md:79-85`,
  SUPPORTED-honesty `:36-41`.
- Crash-frequency monthly + buckets + per-year denominators:
  `docs/research/analyses/descriptive/felt_state_timeline/findings.md:90-113,166,23`.
- Stress→felt reframe pattern (worked example): `stress_felt_curve/findings.md` (whole).
- Site placeholder shapes (read-only): `site/data/charts/walls-of-orange.json`,
  `site/data/charts/felt-state-timeline.json`; asset specs
  `site/assets/ASSETS-NEEDED.md:12-18`.

*End of export. Producer-mode, read-only on sources, no re-lock, no audit run, no git,
no write into the site repo, no touch of any locked result.md.*
