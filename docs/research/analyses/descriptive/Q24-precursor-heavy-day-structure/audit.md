# Descriptive audit — Q24 precursor: heavy-day structural audit

**Status**: LOCKED r1 2026-07-15 (Stage-D producer-mode artefact per CONVENTIONS §1.2 + §2.1 descriptive-before-inference). Precursor to Q24 methodology MD; findings inform unit-of-analysis, window-length, and overlap-policy design decisions.

**Frame**: LC-era stratum (`lc_phase == 'lc'`), matches HA-C4c / HA-C4cp analytical stratum.

**Heavy-day definition**: `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` — the top ~25% of the participant's own LC-era-lagged [d-90, d-30] baseline distribution, aggregated across the 4-axis composite (`effective_exertion_min`, `total_steps`, `max_hr_uds`, `vigorous_min_uds`). Same operand used to define HA-C4c's heavy-day stratum.

**Reproducibility**: `scripts/audit.py` + outputs in `output/`; idempotent re-run against `per_day_master.csv`.

**Cross-refs**: [queued_work.md Q24](../../../methodology/queued_work.md#q24-site-r33----compensatory-rest-after-heavy-days-and-whether-it-strengthened-over-time), [HA-C4c hypothesis](../../hypotheses/HA-C4c-post-heavy-day-recovery/hypothesis.md), [HA-C4cp hypothesis](../../hypotheses/HA-C4cp-post-heavy-day-recovery-personal-baseline/hypothesis.md), [CONVENTIONS §3.1-§3.6](../../../CONVENTIONS.md).

---

## 1. Corpus summary

| Measure | Value |
|---|---|
| LC-era rows | 1524 days (2022-04-04 → 2026-06-05, ~4.2 years) |
| Heavy days (`heavy` + `very_heavy`) | **532 (34.9% of LC-era)** |
| Very-heavy days | 256 (16.8%) |
| Heavy-only days | 276 (18.1%) |
| Crash days | 103 |
| `exertion_class_lagged_lcera` missingness | 70 days (4.6%; bootstrap-window + gap days) |

Source: [output/corpus_summary.csv](output/corpus_summary.csv).

---

## 2. Heavy-day rate over time — 2026 elevation flagged

Annual heavy-day rate:

| Year | Days total | Heavy days | Very-heavy days | **Heavy rate** |
|---|---:|---:|---:|---:|
| 2022 (partial, Apr-Dec) | 272 | 79 | 52 | 29.0% |
| 2023 | 365 | 127 | 52 | 34.8% |
| 2024 | 366 | 125 | 60 | 34.2% |
| 2025 | 365 | 127 | 59 | 34.8% |
| **2026 (partial, Jan-Jun)** | 156 | 74 | 33 | **47.4%** |

Source: [output/counts_by_year_quarter.csv](output/counts_by_year_quarter.csv).

**Pattern**: 2023-2025 stable at ~34-35%; **2026 partial-year rate is 12.5 pp above baseline**. Three non-exclusive readings, all supportable descriptively:

1. Genuine load increase (behaviour change).
2. **Baseline drift** — the [d-90, d-30] lagged reference has fallen, so the participant's "heavy" percentile threshold now catches more days at absolute-lower loads. This is exactly the "running-average complication" flagged at Q24 design time.
3. Seasonal artefact — 2026 covers Jan-Jun only, which may be a higher-activity half of the year. 2023-2025 annual comparison controls seasonality within-year; the 2026 partial does not.

**Interpretive discipline**: Q24 methodology MD must pre-commit **2026 as a caveat** — either report Q24 trajectories with and without 2026, or explicitly acknowledge the elevation as a load-bearing sensitivity dimension.

### Heavy-rate by `recovery_phase`

| Phase | Days | Heavy days | Heavy rate |
|---|---:|---:|---:|
| `lc_pre_ergo` | 171 | 41 | 24.0% |
| `pacing_pre_citalopram_learning` | 56 | 23 | 41.1% |
| `pacing_habit_established` | 509 | 183 | 36.0% |
| `citalopram_modulated` | 788 | 285 | **36.2%** (largest phase) |

Roughly stable except `lc_pre_ergo` (lower — likely a pre-pacing-adaptation phase where load was naturally lighter). Source: [output/counts_by_recovery_phase.csv](output/counts_by_recovery_phase.csv).

---

## 3. Threshold drift audit

**Method**: For each heavy day, extract `eff_exertion_rank_lagged_lcera` (the underlying percentile rank on the effective-exertion axis). If the lagged-baseline is stationary and the class-cutoff is fixed, we expect stable rank distributions on heavy days across quarters.

Quarterly summary ([output/threshold_drift_by_quarter.csv](output/threshold_drift_by_quarter.csv)):

| Quarter | heavy n | rank median | rank p25 | rank p75 | rank min |
|---|---:|---:|---:|---:|---:|
| 2022Q3 | 35 | 0.917 | 0.759 | 0.967 | 0.233 |
| 2023Q2 | 33 | 0.633 | 0.500 | 0.883 | 0.183 |
| 2024Q3 | 27 | 0.700 | 0.284 | 0.850 | 0.242 |
| 2025Q2 | 41 | 0.883 | 0.783 | 0.967 | 0.342 |
| 2026Q1 | 40 | 0.858 | 0.656 | 0.933 | 0.242 |
| 2026Q2 | 34 | 0.909 | 0.652 | 0.963 | 0.217 |

**Observation 1**: Median rank on heavy days fluctuates 0.63-0.92 across quarters — no monotone drift, but real quarter-to-quarter variability.

**Observation 2 (nuance, not bug)**: Some quarterly `rank_min` values sit as low as 0.12-0.24 (well below the ~0.75 heavy cutoff on the effective-exertion axis alone). This is **expected under the multi-axis composite** — `exertion_class_lagged_lcera` is derived from `exertion_rank_composite_lagged_lcera`, which aggregates across 4 axes (`effective_exertion_min`, `total_steps`, `max_hr_uds`, `vigorous_min_uds`). A day can score low on the effective-exertion axis and still be classified `heavy` if it scored high on the other three. Flagged for methodology-MD acknowledgement, not a data-quality concern.

**Interpretive discipline**: Q24 methodology MD should acknowledge (a) the multi-axis nature of the heavy-day definition and (b) that heavy-day *composition* (which axes dominate) may itself vary over time even if the aggregate rate looks stable. A future sensitivity arm could stratify by axis-dominance.

---

## 4. Episode structure — three gap tolerances

**Method**: Assign an `episode_id` to runs of heavy days separated by ≤ `gap_tolerance` non-heavy days. Three definitions computed:

- **gap=0 (contiguous)**: episodes are runs of consecutive heavy days.
- **gap≤1**: heavy days separated by ≤1 non-heavy day merge into one episode.
- **gap≤2**: heavy days separated by ≤2 non-heavy days merge.

Summary ([output/episode_summary.csv](output/episode_summary.csv)):

| gap | n episodes | single-day episodes | multi-day episodes | single-day rate | median span | mean span | p90 span | max span |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **0 (contiguous)** | **314** | **188** | **126** | **59.9%** | **1d** | **1.7d** | **3d** | **10d** |
| ≤1 gap | 180 | 76 | 104 | 42.2% | 2d | 3.7d | 8.1d | 26d |
| ≤2 gap | 125 | 38 | 87 | 30.4% | 5d | 6.2d | 13.6d | 30d |

### Contiguous (gap=0) length histogram — the dominant reading

| Length | Count | Cumulative % |
|---|---:|---:|
| 1 day | 188 | 59.9% |
| 2 days | 77 | 84.4% |
| 3 days | 27 | 93.0% |
| 4 days | 12 | 96.8% |
| 5 days | 6 | 98.7% |
| 6+ days | 4 | 100.0% |
| **Max** | **10 days** | |

Source: [output/episode_length_hist_gap0.csv](output/episode_length_hist_gap0.csv).

**Read**: Under the contiguous definition, **~60% of heavy episodes are single-day, ~85% are ≤2 days, ~93% are ≤3 days**. Multi-day heavy streaks longer than 3 days are the exception (7% of episodes). The corpus has a strongly right-skewed episode-length distribution with a thin tail.

Under the ≤1-gap definition, some contiguous-adjacent short streaks merge into longer episodes (max=26d), but the modal episode is still 1-2 days. Under ≤2-gap, aggressive merging produces occasional 21-30 day "episodes" that are more accurately characterised as sustained-elevated-load periods with intermittent rest days, not true single load-events.

### Intensity stratification — episode structure differs sharply by class

Same episode-labelling logic applied to three masks: `combined` (heavy ∪ very_heavy — primary), `heavy_only` (`heavy` class value), `very_heavy_only` (`very_heavy` class value). Source: [output/episode_summary.csv](output/episode_summary.csv).

| Stratum | n episodes (gap=0) | single-day rate | max span (gap=0) |
|---|---:|---:|---:|
| **combined** | 314 | 60% | **10d** |
| **heavy_only** | 218 | **78%** | **4d** |
| **very_heavy_only** | 190 | **74%** | **4d** |

**Read**: When stratified by intensity class, single-day episodes dominate MORE strongly (78% / 74%) and no episode exceeds 4 days. The 10-day max in `combined` arises when heavy and very_heavy days interleave within a single contiguous heavy-load streak. This matters for the methodology MD: an intensity-stratified sensitivity arm should expect very short episodes (mostly 1 day), reducing the "compensatory rest response to a whole episode" complication that motivated the episode-end unit choice.

---

## 5. Overlap density — the DOMINANT structural constraint

This section holds the hardest single design constraint for Q24. Two independent checks per heavy day:

- **±window**: is there any other heavy day in [-window, +window]?
- **post-window**: is there any other heavy day in [+1, +window]?  ← *this is what matters for trajectory overlap*

### Per-heavy-day overlap ([output/overlap_density_per_heavy_day.csv](output/overlap_density_per_heavy_day.csv))

| Window | ±window contaminated | ±window clean | **Post-window contaminated** | **Post-window CLEAN (usable)** |
|---|---:|---:|---:|---:|
| ±3d / +3d | 92.9% (494) | 38 | 76.5% (407) | **125** |
| ±5d / +5d | 98.9% (526) | 6 | 90.2% (480) | **52** |
| ±10d / +10d | 99.8% (531) | 1 | 97.7% (520) | **12** |
| ±14d / +14d | 100.0% (532) | 0 | 99.1% (527) | **5** |

### Per-episode overlap (gap=0 contiguous, last-day framing) ([output/overlap_density_per_episode.csv](output/overlap_density_per_episode.csv))

| Window | Post-window contaminated | **Post-window CLEAN episodes** |
|---|---:|---:|
| +3d | 60.2% (189) | **125** |
| +5d | 83.4% (262) | **52** |
| +10d | 96.2% (302) | **12** |
| +14d | 98.4% (309) | **5** |

**Sanity check**: The per-heavy-day "clean" and per-episode (gap=0) "clean" converge to the same counts at each window (125 at +3d, 52 at +5d, 12 at +10d, 5 at +14d) — because a heavy day with no heavy in [+1, +w] IS necessarily an episode-end with no successor episode in [+1, +w]. Good structural validation.

### Cross-stratum overlap — the actionable question for the intensity-stratified sensitivity arm

The correct "clean" definition for an intensity-stratified trigger (e.g. very_heavy only) is: **triggered on very_heavy, scanned against COMBINED heavy** — because a very_heavy episode followed by intervening heavy days in the post-window contaminates the "no other heavy load in the recovery window" claim just as much as an intervening very_heavy day would.

Source: [output/overlap_density_cross_stratum.csv](output/overlap_density_cross_stratum.csv).

| Trigger | Scan | Window | n trigger days | Contaminated | **Clean (usable)** |
|---|---|---|---:|---:|---:|
| very_heavy | combined | +3d | 256 | 79.7% | **52** |
| very_heavy | combined | +5d | 256 | 92.6% | **19** |
| very_heavy | combined | +10d | 256 | 98.0% | 5 |
| very_heavy | combined | +14d | 256 | 99.2% | 2 |
| heavy_only | combined | +3d | 276 | 73.6% | **73** |
| heavy_only | combined | +5d | 276 | 88.0% | **33** |
| heavy_only | combined | +10d | 276 | 97.5% | 7 |
| heavy_only | combined | +14d | 276 | 98.9% | 3 |

**The intensity-stratified sensitivity arm sample-size floor**: at +5d, very_heavy-triggered + combined-clean gives **n=19 episodes**. That's small — descriptive with wide bootstrap CIs only, no formal null tests. At +3d, n=52 (matches the combined-primary +5d sample coincidentally). The intensity-stratified arm at extended windows (+10d, +14d) is not viable.

**Design implication**: an intensity-stratified sensitivity arm at Stage D is viable at +3d (n=52) and marginal at +5d (n=19). A more disciplined move at +5d would be to run the intensity-stratified read as a *descriptive-only-with-CI* arm without inference.

### What this means

**Heavy days are massively clustered in this corpus.** A trajectory analysis with strict "no other heavy day in the post-window" policy hits severe sample-size constraints as window grows:

| Window | Strict-clean sample | Interpretability |
|---|---:|---|
| +3d | **125** episodes | Workable for descriptive; comfortable for bootstrap-CI reads |
| +5d | **52** episodes | Small but usable descriptively; block-permutation null still viable |
| +10d | **12** episodes | Descriptive only; too small for null-hypothesis tests |
| +14d | **5** episodes | Narrative only; effectively single-case reads |

Under an **inclusive** overlap policy (all heavy days count, adjust null via permutation block length ≥ window), sample stays at 532 per-heavy-day or 314 per-episode (gap=0) — but each trajectory then reflects response to the entire multi-day heavy-load context, not to the specific target day/episode alone.

---

## 6. Design-decision implications for Q24 methodology MD

Each finding above forces a specific design choice. Locking them here so the methodology MD can proceed without re-derivation.

### 6.1 Unit of analysis: episode-end (gap=0 contiguous), NOT per-heavy-day

**Reason**:
- Per-heavy-day and per-episode(gap=0) converge on the same clean sample at each window (§5 sanity check) — so the sample-size case is neutral.
- Per-episode(gap=0) has cleaner semantics: the participant's post-heavy rest response is presumably to the whole heavy load, not to each constituent day of a 2-3-day streak. Matches the HA-C4c/HA-C4cp bout-unit precedent.
- Per-episode also cleanly avoids double-counting the same recovery window across contiguous heavy days.

**Alternative preserved**: report per-heavy-day AUC / trajectory as a sensitivity arm at Stage D, since it uses the same underlying data. Not primary.

### 6.2 Episode definition: gap=0 (contiguous), with gap≤1 as sensitivity

**Reason**: gap=0 is the tightest, most defensible definition and the participant's stated preference. gap≤1 merges some short streaks separated by a single rest day (which may reflect the same load-event) — worth reporting as sensitivity but the interpretive stretch increases. gap≤2 is too permissive (30-day "episodes" become sustained-load periods, not single load-events).

### 6.3 Windows: primary 3-day + 5-day; extended 10-day (opportunistic) at strict policy

**Reason**:
- **Primary 3-day** (n=125 strict-clean episodes) — comfortable descriptive sample; Chu 2018 24-72h PEM peak window; matches user's stated interest in preserving the shorter window.
- **Primary 5-day** (n=52 strict-clean episodes) — Chu peak + early decay; the participant's own subjective-recovery timescale (~2-3d per `pem_recovery_trajectory_review.md` §2); small but usable descriptively.
- **Extended 10-day** (n=12 strict-clean episodes) — reports the autonomic tail alongside descriptive uncertainty explicitly acknowledging the small sample; matches the corpus's own K-bout-recovery-signal ~2-week autonomic settle prior.
- **14-day** — dropped from primary reads (n=5); may appear as narrative single-case examples only.

### 6.4 Overlap policy: BOTH strict + inclusive reported side-by-side at all windows

**Reason**: §5 gives sharp counts under both policies. Strict gives clean semantics but small sample; inclusive gives full sample but the trajectory reflects sustained-load response. Reporting both surfaces the sample-size vs semantic-cleanness tradeoff transparently. If the two policies agree on the trajectory shape, that's itself informative (finding is robust to policy). If they diverge, the divergence is a finding.

### 6.5 Comparator: "matched ordinary" days = no heavy in [D, D+window] + no crash in [D, D+window] + valid outcome data across the window

Standard from Q24 context; §5 confirms this is workable given the LC-era corpus has 1524 - 532 = **992 non-heavy days**, of which most will meet the "no heavy in [D, D+w]" filter.

### 6.6 Intensity stratification: heavy vs very_heavy as pre-committed sensitivity arm

Per user request, add an intensity-stratified sensitivity arm at Stage D methodology MD. Design (from §4 + §5 cross-stratum):

- **Primary trigger**: `combined` (heavy ∪ very_heavy) — as locked in §6.1.
- **Sensitivity trigger A**: `very_heavy_only` — tests whether trajectory magnitude/shape differs when triggered by the higher-intensity subset. Combined-clean sample: **n=52 at +3d** (workable) / **n=19 at +5d** (marginal — descriptive-only-with-CI) / not viable at +10d.
- **Sensitivity trigger B**: `heavy_only` (excluding very_heavy) — descriptive counterpart to A. Combined-clean sample: n=73 at +3d / n=33 at +5d / n=7 at +10d.
- **Read policy**: report all three side-by-side at +3d; report combined-primary + very_heavy_only at +5d as descriptive-with-CI; combined-only at +10d.
- **What we're looking for**: does the trajectory magnitude/shape scale with intensity (dose-response inside the heavy-load band)? Or is the "heavy" class a uniform-response bucket? Literature (Van Campen 2020, Moore 2023) predicts severity-scaling of recovery time; if that shows up here, it would support the multi-tier heavy-day definition itself.

### 6.7 Caveats to pre-commit in methodology MD

1. **2026 heavy-rate elevation** (§2): report Q24 trajectories with/without 2026, or acknowledge as sensitivity dimension.
2. **Multi-axis heavy-day composition** (§3): heavy days may vary in axis-dominance over time; not stratified in primary read.
3. **Baseline drift** (§3, §2): the lagged [d-90, d-30] reference itself drifts; the heavy-day definition is relative-to-recent-past, not absolute. Interpretation must respect this — "heavy" in 2026 may not equate to "heavy" in 2022 in absolute terms.
4. **Deconditioning + citalopram confounds** (Q24 context): pre-commit as caveats, not to be interpreted away.
5. **Strict-clean sample sizes** (§5): 52 at +5d, 12 at +10d — CI-based reads only, no formal null-hypothesis tests at extended windows.
6. **Multi-axis heavy days ≠ single-axis heavy days** — the corpus's HA-C4c definitional lineage is preserved; alternative single-axis definitions are out of Q24 scope by pre-commit.
7. **Intensity-stratified arm sample floor** (§6.6): very_heavy_only + combined-clean gives n=19 at +5d — descriptive-with-CI only, not viable for null-hypothesis tests. Report constraint explicitly.

---

## 7. Locked design decisions to propagate to Q24 methodology MD

| Decision | Value |
|---|---|
| Unit of analysis | **Episode-end (gap=0 contiguous)**; per-heavy-day as sensitivity |
| Episode definition primary | **gap=0 contiguous**; gap≤1 as sensitivity; gap≤2 out of scope |
| Windows (primary) | **3-day + 5-day** |
| Windows (extended) | **10-day** (strict-clean only, n=12 acknowledged) |
| Windows (dropped) | **14-day** (n=5, narrative-only) |
| Overlap policy | **Both strict + inclusive, side-by-side, at all windows** |
| Comparator | Matched ordinary: no-heavy-in-[D, D+w] + no-crash-in-[D, D+w] + valid outcome data |
| Stratum | LC-era (`lc_phase == 'lc'`), matching HA-C4c/HA-C4cp |
| **Intensity stratification** | **Primary=combined; sensitivity arms=very_heavy_only + heavy_only; report all three at +3d, combined + very_heavy at +5d (descriptive-with-CI), combined-only at +10d** |
| Caveats to pre-commit | 2026 elevation; multi-axis composition; baseline drift; deconditioning; citalopram; small extended-window samples; intensity-stratified sample floor n=19 at +5d |

---

## 8. What does NOT fire

- **Monotone drift** in the heavy-day rate — 2023-2025 stable, 2026 partial elevation only. No clean trend argument for or against pacing improvement over time based on heavy-day frequency alone.
- **Extreme episode lengths** as a corpus feature — max contiguous episode is 10 days, p90 is 3 days. Long episodes are exceptional, not typical.
- **Data-quality flag** on `exertion_class_lagged_lcera` — 4.6% missingness is bootstrap/gap artefact, not a systematic issue.

---

## 9. Lock log

| version | date | change |
|---|---|---|
| r1 | 2026-07-15 | Initial lock. Stage-D producer-mode artefact per CONVENTIONS §1.2. Fresh-session `/research-review` NOT dispatched pre-lock (single-arc descriptive-precursor artefact; findings will be re-verified when the methodology MD it feeds is drafted and independently reviewed). Bug fix (overlap-density post-window scan short-circuit) applied inline before lock. Intensity-stratified structural + cross-stratum overlap sections (§4 stratified table + §5 cross-stratum table + §6.6 design decision) added same-drafting-cycle per user Q "in our tests lets also see if heavy and very heavy makes a difference" before lock; not a post-lock r1→r2 revision. |
