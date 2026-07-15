# Post-heavy-day compensatory rest, sleep, autonomic, and subjective trajectories — operand definition

*Producer-mode methodology MD per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-07-15 as r1; pending fresh-session audit per [`/research-methodology-review`](../../../.claude/commands/research-methodology-review.md) before lock.*

---

## Authorship

**Drafted 2026-07-15** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. Subagent-drafted per user delegation; fresh-session `/research-methodology-review` before lock is the discipline mirror to the parent MD [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md).

**Drafting trigger**: [Site R33 Q24 in queued_work.md](queued_work.md#q24-site-r33----compensatory-rest-after-heavy-days-and-whether-it-strengthened-over-time) reached IN-PROGRESS status 2026-07-15 with the Stage -1 heavy-day structural audit LOCKED r1 same day ([`analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md`](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md)). All design decisions for the Q24 sub-parts 1 + 4 + subjective are LOCKED in the Stage -1 audit §7 decision table; this MD is faithful propagation of those decisions into methodology-MD form, NOT design invention.

**Locked decisions at draft time** (all inherited from Stage -1 audit §7, not newly derived):

1. **Unit of analysis**: episode-end (gap=0 contiguous), per-heavy-day as sensitivity.
2. **Windows**: primary 3-day + 5-day; extended 10-day; 14-day dropped (n=5 narrative-only).
3. **Overlap policy**: both strict + inclusive reported side-by-side at all windows.
4. **Comparator**: matched-ordinary day = no-heavy in [D, D+w] + no-crash in [D, D+w] + valid outcome data.
5. **Intensity stratification**: primary=combined; sensitivity arms=very_heavy_only + heavy_only.
6. **Caveats pre-committed**: 7-item list per audit §6.7 (2026 elevation, multi-axis composition, baseline drift, deconditioning, citalopram, small extended-window samples, intensity-stratified sample floor n=19 at +5d).

**Status**: **r1 DRAFTED 2026-07-15**, awaiting fresh-session methodology review. Producer-mode artefact per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); Stage D descriptive audit runs against this operand only after the review verdict clears.

---

## 1. Purpose and scope

### 1.1 What this MD is

An **operand definition** for *post-heavy-day compensatory rest, sleep + autonomic, and paired subjective trajectories* on per-day aggregates (`per_day_master.csv`, LC-era stratum). The MD locks: what a heavy-day trigger is (inherited from HA-C4c definition), what the unit of analysis is (episode-end vs per-heavy-day), what a matched-ordinary comparator looks like, what windows are read, what outcome operand families are computed, what trajectory summary statistics are produced, how the two-clock (subjective vs autonomic) read is pre-committed, and how intensity stratification is handled. Downstream Stage D descriptive audit + any subsequent Stage H pre-registration inherit these as canonical defaults.

### 1.2 What this MD is NOT

- **NOT a hypothesis pre-reg.** No substantive falsification criterion for "learned pacing" or "silent physiological cost" is locked here; those live in per-HA pre-regs that depend on this MD, drafted only after Stage D descriptive results land.
- **NOT a pipeline extraction spec.** The MD names what the Stage D analysis script must consume + produce; the script's construction is a separate downstream session.
- **NOT a per-minute within-day analysis.** Q24 sub-part 2 (within-day shape) stays blocked on per-minute Garmin extraction; this MD covers only the day-aggregate direction. Sub-part 2 will be authored separately when per-minute extraction lands.
- **NOT a phase-stratified read.** Q24 sub-part 3 (over-time / recovery-phase stratification) requires sub-parts 1 + 4 to run first; phase interaction is deferred to a downstream MD once the primary trajectories are characterised.
- **NOT a counterfactual test of pacing efficacy.** Q24 sub-part 5 ("does resting prevent crashes?") is unfalsifiable at n=1 and stays descriptive-bound-at-best; this MD does not attempt it.

### 1.3 Q24 sub-parts covered

| Sub-part | Q24 label | Status | This MD's coverage |
|---|---|---|---|
| 1 | Day-after rest / activity | Feasible on daily aggregates | **Primary — §6.1 activity outcome family** |
| 2 | Within-day shape | Blocked on per-minute extraction | **Out of scope** (deferred) |
| 3 | Over time / phase stratification | Waits on 1 + 4 | **Out of scope** (deferred) |
| 4 | Sleep + autonomic after a heavy day | Feasible on daily aggregates | **Primary — §6.2 sleep + autonomic outcome family** |
| 5 | Does resting prevent crashes | Unfalsifiable counterfactual | **Out of scope** (structural) |
| subjective | Gevoelscore trajectory (new, added at design time) | Feasible; paired channel | **Conditional — §6.3, gated by §8 decision-tree** |

The subjective sub-part is added because Q24's post-heavy question has a felt-state channel that maps cleanly to the two-clock read the [`literature/reviews/pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md) grounds — Radin 2021, Germain 2025, and Buchheit 2013 all support treating subjective and autonomic trajectories as separate clocks that can dissociate in the post-heavy-load window.

### 1.4 Relation to sibling infrastructure

- **HA-C4c / HA-C4cp** (`analyses/hypotheses/HA-C4c-post-heavy-day-recovery/` + `HA-C4cp-post-heavy-day-recovery-personal-baseline/`) use the same heavy-day trigger operationalisation and the same LC-era stratum. Those hypotheses operate on bout-level Garmin stress recovery via [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md); this MD extends the same trigger to day-aggregate outcome families that live outside the per-bout channel.
- **[`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)** (LOCKED r3) serves as this MD's structural precedent. Section-numbering pattern, zero-vs-NaN discipline, and compression + lock discipline are inherited verbatim in spirit.
- **[Stage -1 audit](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md)** is the authoritative source for all design decisions in this MD. Every locked choice traces to a specific section of that audit; see cross-refs throughout.

---

## 2. Stratum and heavy-day definition

### 2.1 Stratum

**LC-era only** (`lc_phase == 'lc'`, i.e. `date >= 2022-04-04`). This matches the HA-C4c / HA-C4cp analytical stratum and the Stage -1 audit corpus (n=1524 LC-era rows per audit §1). Pre-LC dates are structurally out of scope for compensatory-rest analysis because the "heavy day → compensatory response" question presupposes the LC pacing context.

### 2.2 Heavy-day definition (locked, inherited)

A **heavy day** is a day where `exertion_class_lagged_lcera ∈ {heavy, very_heavy}`. The class is the top ~25% of the participant's own LC-era-lagged [d-90, d-30] baseline distribution on the four-axis composite `exertion_rank_composite_lagged_lcera` (aggregating `effective_exertion_min`, `total_steps`, `max_hr_uds`, `vigorous_min_uds`). Same operand used to define HA-C4c's heavy-day stratum.

**Corpus-level counts** (audit §1):

| Class | n days | rate over LC-era |
|---|---:|---:|
| Combined heavy (`heavy ∪ very_heavy`) | **532** | **34.9%** |
| Very-heavy | 256 | 16.8% |
| Heavy-only | 276 | 18.1% |
| Crash days | 103 | 6.8% |
| `exertion_class_lagged_lcera` missing (bootstrap-window + gap days) | 70 | 4.6% |

### 2.3 Rationale for inheritance (not re-derivation)

Per Stage -1 audit §3 threshold-drift check, the four-axis composite class labels are behaving as expected: median rank on heavy days fluctuates 0.63-0.92 across quarters with no monotone drift. The multi-axis composition means a day can score low on one axis and still be classed `heavy` if it scored high on the other three — this is a design feature (audit §3 observation 2), not a bug. Re-defining "heavy" for this MD would fragment cross-test comparability with HA-C4c / HA-C4cp; the inherited definition is the right one.

**Caveat carried forward** (audit §6.7 item 3): the lagged [d-90, d-30] reference is itself drifting. "Heavy" in 2026 does not equate to "heavy" in 2022 in absolute terms. This is a relative-to-recent-past definition and interpretation of trajectory magnitudes must respect it.

---

## 3. Unit of analysis

### 3.1 Primary: episode-end (gap=0 contiguous)

An **episode** is a run of consecutive heavy days with no non-heavy days between them (gap=0 tolerance). An **episode-end** is the last calendar day of that run. Episodes of length 1 are single-day episodes; the episode-end is the day itself.

**Per Stage -1 audit §4**, under the gap=0 definition:
- Total episodes: 314
- Single-day episodes: 188 (59.9%)
- Multi-day episodes: 126 (40.1%)
- Median span: 1 day; p90 span: 3 days; max span: 10 days
- ≥85% of episodes are ≤2 days; ≥93% are ≤3 days

### 3.2 Rationale for episode-end (locked, from audit §6.1)

1. **Convergence with per-heavy-day at strict-clean sample** (audit §5 sanity check): per-heavy-day "no other heavy in [+1, +w]" and per-episode(gap=0) "episode-end with no successor episode in [+1, +w]" converge on the same counts at each window (125 at +3d, 52 at +5d, 12 at +10d). Sample-size case is neutral.
2. **Cleaner semantics**: the participant's post-heavy rest response is presumably to the whole heavy-load event, not to each constituent day of a 2-3-day streak. The last day of the streak marks the transition point after which compensatory response is measured.
3. **Avoids double-counting**: contiguous heavy days would each produce overlapping recovery windows; episode-end reads one trajectory per event.
4. **Precedent alignment**: matches the HA-C4c / HA-C4cp bout-unit precedent (one bout = one recovery-event).

### 3.3 Sensitivity: per-heavy-day

Per-heavy-day trajectories will be reported as sensitivity arms at Stage D, using the same clean-sample filter. This uses the same underlying data and provides a robustness check on the episode-aggregation choice.

### 3.4 Rejected: gap≤1 as primary, gap≤2 out of scope (audit §6.2)

- **gap≤1** (heavy days separated by ≤1 non-heavy day merged into one episode): borderline defensible; some short streaks split by a single rest day may reflect the same load-event. Reported as a **sensitivity arm** only, not primary.
- **gap≤2**: too permissive. Under gap≤2 aggressive merging produces 21-30 day "episodes" that are more accurately characterised as sustained-elevated-load periods with intermittent rest days, not single load-events. **Out of scope** for this MD.

### 3.5 Crash-adjacency handling: compensatory-success vs compensatory-failure split

A heavy episode-end followed by a crash within the trajectory window is **structurally distinct** from a heavy episode-end followed by no crash. The first case IS the compensatory-failure scenario — the participant's post-heavy response did not prevent the crash. The second case is the compensatory-success scenario — the response (whatever it was) was compatible with avoiding a crash inside the window. Pooling both silently into one trajectory conflates the two mechanisms and biases the average toward whichever is more numerous.

**Locked pre-commit** (user-endorsed 2026-07-15):

- **Primary trajectory pool** (compensatory-success): heavy episode-ends satisfying the strict-clean filter (§5.2) AND having **no crash in `[+1, +w]`**. This is the "does resting after heavy prevent bad outcomes?" reading — the pool where compensatory response had space to work.
- **Compensatory-failure sub-arm** (separate report at Stage D): heavy episode-ends satisfying the strict-clean filter AND having a crash in `[+1, +w]`. Reported side-by-side with primary at each window; interpreted as the sub-pool where compensatory response did NOT prevent a crash, whatever the trajectory shape looks like.

**Sample-size implications**: Stage D will discover how many episode-ends per window fall into each pool. The corpus has 103 crash days (audit §1) across the LC-era; the crash rate on days following heavy-episode-ends is unknown pre-Stage-D. If the compensatory-failure pool is small (n<10 at a given window), it is reported as narrative single-case reads only, not as a bootstrap-CI trajectory.

**Interpretive discipline**: the two pools answer **structurally different questions**:
- Primary: what does the trajectory look like when the participant successfully bridges the recovery window without crashing?
- Compensatory-failure sub-arm: what does the trajectory look like when the recovery window is interrupted by a crash?

Neither is the "correct" reading of Q24 in isolation. The comparison between them is directly informative for the Q24.5 sub-part question ("does resting prevent crashes?"), which per §1.3 is descriptive-bound-at-best (unfalsifiable counterfactual) but gets a genuine empirical anchor from this split. **No pre-registered inferential test compares the two pools at Stage D**; the split is descriptive-only at this stage.

**Comparator symmetry** (§4.1 condition 3 already excludes crash-in-window from matched-ordinary): the matched-ordinary comparator pool already requires no-crash-in-window, so both pools' comparators are drawn from the same clean day-pool. Trajectory contrasts are: primary vs matched-ordinary (compensatory-success reading); compensatory-failure sub-arm vs matched-ordinary (compensatory-failure reading). Consistent per-outcome data-validity filter (§4.2) applies to both.

---

## 4. Comparator

### 4.1 Matched-ordinary definition

A **matched-ordinary day** `D_ord` is any LC-era day satisfying **all three** conditions:

1. `D_ord` is not itself a heavy day (`exertion_class_lagged_lcera ∉ {heavy, very_heavy}`).
2. **No heavy day in `[D_ord, D_ord + w]`** for the window `w` under analysis. Symmetric with the heavy-episode-end clean filter (§3.2) applied to the comparator side.
3. **No crash day in `[D_ord, D_ord + w]`**. Uses the `is_crash` column. Crashes contaminate the recovery-trajectory read on either side of the contrast; the comparator must be clean of them.
4. **Valid outcome data across the window** for the specific outcome operand being trajectory-read. Missing-data at any d+k in the window disqualifies the comparator day for that operand only (per-outcome comparator pool, not shared).

Per Stage -1 audit §6.5, the LC-era corpus has 1524 - 532 = **992 non-heavy days** available as candidate comparators; most will meet the "no heavy in window" filter given the corpus's overlap density (audit §5).

### 4.2 Per-outcome comparator pool

Different outcome operands have different missing-data profiles (§6 below). The matched-ordinary comparator pool is therefore **recomputed per outcome** (condition 4 above). Cross-outcome comparability of comparator pools is not enforced; each outcome's trajectory is read against its own valid-data comparator pool.

### 4.3 No propensity matching, no covariate matching

The comparator is *set-membership matched* (heavy-in-window + crash-in-window + data-validity), NOT propensity-matched or covariate-matched. n=1 corpus size makes propensity matching statistically fragile; per [CONVENTIONS §3.1](../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) the personal-baseline framing is the discipline (each day is its own participant's context). Simple set-membership matching preserves interpretability; covariate adjustment enters as sensitivity arms at Stage D only if a specific confound is identified.

---

## 5. Windows and overlap policies

### 5.1 Window ladder (locked, from audit §6.3)

| Window | Role | Strict-clean sample (episode-end) | Interpretability |
|---|---|---:|---|
| **+3d** | Primary | **125** | Chu 2018 24-72h PEM-peak window; comfortable descriptive sample; bootstrap-CI reads reliable |
| **+5d** | Primary | **52** | Chu peak + early decay; small but usable descriptively; block-permutation null still viable |
| **+10d** | Extended | **12** | Descriptive-only; matches Radin 2021 autonomic-tail expectation partially (Radin's 79d tail is population-scale acute-COVID, not per-episode); too small for null-hypothesis tests |
| ~~+14d~~ | Dropped | 5 | Narrative single-case reads only; not a primary trajectory read |

The +14d window is dropped per audit §6.3 because n=5 does not support even bootstrap-CI reads. It may appear at Stage D as narrative single-case examples but does not participate in the primary trajectory summary statistics.

### 5.2 Overlap policies (both reported side-by-side, from audit §6.4)

At **each window**, two trajectories are computed:

- **Strict-clean**: only episode-ends with no other heavy day in [+1, +w] (samples per §5.1 above).
- **Inclusive**: all episode-ends (n=314 gap=0), with the trajectory interpreted as "response to the entire multi-day heavy-load context spanning the window", not to the target episode alone. Under inclusive policy the block-permutation null (§7.9 below) uses block length ≥ w to preserve the autocorrelation structure the policy admits.

Per audit §6.4 rationale: strict gives clean semantics but small sample; inclusive gives full sample but the trajectory reflects sustained-load response. Reporting both surfaces the sample-size vs semantic-cleanness tradeoff transparently. **Convergence of the two policies on trajectory shape is itself informative** (finding is robust to policy). **Divergence between the two is a finding** — it identifies operand-behaviour that depends on the clean-window assumption.

### 5.3 Post-window vs symmetric-window scan

The overlap filter is **post-window** (`[D+1, D+w]`), not symmetric (`[D-w, D+w]`). This follows the audit §5 discipline and the compensatory-rest question's directional framing: the analytical question is what happens *after* the heavy episode, not whether the episode itself was preceded by other heavy days. Pre-episode contamination is a separate (Q24 sub-part 3, deferred) question about episode buildup.

---

## 6. Outcome operand families

### 6.1 Activity / exertion (Q24 sub-part 1)

Outcome columns computed at each d+k in the window `[D+1, D+w]`:

| Column | Definition | LC-era coverage |
|---|---|---:|
| `total_steps` | Garmin daily step count | 98.5% |
| `effective_exertion_min` | Composite exertion in minutes (primary activity axis) | 100.0% |
| `vigorous_min` | Minutes above vigorous-intensity threshold | 98.6% |
| `active_sec` (report as `active_sec / 60` = active_min) | Total active seconds | 98.6% |
| `exertion_class_lagged_lcera` | Categorical class at d+k; report as class-distribution + as prob(heavy at d+k) | 95.4% |

**Definitional-pair discipline** (CONVENTIONS §3.3): `effective_exertion_min` is the primary composite activity axis; `total_steps` + `vigorous_min` + `active_sec` are correlated definitional siblings that carry channel-specific information but should not be treated as independent evidence. At Stage D each is read against the comparator individually; multiplicity-correction across the family is a Stage-D pre-reg decision (single-cell headline lock + Holm step-down across companions is the project-canonical default per [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) §5.2).

The categorical `exertion_class_lagged_lcera` at d+k is the direct falsifier of the "learned pacing → less heavy-load in recovery window" reading: it asks how often the day after a heavy-episode-end is itself heavy, and how that compares to matched-ordinary day-after distributions.

### 6.2 Sleep + autonomic (Q24 sub-part 4)

Outcome columns computed at each d+k in the window `[D+1, D+w]`. Formulas for the sleep operands are locked in [`sleep_metrics.md`](sleep_metrics.md) (the canonical sleep-operand catalogue); this table cites the columns Q24 consumes without re-defining the formulas inline.

| Column | Definition | LC-era coverage | Notes |
|---|---|---:|---|
| `sleep_duration_min` | Total sleep minutes | 97.0% | Sleep quantity. Family A per [`sleep_metrics.md`](sleep_metrics.md) §4. |
| `sleep_deep_min` | Deep-sleep minutes | 97.3% | Sleep architecture: deep. Family A. |
| `sleep_light_min` | Light-sleep minutes | 97.3% | Sleep architecture: light. Family A. |
| `sleep_rem_min` | REM-sleep minutes | 95.5% | Sleep architecture: REM. Family A. **Added at Stage 3b**: promoted to PRIMARY sleep-architecture outcome after the Stage 3a extractor correction landed `sleep_rem_min` extraction (the earlier "no REM on FR245" assertion was factually wrong per [`sleep_metrics.md`](sleep_metrics.md) §4.2). |
| `sleep_awake_min` | Awake-in-bed minutes | 97.3% | Sleep architecture: awake. Family A. |
| `sleep_efficiency_tib` | `(sleep_duration_min - sleep_awake_min) / sleep_duration_min` — CANONICAL sleep-medicine formula | 96.7% | Bounded [0, 1]; NaN if either input NaN OR `sleep_duration_min == 0`. Family A. Definitional-pair sensitivity variant `sleep_efficiency_staged` is defined in [`sleep_metrics.md`](sleep_metrics.md) §4.4 and read as a sensitivity operand per §6.2.3 below. |
| `stress_mean_sleep` | Garmin sleep-window stress (HRV-proxy) | 97.0% | Autonomic overnight proxy. Family D. |
| `all_day_stress_avg` | Daytime Garmin stress mean | 98.6% | Autonomic waking proxy. |
| `bb_lowest` | Body-battery daily floor | 98.6% | Autonomic reserve proxy. |
| `bb_overnight_gain` | Overnight body-battery gain | **38.9%** | **Sensitivity-only** — see §6.2.1 below. Family E. |
| `hr_median_waking` | Median waking-window heart rate | 98.4% | Morning-HR proxy — see §6.2.2 caveat. |

**Definitional-pair discipline** (CONVENTIONS §3.3): `stress_mean_sleep` and `all_day_stress_avg` are the two Garmin stress channels; `bb_lowest` is the reserve floor. All three inherit the Firstbeat-input opacity caveat per [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md); they are *operational* descriptors of the Garmin trace, not mechanistic autonomic measurements. Sleep-architecture minutes (`sleep_deep_min`, `sleep_light_min`, `sleep_rem_min`, `sleep_awake_min`) sum to `sleep_duration_min` in the raw data; report the four stages side-by-side without inflating them into independent tests. `sleep_efficiency_tib` (canonical) and `sleep_efficiency_staged` (sensitivity variant, defined in [`sleep_metrics.md`](sleep_metrics.md) §4.4) are the two efficiency channels; pick one per analysis.

**Stress framing note** (per user convention): "stress" in this MD refers to Garmin's HRV-derived score, never mental/emotional stress. `stress_mean_sleep` is the overnight autonomic load channel; `all_day_stress_avg` is the daytime autonomic load channel.

#### 6.2.1 `bb_overnight_gain` sparse-availability handling

Data-availability check ran 2026-07-15 on the LC-era stratum (n=1524):

| Variant | LC-era coverage |
|---|---:|
| `bb_overnight_gain` | 38.9% |
| `bb_overnight_gain_best` | 43.8% |
| `bb_overnight_gain_proxy` | 43.8% |

**None of the three variants exceeds 80% coverage.** Per the operand-selection rule, `bb_overnight_gain` is flagged **sparse-availability** and **downgraded to sensitivity-only** in this MD. Rationale: at ~40% coverage, matched-comparator pool intersections shrink materially (both trigger-side and comparator-side must have valid data at every d+k in the window), pushing the effective sample below the interpretability floor for extended windows.

**Stage D handling**: `bb_overnight_gain` (using the `bb_overnight_gain_best` variant, tied with `_proxy` on coverage and closer in name to the primary column) is read only at the +3d window where sample loss is minimal, and only as a companion to the primary sleep + autonomic channels (§6.2 above). It does not participate in the +5d or +10d primary trajectory reads. Report coverage-per-arm explicitly at Stage D.

#### 6.2.2 `hr_median_waking` and the HRM4Pacing caveat

`hr_median_waking` inherits the HRM4Pacing / Clague-Baker 2023 measurement-input caveat surfaced by [Q25 in queued_work.md](queued_work.md#q25-site-r34----re-test-morning-rhr-with-an-overnight-average-hr-proxy-hrm4pacing-caveat): Garmin-reported "RHR" is a lowest-sustained figure rather than a true resting HR, and the HRM4Pacing tradition warns that for ME/CFS-adjacent cohorts the lowest-vs-average gap may misrepresent autonomic state. `hr_median_waking` is a *median-over-waking-window* proxy that partially sidesteps the caveat (it is not Garmin's "RHR" column), but it is still a Garmin-derived HR aggregate on top of a device baseline that has known amplification at rest.

**Stage D handling**: report `hr_median_waking` trajectories with a footnote citing the HRM4Pacing caveat; if the trajectory shows a strong signal, sensitivity to the measurement-input choice is a caveat-class item (CONVENTIONS §4.2), not a re-analysis trigger.

#### 6.2.3 Sensitivity-tier sleep operands

The following operands are read at Stage D as sensitivity companions to the §6.2 primary set. All formulas + coverage + caveats live in [`sleep_metrics.md`](sleep_metrics.md); this section names the six sensitivity operands Q24 consumes and states the per-operand rationale for sensitivity-tier placement.

| Operand | Family (per [`sleep_metrics.md`](sleep_metrics.md)) | Rationale for sensitivity-tier placement |
|---|---|---|
| `sleep_efficiency_staged` | A | Cross-check vs `sleep_efficiency_tib` primary. Definitional-pair per CONVENTIONS §3.3 + `sleep_metrics.md` §4.4. Divergence between the two on nights with non-trivial `sleep_unmeasurable_min` is itself a finding. |
| `bb_overnight_gain` | E | Existing sparse-availability channel (38.9% LC-era). Handled at +3d window only per §6.2.1; unchanged at Stage 3b. |
| `bb_overnight_gain_frac` | E | Ceiling-corrected variant of `bb_overnight_gain` (per `sleep_metrics.md` §8.3). Answers "did the recharge fill the available reserve?" vs the raw "how many BB units?"; useful when heavy-day night starts at low BB (large recharge available) vs high BB (small ceiling). Same sparse-availability caveat as `bb_overnight_gain` — read at +3d only. |
| `sleep_hr_avg_spo2` | D | Overnight-HR proxy (93.0% LC-era). Directly relevant to Radin 2024 Long COVID nightly-HR persistence finding per [`literature/reviews/pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md). Sensitivity because it introduces a third HR channel alongside `hr_median_waking` (primary) and `resting_hr` (companion) — cross-channel divergence is informative but not primary-load-bearing. |
| `spo2_avg_sleep` | D | Existing sensitivity channel (84.8% LC-era; Pulse Ox Sleep Mode toggle constrained). Wiggers G4 deprioritised; included for completeness. |
| `asleep_stress_max_uds` | D | UDS-aggregated sleep-window peak stress (97.9% LC-era); arousal-peak proxy complementing the `stress_mean_sleep` primary mean-of-sleep-window channel. Sensitivity because a peak-vs-mean divergence in trajectory shape is informative but the mean is the primary load-bearing channel. |

**Direction pre-commits for sensitivity operands** (extension of §7.7):
- `sleep_efficiency_staged`: same direction as `sleep_efficiency_tib` (cost-of-heavy-load = negative).
- `bb_overnight_gain_frac`: same direction as `bb_overnight_gain` (cost-of-heavy-load = negative; recharge fraction depressed after heavy day).
- `sleep_hr_avg_spo2`: same direction as `hr_median_waking` (cost-of-heavy-load = positive; elevated overnight HR).
- `asleep_stress_max_uds`: same direction as `stress_mean_sleep` (cost-of-heavy-load = positive; elevated sleep-window arousal peak).

**Stage D reporting discipline**: sensitivity-tier operands are read side-by-side with primary at every reported window; convergence with the primary is a robustness finding, divergence is a finding in its own right (per CONVENTIONS §4.2).

### 6.3 Subjective paired (Q24 subjective, conditional)

Outcome column computed at each d+k in the window `[D+1, D+w]`:

| Column | Definition | LC-era coverage |
|---|---|---:|
| `gevoelscore` | Self-rated felt-state (1-10 scale) | **90.0%** |

The subjective channel is the participant's daily felt-state rating. Its coverage (90.0%) is lower than the sleep + autonomic channels (~97%) because it is manually entered rather than device-derived; missing-data days for `gevoelscore` are days without a manual entry, not days with a "zero" score.

**Conditional use** (§8 decision-tree): the subjective channel is paired against the autonomic channels for the two-clock read but its trajectory is descriptively reported unconditionally. The pre-committed decision-tree (§8) governs the interpretive framing of the paired read.

### 6.4 Zero-vs-NaN discipline (per §11 below)

Under no circumstance is `.fillna(0)` applied to any outcome trajectory value. Missing data at d+k means missing observation, not zero response. See §11 for the full policy.

### 6.5 Explicit exclude — Family B (regularity / consistency) reserved for Q24 sub-part 3

Family B operands per [`sleep_metrics.md`](sleep_metrics.md) §5 — Sleep Regularity Index (SRI) 7d + 14d, `bedtime_std_14d`, `waketime_std_7d`/`_14d`, `midpoint_std_7d`/`_14d`, `sleep_duration_std_7d`/`_14d` — are **NOT read at the +3d / +5d / +10d day-after trajectory windows** in Q24 sub-parts 1 + 4 + subjective. Rationale:

- Family B operands are rolling-window multi-night constructs (7d or 14d windows). Reading them at d+3 after a heavy episode conflates the post-episode response with the last three days of the pre-episode window — the wrong reference frame for the day-after-trajectory question.
- Regularity is a between-phase construct (comparing regularity across LC phases, or across pre- vs post-intervention epochs), not a day-after-trajectory construct.
- Family B is the natural analytical home for Q24 sub-part 3 (phase-stratification: does the compensatory-rest response strengthen over time?). See [`sleep_metrics.md`](sleep_metrics.md) §5.4 for the operand-catalogue-level framing.

**Exception**: the currently-implemented Family B operand `bedtime_std_7d` (per DATA_DICTIONARY §7) is a rolling channel that could in principle be read at d+3 as a "did the participant's bedtime regularity drift after the heavy episode?" outcome. Q24 declines to read it at the trajectory windows for the same reason above — the rolling-window construction makes the d+3 reading conflate the pre- and post-episode contribution. If a downstream analysis needs a bedtime-drift-after-heavy-day operand, it should be a per-day operand (e.g. `|bedtime_hour_local(d+k) - bedtime_hour_local(D)|`), not a rolling-std channel.

---

## 7. Trajectory summary statistics

For each `(outcome operand, window, overlap-policy, trigger-stratum)` combination, the trajectory is a vector of values across d+1, d+2, ..., d+w. Nine summary statistics are computed per trajectory (per audit §7 discipline gate + this MD's operand lock):

### 7.1 Per-day mean ± bootstrap CI at each d+k

Vector of per-d+k means for the heavy-arm and matched-ordinary-arm, with bootstrap 95% CIs (block bootstrap per §7.9). Primary descriptive output; feeds the trajectory-plot deliverable at Stage D.

### 7.2 Mean-trajectory difference vector (heavy − matched-ordinary at each d+k)

Vector `Δ(k) = mean_heavy(d+k) − mean_matched_ordinary(d+k)` for k = 1, ..., w, with bootstrap-CI bands per k. This is the core contrast — the observed *shape* of the heavy-vs-ordinary post-episode divergence.

### 7.3 AUC (cumulative sum over window)

`AUC = Σ_{k=1..w} Δ(k)`. Scalar per (outcome, window, overlap, stratum). Sensitive to total cumulative effect across the window; robust to individual-day noise. Bootstrap 95% CI reported.

### 7.4 Slope (linear fit through trajectory)

Linear regression slope of `Δ(k)` on `k`. Scalar per (outcome, window, overlap, stratum). Positive slope on a decay-outcome (e.g. `stress_mean_sleep`) would indicate widening divergence over the window; negative slope indicates re-convergence.

### 7.5 Peak-location (which d+k the extremum sits at)

Integer `k*` ∈ {1, ..., w} where `|Δ(k)|` is maximal. Directly tests the **delayed-onset prediction** — the literature review (Chu 2018) documents PEM onset can lag the trigger by 24-72h, so k*=2 or 3 for autonomic outcomes would be consistent with delayed-onset. Reported with a peak-magnitude value.

### 7.6 Return-to-baseline time (RTBT)

First d+k where `Δ(k)` re-crosses the matched-ordinary median (or a pre-specified baseline reference). Integer ∈ {1, ..., w, w+1}; the value `w+1` is a censored "did not return within window" outcome (analogous to the parent MD's `did_not_return_flag`). **Literature-central metric per Moore 2023** (mean recovery time = 12.7d in ME/CFS, range 1-64d); the corpus's shorter windows (3d / 5d / 10d) put most heavy-episode RTBTs at the censored bound, and the censored-rate itself is the informative comparison to the matched-ordinary arm.

### 7.7 Below-baseline day count

Discrete count: how many d+k in the window have `Δ(k) < 0` (for outcomes where "below matched-ordinary" is the physiologically-meaningful direction — e.g. total_steps, effective_exertion_min: fewer steps after heavy day) OR `Δ(k) > 0` (for stress/autonomic-load outcomes where "above matched-ordinary" is the physiologically-meaningful direction — e.g. stress_mean_sleep, hr_median_waking: elevated load after heavy day). Robust to per-day noise; simple to interpret.

**Direction pre-commit per outcome**:
- Activity outcomes (`total_steps`, `effective_exertion_min`, `vigorous_min`, `active_sec`): "compensatory response" direction is **negative** (fewer than matched-ordinary).
- Sleep-quantity outcomes (`sleep_duration_min`, `sleep_deep_min`): "compensatory response" direction is **positive** (more than matched-ordinary).
- Sleep-architecture REM (`sleep_rem_min`): direction is **bidirectional per literature** with a compensatory reading of **positive** (↑ after heavy day = compensatory; REM rebound after sleep deprivation is classical). Report both directions; a negative-direction finding is a substantive result in its own right, not a sign inversion of the expected axis. Anchor: general sleep-medicine REM-rebound literature; the specific PEM/LC anchor is thin (Mekhael 2022 reports LC sleep-architecture disturbance without a pinned direction on REM specifically per [`literature/reviews/pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md)).
- Autonomic-load outcomes (`stress_mean_sleep`, `all_day_stress_avg`, `hr_median_waking`, `sleep_awake_min`): "cost of heavy load" direction is **positive** (elevated above matched-ordinary).
- Reserve outcomes (`bb_lowest`, `bb_overnight_gain`, `sleep_efficiency_tib`): "cost of heavy load" direction is **negative** (depressed below matched-ordinary).
- Subjective (`gevoelscore`): "cost of heavy load" direction is **negative** (worse than matched-ordinary).

These directions are the pre-committed reading axis; opposite-direction findings are reported as sign-inversions (findings in their own right per CONVENTIONS §4.2).

### 7.8 Trajectory variability

`std(Δ(k))` across k = 1, ..., w. Scalar per (outcome, window, overlap, stratum). **Autonomic-instability proxy per Radin 2021** — the biphasic dip-then-elevated post-COVID RHR pattern would show up here as high trajectory variability even when AUC is small. Reported alongside slope for characterisation.

### 7.9 First-crossing day

First d+k where `Δ(k)` falls outside the matched-ordinary arm's bootstrap 95% CI. Integer ∈ {1, ..., w, w+1}; `w+1` is a censored "trajectory never diverges significantly" outcome. Tests the **delayed-onset prediction** at the arm-comparison level (§7.5 tests it at the extremum-location level).

---

## 8. Decision-tree gates for the two-clock read

Per the literature review's core dissociation observation (Radin 2021 objective-slow / behavioural-fast; Germain 2025 molecular-peak-during-subjective-recovery; Buchheit 2013 channel-specific recovery clocks), the paired subjective vs autonomic trajectory read is **pre-committed** into four branches. All four are pre-committed outcome space; interpretation is disciplined regardless of which fires. This closes the "was the subjective response found, or was the autonomic response found?" degrees-of-freedom hole up front.

The decision-tree operates on **Stage D descriptive verdicts** — specifically the "decay" pattern of each channel across the +3d + +5d primary windows. "Decay" here means: the trajectory-difference vector `Δ(k)` starts at some nonzero magnitude at d+1 and monotonically (or near-monotonically) returns toward zero by d+w. "Sustained" means: no decay pattern; `Δ(k)` stays at similar magnitude across the window.

### 8.1 Pre-committed decay-screen operationalisation (peak-based, per-channel)

For a given channel and window, "decays" is operationalised as:

`|Δ(w)| / |Δ(k*)| < 0.5`

where `k* = argmax_{k ∈ [1, w]} |Δ(k)|` is the **peak-location** per §7.5 — the day in the window at which the trajectory-difference magnitude is largest. "Decays" means the divergence at window end is less than half the peak divergence within the window.

**Rationale for peak-based (not window-start-based) formulation** (user-endorsed 2026-07-15):

- The naive `|Δ(w)| / |Δ(1)| < 0.5` rule is **unstable under delayed onset**. Chu 2018 documents PEM onset can lag the trigger by 24-72h, so `|Δ(1)|` may be near-zero even when a true recovery signal is present at k*=2 or k*=3. In that case the ratio is ill-defined (denominator→0) or produces a false "no decay" verdict because `|Δ(1)|` ≈ `|Δ(w)|` when both are near-zero.
- Peak-based normalisation handles delayed onset naturally: the divergence is measured relative to when it was largest, not when the trigger occurred. This aligns with the literature's expected shape (delayed peak followed by decay) rather than assuming a monotonically decreasing pattern.
- The 0.5 threshold is preserved as a pre-committed structural threshold, not data-driven. It corresponds to "at least half the peak divergence has recovered by window end" — a conservative operationalisation of decay that avoids false-positive-decay from a single-day dip.

**Screens run per channel, not on a single primary channel** (user-endorsed 2026-07-15):

- **§8a subjective decay screen**: one screen on `gevoelscore` (paired subjective channel per §6.3).
- **§8b autonomic decay screens (per-channel)**: independent screens on **each autonomic channel** in the primary set: `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`, `hr_median_waking`, `sleep_hr_avg_spo2` (five channels; the last from the sleep-metrics arc).

The autonomic decision-tree branch verdict is **per-channel**, not compressed into a single primary channel. This preserves information about channel-disagreement — a case where `stress_mean_sleep` decays but `hr_median_waking` does not is itself a substantive finding about which autonomic axis carries the recovery signal (per Radin 2024's nightly-HR-persistence finding, `sleep_hr_avg_spo2` may sit closer to the literature-predicted slow tail than `stress_mean_sleep`).

**Rationale for per-channel (not composite) analysis**: (a) a composite z-score index would collapse the very information the decision-tree is designed to preserve; (b) channels have known differential validity on FR245 (Miller 2022 sleep-stage κ=0.25 "poor" vs timing/duration κ=0.35; Firstbeat opacity per `hrv_proxy_via_stress.md`), and a composite propagates the weakest input; (c) with 5 autonomic channels × 4 branches = 20 potential channel-branch combinations, per-channel reporting adds columns to the Stage D output table but no interpretive overhead — the branch definition is uniform.

### 8.2 Four branches (per autonomic channel)

For each `(autonomic channel c, window w, overlap policy p)` combination, the branch verdict is:

| Branch | Subjective decays | Autonomic channel `c` decays | Interpretation | Pre-reg pathway |
|---|:---:|:---:|---|---|
| **BOTH decay** | Yes | Yes | Two-clock comparison is well-formed for channel `c`. Test whether subjective decays FASTER (literature prediction: felt-state fast, autonomic slow per Radin + Germain). If subjective decays faster: literature-concordant two-clock finding for channel `c`. If equal or autonomic faster: reversal-of-literature finding for channel `c`. | **Candidate for Stage H pre-reg** — two-clock comparison test on channel `c` |
| **ONLY autonomic decays** | No | Yes | "Silent physiological cost" pattern on channel `c`: felt-state does not decay in the observation window while autonomic axis `c` settles. Structurally distinct from the literature's "felt-fast / autonomic-slow" — this is "autonomic-fast / felt-stuck-elevated" on channel `c`. Name + describe. | **Candidate for autonomic-side pre-reg** on channel `c` |
| **ONLY subjective decays** | Yes | No | Literature-inversion anomaly on channel `c`: felt-state recovers but autonomic axis `c` sustained. Look for confounds first (measurement drift, medication, sleep architecture change). | **Descriptive only, no pre-reg**; report as anomaly with confound audit |
| **NEITHER decays** | No | No | Null on channel `c` at window `w`. Both the subjective channel and autonomic channel `c` sustained above matched-ordinary across the observation window. May indicate the window is too short (Moore 2023 range 1-64d; the corpus's max 10d window would truncate long-tail recovery), or the corpus's heavy-load bar is too soft to produce meaningful decay on channel `c`. | **Report as null; no pre-reg**; extend to +10d for descriptive-only characterisation |

**Reporting format**: Stage D produces a matrix of branch verdicts, one row per autonomic channel × primary window (5 channels × 2 windows = 10 rows at primary; 5 additional rows at extended +10d = 15 total branch verdicts).

### 8.3 Discipline

The four branches are pre-committed **before** Stage D descriptive results land. Any post-hoc branch definition (e.g. "well, ¾ decay could count as decay too") is disallowed per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference. Which branch fires per channel is a descriptive verdict; interpretation of that verdict follows the pre-committed reading in §8.2.

**Cross-window discipline**: the decay screens run **at each primary window** (+3d + +5d). If the branches disagree across windows for the same channel (e.g. BOTH-decay at +3d, ONLY-autonomic-decay at +5d on `stress_mean_sleep`), the branch-disagreement is itself a finding and both branch verdicts are reported for that channel.

**Cross-channel discipline** (user-endorsed 2026-07-15): the decay screens run **per autonomic channel independently**. If the branches disagree across channels at the same window (e.g. BOTH-decay on `stress_mean_sleep` but ONLY-subjective-decay on `hr_median_waking` at +5d), the channel-disagreement is itself a substantive finding — it identifies which autonomic axis carries the recovery signal (or lack of it) on this corpus. Report all per-channel branch verdicts side-by-side; do not compress into a "majority verdict" or a "primary channel wins" rule. Channel-disagreement points at operand-behaviour differences that a composite would hide.

**Cross-stratum discipline**: the decay screens run **at the combined-primary stratum** (§9 primary). Intensity-stratified branches (very_heavy_only, heavy_only) are read descriptively at Stage D but not gated by the four-branch decision-tree — the intensity arms may support or complicate the primary branch verdict but do not overturn it.

**Cross-pool discipline** (per §3.5): the decay screens run on the **compensatory-success primary pool**. The compensatory-failure sub-arm gets its own descriptive read at Stage D (per §3.5) but is not gated by the four-branch decision-tree; the sub-arm's trajectory interpretation is inherently different (the recovery window was interrupted by a crash, so "decay" and "sustained" carry different semantic weight).

---

## 9. Intensity stratification

Per Stage -1 audit §6.6, an intensity-stratified sensitivity arm is pre-committed to test whether trajectory magnitude/shape scales with intensity (Van Campen 2020 severity-scaling prediction; Moore 2023 severity-related recovery variance).

### 9.1 Three triggers

| Trigger | Definition | Primary sample (+3d strict-clean, episode-end) |
|---|---|---:|
| **Combined** | `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` | **125** (episode-end gap=0 strict-clean at +3d) |
| **Very-heavy only** | `exertion_class_lagged_lcera == 'very_heavy'` | **52** (very_heavy-triggered + combined-clean at +3d) |
| **Heavy only** | `exertion_class_lagged_lcera == 'heavy'` (excluding very_heavy) | **73** (heavy-only-triggered + combined-clean at +3d) |

**Cross-stratum scan discipline**: for the intensity-stratified triggers, the "clean" filter uses **combined heavy as the scan set**, not the trigger stratum alone. A very_heavy-episode followed by intervening heavy days contaminates the recovery window just as much as an intervening very_heavy day would (per audit §5 cross-stratum table). This is why very_heavy-triggered + combined-clean gives n=52 at +3d, matching the combined-primary +5d sample coincidentally.

### 9.2 Read policy by window

| Window | Combined (primary) | Very-heavy only | Heavy only |
|---|:---:|:---:|:---:|
| **+3d** | Full read (n=125) | Full read (n=52) | Full read (n=73) |
| **+5d** | Full read (n=52) | **Descriptive-with-CI only** (n=19) | Descriptive-with-CI only (n=33) |
| **+10d** | Descriptive only (n=12) | Not viable (n=5) | Not viable (n=7) |

**Rationale** (from audit §6.6 + §5): the very_heavy_only + combined-clean floor at n=19 (+5d) is the intensity-stratified sample-size limit for descriptive-with-CI reads. Below n=15 (very_heavy at +10d: n=5; heavy_only at +10d: n=7) the sample supports narrative single-case reads only.

### 9.3 Analytical target

Does the trajectory magnitude/shape scale with intensity (dose-response inside the heavy-load band)?

- **Scaling present**: very-heavy-triggered trajectory divergence exceeds heavy-only-triggered divergence in magnitude, with combined sitting between. Supports the multi-tier heavy-day definition itself + Van Campen 2020's severity-scaling prediction transferred to n=1.
- **Scaling absent**: heavy is a uniform-response bucket; the very_heavy tier is a definitional artefact of the composite threshold, not a physiologically-distinct load level.
- **Scaling reversed**: heavy-only-triggered divergence exceeds very-heavy-triggered. Would indicate the composite class labels are misspecified relative to the outcome operand.

All three outcomes are descriptively reportable; no pre-committed falsifier at Stage D. The intensity-stratified read is a *characterisation* of the operand behaviour, not a hypothesis test.

---

## 10. Confounds pre-committed as caveats

Per Stage -1 audit §6.7 + [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class discipline. Each of the following is acknowledged as an uncorrected confounder; NONE is claimed to drive the trajectory outcomes a-priori.

1. **2026 heavy-rate elevation** (audit §2): 47.4% partial-year rate vs ~34-35% baseline for 2023-2025. Three non-exclusive readings all supportable: (a) genuine load increase; (b) baseline drift (the [d-90, d-30] lagged reference has fallen); (c) seasonal artefact (2026 is Jan-Jun partial only). **Stage D handling**: report primary trajectories on the full LC-era corpus; report a sensitivity trajectory excluding 2026; if the two disagree substantially, escalate the 2026 stratum as a finding.

2. **Multi-axis heavy-day composition** (audit §3): the four-axis composite means heavy days vary in axis-dominance over time; the 2022 heavy day and the 2026 heavy day may be dominated by different axes. Not stratified in primary read. Reported as caveat; a future sensitivity arm may stratify by axis-dominance.

3. **Baseline drift** (audit §3, §2): the lagged [d-90, d-30] reference itself drifts. The heavy-day definition is relative-to-recent-past, not absolute. Interpretation must respect that "heavy" is a rolling-relative label. Caveat-class.

4. **Deconditioning**: the participant's baseline exertion capacity has shifted downward across the LC era; fewer / lighter days recently could produce a floor effect (fewer post-heavy activity units are available) that mimics compensatory-rest without a behavioural-choice interpretation. Caveat-class; not corrected in the primary read.

5. **Citalopram-era vs non-citalopram-era**: medication onset 2024-04-09 splits the corpus into two dose-state populations; citalopram is known to modulate autonomic channels per [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md). Stage D primary read pools across dose-state; phase-stratified sensitivity is Q24 sub-part 3 (deferred). Caveat-class; a strong Stage D finding will motivate Q24 sub-part 3 authorship.

6. **Small extended-window samples** (audit §5): 52 at +5d, 12 at +10d — CI-based reads only, no formal null-hypothesis tests at extended windows. Reported explicitly per window; sample-size floor is not "corrected" but is bounded by policy.

7. **Intensity-stratified sample floor n=19 at +5d** (audit §6.6): very_heavy_only + combined-clean at +5d is descriptive-with-CI only, not viable for null-hypothesis tests. Explicit constraint at Stage D reporting.

---

## 11. Zero-vs-NaN discipline

Per [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) §5 pattern, extended to this MD's outcome operands.

**Never `.fillna(0)` on any trajectory outcome.** Missing data at d+k means missing observation, not zero response. The following per-outcome policies apply:

- **`total_steps`**: missing data = uninstrumented day (Garmin not worn or not syncing), NOT zero steps. Zero-value days (Garmin worn, zero steps) are legitimate observations and remain in the trajectory.
- **`sleep_duration_min`, `sleep_deep_min`, `sleep_light_min`, `sleep_rem_min`, `sleep_awake_min`**: missing data = uninstrumented night, NOT zero-sleep. A missing-sleep night disqualifies the day from sleep-outcome trajectory reads only. `sleep_rem_min` has slightly lower coverage (95.5% vs 97.3%) due to nights where Garmin used the deep/light/awake-only classifier — see [`sleep_metrics.md`](sleep_metrics.md) §4.2.
- **`sleep_efficiency_tib`** (derived): NaN if either `sleep_duration_min` or `sleep_awake_min` is NaN, OR if `sleep_duration_min == 0`. The zero-denominator case is a device-side artefact (Garmin recorded no sleep on that date), NOT a zero-efficiency observation. Per-operand NaN policy for the full sleep family lives in [`sleep_metrics.md`](sleep_metrics.md) §10.
- **`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`, `bb_overnight_gain`, `hr_median_waking`**: missing data = uninstrumented, NOT zero autonomic load. `bb_overnight_gain` sparse-availability handling per §6.2.1 is separate from the zero-vs-NaN discipline.
- **`gevoelscore`**: missing data = no manual entry on that day, NOT a zero-felt-state. The 90.0% coverage rate means the trajectory pool is ~10% smaller than the sleep + autonomic pools; report per-arm n per window explicitly.
- **`exertion_class_lagged_lcera`**: missing data = bootstrap-window or gap day (per audit §1 the 4.6% missingness is structural, not data-quality). Missing-class days are excluded from both the trigger side and the class-outcome side.

**Explicit missing-data reporting at Stage D**: per (outcome, window, overlap, stratum) cell, report n_valid per k = 1, ..., w. Cells with n_valid < 5 at any k drop from summary-statistic computation and are flagged in the descriptive audit output.

**Cross-outcome pool independence**: the matched-ordinary comparator pool is recomputed per outcome (§4.2). This means a comparator day may participate in the `total_steps` trajectory pool but not in the `bb_overnight_gain` trajectory pool if the latter's data-availability filter drops it. Cross-outcome comparability of comparator pools is not enforced.

---

## 12. Compression and lock discipline

Producer-mode methodology MD per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). The lock discipline follows the parent MD [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) §3.6 compression pattern:

1. **Draft (this file, r1)**: producer-mode subagent draft with all Stage -1 audit decisions propagated. No new design decisions beyond faithful propagation.
2. **Fresh-session `/research-methodology-review`**: reviewer-mode session (different Claude session, cold context) audits this MD against the CONVENTIONS §2.2 four-input bar + applicable 4-layer checklist items. Produces reviewer report at `docs/research/reviews/methodology-post_heavy_day_compensatory_rest-YYYY-MM-DD.md`.
3. **r2 lock with §3.6 compression**: reviewer fires absorbed inline via the parent MD's compression discipline (mechanical clarifications, cross-cites, caveat additions); architectural changes escalate to r2-with-design-change and re-review.
4. **Stage D descriptive audit runs against r2-locked operand**: no Stage D output until the operand is locked.

**Compression rule** (inherited from parent MD): reviewer absorption at r2 is *mechanical* (clarifications, cross-cites, added caveats) NOT architectural (design changes). Any architectural change forces re-review before lock.

---

## 13. Lock log

| version | date | change |
|---|---|---|
| r1 | 2026-07-15 | Initial draft as producer-mode methodology MD post-Stage -1-audit lock. Faithful propagation of Stage -1 audit §7 locked decisions: episode-end (gap=0) as unit, per-heavy-day as sensitivity; 3d + 5d primary windows + 10d extended; both strict + inclusive overlap policies at all windows; matched-ordinary comparator (no-heavy + no-crash + valid-outcome in [D, D+w]); LC-era stratum; intensity-stratified sensitivity arm (combined primary + very_heavy_only + heavy_only). Adds Q24 subjective sub-part paired channel gated by the §8 four-branch decision-tree. Nine trajectory summary statistics per (outcome, window, overlap, stratum). Seven pre-committed caveats per audit §6.7. Zero-vs-NaN discipline per parent MD §5. `bb_overnight_gain` downgraded to sensitivity-only per data-availability check 2026-07-15 (all three variants <80% coverage on LC-era stratum). Subagent-drafted per user delegation; fresh-session `/research-methodology-review` before lock is the peer-review discipline. |
| r1 extended pre-lock | 2026-07-15 | Stage 3b documentation pass extends the r1 draft (pre-lock, not a post-lock r2 revision) with cross-references to the newly drafted [`sleep_metrics.md`](sleep_metrics.md) operand catalogue: (1) §6.2 sleep-operand table renames `sleep_efficiency` → `sleep_efficiency_tib` (canonical) with `sleep_efficiency_staged` named as the sensitivity variant per `sleep_metrics.md` §4.4; (2) §6.2 adds `sleep_rem_min` as PRIMARY sleep-architecture outcome (95.5% LC-era coverage) following the Stage 3a extractor correction that landed REM extraction (the earlier "no REM on FR245" assertion was factually wrong per `sleep_metrics.md` §4.2); (3) §6.2.3 NEW subsection names six sensitivity-tier sleep operands (`sleep_efficiency_staged`, `bb_overnight_gain`, `bb_overnight_gain_frac`, `sleep_hr_avg_spo2`, `spo2_avg_sleep`, `asleep_stress_max_uds`) with per-operand rationale + direction pre-commits; (4) §6.5 NEW subsection reserves Family B (SRI + timing-SD) operands for Q24 sub-part 3 (phase-stratification) and explicitly excludes them from +3d / +5d / +10d trajectory reads; (5) §7.7 direction pre-commit extended with `sleep_rem_min` (bidirectional per literature; compensatory reading = positive per REM-rebound literature); (6) §14 cross-references adds `sleep_metrics.md`. Substantive Q24 design decisions unchanged; formula ownership moved to the canonical operand catalogue. |
| r1 load-bearing calls resolved pre-lock | 2026-07-15 | Three load-bearing design calls flagged during r1 drafting resolved via user endorsement 2026-07-15 (pre-lock, not a post-lock revision): (1) **§3.5 NEW subsection** — crash-adjacency handling: heavy-episode-ends with a crash in `[+1, +w]` are excluded from the primary trajectory pool and reported separately as a **compensatory-failure sub-arm** at Stage D (per-window sample TBD). Primary pool = compensatory-success (no-crash-in-window). Cleanly separates the "does resting after heavy prevent bad outcomes?" reading from the "what does the trajectory look like when compensation failed?" reading; the two answer structurally different questions and comparing them is directly informative for the Q24.5 sub-part (unfalsifiable counterfactual). No pre-registered inferential test compares the two pools at Stage D. (2) **§8.1 rewrite** — decay-screen operationalisation changed from window-start-based `|Δ(w)| / |Δ(1)| < 0.5` to **peak-based** `|Δ(w)| / |Δ(k*)| < 0.5` where `k*` is peak-location per §7.5. Handles delayed onset (Chu 2018 24-72h) naturally; the naive window-start formulation is ill-defined when `|Δ(1)| ≈ 0` at true peak k*=2 or 3. 0.5 threshold preserved. (3) **§8.1 + §8.2 + §8.3 rewrite** — autonomic decay screen changed from single-primary-channel (`stress_mean_sleep`) to **per-channel independent screens** across all 5 primary autonomic channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`, `hr_median_waking`, `sleep_hr_avg_spo2`). Branch verdict is per-channel; channel-disagreement is a substantive finding (identifies which autonomic axis carries the recovery signal per Radin 2024 nightly-HR-persistence). Cross-channel discipline added to §8.3. Composite z-score index explicitly rejected: (a) would collapse the information the decision-tree preserves; (b) channels have differential validity on FR245 (Miller 2022 sleep-stage κ=0.25 vs timing/duration κ=0.35) — composite propagates the weakest input; (c) 5 channels × 4 branches = 20 reporting cells but uniform branch definition, no interpretive overhead. Reporting matrix at Stage D: 5 channels × 2 primary windows = 10 rows + 5 extended-window rows = 15 branch verdicts. |

---

## 14. Cross-references

- [CONVENTIONS §1.1, §2.1, §2.2, §3.1-§3.6, §4.2](../CONVENTIONS.md) — producer-mode + descriptive-before-inference + four-input bar + audit hooks + caveat-class framing.
- [Stage -1 audit `analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md`](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md) — THE authoritative source for all locked design decisions in this MD.
- [`methodology/queued_work.md` §Q24](queued_work.md#q24-site-r33----compensatory-rest-after-heavy-days-and-whether-it-strengthened-over-time) — Q24 five sub-parts brief + Q24 status (this MD covers sub-parts 1 + 4 + new subjective; 2 blocked; 3 + 5 deferred).
- [`methodology/bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) (LOCKED r3) — structural precedent for producer-mode methodology MD tone + §11 zero-vs-NaN discipline + §12 compression + lock discipline.
- [`methodology/sleep_metrics.md`](sleep_metrics.md) — canonical sleep-operand catalogue consumed by §6.2 primary set + §6.2.3 sensitivity set; owns the definitional-pair discipline (`sleep_efficiency_tib` vs `sleep_efficiency_staged`), the Family B DEFERRED reservation (§6.5), and the per-operand zero-vs-NaN policy inherited by §11.
- [`literature/reviews/pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md) — literature grounding for expected post-heavy trajectory shapes: Chu 2018 (PEM peak 24-72h + delayed onset), Moore 2023 (ME/CFS recovery mean 12.7d, range 1-64d, extremely prolonged decay), Radin 2021 (autonomic tail 79d in acute COVID; biphasic dip-then-elevated), Van Campen 2020 (day-2 CPET severity-scaling), Germain 2025 (molecular dysregulation peaks during subjective recovery — motivates the two-clock read in §8).
- [`analyses/hypotheses/HA-C4c-post-heavy-day-recovery/`](../analyses/hypotheses/HA-C4c-post-heavy-day-recovery/) — sibling hypothesis using same heavy-day trigger at bout-level Garmin stress recovery.
- [`analyses/hypotheses/HA-C4cp-post-heavy-day-recovery-personal-baseline/`](../analyses/hypotheses/HA-C4cp-post-heavy-day-recovery-personal-baseline/) — sibling personal-baseline sister to HA-C4c.
- [`DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) — column-semantics reference for all §6 outcome operands.
- [`methodology/hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) — Firstbeat-input opacity caveat inherited by §6.2 Garmin stress channels.
- [`methodology/citalopram_phase_stratification.md`](citalopram_phase_stratification.md) — dose-state axis; §10 caveat 5 references but does not stratify.

---

*Producer-mode methodology MD. Update when (a) the fresh-session review verdict lands and informs r2 compression, (b) Stage D descriptive results land and inform which §8 branch fires (Stage H pre-reg pathway then activates), (c) a downstream sub-part (2 / 3 / 5) becomes feasible and warrants operand extension.*
