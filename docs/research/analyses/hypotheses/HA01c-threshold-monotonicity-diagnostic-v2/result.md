# HA01c v2 threshold-monotonicity diagnostic — result

**Run date**: 2026-06-07. **Test script**: [test.py](test.py).
**Pre-registration**: [diagnostic.md](diagnostic.md), locked
2026-06-07 per testing playbook
([../../methodology/testing-playbook.md](../../methodology/testing-playbook.md))
section 9 + locked v2 criteria
([../../methodology/threshold-sweep-rescue-criteria-v2.md](../../methodology/threshold-sweep-rescue-criteria-v2.md))
adapted for rank thresholds. **Output data**: [result-data.json](result-data.json).

## TL;DR — HA01c v2 verdicts (mixed)

| era | v2 verdict | reason |
|---|:-:|---|
| **train**    | **AMBIGUOUS** | shape is bumpy-but-never-negative; falls between Cat 3 (rising-to-peak, monotone) and Cat 4 (sign-changes) |
| **validate** | **RESCUE** via Cat 1 | textbook canonical decline (peak τ=0.60 with +24.6 pp, monotone decline beyond, Spearman ρ=-0.850) |

**Overall (per playbook §4.4 both-eras rule)**: mixed v2 → HA01c
stays **"SUPPORTED-with-stability-mixed"** — honest but **NOT
load-bearing**. Per [HA01c v2 diagnostic.md §6.2](diagnostic.md):
*"Mixed. The both-eras rule blocks load-bearing. HA01c stays
'SUPPORTED-with-stability-mixed' — honest but not load-bearing."*

This is the **first AMBIGUOUS verdict in the v2 series** (after
RESCUE Cat 3 ×2 for HA10/HA07d, RESCUE Cat 1/2 for HA07d/HA11,
CLOSE Cat 4 for HA06b). The locked criteria correctly surface the
edge case rather than forcing a fit. Discipline binds.

## Section 1: Discrimination curves

### 1.1 Train (n_clean=11, n_null=195)

| τ | disc (pp) | freq (event) |
|---:|---:|---:|
| 0.50 | +15.4 | 100.0% |
| 0.60 | **+6.4** | 81.8% |
| 0.70 | +16.2 | 81.8% |
| 0.75 | **+21.3** ← peak | 81.8% |
| 0.80 | +10.3 | 63.6% |
| 0.85 | +7.9 | 54.5% |
| 0.90 | +2.0 | 36.4% |
| 0.95 | +7.3 | 27.3% |

Shape stats:
- Peak τ = 0.75, peak_disc = +21.3 pp
- Sign-changes in [0.60, 0.90] = **0** (never crosses zero)
- Spearman ρ = -0.452 (declining on average, but with the 0.60 dip)
- max_neg = +2.0 (no negative values across full grid)

### 1.2 Validate (n_clean=15, n_null=195)

| τ | disc (pp) | freq (event) |
|---:|---:|---:|
| 0.50 | +15.4 | 100.0% |
| 0.60 | **+24.6** ← peak | 100.0% |
| 0.70 | +21.0 | 86.7% |
| 0.75 | +19.5 | 80.0% |
| 0.80 | +13.3 | 66.7% |
| 0.85 | +13.3 | 60.0% |
| 0.90 | +12.3 | 46.7% |
| 0.95 | +6.7 | 26.7% |

Shape stats:
- Peak τ = 0.60, peak_disc = +24.6 pp
- Sign-changes in [0.60, 0.90] = **0**
- Spearman ρ = **-0.850** (strongly negative — classic monotone decline)
- max_neg = +6.7 (all positive)

## Section 2: Five-category shape-rule evaluation

Per locked rank-adapted criteria in [diagnostic.md §4.4](diagnostic.md).

### 2.1 Train

| category | passed? | detail |
|---|:-:|---|
| **Cat 1** canonical decline | **fail** | peak τ=0.75 NOT in [0.50, 0.70]; monotone_beyond_peak=False |
| **Cat 2** stable plateau | **fail** | plateau_range = 19.3 pp > 5 pp threshold |
| **Cat 3** rising / late-peak | **fail** | peak τ=0.75 < 0.80; monotone_rise_to_peak=False (the 0.50→0.60 drop from +15.4 to +6.4 breaks monotone rise) |
| **Cat 4** bumpy with sign-changes | **fail** | 0 sign-changes (never crosses zero) |
| **Cat 5** loose-tail noise | **fail** | peak_disc = +21.3 pp >> 5 pp floor |

**Train v2 verdict: AMBIGUOUS**. No category triggers.

**Why AMBIGUOUS** (not CLOSE): the train shape is bumpy
(15.4→6.4→16.2→21.3→10.3→7.9→2.0→7.3) but never crosses zero, so
Cat 4 (which requires ≥1 sign-change) does not trigger. The shape
has peak at τ=0.75 (not 0.50-0.70 for Cat 1; not ≥0.80 for Cat 3)
and the rise to peak is non-monotone (the 0.50→0.60 drop). It's a
genuine edge case the locked rule doesn't cleanly categorize.

**Reading**: the train signal is robust (peak +21.3 pp, all 8
thresholds positive, declining on average ρ=-0.45) but the locked
v2 shape criteria can't classify it. The locked discipline returns
AMBIGUOUS rather than forcing a fit — this is the rule working as
designed.

### 2.2 Validate

| category | passed? | detail |
|---|:-:|---|
| **Cat 1** canonical decline | **PASS** | peak τ=0.60 in [0.50, 0.70]; monotone_beyond_peak=True (24.6→21.0→19.5→13.3→13.3→12.3→6.7, all non-increasing); peak_disc ≥ +7 at τ=0.75 = True (+19.5 pp); signs ≤ 1 = True (0) |
| **Cat 2** stable plateau | fail | plateau_range = 17.9 pp > 5 pp threshold |
| **Cat 3** rising / late-peak | fail | peak τ=0.60 < 0.80 |
| **Cat 4** bumpy with sign-changes | fail | 0 sign-changes |
| **Cat 5** loose-tail noise | fail | peak_disc = +24.6 pp |

**Validate v2 verdict: RESCUE via Cat 1**. Textbook canonical decline.

**Reading**: validate is the cleanest Cat 1 shape in the v2 round.
Peak at the loosest threshold (0.60) with +24.6 pp, declining
monotonically as the threshold tightens. ρ=-0.850 confirms strong
negative correlation between threshold and discrimination. The
validate-era effective_exertion signal is threshold-stable in the
"classic" sense — the discrimination is highest when the bar is
loose and decays predictably as the bar tightens. No bumps, no
sign-changes, no surprises.

## Section 3: Why train AMBIGUOUS while validate RESCUES

This is a genuine era-moderator finding on threshold-stability,
not just on discrimination magnitude:

- **Validate-era crashes**: the precursor signal is broadly
  distributed across rank tiers (peak +24.6 at τ=0.60). Most
  crashes hit at least 0.60 in the lead-up; tighter thresholds
  catch fewer crashes but with similar excess vs null. Classic
  shape.
- **Train-era crashes**: the precursor signal is concentrated at
  τ=0.70-0.75 (peak +21.3 at τ=0.75; weak at τ=0.60 with +6.4).
  Many train crashes hit the τ=0.50 bar (100%) AND the τ=0.70 bar
  (81.8%) BUT not at intermediate τ=0.60 — there's a local dip.

Why the dip at τ=0.60 in train?

One hypothesis: the train-era crash precursor activity pattern is
**bimodal** — some crash days are preceded by very-heavy days
(rank 0.85+) and others by moderate-heavy days (rank 0.70-0.80),
but few are preceded by mild-elevation days (rank 0.55-0.65). The
null windows happen to include many rank 0.55-0.65 days (the
"typical above-median" tier in the lagged 30-90 day baseline). So
the τ=0.60 boundary catches the null distribution's natural
elevation but NOT the train crashes' bimodal cluster.

In validate, the precursor activity is more uniformly elevated,
so the canonical decline applies cleanly.

This is a *descriptive* hypothesis, not a re-pre-registration —
it would need a separate test on the per-day rank distributions
to confirm. For the current diagnostic, the verdict is AMBIGUOUS
on train, RESCUE on validate.

## Section 4: Cross-references to other v2 round verdicts

This is the **5th v2 diagnostic** in the v2 round.

| diagnostic | train | validate |
|---|---|---|
| HA10 | n/a (train was already SUPPORTED v1) | RESCUE Cat 3 |
| HA07d | RESCUE Cat 3 | RESCUE Cat 2 + Cat 3 |
| HA06b | **CLOSE Cat 4** (permanently demoted) | n/a (validate was already REFUTED v1) |
| HA11 | RESCUE Cat 1 | n/a |
| **HA01c (this)** | **AMBIGUOUS** (first in series) | RESCUE Cat 1 |

The locked v2 framework now has worked examples of all four outcomes:
RESCUE (multiple sub-categories), CLOSE, AMBIGUOUS (first instance:
HA01c train), and the symmetric demotion case (HA06b).

## Section 5: What this means for HA01c's load-bearing status

Per [HA01c v2 diagnostic.md §6.2](diagnostic.md): *"Mixed. The
both-eras rule (playbook §4.4) blocks load-bearing. HA01c stays
'SUPPORTED-with-stability-mixed' — honest but not load-bearing."*

- HA01c's locked SUPPORTED both-eras verdict
  ([HA01c result.md](../HA01c-effective-exertion-shock/result.md))
  **stays on record**.
- HA01c does **NOT graduate to load-bearing** in synthesis.
- effective_exertion as a single-axis precursor is **honest at
  τ=0.75** but the train-arm threshold-stability is undecided
  under the locked v2 framework.

This means in the project synthesis:

- HA07d remains the **only project-level overall-SUPPORTED + v2-
  validated finding** (both eras RESCUE).
- HA10 validate (+RESCUE) remains the corroborating secondary
  for the validate-era freeze pattern.
- HA01c is added as **SUPPORTED-with-stability-mixed**: noted in
  the synthesis but not used to make load-bearing claims.
- HA01b composite REFUTED stays unchanged on record.

## Section 6: Card-craft implications

Per playbook §2.7 (card.md craft rule): card.md is only drafted
**if result.md is SUPPORTED** AND **specificity tables pass per
§6.2**. HA01c's v2 outcome (SUPPORTED-with-stability-mixed) means
the load-bearing gate did NOT pass for synthesis purposes. Even
without the v2 mixed outcome, the specificity caveat (2.2%
posterior per fire vs 1.7% base rate) would have blocked card
drafting per playbook §6.2.

**No HA01c card.md will be drafted.** The user's pre-committed
choice for this phase was to wait for HA01c + v2 to resolve before
any card work; the resolution is: do not draft.

Per playbook §6.6 no-go list: even if a future tighter-threshold
re-test resurrected effective_exertion as load-bearing, the
acceptable surface would be reflective-only (timeline annotation
of crossings during after-the-fact review). NOT crash-risk
percentages, traffic lights, push notifications, or automated
targets.

## Section 7: Compliance verification (playbook §9, 19 items)

All 19 items satisfied per diagnostic.md §2. Re-verified on
completion:

- [x] Folder structure: `HA01c-threshold-monotonicity-diagnostic-v2/`
- [x] Pre-registration locked 2026-06-07 BEFORE this script ran
- [x] References playbook + locked v2 criteria doc
- [x] crash_v1 used (29 episodes; 14 train, 15 validate)
- [x] Default train/validate split + both-eras rule applied
- [x] Lagged baseline column (`effective_exertion_rank_lagged`)
- [x] Relative thresholds (rank thresholds, not absolute)
- [x] Primary direction: one-sided elevated (matches HA01c)
- [x] 3-episode dry-run gate: ran (in stdout)
- [x] 3-criterion bar evaluated at locked-threshold (τ=0.75) AND
  threshold sweep around it
- [x] Null sample seed `20260605`, N=200
- [x] Validity floors per playbook §4.6
- [x] Decision rules → verdict categories per locked v2 criteria
  (RESCUE / CLOSE / AMBIGUOUS)
- [x] Channel non-independence: single-axis test, noted in HA01c
  result.md caveat 3
- [x] Multi-comparison disclosure: 8 thresholds × 2 eras = 16
  evaluations; the v2 shape rule is precisely the multi-comparison
  control
- [x] No further v2 nesting needed (this IS the v2)
- [x] No-go surfaces flagged: §6 above
- [x] Hardware constraints: none specific
- [x] Audit trail: §4 cross-reference table to other v2 verdicts

## Section 8: Outputs to downstream artefacts

- **HA01c locked verdict on record**: SUPPORTED both eras at
  τ=0.75 ([HA01c result.md](../HA01c-effective-exertion-shock/result.md)).
- **HA01c v2 verdict on record**: train AMBIGUOUS / validate RESCUE
  Cat 1; overall **mixed → SUPPORTED-with-stability-mixed, NOT
  load-bearing**.
- **Synthesis docs**: STOCKTAKE, synthesis.md, addendum, registry,
  QUEUED-WORK to be updated with this v2 outcome.
- **No card.md drafted**.
- **No HA01d follow-up pre-registered** at this time (would
  require a separate user decision to re-pre-register a tighter
  threshold or alternative shape).

---

*Result locked 2026-06-07. v2 threshold-monotonicity diagnostic for
HA01c is closed. The locked v2 framework returned the first
AMBIGUOUS verdict in the v2 series — discipline binds even when
the framework can't categorize the train shape cleanly.*
