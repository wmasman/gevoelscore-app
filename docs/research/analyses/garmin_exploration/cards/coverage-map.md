# Measurement-regime coverage map (R17) — per-signal coverage window + artifact-risk

**Producer-mode assembly artefact.** Assembled 2026-06-30 for Wiggers-site request R17.
Derivative read-over already-documented provenance — **no new extraction, no new test, no
re-lock, no audit, no git**. Read-only on all source MDs. Does NOT touch any locked
`result.md`.

**What this is.** For every scorecard signal (and the structurally-relevant blocked /
proxy channels), the coverage window and any cutover / availability date, so the site can
flag where an apparent over-time difference is a **DATA-AVAILABILITY artifact, not a body
change**. This is the map that separates FAKE time-variation from real: it underpins the
measurement-regime driver in the ledger (R15) and the HA10 / H04 caveats from R18.

**Load-bearing distinction.** Signals split cleanly into two regimes:

- **Full-coverage daily UDS (no artifact risk)** — daily pre-computed aggregates that
  Garmin emitted for the whole `2021-08-16 → present` dump. An over-time difference in
  these is a body/behaviour change, not an availability artifact. `resting_hr`, the BB
  daily anchors (`bb_highest` / `bb_lowest` / `bb_*`), steps, intensity-minutes are here.
- **Resolution / coverage cutover (artifact risk)** — channels whose underlying data
  rolled out mid-corpus on this FR245. An apparent "this got worse/better over time"
  difference can be the cutover, not the body. Per-minute sleep BB, `bb_overnight_gain`
  truth, and (degenerately, never available) literal HRV are here.

---

## 0. Framing rules this map obeys (do not strip on re-use)

1. **Two device-wide invariants frame everything.** Single watch, single firmware family:
   one FR245 (serial 3377851255, product `fr245`) worn continuously
   `2021-08-16 → present`, verified across all 21,219 FIT files
   (`bb_overnight_gain_proxy.md:61`). And: the FR245 / Elevate V3 sensor **never produces
   nightly HRV** — not extracted, not raw, not derivable
   (`garmin_indicators_audit.md:198-227`, `hrv_proxy_via_stress.md:100-115`).
2. **Cutover ≠ analysis boundary, but must be checked against it.** A cutover that
   co-locates with an analysis boundary (e.g. a phase split) is where artifact and real
   change are confounded; the `note` field states co-location explicitly.
3. **The R18 HA10 / H04 correction is reflected, not re-decided.** HA10 and H04 ride the
   **full-coverage daily UDS BB anchors** (`bb_highest` etc.), NOT the per-minute cliff.
   They were corrected in R18 to full-coverage UDS; this map carries `artifact-risk: NO`
   for them and cites the 98.2% coverage figure (§3).

---

## 1. Proposed export shape for the site

Per-signal record:

```
{
  signal: string,            // scorecard channel id / construct
  coverage_from: "YYYY-MM-DD" | "full" ("full" = 2021-08-16 dump start),
  coverage_to?: "YYYY-MM-DD", // present/open if omitted
  regime: "full_uds" | "cutover" | "blocked",
  artifact_risk: "yes" | "no",
  note: string               // the cutover/availability fact + whether it
                             // co-locates with an analysis boundary
}
```

`artifact_risk` is the single field the site reads to decide whether an over-time delta on
that signal may be a data-availability artifact. `full_uds` ⇒ `no`; `cutover` /
`blocked` ⇒ `yes` (a blocked channel's "time variation" is entirely a rollout artifact
because there is no body signal underneath at all before the cutover).

---

## 2. Per-signal coverage table

Analysis-window anchors used in the `note` column (verified, cited §4):

- **Single pool / Stratum-4 start**: 2022-09-03 (`registry.md:22-23,33`).
- **Retired train/validate split boundary**: 2023-12-31 (`registry.md:22-23`).
- **Citalopram buildup→consolidation boundary**: ~2024-06-20
  (`bb_overnight_gain_proxy.md:9`); broader citalopram phase ~2024-04-09 onward.

| signal | construct | coverage_from | coverage_to | regime | artifact-risk | note |
|---|---|---|---|---|:--:|---|
| **resting_hr** (HA06b) | RHR z-score (bidir) | 2021-08-16 (full) | present | full_uds | **NO** | Garmin UDS algorithmic RHR, passthrough; observed full-window range 47–65 bpm, 0 outliers in 1731 days (`garmin_indicators_audit.md:92`). No cutover; spans both analysis boundaries cleanly. |
| **bb_highest / morning BB peak** (HA10) | morning BB peak z (bidir) | 2021-08-16 (full) | present | full_uds | **NO** | Daily UDS `HIGHEST` anchor, full corpus. **98.2% coverage** (1670 / ~1700 days), 62 daytime-peak exclusions = 3.6% (`HA10-bb-overnight-recharge/result.md:221-224`). **NOT the per-minute cliff** (§3, R18 correction). |
| **exertion class** (HA01b) | exertion-class lead-up | 2021-08-16 (full) | present | full_uds | **NO** | `effective_exertion` + step features; 2022Q3 gap **resolved** 2026-06-12, now 100% fill from 2021Q3 (`ANALYSIS_START` extended 2022-09-03→2021-08-16) (`garmin_indicators_audit.md:103-104`). v3.1 rolling-baseline values for 2022-09-23→2022-10-22 shifted on re-extract; not an availability cutover, a baseline-recompute (note for reproducibility only). |
| **sleep stress mean delta** (HA07c) | sleep-window mean stress | 2021-08-16 (full) | present | full_uds | **NO** | `stress_mean_sleep`, FIT-derived from sleep type-49 monitoring_b across full corpus (`garmin_indicators_audit.md:112`). Per-night validity gate (≥120 samples) drops watch-off nights silently, but this is per-night missingness, not a dated cutover — no over-time regime shift. |
| **sleep stress stdev delta** (HA07d) | sleep-stress variability (stdev, bidir) | 2021-08-16 (full) | present | full_uds | **NO** | `stress_stdev_sleep`, same extraction + same per-night gate as HA07c (`garmin_indicators_audit.md:113`). The only single-pool SUPPORTED scorecard signal; full-coverage, no artifact risk. |
| **per-minute stress-spike count** (H02b) | spike count (stress ≥75, ≥5 min, 3d) | 2021-08-16 (full) | present | full_uds | **NO** | `max_spike_minutes` from per-minute stress in FIT monitoring_b, full corpus (`garmin_indicators_audit.md:120`). Per-minute *stress* is in the FIT dump for the whole window — distinct from per-minute *BB*, which is not. Days <60 samples flagged invalid (per-day, not dated). |
| **within-day U-dip count** (HA11) | within-day stress U-dip count | 2021-08-16 (full) | present | full_uds | **NO** | Derived from the same full-corpus per-minute stress trace as H02b; no BB-cliff dependency. |
| **bb_overnight_gain (truth)** | SLEEPEND − SLEEPSTART overnight charge | 2024-09-18 | present | cutover | **YES** | Two-stage UDS rollout on this FR245: `SLEEPSTART` first emitted **2024-07-08**, `SLEEPEND` first emitted **2024-09-18** (`bb_overnight_gain_proxy.md:9,121-122`). 593/1755 days = 33.8% coverage. Pre-2024 absence is structural: 0 days. **Co-locates with the ~2024-06-20 citalopram boundary** (`n_pre=0, n_post=0` on truth channel) — any apparent citalopram-era BB-gain change on the truth channel is an availability artifact, not a body effect. |
| **bb_overnight_gain_best (truth+proxy)** | fused: truth, else `HIGHEST−SLEEPSTART` proxy | 2024-07-08 | present | cutover | **YES** | Proxy hard-floored at **2024-07-08** by construction; NaN before, do not impute (`bb_overnight_gain_proxy.md:77,122-124`). Buys +74 days (71 bridge 2024-07-08→2024-09-17 + 3 SLEEPEND-failure nights). Still pre-2024 blank. Same citalopram-boundary co-location caveat. Proxy-source rows must be disclosed per-analysis (`bb_overnight_gain_proxy.md:71`). |
| **per-minute sleep BB** (H03b / H04b) | per-3-min BB during sleep (integral) | 2024-06-03 | present | cutover | **YES** | `sleepBodyBattery` per-3-min array empty before **~2024-06-03**; `bodyBatteryChange` daily scalar None before **~2023-12-31** (`H03b…/result.md:14-17,33-40,72-77`). 716 valid days, ~97% within 2024-06-03→2026-06-05. **The 2023-12-31 scalar cutover co-locates EXACTLY with the retired train/validate boundary** — H03b train-era coverage is zero, validate only 6 clean episodes → INCONCLUSIVE×12. This is the canonical per-minute BB cliff. **Not in the scorecard** (INCONCLUSIVE, no card); listed because it is the channel HA10 is repeatedly mistaken for. |
| **literal HRV** (HA07/HA08, B1–B5) | nightly HRV Status / RMSSD | — | — | blocked | **YES** | **Hardware-blocked, never available on any date.** FR245 / Elevate V3 produces no nightly HRV — not raw, not derivable (`garmin_indicators_audit.md:198-227`; `hrv_proxy_via_stress.md:100-115`; `registry.md:1064-1066`). Any "HRV over time" is 100% a non-existence artifact. Substantive autonomic claims ride the `stress_mean_sleep` proxy (= HA07c/HA07d), which IS full-coverage. A device upgrade would unblock HRV from the upgrade date forward only. |

---

## 3. The R18 HA10 / H04 correction — reflected here

The single most important thing this map must get right: **HA10 and H04 do NOT ride the
per-minute BB cliff.** They were CORRECTED in R18 to the full-coverage daily UDS BB
anchors, and this map carries them as `artifact-risk: NO`.

- **HA10** operationalises morning BB peak from the **daily UDS `HIGHEST` anchor**, present
  for the full corpus at **98.2% coverage** (1670 / ~1700 days)
  (`HA10-bb-overnight-recharge/result.md:214,221-224`). It is explicitly a "3-anchor coarse
  proxy" using HIGHEST/LOWEST/MOSTRECENT, NOT the per-minute trajectory
  (`HA10-bb-overnight-recharge/result.md:214-217`; `H03b…/result.md:103-114`).
- The **per-minute cliff** (≈2024-06-03 array rollout / 2023-12-31 scalar rollout) belongs
  to **H03b / H04b** — a *different, sharpening* test that returned INCONCLUSIVE precisely
  because it depends on the post-cutover per-minute array (`H03b…/result.md:7-27`). H03b
  does NOT contaminate HA10; HA10 "stays as the canonical BB overnight recharge finding"
  on full-coverage anchors (`H03b…/result.md:101-124`).
- **H04** (BB net delta, refuted both eras — `REJECTED.md:43`) likewise rides the daily BB
  anchors, not the per-minute array.

**Therefore:** an over-time difference in HA10's or H04's BB signal is a body/behaviour
difference, NOT a per-minute-availability artifact. Do not let the per-minute cliff's
2024 cutover be attributed to HA10/H04. Only the per-minute-dependent channels
(`bb_overnight_gain` truth/best, H03b/H04b per-minute) carry the cutover.

---

## 4. Co-location summary — where cutover meets an analysis boundary

| cutover date | what rolls over | co-located analysis boundary? | consequence |
|---|---|---|---|
| **2023-12-31** | `bodyBatteryChange` daily scalar populated (`H03b…/result.md:14`) | **YES — exactly the retired train/validate split** (`registry.md:22-23`) | per-minute-dependent BB analyses have ZERO train coverage; pre-split vs post-split BB-gain contrasts are confounded with availability. |
| **2024-06-03** | `sleepBodyBattery` per-3-min array populated (`H03b…/result.md:15`) | near the ~2024-06-20 citalopram boundary | per-minute BB sharpening (H03b) impossible pre-citalopram; train-era zero. |
| **2024-07-08** | UDS `SLEEPSTART` emitted (`bb_overnight_gain_proxy.md:9`) | just before ~2024-06-20 citalopram boundary | proxy `bb_overnight_gain_best` floor; pre-boundary truth = 0 days. |
| **2024-09-18** | UDS `SLEEPEND` emitted (`bb_overnight_gain_proxy.md:9`) | post ~2024-06-20 citalopram boundary | `bb_overnight_gain` truth `n_pre=0, n_post=0` at the citalopram boundary (`bb_overnight_gain_proxy.md:9`). |
| **(none)** | full-coverage UDS: `resting_hr`, `bb_highest`, exertion, sleep-stress mean/stdev, per-minute *stress* | — | span 2022-09-03 Stratum-4 start and 2023-12-31 split cleanly; **no artifact risk**. |

The full-coverage daily UDS channels (Stratum-4 start 2022-09-03 onward all populated)
carry **no** measurement-regime confound across either analysis boundary. Every scorecard
signal except none — all 7 scorecard signals — sits in the full-coverage regime. The
cutover/blocked channels are exactly the per-minute-BB and literal-HRV families, none of
which are single-pool scorecard verdicts.

---

## 5. Source citations (file:line)

- Single watch / firmware invariant: `bb_overnight_gain_proxy.md:61`.
- HRV hardware block (FR245 / Elevate V3, never available): `garmin_indicators_audit.md:198-227`;
  `hrv_proxy_via_stress.md:100-115`; `registry.md:1064-1066`.
- `resting_hr` full-window provenance + 47–65 bpm range: `garmin_indicators_audit.md:92`.
- HA10 daily-anchor (HIGHEST) BB peak + 98.2% coverage + 3-anchor coarse proxy:
  `HA10-bb-overnight-recharge/result.md:214-224`.
- Exertion 2022Q3 gap resolved / 100% fill from 2021Q3: `garmin_indicators_audit.md:103-104`.
- Sleep-stress mean (`stress_mean_sleep`) + stdev provenance + per-night gate:
  `garmin_indicators_audit.md:112-113`.
- Per-minute stress spike (`max_spike_minutes`) full-corpus FIT: `garmin_indicators_audit.md:120`.
- `bb_overnight_gain` two-stage UDS rollout (SLEEPSTART 2024-07-08, SLEEPEND 2024-09-18),
  citalopram-boundary `n_pre=0/n_post=0`, coverage 33.8%, proxy floor + 74-day gain +
  proxy-disclosure rule: `bb_overnight_gain_proxy.md:9,71,77,121-124`.
- Per-minute BB cutovers (`bodyBatteryChange` ~2023-12-31, `sleepBodyBattery` ~2024-06-03),
  train zero-coverage, INCONCLUSIVE×12, HA10 stays canonical: `H03b…/result.md:7-27,33-40,72-77,101-124`.
- Stratum-4 start 2022-09-03, retired train/validate boundary 2023-12-31:
  `registry.md:22-23,33`.
- H04 BB net delta refuted: `REJECTED.md:43`.
- Citalopram buildup→consolidation boundary ~2024-06-20: `bb_overnight_gain_proxy.md:9`.

*End of map. Producer-mode, read-only on sources, no re-lock, no audit run, no git.
Does not write into the site repo and does not touch any locked result.md.*
