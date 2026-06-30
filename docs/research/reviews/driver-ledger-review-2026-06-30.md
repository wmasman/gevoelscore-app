# Review — driver-ledger (R15) + net-of-drivers findings (R16+R20)

**Review date**: 2026-06-30
**Reviewer**: independent, fresh-session (CONVENTIONS §1.2). No prior
context on how the targets were drafted; read cold and adversarially.
**Targets** (read in full, read-only):

1. `docs/research/analyses/garmin_exploration/cards/driver-ledger.md`
   (R15 — 7-driver consolidating ledger; feeds the site /drivers page).
2. `docs/research/analyses/descriptive/operationalisation_support/net_of_drivers/findings.md`
   (R16+R20 — net-of-driver corrections; feeds citalopram `modelled-out`).

**Standard**: the 4-layer checklist in
`docs/research/reviews/README.md` + audit hooks in
`docs/research/CONVENTIONS.md` §3 and §4.

**Sources independently consulted** (not assumed correct):
`citalopram_phase_stratification.md` §2/§4/§5.A–C/§6,
`citalopram_dose_response_stress_mean_sleep.md` §5.6.1 + :328-330,
`single_pool_reanchor/findings.md` (raw numbers + operands),
`clusters-export.md` :20-78, `coverage-map.md` :82-134,
`phase_boundary_convergence/findings.md` :44-113,
`lc_recovery_phase_axis.md` :310-318,
`garmin_pacing_practice.md` :25-33,
`intervention_effects_descriptive.md` :500-509,
`CONVENTIONS.md` §3.4 + §3.6.

---

## 1. What the data shows (empirical claim separated from framing)

**Empirical core.** A graded citalopram dose-response is *measured* in
this n=1 corpus on three autonomic-load/recovery channels
(`stress_mean_sleep` +0.43/mg, `all_day_stress_avg` +0.57/mg,
`bb_lowest` −1.13/mg; buildup post-CPAP β, HAC 95% CI excludes zero),
with a flat spring-2025 control. When that measured driver is modelled
out of the locked single-pool scorecard reads via the §5.B dose-adjusted
predictor, **nothing strengthens**: the delta/slope primitives (HA07c
+10.8, HA08c +13.4) are near-invariant, the one spike level that moves
(H02b +3.5→+2.5) moves *toward null*, and every confirmed-channel signal
was already single-pool NOT-SUPPORTED and stays NOT-SUPPORTED.

**Framing layer (the ledger's, separated out).** Seven candidate
drivers are each assigned a status on a 6-slot taxonomy that encodes
*how far the work has gone, not how big the effect is* — with
`un-examined` and `examined-not-visible` published as honest states.
The headline the ledger sells is "three changes at once across the era —
recovering body, improving pacing, a dose-modulated drug — only one
(citalopram) carries a measured magnitude." This framing is disciplined:
it refuses to collapse the era into a clean recovery story and refuses
to let any single driver be called "controlled for."

---

## 2. Independent verification of the load-bearing numbers

Every raw number reproduces against the locked
`single_pool_reanchor/findings.md`:

| signal | ledger/net-of-drivers raw | source (single_pool_reanchor) | match |
|---|---|---|---|
| HA07c | +10.8 | :16 / :41 | ✓ |
| HA08c | +13.4 | :18 / :55 | ✓ |
| H02b | +3.5 | :23 / :90 | ✓ |
| HA07d | +19.7 | :17 / :48 | ✓ |
| HA11 | +16.8 | :20 / :69 | ✓ |
| HA10 | +4.1 | :19 / :62 | ✓ |
| HA06b | +6.7 | :25 / :104 | ✓ |
| HA01b | +5.1 | :15 / :34 | ✓ |

The three confirmed betas reproduce exactly against
`citalopram_dose_response_stress_mean_sleep.md` §5.6.1
(:896-898): +0.429→+0.43, +0.565→+0.57, −1.134→−1.13; resting_hr +0.030
p=0.34 (correctly recorded as not-confirmed). The "stress = GSS, not
mental stress" anchor verifies at `:328-330`. The §5.B correction
formula `channel_adj = channel − beta·dose` reproduces verbatim against
`citalopram_phase_stratification.md` :270. **No transcription error
found in any load-bearing figure.**

---

## 3. The two load-bearing nuances — do they survive?

### 3.1 The delta/slope-invariance claim — SURVIVES (with one precision caveat)

The claim: for a night-over-night delta (HA07c) or trailing-5d slope
(HA08c), subtracting a slow-moving plasma dose barely changes the
operand because `delta(channel_adj) = delta(channel) − beta·delta(dose)`
and `delta(dose) ≈ 0` day-to-day.

**Independently this is sound.** The §5.B correction is a *level* shift
proportional to dose. A first difference of a level shift is
proportional to the first difference of dose; the dose series in this
corpus moves on a PK-smoothed plasma trajectory (the doc's own spot
checks: 30.0 at plateau, ~19.9–20.0 across a month of consolidation),
so `delta(dose)` over a single night is near-zero on all but a handful
of titration-step days. A slope is a linear operator on the level, so it
inherits the same cancellation: the dose contribution to a trailing-5d
OLS slope is `beta·slope(dose)`, again near-zero for a slow ramp. The
doc's stated mechanism ("the same shift hits both the value and its
baseline", net_of_drivers :104-108) is the correct second reason — the
operand is z-scored against a *lagged baseline of deltas*, so even the
residual dose contribution is partly differenced out a second time. The
empirical result (HA07c +10.8→+10.8 exactly; HA08c +13.4→+13.4 with CI
widening marginally) is exactly what the math predicts.

**Precision caveat (minor).** "Near-invariant by construction" is true
*for a slowly-varying dose*, not unconditionally. On titration days
(buildup ramp, afbouw taper) `delta(dose)` is non-trivial — e.g. the
afbouw spot-checks show 10.0→8.2 mg across a month, ~0.06 mg/day, but
single-day titration steps can be larger. The cancellation is therefore
*empirical-given-this-dose-trajectory*, not a pure algebraic identity.
The ledger phrasing "by construction" (driver-ledger :236, :173) slightly
overstates this — it is "by construction *of a slow-moving dose*". This
is the one phrase I would soften. It does not change any verdict.

### 3.2 The citalopram `modelled-out` call — SURVIVES

The status move `bounded → modelled-out` is licensed: (a) the driver is
`bounded` (three CONFIRMED channels with CI-excludes-zero betas); (b) the
correction-license condition in `citalopram_phase_stratification.md` §4
is met (these are exactly the load-bearing CONFIRMED channels §5
treatments are *for*); (c) §5.B is the prescribed cross-phase treatment
and is applied as written; (d) the dose series the correction needs is
materialised (`dose_plasma_mg`, 1372/1372 non-null, range 0–30,
spot-checks match the phase trajectory — net_of_drivers §1). The
taxonomy's own definition of `modelled-out` ("a correction removes the
driver's contribution from downstream reads", driver-ledger :52) is
satisfied on the channels where the correction is wireable and exact
(HA07c, HA08c, HA07d). **The call is defensible.**

One honesty point in the `modelled-out` *favor*: the doc does not
oversell it. It states plainly that the correction *barely moves*
the delta/slope channels and that none strengthened — i.e. `modelled-out`
here means "we removed it and confirmed it was never doing the work,"
not "removing it rescued a signal." That is the correct, non-inflating
reading of `modelled-out` for this corpus.

---

## 4. Per-driver status audit (all 7 independently checked)

| driver | status | defensible vs source? | note |
|---|---|---|---|
| **recovery** | `visible-unquantified` | **yes** | "5 of 6 lived boundaries, never watch-tuned, surface independently; 6th out-of-corpus" matches `phase_boundary_convergence/findings.md` :46-48 + tally :72-73; rp4 +3.0 bpm CI[+2.0,+4.0] matches :105. No magnitude claimed; recovery_arc v2 correctly flagged queued-behind-lock (`lc_recovery_phase_axis.md` :314). |
| **pacing** | `visible-unquantified` | **yes** | efficacy correctly out-of-scope + queued C.4/C.5 (`garmin_pacing_practice.md` :25-28). R3 paradox stated without smuggling an efficacy claim. |
| **citalopram** | `modelled-out` | **yes** | see §3.2. |
| **CPAP** | `irreducible` | **yes** | 7-day collision with citalopram-start; both 2024-04-09 and 2024-04-16 marked UNANALYZABLE at every buffer (`intervention_effects_descriptive.md` :504-505). `irreducible` is the right taxonomy slot. |
| **season** | `visible-unquantified` | **yes** | Stratum-1 ~7-month winter/shoulder illness×season confound; decomposition queued Q16. No season number invented. |
| **chance** | `examined-not-visible` / `un-examined` (split) | **yes** | effective-N 3–4, honest α 0.0125, H02b sole survivor counting once — all reproduce against `clusters-export.md` :26,54,69-78. Corpus-wide FWER honestly carried as `un-examined`. |
| **measurement-regime** | `examined-not-visible` (scorecard) / `bounded` (non-scorecard) | **yes** | all 7 scorecard signals full-coverage UDS, artifact-risk NO, reproduces against `coverage-map.md` :127-133; HA10/H04 R18 correction to UDS anchors verified :94-115. |

**On the "correction-licensed (negatively)" framing for measurement-regime
(driver-ledger :174, drivers.json `correction-licensed-negatively`).**
The prompt asks whether this is a category error. It is *not* — but it is
a strained label. The honest content is: the licensed claim is
*artifact-risk NO*, i.e. "no availability adjustment is needed." That is
a real, defensible claim (the §6 prose states it correctly). But calling
the *absence of a needed correction* "correction-licensed (negatively)"
is an idiosyncratic coinage that risks reading as "a correction was
applied with a negative sign." I would relabel this `no-correction-needed`
or fold it under `complicates-only (resolved)`. **Framing nit, not an
error** — the underlying claim survives.

**On the chance "examined-not-visible / un-examined" split.** Coherent
and correct: the multiple-comparison exposure *is* partly examined
(effective-N → honest Bonferroni), and the corpus-wide FWER genuinely is
*not* assembled. Two sub-statuses on one driver is unusual but honest;
it correctly refuses to claim a single corpus-wide false-discovery number
that does not exist.

---

## 5. The H02b approximation — honest, and correctly caveated

The double-flag (net_of_drivers §3.3) is **honest and verified against
the operand definitions**. H02b's single-pool operand rides
`max_spike_minutes` (a DURATION metric in minutes) —
confirmed at `single_pool_reanchor/findings.md` :88. The +0.57/mg beta
is the `all_day_stress_avg` DAILY-MEAN beta (stress points/mg) —
confirmed at `citalopram_dose_response` :897. So applying it to H02b is
genuinely (a) a daily-mean beta on a spike metric AND (b) a
points-subtracted-from-minutes unit mismatch. Both flags are real; the
doc raises both unprompted. "Direction right, magnitude indicative" is
the correct caveat strength — the sign of the dose-driven inflation is
defensible (more dose → more stress → more spike-minutes), but the
+3.5→+2.5 magnitude is not a calibrated residual and the doc says so and
marks the row APPROXIMATION in the table (:67). **No overclaim.** If
anything this row is *more* conservatively flagged than it strictly needs
to be, which is the right direction to err.

---

## 6. HA11 netted=null — a real constraint, not an avoidable gap

The claim: HA11's `u_dip_count` operand bakes the S_pre≥40 gate in at
*per-minute* extraction, and `per_day_master.csv` holds only daily
aggregates, so dose-correcting the gate would require re-detecting U-dips
on a dose-corrected *per-minute* stress series that does not exist in the
master. Subtracting a stress-*level* beta from an event *count* is
dimensionally meaningless (net_of_drivers §3.4).

**This is a real constraint, independently confirmed.** The single-pool
operand for HA11 is "max signed z (4d) of `u_dip_count` (per-day count
primitive in master)" (`single_pool_reanchor/findings.md` :67) — a
count, not a level. The master is daily-aggregate by construction.
Dose-correcting a gate that fires at minute resolution cannot be done
from a daily column without re-running detection on a minute-level
series. The doc records the exact future-fix spec
(`S_pre_adj(t) = S_pre(t) − 0.43·dose_plasma_mg(d)` on the per-minute
series, then recompute the daily count). **`netted=null` is the honest
call** — reporting raw-only +16.8 with the wiring gap stated is correct,
not a papered-over gap. The only thing I would add: the master *does*
carry `dose_plasma_mg` daily, so a future fix needs the minute-level
*stress export*, which the doc correctly identifies as the missing piece.

---

## 7. Framing discipline — stress = GSS held throughout

Checked every per-driver row, every acted-on-live row, and both
drivers.json blocks for any implication of emotional/mental stress.
**None found.** The binding rule is stated in driver-ledger §0.1 and
net_of_drivers :31, and every "stress" reference downstream is qualified
(GSS / autonomic / HRV-derived) or is unambiguously the Garmin channel.
The acted-on-live "stress at rest (low-motion + high GSS)" row (§3) is
explicitly the device signal. **Pass.**

---

## 8. What fired — audit hooks (Layer 4)

### 8.1 §3.4 crash-drop sensitivity on the dose-response — FIRES (minor)

CONVENTIONS §3.4 requires a crash-drop sensitivity row on *every Layer 4+
correlation/regression touching PEM-pacing variables*. The net-of-drivers
overlay is a discrimination-statistic re-read, not a regression, and its
§7 caveat 2 explicitly defers crash-drop (and serial-dependence, and
spike-resolution) to the locked HA verdicts, stating the overlay is a
*single-confounder fix only*. This is a defensible scoping — the locked
verdicts carry their own §3.4 records, and `single_pool_reanchor`
:183 confirms the single pool inherits the same 29-episode crash set
without re-running a per-episode drop sweep. **But**: the *dose-response
betas themselves* (+0.43/+0.57/−1.13) are regressions on autonomic-load
channels, and neither target restates whether those betas carry a
crash-drop sensitivity row in their source MD. The hook fires at the
disclosure level: the ledger's citalopram row and the net-of-drivers
method note should add one sentence pointing at where the *dose-response
regression's* crash-drop diagnostic lives (or noting it was not run). As
stands a reader cannot tell whether the load-bearing betas are
crash-robust. **Magnitude: minor** — it is a missing pointer, not a
missing analysis, and the corrections move toward null regardless.

### 8.2 §3.6 named-counts — PASSES

net_of_drivers §5 names the triple correctly: scheme (`crash_v2`),
unit (episode-level `n_crash_episodes = 29` + day-level per-signal
`n_crash`/`n_null`), source file (`labels_crash_v2.csv`). Per-signal
count-triples are tabulated (:183-198). This is a model §3.6 disclosure.
The ledger inherits these counts by reference. **Pass.**

### 8.3 §4.1/§4.2 caveat-class — PASSES

net_of_drivers §7 carries the descriptive-no-causal caveat, the
single-confounder-fix caveat, the buildup-β-may-overcorrect tradeoff,
the CI-widening note, the HA11-unwireable note, and the
H02b-approximation note. The ledger §0 binds the GSS/era/single-subject
caveats and §8 carries the un-examined flags. **Pass.**

### 8.4 §4.3 prior-driven vs post-hoc — PASSES

The dose-response is a prior-specified confirmatory test (the §1.4 SSRI
nocturnal-autonomic prior); the net-of-drivers correction is a
mechanical overlay, not a new hypothesis. No post-hoc dredging. **Pass.**

---

## 9. What does NOT fire (selective, with evidence)

- **Autocorrelation / Layer 3** — the overlay reuses the locked
  block-permutation null (E[L]=7, B=10,000, stationary-bootstrap CI,
  documented seeds 20260605/20260624). Not a plain-OLS SE. Passes
  Natesan/WWC transfer.
- **Data provenance / Layer 2** — every figure traces to a named source
  file:line; the dose series provenance and the "stale §8.3 QUEUED note"
  reconciliation (net_of_drivers §1) are disclosed rather than glossed.
- **Effective-N inflation** — the ledger refuses "seven agreeing
  signals," carries effective-N 3–4 explicitly, and tags clusters so the
  site cannot re-inflate one driver into "moved many signals."

---

## 10. Genuine-gap honesty — verified

All six prompt-flagged gaps are carried as *gaps*, not papered over:
recovery magnitude (un-decomposed, queued), pacing efficacy
(un-examined, queued C.4/C.5), season number (queued Q16, no number
invented), CPAP magnitude (irreducible, none obtainable), corpus-wide
FWER (un-examined as a single number), citalopram mechanism
(literature-MIXED, n=1 cannot adjudicate). The ledger §8 + §9 and
net_of_drivers §7 are explicit on each. **This is the strongest part of
both documents** — the `un-examined` taxonomy slot is used as designed.

---

## 11. What would strengthen these findings

1. **Soften "by construction"** (driver-ledger :173, :236;
   net_of_drivers :78) to "by construction *of a slowly-varying dose*",
   or add one clause noting the cancellation is empirical-given-this-PK-
   trajectory and would weaken on a sharp titration step. One-line fix;
   removes the only overstated phrase.
2. **Add the §3.4 pointer for the dose-response betas** (§8.1 above): one
   sentence in the citalopram row and the net-of-drivers method note
   saying where the dose-response regression's crash-drop diagnostic
   lives, or that it was not run. Closes the only fired audit hook.
3. **Relabel `correction-licensed-negatively`** to `no-correction-needed`
   (or `complicates-only (resolved)`) for measurement-regime — the
   current coinage risks reading as a signed correction. Cosmetic, but
   this ledger feeds a public site.
4. **HA11 future-fix**: state that `dose_plasma_mg` *is* present daily
   and only the minute-level *stress* export is missing, so the
   future-fix blocker is precisely one export, not a modelling gap.
   (net_of_drivers §3.4 nearly says this; make it one sentence in the
   ledger §9 residual so the site's "open questions" is precise.)

None of these changes a verdict or a status.

---

## 12. Verdict

**ACCEPT-WITH-MINOR-REVISIONS.**

The empirical spine is faithfully reproduced (every load-bearing number
verified against locked sources with zero transcription error), the two
load-bearing nuances both survive independent scrutiny (the
delta-invariance claim is mathematically sound modulo a "slow-moving
dose" precision caveat; the citalopram `modelled-out` call is validly
licensed and, to its credit, non-inflating), all seven driver statuses
are defensible against their cited sources, and the genuine gaps are
carried honestly as gaps. The revisions are a single overstated phrase
("by construction"), one missing audit-hook *pointer* (§3.4 on the
dose-response betas — the analysis exists in the locked verdicts; only
the disclosure pointer is absent), one idiosyncratic status label, and
one precision sentence on the HA11 blocker. Highest-priority concern is
Layer 4 (§3.4 disclosure pointer); it is a pointer gap, not an analysis
gap, hence minor rather than REVISION-RECOMMENDED.

The citalopram `modelled-out` call **survives**. The delta-invariance
claim **survives** (soften "by construction"). stress=GSS framing holds
throughout; no row implies emotional stress.

---

*Independent fresh-session review per CONVENTIONS §1.2. Read-only on
both targets; no target edited, no git, no push. Numbers verified against
single_pool_reanchor, citalopram_dose_response §5.6.1,
citalopram_phase_stratification §4/§5, clusters-export, coverage-map,
and phase_boundary_convergence as cited inline.*
