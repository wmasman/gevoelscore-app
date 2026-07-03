# Descriptive precondition -- post-crash exertion relapse (danger-window)

**Status**: producer-mode descriptive precondition, STAGE 1 of the
post-crash-exertion-relapse ("push-crash danger window") pipeline. Layer-1
descriptive per [CONVENTIONS §4.1](../../../CONVENTIONS.md): characterises
**event location, exposure + outcome definition, data coverage, and the
comparison design space** so the pre-registration can lock with the outcome
unseen. Drafted 2026-07-03 by Claude (Opus 4.8) under producer-mode
authorization, for the participant-researcher (repo owner). Backs the
methodology MD [`../../../methodology/post_crash_exertion_relapse.md`](../../../methodology/post_crash_exertion_relapse.md).

> ## NO-OUTCOME-PEEK STATEMENT (binding)
>
> The hypothesis is a pre-registered inferential test: *does a single
> supra-threshold physical exertion spike in the post-crash danger window
> raise relapse likelihood?* This precondition characterises **only**: the
> events, the danger-window and exposure definitions, data coverage /
> missingness, the **exposure** distribution (a predictor), and the set of
> comparison windows. It does **NOT** compute, estimate, or inspect the
> **outcome** -- the relapse rate, or any exposure-versus-relapse
> relationship. **No relapse counts, conditional or marginal, were computed.**
> The exposure-versus-relapse contrast IS the test; it runs only after the
> pre-reg locks and is fresh-session reviewed (per
> [CONVENTIONS §1.2 / §3.5](../../../CONVENTIONS.md)). Every number below is
> either a coverage / non-null count or an **exposure** (predictor)
> distribution -- never an outcome.

---

## 1. Event location

Trigger events (t0 = felt-state nadir), on the Stratum-4 surface (LC with
gevoelscore + crash labels, 2022-09-03 to 2026-06-05):

| Event class | Source | n |
|---|---|---|
| **Crashes (primary)** | `per_day_master.csv` `crash_episode_id` + `is_crash`; nadir = min-`gevoelscore` day per episode | **29** |
| **Dips (mechanism-control)** | `is_dip` (transient single-bad-days) | **79** |

Named per [CONVENTIONS §3.6](../../../CONVENTIONS.md): *29 crash episodes and
79 dip days on Stratum 4 (`per_day_master.csv`, `is_crash` / `is_dip`,
2022-09-03 to 2026-06-05)*. Crashes carry a distinctive post-crash autonomic
recovery signature (HA-P6: 4/7 channels distinguishable from matched controls;
R9); dips do NOT (flat overnight stress) -- so dips are the **mechanism
control**: if premature exertion after a *dip* does not raise relapse but
after a *crash* it does, the mechanism is autonomic-window-specific, not
"any bad day."

## 2. Exposure + outcome definition (design, not computed)

**The hypothesis** (mechanism): after a crash the PEM threshold is transiently
lowered; during the **danger window** (felt-state recovered, autonomic not yet
settled) a single **supra-threshold physical exertion spike** is more likely
to trip a relapse than at baseline. Grounded in the single-bout
threshold-crossing PEM paradigm (2-day CPET; VT1-as-PEM-threshold) per
[`../../../literature/push crash research.md`](../../../literature/push%20crash%20research.md)
and [`../../../literature/pacing-and-crash-mitigation.md`](../../../literature/pacing-and-crash-mitigation.md);
the danger-window rationale is the symptom-fast / autonomic-slow dissociation
(R9 + [`../../../literature/reviews/pem_recovery_trajectory_review.md`](../../../literature/reviews/pem_recovery_trajectory_review.md)).

- **Felt-recovered gate**: `gevoelscore >= 4` (back into the normal 4-5 band,
  out of the <=3 crash/dip zone), first such day in t+1..t+10.
- **Danger window**: felt-recovery day .. nadir+10 (inside the ~2-week
  autonomic-settle window).
- **Exposure -- PRIMARY (threshold-crossing)**: the **peak** single-day
  `eff_exertion_rank_lagged_lcera` in the danger window, as a **continuous
  dose-response**. Lagged, era-local baseline ([d-90, d-30], LC-era days) per
  [CONVENTIONS §3.2](../../../CONVENTIONS.md) -- "a spike relative to your
  *current* capacity," self-cleaning against crash contamination.
- **Exposure -- SECONDARY (dose-accumulation, competing)**: cumulative load
  (count of shock-days / summed rank) in the danger window. Pits
  threshold-crossing vs dose-accumulation (a contrast no published study has
  run, per `push crash research.md`).
- **Outcome (the TEST, not computed here)**: a new crash OR dip within ~4 days
  of the exertion spike (delayed-onset PEM; 3/4/5-day sensitivity band).
- **Scope**: **physical exertion only.** `eff_exertion` is blind to cognitive
  / emotional / orthostatic load, which draws on the same envelope and can
  trigger PEM (`pacing-and-crash-mitigation.md`). A relapse with no physical
  spike is expected noise (a possible mental-PEM trigger, the parked R4), not
  evidence against the hypothesis.

## 3. Coverage / computability (exposure + non-null only)

Computed on the danger windows. **No outcome computed.**

| Quantity | Crashes | Dips |
|---|---|---|
| Events with a felt-recovery day (`gevoelscore >= 4`) in t+1..t+10 | **28 / 29** | **79 / 79** |
| `eff_exertion_rank_lagged_lcera` coverage in danger windows | **236 / 236 days (100%)** | **790 / 790 (100%)** |
| Events excluded (no felt-recovery or no exertion coverage) | 1 | 0 |

**Exposure distribution (predictor only), crash danger windows (n=28):** peak
`eff_exertion_rank_lagged_lcera` median **0.93** (p25 0.83, p75 0.98, range
0.60-1.00). Count of days >= 0.75 spread 0-6 (median ~3).

### 3.1 The degenerate-binary finding (why the design uses a continuous peak)

A naive **binary** exposure (">= 1 day >= 0.75 in the danger window") flags
**24 / 28** crash windows as exposed (86%) -- because ">= 1 day above your own
75th percentile in a ~week window" is near-guaranteed by construction. That
leaves only 4 unexposed: **no usable contrast group.** This is the load-bearing
precondition finding: it **rules out a binary exposure** and mandates the
**continuous peak dose-response** (§2), which uses the full 0.60-1.00 gradient
and needs no arbitrary cutoff. (It also dodges HA01c's threshold-monotonicity
trap.) The pacing-confound concern was thus **inverted**: exposure is not
censored by pacing, it is near-ubiquitous, so the design problem is
*contrast*, not *rarity*.

## 4. Comparison design space (counts + design only)

- **Primary test**: dose-response of relapse on the **continuous peak
  exertion** in the danger window (crashes, n=28 usable). Not a binary
  exposed/unexposed split (§3.1).
- **Mechanism control**: the same on **dips** (n=79). Crash-vs-dip divergence
  is the autonomic-specificity read.
- **Null**: block-permutation / stationary-bootstrap at E[L] ~ 7
  ([`../../../methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md))
  to respect autocorrelation; a base-rate / regression-to-the-mean reference
  (relapse is common after any low day) is required, not a naive comparison.
- **Relapse window**: ~4 days post-spike, 3/4/5-day sensitivity.
- **Threshold-crossing vs dose-accumulation**: peak (primary) vs cumulative
  (secondary) as competing predictors.

## 5. Open inputs

| # | What is missing | Blocks | Path |
|---|---|---|---|
| 1 | User lock on the methodology decisions (danger-window length, relapse-window, peak-vs-cumulative primacy, crash-vs-dip roles) | The pre-registration | Methodology MD + fresh-session `/research-methodology-review` |
| 2 | Pre-specify the base-rate / RTM null construction (matched non-event windows vs within-window) | The pre-reg's null | Methodology MD §(null) |
| 3 | Reverse-causation guard: a brewing relapse may itself suppress exertion; the pre-reg must state how the peak-before-relapse ordering is enforced | Inference validity | Methodology MD §(confounds) |

## 6. Cross-references

- [`../../../methodology/post_crash_exertion_relapse.md`](../../../methodology/post_crash_exertion_relapse.md)
  (the methodology MD this backs).
- [`../../hypotheses/HA01c-effective-exertion-shock/hypothesis.md`](../../hypotheses/HA01c-effective-exertion-shock/hypothesis.md)
  (the inherited exertion-shock operand: `eff_exertion_rank_lagged` >= tau,
  SUPPORTED, load-bearing withheld on threshold-monotonicity).
- [`../../garmin_exploration/cards/peri-event-recovery-export.md`](../../garmin_exploration/cards/peri-event-recovery-export.md)
  (R9 recovery curves + crash-vs-dip contrast) and
  [`../../hypotheses/HA-P6/result.md`](../../hypotheses/HA-P6/result.md) /
  [`../../hypotheses/HA-P7/result.md`](../../hypotheses/HA-P7/result.md).
- Literature: `push crash research.md`, `pacing-and-crash-mitigation.md`,
  `reviews/pem_recovery_trajectory_review.md`.
- [CONVENTIONS.md](../../../CONVENTIONS.md) §3.2 (lagged-lcera baseline), §3.6
  (named counts), §4.1 (no interpretive marks).
