# Driver ledger (R15) — what could be driving the over-time story, and how far each is pinned down

**Producer-mode assembly artefact.** Assembled 2026-06-30 for Wiggers-site request R15.
Consolidates **R3** (pacing paradox), **R5** (convergent-discovery + acted-on-live flags),
**R6** (era=three confounds), and the **R12** driver narrative into ONE living object.
Read-only over already-landed methodology + analysis MDs — **no new extraction, no new
test, no re-lock, no audit, no git**. Does NOT write into the site repo and does NOT touch
any locked `result.md`.

**What this is.** A single ledger of every candidate *driver* that could explain a
difference the scorecard shows — recovery, pacing, citalopram, CPAP, season, chance,
measurement-regime — with a **status** (how far it has been pinned down), the **channels**
it touches, the **finding**, and a numeric **bound** where one exists. Plus the three
framing passages (R3 pacing paradox, R5 acted-on-live per-signal flags, R6 three-confounds)
and the proposed `drivers.json` shape.

**Why a ledger.** The point of publishing this is to show the work-in-progress honestly.
A driver that is **un-examined** is a *valid published status* — it says "we have not looked
yet", not "there is nothing here". Statuses are **provisional** and move as analyses land.
**Update 2026-06-30: the R20 net-of-driver correction has landed** ([`net_of_drivers/findings.md`](../../descriptive/operationalisation_support/net_of_drivers/findings.md)) and moves citalopram from `bounded` to **`modelled-out`** on the confirmed channels — see the §2 citalopram row and §5 drivers.json for the netted numbers. **Fresh-session review 2026-06-30** ([`reviews/driver-ledger-review-2026-06-30.md`](../../reviews/driver-ledger-review-2026-06-30.md)): verdict **ACCEPT-WITH-MINOR-REVISIONS** — all numbers reproduced, all 7 statuses defensible, citalopram `modelled-out` + the delta-invariance nuance both survived independent scrutiny; 3 minor wording/disclosure fixes absorbed (slow-moving-dose caveat, `no-adjustment-needed` relabel, §3.4 crash-drop pointer).

---

## 0. Binding framing rules (do not strip on re-use)

1. **"stress" = Garmin's HRV-derived Stress Score (GSS)**, a 0-100 composite derived
   primarily from heart-rate variability (`citalopram_dose_response_stress_mean_sleep.md:328-330`).
   It is **NOT mental/emotional stress**. Never let any driver row imply emotional stress.
2. **The citalopram dose-response was MEASURED in this body** and stands on its own as
   local n=1 evidence (`ssri_citalopram_hrv_review.md:5`). The *mechanism* (HRV-blunting)
   is a separate question and is literature-**MIXED** (`ssri_citalopram_hrv_review.md:9-17`).
   Record both: measured-driver = confirmed; mechanism = plausible-not-established.
3. **A status taxonomy slot is a claim about how far the work has gone, not about how big
   the effect is.** `un-examined` and `examined-not-visible` are honest, publishable states.
4. **Effective-N ≈ 3-4, not 7** (`clusters-export.md:54`). A driver that touches one cluster
   member touches its redundant siblings. Per-channel rows below tag the cluster so the site
   never re-inflates a one-cluster driver into "moved many signals".
5. **Single subject** (L1), **era-confounded** (L2), **single device FR245 / Elevate V3** (L3),
   **analyst-is-subject** (L4) per `research_line_limitations.md`. Every driver inherits these;
   the per-driver rows cite the *specific* L-IDs that bite hardest.

---

## 1. Status taxonomy (pick one per driver)

| status | meaning | publishable? |
|---|---|---|
| `un-examined` | no analysis has looked at this driver yet | **yes** — shows the frontier |
| `examined-not-visible` | looked; no readable signature in the watch data for the scorecard signals | yes |
| `visible-unquantified` | a shift is visibly present but not yet decomposed into a number | yes |
| `bounded` | measured with a magnitude + uncertainty on confirmed channels | yes |
| `modelled-out` | a correction removes the driver's contribution from downstream reads | yes |
| `irreducible` | structurally cannot be separated from a co-event by any available design | yes |

Statuses are provisional. The **direction of travel** is recorded per row where a queued
analysis is expected to move it.

---

## 2. The per-driver ledger

`{id, status, channels[], finding, bound}` per candidate driver. `channels[]` uses the
scorecard channel ids (cluster in brackets per `clusters-export.md:69-78`).

| id | status | channels | finding | bound |
|---|---|---|---|---|
| **recovery** | `visible-unquantified` | rp1-rp5 boundaries read on resting_hr (HA06b/C2), stress_mean_sleep (HA07c/C2), morning BB peak (HA10/C2), within-day stress (C1) | 5 of 6 lived recovery-phase boundaries — fixed from the lived story, **never tuned to the watch** — independently surface as multi-channel shifts in the Garmin data; the 6th is out-of-corpus (`findings.md:46-48,63-70`). The recovery slope also runs *underneath* the citalopram afbouw window and is the inherited substantive confound (`citalopram_dose_response_stress_mean_sleep.md:80-98`). | not decomposed into a per-day-of-recovery magnitude. rp4 (learning→habit) reproduces the prior resting-HR finding +3.0 bpm CI [+2.0,+4.0] (`findings.md:105-107`). |
| **pacing** | `visible-unquantified` | live: morning BB (§3.1), daytime BB drain + 25/20/15 floor (§3.2), stress-at-rest (§3.3), cog/emo budget (§3.4), felt state (§3.5). NOT live: within-day RHR (§4.1), HRV (§4.2) | The participant actively paces off 5 Garmin/felt channels (`garmin_pacing_practice.md:97-183`). Protocol is a **recent stabilisation, not a constant** — high-fidelity in recent months, partial earlier (`garmin_pacing_practice.md:62-79`). This is the **R3 pacing paradox** (§4): the very behaviour under study shapes the data it is measured in. | un-quantified by design — pacing *efficacy* descriptive work is queued (QUEUED-WORK C.4 + C.5; `garmin_pacing_practice.md:28`), not run. No magnitude yet. |
| **citalopram** | `bounded` → heading `modelled-out` (via R20) | CONFIRMED: stress_mean_sleep (HA07c/C2), all_day_stress_avg (C2), bb_lowest (C2-adjacent). WEAK: resting_hr (HA06b/C2). REJECTED: respiration_avg_sleep | Measured graded dose-response, confirmed across both phases (afbouw 2026 + buildup-2024 post-CPAP) with a flat spring-2025 control ruling out the generic-spring alibi (`citalopram_dose_response_stress_mean_sleep.md:894-960`). Mechanism (HRV-blunting) is literature-**MIXED, leaning weak** (`ssri_citalopram_hrv_review.md:9-17`). | **stress_mean_sleep +0.43/mg** [+0.16,+0.70] p=0.001; **all_day_stress_avg +0.57/mg** p=0.000; **bb_lowest −1.13/mg** p=0.000 (buildup post-CPAP β; `citalopram_dose_response_stress_mean_sleep.md:896-898`). resting_hr +0.03/mg p=0.34 (not confirmed). R20 net-of-driver correction running concurrently — corrected numbers land separately. |
| **CPAP** | `irreducible` | would-be: stress_mean_sleep, respiration_avg_sleep, bb_* (sleep-recovery family) | CPAP-end (2024-04-16) sits **7 days** from citalopram-start (2024-04-09); the 2024-04 cluster is **structurally unanalyzable at every buffer** — all pre/post windows empty (`intervention_effects_descriptive.md:154,504-505`). A different design (ITS with both modelled jointly) would be needed (`intervention_effects_descriptive.md:537`); §8.1 names some boundaries structurally unanalysable. | none obtainable from this corpus by this method. CPAP-start (2024-01-10) is separately analyzable but showed no detrend-surviving step (`intervention_effects_descriptive.md:524`). |
| **season** | `visible-unquantified` | Garmin-only baseline channels (RHR, sleep stress, BB shape) on Stratum-1 contrasts | Stratum-1 (pre-corona) Garmin coverage is **~7 months, Aug-Mar = winter + shoulder only** — any Stratum-1 vs Stratum-3/4 baseline contrast confounds illness-state with season **by construction** (`lc_era_temporal_segmentation.md:34`). Inside the afbouw window, daylight rises ~12h→16h ~linearly; the linear time covariate absorbs monotonic seasonal drift, the spring-2025 control rules out generic spring (`citalopram_dose_response_stress_mean_sleep.md:104-120`). | not decomposed. Season-stratified contrast workflow is **queued, not run** (queued_work Q16; `queued_work.md:775-790`). |
| **chance** | `examined-not-visible` (where corrected) / `un-examined` (corpus-wide FWER) | all scorecard channels | Multiple-comparison exposure is partly handled: honest effective-N ≈ 3-4 ⇒ Bonferroni α ≈ 0.0125; **H02b/H02d is the only primary verdict surviving an honest effective-N correction**, and counts as one finding via collinearity (`clusters-export.md:26`). A full corpus-wide false-discovery accounting across all HAs is not assembled here. | effective-N **3-4** (vs nominal 7; `clusters-export.md:54`); honest α ≈ 0.0125 (`clusters-export.md:26`). No single corpus-wide FWER number. |
| **measurement-regime** | `examined-not-visible` (FOR THE SCORECARD) / `bounded` (non-scorecard sharpening tests) | scorecard: resting_hr, bb_highest, stress mean/stdev sleep, per-minute stress, U-dip — **all full-coverage UDS**. cutover: bb_overnight_gain truth/best, per-minute sleep BB; blocked: literal HRV | **All 7 scorecard signals sit in the full-coverage daily-UDS regime — artifact-risk NO** (`coverage-map.md:127-133`). An over-time delta on a scorecard signal is a body/behaviour change, not a data-availability artifact. Artifact-risk is **confined to the non-scorecard sharpening channels** (per-minute BB cliff ~2024-06-03 / scalar 2023-12-31; bb_overnight_gain two-stage rollout SLEEPSTART 2024-07-08 / SLEEPEND 2024-09-18; literal HRV hardware-blocked). HA10/H04 were corrected (R18) to full-coverage UDS anchors, not the per-minute cliff (`coverage-map.md:94-115`). | scorecard artifact-risk = NO across both analysis boundaries. Bounded elsewhere: bb_overnight_gain 33.8% coverage; per-minute BB ~716 valid days; the 2023-12-31 scalar cutover **co-locates exactly with the retired train/validate split** (`coverage-map.md:86-88,123`). |

---

## 3. R5 — per-signal "acted-on-live?" flags (convergent-discovery)

R5's load-bearing point: the pacing protocol **acts on** some signals in real time (a live
behavioural loop predates any analysis), and merely **recognises** others retrospectively.
The boolean per signal is read straight off `garmin_pacing_practice.md` §3 (live) vs §4
(research-side only). A live signal carries the stronger "convergent-discovery" prior — the
participant arrived at it independently, before Wiggers' vocabulary and before the corpus
analysis (`garmin_pacing_practice.md:51-60`).

| signal / construct | acted-on-live? | how it is read in daily life | source |
|---|:--:|---|---|
| Morning Body Battery (overnight gain, level, carryover, felt-divergence) | **yes** | wake-time glance sets the day's envelope | `garmin_pacing_practice.md:102-112,219-222` |
| Daytime BB — drain rate + 25/20/15 floor | **yes** | late-afternoon decision check; commit-or-shrink | `garmin_pacing_practice.md:114-131,225-234` |
| Stress at rest (low-motion + high GSS) | **yes** | mid-day "wait it out"; evening "early bed" | `garmin_pacing_practice.md:133-145,236-244` |
| Cognitive / emotional load budget | **yes** | reactive cancels; informal 16:00 horizon | `garmin_pacing_practice.md:147-166` |
| Felt state (independent ground-truth) | **yes** | trusted on divergence; often wins vs BB | `garmin_pacing_practice.md:168-183` |
| Within-day RHR | **no** | recognised post-hoc (Wiggers A4 resonates with felt memory) but NOT read live | `garmin_pacing_practice.md:188-204` |
| HRV (nightly) | **no** | not available on FR245; retrospective even if path-C unblocked | `garmin_pacing_practice.md:207-211` |

**Read for the site**: the convergent-discovery story is strongest on the five §3 channels
(live behavioural loop = independent prior). RHR and HRV are *recognition*, not *operation* —
a hypothesis operationalised on RHR-shaped columns tests whether the post-hoc recognition has
measurable substrate, not whether a live loop exists (`garmin_pacing_practice.md:198-204`).

---

## 4. R3 — the pacing-paradox passage (bounded)

**The paradox.** The participant paces *off the watch* (and felt state) every day — see §3.
Pacing is therefore not an external variable acting on an untouched body; it is a behaviour
**woven into the very data the scorecard measures**. A "quieter autonomic signal over time"
is partly the body recovering and partly the participant getting better at not provoking it.
The two cannot be cleanly separated within a single self-paced corpus.

**Why it is bounded, not unbounded.** Three things keep the paradox from swallowing every
finding:

1. **The protocol is a recent stabilisation, not a constant** (`garmin_pacing_practice.md:62-79`).
   It was partial-fidelity in 2022-23 (pacing being learnt) and during the work-attempt /
   work-stop periods, and high-fidelity only in the most recent months. So pacing-as-confound
   has a *time profile*, not a flat presence — earlier eras are less pacing-shaped than recent
   ones.
2. **Pacing live-channels are enumerated** (§3) and **separated from research-side-only
   channels** (§4). A finding that rides a NOT-live channel (within-day RHR, HRV) is not
   directly inside the live behavioural loop, which bounds the paradox's reach for those
   specific channels.
3. **Efficacy is un-tested, so no efficacy claim is being smuggled in.** Whether the protocol
   *works* is explicitly out of scope and queued (QUEUED-WORK C.4 + C.5;
   `garmin_pacing_practice.md:27-28`). The ledger records pacing as `visible-unquantified`,
   not as a measured driver — honest about the gap.

**What the site must NOT say**: that a recovery signal is "really just pacing" (un-tested),
nor that pacing is "controlled for" (it is not — it is a `visible-unquantified` driver woven
into the substrate). The honest line is: *pacing is present, acted-on-live on five channels,
of time-varying fidelity, and its efficacy is not yet measured.*

---

## 5. R6 — the "three confounded changes" passage (era=three)

The era shift (roughly pre-2024 → citalopram era) is **not pure biology**. At least three
things changed across the 2024-04 region, and the site must present all three rather than
selling the era as a clean recovery step:

1. **A different body.** The LC recovery trajectory (crash frequency ~10/yr in 2023-24 → ~2/yr
   in 2025-26) runs underneath the whole era and is the inherited substantive confound
   (`citalopram_dose_response_stress_mean_sleep.md:80-83`; `intervention_effects_descriptive.md:21`).
   The body in 2026 is simply further along the recovery arc than the body in 2024.
2. **Better pacing fidelity.** Per §4, the pacing protocol stabilised over recent months
   (`garmin_pacing_practice.md:62-79`) — the participant got *better at pacing* across the
   same span, so behaviour-shaping of the data increased over the era.
3. **Citalopram dose-modulation.** A measured, confirmed dose-response on the autonomic-load +
   recovery channel family (§2 citalopram row) sits inside the era — the watch's GSS and BB
   nadir move with plasma dose at the magnitudes bounded above
   (`citalopram_dose_response_stress_mean_sleep.md:896-898`).

**The collision that makes it irreducible at one seam.** Citalopram-start (2024-04-09) and
CPAP-end (2024-04-16) sit 7 days apart; the 2024-04 cluster is structurally unanalyzable
(`intervention_effects_descriptive.md:154`; `lc_recovery_phase_axis.md:176-178`). So the
rp5 "pacing→medication era begins" boundary is a **genuine seam in the data but a confounded
one** — honest convergence, ambiguous cause (`findings.md:69`).

**What the site must say**: the era is *three changes at once* — recovering body + improving
pacing + a dose-modulated drug — not a single biology story. Citalopram is the one of the
three with a measured magnitude (bounded); the other two are present-but-unquantified.

---

## 6. Correction-licensed vs complicates-only

A driver is **correction-licensed** if its magnitude is measured well enough to subtract or
adjust out downstream (bounded / confirmed channels). A driver is **complicates-only** if it
muddies interpretation but offers no number to correct with.

| driver | class | reason |
|---|---|---|
| **citalopram** | **correction-licensed → modelled-out** | bounded per-mg β on 3 CONFIRMED channels; R20 net-of-driver correction **landed 2026-06-30** (`net_of_drivers/findings.md`): delta/slope channels near-invariant (dose cancels in the difference), H02b +3.5→+2.5, none strengthened. Dose-naive at bout level (0/7 CONFIRMED). |
| **measurement-regime** | **no-adjustment-needed** | scorecard = full-coverage; the licensed claim is *artifact-risk NO* — scorecard deltas need no availability adjustment (`coverage-map.md:127-133`). (Not a signed correction; "nothing to subtract".) Non-scorecard sharpening channels are bounded/excluded. |
| **chance** | **partially correction-licensed** | effective-N 3-4 licenses an honest Bonferroni α ≈ 0.0125 (`clusters-export.md:26`); a full corpus FWER is not assembled. |
| **recovery** | complicates-only | visible across boundaries but not decomposed into a magnitude; no subtractable number. |
| **pacing** | complicates-only | `visible-unquantified`; efficacy un-tested; woven into substrate, not separable. |
| **season** | complicates-only | confounded with illness-state by Stratum-1 construction; decomposition queued, not run. |
| **CPAP** | complicates-only (irreducible) | 7-day collision with citalopram-start; no magnitude obtainable by this design. |

---

## 7. Proposed `drivers.json` shape

```json
{
  "request_id": "R15",
  "title": "Driver ledger: what could be driving the over-time story, and how far each is pinned down",
  "assembled": "2026-06-30",
  "framing": {
    "stress_is_gss": "Garmin HRV-derived Stress Score, NOT emotional stress",
    "effective_n": { "low": 3, "high": 4, "nominal_channels": 7 },
    "status_taxonomy": ["un-examined", "examined-not-visible", "visible-unquantified",
                        "bounded", "modelled-out", "irreducible"]
  },
  "drivers": [
    {
      "id": "recovery",
      "status": "visible-unquantified",
      "channels": ["resting_hr", "stress_mean_sleep", "morning_bb_peak", "within_day_stress"],
      "finding": "5 of 6 lived recovery-phase boundaries (never tuned to the watch) surface independently in the Garmin data; 6th out-of-corpus.",
      "bound": null,
      "correction_class": "complicates-only",
      "direction_of_travel": "decomposition queued (recovery_arc v2)"
    },
    {
      "id": "pacing",
      "status": "visible-unquantified",
      "channels": ["morning_bb", "daytime_bb_drain", "stress_at_rest", "cog_emo_load", "felt_state"],
      "finding": "Acted-on-live on 5 channels; recent stabilisation, not a constant; efficacy un-tested. R3 pacing paradox.",
      "bound": null,
      "correction_class": "complicates-only",
      "direction_of_travel": "efficacy descriptive work queued (C.4 + C.5)"
    },
    {
      "id": "citalopram",
      "status": "modelled-out",
      "channels": ["stress_mean_sleep", "all_day_stress_avg", "bb_lowest", "resting_hr"],
      "finding": "Measured graded dose-response confirmed at daily-aggregate across both phases; spring-2025 control flat. Modelled out via R20 net-of-driver correction (dose_plasma_mg present 1372/1372 days). Mechanism (HRV-blunting) literature-MIXED. Dose-naive at bout level (0/7 features CONFIRMED, n-limited).",
      "bound": {
        "stress_mean_sleep_beta_per_mg": 0.43,
        "all_day_stress_avg_beta_per_mg": 0.57,
        "bb_lowest_beta_per_mg": -1.13,
        "resting_hr_beta_per_mg": 0.03,
        "resting_hr_confirmed": false,
        "beta_source": "buildup post-CPAP, HAC 95% CI"
      },
      "correction_class": "correction-licensed",
      "mechanism_status": "plausible-not-established (literature mixed)",
      "netted_single_pool_pp": {
        "HA07c": "10.8 -> 10.8 (near-invariant; delta primitive)",
        "HA08c": "13.4 -> 13.4 (near-invariant; slope primitive)",
        "H02b": "3.5 -> 2.5 (toward null; daily-mean-beta-on-spike approximation)",
        "HA07d_sensitivity": "19.7 -> 18.7 (variance primitive, ~no change; stays SUPPORTED)",
        "HA11": "raw 16.8, netted=null (gate not wireable from master)",
        "note": "All confirmed channels already single-pool NOT-SUPPORTED; correction moves further toward null, none strengthened. Delta/slope primitives near-invariant by construction of a slow-moving dose (it cancels in the day-over-day difference; empirical-given-this-PK-trajectory, not an algebraic identity) -- the scorecard's delta-stress signals were never strongly dose-confounded."
      },
      "source": "net_of_drivers/findings.md (R20, landed 2026-06-30)"
    },
    {
      "id": "cpap",
      "status": "irreducible",
      "channels": ["stress_mean_sleep", "respiration_avg_sleep", "bb_sleep_recovery"],
      "finding": "CPAP-end 7 days from citalopram-start; 2024-04 cluster structurally unanalyzable at every buffer.",
      "bound": null,
      "correction_class": "complicates-only",
      "direction_of_travel": "would need ITS joint-model design (out of scope)"
    },
    {
      "id": "season",
      "status": "visible-unquantified",
      "channels": ["resting_hr", "sleep_stress", "bb_shape"],
      "finding": "Stratum-1 covers only ~7 months winter+shoulder; illness-state confounded with season by construction. Afbouw spring-control flat.",
      "bound": null,
      "correction_class": "complicates-only",
      "direction_of_travel": "season-stratified contrasts queued (Q16)"
    },
    {
      "id": "chance",
      "status": "examined-not-visible",
      "channels": ["all_scorecard"],
      "finding": "Effective-N 3-4 licenses honest Bonferroni alpha 0.0125; H02b/H02d is the only primary verdict surviving it (counts once).",
      "bound": { "effective_n_low": 3, "effective_n_high": 4, "honest_alpha": 0.0125 },
      "correction_class": "partially correction-licensed",
      "direction_of_travel": "corpus-wide FWER not assembled"
    },
    {
      "id": "measurement-regime",
      "status": "examined-not-visible",
      "scope": "FOR THE SCORECARD",
      "channels": ["resting_hr", "bb_highest", "stress_mean_sleep", "stress_stdev_sleep",
                   "max_spike_minutes", "u_dip_count"],
      "finding": "All 7 scorecard signals are full-coverage daily UDS; artifact-risk NO across both analysis boundaries.",
      "bound": { "scorecard_artifact_risk": "no" },
      "correction_class": "no-adjustment-needed",
      "non_scorecard_bounded": ["bb_overnight_gain", "per_minute_sleep_bb", "literal_hrv"],
      "direction_of_travel": "stable; bounded on non-scorecard sharpening channels"
    }
  ],
  "acted_on_live": {
    "morning_bb": true, "daytime_bb": true, "stress_at_rest": true,
    "cog_emo_load": true, "felt_state": true,
    "within_day_rhr": false, "nightly_hrv": false
  },
  "headline": "Three changes at once across the era — recovering body, improving pacing, a dose-modulated drug — only one of which (citalopram) carries a measured magnitude."
}
```

---

## 8. Genuinely un-examined / un-quantified flags (no inventing a finding)

Per the brief, these are flagged as work-not-yet-done rather than dressed up as findings:

- **recovery magnitude** — boundaries *converge* (visible) but no per-recovery-day magnitude
  exists; recovery_arc v2 decomposition is queued behind the lc_recovery_phase_axis lock,
  not run (`lc_recovery_phase_axis.md:313-314`).
- **pacing efficacy** — genuinely **un-examined as a measured effect**; the pacing MD is a
  prior-source protocol doc, and efficacy descriptive work (C.4 + C.5) has not run
  (`garmin_pacing_practice.md:27-28`).
- **season decomposition** — queued (Q16), not run; no season-attributable number exists
  (`queued_work.md:775-790`).
- **CPAP magnitude** — irreducible at the 2024-04 seam; no number obtainable by this design
  (`intervention_effects_descriptive.md:537`).
- **chance / corpus-wide FWER** — only the effective-N-corrected α is assembled; a full
  multi-HA false-discovery accounting is **un-examined** as a single number.
- **citalopram net-of-driver corrected numbers** — R20 **LANDED 2026-06-30**
  (`net_of_drivers/findings.md`): citalopram moved `bounded` → `modelled-out`; numbers folded
  into the §2 row + §5 drivers.json. Honest read: the delta/slope scorecard channels were never
  strongly dose-confounded (the day-over-day differencing already cancels the slow-moving dose),
  so the correction barely moves them; only the H02b spike level shifts (+3.5 → +2.5, an
  approximation). HA11's gate is not wireable from the master (future-fix spec recorded).
- **citalopram mechanism** — the HRV-blunting mechanism is literature-MIXED
  (`ssri_citalopram_hrv_review.md:9-17`); the measured driver is confirmed but the *why* is
  plausible-not-established. Not a gap to be filled by this corpus (n=1 cannot adjudicate
  mechanism).

---

## 9. Open questions (anything needing fresh work or a downstream landing)

1. ~~**R20 net-of-driver correction**~~ — **DONE 2026-06-30** (`net_of_drivers/findings.md`):
   citalopram → `modelled-out`; numbers in §2 + §5. One residual: **HA11's S_pre gate is not
   wireable from the master** (u_dip_count bakes the per-minute gate in at extraction; no
   per-minute stress series in the master to dose-correct) — raw +16.8 only, future-fix spec
   recorded in the R20 findings.
2. **recovery_arc v2** — would upgrade recovery from `visible-unquantified` toward a
   per-phase-bounded read. *(Queued behind lock.)*
3. **pacing efficacy (C.4 + C.5)** — would move pacing off `visible-unquantified`. *(Queued.)*
4. **Q16 season decomposition** — would move season off `visible-unquantified` for the
   Stratum-1 contrasts. *(Queued.)*
5. **Corpus-wide FWER** — a single multi-HA false-discovery number would move the chance row's
   corpus-wide sub-status off `un-examined`. *(Not scoped.)*
6. **Per-phase / per-era cluster invariance** — the effective-N 3-4 collapse is computed
   full-window; if the site ever claims the driver→cluster mapping is era-stable, a per-phase
   re-computation is required (`clusters-export.md:174`). *(Fresh run, not claimed here.)*

---

## 10. Privacy statement (stated; not script-run — user gates the audit)

This ledger carries **aggregated coefficients, status labels, day-count integers, and
categorical driver/channel metadata only**:

- **No per-day series, no raw biometrics** — no HR/HRV/stress/BB/gevoelscore values, no
  per-event rows. The only numbers are regression β/mg, effective-N, α, coverage percentages,
  and boundary metadata.
- **Dates present are boundary/era metadata only** (intervention dates, cutover dates,
  analysis-window endpoints), not observations.
- **Counts are corpus-level aggregates** (coverage %, day counts) — they reveal coverage,
  not content.

Conclusion: **R15 is privacy-safe for the site as assembled.** (The user gates
`audit_for_publication.py`; this is the producer's pre-statement, not a substitute for that
run.)

---

## 11. Source citations (file:line)

- Pacing live channels (§3) vs research-side-only (§4); recent-stabilisation temporal
  qualifier: `garmin_pacing_practice.md:62-79,97-211,219-244`.
- Pacing origins / convergent-discovery (Wiggers names patterns already seen):
  `garmin_pacing_practice.md:39-60`. Efficacy out-of-scope + queued:
  `garmin_pacing_practice.md:27-28`.
- Citalopram per-channel confirmed β (buildup post-CPAP):
  `citalopram_dose_response_stress_mean_sleep.md:894-960`. Spring-2025 flat control +
  cross-window verdict: `:770-862`. "stress" = GSS: `:328-330`. LC-recovery substantive
  confound under afbouw: `:80-98`.
- Citalopram downstream correction patterns (§5.A/B/C = R20 license):
  `citalopram_phase_stratification.md:226-321`.
- CPAP + citalopram 7-day collision; 2024-04 cluster structurally unanalyzable; some
  boundaries structurally unanalysable: `intervention_effects_descriptive.md:21,154,504-505,537`.
- Recovery: 5 of 6 lived boundaries visible, never watch-tuned; rp4 +3.0 bpm; rp5 confounded:
  `findings.md:46-48,63-70,105-107`. Recovery axis warrants + recovery_arc v2 queued:
  `lc_recovery_phase_axis.md:161-178,313-314`.
- Season: Stratum-1 ~7-month winter/shoulder illness×season confound:
  `lc_era_temporal_segmentation.md:34`. Season decomposition queued: `queued_work.md:775-790`.
- Measurement-regime: scorecard full-coverage artifact-risk NO; non-scorecard cutover/blocked;
  HA10/H04 R18 correction; train/validate cutover co-location: `coverage-map.md:86-88,94-133`.
- citalopram mechanism literature-MIXED: `ssri_citalopram_hrv_review.md:5,9-17`.
- Effective-N 3-4; honest α 0.0125; H02b/H02d sole survivor; one-cluster-touches-siblings:
  `clusters-export.md:26,54,69-78`.
- Systemic limitations L1/L2/L3/L4: `research_line_limitations.md` §3 (L1 single-subject,
  L2 era confounds incl. 2024-04 cluster, L3 device FR245/no-HRV, L4 analyst-is-subject).

---

*Assembled 2026-06-30 (R15) in producer-mode from already-landed methodology + analysis
MDs. No data recomputation; no methodology-MD or HA-artefact modification; no site-repo
write; no locked result.md touched; no push / audit / git. Statuses are provisional and
move as queued analyses (R20, recovery_arc v2, C.4/C.5, Q16) land.*
