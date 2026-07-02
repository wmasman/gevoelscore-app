# Descriptive precondition — COVID peri-event check (R23)

**Status**: producer-mode descriptive precondition, STAGE 1 of the R23
peri-event check (*does the watch's autonomic factor visibly move during
the ~14-day COVID infection?*). This artefact characterises **event
location, factor definition, data coverage, and the comparison design
space** so the pre-registration can lock with the outcome unseen. It is
Layer-1 descriptive: **no causal or interpretive marks** per
[CONVENTIONS §4.1](../../../CONVENTIONS.md). Drafted 2026-06-30 by
Claude (Opus 4.8) under producer-mode authorization, the
participant-researcher (repo owner). Companion to the proposed methodology MD
[`../../../methodology/peri_event_known_event_check.md`](../../../methodology/peri_event_known_event_check.md).

> ## NO-OUTCOME-PEEK STATEMENT (binding)
>
> R23 is a **pre-registered single-event test**. Pre-registration is
> only credible if the outcome is unseen when the design locks. This
> precondition characterises **only**: the event dates, the window
> length, data coverage / missingness in the window, whether the factor
> is computable there, the factor definition, and the set of candidate
> comparison ("ordinary") windows + their count. It does **NOT** compute,
> estimate, plot, or infer whether the autonomic factor actually moved
> during the infection vs baseline. **No biometric values, means,
> trends, z-scores, or infection-vs-baseline contrasts were inspected or
> computed in producing this document.** The infection-vs-baseline
> contrast IS the test; it runs only after the pre-reg locks (per
> [`_plan_results_analysis_layer.md`](../../../methodology/_plan_results_analysis_layer.md)
> §3.5 hard rule + [CONVENTIONS §1.2](../../../CONVENTIONS.md)). Every
> coverage number below is a **row-presence / non-null day count** —
> never a channel value.

---

## 1. Event location

**Confirmed single COVID infection event.**

| Source | Entry | Dates |
|---|---|---|
| [CONVENTIONS §5](../../../CONVENTIONS.md) anchor | corona infection span | **2022-03-21 → 2022-04-03** (14 days inclusive) |
| `annotations.yaml` (`raw/directus_exports/`) | `label: Corona-infectie`, `category: trigger`, note: *"Een aantal dagen op bed met koorts. Donderdag 31-03 voelt over de infectie heen. Trigger voor long-covid onset. Bevestigd door 0 training-activities in week 12."* | core symptom window **2022-03-23 → 2022-03-30** |
| `annotations.yaml` supporting marker | `Eerste ziektedag ketenverzuim` | 2022-03-28 |
| `annotations.yaml` supporting context | `Training-periode ... voorbereiding Ardennen`; week 12 (21-27 mrt) = 0 training minutes, consistent with corona-ziek-week | 2022-03-16 → 2022-03-22 |

- **Window length**: 14 days (2022-03-21 → 2022-04-03 inclusive). Confirmed.
- **Era**: the window carries `lc_phase == corona_infection` — **Stratum 2
  (acute corona infection)** per
  [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md)
  and [`research_line_limitations.md`](../../../methodology/research_line_limitations.md)
  L2. It sits at the **Stratum-1 (pre-corona healthy) → Stratum-2
  (acute infection) hard boundary**, immediately before the
  Stratum-2→Stratum-3 (LC) boundary at 2022-04-04. The era is
  **corona-transition, Garmin-only** (pre-gevoelscore; gevoelscore
  logging starts 2022-09-03).
- **Single event**: a search of `annotations.yaml` / event_labels for
  reinfection / second-infection terms (`herinfect`, `reinfect`,
  `tweede`, later-year infection) returned **no matches**. This COVID
  infection is the **single independently-known autonomic event** in
  the corpus — independently dated from contemporaneous notes
  (bed-with-fever + 0 training activities), not derived from the
  biometrics. No reinfection event exists to report.

## 2. Factor definition resolution

**The "autonomic factor" is the cross-channel "autonomic-state"
cluster** defined in
[`../../garmin_exploration/cards/cross-channel-correlation.md`](../../garmin_exploration/cards/cross-channel-correlation.md)
(computed 2026-06-08). It is a **structural / correlational collapse**
(channels that move together because they share an autonomic cause;
effective-N ≈ 1 for the cluster) — **NOT a PCA first principal
component, NOT a named weighted composite, NOT a variance-decomposition
construct.** No variance-explained percentage is defined; the factor is
the correlational near-identity of the channels.

**Core triad (Cluster 2, site label "overnight autonomic state"):**

| Role | Channel | Primitive | Relation to anchor (verbatim ρ) |
|---|---|---|---|
| Primary anchor | HA07c | `sleep_stress_mean` | — |
| Redundant (inverse) | HA10 | `morning_bb_peak` | Spearman ρ = **−0.922** (structural in Garmin's BB algorithm) |
| Peripheral | HA06b | `resting_hr` | ρ = **+0.377** to HA07c; **−0.393** to HA10 |

(HA07d `sleep_stress_stdev`, ρ=+0.50 to HA07c, and HA08c, a slope of the
same primitive, are adjacent cluster members; the core is the triad.)

### 2.1 Definition discrepancy — flagged

The R23 register states the factor is from `cohort_topology/findings.md`.
**This is incorrect.**
[`../trajectory/cohort_topology/findings.md`](../trajectory/cohort_topology/findings.md)
is **event-topology + recovery-window work** (29 crashes + 79 dips,
per-channel recovery trajectories, matched-control baselines) — it
characterises crash/dip *geometry*, **not** an inter-signal factor. The
factor's only source is the cross-channel card above.
[`../../garmin_exploration/cards/clusters-export.md`](../../garmin_exploration/cards/clusters-export.md)
already records this correction verbatim: *"cohort_topology/findings.md
is event-topology + recovery-window work (crash/dip geometry), NOT the
inter-signal factor definition. There is no separate cohort_topology
factor doc to fold in; the cross-channel card is the whole factor
substrate."* The earlier check that flagged cohort_topology as
recovery-work was **correct**. The pre-reg must cite the cross-channel
card as the factor source. The choice of operationalisation (single
HA07c anchor vs triad-coherence readout) is surfaced as decision (g) in
the methodology MD §5.

**Guardrail**: "stress" here = **Garmin HRV-derived GSS** (Firstbeat),
not mental stress. The FR245 has no direct HRV (L3); the factor recovers
the autonomic signal through the overnight-stress / body-battery / RHR
triad per [`hrv_proxy_via_stress.md`](../../../methodology/hrv_proxy_via_stress.md).

## 3. Coverage / computability in the infection window (row presence only)

**Source**: `per_day_master.csv` at
`C:\Users\Gebruiker\Documents\gevoelscore-data\unified\per_day_master.csv`;
`lc_phase` column present with `corona_infection` value across the
transition. All numbers below are **non-null day counts** — no values
inspected.

**Infection window 2022-03-21 → 2022-04-03 (14 days):**

| Factor component / proxy channel | Column | Days with non-null row |
|---|---|---|
| Resting HR (HA06b) | `resting_hr` | 14 / 14 |
| Overnight stress (HA07c proxy) | `all_day_stress_max` (raw stress channel) | 14 / 14 |
| Body-battery (HA10 proxy) | `bb_highest` (raw BB channel) | 14 / 14 |
| Respiration (context channel) | `respiration_max_24h` | 14 / 14 |

**March 2022**: 31/31 days present on all four channels. **April 2022**:
30/30 days present on all four channels.

**Computability verdict**: the factor's component **channels are
present for every day of the infection window** — the factor is
computable across the window at the raw-channel level. **The exact
overnight primitive was subsequently confirmed** (see §5.1): the HA07c
anchor's real column is `stress_mean_sleep` (14/14 in the window), and
HA10's operand is the daily `bb_highest` (14/14); `resting_hr` (HA06b)
is likewise 14/14. All three factor components are non-null on every
infection-window day at the exact-primitive level.

## 4. Comparison design space (counts only)

**Pre-LC healthy era (the only legitimate "ordinary" comparator)**:
2021-08-16 (GDPR-dump start / Stratum-1 start) → 2022-03-20 (last
pre-corona day). Span = **217 days**, `lc_phase == pre_corona`
(Stratum 1). Post-infection days are LC-era and **not interchangeable**
with healthy baseline per the L2 HARD-BOUNDARY rule, so the comparator
band is Stratum 1 only.

| Quantity | Count |
|---|---|
| Candidate **non-overlapping** 14-day windows in pre-LC era | **15** (217 ÷ 14 = 15 full + 7-day remainder) |
| Candidate **sliding** 14-day windows (step 1 day) | **204** (217 − 14 + 1) |

**Pre-LC per-channel coverage density** (row presence over 217 days):

| Channel | Days present | Density |
|---|---|---|
| `resting_hr` | 217 / 217 | 100.0% |
| `all_day_stress_max` | 217 / 217 | 100.0% |
| `respiration_max_24h` | 216 / 217 | 99.5% (1 day missing) |
| `bb_highest` | 216 / 217 | 99.5% (1 day missing) |

**Design-space verdict**: essentially **all 15 non-overlapping (and all
204 sliding) candidate windows are computable** — coverage is
99.5–100% across the pre-LC band, so the matched-window null is
well-populated. Named per [CONVENTIONS §3.6](../../../CONVENTIONS.md):
*15 independent non-overlapping 14-day pre-LC windows (per_day_master.csv,
`lc_phase == pre_corona`, 2021-08-16 → 2022-03-20)*; 204 sliding windows
over the same band for the richer (autocorrelated) null distribution.

## 5. Open inputs

| # | What is missing | Blocks | Cheapest path | Fallback |
|---|---|---|---|---|
| 1 | ~~Confirm `sleep_stress_mean` (HA07c) + `morning_bb_peak` (HA10) are **non-null in 2022-03**~~ **RESOLVED 2026-07-02** (see §5.1) | ~~Locking HA07c as the factor's primary anchor~~ — anchor locked | non-null count run | — |
| 2 | User lock on methodology decisions (a)–(g) | The pre-registration | Methodology MD §5 + fresh-session `/research-methodology-review` | — |

### 5.1 Open-input #1 resolution (2026-07-02, coverage-only)

The exact-primitive columns resolve to real `per_day_master.csv` names:
**HA07c `sleep_stress_mean` → `stress_mean_sleep`** (the sleep-window
stress mean); **HA10 `morning_bb_peak` → `bb_highest`** (HA10's operand
is the daily UDS BB peak per the R18 correction; "morning_bb_peak" was a
descriptive label, not a column). A **presence-only** non-null count
(no values, means, or contrasts inspected — see the binding statement
above) returns:

| Primitive | Infection window (14 d) | March 2022 | Pre-LC comparator band (217 d) |
|---|---|---|---|
| `stress_mean_sleep` (HA07c anchor) | 14 / 14 | 31 / 31 | 215 / 217 (99.1%) |
| `bb_highest` (HA10) | 14 / 14 | 31 / 31 | 216 / 217 (99.5%) |
| `resting_hr` (HA06b) | 14 / 14 | 31 / 31 | 217 / 217 (100%) |

**Anchor lock (contingency g1 satisfied):** `stress_mean_sleep` is
non-null on every infection-window day, so the **primary anchor is HA07c
`stress_mean_sleep`**, with `bb_highest` (redundant inverse) and
`resting_hr` (peripheral) as the companion triad. The pre-specified
HA06b-primary fallback is **not** triggered. The comparator null remains
well-populated (99.1–100% density across the 217-day pre-LC band).

## 6. Cross-references

- [`../../../methodology/peri_event_known_event_check.md`](../../../methodology/peri_event_known_event_check.md)
  — the proposed methodology MD this precondition backs (design space,
  four-input reasoning, the (g) discrepancy decision).
- [`../../garmin_exploration/cards/cross-channel-correlation.md`](../../garmin_exploration/cards/cross-channel-correlation.md)
  — **the factor source** (Cluster 2 autonomic-state triad).
- [`../../garmin_exploration/cards/clusters-export.md`](../../garmin_exploration/cards/clusters-export.md)
  — records the cohort_topology-is-not-the-factor correction.
- [`../trajectory/cohort_topology/findings.md`](../trajectory/cohort_topology/findings.md)
  — event-topology / recovery work (the mis-cited source; adjacent, not
  the factor).
- [CONVENTIONS.md](../../../CONVENTIONS.md) §3.6 (named counts), §4.1
  (no interpretive marks), §4.3 (prior-driven = confirmatory), §5 (LC
  timeline anchor).
- [`research_line_limitations.md`](../../../methodology/research_line_limitations.md)
  L1 / L2 / L3 / L7.
- [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md)
  — Stratum 1 / Stratum 2 boundaries.
