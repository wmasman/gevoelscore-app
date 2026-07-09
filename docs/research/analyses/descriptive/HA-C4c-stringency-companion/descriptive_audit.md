# HA-C4c-stringency-companion / descriptive_audit.md

**Status**: **LOCKED r1 2026-07-09** by user acceptance ("Apply now (add
NON-TRIGGER block to audit + lock r1)" 2026-07-09). Step 1 Pass 1 output
of the two-step companion study formalised at
[`hypotheses/HA-C4c-stringency-companion/protocol.md`](../../hypotheses/HA-C4c-stringency-companion/protocol.md)
LOCKED r1 2026-07-09. Distributional-only characterisation of the
T-parameterised operand `bout_n_did_not_return_within_T_day` for
T in {30, 60, 120, 180} minutes over the LOCKED HA-C4c primary stratum;
no effect view, no heavy-T vs non-heavy-T contrast, no crash or gevoelscore
cross-look. Sec 5 f2(T) input table + Sec 5.1 Step-2-decision block
(rule applied 2026-07-09 post-Pass-1 under user authorization): **outcome
NON-TRIGGER** (f2(T) > 0.30 at T in {30, 60}); Step 2 pre-registration does
NOT proceed via this pathway; OI-025 status transitions to
CLOSED-DESCRIPTIVE-ONLY-COMPLETED; guide r3 Sec 4.2.1 condition 2
future-closeability preserved via new OI-033 (personal-baseline SD-anchored
sister-HA pre-reg independent of stringency-family; named same commit-cycle
per user Q "Close OI-025 + name a new OI for Sec 4.2.1 condition 2
keep-alive"). Substantive descriptive-layer observation: monotone descent
of f2(T) corroborates Stage I Sec 3 stringent-operand-threshold
interpretation (CAVEAT-CLASS per CONVENTIONS Sec 4.2; no new inference
beyond HA-C4c LOCKED r2 + Stage I r1).

## Authorship

Drafted 2026-07-09 by Claude (Opus 4.7, 1M context) in reviewer-mode-with-
authorization per [CONVENTIONS Sec 1.2](../../../CONVENTIONS.md#12-producer-vs-reviewer-mode).
Authorising user: Willem. Extraction script + companion data emitted from the
same session; the descriptive audit is the reader-facing summary. Fresh-session
`/research-review` on any downstream Step 2 pre-registration remains required
per [`_plan_results_analysis_layer.md`](../../../methodology/_plan_results_analysis_layer.md)
Sec 4 row for `hypothesis.md`; this audit is Pass 1 output and does NOT
require pre-lock fresh-session review (Pass 1 is distributional-only and
does not license any claim).

**Verification log**:

- Read protocol Sec 2 (LOCKED r1 2026-07-09) as binding scope document; Sec 2.2
  T-parameterisation form, Sec 2.3 five analysis items, Sec 2.4 four Pass 1
  hard walls, Sec 2.5 output artefact spec.
- Read [HA-C4c hypothesis.md](../../hypotheses/HA-C4c/hypothesis.md) Sec 4.2
  stratum + Sec 4.4 day-validity gate + Sec 6 exclusion rules.
- Read [HA-C4c result.md](../../hypotheses/HA-C4c/result.md) Sec 3 + Sec 4
  for the T=180 sanity target (mean 0.6444, median 1.00, sigma 0.6703,
  p25-p75 [0.00, 1.00], range [0.00, 3.00], stratum n=1274 = 465 heavy-T +
  809 non-heavy-T).
- Read [`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md)
  Sec 3.2 return-window rule (LOCKED) as the source form for the
  T-parameterisation.
- Extraction script:
  [`pass1_extract.py`](pass1_extract.py); emitted per Sec 5 below.

---

## 1. Scope

**Stratum** (verbatim from protocol Sec 2.1 = HA-C4c hypothesis.md Sec 4.2 +
Sec 4.4):

> Cross-phase-pooled LC-era days with `citalopram_phase in {unmedicated,
> buildup, consolidation, afbouw, post_afbouw}`; days `>= 2022-11-17`
> (recovery_phase 4b + 5); April 2024 cluster (2024-04-09 to 2024-04-16)
> excluded; 21-day device-baseline-lag excluded per parent MD Sec 3.4;
> `bout_n_did_not_return_day` computable + `exertion_class_lagged_lcera`
> computable per HA-C4c pre-reg Sec 4.4 day-validity gate.

**Stratum day count on this corpus (reproduced from HA-C4c primary)**:
**1274 days** (identical to HA-C4c hypothesis.md Sec 4.7 anticipated ~1274
and to HA-C4c result.md Sec 3 headline n_days total 465 + 809 = 1274).

**Bout population inside the stratum**: **3675 bouts** across the 1274 days
(subset of the 4317 total bouts in `per_bout_master.csv`; the 642 excluded
bouts are on days outside the primary stratum: pre-2022-11-17 phase 4a,
the April 2024 cluster, the 21-day device-baseline-lag, and days missing the
exertion classification per Sec 4.4 gate).

**Pass 1 hard walls in force** (protocol Sec 2.4):

1. No effect view (no heavy-T vs non-heavy-T contrast; no Cliff's delta; no
   Mann-Whitney U; no block-permutation null in this pass).
2. No crash or gevoelscore cross-look (those columns were not read by the
   extraction script).
3. No stratification by `exertion_class_lagged_lcera` in the distributions
   below; the column is used only as a day-validity gate per HA-C4c Sec 4.4.
4. No threshold recommendation from this audit; the Sec 5 f2(T) table is
   emitted as the input to the protocol Sec 4 rule, without classification
   as Trigger / Non-trigger / Ambiguous.

---

## 2. Per-threshold distributions

### 2.1 T = 30 minutes

| metric | value |
|---|---:|
| n_days | 1274 |
| mean | 1.6813 |
| median | 2.00 |
| p25 | 1.00 |
| p75 | 2.00 |
| min | 0 |
| max | 5 |
| sd | 0.8928 |
| **f1(T)** = fraction of days with >= 1 event | **0.9152** |
| **f2(T)** = fraction of days with >= 2 events (**Sec 4 rule input**) | **0.5863** |
| **f3(T)** = fraction of days with >= 3 events | **0.1570** |
| f_zero = fraction of days with 0 events | 0.0848 |
| Poisson-expected zero fraction at observed mean | 0.1861 |
| observed / Poisson zero ratio | 0.4555 |
| per-threshold NaN fraction on stratum | 0.0000 |

### 2.2 T = 60 minutes

| metric | value |
|---|---:|
| n_days | 1274 |
| mean | 1.2732 |
| median | 1.00 |
| p25 | 1.00 |
| p75 | 2.00 |
| min | 0 |
| max | 4 |
| sd | 0.7952 |
| **f1(T)** = fraction of days with >= 1 event | **0.8375** |
| **f2(T)** = fraction of days with >= 2 events (**Sec 4 rule input**) | **0.3846** |
| **f3(T)** = fraction of days with >= 3 events | **0.0479** |
| f_zero = fraction of days with 0 events | 0.1625 |
| Poisson-expected zero fraction at observed mean | 0.2799 |
| observed / Poisson zero ratio | 0.5804 |
| per-threshold NaN fraction on stratum | 0.0000 |

### 2.3 T = 120 minutes

| metric | value |
|---|---:|
| n_days | 1274 |
| mean | 0.8438 |
| median | 1.00 |
| p25 | 0.00 |
| p75 | 1.00 |
| min | 0 |
| max | 3 |
| sd | 0.7145 |
| **f1(T)** = fraction of days with >= 1 event | **0.6648** |
| **f2(T)** = fraction of days with >= 2 events (**Sec 4 rule input**) | **0.1688** |
| **f3(T)** = fraction of days with >= 3 events | **0.0102** |
| f_zero = fraction of days with 0 events | 0.3352 |
| Poisson-expected zero fraction at observed mean | 0.4300 |
| observed / Poisson zero ratio | 0.7794 |
| per-threshold NaN fraction on stratum | 0.0000 |

### 2.4 T = 180 minutes

| metric | value |
|---|---:|
| n_days | 1274 |
| mean | 0.6444 |
| median | 1.00 |
| p25 | 0.00 |
| p75 | 1.00 |
| min | 0 |
| max | 3 |
| sd | 0.6703 |
| **f1(T)** = fraction of days with >= 1 event | **0.5385** |
| **f2(T)** = fraction of days with >= 2 events (**Sec 4 rule input**) | **0.1020** |
| **f3(T)** = fraction of days with >= 3 events | **0.0039** |
| f_zero = fraction of days with 0 events | 0.4615 |
| Poisson-expected zero fraction at observed mean | 0.5249 |
| observed / Poisson zero ratio | 0.8793 |
| per-threshold NaN fraction on stratum | 0.0000 |

**Missingness cross-check**: all four thresholds share the same 1274-day
stratum; the per-threshold NaN fraction is 0.0000 across all T because a
day satisfying the HA-C4c day-validity gate always has at least the
underlying per-minute stress trace + bout extraction populated, and days
with no detected bouts contribute an integer 0 count at every T (per parent
MD Sec 4 aggregation semantics). The identical-missingness sanity per
protocol Sec 2.3 item 4 holds.

---

## 3. Continuous underlying bout-return-time distribution

Bout population: 3675 bouts across the 1274-day stratum. Return-time per bout
is `tail_length` in minutes (parent MD Sec 4; bounded at 180 by the
return-window cap per Sec 3.2 rule (b), and truncated earlier at sleep
onset for sleep-spanning bouts per Sec 3.2 edge case).

**Descriptives on `tail_length` over the stratum's total bout population**:

| metric | value (minutes) |
|---|---:|
| n_bouts | 3675 |
| mean | 73.92 |
| median | 44.00 |
| sd | 67.97 |
| min | 1.0 |
| p05 | 5.0 |
| p10 | 5.0 |
| p25 | 13.0 |
| p50 | 44.0 |
| p75 | 144.0 |
| p90 | 180.0 |
| p95 | 180.0 |
| p99 | 180.0 |
| max | 180.0 |

**Histogram** (10 equal bins from 0 to 180 minutes; counts of bouts per bin):

| bin (minutes) | n_bouts |
|---|---:|
| [0, 18) | 1136 |
| [18, 36) | 513 |
| [36, 54) | 318 |
| [54, 72) | 221 |
| [72, 90) | 174 |
| [90, 108) | 150 |
| [108, 126) | 134 |
| [126, 144) | 106 |
| [144, 162) | 96 |
| [162, 180] | 827 |

**Positioning of the four protocol thresholds against the underlying
distribution**:

- T = 30 min sits between p10 (5.0) and p25 (13.0) shifted right; roughly
  the p33 by inspection of the cumulative histogram (about 1136 + 513 +
  half of the [18, 36) bin have `tail_length <= 30`, or ~1908 of 3675
  ~= 52% of bouts). Correspondingly a bout is flagged
  did-not-return-within-30 for ~48% of bouts (2509 / 4317 at the bout-total
  level per the extraction script log, or a comparable fraction on the
  stratum's 3675).
- T = 60 min sits between p50 (44.0) and p75 (144.0), closer to p50. Cumulative
  through [54, 72) sits at ~2222 / 3675 ~= 60% of bouts have `tail_length
  <= 60`; correspondingly ~40% flagged did-not-return-within-60.
- T = 120 min sits inside the [108, 126) bin, at p75 (144.0) neighbourhood on
  the right. Cumulative ~3009 / 3675 ~= 82% at `tail_length <= 120`;
  correspondingly ~18% flagged did-not-return-within-120.
- T = 180 min is the right edge of the distribution; the p90-p99 range is
  saturated at 180 by construction (the 180-minute forward cap). The 827
  bouts in the [162, 180] bin include the 984 total did-not-return-flag=True
  bouts (across the full 4317-bout population), a fraction of which are also
  sleep-truncated below 180. Approximately 22.5% of the stratum's 3675 bouts
  are in the terminal bin.

The four T cuts sample the return-time distribution at four progressively
right-shifted percentile positions; T=30 near the ~52-percentile of the
tail_length distribution, T=60 near the ~60-percentile, T=120 near the
~82-percentile, T=180 at the terminal saturation point.

---

## 4. Sanity check: T=180 base rate reproduces HA-C4c result.md

Protocol Sec 2.2 anchors the T=180 sanity: the T-parameterised operand
`bout_n_did_not_return_within_180_day` is by construction identical to
HA-C4c's LOCKED primary operand `bout_n_did_not_return_day` (both reduce to
the pipeline's `did_not_return_flag` per parent MD Sec 3.2, since
`tail_length > 180` is empty by construction of the 180-minute cap). The
extraction script asserts this reduction as a structural check
(`assert bouts["did_not_return_within_180_flag"] == bouts["did_not_return_flag"]`),
which passed at runtime (see the script log line
`sanity: T=180 flag == did_not_return_flag: PASS`).

Computed per-day operand statistics on the stratum vs HA-C4c result.md
Sec 3 + Sec 4 anchor:

| statistic | this audit (T=180) | HA-C4c result.md | delta |
|---|---:|---:|---:|
| n_days | 1274 | 1274 (465 + 809) | 0 |
| mean | 0.644427 | 0.6444 | 0.000027 |
| median | 1.00 | 1.00 | 0.00 |
| sd | 0.6703 | 0.6703 | 0.0000 |
| p25 | 0.00 | 0.00 | 0.00 |
| p75 | 1.00 | 1.00 | 0.00 |
| min | 0 | 0.00 | 0 |
| max | 3 | 3.00 | 0 |

**Sanity: PASS.** `|delta_mean|` = 0.000027 << 0.001; all other reported
statistics reproduce HA-C4c result.md Sec 3 + Sec 4 exactly. The stratum
day count of 1274 reproduces both HA-C4c hypothesis.md Sec 4.7 anticipated
n and HA-C4c result.md Sec 3 headline arm-sum. Publication is authorised
per the dispatcher's sanity gate (Sec 5 below emits the Sec 4 rule input
table with confidence).

---

## 5. Pre-committed Sec 4 decision-rule input table

Per protocol Sec 4.2, the primary rule input is `f2(T)` = fraction of stratum
days with `bout_n_did_not_return_within_T_day >= 2`, for T in {30, 60, 120,
180}. The four values from Sec 2 above, collected as a clean table:

| T (minutes) | f2(T) |
|---:|---:|
| 30 | **0.5863** |
| 60 | **0.3846** |
| 120 | **0.1688** |
| 180 | **0.1020** |

**Reader note**: this table is the numeric input to the protocol Sec 4
asymmetric-bar decision rule. The rule was applied 2026-07-09 immediately
post-Pass-1-execution under explicit user authorization ("Apply now (add
NON-TRIGGER block to audit + lock r1)" at the routing question following
Pass 1 completion); outcome + rule-walk + consequences recorded per
protocol Sec 4.6 in Sec 5.1 below. Pass 1 hard wall 4 (no threshold
recommendation) was in force during the extraction + audit drafting; the
Sec 5.1 rule application is a POST-PASS-1 mechanical operation reading
this Sec 5 input table against the LOCKED r1 protocol Sec 4.3 / Sec 4.4 /
Sec 4.5 criteria, and is not a threshold recommendation.

### 5.1 Step-2-decision outcome (per protocol Sec 4.6)

Rule applied 2026-07-09 under user authorization.

**Outcome token**: `NON-TRIGGER (f2(T) > 0.30 at T in {30, 60})`.

**Rule walk** per protocol Sec 4.3 / Sec 4.4 / Sec 4.5:

- **Sec 4.3 Trigger criterion** (f2(T) < 0.10 for ALL T): NOT MET. T=180 =
  0.1020 is above 0.10 (by 0.0020); T=30 = 0.5863 is far above 0.10.
- **Sec 4.4 Non-trigger criterion** (f2(T) > 0.30 for ANY T): **MET** at
  T=30 (0.5863) AND at T=60 (0.3846). Strict Non-trigger rule fires.
- **Sec 4.5 Ambiguous** (any T in [0.10, 0.30] band, absent strict
  Non-trigger fire): NOT APPLICABLE. Strict Non-trigger under Sec 4.4
  fires first; the T=120 value (0.1688) sits inside the [0.10, 0.30]
  band but does not reach the rule since the strict Non-trigger criterion
  already resolved.

**Consequences per protocol Sec 4.4 verbatim discipline**:

- Step 2 pre-registration does NOT proceed via this pathway (2a / 2b / 2c
  paths are NOT triggered by this OI).
- Pass 1 output retained as scoped descriptive artefact (this audit).
- LOAD-BEARING protocol Sec 1.2 attribution NOT operationalised via this
  OI. Stage A [`construct-bout-recovery-signal.md`](../../actionability/construct-bout-recovery-signal.md)
  Sec 5.6 row-4 closure-pathway pointer to OI-025 is exhausted.
- OI-025 in [`_open_inputs.md`](../../../methodology/_open_inputs.md)
  status transitions: PROTOCOL-LOCKED / EXECUTION-PENDING (as of 2026-07-09
  Bundle H) -> CLOSED-DESCRIPTIVE-ONLY-COMPLETED (this event, Bundle H+
  event 4).
- Guide r3 [`actionability_translation.md`](../../../methodology/actionability_translation.md)
  Sec 4.2.1 condition 2 (concrete OI names the closure pathway) requires
  a NEW OI to keep the first-ever operational instance's discipline
  honest. Per user Q "Close OI-025 + name a new OI for Sec 4.2.1 condition 2
  keep-alive" (2026-07-09), a new OI is surfaced in `_open_inputs.md`
  same commit-cycle as **OI-033** (personal-baseline SD-anchored sister-HA
  pre-reg independent of the stringency-family; naming a fresh closure
  pathway analogous to the HA-C3 / HA-C3p sister-pre-reg pattern).

**Substantive descriptive-layer interpretation** (permitted at this layer
as descriptive fact per CONVENTIONS Sec 4.1 descriptive-before-inference;
does NOT license any inference beyond what HA-C4c LOCKED r2 + Stage I r1
already licensed):

The monotone descent of f2(T) from 0.5863 (T=30) to 0.1020 (T=180)
corroborates the Stage I Sec 3 stringent-operand-threshold interpretation
that grounds the HA-C4c PARTIAL magnitude-below-threshold finding. Only
the 180-min operand captures a genuinely tail-rare event (~1 in 10 days
carry two or more); less-stringent thresholds capture progressively more
commonplace patterns (up to ~59% of days at the 30-min threshold). The
3-hour non-return-window operand is doing real work at the stringent
tail-position that Stage I Sec 3 amendment named; the T-parameterisation
family across {30, 60, 120, 180} maps the shape of that tail-position
across the whole return-time distribution.

This descriptive observation is CAVEAT-CLASS per CONVENTIONS Sec 4.2:
it corroborates the stringent-operand-threshold reading without extending
it, without proposing a new operand, and without recomputing any HA-C4c
LOCKED number.

---

## 6. Open inputs / data-quality observations

Data-quality surface observations from the run (protocol Sec 2.3 item 4 +
general audit hygiene). None rise to full OI-queue entries at this pass; the
sibling non-blocking OI-023 already tracks the per-channel missingness
diagnostic on `bout_n_did_not_return` and is unchanged by this audit
(protocol Sec 7.3).

- **Zero-inflation shape across T**: the observed / Poisson zero ratio
  monotonically increases from 0.4555 at T=30 to 0.8793 at T=180. At T=30
  observed zeros are less than half of the Poisson expectation at the
  observed mean, consistent with an over-dispersed positive count
  distribution at short thresholds. At T=180 the observed zero fraction is
  ~88% of the Poisson expectation, close to Poisson-compatible. Descriptive
  observation only; no per-threshold-tuned interpretation is drawn (Pass 1
  hard walls).
- **Sleep-truncation contribution**: 44 of 984 (~4.5%) `did_not_return_flag`
  bouts across the full 4317-bout population are sleep-truncated below the
  180-minute cap (at tail_length < 180 with `truncated_at_sleep_flag=True`).
  The T-parameterisation script counts these as did-not-return-within-T for
  all T (per protocol Sec 2.2 parent-MD-form fidelity); this is a design
  choice that mirrors parent MD Sec 3.2 semantics but readers of downstream
  work should be aware of the subset.
- **Missingness**: zero NaN counts per threshold on the 1274-day stratum
  after `fillna(0)` on days with no bouts. Underlying `bout_n_did_not_return`
  was likewise 0 NaN on the stratum by construction of the Sec 4.4 gate.
- **Motion-confound corpus property carries forward**: 99.3% of all 4317
  bouts carry `motion_confound_flag=True` per HA11-bout-redo result Sec 4
  + HA-C4c result.md Sec 5 motion-clean-only arm reaffirmation. This audit
  did NOT stratify by motion-confound (Pass 1 hard wall 3 spirit + protocol
  Sec 2.5 does not name motion-clean as a Pass 1 slice); any Step 2b or 2a
  pre-reg drafted downstream would inherit the same corpus-property
  observation via HA-C4c Sec 8 caveat 4.

---

## 7. Cross-references

- Binding protocol: [`hypotheses/HA-C4c-stringency-companion/protocol.md`](../../hypotheses/HA-C4c-stringency-companion/protocol.md)
  LOCKED r1 2026-07-09. Sec 2 Pass 1 spec; Sec 4 decision rule (input by
  this audit's Sec 5 f2(T) table); Sec 2.4 hard walls enforced in this audit.
- Parent hypothesis: [`hypotheses/HA-C4c/hypothesis.md`](../../hypotheses/HA-C4c/hypothesis.md)
  r2 LOCKED 2026-06-23. Sec 4.2 stratum + Sec 4.4 day-validity gate
  reproduced by the Sec 4 sanity check.
- Parent result: [`hypotheses/HA-C4c/result.md`](../../hypotheses/HA-C4c/result.md)
  LANDED 2026-06-23. Sec 3 headline + Sec 4 per-day distribution
  characteristics form the T=180 sanity anchor.
- Parent methodology: [`methodology/bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md)
  LOCKED. Sec 3.2 return-window rule form for the T-parameterisation;
  Sec 4 per-bout feature set carries the `tail_length` + `did_not_return_flag`
  columns this audit reads.
- Data dictionary: [`DATA_DICTIONARY.md`](../../../DATA_DICTIONARY.md).
  `bout_n_did_not_return`, `bout_return_time_min`, `pre_bout_baseline`,
  `citalopram_phase` column semantics.
- Stage I closure path 2: [`interpretation/HA-C4c.md`](../../interpretation/HA-C4c.md)
  Sec 4.7 closure-path 2 context (own-research entry 1 at Sec 4.8 seeded
  this two-step study; Sec 4.7's closure discipline binds the downstream
  Step 2 decision).
- Companion data:
  `$GEVOELSCORE_DATA_PATH/analyses/descriptive/HA-C4c-stringency-companion/pass1_distributions.csv`
  (1274 rows; per-day counts at all four T + HA-C4c primary column;
  gitignored per project data-privacy convention).
- Summary metrics:
  `$GEVOELSCORE_DATA_PATH/analyses/descriptive/HA-C4c-stringency-companion/pass1_summary.json`
  (per-threshold summary stats + tail_length quantiles + sanity block;
  gitignored).
- Extraction script (this repo):
  [`pass1_extract.py`](pass1_extract.py). Reproducible from `per_bout_master.parquet`
  + `per_day_master.csv` via a single `python` invocation from repo root.
- Locked plan drift: [`_plan_results_analysis_layer.md`](../../../methodology/_plan_results_analysis_layer.md)
  Sec 4 row for `hypothesis.md`: binds fresh-session `/research-review` on
  any downstream Step 2 pre-registration; does NOT bind Pass 1 output per
  protocol Sec 7.2 rationale.

---

## 8. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-07-09 | **Drafted r1** (reviewer-mode-with-authorization; dispatched-by-orchestrator) | Step 1 Pass 1 output per protocol LOCKED r1 2026-07-09 Sec 2.5. Emitted alongside `pass1_extract.py` + `pass1_distributions.csv` + `pass1_summary.json`. Sanity PASS on T=180: computed per-day mean 0.644427 vs HA-C4c result.md target 0.6444, delta 0.000027 << 0.001 bar; stratum n=1274 reproduces HA-C4c result.md headline. Four hard walls per protocol Sec 2.4 enforced structurally in the extraction script (no effect view; no crash / gevoelscore cross-look; no exertion_class stratification of distributions; no threshold recommendation in the audit). Sec 5 f2(T) table emitted as the input to the protocol Sec 4 asymmetric-bar decision rule; the rule evaluation is a separate downstream event and its outcome is not recorded in this DRAFT r1 audit. Fresh-session `/research-review` NOT dispatched pre-lock: this is Pass 1 distributional output on a follow-on protocol; the plan Sec 4 fresh-session bar applies to any downstream Step 2 pre-registration, not to Pass 1's descriptive audit. Retained as retrospective drift-trigger per plan Sec 3.7. |
| 2026-07-09 | **LOCKED r1 + Sec 5.1 Step-2-decision block added** (post-Pass-1 rule application under user authorization) | User Q "Apply now (add NON-TRIGGER block to audit + lock r1)" at routing question following Pass 1 completion (2026-07-09). Sec 5.1 added with NON-TRIGGER outcome token + rule walk (Sec 4.3 Trigger NOT MET at T=180 = 0.1020 > 0.10; Sec 4.4 Non-trigger MET at T=30 = 0.5863 AND T=60 = 0.3846 both > 0.30; Sec 4.5 Ambiguous NOT APPLICABLE) + consequences per protocol Sec 4.4 discipline (Step 2 pre-reg NOT triggered; OI-025 -> CLOSED-DESCRIPTIVE-ONLY-COMPLETED same commit-cycle; Stage A Sec 5.6 row-4 closure-pathway pointer exhausted; guide r3 Sec 4.2.1 condition 2 future-closeability requires NEW OI; **OI-033** (personal-baseline SD-anchored sister-HA pre-reg independent of stringency-family) surfaced in `_open_inputs.md` same commit-cycle as fresh closure pathway per user Q "Close OI-025 + name a new OI for Sec 4.2.1 condition 2 keep-alive"). Sec 5 Reader note updated to reflect rule application (previously read "deliberately NOT drawn in this audit"; now reads "applied 2026-07-09 post-Pass-1-execution under user authorization"). Status header updated LOCKED r1 with outcome + consequences summary. **Substantive descriptive-layer observation**: monotone descent of f2(T) from 0.5863 (T=30) to 0.1020 (T=180) corroborates Stage I Sec 3 stringent-operand-threshold interpretation as CAVEAT-CLASS per CONVENTIONS Sec 4.2 (no new inference beyond HA-C4c LOCKED r2 + Stage I r1). Fresh-session `/research-review` NOT dispatched for the Sec 5.1 addition: mechanical rule application per protocol Sec 4.6 pre-committed criteria + user-authorized closure of OI-025 + user-authorized surfacing of OI-033 name; no methodology change; no LOCKED-r2 upstream artefact modification. Retained as retrospective drift-trigger per plan Sec 3.7. **Bundle H+ event 4** on origin/main: Track B Pass 1 audit LOCKED r1 + OI-025 closure + OI-033 surfacing. |

---

*End of descriptive_audit.md.*
