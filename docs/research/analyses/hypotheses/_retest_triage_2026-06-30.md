# Hypothesis re-test triage — what actually moves under the single-pool reframe

> **R18** in the site register
> ([`research-requests.md`](../../../../../wiggers_research_story/site/docs/research-requests.md) §G).
> Governs scope for the whole site-delivery track: it makes "we did not
> redo everything" a **documented, auditable decision**, not a gap.

## Authorship

- **Drafting session**: 2026-06-30, Claude under user authorization.
- **Authorising user**: the participant-researcher (repo owner).
- **Mode**: reviewer-mode-with-authorization (CONVENTIONS §1.2). This
  artefact reads locked `result.md` verdicts and recommends per-hypothesis
  actions; it is **DRAFT** and **not locked**. Per CONVENTIONS §1.2, the
  `/research-review` peer-review must run in a **different session** —
  fresh, doc-only — before this triage is treated as binding.
- **Rigor note**: the 2026-06-30 row-review pass (§2.2) read each
  `result.md` + the cited driver/methodology MDs and filled `rests_on`,
  flag (b), and flag (c) with file:line citations. **No verdict is
  moved** — every locked `result.md` is unchanged; this triage only
  *routes* (no-change / overlay-only / needs-rerun, with R20/R21/R14-v2
  destinations). The row-review was evidence-gathering by three
  read-only reviewers; the merge and any judgement calls are the PM's
  and remain **DRAFT** until the fresh-session `/research-review`.
- **Status 2026-06-30: RE-CONFIRMED / treated as binding.** Both lock
  gates cleared: C4b decided (HONEST-CLOSE, §3) and the fresh-session
  review ran (REVISION RECOMMENDED → all items absorbed, §4). The
  absorbed changes are rationale-only (no verdict moves, re-run short
  list = HA01c only), so per the project's Option-γ pattern the user
  re-confirmed rather than ordering a second review pass. The one open
  methodological flag for the next reviewer: the §3.7-excludes-lagged-z
  call that downgraded HA10 to overlay-only (§2.2).

## 1. Purpose & method

The single-pool reframe (`train_validate_split_fate.md`: the 2023-12-31
train/validate split retired as primary;
`lc_era_temporal_segmentation.md`: two-era framing deleted) changes the
*frame* every locked verdict was read in. R18 asks, per hypothesis:
**what does the current verdict rest on, and does the descriptive
backdrop disturb it?**

Three failure modes to flag per hypothesis:

- **(a) split-dependent** — the verdict leaned on the early/late
  (train/validate) contrast, now demoted to a descriptive overlay.
  Re-read single-pool (mostly done in R14).
- **(b) driver-exposed** — the signal is touched by an established
  driver (citalopram, pacing, CPAP, season, measurement-regime) not yet
  netted out. Routes to R20.
- **(c) shape-assuming** — the test assumed a monotone/linear
  felt-state↔signal relation that `/not-a-straight-line` (the
  shape-not-linear / HA-C3 finding) calls into question. Routes to R21.

**Action taxonomy** (per row): `no-change` · `overlay-only` (era
contrast ships as a number+CI, no per-era verdict) · `needs-rerun`
(single-pool / net-of-driver re-read required).

**Expected & honest outcome** (handoff §G): *most rows are `no-change`
or `overlay-only`.* The triage's job is to make the short list of
genuine re-runs explicit.

**Sources.** [`registry.md`](registry.md) + per-hypothesis `result.md`;
[`STOCKTAKE.md` §6](../../STOCKTAKE.md) (descriptive patterns A–H);
[`train_validate_split_fate.md`](../../methodology/train_validate_split_fate.md);
[`single_pool_reanchor/findings.md`](../descriptive/operationalisation_support/single_pool_reanchor/findings.md);
[`queued_work.md`](../../methodology/queued_work.md) Q10.

## 2. Triage table (row-review COMPLETE 2026-06-30; pending fresh-session review)

Flags (b)/(c) and `rests_on` filled by the 2026-06-30 row-review pass
(three dispatched reviewers, grouped by channel family; determinations
merged here by the PM — see §2.2 provenance). Flag (a) split-dependence
is from the registry verdict structure. **CONFIRMED** = a citalopram
dose-modulated channel where the §5.B net-of-driver correction is
licensed (`stress_mean_sleep` +0.43/mg, `all_day_stress_avg` +0.57/mg,
`bb_lowest` −1.13/mg); **complicates** = driver present but no
correction licensed (raw only).

| Hypothesis | Channel | Current verdict | rests_on | (a) split | (b) driver-exposed | (c) shape | Action |
|---|---|---|---|---|---|---|---|
| H02b | within-day stress spike | train-sup / validate near-miss; overall refuted | train-window discrimination | **YES** | **YES** — citalopram `all_day_stress_avg` CONFIRMED; spike-β *inferred* not measured → raw overlay mandatory | NO | overlay-only **→R20** (single-pool +3.5pp NOT-SUP) |
| H02d | bridge stress spike | train +31.8 / validate refuted (all 4 arms) | train-window discrimination | **YES** | YES — same as H02b; validate refutation *not* driver-rescuable | NO | overlay-only (SUPERSEDED-by-equiv w/ H02b) |
| HA06b | nightly RHR z-score | train SUP / validate refuted | train-window + directionality | **YES** | **NO-confirmed** — RHR weak dose (β+0.03, p=0.34); lagged-z absorbs → complicates only | NO | no-change (single-pool +6.7pp NOT-SUP) |
| HA07c | sleep-stress mean delta | train SUP / validate refuted | train-window | **YES** | **YES** — `stress_mean_sleep` CONFIRMED (measured β); §5.B licensed | NO | overlay-only **→R20** (single-pool +10.8pp NOT-SUP; correction pushes further down) |
| HA07d | sleep-stress stdev delta | **OVERALL SUPPORTED both eras** | both-era discrimination | NO | YES-**weak** — variability decoupled from level-acting dose driver; strongest arm is low-dose | NO | **no-change** (single-pool +19.7pp p=0.029 SUP; §5.B sensitivity overlay only) |
| HA08c | sleep-stress slope | train SUP / validate refuted | train-window | **YES** | **YES** — `stress_mean_sleep` slope CONFIRMED; trend most dose-entangled | NO | overlay-only **→R20** (single-pool +13.4pp NOT-SUP) |
| HA10 | morning BB peak z (daily UDS `bb_highest`) | train refuted / **validate SUPPORTED** | validate-window (reverse split) | **YES** | complicates — daily UDS `bb_highest`, **98.2% coverage → NO measurement-regime confound** (corrected per review); non-CONFIRMED `bb_overnight_gain`-family; **redundant in Cluster 2 (≡−HA07c)** per R25 | NO | **overlay-only** — single-pool **already settles it** (+4.1pp, p=0.43 NOT-SUP); validate +16.2pp is a *descriptive overlay, not a verdict*; do **not** propagate validate-SUPPORTED; §3.7 N/A (lagged-z) |
| HA11 | within-day U-dip count | train SUP / validate refuted | train-window | **YES** | **YES** — `S_pre≥40` gate rides CONFIRMED stress channel; lagged-z only *partial* | NO | overlay-only **→R20** (single-pool +16.8pp p=0.091 NOT-SUP) |
| H01 | RHR drift (absolute) | REFUTED both eras | absolute-threshold lead-up | NO | **NO-confirmed** — RHR not dose-modulated; season complicates (raw only) | NO | no-change (single-pool −3.1pp) |
| H04 | BB net-drain (daily UDS) | REFUTED both (validate +13.3 near-miss) | daily BB net-drain threshold | YES (reverse) | complicates — same **full-coverage UDS** fields as HA10 (no coverage cliff; corrected per review); BB-algorithm/firmware opacity complicates; not `bb_lowest`, not CONFIRMED | NO | overlay-only — REFUTED both eras, single-pool +0.5pp, **no live verdict at stake** |
| HA01b | exertion-class 4d | REFUTED both (v3.2); v3.1 +17.3 artefact | exertion shock frequency | **YES** | YES — pacing-fidelity, exertion channel → complicates (not citalopram) | NO | overlay-only (single-pool +5.1pp NOT-SUP) |
| HA01c | effective-exertion rank | SUPPORTED both, GATED on v2 diag | rank≥0.75 precursor | partial | YES — pacing-fidelity, exertion → complicates | NO | **needs-rerun (single-pool)** — NOT run in reanchor; R14-v2; load-bearing WITHHELD |
| HA-C3 | stress→felt curve (Wiggers bins) | REJECTED (wrong-direction) | curve shape (mid-stress peak) | NO | YES — citalopram `all_day_stress_avg` CONFIRMED; **netted by §5.A unmed-primary design** | **SELF** | no-change → **R21** anchor |
| HA-C3p | stress→felt curve (personal bins) | PARTIAL (same inverse shape) | curve shape | NO | YES — citalopram CONFIRMED; §5.A netted | **SELF** | no-change (cluster pipeline) → R21 |
| HA-C4c | bout failure-to-return | PARTIAL (bar-b δ=0.120 fail) | cross-phase bout contrast | NO (cross-phase) | YES — cross-phase pooled (conditional; **unmed-only REJECTED** → stratum-fragility) | NO | overlay-only (carry unmed-REJECTED caveat) |
| HA11-bout-redo | bout-framework validity | PARTIAL (bar-3 p fail, n-driven) | framework-validity | NO | N/A (methodology validation) | N/A | no-change (TRUSTED Stage D) |
| K01 | crash depth across eras | suggestive-underpowered | era contrast (era=predictor) | **YES** | YES — season/recovery-trajectory = predictor-of-interest, not a confound to net | NA | overlay-only (NOT single-poolable; mean +0.67 > median) |
| K02 | crash duration across eras | refuted-on-bar; tail-collapse | era contrast | **YES** | YES — season/recovery = predictor | NA | overlay-only (NOT single-poolable; ship tail-collapse not median) |

### 2.2 Row-review synthesis & routing (2026-06-30)

The row-review ran as three parallel read-only reviewers (stress family;
autonomic/BB/RHR family; exertion/curve/bout/crash family), each applying
the same driver-ledger facts. They agreed on the CONFIRMED-channel
definitions; determinations merged above by the PM. **Net result —
genuinely-disturbed rows are a short list:**

- **needs-rerun (only 1):**
  - **HA01c** — *single-pool* re-run. Never run in the reanchor (R14-v2);
    `effective_exertion_rank_lagged` column available; load-bearing
    already WITHHELD pending its v2 diagnostic. **The one genuine new
    computation.**
- **HA10 re-assessed → overlay-only (PM, 2026-06-30; flagged for
  confirmation).** Following the fresh-session review's correction to its
  honest conclusion: with the phantom measurement-regime confound removed,
  HA10's single-pool number **already exists and settles it** (+4.1pp,
  p=0.43 NOT-SUPPORTED). "Verdict-fragility" is real but calls for honest
  **overlay framing** (validate +16.2pp ships as a descriptive overlay,
  never a verdict), not a new run. The §3.7 detrend hook the review
  suggested is **withdrawn**: §3.7 scope explicitly *excludes*
  lagged-baseline z-score tests, which HA10 is. A trajectory check would
  only matter to *resurrect* the validate-era signal — which single-pool
  says not to. HA10 is also redundant in Cluster 2 (≡−HA07c) regardless.
  *This §3.7-exclusion call is a methodological judgement; flagged for the
  next review to sanity-check.*
- **overlay-only + route to R20 (net-of-driver residual, 4):** H02b,
  HA07c, HA08c, HA11. All ride a CONFIRMED-stress channel; single-pool
  already NOT-SUPPORTED and the dose correction pushes them *further*
  toward null (dose inflates the train signal), so R20 is **ledger/residual
  work, not verdict-moving** — the R18 verdict is settled.
- **overlay-only (7):** **HA10** (single-pool collapses the
  validate-SUPPORTED to +4.1pp; ship the overlay, never the verdict),
  H02d, H04 (full-coverage UDS, REFUTED both eras, no live verdict at
  stake — *not* a measurement-regime case), HA01b, HA-C4c (carry the
  unmedicated-REJECTED stratum-fragility caveat), K01, K02 (era=predictor,
  ship number+CI not narrative).
- **no-change (6):** HA07d (the one signal that holds — SUPPORTED both
  single-pool and era-split), H01, HA06b (no licensed driver), HA-C3,
  HA-C3p (the shape finding itself → R21), HA11-bout-redo (methodology).
- **flag (c) shape-assuming** is carried by exactly **two** rows, both
  **SELF**: HA-C3 + HA-C3p. Their named untested rival is the **R21
  activity×stress interaction** ("best in the middle" may be partly an
  activity map) — flagged, not addressed in either result.

### 2.1 Single-pool substrate already exists (verified 2026-06-30)

The R14 single-pool re-run is **done** for the ten core tests at
[`single_pool_reanchor/findings.md`](../descriptive/operationalisation_support/single_pool_reanchor/findings.md)
(run 2026-06-24; block-permutation null E[L]=7, B=10,000, stationary
bootstrap 95% CI; full Stratum-4 pool n=29 crashes). It executes the
binding recipe at `train_validate_split_fate.md` §5.7. Consequence for
this triage: **most `needs-rerun` rows collapse to `overlay-only`** —
the single-pool number already exists. Headline: **all 10 CONVERGE with
their locked overall verdicts; only HA07d clears single-pool** (perm
p=0.029); the other nine are NOT-SUPPORTED with wide CIs (the train-era
signals were era-specific).

**Still genuinely uncovered** (R14-v2 fodder, plan as work):
- **HA01c** (effective-exertion rank) — NOT-RUN in the reanchor.
- **H03** (sleep-efficiency) — NOT-RUN (REFUTED both eras; low priority).
- **C4b** rest-stress low-motion n=9 — separate cell (§3 below).
- **HA-C3 / HA-C3p** (stress→felt *curve*) + **HA-C4c / HA11-bout-redo**
  (bout-level) — these are not discrimination tests; they travel the
  cluster pipeline (rollout Phases A/B/C), not this cross-check.
- **Per-channel E[L]\*** (Shared gap 1): only `stress_mean_sleep` +
  `stress_low_motion` have data-driven block lengths; the rest inherit
  E[L]=7 with a caveat. A factor-of-2 deviation could move specific
  p-values (point estimates robust). Closing it = separate descriptive
  runs.

## 3. Named cell to resolve: rest-stress low-motion (C4b), n=9

Per handoff §G (2026-06-30) + `claims[6]`: the pooled rest-stress
low-motion cell fell to **n=9 (< the n≥10 bar)** and currently reads
`genuinely open`. The triage **must** return an explicit
**expand-or-honest-close** action, not leave it dangling.

**Count-triple (CONVENTIONS §3.6)**: the n=9 is **crash-episodes meeting
the C4b rest-stress low-motion primary-cell predicate** (crash_v2
episode-level, `labels_crash_v2.csv` unique crash-`episode_id`),
operationalised per `stress_low_motion_primitive.md`. The exact cell-CSV
and predicate must be cited verbatim when the honest-close is written up
for the site (confirm at write-up; not invented here).

**Decision options (for the row-review + user call):**

1. **Expand** — widen the cell's inclusion window or pooling so n ≥ 10
   (e.g. relax the low-motion gate, or pool an additional citalopram
   phase) — *only if* defensible per
   `stress_low_motion_primitive.md` / `citalopram_phase_stratification.md`
   without manufacturing the result. Requires a methodology note.
2. **Honest-close** — publish as an honest limit: "n=9 is below our
   pre-registered n≥10 floor; we report the descriptive direction with
   wide error and decline a verdict." Logs an `_open_inputs.md` entry.

**DECISION (2026-06-30, user): HONEST-CLOSE.** The row-review (§2.2)
confirmed C4b is **distinct from HA-C4c** (the bout-level
`bout_n_did_not_return` test, fully powered at n=1274) and that the n=9
rest-stress low-motion cell is **not resolved anywhere** in the closed
results — genuinely open below the n≥10 floor, with no non-peeking
expansion path. The user's call (2026-06-30) is to **honest-close**:
publish the descriptive direction with wide error, **decline a verdict**,
and surface the limit plainly on the site (it softens the copy rather
than leaving it over-promising). Logged as `_open_inputs.md` **OI-019**.
The fresh-session `/research-review` will confirm the close is stated
honestly, not adjudicate whether to expand.

## 4. Next steps (rigor-preserving)

1. ~~**Row-review pass**~~ — **DONE 2026-06-30** (§2.2): three read-only
   reviewers filled `rests_on`, flag (b), flag (c) with file:line cites;
   merged by PM. Genuinely-disturbed short list = **HA10**
   (regime-controlled re-run) + **HA01c** (single-pool re-run); 4 rows
   route to R20 (residual, not verdict-moving); rest are
   overlay-only/no-change.
2. ~~Cross-check `needs-rerun` vs single_pool_reanchor~~ — **DONE**: 8 of
   the 10 reanchor HAs settled by the existing single-pool numbers.
3. ~~**Resolve the C4b n=9 cell**~~ — **DONE 2026-06-30**: user decided
   **HONEST-CLOSE** (§3); logged OI-019.
4. ~~**Fresh-session `/research-review`**~~ — **DONE 2026-06-30**: verdict
   **REVISION RECOMMENDED**, report at
   [`../../reviews/retest_triage-review-2026-06-30.md`](../../reviews/retest_triage-review-2026-06-30.md).
   Absorbed: HA10's measurement-regime rationale was a Layer-2 provenance
   error (operand is daily UDS `bb_highest` at 98.2% coverage, not
   per-minute BB; no 2024-06 cliff) — corrected to single-pool
   verdict-fragility; H04's identical mis-flag corrected; §3.6 count-triple
   + §3.7 detrend hook added. **No verdict and no short-list row changed**
   — revisions are rationale-only.
5. **User call**: the absorbed changes are non-structural (no verdict
   moves, short list unchanged), so a re-confirmation rather than a second
   full fresh-session review is defensible per the project's Option-γ
   pattern — **or** request a second review pass. Until one or the other,
   this triage is REVISED-DRAFT, not locked.

## 5. Cross-references

- [`registry.md`](registry.md) — verdict source.
- [`../../methodology/train_validate_split_fate.md`](../../methodology/train_validate_split_fate.md) — the retire-the-split decision.
- [`../../methodology/_rollout_order_site_delivery_2026-06-30.md`](../../methodology/_rollout_order_site_delivery_2026-06-30.md) — Wave 0 placement.
- [`../descriptive/operationalisation_support/single_pool_reanchor/`](../descriptive/operationalisation_support/single_pool_reanchor/) — R14 substrate.
