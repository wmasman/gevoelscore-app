# Rollout order — site-delivery track (2026-06-30)

**Status**: **PROPOSED r1**, drafted 2026-06-30 by Claude under user
interview. Producer-mode planning artefact (underscore-prefix
convention matching [`_rollout_order_2026-06-25.md`](_rollout_order_2026-06-25.md),
[`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md)).
**Not LOCKED** — requires a fresh-session `/research-methodology-review`
pass before lock, per the same discipline that governed
[`_rollout_order_2026-06-25.md`](_rollout_order_2026-06-25.md) and the
synthesis-structure map.

**Authorising decision (2026-06-30).** This artefact is a *sanctioned
deviation* from the locked by-cluster rollout in
[`_rollout_order_2026-06-25.md`](_rollout_order_2026-06-25.md). That
doc's §1 deviation rule requires explicit user decision in-session for
any departure from the by-cluster order; the user gave it on 2026-06-30
("New site-delivery rollout doc" — author a lock-disciplined doc that
sequences the site backlog by placeholder-priority and supersedes the
cluster order *for the site-delivery track only*). The two rollouts
coexist: the cluster rollout still governs the interpretive-coherence
track; this doc governs the order in which the
[`wiggers_research_story` site](../../../../wiggers_research_story/site/docs/handoff-2026-06-30.md)
requests R1–R28 are produced.

---

## 1. Purpose

The site (`wiggers_research_story`) is built but running on placeholder
data; its
[`handoff-2026-06-30.md`](../../../../wiggers_research_story/site/docs/handoff-2026-06-30.md)
triages a register of 28 requests (R1–R28,
[`research-requests.md`](../../../../wiggers_research_story/site/docs/research-requests.md))
by **what unblocks the most live placeholders**. That is a *leverage*
ordering. It is not a *dependency* ordering, and this research line's
gates impose dependencies the handoff's P1/P2/P3 does not encode:

- descriptive-before-inference (CONVENTIONS §2.1),
- methodology-MD-before-locking-a-major-choice (CONVENTIONS §2.2),
- fresh-session peer review of every reviewer-mode artefact
  (CONVENTIONS §1.2),
- audit-before-push privacy gate (CONVENTIONS §2.3),
- single-pool primacy (`train_validate_split_fate.md`).

This doc re-sequences R1–R28 into dependency-respecting **waves**, and
records which **rigor-lane** each request travels. It is the
project-management layer over the handoff: nothing reaches the site
except as the patient-audience **Stage T** output of the locked
results-analysis layer ([`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)).
The site *inherits*; it does not reinvent.

## 2. Rigor-lanes (the depth-of-rigor each request must pass through)

| Lane | Name | Pipeline | Mode |
|---|---|---|---|
| 0 | Export locked result | locked result → privacy-safe export JSON → `audit_for_publication.py` | producer |
| 1 | Assemble / collate | ≥2 locked results → one consolidated object (derivative computation, **no new null draws**) → privacy pass | producer or reviewer (if it carries a verdict) |
| 2 | Single-pool re-run of locked HAs | re-compute locked primitives under single-pool + permutation-null + bootstrap-CI (`train_validate_split_fate.md` §5; `permutation_null_block_length.md`; queued as Q10) → result re-issue | reviewer-mode-with-authorization |
| 3 | Net-new descriptive analysis | producer Layer-1/3 on `per_day_master.csv` → descriptive result doc → privacy pass (Stage D applies; **no verdict**) | producer |
| 4 | Net-new pre-registered inferential test | descriptive precondition → methodology MD (if §2.2 major choice) → pre-reg → *fresh-session review* → test → result → *fresh-session review* | reviewer-mode-with-authorization |
| 5 | Literature review | `/fetch-paper` batch → contextualisation brief → `/reading` registry | producer (agent task) |
| 6 | Honest-limit only | documented limit, no forced number (`weak` data) | reviewer |
| 7 | Interpretive passthrough to site | D → I → S₁ → S₂ → A → **T (patient-audience)** via `/research-interpret` | reviewer-mode-with-authorization |

Every request terminates in **Lane 7** — the Stage T patient-audience
track is the only sanctioned path onto the site.

## 3. Request → lane map

| Req | Title (short) | Status (handoff) | Lane | Existing asset / queue |
|---|---|---|---|---|
| R1 | per-claim chart exports | have | 0 | `ASSETS-NEEDED.md` shapes; reframe single-pool |
| R2 | per-signal trust metrics | assemble | 1 | `primary-verdict-statistics.md` (re-derive vs R14), specificity cards |
| R3 | pacing paradox (bounded) | new | 1 | folded into R15 driver ledger; `garmin_pacing_practice.md` |
| R4 | trigger type phys/emo/cog | weak | 6 | honest-limit only; `cat_belasting_*`, H2 |
| R5 | convergent-discovery + paced-on flags | assemble | 1 | folded into R15; `garmin_pacing_practice.md` §2–4 |
| R6 | era shift = three confounds | assemble | 1 | folded into R15; `citalopram_dose_response_*`, K01/K02 |
| R7 | beyond-the-guide findings | new/assemble | 4/7 | `personal_hypotheses.md` P6/P7; future layer |
| R8 | research-layer package | assemble | 7 | `registry.md`, `STOCKTAKE.md`, methodology/ |
| R9 | peri-event recovery curve | new | 3 | Q9 infra (per-minute crash signatures) |
| R10 | trajectory time-series | assemble | 3 | proven-indicator series |
| R11 | activity before/after | new | 3 | era activity volumes |
| R12 | structurally-different-body (inferential) | new | 4 | Q16 season; `recovery_arc`; HA-P6 |
| R13 | felt-state establishing timeline | assemble | 3 | `day_entries.csv`, `crash_v2`, `corpus.json` |
| R14 | single-pool primary verdicts | assemble (+v2) | 0/1 (+2) | **DONE for 10 tests** in `single_pool_reanchor/findings.md`; remaining = export packaging + R14-v2 (HA01c, H03, C4b) |
| R15 | driver-ledger statuses | assemble/new | 1 | consolidates R3+R5+R6+R12-narrative; `/drivers` |
| R16 | established-driver corrections | new | 2 | `citalopram_phase_stratification.md` §5.A/B/C |
| R17 | measurement-regime coverage map | assemble | 1 | `garmin_indicators_audit.md`; H03b |
| R18 | hypothesis re-test triage | assemble | 1 | **started**: [`analyses/hypotheses/_retest_triage_2026-06-30.md`](../analyses/hypotheses/_retest_triage_2026-06-30.md) |
| R19 | per-signal recovery-phase axis | new | 3 | `lc_recovery_phase_axis.md`; per-HA re-aggregation |
| R20 | net-of-drivers re-read | new/assemble | 2 | generalises R16 across ledger |
| R21 | activity-conditioned C3 retest | new | 4 | `HA-C3.md` §4.8 (HA-C3-v3 sibling) |
| R22 | binned stress→felt curve | new | 3 | `HA-C3p/` quintile substrate |
| R23 | COVID known-event external check | new | 4 | **Wave-4 committed**; Q9 peri-event tooling; `cohort_topology` |
| R24 | wearable-validity lit in LC/ME-CFS | new | 5 | sibling of `expected_shapes_*review.md` |
| R25 | cross-channel matrix + effective-N | assemble/new | 0/3 | **`cross-channel-correlation.md` ≈ done**; re-confirm Stratum-4 |
| R26 | HR-correction sensitivity | new | 4 | scoped later; `note_2026-06-29_*` track |
| R27 | phase-boundary convergence status | assemble | 0/1 | Q4.3 `era_boundaries/findings.md` |
| R28 | per-phase p25/p75 export | have/new | 0 | `recovery_arc` v2 emit |

## 4. Wave schedule (dependency-respecting)

Primary criterion: **unblock the spine first, then the cheapest exports,
then the descriptive backdrop, then the driver ledger, then the one
committed heavy test.** Each wave passes the §6 gate before any push.

### Wave 0 — The spine (everything inherits these)
- **R18** retest triage — *governs scope*; decides which HAs are
  `no-change` / `overlay-only` / `needs-rerun`, and the C4b n=9
  expand-or-honest-close call. **Do first.** (Verified 2026-06-30: most
  rows resolve immediately against the existing R14 substrate.)
- **R14** single-pool primary verdicts — the ten-test re-run is **already
  done** ([`single_pool_reanchor/findings.md`](../analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md),
  2026-06-24, full rigor). Wave-0 work is **export packaging** (Lane 0/1:
  numbers → site shape + privacy pass, carrying the §5.7 number-not-
  narrative / no-era-verdict framing verbatim) — *not* recomputation.
- **R14-v2** (Lane 2, plan as new work) — close the reanchor's coverage
  gaps: **HA01c** + **H03** (NOT-RUN), the **C4b n=9** cell
  (expand-or-honest-close), and optionally the per-channel **E[L]\***
  backstop. The curve/bout clusters (HA-C3/C3p, HA-C4c/HA11-bout) are
  covered by rollout Phases A/B/C, not here.

### Wave 1 — Trust + structure exports (most placeholders, low risk)
- **R2** trust panel (re-derived vs R14's single-pool numbers).
- **R25** cross-channel matrix + effective-N (re-confirm on Stratum-4,
  privacy pass — closest to done).
- **R1** per-claim chart exports (single-pool reframe; drop decay/swing).
- **R17** coverage map (separates real time-variation from artifact).

### Wave 2 — The descriptive backdrop (the new change-over-time spine)
- **R13** felt-state establishing timeline (home opener; month-level).
- **R19** per-signal recovery-phase-axis read (replaces early-vs-late).
- **R27** phase-boundary convergence — finalize status.
- **R22** binned stress→felt curve for `/not-a-straight-line`.

### Wave 3 — The driver ledger
- **R15** driver-ledger statuses (consolidates R3 + R5 + R6 +
  R12-narrative; `un-examined` is a valid published status).
- **R20** net-of-drivers re-read (collapsibility correction; **only**
  confirmed channels — stress, `bb_lowest`).
- **R16** established-driver corrections (raw + corrected both shown).

### Wave 4 — Committed heavy test (one only, per 2026-06-30 decision)
- **R23** known-event external check (COVID infection). Full Lane-4
  pipeline: peri-event methodology MD → pre-reg → fresh-session review →
  test → result → fresh-session review. **A null is publishable** and
  softens the `three-things` copy. *Highest leverage on the site, but
  slowest — it cannot be an export.*
- R21 / R26 / R12 are **scoped after R23 lands**, not committed now.

### Parallel track (no dependency, start anytime)
- **R24** wearable-validity lit review (Lane 5; agent task). Can run
  from day one alongside any wave.

### Wave 5 — Future layer / honest limits
- **R7**, **R8**, **R9**, **R10**, **R11**, **R28**, **R4** (weak).

### Terminal hop (every wave)
- Route each landed result into the site via the **Stage T
  patient-audience** track of `/research-interpret`. Map-growth
  (`synthesis_structure_map.md`) is required wherever a request touches
  a construct not yet in the map — a gated step, not free.

## 5. Order summary

| Order | Wave | Requests | Lane(s) | Gate before push |
|---|---|---|---|---|
| 1 | 0 | R18, R14 | 1, 2 | fresh-session review (R14 result); audit |
| 2 | 1 | R2, R25, R1, R17 | 1, 0/3 | audit; R2/R25 reviewer-checked vs R14 |
| 3 | 2 | R13, R19, R27, R22 | 3, 0/1 | Stage D per analysis; audit |
| 4 | 3 | R15, R20, R16 | 1, 2 | reviewer review (R20/R16 corrections); audit |
| 5 | 4 | R23 | 4 | methodology MD + 2× fresh-session review; audit |
| — | ∥ | R24 | 5 | privacy pass on brief |
| 6 | 5 | R7, R8, R9, R10, R11, R28, R4 | 3/4/6/7 | per-lane |

## 6. The rigor-gate contract (applied to every wave)

1. **Descriptive before inference** — no Lane-4 pre-reg starts until its
   Stage D `descriptive_audit.md` is TRUSTED.
2. **Methodology MD before any major lock** — R23 peri-event window,
   R21 activity covariate, R26 HR-partialling, R12 confound controls
   each likely trip §2.2 → four-input MD before the pre-reg locks.
3. **Fresh-session peer review** — every reviewer-mode artefact drafted
   in one session, reviewed in a different session, doc-only.
4. **Privacy / audit-before-push** — `python
   docs/research/pipeline/audit_for_publication.py` must `[PASS]`;
   stage-then-audit newly-authored files; aggregated only, no dated raw
   points, month-level crash positions.
5. **Single-pool primacy** — era/phase differences ship as *a number
   with wide error*, never a per-era verdict.
6. **`_open_inputs.md` is the honest-limit ledger** — anything we can't
   say cleanly becomes a logged open-input + the one-tier-narrower
   fallback, not silence and not an inflated number.

## 7. Cross-references

- [`_rollout_order_2026-06-25.md`](_rollout_order_2026-06-25.md) — the
  by-cluster rollout this doc deviates from (with authorization).
- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) —
  the six-stage layer every request terminates in.
- [`synthesis_structure_map.md`](synthesis_structure_map.md) — map-growth
  gate for constructs not yet registered.
- [`train_validate_split_fate.md`](train_validate_split_fate.md) §5,
  [`permutation_null_block_length.md`](permutation_null_block_length.md) —
  the single-pool re-run recipe (R14/R20).
- [`queued_work.md`](queued_work.md) — Q9 (peri-event infra for R9/R23),
  Q10 (single-pool cross-check = R14/R18 spine), Q16 (season for R12).
- [`research_line_limitations.md`](research_line_limitations.md) — the
  L-IDs every site claim must cite.
- [`../../../../wiggers_research_story/site/docs/handoff-2026-06-30.md`](../../../../wiggers_research_story/site/docs/handoff-2026-06-30.md)
  + [`research-requests.md`](../../../../wiggers_research_story/site/docs/research-requests.md) — the source register.

## 8. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-30 | Drafted r1 (PROPOSED) | Producer-mode under user interview. Sequencing decision: site-delivery track supersedes by-cluster order (authorized deviation from `_rollout_order_2026-06-25.md`). Wave-4 scope: R23 only. First content artefact: R18 triage. NOT LOCKED — fresh-session `/research-methodology-review` pending before lock. |
