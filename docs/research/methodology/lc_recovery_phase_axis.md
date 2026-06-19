# LC recovery-phase axis — lived-experience + intervention-evidence stratification of Stratum 4

## Authorship

- **Drafted**: 2026-06-19 by Claude (Opus 4.7), in producer-mode per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-helps-the-user-build-the-research-artefact).
- **Authorising user**: user (name redacted for publication-safety per `audit_for_publication.py` discipline).
- **Drafting-session context**: directly follows the `trajectory/recovery_arc/` v1 landing (commit `24dad02`) where the v1 4-phase structure (healthy / acute / lc_pre_gevoelscore / lc_with_gevoelscore) lumped a clinically heterogeneous ~4-year LC era into one bin. User-flagged 2026-06-19 that descriptive work needs a **data-informed + lived-experience-grounded** axis as the canonical substrate, and that the same axis should be **opt-in for HA pre-regs**.
- **Status**: **r2 LOCKED 2026-06-19** per [CONVENTIONS §2.2 + §2.3](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) audit hooks + [`hypothesis_lock_process.md §3.6`](hypothesis_lock_process.md) compression. Dates within phases 3-5 are structurally fixed by canonical sources cited inline; the phase-4-internal habit-formation sub-boundary is locked at 2022-11-17 (8 weeks post-ergotherapie-start) per the §7b operationalisation interview cleared 2026-06-19 (see §3.4a + §3.4b).

---

## Citation status

This MD runs on first-principles methodological reasoning plus established conventions documented in the project's existing methodology MDs ([`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md), [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md), [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md), [`garmin_pacing_practice.md`](garmin_pacing_practice.md)). Project literature anchors already fetched: [Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) (n-of-1 time-varying confounder adjustment, referenced via `citalopram_phase_stratification §1.3`); WWC 2022 + SCRIBE 2016 + Natesan Batley 2023 single-case standards (referenced via `CONVENTIONS.md` §1.2). Candidate ME/CFS + Long COVID pacing literature anchors (Goudsmit 2012 envelope theory; Davis 2021 LC characterisation; Larun 2017 graded exercise critique) are **not** yet fetched into `docs/research/literature/`; the §5 four-input reasoning literature row is honestly downgraded to "deferred" for those anchors. The methodological reasoning stands on its own and does not depend on any specific not-yet-fetched paper.

---

## 1. What this MD is, what it is not

### 1.1 Is

A **canonical phase-axis specification** for sub-stratifying the LC era (Stratum 4 per [`lc_era_temporal_segmentation §1`](lc_era_temporal_segmentation.md#1-data-given-strata-background-not-a-methodological-choice), plus the pre-Stratum-4 LC days 2022-04-04 → 2022-09-02) into clinically + intervention-evidence-meaningful phases. Becomes the default substrate for **descriptive work where phase-stratification is informative**, and **opt-in for HA pre-regs** that have reason to stratify by recovery phase.

Sits **orthogonal to** [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) (medication-state axis): the citalopram axis is a sub-axis of the citalopram-modulated phase here, and the two can be cross-classified for tests that need both dimensions.

### 1.2 Is not

- A hypothesis test or a falsification claim.
- A binding axis for all HA pre-regs — per-pre-reg authors opt in.
- A re-derivation of the data-given LC-era strata ([`lc_era_temporal_segmentation §1`](lc_era_temporal_segmentation.md)). Phases 1 (healthy) + 2 (acute infection) are inherited verbatim from that MD; this MD adds the within-Stratum-4 sub-segmentation that `lc_era_temporal_segmentation.md` declined to default-commit to.
- A replacement for the time-varying-confounder treatment patterns in [`citalopram_phase_stratification.md §5`](citalopram_phase_stratification.md#5-the-three-downstream-test-treatment-patterns). Those patterns (per-phase / dose-adjusted-predictor / per-mg-subtraction) apply at the citalopram axis; this MD adds a higher-level recovery-phase axis above them.
- A methodology MD for the *acute infection → LC transition* (covered by `lc_era_temporal_segmentation §1` data-given event boundary 2022-04-04, "Monday after Fietsweekend Ardennen").

### 1.3 Relationship to existing axes — three layers

| layer | axis | source-of-truth MD | role |
|---|---|---|---|
| Outer | Data-given strata (pre-illness / acute / LC) | [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) §1 | Event-driven boundaries; not a methodological choice |
| **Middle (this MD)** | **LC recovery phase axis** | **THIS MD** | **M1 hypothesis-driven + M2 intervention-evidence sub-segmentation of the LC era** |
| Inner | Citalopram dose-state | [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) §3 | Medication-state sub-axis; nested within the citalopram-modulated phase of THIS MD |

Cross-classification example: a per-day row in Stratum 4 has (a) `lc_phase` = "lc" from the outer axis, (b) `recovery_phase` = (e.g.) "pacing_habit_established" from this MD, and (c) `citalopram_phase` = "unmedicated" from the inner axis. The three axes are factorable.

---

## 2. The proposed phase structure (r1)

**Six phases**: two inherited verbatim from [`lc_era_temporal_segmentation §1`](lc_era_temporal_segmentation.md#1-data-given-strata-background-not-a-methodological-choice) + four new within-LC phases (phase 4 splits into sub-phases 4a + 4b per the §7b operationalisation lock 2026-06-19).

| # | phase name (canonical kebab-case) | window | duration | warrant class | data scope |
|---|---|---|---:|---|---|
| 1 | `pre_illness_healthy` | 2021-08-16 → 2022-03-20 | ~217 days | data-given (Garmin extract start; COVID onset eve) | Garmin only |
| 2 | `acute_infection` | 2022-03-21 → 2022-04-03 | 14 days | data-given (PCR-positive; "Monday after Fietsweekend Ardennen") | Garmin only |
| 3 | `lc_pre_ergo` | 2022-04-04 → 2022-09-22 | ~171 days | **M1 lived-experience** (no pacing; no intervention; chronic patterns crystallising) | Garmin only (gevoelscore from 2022-09-03 → partial: last 19 days have gevoelscore) |
| 4a | `pacing_pre_citalopram_learning` | 2022-09-22 → 2022-11-17 | 56 days (8 weeks) | **M1 lived-experience** (ergotherapy onboarding + habit formation; CLEARED §7b 2026-06-19) | Garmin + gevoelscore (full); overlaps ergotherapie 2022-09-22 → 2022-12-22 partial |
| 4b | `pacing_habit_established` | 2022-11-17 → 2024-04-09 | ~508 days | **M1 lived-experience** (pacing habit established; effectiveness still mediated by outside forces; CLEARED §7b 2026-06-19) | Garmin + gevoelscore (full); ergotherapie tail 2022-11-17 → 2022-12-22; CPAP 2024-01-10 → 2024-04-16 overlaps tail |
| 5 | `citalopram_modulated` | 2024-04-09 → 2026-06-04 | ~787 days | **M2 documented confounder** ([`citalopram_dose_response §5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) confirmed dose-modulation on 3 channels) | Garmin + gevoelscore; sub-axis = citalopram phase ([`citalopram_phase_stratification §3`](citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)) |

**Note on phase 4 sub-phases (CLEARED 2026-06-19 at r2 lock)**: the §7b operationalisation interview (Strand B discipline per [`descriptive/README §7b`](../analyses/descriptive/README.md#7b-strand-b-operationalisation-interview-r3-added-2026-06-18)) was completed 2026-06-19 in a user session. The locked operationalisation: **8-week post-ergotherapie-start duration anchor** splits phase 4 into `pacing_pre_citalopram_learning` (4a; 2022-09-22 → 2022-11-17) and `pacing_habit_established` (4b; 2022-11-17 → 2024-04-09). The 4b naming (replacing the r1 working name `pacing_effective`) is more precise: habit-established ≠ effectiveness-achieved, with pacing effectiveness still mediated by outside forces per the user's lived-experience report. The per-sub-phase warrants live at §3.4a + §3.4b. Falsifiability hook: the 8-week boundary's discriminative power on per-sub-phase channel medians is itself testable in descriptive Layer 1 (e.g. as a recovery_arc v2 sensitivity arm; no causal claim).

**Note on phase 5 sub-axis**: within phase 5 the [`citalopram_phase_stratification.md §3`](citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification) 4-phase sub-axis (unmedicated [absent in phase 5 by construction] / buildup / consolidation / afbouw / post_afbouw) applies. For descriptive work where citalopram sub-structure matters, use the cross-classification `(recovery_phase=citalopram_modulated, citalopram_phase=*)`. The afbouw sub-phase is the right edge of phase 5 (2026-03-20 → 2026-06-05, 78 days, inclusive); the post_afbouw sub-phase begins 2026-06-06 per the `citalopram_phase()` helper in `citalopram_phase_stratification §3` and is currently OUT-OF-CORPUS (Garmin data ends 2026-06-04 per [STOCKTAKE §1](../STOCKTAKE.md#1-the-corpus)) so this MD does NOT add a phase 6 for it.

### 2.1 Computing the phase for an arbitrary date `d` (canonical helper)

```python
from datetime import date

def lc_recovery_phase(d: date) -> str:
    """Per lc_recovery_phase_axis.md §2. r2 LOCKED 2026-06-19."""
    if d < date(2022, 3, 21):
        return "pre_illness_healthy"
    if d < date(2022, 4, 4):
        return "acute_infection"
    if d < date(2022, 9, 22):
        return "lc_pre_ergo"
    if d < date(2022, 11, 17):
        return "pacing_pre_citalopram_learning"
    if d < date(2024, 4, 9):
        return "pacing_habit_established"
    # Phase 5 — citalopram_modulated; sub-axis via citalopram_phase() per
    # citalopram_phase_stratification.md §3
    return "citalopram_modulated"
```

---

## 3. Per-phase warrants

### 3.1 Phase 1 — `pre_illness_healthy` (inherited)

**Warrant**: data-given. Inherited verbatim from [`lc_era_temporal_segmentation §1`](lc_era_temporal_segmentation.md#1-data-given-strata-background-not-a-methodological-choice). No methodological choice — the Garmin extract starts 2021-08-16; COVID infection is 2022-03-21.

**Boundary endpoints**:
- Left: 2021-08-16 (Garmin extract start, inherited from `lc_era_temporal_segmentation §1`).
- Right: 2022-03-20 (eve of COVID infection).
- **n_days**: ~217 days.

### 3.2 Phase 2 — `acute_infection` (inherited)

**Warrant**: data-given. Same inheritance. Boundaries documented at [`lc_era_temporal_segmentation §1`](lc_era_temporal_segmentation.md): "Monday after Fietsweekend Ardennen" anchors the LC start at 2022-04-04.

**Boundary endpoints**:
- Left: 2022-03-21 (PCR-positive; COVID infection start per `lc_era_temporal_segmentation §1`).
- Right: 2022-04-03 (eve of LC start).
- **n_days**: 14 days.

### 3.3 Phase 3 — `lc_pre_ergo` (NEW — M1 lived-experience warrant)

**Warrant class**: M1 per [`lc_era_temporal_segmentation §2`](lc_era_temporal_segmentation.md#2-the-methodological-question) — "a specific hypothesis predicts a change-point" where the hypothesis is independently motivated and pre-registered.

**Warrant body**: This phase covers LC days **before pacing as a practice was learned** and **before any external intervention** (ergotherapie, CPAP, citalopram). Per [`garmin_pacing_practice.md §2 Origins`](garmin_pacing_practice.md#2-origins): pacing as a framework came from ergotherapie ("standard Dutch ergo-PEM track early in the LC course"); specific Garmin thresholds emerged over years of trial-and-error. Per [`garmin_pacing_practice.md temporal-qualifier`](garmin_pacing_practice.md#temporal-qualifier--this-protocol-is-a-recent-stabilisation-not-a-constant): "the protocol was not in place from the start of LC. It emerged and evolved over time." This phase is the **pre-protocol period** where acute symptoms developed into chronic patterns absent any operationalised pacing or external intervention. The user's lived-experience description (2026-06-19): "the phase where i found out that the acute symptoms developed into chronic patterns".

**Boundary endpoints**:
- Left: 2022-04-04 (LC start, inherited from `lc_era_temporal_segmentation §1`).
- Right: 2022-09-22 (Ergotherapie Rouschop start per [`intervention_effects_descriptive §3`](intervention_effects_descriptive.md#3-baseline-channel-step-change-check)). This is the canonical pacing-onset date because ergotherapie supplied the pacing framework per `garmin_pacing_practice §2`.
- **n_days**: ~171 days.

**Per-test usage hint**: descriptive analyses use phase 3 as the **untreated chronic-patterns-crystallising reference** for any "did intervention X alter trajectory" question.

### 3.4 Phase 4 — pacing (pre-citalopram era), split into sub-phases 4a + 4b via §7b operationalisation (M1 lived-experience)

**Warrant class**: M1 per `lc_era_temporal_segmentation §2`.

**Warrant body (parent)**: This phase covers LC days **with pacing practice active but pre-medication**. Pacing began with ergotherapie 2022-09-22; ergo ended ~2022-12-22 (~13 weeks, end-date approximate per `intervention_effects_descriptive §3`); pacing practice continued and evolved past the formal ergo programme through ~564 days of pre-medication LC. CPAP-interventie (2024-01-10 → 2024-04-16) sits in the tail of this phase but is not a phase boundary because per [`intervention_effects §8.3`](intervention_effects_descriptive.md#83-reading-per-the-5-decision-framework) "no corpus-wide M2 boundary is supported" for CPAP across channels — CPAP is an event-overlay, not a phase boundary. The §7b operationalisation interview (CLEARED 2026-06-19 in user session) splits phase 4 into two sub-phases per the user's lived-experience boundary at 8 weeks post-ergotherapie-start: sub-phase 4a (`pacing_pre_citalopram_learning`) covers ergotherapy onboarding + habit formation; sub-phase 4b (`pacing_habit_established`) covers the post-onboarding period through citalopram buildup. M1 lived-experience boundaries are event-anchored to the lived-experience report itself per the §5.1 M1 carve-out (the date is calculated from a documented anchor event + a duration named in the lived report; this is distinct from data-driven boundary detection on channel time series).

**Boundary endpoints (parent, union of 4a + 4b)**:
- Left: 2022-09-22 (Ergotherapie start; canonical pacing-onset).
- Right: 2024-04-09 (Citalopram buildup start per `citalopram_phase_stratification §3`).
- **n_days**: ~564 days (combined 4a + 4b).

**Per-test usage hint (parent)**: descriptive analyses use phase 4 as the **pacing-active, pre-medication** reference. For HA tests on autonomic-load channels affected by citalopram, phase 4 is a methodologically clean unmedicated-with-pacing window where the dose-confounder is zero by construction. Sub-phases 4a + 4b enable finer pacing-learning-vs-habit-established stratification when the question warrants it.

#### 3.4a Sub-phase 4a — `pacing_pre_citalopram_learning` (NEW r2 — M1 lived-experience warrant)

**Warrant class**: M1 per `lc_era_temporal_segmentation §2`. Operationalised via §7b interview 2026-06-19; M1 boundary is event-anchored to the lived-experience report itself per the §5.1 M1 carve-out.

**Warrant body (user verbatim, 2026-06-19)**: *"8 weeks of ergotherapy where I learned the basic principles and got into the habit; gradual improvement during this window"*.

**Boundary endpoints**:
- Left: 2022-09-22 (Ergotherapie start; canonical pacing-onset).
- Right: 2022-11-17 (Ergotherapie start + 56 days; 8-week habit-formation duration per the §7b operationalisation rule).
- **n_days**: 56 days (8 weeks).

**Per-test usage hint**: descriptive analyses use sub-phase 4a as the **pacing-learning, ergo-onboarding** reference; overlaps the formal ergotherapie Rouschop programme (which extends through 2022-12-22, overlapping into the early part of 4b).

**Falsifiability hook (descriptive Layer 1, no causal claim)**: per the §7b operationalisation, the 8-week boundary's discriminative power on per-sub-phase channel medians is itself testable in descriptive Layer 1 (e.g. as a recovery_arc v2 sensitivity arm). A "fails to discriminate" finding would invite a §7b re-interview or sub-boundary withdrawal under a v2 amendment.

#### 3.4b Sub-phase 4b — `pacing_habit_established` (NEW r2 — M1 lived-experience warrant)

**Warrant class**: M1 per `lc_era_temporal_segmentation §2`. Operationalised via §7b interview 2026-06-19. The `pacing_habit_established` naming (replacing the r1 working name `pacing_effective`) is more precise: habit-established ≠ effectiveness-achieved; pacing effectiveness remains mediated by outside forces (e.g. workload demands, season, illness, ergo programme tail), but the overall habit was established per the user's lived report.

**Warrant body (user verbatim, 2026-06-19)**: *"After 8 weeks, pacing got into a rhythm (still mediated in effectiveness by outside forces, but the overall habit was established)"*.

**Boundary endpoints**:
- Left: 2022-11-17 (Ergotherapie start + 56 days; 8-week habit-formation duration).
- Right: 2024-04-09 (Citalopram buildup start per `citalopram_phase_stratification §3`).
- **n_days**: ~508 days.

**Per-test usage hint**: descriptive analyses use sub-phase 4b as the **pacing-habit-established, pre-medication** reference. The CPAP-interventie 2024-01-10 → 2024-04-16 overlaps this sub-phase's tail; per §3.6 the last 7 days of sub-phase 4b contain the CPAP-end event (collision with the phase-4b → phase-5 boundary at 2024-04-09). Ergotherapie tail 2022-11-17 → 2022-12-22 overlaps this sub-phase's left edge.

### 3.5 Phase 5 — `citalopram_modulated` (NEW — M2 documented confounder warrant)

**Warrant class**: M2 per `lc_era_temporal_segmentation §2` — "a documented confounder or data-quality regime".

**Warrant body**: Citalopram is **empirically confirmed to modulate ≥3 autonomic-load + recovery channels** per [`citalopram_dose_response_stress_mean_sleep.md §5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14): `stress_mean_sleep` β=+0.43/mg (p=0.001), `all_day_stress_avg` β=+0.57/mg (p=0.000), `bb_lowest` β=−1.13/mg (p=0.000). Per [`citalopram_phase_stratification.md §4-§5`](citalopram_phase_stratification.md#4-per-channel-inheritance-rules): tests on these load-bearing CONFIRMED channels MUST adopt one of the §5.A / §5.B / §5.C treatment patterns when spanning more than one citalopram phase. This MD's phase 5 *contains* the entire citalopram axis as a sub-stratification, exposing the M2 confounder structurally.

**Boundary endpoints**:
- Left: 2024-04-09 (Citalopram buildup start per `citalopram_phase_stratification §3`).
- Right: 2026-06-04 (corpus end per `STOCKTAKE §1`; post-afbouw begins 2026-06-06 per `citalopram_phase_stratification §3` and is currently out-of-corpus).
- **n_days**: ~787 days.

**Sub-axis**: the 4-phase citalopram axis (`unmedicated` is absent within phase 5; `buildup` 2024-04-09 → 2024-06-19; `consolidation` 2024-06-20 → 2026-03-19; `afbouw` 2026-03-20 → 2026-06-05 (inclusive); `post_afbouw` 2026-06-06 → present per `citalopram_phase()` in `citalopram_phase_stratification §3`, currently empty in the corpus) applies as the inner axis per §1.3 layering.

**Per-test usage hint**: see §6 for the phase-stratify vs detrend tradeoff.

### 3.6 The 2024-04 boundary-collision is inherited

The 7-day proximity of Citalopram buildup start (2024-04-09) + CPAP end (2024-04-16) is documented at [`intervention_effects §2b + §8.1`](intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain). This MD's phase-4/phase-5 boundary sits at 2024-04-09 (citalopram), making the last 7 days of phase 4 (specifically sub-phase 4b `pacing_habit_established`) contain the CPAP-end event. Per `intervention_effects §8.1` neither event is analytically separable at this resolution; this MD does NOT attempt to disentangle them. Downstream analyses that need to isolate CPAP-end effects must use a different design (ITS or matched-window) per `intervention_effects §8.3`.

---

## 4. Alternatives considered

| label | proposal | verdict | reason |
|---|---|---|---|
| **(a)** | Status quo — no within-Stratum-4 sub-segmentation default per `lc_era_temporal_segmentation §3` | rejected as default substrate | The default works for HA pre-regs (per-pre-reg M1/M2/M3 warrant gating) but is sub-optimal for **descriptive work** where the lived-experience structure is the substantive question. Lumping `lc_pre_ergo` + the pacing era (phase 4: sub-phases 4a + 4b) + `citalopram_modulated` into one `lc_with_gevoelscore` bin (as `recovery_arc` v1 did) loses the clinical heterogeneity that drives the descriptive story. |
| **(b)** | Use the citalopram axis (`citalopram_phase_stratification §3`) as the canonical multi-year axis | rejected | The citalopram axis is a medication-state sub-axis; it has no `lc_pre_ergo` or pacing-era (phase 4) analog. Adopting it as the canonical axis collapses 22+ months of pre-citalopram LC into a single `unmedicated` cell, losing the ergo-onset + pacing-learning structure. The two axes are orthogonal and both should exist. |
| **(c)** | Algorithmic change-point detection (PELT / binary segmentation) on `gevoelscore_rolling_*` or autonomic channels | rejected per `lc_era_temporal_segmentation §4` | Re-creates the deleted trajectory framing. Externally-grounded reasons (lived experience + intervention evidence) are stronger anchors than data-driven boundary detection on the very channels the boundaries would then be tested against — a circular self-confirmation risk. |
| **(d)** | Event-overlay only (events as plot markers, not phase boundaries) | rejected for descriptive work | Sufficient for visualisation but doesn't enable per-phase descriptive characterisation (median + IQR + bootstrap CI per phase × channel) — which is the primary use case for the recovery_arc v2 + future Strand B trajectory analyses. |
| **(e)** | One-phase-per-intervention axis (CPAP-on / CPAP-off / Citalopram-buildup / -consolidation / -afbouw / -post) | rejected | Pure intervention-driven; ignores the lived-experience `lc_pre_ergo` + pacing-learning phases that pre-date all interventions. Also runs into the 2024-04 boundary collision unproductively (every CPAP-related boundary touches a citalopram boundary). |
| **(f) — CHOSEN** | Lived-experience M1 + intervention-evidence M2 axis with **phases 1+2 inherited from data-given strata + 3+4+5 from M1/M2 warrants** + orthogonal citalopram sub-axis preserved within phase 5 | proposed | Honours `lc_era_temporal_segmentation §6 criteria for sub-boundaries`: warrants documented (§3); pre-spec'd before any test runs (this MD); no re-tuning after results (lock discipline); no per-segment confirmatory claim under M3 (descriptive only by default; HA adoption opt-in per-pre-reg). Preserves orthogonal citalopram axis. Default canonical for descriptive work; opt-in for HA tests. |

---

## 5. Four-input reasoning

### 5.1 Best-practices standards

- **Stratification by lived-experience clinical phase** is standard in n-of-1 / SCED designs ([WWC 2022 SCED standards](../literature/methodology/wwc_2022_sced_standards.pdf); [SCRIBE 2016](../literature/methodology/scribe_2016_single_case_reporting.pdf); [Natesan Batley 2023](../literature/methodology/natesan_batley_2023_bayesian_sced.pdf)). The discipline requires (a) phases be operationally distinguishable; (b) phase boundaries be documented event-anchored; (c) per-phase analyses be honest about within-phase n.
- **Time-varying confounder adjustment in n-of-1 self-tracked data** is the framework anchor for the citalopram sub-axis nesting per [Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) (cited via `citalopram_phase_stratification §1.3`).
- **Phase boundaries should be event-anchored, not data-driven**: per `lc_era_temporal_segmentation §4` + `citalopram_phase_stratification §3`, both prior MDs explicitly reject PELT / change-point detection in favor of documented-event-anchored boundaries. This MD inherits the discipline, **with an explicit M1 sub-case carve-out**: lived-experience-derived boundaries may include duration rules anchored to a documented event (e.g. the §3.4 8-week post-ergotherapie-start sub-boundary at 2022-11-17). The anchor remains a documented event (ergotherapie start, 2022-09-22); the duration window is the M1 lived-experience warrant per `lc_era_temporal_segmentation §2`. This is distinct from data-driven boundary detection on channel time series — the duration is named in the lived report, not extracted from a Garmin channel — and is therefore M1-defensible without violating the no-data-driven-boundaries discipline.
- **Sub-segmentation requires per-segment warrant**, not blanket adoption: per `lc_era_temporal_segmentation §6` four-criterion gate. Each phase here states its warrant individually (§3); the four criteria (warrant + documented + no re-tuning + descriptive-only-by-default) are honored.

### 5.2 Established literature

**Deferred for ME/CFS-specific anchors** (Goudsmit 2012 envelope theory; Davis 2021 LC characterisation; Larun 2017 graded-exercise critique). These would strengthen the **substantive case** that lived-experience pacing-learning phases are clinically meaningful sub-structures of LC recovery; the methodological reasoning above does not depend on them.

**Inherited project-canonical anchors** (already fetched):
- `citalopram_phase_stratification §1.3` → Daza 2018 for the time-varying-confounder framework.
- `lc_era_temporal_segmentation §5.1` → SCED observational-cohort stratification orthodoxy.
- `CONVENTIONS §1.2` → SCRIBE 2016, CENT 2015, STROBE 2007, WWC 2022, Natesan Batley 2023 (the project's research-discipline standards).

A future revision could queue and absorb the deferred ME/CFS-specific anchors; the framework itself doesn't change.

### 5.3 Our own vision on tradeoffs

| dimension | status quo (a) | citalopram-only (b) | algorithmic (c) | CHOSEN (f) |
|---|---|---|---|---|
| Captures lived-experience structure | no | no (only medication state) | partial (depends on which channel is the change-point input) | yes (M1 warrants per phase) |
| Captures intervention-evidence structure | no | partial (citalopram only) | yes if channel-input is the load-bearing one | yes (M2 warrant for phase 5) |
| Risk of circular self-confirmation | low | low | high (boundaries from data → tested against data) | low (event-anchored boundaries) |
| Researcher degrees of freedom on boundaries | minimal (no boundaries) | minimal (locked at citalopram MD lock) | high (algorithm hyperparams) | minimal (event-anchored + §7b interview locks the only TBD date) |
| Compatible with descriptive Layer 1 discipline | yes (no sub-segmentation = no claim) | yes | mixed (algorithm = inferential layer leaking into descriptive) | yes (boundaries are descriptive substrate; no causal claim) |
| Compatible with HA opt-in pattern | n/a | n/a | n/a | yes (per-pre-reg adoption per `lc_era_temporal_segmentation §6`) |
| Cross-axis orthogonality preserved | n/a | n/a | n/a | yes (citalopram axis nested within phase 5) |
| Per-phase n adequate for descriptive | n/a | mixed (buildup + afbouw short) | varies | mostly yes (phase 3 ~171, 4b ~508, 5 ~787 days — bootstrap-tractable); phase 4a (56 days) is tight and IQR + CI will be wide — honestly surfaced |

**Trade-off summary**: the chosen axis pays a complexity cost (3 layers instead of 1) and gains descriptive-substrate fidelity to the lived-experience corpus + structural exposure of the citalopram M2 confounder. The HA-opt-in pattern absorbs the complexity cost downstream — pre-reg authors that don't need the recovery axis ignore it; those that do cite this MD. Single-axis simplicity (rejected alternatives) costs descriptive fidelity and structural transparency.

### 5.4 Our research limitations + objectives

- **n=1 single-subject across ~5 years**: phase-stratification is the closest available replication test, but it is weaker than across-person replication. Sub-segmentation amplifies this — per-phase n is one slice of one person's corpus. Descriptive characterisation is the legitimate primary use; HA tests on phase-stratified cells inherit the limitation transparently per per-pre-reg caveat.
- **Uneven per-phase durations**: phases 2 (14 days) + 3 (~171 days) + 4a (56 days) + 4b (~508 days) + 5 (~787 days) span ~2 orders of magnitude (smaller phases 2 + 4a at ~14-56 days; larger phases 3 + 4b + 5 at ~171-787 days). Descriptive analyses must report n explicitly per phase ([CONVENTIONS §3.6 named-counts discipline](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file)). Bootstrap CIs widen with smaller phase n; this is honestly surfaced, not hidden. Sub-phase 4a's small n (56 days) is the tightest per-cell constraint introduced at r2; recovery_arc v2 + descriptive consumers must report 4a IQR + CI even when wide.
- **Phase-4-internal "pacing became effective" boundary is intrinsically fuzzy**: per `garmin_pacing_practice §2`, the protocol "emerged and evolved over time" — there is no sharp transition. The §7b operationalisation interview (CLEARED 2026-06-19) anchored the sub-boundary to a habit-formation duration (8 weeks post-ergotherapie-start), not an effectiveness moment. The user explicitly re-named the late sub-phase `pacing_habit_established` (not `pacing_effective`) because effectiveness remains mediated by outside forces. The fuzziness is honestly absorbed into the warrant (habit-formation duration, M1-defensible per `lc_era_temporal_segmentation §2`); the falsifiability hook (§3.4a + §3.4b) admits a revision path via recovery_arc v2 descriptive distinguishability.
- **2024-04 boundary-collision constraint**: the CPAP-end + citalopram-start collision sits at the phase-4/phase-5 boundary. This MD does NOT attempt to disentangle them; per `intervention_effects §8.3` the design that could (ITS with both interventions modeled together) is out of scope. The collision is documented as a phase-4-tail caveat (§3.6).
- **Citalopram afbouw is in-progress**: the corpus right edge is 2026-06-04; post-afbouw begins 2026-06-06 per [`citalopram_phase_stratification §3`](citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification). As new data accrues, phase 5 may need a phase-6 (`post_afbouw`) appended via a v2 amendment. Per `lc_era_temporal_segmentation §7 item 6 as-of-date convention`, this MD also adopts: descriptive analyses citing this axis state their as-of-date; the phase-6 question is queued for the first refresh when post-afbouw data exists.
- **Long-memory inheritance under phase-stratification**: [`recovery_arc/findings.md`](../analyses/descriptive/trajectory/recovery_arc/findings.md) (commit `24dad02`, 2026-06-19) found that 6 of 7 Stratum-4 cells on the HA-P6 channel set fire the factor-of-2 E[L]\* flag — per-phase E[L]\* in approximately [12, 30] days vs the project default E[L]=7 from [`permutation_null_block_length.md`](permutation_null_block_length.md). This long-memory structure inherits into any per-phase descriptive analysis on these channels: phase-stratified bootstrap CIs that use the default E[L]=7 block will underestimate uncertainty on long phases (4a + 4b combined, 5) where the long-memory structure exists. Per-phase E[L]\* should be data-driven OR conservatively widened to match the recovery_arc-observed range. The §6.6 prescription below names this explicitly.

**Objectives served**:
1. Restore the lived-experience clinical structure to the descriptive substrate.
2. Expose the citalopram M2 confounder structurally (rather than relying on per-test §5.B detrend).
3. Preserve the orthogonal citalopram axis for tests that need the dose-state dimension.
4. Provide a citable canonical axis for any descriptive analysis + opt-in axis for HA pre-regs.
5. Anchor the §7b operationalisation interview discipline to a concrete need (the phase-4 sub-boundary, locked 2026-06-19 as `pacing_habit_established` at 2022-11-17).

---

## 6. Operational consequences

### 6.1 Detrend vs phase-stratify within phase 5 — the inherited §5.A/§5.B/§5.C tradeoff

The user's 2026-06-19 question — "include citalopram as a separate phase, and/or control for citalopram effect in detrending" — maps exactly onto the existing [`citalopram_phase_stratification §5`](citalopram_phase_stratification.md#5-the-three-downstream-test-treatment-patterns) treatment patterns, inherited verbatim here for phase 5:

- **Pattern §5.A (per-phase stratification)**: descriptive analyses report per-(recovery_phase, citalopram_phase) cells, cross-classified. Adopted by default for any descriptive analysis that wants to surface the citalopram step structurally. Cost: smaller per-cell n.
- **Pattern §5.B (dose-adjusted predictor)**: descriptive analyses computing per-recovery-phase descriptives on a citalopram-CONFIRMED channel may pre-compute `channel_adj(d) = channel(d) - β · dose_plasma_mg(d)` per `citalopram_phase_stratification §5.B`, then take per-recovery-phase descriptives on `channel_adj`. The phase-5 descriptive reads then exclude the citalopram dose component, isolating the recovery-phase-attributable structure. Cost: depends on β being correct; inherits the buildup-β-vs-afbouw-β tradeoff.
- **Pattern §5.C (per-mg full subtraction)**: out of scope for descriptive work; documented in `citalopram_phase_stratification §5.C` for HA tests.

**Recommended default for descriptive work using this axis** (proposed; user can override): **both §5.A and §5.B are computed as parallel sensitivity rows for any phase-5 cell on a CONFIRMED-citalopram channel**. The per-cell narrative compares the two — if the §5.A and §5.B reads agree, the recovery-phase-attributable structure is robust to the citalopram detrend; if they disagree, the divergence is the substantive descriptive finding.

### 6.2 Adoption by `recovery_arc` v2

[`trajectory/recovery_arc/`](../analyses/descriptive/trajectory/recovery_arc/) v1 (commit `24dad02`) uses the 4-phase data-given axis. v2 will adopt this MD's 6-phase axis (1, 2, 3, 4a, 4b, 5) per the §7b operationalisation lock 2026-06-19. The v1 `findings.md` headline "+3.3-unit elevation over healthy sustained through Stratum 4" decomposes in v2 into per-recovery-phase headlines.

### 6.3 Adoption by other descriptive analyses (Strand A + Strand B)

Per [`descriptive/README §6.1 + §6.3`](../analyses/descriptive/README.md#61-operationalisation_supportstress_mean_sleep-strand-a-first): existing Strand A `operationalisation_support` analyses (e.g. `stress_mean_sleep`) use the citalopram axis for phase-stratification per `citalopram_phase_stratification`. These analyses MAY additionally cross-classify by this MD's recovery-phase axis for the longer-arc story. Recommended pattern: existing Strand A keeps the citalopram axis as primary; cross-classification with this MD's axis is a sensitivity arm.

### 6.4 Adoption by HA pre-regs (opt-in; per-pre-reg M1/M2/M3 warrant)

Per `lc_era_temporal_segmentation §6`: HA pre-regs adopting this MD's recovery-phase axis as sub-stratification of Stratum 4 must state the M1/M2/M3 warrant in their `§3 Data sources` block, citing this MD. The warrant is **already supplied per phase by §3 above**; the pre-reg cites the relevant phase's warrant. Concrete example: an HA pre-reg comparing `bb_lowest` across `pacing_habit_established` vs `citalopram_modulated` cites this MD's §3.5 M2 warrant (citalopram-confirmed dose-modulation on `bb_lowest`).

### 6.5 Per-day master CSV columns (queued, NOT in r1)

If user confirms, a follow-up pipeline patch adds `recovery_phase` as a new column to `per_day_master.csv`, computed via §2.1's `lc_recovery_phase(d)` function. This makes the axis trivially queryable. r1 does NOT pre-commit this — the column add is queued behind the lock + §7b date-lock and surfaced as Operational consequence (5).

### 6.6 Block-aware bootstrap discipline for per-phase descriptives (added r2 per L4.1 absorb)

**Recommended default for descriptive work using this axis** (proposed; user can override): per-phase per-channel **block-bootstrap CI with per-phase E[L]\*** (data-driven via the Patton-White-Politis convention in [`permutation_null_block_length.md`](permutation_null_block_length.md)), with fall-back to project default E[L]=7 when per-phase n is insufficient for stable E[L]\* estimation. The default reporting is: median + IQR + the block-bootstrap 95% CI. Per §5.4 long-memory inheritance, channels in the HA-P6 set on long phases (4a + 4b combined, 5) should expect E[L]\* > 7 and report accordingly; iid bootstrap CIs would systematically under-cover on those cells.

Prescribed for: `recovery_arc` v2 refresh, future Strand A + Strand B descriptive analyses adopting this axis, and any HA pre-reg that opts into per-phase stratification on a channel where recovery_arc v1 already fired the factor-of-2 E[L]\* flag.

---

## 7. Status

**r2 LOCKED 2026-06-19**.

**Process state**: producer-mode r2 absorb + lock-commit. r1 drafted 2026-06-19; fresh-session methodology audit completed 2026-06-19 ([`reviews/lc_recovery_phase_axis-2026-06-19.md`](../reviews/lc_recovery_phase_axis-2026-06-19.md), verdict PASS-with-caveats); §3.6 compression applied per [`hypothesis_lock_process.md §3.6`](hypothesis_lock_process.md) (mechanical r2; no architectural change). The r2 absorbs closed the 5 audit fires (L1.1, L2.6, L4.1, L4.2, plus §7b operationalisation absorb), added the §7b sub-phase split (4a + 4b) per the user-session interview output, and added reciprocal citations to `citalopram_phase_stratification.md` + `lc_era_temporal_segmentation.md`. The 5 §7.1 lock-blocking gates are confirmed at the r2 lock-commit message.

### 7.1 Lock-blocking gates (the lock-commit message MUST confirm each)

1. **Four-input bar surfaced** (CONVENTIONS §2.2): all four §5 inputs visibly addressed. *(r1 status: addressed; literature deferred-but-named honestly.)*
2. **Sub-boundary warrants documented per phase** (`lc_era_temporal_segmentation §6` criterion 1): each phase has a §3 entry naming its warrant class + justification. *(r1 status: §3 done for phases 1-5; phase 4b is gated on §7b.)*
3. **§7b operationalisation interview cleared**: the user has either locked the `pacing_effective` date or affirmed no useful boundary exists. *(r2 status: CLEARED 2026-06-19 by user session; locked operationalisation absorbed into §3.4a + §3.4b; the late sub-phase is named `pacing_habit_established` per user choice — see §3.4b.)*
4. **Cross-axis link consistency**: `citalopram_phase_stratification.md` cross-references this MD reciprocally OR is documented as already-canonical without recip-cite-needed. *(r1 status: outbound cite present; reciprocal is a queued lock-time edit.)*
5. **Audit-for-publication clean** (CONVENTIONS §2.3): run `docs/research/pipeline/audit_for_publication.py` before any push. *(r1 commit will run this.)*

### 7.2 Hard discipline rules for THIS session (per bout-level handoff §7 producer-mode pattern) — *honored at r1 session 2026-06-19; preserved as historical record at r2 lock*

- **End at r1 + commit. Do NOT self-audit.** Fresh-session reviewer reads cold per CONVENTIONS §1.2 reviewer-mode-with-authorization fresh-session discipline. *(honored: r1 session ended at commit; fresh-session audit performed by separate session 2026-06-19.)*
- **Do NOT lock in this session.** Lock requires the audit output + the §7b interview to be present. *(honored: lock happened in a separate session 2026-06-19 after the audit + §7b interview both landed.)*
- **Do NOT pre-author what the §7b interview should ask.** The interview brief is its own deliverable in a later session. *(honored: §7b operationalisation interview output was produced in a separate user session 2026-06-19 and absorbed at r2 lock.)*

---

## 8. Open follow-ups

1. **§7b operationalisation interview** for the phase-4 sub-boundary — **CLEARED 2026-06-19** in user session. The 8-week post-ergotherapie-start rule defines the `pacing_pre_citalopram_learning` → `pacing_habit_established` sub-boundary at 2022-11-17. Absorbed at r2 lock into §3.4a + §3.4b. Gates §7.1 criterion 3.
2. **Per-day master CSV column add** for `recovery_phase` (§6.5). Pipeline patch in `pipeline/03_consolidate/build_unified_dataset.py`. Queued behind lock.
3. **`recovery_arc` v2** using the locked axis. Refreshes `findings.md` + plots from a per-phase × per-channel reading using the 5-or-6-phase structure. Queued behind lock.
4. **Reciprocal citation** from `citalopram_phase_stratification.md` + `lc_era_temporal_segmentation.md` to this MD. Lock-time edit. Queued behind lock.
5. **STOCKTAKE entry** for the new methodology MD per [`STOCKTAKE.md §8 trigger "New methodology MD locked"`](../STOCKTAKE.md). Queued behind lock.
6. **HA-* opt-in adoption pattern** documentation in `hypothesis_lock_process.md` if the discipline matures into a project-canonical pattern. Queued behind ≥2 HA pre-regs adopting this axis.
7. **Phase 6 (`post_afbouw`) amendment** when the corpus first acquires post-2026-06-05 data. v2 revision trigger.
8. **Literature fetch** for the deferred ME/CFS pacing anchors (Goudsmit 2012, Davis 2021, Larun 2017). Queued at `QUEUED-WORK.md` Tier 3.

---

## 9. Cross-references

- [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) §1 (inherited outer axis), §2 (M1/M2/M3 warrant framework), §6 (sub-boundary criteria), §7 item 6 (as-of-date convention).
- [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) §3 (orthogonal inner axis), §4 (per-channel inheritance), §5 (per-phase / dose-adjusted / per-mg treatment patterns).
- [`citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md) §5.5-§5.6 (empirical β values that anchor §3.5 M2 warrant).
- [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md) §3 (canonical intervention dates), §2b (2024-04 boundary-collision caveat), §8.3 (no corpus-wide M2 boundary across channels).
- [`garmin_pacing_practice.md`](garmin_pacing_practice.md) §2 Origins (lived-experience anchor for phase 3 + 4 warrants), temporal-qualifier paragraph (protocol-stabilisation-over-time framing).
- [`CONVENTIONS.md`](../CONVENTIONS.md) §1.1 (producer-mode discipline), §2.2 (four-input bar), §2.3 (audit before push), §3.6 (named counts), §4.2 (caveats vs a-priori), §4.3 (no interpretive marks).
- [`descriptive/README.md`](../analyses/descriptive/README.md) §7b (Strand B operationalisation interview discipline applied at §8.1 follow-up).
- [`analyses/descriptive/trajectory/recovery_arc/`](../analyses/descriptive/trajectory/recovery_arc/) — first consumer (v2 refresh queued behind lock).
- [`STOCKTAKE.md`](../STOCKTAKE.md) — refresh trigger at lock-commit.
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) §0 — methodology MD carve-out (this MD is NOT governed by the HA lock process; governed by CONVENTIONS §2.2 + §2.3 instead).
- [`bout_level_recovery_dynamics.md` *(planned, not yet drafted)*](bout_level_recovery_dynamics.md) — orthogonal methodology arc (within-day resolution); per the PM brief at [`research-pm-brief-bout-level-recovery-pivot-2026-06-19.md`](file:///C:/Users/Gebruiker/.claude/plans/research-pm-brief-bout-level-recovery-pivot-2026-06-19.md). Cross-phase scope in that MD uses the citalopram axis; it MAY optionally inherit this MD's recovery-phase axis at its own lock if useful (non-binding cross-reference).

---

*Drafted 2026-06-19 by Claude (Opus 4.7) in producer-mode under user authorisation. r1 drafted in fresh session 2026-06-19; fresh-session methodology audit by independent session 2026-06-19 (verdict PASS-with-caveats; §3.6 compression eligible). r2 absorbs + LOCK by separate drafter session 2026-06-19. The §7b operationalisation interview for the phase-4 sub-boundary CLEARED 2026-06-19 in a separate user session; output absorbed into §3.4a + §3.4b at r2 lock.*
