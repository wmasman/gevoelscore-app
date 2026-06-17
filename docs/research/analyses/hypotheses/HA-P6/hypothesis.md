# HA-P6 — Post-crash window distinctive autonomic-recovery shape (Personal-register, descriptive characterisation) — **v3**

## Authorship

**Drafted 2026-06-17 (v3)** by Claude (Opus 4.7 1M) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. v3 is a SUPERSESSION of v2 (LOCKED 2026-06-17 by user acceptance under option-A compression, archived at [`hypothesis-v2-archived.md`](hypothesis-v2-archived.md)) per [`hypothesis_lock_process.md §3.9 step 4`](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock): the v2 fresh-session [`/research-review`](../../../reviews/README.md) audit on 2026-06-17 (report at [`reviews/HA-P6-2026-06-17-v2.md`](../../../reviews/HA-P6-2026-06-17-v2.md), verdict **PASS with caveats**) named two substantive Layer-2 / Layer-3 fires + four minor Layer-1 / Layer-3 fires + two side observations on v2's §4.8.1 / §7 / §4.8.4 / §10.4 sections, all explicitly closeable via spec-precision refinements (extensions, not re-architecture per the audit's verdict line). v3 absorbs the audit's eight named closures; v2 produced no `result.md` (no dry-run had been run between v2 lock 2026-06-17 and the fresh-session audit 2026-06-17).

**v3 supersedes v2 rather than absorbing as v2-r2** per the project's HA-C4b precedent (v1 → archived → v2 → archived → v3 → LOCKED; each version has its own pre-lock arc; no post-lock-r2 pattern in project history). The v2 LOCKED state at commit [`ef4f105`](https://github.com/willemmasman/gevoelscore-app/commit/ef4f105) is preserved as the historical record of what the option-A compression-at-lock decision produced before the audit fired; v3 takes the audit's findings as the deferred §3.6 re-audit content and binds them into the new lock arc cleanly.

**Parent artefacts for v3**:
- v2 LOCKED [`hypothesis-v2-archived.md`](hypothesis-v2-archived.md) (2026-06-17, by user acceptance under option-A compression at commit `ef4f105`)
- v2 fresh-session audit [`reviews/HA-P6-2026-06-17-v2.md`](../../../reviews/HA-P6-2026-06-17-v2.md) (fresh session, 2026-06-17, PASS-with-caveats, 8 closures named in §4 + §2)
- v1 LOCKED [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md) (2026-06-15-r3) — historical context
- v1 audit [`reviews/HA-P6-2026-06-15.md`](../../../reviews/HA-P6-2026-06-15.md) (v1 fresh-session, REVISION RECOMMENDED → v2 r2 closures absorbed)
- v1 HALT [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md) (2026-06-17, two channels FLAG on v1's §7 sanity gate — the original trigger for v2)
- v1 implementation [`script-v1-archived.py`](script-v1-archived.py) (2026-06-17, faithful to v1 §10 spec)

**The three closures inherited from v2 (carried forward unchanged)** — these are the spec-precision refinements v2 originally introduced in response to the v1 HALT and that v3 retains unchanged:

- **(c) §4.8.1 "pre-crash baseline values" input-pool interpretation (carried from v2)** — v1's `sanity_checks()` chose the **concatenation interpretation**: per-channel input was the union of per-episode `[t0-90, t0-30]` LC-era same-phase non-crash baseline values across all 29 episodes, concatenated into one flat array. This produces artificial lag-1 discontinuities at every episode boundary and explains why four of seven channels returned the estimator's default 7 (the ACF of a concatenated mixed-time-source series has no clean cutoff). **v2/v3 commits to interpretation (ii)**: the per-channel pooled-LC daily time series (LC era 2022-04-04 to data-cut, eligible-day filter applied, ordered by date). This matches HA-P7's `estimate_block_length(cc14)` usage at [HA-P7 `test.py` line 763](../HA-P7/test.py) on `cc14 = df.loc[mask_pool, "crash_count_14d"]`. The methodology MD's "Operational consequences" §2 in [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) frames E[L]\* as a property of the time series, not of an analysis subset. See §4.8.1 for the v3 specification (which adds an unmedicated-stratum sensitivity arm per v3 closure #1; see below).

- **(a) §4.8.1 + §7 E[L]\* sanity-check policy refinement (carried from v2; refined in v3)** — v1's §7 sanity policy treated the estimator's default 7 (returned as a fallback when the ACF was inconclusive or the closed-form formula degenerated) as PASS, mechanically equivalent to a verified real estimate. This was honest at the level of bytes but not at the level of provenance. v2 introduced a three-verdict logic (PASS-real / PASS-fallback / FAIL); **v3 refines this into a four-verdict logic** per the v2 audit's L3.4 substantive fire on PASS-fallback discipline — see §4.8.1 + §7 for the v3 specification. The v3 override mechanism extends the methodology MD's per-hypothesis-override clause to per-channel-within-a-hypothesis, with **v3-added cap** (closure #3 below) and the **v3-added PASS-fallback-no-cutoff override row** (closure #2 below).

- **(b) §4.8.4 per-episode `recovery-completeness` threading (carried from v2 unchanged)** — v1 implementation gap diagnosed by the v1 test session: `run_cell` stored per-episode completeness as a median across episodes (`completeness_median`), not as a per-episode array; `secondary_correlations` hard-coded `completeness = float("nan")` per episode, producing an all-NaN array and n=0 in the §4.8.4 completeness Spearman. v2 specifies: **per-episode completeness is computed and stored as `completeness_per_episode` in the (channel × phase × baseline-arm × t0-anchor) cell during the §4.8.1 trajectory pass**; §4.8.4 reads the array directly. v2 additionally adds: (i) a **denominator-undefined exclusion rule** at §4.5 step 7 (`abs(μ_ch - channel(t0_i)) < ε = 0.5×σ_ch`; episodes with undefined completeness contribute to §1.1 trajectory but not to §1.2 completeness Spearman; their count is reported separately in §6 + §10.1); (ii) explicit **baseline-source disambiguation** at §4.8.4 (the single-cell-lock pooled-LC × Arm-A cell names the §1.1 trajectory-comparison baseline; the per-episode completeness denominator μ_ch is always from the **Arm-B lagged baseline** because Arm-A produces a matched-control trajectory, not a scalar baseline mean). v3 carries this forward unchanged.

**The eight v3-NEW closures from the v2 audit** ([`reviews/HA-P6-2026-06-17-v2.md`](../../../reviews/HA-P6-2026-06-17-v2.md) §4 + §2):

- **(v3 #1) Pooled-LC stationarity contamination + unmedicated-stratum E[L]\* sensitivity arm (L2.2 substantive)** — v2's pooled-LC E[L]\* under interpretation (ii) spans 4 years crossing CPAP + Citalopram intervention transitions documented as level shifts on the autonomic-load channels per [`intervention_effects_descriptive.md`](../../../methodology/intervention_effects_descriptive.md) (β=+0.57/mg for `all_day_stress_avg`; β=+0.43/mg for `stress_mean_sleep`; β=-1.13/mg for `bb_lowest`). The data-driven estimator computes the empirical ACF; on a non-stationary series with intervention-induced level shifts, the ACF shows spurious long-range correlation reflecting the level shifts rather than within-phase autocorrelation. The same channels that triggered v1's HALT will likely still FAIL under (ii) — but partly as a pooled non-stationarity artefact, not a clean within-phase ACF read. **v3 adds a §4.8.1 within-stratum E[L]\* sensitivity arm** computed on the unmedicated-stratum daily series (2022-04-04 → 2024-04-08, no CPAP/Citalopram transitions); the unmedicated-stratum E[L]\* is the low-confounding reference. When pooled-LC E[L]\* > 10.5 but unmedicated-stratum E[L]\* is within [3.5, 10.5] for the same channel, the FAIL-override magnitude binds to the within-stratum E[L]\* (closer-to-clean ACF estimate) rather than the pooled-LC estimate. See §4.8.1 sensitivity-arm sub-bullet + §8 stationarity-contamination caveat.

- **(v3 #2) Four-verdict logic — split PASS-fallback by note (L3.4 substantive)** — v2's three-verdict logic treated PASS-fallback as proceed-with-default-E[L]=7 + flag. The v2 audit's L3.4 fire: the estimator's `note` field distinguishes "No clear ACF cutoff (all lags within max_lag are significant)" (a **positive long-dependence signal** — every lag from 1 to max_lag has significant autocorrelation) from "Closed-form formula degenerate" or "n<30" (genuine "estimator cannot say"). Proceeding with E[L]=7 in the all-lags-significant case is structurally false-conservative. **v3 splits PASS-fallback into two**: **PASS-fallback-no-cutoff** (note matching "No clear ACF cutoff" or "all lags significant"; **per-channel override E[L] = 14**, with cap per closure #3) and **PASS-fallback-degenerate** (note matching "Closed-form formula degenerate" or "n<30 baseline pool"; proceed with default E[L]=7 + methodological flag). The v3 §4.8.1 override table extends to cover PASS-fallback-no-cutoff for all channels (was v2's per-channel-override-FAIL pre-spec; v3 generalises to PASS-fallback-no-cutoff too); per v1's empirical pattern, `bb_lowest` and `resting_hr` are the expected PASS-fallback-no-cutoff channels.

- **(v3 #3) Override magnitude cap at min(round(E[L]\*), 21) (L1.3 minor)** — v2's `E[L] = round(E[L]*)` is uncapped. At n=29 episodes + 5-day window, E[L] in the tens collapses the bootstrap resampling-resolution (geometric block lengths with E[L]=30 mean most resamples are dominated by single blocks). **v3 caps at 21** (resampling-resolution floor; one block at E[L]=21 dominates ~70% of the 5-day window). Cap-binding cases — where the data-driven E[L]\* exceeds 21 — get a "cap-binding" flag in result.md naming the channel + the cap-fire + the effective resampling-resolution constraint. See §4.8.1 override-cap sentence + §8 cap-binding caveat.

- **(v3 #4) Paired-by-episode bootstrap binding for §9 first-branch trigger (L1.3 minor)** — v2 §9 head asserts "paired stationary-bootstrap machinery" for the median DIFFERENCE (crash trajectory minus matched-control trajectory) but §4.8.1 only describes per-day median CIs, not the paired-difference CI. **v3 adds an explicit sentence in §4.8.1** specifying that the §9 first-branch trigger uses **paired-by-episode resampling**: for each bootstrap iteration, episode indices are resampled (each resample draws one (crash_i, matched_control_i) pair from the n_eligible_pairs pool); per-day median DIFFERENCE is computed on the paired-resample distribution; CI excludes 0 per the §9 head trigger binding. B = 10,000 for the headline cell. See §4.8.1 paired-bootstrap sentence.

- **(v3 #5) `[3.5, 10.5]` vs methodology MD's `[3, 14]` choice acknowledged (L3.4 minor)** — the methodology MD's override clause condition (i) gives the example "ACF crosses zero at a lag substantially different from 7 (e.g. < 3 or > 14 days)." v2 operationalises this as `|E[L]*-7|/7 > 0.5` → `E[L]* < 3.5 OR E[L]* > 10.5`, which is tighter than the MD's `[3, 14]` example on both ends. The MD's `e.g.` framing makes both ranges defensible; the MD's earlier sentence "If E[L]\* differs from 7 by more than a factor of 2, flag for review" supports the factor-of-2 reading. **v3 names this choice explicitly** in §4.8.1: the factor-of-2 framing is binding; the `[3, 14]` example is recognised but not used; v2's tighter `[3.5, 10.5]` gate catches `E[L]*=12` as FAIL where the MD's example would not (the conservative direction). See §4.8.1 verdict-range acknowledgment.

- **(v3 #6) Interpretation (ii) eligible-day filter deviation from "Stratum 4 days" baseline acknowledged (L3.4 minor)** — the methodology MD's override clause condition (i) specifies the ACF is "computed over Stratum 4 days" (per [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md): "LC with gevoelscore + crash labels" — the full LC era including crash days). v2's interpretation (ii) filter excludes crash days; **v3 acknowledges this deviation** in §4.8.1 as conservative (filters out the most anomalous days; the inter-crash-trajectory ACF is the cleaner anchor for the per-day median CI machinery that §4.8.1 binds to). See §4.8.1 eligible-day-filter acknowledgment sentence.

- **(v3 #7) §4.8.4 day-level-E[L]-on-per-episode-summary granularity mismatch acknowledged (side / structural)** — the §4.8.4 secondary Spearman uses per-episode resampling within phase but binds to the per-channel `E[L]` at the day-level from §4.8.1; the methodology MD's block-length policy was designed for day-level inference. Per-episode summaries are not autocorrelated within an episode in the same way daily values are, so the day-level E[L] over-conservatively widens the per-episode-summary CIs by construction. This is structural and inherited from v1 (v1 audit did not catch it; v2 audit's side observation surfaced it). **v3 adds a §8 caveat** naming the mismatch + the cross-cell-comparability rationale (using the same per-channel E[L] across cells preserves comparability across cells); the per-episode-summary-aware block-length alternative (inter-episode interval structure) is **deferred** to v4 / methodology-MD update. See §8 granularity-mismatch caveat.

- **(v3 #8) §10.4 line-count arithmetic fix (side typo)** — v2 §10.4 final paragraph reads "~450 lines (v1 was ~1843 lines including report-emit; the v2 modifications add ~50 lines)" — the arithmetic is internally inconsistent (v2 = 450 ≠ v1 1842 + ~50). **v3 rewords** for arithmetic consistency: "v3 is a planned rewrite at ~450 lines (v1's `script-v1-archived.py` is 1842 lines; v3 is a leaner architecture dropping the v1 report-emit bloat); the v3-specific closure-driven new logic adds ~50 lines of computation alongside the v2 closures' ~50 lines (total ~100 lines of new logic vs v2's ~50)." See §10.4.

**Operationalisation choices carried forward from v1 + v2 unchanged in v3**:

1. Sub-hypothesis scope (primary descriptive + secondary correlational, no SUPPORTED bar) — from v1.
2. Channel set (7 channels per §4.1; `n_minutes_resp_above_18` remains queued for HA-P6-v4) — from v1.
3. Matched-baseline construction (Option C: Arm A matched-deep-trough non-crash days + Arm B lagged personal baseline) — from v1.
4. §9 observation-shape branches (all four pre-spec'd; the §9 head trigger-phrase binding from v1 r2 + v3 paired-bootstrap clarification per closure #4) — from v1 + v3 refinement.
5. Window definitions, t0 anchors, §4.6 detrend binding, §4.7 phase-stratified arm, §4.8.2 recovery-completion-day estimate, §4.8.3 algorithmic shape classifier (six categories, first-match priority) — from v1.
6. §8 caveats (v1 set + v2's (a) autocorrelation-honesty + v2's (b) completeness-source-disambiguation + v3's three new caveats per closures #1, #3, #7).
7. §6 exclusion rules (v1 set + v2's undefined-completeness rule).
8. Single-cell headline lock for §9 bullets 7/8 (pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window) — from v1 r2.
9. v2's interpretation (ii) E[L]\* input-pool reading (closure (c)) — unchanged in v3.
10. v2's per-episode `completeness_per_episode` threading + ε = 0.5 × σ_ch rule + Arm-B μ_ch disambiguation (closure (b)) — unchanged in v3.

**Compression decision per [`hypothesis_lock_process.md §3.6`](../../../methodology/hypothesis_lock_process.md#36-re-audit-step-stage-4-of-the-arc)**: v3 closures are mechanical extensions (the v2 audit verdict line: "want explicit acknowledgement in §8 plus a sensitivity arm or override-extension rather than a re-architecture"):
- Closures #1, #7 are §8 caveats + a §4.8.1 within-stratum sensitivity arm (reporting-layer additions per §3.7's "reporting layer vs approach change" heuristic — no new statistical machinery, no change to the cross-cell-comparability anchor).
- Closures #2 is an override-table row extension (splits PASS-fallback into two notes-driven sub-categories; same machinery, finer disposition).
- Closure #3 is a `min(round(E[L]*), 21)` cap on an existing value (one-line refinement; no new machinery).
- Closures #4, #5, #6 are one-sentence §4.8.1 acknowledgments / bindings (no machinery change).
- Closure #8 is a §10.4 typo fix.

Per §3.6 acceptability criteria, **re-audit skipped, lock direct** — the v2 audit at [`reviews/HA-P6-2026-06-17-v2.md`](../../../reviews/HA-P6-2026-06-17-v2.md) IS the fresh-session audit that v2 compressed; v3 absorbs its eight named closures verbatim; running a v3-on-v2-audit-closures fresh-session re-audit would re-walk the same closures the v2 audit already named (a second-iteration would only validate the closure faithfulness, which the lock-commit message confirms explicitly). The lock-commit message will cite §3.6 compression criteria explicitly + the v2-audit-as-§3.6-re-audit reading.

**Audit recommendation absorption check (carried across v1 + v2 audits)**:
- v1 audit recommendation #5 (per-phase minimum-n gate on §9 third-branch propagation): **NOT absorbed in v3** — the v2 audit did not name a per-phase n-gate threshold either; #5 stays queued for HA-P6-v4 if it materially fires in the v3 test session's per-phase reads.
- v1 audit recommendation #6 (register-row pointer): executed at v1 lock; updated to point at v2 at v2 lock; **updated to point at v3 at v3 lock** per §3.8 gate 3.
- v2 audit's three side observations (§4.7 buildup boundary one-day check; v2 §4.8.1 closure (c) HA-P7 cross-reference verified; v2 spec invokes handoff path local-only): non-fires; flagged-for-awareness only; no closure required.

**Status: LOCKED 2026-06-17 by user acceptance under option-A compression per §3.6.** The pre-registration is locked at the state of this file's HEAD on 2026-06-17. Further modifications create HA-P6-v4 with v3 archived per [`hypothesis_lock_process.md §3.9 step 4`](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). The next session writes / revises `script.py` per the v2 + v3 closures and runs the v1-defined §10.4 protocol (dry-run → halt-or-go → full run → result.md). **After v3 lock, [`/research-review`](../../../reviews/README.md) may optionally run in a fresh session per [`feedback_pre_reg_writer_role.md`](C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_pre_reg_writer_role.md)** as a second-iteration validation of v3's closure faithfulness; if invoked, the review report lands in [`reviews/`](../../../reviews/) at `HA-P6-2026-06-17-v3.md` with the addendum *"Fresh session — no exposure to the v3 drafting context; doc-only knowledge; second-iteration validation that v3's closures faithfully absorb the v2 audit at `HA-P6-2026-06-17-v2.md`."* The user may also choose to skip this second-iteration audit and proceed directly to the v3 test session given the v3 closures' mechanical-extension character.

---

**Pre-registration v3 written 2026-06-17, AFTER the v2 fresh-session audit AND BEFORE any post-crash trajectory inspection on the per-channel recovery shape.** Locked at user acceptance. Any subsequent change creates HA-P6-v4.

**This is Layer 1 descriptive characterisation per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference), NOT a SUPPORTED / NOT-SUPPORTED inferential test.** P6 always produces a trajectory characterisation — the question is *what shape* the post-crash window has. The §5 "findings shape" is what the result.md will REPORT regardless of the actual data; the §9 "observation shape outcomes" are pre-spec'd downstream implications of each finding shape. The v2 closures (a) (b) (c) refine the §4.8.1 / §4.8.4 / §7 machinery; v3 closures #1-#8 further refine §4.8.1 / §7 / §8 / §10.4 per the v2 audit; the §1 + §5 + §9 framings are unchanged from v1.

HA-P6 closes the post-crash side of the multi-scale dynamics framing from the [lived-experience braindump](../../../lived_experience_garmin_pacing_2026-06-14.md). The pre-crash side is covered by P2 / HA01b / HA11 / P4 / P5 / HA-C4b; the recovery side has been a gap until now. **P6 is also the load-bearing input to HA-P7's window-length assumption**: if P6 finds the recovery period extends to 14 days or beyond, P7's 14d-recent-crash-density window is empirically validated; if recovery completes within ~5 days and the post-window is a generic gap day, P7's 14d window is a generic period, not a crash-specific one.

## 1. Claim

### 1.1 Primary (descriptive characterisation)

In the LC era (`date >= 2022-04-04`), for each of the 7 channels listed in §4.1, the per-day median + IQR trajectory across days `[t+1, t+5]` after crash_v2 episode-end (t0) **is characterised along three dimensions** (with the matched non-crash trajectory as comparator; "differs from comparator" reads bind to the §9 head operational binding):

- **Depth** — magnitude of the per-channel deviation from the lagged baseline at the minimum
- **Duration** — number of days until the channel returns to within 0.5 SD of the lagged baseline
- **Completeness** — fraction of the lagged-baseline level recovered by t+5

The matched non-crash trajectory is computed in **two parallel arms** (Option C): (a) matched-deep-trough non-crash days (strict RTM control); (b) lagged personal baseline per [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses). Both arms are reported; concordance across arms increases confidence in the recovery-shape characterisation; divergence is documented as a methodological finding.

### 1.2 Secondary (correlational sub-hypothesis)

For the descriptive characterisation outputs from §1.1, **Spearman correlations are reported with block-bootstrap 95% CIs** between:

- Per-episode recovery-rate (slope on `[t+1, t+5]`) AND same-episode crash duration (days)
- Per-episode recovery-completeness (% return to lagged baseline by t+5, **computed per the §4.5 step 7 formula with the v2 denominator-undefined ε = 0.5×σ_ch rule per channel; episodes with undefined completeness excluded from this correlation only**) AND next-crash interval (days to next crash_v2 episode start)

The secondary is **correlational descriptive only — NO SUPPORTED bar**. Block-bootstrap CIs at the per-channel `E[L]` determined by §4.8.1 (default 7 for PASS-real and PASS-fallback-degenerate channels; **override E[L]=14 for PASS-fallback-no-cutoff channels per v3 closure #2**; **min(round(E[L]\*), 21) for FAIL channels per v3 closures #3** — capped at 21) per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) handle the autocorrelation that would otherwise inflate apparent significance. The secondary's role is to surface whether the recovery-shape characteristics carry information about the broader crash dynamics, not to test a specific predictive claim. See §8 v3 granularity-mismatch caveat (closure #7) on the day-level-E[L]-on-per-episode-summary structural mismatch inherited from v1.

### 1.3 Tertiary (descriptive late-recovery sensitivity arm)

Same shape characterisation as §1.1, applied to days `[t+6, t+10]`. Reports whether the recovery has continued beyond t+5 OR has plateaued. Descriptive only.

---

## 2. Why we think this

- **Lived experience prior**. From the [lived-experience braindump](../../../lived_experience_garmin_pacing_2026-06-14.md): *"and just after a crash?"* is explicitly raised as an underexplored timescale. The multi-scale dynamics framing (*"strings of crashes, response to a previous longer period of ineffective pacing"*) motivates examining what happens AFTER a crash, not just before. P6 closes this gap.
- **PEM recovery-debt mechanism**. The biological story: PEM recovery is a multi-day autonomic re-equilibration process; recovery completeness plausibly mediates next-crash risk. If a crash is followed by partial-only recovery, the post-crash window itself becomes an elevated-risk window. This mechanism predicts P7's positive direction; P6 is its descriptive sibling.
- **Wiggers H5 — lag order** ([wiggers_testable_hypotheses.md#h5](../../../wiggers_testable_hypotheses.md#h5--each-metric-has-a-characteristic-lag-vs-exertion-lags-differ-by-metric), PDF lines 925-928): *"HRV drops after several days of overexertion ... even if the person rested well immediately after."* Implies a multi-day post-event autonomic tail with channel-specific characteristic lags. P6's per-channel timing characterisation (§1.1 duration) is the descriptive sibling of Wiggers H5.
- **Aitken et al. 2026** supports wearable signals as lagging indicators of subjective state (queued in [`_pending_literature_fetch.md`](../../../methodology/_pending_literature_fetch.md)).
- **Sibling project context**. The project has documented dose-confirmed responses on `stress_mean_sleep`, `all_day_stress_avg`, and `bb_lowest` per [citalopram_dose_response §5.6](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14). The recovery-shape question intersects with this: per-channel recovery shape may differ across Citalopram phases as a downstream consequence of the dose-response. The phase-stratified sensitivity arm in §4.7 addresses this.
- **Cheapest test in the queue alongside P7**. No FIT extraction; uses existing per-day columns + crash labels.

## 3. Data sources

- **Crash labels**: `crash_v2` scheme defined in [`crash_v2-definition/definition.md`](../crash_v2-definition/definition.md); the labels CSV `labels_crash_v2.csv` lives at `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv` (gitignored external data path) and is propagated into `per_day_master.csv` as the `is_crash` boolean column by the [`build_unified_dataset.py`](../../../pipeline/03_consolidate/build_unified_dataset.py) pipeline. Episode-level boundaries (start, end, duration) are derived from contiguous `is_crash == True` runs.
- **Per-day channels**: from `per_day_master.csv`. The 7 channels in §4.1.
- **Phase membership**: `dose_plasma_mg` column in `per_day_master.csv` (PK-smoothed per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)); phase derivable from the date via the `citalopram_phase(d)` function in that MD §3.
- **Analysis window**: LC era pooled (no train/validate split — descriptive characterisation does not need held-out validation per the [hypothesis_lock_process MD](../../../methodology/hypothesis_lock_process.md)). Per-phase n estimates given in §4.7.
- **Episode count**: **29 LC-era crash_v2 episodes** — predicate: contiguous `is_crash == True` runs from `per_day_master.csv` restricted to dates >= 2022-04-04 and <= 2026-06-05; source: `labels_crash_v2.csv` via `per_day_master.csv`. n=29 documented in [`personal_hypotheses.md` P6 register entry caveat 2](../../../personal_hypotheses.md). v1 dry-run confirmed n=29 with the v1 implementation's episode-detection (contiguous-run algorithm); see [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md) for the per-phase split (pooled 29; unmedicated 18; buildup 3; consolidation 6; afbouw 2; post_afbouw 0) and the episode roster (table of 29 rows with start/end/duration/phase/t0 per episode).

**Data-cut unchanged from v1**: as-of-date 2026-06-05. v2 does not advance the as-of-date.

**No FIT extraction required.** All inputs are existing per-day columns in the consolidated master.

## 4. Measurement protocol

### 4.1 Channel set (locked from v1; per-channel E[L] policy added in v2 §4.8.1)

Seven channels per phase, ordered by mechanism family:

| channel | dose-response status | family |
|---|---|---|
| `stress_mean_sleep` | CONFIRMED dose-modulated (β=+0.43/mg in buildup post-CPAP) | autonomic-load |
| `all_day_stress_avg` | CONFIRMED dose-modulated (β=+0.57/mg; strongest channel) | autonomic-load |
| `bb_lowest` | CONFIRMED dose-modulated (β=-1.13/mg) | recovery |
| `bb_overnight_gain` | partial (no buildup data; coverage starts 2024-09-18) | recovery |
| `resting_hr` | weak (consistent direction, near-significance) | cardiovascular |
| `gevoelscore` | outcome-channel (per [intervention_effects §3b](../../../methodology/intervention_effects_descriptive.md#3b-outcome-channel-contamination-check-gevoelscore)) — outcome contamination check | felt-state |
| `stress_low_motion_min_count_S60_Mlow` | indirectly dose-modulated (raw stress threshold) | autonomic-load (concurrence pattern) |

**Channel coverage caveats** (apply per phase):
- `bb_overnight_gain` is NaN before 2024-09-18 (~64% of LC-era days). For pre-2024-09-18 crash episodes, this channel emits NaN; the trajectory characterisation skips this channel for those episodes. Per-episode n's per channel reported in §10.1 dry-run. v1 dry-run confirmed 5 post-2024-09-18 episodes contribute to this channel.
- `gevoelscore` is the OUTCOME-channel; per [intervention_effects §3b](../../../methodology/intervention_effects_descriptive.md#3b-outcome-channel-contamination-check-gevoelscore), reading its trajectory is methodologically distinct from reading baseline channels. P6 reports `gevoelscore` trajectory as the **outcome-shape companion** (does the felt-state recovery shape match the autonomic-channel recovery shape?), NOT as a sibling baseline channel.
- `stress_low_motion_min_count_S60_Mlow` is the Session E primitive (commit `14a32a3`); 1722 valid days; coverage matches the stress-sample availability.

**v3 per-channel E[L] policy**: see §4.8.1 + §7. Each channel is assigned a **four-verdict** E[L] disposition (PASS-real / PASS-fallback-degenerate / PASS-fallback-no-cutoff / FAIL) at the test-session dry-run, computed on both the **pooled-LC** and the **unmedicated-stratum sensitivity arm** per v3 closures #1 + #2. The override magnitude is **capped at `min(round(E[L]*), 21)`** per v3 closure #3; cap-binding cases flagged in result.md.

`n_minutes_resp_above_18` (Session E respiration companion) is queued for v4 (orthogonal to other channels; would add a respiration trajectory arm).

### 4.2 Window definition (locked from v1)

- **Primary window**: `[t+1, t+5]` after `t0` (5 days). Matches the register entry.
- **Sensitivity arm**: `[t+6, t+10]` after `t0` (late-recovery; 5 days). Reports whether recovery has continued or plateaued beyond t+5.
- **Pre-event window for matched-baseline construction**: `[t0 - 90, t0 - 30]` (the standard lagged-personal-baseline window per CONVENTIONS §3.2).

### 4.3 t0 anchor (locked from v1)

- **Primary t0 = crash_v2 episode-end** (first day after the episode where `gevoelscore` returns above the crash_v2 threshold for the episode-end-defining number of consecutive days).
- **Sensitivity t0 = last-below-threshold-day** within the episode (the lowest-felt-state day; if multiple tied days, the last one).
- Both anchors reported; concordance increases confidence; divergence documented as t0-sensitivity finding.

### 4.4 Matched-baseline construction Arm A — matched deep-trough non-crash days (locked from v1)

For each crash episode `i` with episode-end day `t0_i`:

1. **Extract pre-crash trajectory**: gevoelscore on `[t0_i - 10, t0_i - 1]` (10 days before episode-end; covers the in-episode period + a brief pre-episode lead-in).
2. **Find candidate matched days**: LC-era days `d_match` that satisfy ALL of:
   - `d_match` is NOT in any crash_v2 episode within the surrounding `[d_match - 20, d_match + 10]` window
   - gevoelscore trajectory on `[d_match - 10, d_match - 1]` is within ±1 absolute gevoelscore-point of the crash episode's `[t0_i - 10, t0_i - 1]` trajectory at every aligned day (i.e. matched-pair similarity criterion)
   - `d_match` is in the same Citalopram phase as `t0_i` (per §4.7)
3. **If multiple candidates**: pick the one with smallest mean-absolute-deviation from the crash episode's pre-trajectory.
4. **If no candidates within ±1 gevoelscore-point**: relax to ±1.5, ±2 in sensitivity arms; if still no match → flag episode as "no Arm A control available"; that episode contributes only to Arm B.
5. **Matched control trajectory**: per-channel value on `[d_match + 1, d_match + 5]` (mirrors the crash's `[t0_i + 1, t0_i + 5]`).

Arm A is the **strict RTM control**: for each crash episode, the matched non-crash day's recovery trajectory shows what RTM-driven post-trough recovery looks like ABSENT a crash mechanism. If the crash's recovery trajectory matches the Arm-A trajectory, RTM dominates. v1 dry-run reported 27/29 episodes matched within the ±2 tolerance ladder (15 at ±1.0, 12 at ±2.0); v2 retains the same tolerance ladder.

### 4.5 Matched-baseline construction Arm B — lagged personal baseline (locked from v1; v2 step-7 ε rule added)

For each crash episode `i`:

1. **Lagged-baseline window**: `[t0_i - 90, t0_i - 30]` per CONVENTIONS §3.2.
2. **Restrict to LC-era days** (`_lagged_lcera` discipline): exclude pre-2022-04-04 days from the baseline window.
3. **Restrict to same-phase days** per [phase_stratification §5.A](../../../methodology/citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk).
4. **Restrict to non-crash days within the baseline window** (exclude `is_crash == True` days).
5. **Compute per-channel baseline statistics**:
   - **Baseline median** (μ_ch): trimmed mean (10/90 cut) of the channel's value across eligible baseline days.
   - **Baseline SD** (σ_ch): stdev of the same trimmed values.
   - Computed only when ≥ 40 of 60 eligible baseline days are valid AND same-phase.
6. **Per-channel z-score recovery shape**: `z_ch(t0_i + k) = (channel(t0_i + k) - μ_ch) / σ_ch` for k ∈ {1, 2, 3, 4, 5}.
7. **Recovery completeness — per-episode formula + v2 denominator-undefined rule**:
   - Formula: `% return = abs(channel(t0_i + 5) - channel(t0_i)) / abs(μ_ch - channel(t0_i))` — fraction of the deviation from baseline that has been recovered by t+5.
   - **Denominator-undefined rule (v2)**: completeness is **undefined** when `abs(μ_ch - channel(t0_i)) < ε` for `ε = 0.5 × σ_ch` (the threshold is per-channel-aware via σ_ch, so that low-σ channels like `gevoelscore` use a small ε proportional to their natural variability, while high-σ channels like `bb_overnight_gain` use a proportionally larger ε). Episodes with undefined completeness are still included in §1.1 trajectory aggregation (their raw recovery trajectory is informative) but are **excluded from the §4.8.4 completeness Spearman** for the channel where the rule fires (per-channel exclusion; an episode can be undefined-completeness for one channel and well-defined for another).
   - **Reporting**: the per-channel count of undefined-completeness episodes is reported separately in §6 + §10.1, alongside the missing-baseline-eligibility exclusion count (those are separate exclusion categories; an episode can be missing-baseline OR undefined-completeness, but the categories don't overlap because undefined-completeness requires a valid μ_ch).

Arm B is the **standard project-pattern control** matching the rest of the corpus.

### 4.6 CONVENTIONS §3.7 trajectory-detrend sensitivity (binding; locked from v1)

Per [CONVENTIONS §3.7](../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons): for each channel × phase × matched-baseline-arm, report a **detrended sensitivity arm**:

1. Fit a linear trend on the pre-crash baseline window `[t0_i - 90, t0_i - 30]` per channel.
2. Extrapolate the fitted line forward through the post-crash window `[t0_i + 1, t0_i + 5]` (and the late-recovery arm `[t0_i + 6, t0_i + 10]`).
3. Subtract the extrapolated line from both pre and post values.
4. Recompute the per-channel trajectory and the §1.1 depth / duration / completeness metrics on the residuals.
5. **Reading**: if the recovery shape SURVIVES detrending (the trajectory metrics are similar to the raw arm), the post-crash trajectory is genuinely event-driven (the crash); if the trajectory FAILS detrending (becomes a flat residual line), the apparent recovery was just the LC recovery trajectory continuing.

§3.7 binding applies because P6's central comparison is "recovery trajectory" vs "baseline" — structurally a pre-vs-post comparison on the LC frame. The detrend sensitivity is reported per (channel × phase × matched-baseline-arm) cell; the result table is dense but the §3.7 audit hook is firmly engaged.

### 4.7 Phase-stratified arm (descriptive only; locked from v1; v1 dry-run validated)

Per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification), report per-phase verdicts:

| phase | window | n (per v1 dry-run, post Sec-6 buildup CPAP buffer) |
|---|---|---:|
| unmedicated | LC start 2022-04-04 → 2024-04-08 | 18 |
| buildup (post-CPAP-buffer 2024-04-30+) | 2024-04-30 → 2024-06-19 | 3 |
| consolidation (30mg plateau) | 2024-06-20 → 2026-03-19 | 6 |
| afbouw + post-afbouw (merged) | 2026-03-20 → 2026-06-05 | 2 (0 in post_afbouw) |

v1 dry-run confirmed pooled n=29; the per-phase split is as reported above. **Per-phase reporting is descriptive only.** Wide CIs expected for low-n phases (buildup n=3; afbouw n=2); the *shape* differences are the finding, not the magnitude. The pooled-LC headline (the median trajectory aggregated across all 29 episodes) is the headline shape characterisation; per-phase shapes are reported alongside.

**Important per dose-response framework**: P6 caveat 5 in the register narrowed the v3 dose-response finding's impact on P6 specifically — three channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) inherit a recovery-shape calibration concern across the entire Citalopram-traject (2024-04 → ongoing). Per-phase reporting addresses this directly; the §3.7 detrend per phase is the within-phase calibration check.

### 4.8 Statistical machinery — descriptive trajectory + block-bootstrap CIs

#### 4.8.1 Per-channel per-day per-phase trajectory + **v3 four-verdict E[L]\* policy + override table with cap + within-stratum sensitivity arm + paired-bootstrap binding**

For each (channel × phase × matched-baseline-arm × detrend-arm) cell:

- Compute per-day median + IQR across the per-episode trajectories at days `[t+1, t+5]` (primary) and `[t+6, t+10]` (sensitivity).
- Compute 95% CIs on the per-day median via **stationary-bootstrap at the per-channel `E[L]`** per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The per-channel `E[L]` is determined at the test session's dry-run per the §7 four-verdict logic + the v3 override table (below). Wilson CIs are NOT used (Wilson assumes i.i.d.; per-episode trajectories on the same channel are not independent across crashes that span the same season / phase / pacing-state).
- Block lengths drawn from Geometric(1/E[L]); `B = 10,000` resamples for headline cells; report percentile CI.
- Individual-event traces (n=29 faint lines) overlaid on the median + IQR band per channel.
- **Per-episode `completeness_per_episode` array stored in the cell during this trajectory pass** (v2 closure (b)); read directly by §4.8.4. The per-episode value is computed per §4.5 step 7 (formula + v2 ε-undefined rule); undefined values are stored as NaN. Per-episode `raw_per_episode`, `z_per_episode`, `control_per_episode`, `completeness_per_episode` are all consistent-shape `(n_episodes, n_days)` (or `(n_episodes,)` for completeness, which is one scalar per episode).
- **Paired-by-episode bootstrap for the §9 first-branch trigger (v3 closure #4)**: for Arm-A cells, the per-day median DIFFERENCE (crash trajectory minus matched-control trajectory) is computed via **paired stationary-bootstrap**: each bootstrap iteration resamples episode indices (each resample draws one `(crash_i, matched_control_i)` pair from the n_eligible_pairs pool via stationary-bootstrap on the paired-index sequence at the per-channel `E[L]`); per-day median DIFFERENCE is computed on the paired-resample distribution; CI excludes 0 per the §9 head trigger binding. `B = 10,000` for the locked headline cell. This binds the §9 head's "paired stationary-bootstrap machinery" assertion to a concrete machinery in §4.8.1.

##### Data-driven E[L]\* companion — interpretation (v2 closure (c) + v3 closures #1, #5, #6)

The data-driven E[L]\* estimator is run **once per channel on TWO input series**, both under interpretation (ii) (pooled-LC daily time series of the channel, ordered by date):

**Series A — pooled-LC headline E[L]\***:
- LC era only (`date >= 2022-04-04`, `date <= 2026-06-05`)
- Non-crash days only (`is_crash == False`)
- No same-phase restriction (pooled across all phases)

**Series B — unmedicated-stratum E[L]\* sensitivity arm (v3 closure #1)**:
- Unmedicated stratum only (`date >= 2022-04-04 AND date < 2024-04-09`) — the longest single-phase clean-ACF window, no CPAP intervention, no Citalopram dose-response transitions
- Non-crash days only (`is_crash == False`)
- n=18 episodes' worth of LC days; n_eligible_days ~ 700 days (post-LC-start + non-crash filter)

**Series C — per-phase diagnostic E[L]\* (v2 carry-forward)**:
- Per-phase same-phase restriction added; reported in dry-run as diagnostic; does NOT trigger the override policy by itself.

**v3 four-verdict assignment logic (closure #2 splits PASS-fallback)** — the verdict is assigned per channel based on Series A (pooled-LC headline E[L]\*) with Series B's unmedicated-stratum E[L]\* as the cross-check:

The estimator (`compute_data_driven_block_length` / `estimate_block_length` in [`_utils/inference.py`](../../_utils/inference.py)) operates on the empirical ACF of an ordered time series; concatenating non-adjacent per-episode windows (the v1 interpretation) injects fake lag-1 discontinuities at every concat boundary, producing the "No clear ACF cutoff" / "Closed-form formula degenerate" fallback returns v1 observed for four of seven channels. v3 inherits v2's interpretation (ii) reading and HA-P7 [`test.py` line 763](../HA-P7/test.py)'s precedent (`estimate_block_length(cc14)` on the pooled-LC crash_count_14d time series).

**v3 closure #5 — verdict-range acknowledgement**: the FAIL gate uses `[3.5, 10.5]` (`|E[L]*-7|/7 > 0.5`). The methodology MD's override clause condition (i) gives an alternative example `< 3 or > 14` (`[3, 14]`). The MD's framing is "e.g." (example, not binding); v3 binds to the **factor-of-2 framing** consistent with the MD's earlier sentence "If E[L]\* differs from 7 by more than a factor of 2, flag for review." v3 acknowledges the choice: `[3.5, 10.5]` is the tighter reading; an `E[L]*=12` would FAIL under v3's gate where the MD's `[3, 14]` example would not (conservative direction; the v3 gate widens the override-trigger zone).

**v3 closure #6 — eligible-day filter deviation acknowledgement**: the methodology MD's override clause condition (i) specifies the ACF is "computed over Stratum 4 days" per [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) — "LC with gevoelscore + crash labels" (the full LC era including crash days). v3 deviates by excluding crash days (Series A's `is_crash == False` filter). The deviation is in the conservative direction: filtering crash-day spikes (which are by-construction the most anomalous days) yields a cleaner inter-crash-trajectory ACF that better matches the per-day median CI machinery §4.8.1 binds to. v3 acknowledges the deviation explicitly here; the audit trail is the §4.8.1 paragraph itself.

##### §7 four-verdict logic + per-channel E[L] override table (v3 refinement of v2 closure (a))

Replaces v2's three-verdict logic (which is itself the refinement of v1's binary FLAG / ok in [`script-v1-archived.py`](script-v1-archived.py) `sanity_checks()`). v3 splits PASS-fallback into two notes-driven sub-categories per v3 closure #2. The verdict is assigned per channel based on Series A (pooled-LC E[L]\*) with Series B (unmedicated-stratum E[L]\*) as the cross-check on level-shift contamination (v3 closure #1):

| verdict | trigger condition (Series A pooled-LC E[L]\*) | per-channel E[L] used in §4.8.1 CIs | result.md flag |
|---|---|---:|---|
| **PASS-real** | estimator returned a numeric value `E[L]*` AND `3.5 <= E[L]* <= 10.5` | 7 (project default) | none — the data-driven companion certifies the default's reasonableness |
| **PASS-fallback-degenerate** | estimator could not compute; note matches "Closed-form formula degenerate" OR "n<30 baseline pool" | 7 (project default) | "PASS-fallback-degenerate: estimator returned default 7 due to *<note>*; the default is operational, not a data-verified estimate" — surfaced per channel in result.md headline E[L] table + §3.7 detrend table |
| **PASS-fallback-no-cutoff** *(v3 NEW)* | estimator could not compute; note matches "No clear ACF cutoff" OR "all lags within max_lag are significant" — i.e. **positive long-dependence signal** | **14** (v3 conservative pre-spec for documented long-dependence channels; capped by closure #3 — `min(14, 21) = 14` so cap never binds at this verdict in practice) | "PASS-fallback-no-cutoff: estimator note indicates long dependence; v3 override E[L]=14 per §4.8.1" — surfaced per channel in result.md headline + §3.7 detrend table |
| **FAIL** | estimator returned a numeric value `E[L]*` AND (`E[L]* < 3.5` OR `E[L]* > 10.5`) | **per-channel override E[L] = `min(round(E[L]*), 21)`** per §4.8.1 cap (v3 closure #3) — Series B cross-check applies (v3 closure #1) | "FAIL-override: pooled-LC E[L]\*=<value>; v3 override E[L]=<override> per §4.8.1 table; cap-binding=<yes/no>; Series B unmedicated-stratum E[L]\*=<value>" — surfaced per channel in result.md headline + §3.7 detrend table |

**v3 closure #1 — Series B cross-check on FAIL**: when a channel's pooled-LC E[L]\* (Series A) > 10.5 (FAIL on the upper end) **AND** the unmedicated-stratum E[L]\* (Series B) is within `[3.5, 10.5]` (PASS-real on the cleaner anchor), the FAIL on Series A is partially a pooled non-stationarity artefact (intervention-induced level shifts inflating the empirical ACF). In that case, the **override magnitude binds to Series B** (the closer-to-clean ACF estimate) rather than Series A: `override E[L] = min(round(Series_B_E[L]*), 21)`. If Series B is also FAIL (E[L]\* > 10.5), the channel's long dependence is robust across the stratification and Series A's pooled-LC magnitude binds. Result.md surfaces both magnitudes alongside the binding choice.

**v3 closure #3 — override magnitude cap at 21**: the override magnitude is capped at `min(round(E[L]*), 21)`. Rationale: at n=29 episodes and per-day window of 5 days, E[L] = 21 already means one geometric block dominates ~70% of the window; beyond 21 the bootstrap is effectively a non-replacement subsample of one block. The cap at 21 is the resampling-resolution floor; cap-binding cases (where data-driven E[L]\* > 21) are flagged in result.md as "cap-binding" with the empirical Series A + Series B magnitudes + the cap-fire + the effective resampling-resolution constraint. The cap applies to FAIL channels only; PASS-fallback-no-cutoff at E[L]=14 is structurally below the cap.

**PASS-fallback-degenerate proceeds with E[L]=7** (does NOT halt). The closed-form-degenerate or n<30 fallback is a genuine "estimator cannot say" condition; defaulting to the project E[L]=7 is mechanically equivalent to the project default; the provenance ("estimator could not certify") is named in result.md.

**PASS-fallback-no-cutoff proceeds with E[L]=14** (does NOT halt; v3 NEW per closure #2). The "all lags significant" estimator note is a **positive signal of long dependence** — every lag from 1 to max_lag has significant autocorrelation — not a neutral fallback. Proceeding with E[L]=7 would be structurally false-conservative (CIs too narrow because resampling pretends dependence ends at 7 days when the ACF says it doesn't). E[L]=14 is the v3 conservative pre-spec for documented long-dependence channels: it doubles the project default, captures the one-week-doubling that the "all lags significant" note implies, and remains comfortably below the cap.

**FAIL proceeds with the override** (does NOT halt). The override widens the per-channel CIs honestly per the channel's documented autocorrelation; the alternative (E[L]=7 + caveat) would produce false-conservative CIs that mask the channel's multi-day drift. v3 closure #1 (Series B cross-check) refines the override magnitude when level-shift contamination is plausible.

**Halt condition** (refined from v1 + v2; v3 narrower):
- Pooled n outside `[25, 35]` — structural episode-detection sanity (carried unchanged).
- `bb_overnight_gain` zero post-2024-09-18 episodes — structural coverage sanity (carried unchanged).
- Any of the five PASS-real-expected channels (everything except `all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`, `bb_lowest`, `resting_hr`) returning FAIL — v2 narrower-halt condition; v3 carries forward. Note: v3 adds `bb_lowest` and `resting_hr` to the "expected to fall in PASS-fallback-no-cutoff under interpretation (ii)" set per v1's empirical pattern, so a FAIL on these two does NOT halt either; the disposition is the PASS-fallback-no-cutoff override at E[L]=14. (The four PASS-real-expected channels are now: `stress_mean_sleep`, `bb_overnight_gain`, `gevoelscore`, plus any unmedicated-stratum-clean channels; if any of these four FAIL on Series A AND Series B, halt + revise spec → HA-P6-v4.)

The four-verdict logic is the disposition; halt is the structural fallback.

##### Per-channel E[L] disposition table (v3 refinement of v2 closure (a))

Pre-specified at v3 lock. The override value is `min(round(E[L]*), 21)` from the test-session dry-run under interpretation (ii) — Series A (pooled-LC) by default, Series B (unmedicated-stratum) if v3 closure #1's Series-A-FAIL-but-Series-B-PASS condition fires. The override is a **policy choice** (rule + cap pre-spec'd); the empirical magnitudes come from the test session and are reported in result.md alongside the override.

| channel | v3 expected verdict (best estimate; binding logic per §7 table) | v3 disposition rule | rationale |
|---|---|---|---|
| `stress_mean_sleep` | PASS-real expected on Series A AND Series B | use whichever verdict fires per the four-verdict logic | dose-confirmed channel; daily-resolution stress signal; ACF expected to decay within a week. v1 (i)-interpretation E[L]\*=6.50 was already clean. |
| `all_day_stress_avg` | FAIL likely on Series A (long ACF inherits dose-response level shifts); PASS-real possible on Series B (unmedicated stratum, no Citalopram transitions) | if FAIL on A and PASS-real on B: override E[L] = min(round(B), 21). If FAIL on both: override E[L] = min(round(A), 21). | Documented multi-day drift (autonomic-load family; dose-modulated β=+0.57/mg). v1 (i)-interpretation E[L]\*=22.21 was inflated; v3 Series B cross-check disentangles within-phase ACF from pooled level-shift contamination. |
| `bb_lowest` | PASS-fallback-no-cutoff expected per v1 note "No clear ACF cutoff (all lags within max_lag are significant)" — if (ii) interpretation resolves the ACF then PASS-real | if PASS-fallback-no-cutoff: override E[L]=14 (v3 closure #2). If FAIL: override per §7 table. If PASS-real: E[L]=7. | Recovery channel; v1's "all lags significant" note is a positive long-dependence signal that v3 closure #2 absorbs with the E[L]=14 override. |
| `bb_overnight_gain` | PASS-fallback-degenerate likely (coverage gap → smaller eligible pool → estimator may degenerate) | use whichever verdict fires. If PASS-fallback-degenerate: E[L]=7 default. If PASS-fallback-no-cutoff: E[L]=14 override. If FAIL: override per §7 table. | Coverage gap (post-2024-09-18 only) constrains the eligible series; the v1 fallback was closed-form degenerate (= PASS-fallback-degenerate in v3 vocabulary). |
| `resting_hr` | PASS-fallback-no-cutoff expected per v1 note "No clear ACF cutoff" — if (ii) interpretation resolves then PASS-real | if PASS-fallback-no-cutoff: override E[L]=14 (v3 closure #2). If FAIL: override per §7 table. If PASS-real: E[L]=7. | Cardiovascular channel; same long-dependence pattern as bb_lowest in v1. v3 closure #2 absorbs it without halt. |
| `gevoelscore` | PASS-fallback-degenerate possible (closed-form degenerate in v1) or PASS-real under (ii) | use whichever verdict fires per the four-verdict logic | Outcome channel; daily-resolution self-report. v1 fallback was closed-form degenerate. |
| `stress_low_motion_min_count_S60_Mlow` | FAIL likely on Series A (count metric with high day-over-day autocorrelation); Series B cross-check applies | if FAIL on A and PASS-real on B: override E[L] = min(round(B), 21). If FAIL on both: override E[L] = min(round(A), 21). Cap likely to bind given v1 (i)-interpretation E[L]\*=30.72. | Documented multi-day-correlated count metric (Session E primitive); v1 (i)-interpretation E[L]\*=30.72 was inflated. v3 Series B cross-check + cap together disentangle and bound the override. |

**Cross-reference to the methodology MD's override clause**: per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) "Decision (proposed; pending user review)", per-hypothesis override is allowed when (i) the metric's empirical autocorrelation crosses zero at a lag substantially different from 7, (ii) the override is pre-registered in the hypothesis file before any test run, (iii) the override is justified in the hypothesis file with a 1-paragraph ACF readout. v3 satisfies all three for the FAIL-channel + PASS-fallback-no-cutoff overrides: (i) the FAIL verdict gates on `|E[L]*-7|/7 > 0.5` (v3 closure #5 binds factor-of-2 framing); for PASS-fallback-no-cutoff, the "all lags significant" note IS a stronger-than-factor-of-2 signal in the long direction; (ii) v3 IS the pre-registration vehicle, the override table is locked at v3 lock before the test run; (iii) the v3 §4.8.1 disposition-table-rationale column + the result.md per-channel ACF readout together satisfy the readout requirement — the rule + rationale + expected-pattern are pre-committed in hypothesis.md, the empirical magnitude lands at the test session per the v2-audit-acknowledged split-compliance reading.

The override extends the MD's per-hypothesis-override grammar to per-channel-within-a-hypothesis with v3-added refinements (Series B cross-check; cap; PASS-fallback-no-cutoff sub-verdict). This is a natural generalisation: a multi-channel hypothesis where channels have heterogeneous ACF structures should not be forced to one global E[L] for all channels; the MD's intent (cross-hypothesis comparability + p-hacking guard) is preserved because v3 pre-registers the per-channel policy + the override magnitudes + the cap at v3 lock.

#### 4.8.2 Per-channel recovery-completion-day estimate (locked from v1)

Per channel × phase × matched-baseline-arm: the **median day at which the channel returns to within 0.5 SD of the lagged baseline**. If no episode's trajectory returns within 0.5 SD by t+5, report "not within window" + median residual at t+5. If recovery is complete by t+1 (median trajectory already within 0.5 SD), report "complete by t+1" + median trajectory at t+1.

#### 4.8.3 Per-channel qualitative shape descriptions per phase (locked from v1; algorithmic pre-specs)

For each (channel × phase) cell, classify the median trajectory shape into one of six categories. The classifier operates on the Arm-B lagged-baseline z-scored median trajectory `z_ch(t+k)` for k in {1, 2, 3, 4, 5} (per §4.5 step 6) with first-differences `dz(k) = z_ch(t+k) - z_ch(t+k-1)` for k in {2, 3, 4, 5} and per-day block-bootstrap 95% CIs from §4.8.1. Categories are evaluated in priority order; the FIRST matching category wins:

1. **`no-meaningful-change`** — ALL of (a) per-day median |z_ch(t+k)| < 0.3 for every k in {1..5}, (b) per-day block-bootstrap 95% CI on the median includes 0 on every k in {1..5}, (c) §3.7 detrend residual on the median trajectory has slope |beta| < 0.05 SD/day.

2. **`overshoot-then-settle`** — ALL of (a) the median trajectory CROSSES the lagged baseline within the primary window (a sign-change between `z_ch(t+k)` and `z_ch(t+k+1)` for at least one k in {1..4}), AND (b) the post-crossing absolute z stays < 0.5 for every day from the crossing to t+5 (lands at baseline; does not oscillate back across).

3. **`monotonic-recovery`** — ALL of (a) the first-differences `dz(2), dz(3), dz(4), dz(5)` are sign-consistent (all > 0 if z_ch(t+1) is negative; all < 0 if z_ch(t+1) is positive — i.e. consistent direction toward baseline), AND (b) either |z_ch(t+1)| - |z_ch(t+5)| >= 1.0 (recovers at least 1.0 SD across the window) OR |z_ch(t+5)| < 0.5 (lands within 0.5 SD of baseline by t+5).

4. **`stair-step-recovery`** — ALL of (a) |z_ch(t+1)| - |z_ch(t+5)| >= 0.5 (net progress toward baseline of at least 0.5 SD across the window), AND (b) at least one |dz(k)| < 0.15 (one or more "flat" days mid-window), AND (c) the remaining first-differences are sign-consistent toward baseline (the recovery is interrupted by a flat plateau but resumes; does NOT reverse).

5. **`slow-grind-incomplete`** — ALL of (a) |z_ch(t+5)| < |z_ch(t+1)| (net progress toward baseline), AND (b) |z_ch(t+5)| >= 0.5 (incomplete recovery; still > 0.5 SD from baseline at end of window), AND (c) the cell did not match categories 1-4 above.

6. **`noisy-inconclusive`** — fallback. Fires if (a) the per-day block-bootstrap 95% CI half-width is > 1.0 SD on >= 3 of 5 days, OR (b) none of categories 1-5 match (signature of an oscillating / non-monotonic / non-classifiable trajectory). If a cell is flagged as `noisy-inconclusive` AND condition (a) is satisfied, the cell is annotated `noisy-CI-driven`; if only (b) is satisfied, the cell is annotated `noisy-shape-driven`. Result.md surfaces the annotation alongside the category.

The classifier emits the matched category PER (channel × phase × matched-baseline-arm × detrend-arm × t0-anchor × window-arm) cell in the result CSV; §9 propagations cite the **pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window** headline cell per channel (per the §9 head single-cell lock).

#### 4.8.4 Secondary correlational sub-hypothesis — block-bootstrap CIs + **v2 per-episode completeness threading (closure (b))**

For each channel × phase × matched-baseline-arm × {recovery-rate, recovery-completeness}:

- **Recovery rate**: per-episode slope of the channel's trajectory on `[t+1, t+5]` via OLS on the per-episode z-scored trajectory (`z_per_episode` stored in the cell during §4.8.1).
- **Recovery completeness**: per-episode `completeness_per_episode` value stored in the cell during the §4.8.1 trajectory pass (closure (b)); computed per §4.5 step 7 formula with the v2 ε-undefined rule. **Episodes with undefined completeness (per the §4.5 step 7 ε rule) are excluded from the completeness Spearman for the channel where the rule fires**; their per-channel counts are reported in result.md alongside the n of the Spearman.
- **Per-episode crash duration**: number of `is_crash == True` days in the episode (from contiguous-run detection).
- **Per-episode next-crash interval**: days from `t0` to the next crash_v2 episode start (NaN if no subsequent episode within LC era; reported as right-censored).
- **Spearman correlation** between (recovery-rate, crash-duration) and (recovery-completeness, next-crash-interval), per cell.
- **Block-bootstrap 95% CI** at the per-channel `E[L]` from §4.8.1 (default 7 for PASS-real / PASS-fallback channels; override for FAIL channels). Per-episode resampling within phase; B = 10,000.
- **CI containing 0 → null correlation read**; otherwise report sign + magnitude.
- **No SUPPORTED bar**. This is descriptive correlation, not an inferential test.

##### v2 baseline-source disambiguation for the single-cell-locked completeness Spearman (closure (b))

The single-cell lock for §9 bullets 7/8 is **pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window** per the v1 r2 closure (carried forward unchanged). The Arm-A label names the **§1.1 trajectory-comparison baseline** (matched-deep-trough non-crash days) that the cell's trajectory is reported against. The per-episode `completeness_per_episode` denominator μ_ch is **always from the Arm-B lagged baseline** (Arm-B's `μ_ch` per §4.5 step 5), because:

- Arm A produces a per-episode matched-control **trajectory** (5 days of channel values from `[d_match+1, d_match+5]`), not a per-episode baseline **mean**.
- The §4.5 step 7 completeness formula requires `μ_ch` (a scalar baseline level) and `channel(t0_i)` (a scalar episode-end value). The scalar `μ_ch` is well-defined only from Arm-B (the lagged personal baseline).
- The two arms answer different questions: Arm-A asks "does the post-crash trajectory match RTM-only?"; Arm-B asks "does the post-crash trajectory return to the pre-crash baseline level?". Completeness binds to the Arm-B question by construction.

This disambiguation closes the v1 spec ambiguity flagged by the v1 test session ("the cell is locked but the baseline-source for per-episode completeness is not"). v2 resolves: **all per-episode completeness values use Arm-B μ_ch**, regardless of the cell's named §1.1 baseline-arm. The "pooled-LC × Arm-A × ..." single-cell-lock identifier names the §1.1 trajectory-comparison cell; the §1.2 completeness Spearman uses the per-episode array from that cell, with denominators from Arm-B μ_ch.

---

## 5. Pre-registered findings shape (NOT a falsification criterion; locked from v1)

Per the lock-process MD §3.5 + the handoff §4.5: P6 is descriptive; there is NO SUPPORTED / NOT-SUPPORTED bar. The §5 section enumerates what the **result.md will report regardless of the actual data**:

1. **Per-channel per-day median + IQR + individual-event traces** for each of the 7 channels × {pooled LC, 4 phases} × 2 matched-baseline-arms × 2 detrend-arms × 2 window-arms (primary 5d + late-recovery 5d) × 2 t0-anchors. Result CSV emits one row per (channel, phase, baseline_arm, detrend_arm, window_arm, t0_anchor, day_offset) cell with median, IQR, individual-trace count, and block-bootstrap 95% CI **at the per-channel E[L] determined by the v3 §4.8.1 four-verdict logic** (PASS-real / PASS-fallback-degenerate / PASS-fallback-no-cutoff / FAIL).
2. **Per-channel E[L] verdict + value table** (v3 refinement of v2 closure (a)): one row per channel naming the **four-verdict** disposition (PASS-real / PASS-fallback-degenerate / PASS-fallback-no-cutoff / FAIL), the **Series A pooled-LC empirical `E[L]*`**, the **Series B unmedicated-stratum empirical `E[L]*`** (v3 closure #1 sensitivity arm), the binding-magnitude choice (A or B per closure #1), the **cap-binding flag** (yes/no per closure #3), the rationale per §4.8.1 disposition table, and the E[L] value used for that channel's per-day CIs.
3. **Per-channel recovery-completion-day estimate** (§4.8.2): median day to return within 0.5 SD of lagged baseline per channel × phase × matched-baseline-arm.
4. **Per-channel qualitative shape description** (§4.8.3): the classified shape per channel × phase, with the algorithmic priority-order pre-specs applied.
5. **§3.7 detrended sensitivity** per (channel × phase × matched-baseline-arm) cell.
6. **Secondary correlational sub-hypothesis** outputs (§4.8.4): Spearman correlations with block-bootstrap CIs for (recovery-rate, crash-duration) and (recovery-completeness, next-crash-interval) per channel × phase × matched-baseline-arm. **Per-channel undefined-completeness exclusion count** (v2 closure (b)) reported alongside each completeness-Spearman n.
7. **Concordance / divergence reads**: Arm A (matched-deep-trough) vs Arm B (lagged baseline) concordance per (channel × phase) cell. Divergence flagged as methodological finding per §9.
8. **t0-sensitivity concordance**: episode-end-t0 vs last-below-threshold-day-t0 concordance per (channel × phase × matched-baseline-arm) cell. Divergence flagged.

The result.md leads with a per-channel summary table (7 rows × pooled LC × primary-baseline-arm × no-detrend) for headline trajectory readings; the full multi-arm table is in the result CSV. The per-channel E[L] verdict table (#2 above) is reported in the result.md headline section, immediately after the trajectory summary.

---

## 6. Exclusion rules (locked from v1; v2 adds undefined-completeness)

- **Crash episodes outside the LC era** (`t0 < 2022-04-04` OR `t0 > 2026-06-05`) excluded.
- **Crash episodes whose `[t0+1, t0+5]` window extends beyond 2026-06-05 (data-cut)** are reported with truncated trajectories; the late-recovery arm `[t0+6, t0+10]` is reported with available data only.
- **Crash episodes within the 2024-04 boundary cluster** (`t0` in `[2024-04-09, 2024-04-16]`) excluded per [intervention_effects §8.1](../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable).
- **Buildup-phase episodes strictly before 2024-04-30** (first 21 days of buildup: 2024-04-09 through 2024-04-29 inclusive) excluded from the phase-stratified buildup arm (CPAP-end confound buffer). Included in the pooled LC headline with flag.
- **Crash episodes lacking lagged-baseline availability** (fewer than 40 of 60 same-phase eligible baseline days) excluded from Arm B; reported separately.
- **Crash episodes lacking matched-deep-trough candidates** (no Arm A match within ±2 gevoelscore-points after sensitivity relaxation) excluded from Arm A; reported separately.
- **Per-channel exclusions**: if a channel value is NaN at any of `[t+1, t+5]` or the lagged-baseline window has < 40 valid same-phase days for that channel, the channel × episode cell is excluded from the trajectory aggregation; reported in the dry-run.
- **Per-channel undefined-completeness exclusions (v2 closure (b))**: episodes with `abs(μ_ch - channel(t0_i)) < ε = 0.5 × σ_ch` for a given channel are excluded from the §4.8.4 completeness Spearman for THAT channel only; they remain included in the §1.1 trajectory aggregation. The per-channel count of undefined-completeness episodes is reported in the dry-run + the result.md §4.8.4 row. The categories don't overlap with missing-baseline (an undefined-completeness episode must have a valid μ_ch + σ_ch by definition).

## 7. Expected shape if hypothesis is true (locked from v1; v2 sanity-check ranges refined)

Qualitative descriptions per channel (sanity-check ranges; not falsification criteria):

- **`stress_mean_sleep` and `all_day_stress_avg`**: median trajectory peaks at t0 (highest deviation from baseline), gradually decays toward baseline over 3-5 days. Recovery-completion-day estimate: t+3 to t+5 in unmedicated phase; possibly delayed in consolidation phase (per the dose-modulation caveat).
- **`bb_lowest`**: median trajectory at minimum on t0 (or t+1 if the floor is hit overnight); gradually rises toward baseline over 1-3 days. Recovery-completion-day estimate: t+1 to t+2.
- **`bb_overnight_gain`**: where available (post-2024-09-18 only), trajectory at minimum on t0+1 (the first night after the episode-end); recovery to baseline over 2-3 days.
- **`resting_hr`**: median trajectory at maximum (highest above baseline) on t0; gradually decays over 2-4 days. Wiggers H5 prediction: HRV-related channel has a longer characteristic lag than HR.
- **`gevoelscore`**: by construction of episode-end definition, gevoelscore returns to above-threshold ON the episode-end day. Trajectory on `[t+1, t+5]` is the *post-recovery* gevoelscore — should remain near or above baseline. Any dip indicates a "stair-step" recovery pattern (partial recovery + relapse).
- **`stress_low_motion_min_count_S60_Mlow`**: per Session E exploration, this channel correlates ρ=0.79 with stress-time channels; trajectory should mirror `all_day_stress_avg`.

### v3 sanity-check verdicts (refinement of v2 closure (a) per v3 closures #1 + #2 + #3)

- **Sanity-check on episode count**: pooled LC n should be ~29 per the register. If pooled n is < 25 after exclusions OR > 35 → **halt** (the episode-detection algorithm may have changed; the dry-run should produce n=29 ± 2). v1 dry-run confirmed n=29.

- **Sanity-check on `E[L]*` per channel** (v3 four-verdict logic; interpretation (ii) — pooled-LC daily time series with eligible-day filter; Series A pooled-LC + Series B unmedicated-stratum sensitivity arm per v3 closure #1):
  - **PASS-real**: Series A `E[L]*` numeric AND `3.5 <= E[L]* <= 10.5` → proceed with E[L]=7 for that channel; no flag.
  - **PASS-fallback-degenerate**: Series A estimator could not compute; note matches "Closed-form formula degenerate" OR "n<30 baseline pool" → proceed with E[L]=7 for that channel; methodological flag in result.md naming the fallback reason per channel. Does NOT halt.
  - **PASS-fallback-no-cutoff** *(v3 NEW per closure #2)*: Series A estimator could not compute; note matches "No clear ACF cutoff" OR "all lags within max_lag are significant" — positive long-dependence signal → **override E[L]=14** for that channel; methodological flag in result.md naming the long-dependence pattern. Does NOT halt.
  - **FAIL**: Series A `E[L]*` numeric AND (`E[L]* < 3.5 OR E[L]* > 10.5`) → check Series B (unmedicated-stratum `E[L]*`) per v3 closure #1: if Series B is PASS-real (`3.5 <= Series B E[L]* <= 10.5`) AND Series A FAIL on the upper end (`E[L]* > 10.5`), the pooled-LC Series A is contaminated by level shifts; bind override to Series B: `E[L] = min(round(Series_B_E[L]*), 21)`. If both Series A and Series B FAIL: bind override to Series A: `E[L] = min(round(Series_A_E[L]*), 21)`. Cap-binding flag fires when `round(E[L]*) > 21`.
  - **Halt-on-FAIL discipline (v3)**: FAIL is the expected verdict for `all_day_stress_avg` + `stress_low_motion_min_count_S60_Mlow` (the two pre-spec'd-FAIL-override channels) and acceptable for `bb_lowest` + `resting_hr` (the two pre-spec'd-PASS-fallback-no-cutoff-or-FAIL channels per v1's empirical pattern). FAIL on any of the three remaining channels (`stress_mean_sleep`, `bb_overnight_gain`, `gevoelscore`) → **halt + revise spec → HA-P6-v4** (these are v3-PASS-real-expected channels under interpretation (ii)).

- **Sanity-check on `bb_overnight_gain` post-2024-09-18 episode count**: must be ≥ 1. v1 dry-run confirmed 5. If 0 → halt + revise spec → HA-P6-v4.

If the sanity check halts on the dry-run, the spec needs revision BEFORE running the full characterisation. The §10.1 dry-run is the gate.

## 8. Caveats result.md must explicitly acknowledge

- **Regression to the mean (RTM) is the central confound**. Crash days have low gevoelscore by definition; subsequent days regress toward the participant's mean by construction. Arm A (matched-deep-trough non-crash days) is the strict RTM control; if the crash's recovery trajectory matches the Arm-A trajectory on a channel × phase × detrend cell, RTM dominates that cell and the recovery shape is NOT autonomic-specific. **Result.md leads with the Arm A vs crash trajectory comparison per channel — this is the load-bearing read**.

- **n=29 LC-era episodes is sparse**. Per-channel per-day post-crash distributions have wide block-bootstrap CIs by construction. Descriptive characterisation is informative regardless; predictive sub-claims (§4.8.4) need careful framing — the CIs WILL be wide; reporting honestly is the discipline.

- **Power-calc dispatch** (per [hypothesis_lock_process MD §3.2 step 4 / §3.8 gate 1](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)). Power calc inapplicable per Daza 2018 within-subject design (see [Daza 2018 PDF](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) for the within-subject counterfactual framing); additionally, HA-P6 is Layer 1 descriptive characterisation per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference) with no SUPPORTED bar to power against. The block-bootstrap CIs per §4.8.1 are the inference machinery; their honest width at n=29 is the discipline.

- **Crash_v2 episode boundaries depend on the t0 definition**. The §4.3 t0-sensitivity arm (episode-end-t0 vs last-below-threshold-day-t0) reports concordance; divergence between arms is a t0-sensitivity finding for downstream consumers.

- **Self-reported crash labels** via crash_v2. The label generator (`gevoelscore` self-report) has the same instrument-level bias as P7 caveat 5. Any systematic drift in self-reporting propagates into both the episode boundaries AND the §4.8.4 secondary correlations.

- **Intervention-baseline dose-response broadens P6's caveat** per [P6 register caveat 5](../../../personal_hypotheses.md) (substantively broadened from pre-v3 reading). Three channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) are CONFIRMED dose-modulated; recovery-shape characterisation across the Citalopram-traject (2024-04 → ongoing) inherits a calibration concern on these channels. The §4.7 phase-stratified sensitivity arm + the §3.7 detrend per phase addresses this directly. `respiration_avg_sleep` is REJECTED dose-modulated (not in P6's panel; queued for v3). `resting_hr` is weakly dose-modulated (soft caveat).

- **Channel coverage gaps**. `bb_overnight_gain` starts 2024-09-18 (~64% of LC-era days NaN per [intervention_effects §2b](../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain)). Pre-2024-09-18 crash episodes contribute NaN to this channel; per-channel n's reported. v1 dry-run confirmed 5 post-2024-09-18 episodes contribute.

- **CONVENTIONS §3.7 trajectory-detrend is binding** per §4.6. Without §3.7 detrend, the apparent recovery shape may be the LC recovery trajectory (~10/year → ~2/year crash drop) continuing through the post-crash window. Phase-stratified detrend is the within-phase calibration check.

- **§3.4 inapplicable-to-primary by construction** (added per the [hypothesis_lock_process MD](../../../methodology/hypothesis_lock_process.md) §5 sanity check + the HA-P7 r2 audit-closure pattern). CONVENTIONS §3.4 crash-drop sensitivity binds correlations / regressions on PEM-pacing variables to report results with and without `is_crash == True` rows. **For HA-P6's primary descriptive trajectory characterisation**, §3.4 is **inapplicable by construction**: the trajectory IS computed across crash episodes; dropping `is_crash == True` rows would eliminate the entire test sample. **For the §4.8.4 secondary correlational sub-hypothesis** (recovery-rate vs crash-duration; recovery-completeness vs next-crash-interval), the correlation is at the per-episode-summary level, not per-day; `is_crash` is not a variable in the correlation. **The hook is therefore explicitly dispatched**: inapplicable-to-primary by-construction; inapplicable-to-secondary because the correlation operates on per-episode summary statistics, not per-day observations.

- **Matched-baseline construction (Arm A) is operational, not a gold-standard**. The ±1-gevoelscore-point matching tolerance is an operational choice; sensitivity arms at ±1.5 and ±2 report robustness. The matching does not control for unmeasured factors (life events, seasons, intervention transitions) that may co-occur with crashes; Arm B (lagged baseline) is the project-pattern complement.

- **The pre-crash window** (`t-N` to `t-1`) is explicitly **NOT IN SCOPE** for HA-P6 per the register entry. Pre-crash signals are covered by P2 / HA01b / HA11 / P4 / P5 / HA-C4b.

- **Mechanistic claims about recovery physiology are out of scope**. P6 characterises the *shape*; the *why* is for downstream hypothesis tests.

### v2 caveat: per-channel E[L] override honest autocorrelation framing (closure (a))

- **Two channels are pre-spec'd for per-channel E[L] override on FAIL** (per §4.8.1 override table): `all_day_stress_avg` and `stress_low_motion_min_count_S60_Mlow`. The v1 dry-run under the v1-interpretation produced E[L]\*=22.21 and E[L]\*=30.72 respectively (both far outside [3.5, 10.5]); the v2-interpretation (pooled-LC daily time series, non-crash filter) will produce different numbers but these channels have **documented multi-day drift inherent to their construction**: `all_day_stress_avg` is an autonomic-load aggregate over the day's stress samples; `stress_low_motion_min_count_S60_Mlow` is a daily count metric where consecutive days share a large fraction of their input via the rolling-stress-state. Their daily-resolution ACF should be expected to decay slowly. **The v2 per-channel E[L] override widens these channels' per-day CIs honestly**; the alternative (false-conservative E[L]=7) would understate the channels' autocorrelation and inflate apparent precision. Per-day CIs on these two channels will be visibly wider than the other five channels' CIs in result.md — this is the honest reporting per the methodology MD's "robustness to non-stationarity" weighting.
- **Four channels may produce PASS-fallback** depending on the test session's daily-series ACF: `bb_lowest`, `bb_overnight_gain`, `resting_hr`, `gevoelscore`. The estimator returning the default 7 in PASS-fallback is **operational, not data-verified**; result.md must surface this per channel with the estimator's `note` field (the fallback reason) so the reader does not mistake the default 7 for a certified estimate. v1 dry-run produced PASS-fallback for these four under interpretation (i); the v2 interpretation (ii) should produce real estimates for `bb_lowest`, `resting_hr`, and `gevoelscore` (their daily series have well-defined ACFs); `bb_overnight_gain` may continue to PASS-fallback due to the coverage gap producing a small eligible pool.

### v2 caveat: completeness baseline-source disambiguation (closure (b))

- **The §4.8.4 completeness Spearman binds to Arm-B μ_ch regardless of the cell's named §1.1 baseline-arm**. The single-cell lock for §9 bullets 7/8 is `pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window`; the "Arm-A" label there names the §1.1 trajectory-comparison baseline (matched-deep-trough non-crash days). The per-episode `completeness_per_episode` value computed for the §4.8.4 Spearman uses the **Arm-B lagged baseline** μ_ch + σ_ch (per §4.5 step 5), because the completeness formula requires a scalar baseline level (which Arm-B provides) and Arm-A provides only a 5-day matched-control trajectory. Result.md surfaces this disambiguation in the §4.8.4 row header.
- **Undefined-completeness exclusion is per-channel**: an episode can be undefined-completeness for one channel (`abs(μ_ch - channel(t0_i)) < 0.5 × σ_ch` fires) and well-defined for another. The per-channel count of undefined-completeness episodes is reported alongside the n of the completeness Spearman for that channel. This is separate from the missing-baseline exclusion (an undefined-completeness episode must have a valid Arm-B μ_ch + σ_ch by definition).

### v3 caveat: pooled-LC E[L]\* stationarity contamination + unmedicated-stratum sensitivity arm (closure #1)

- **The pooled-LC daily series spans 2022-04-04 → 2026-06-05 (~4 years) and crosses intervention transitions** documented as level shifts on the autonomic-load channels per [`intervention_effects_descriptive.md`](../../../methodology/intervention_effects_descriptive.md): the CPAP-start boundary (2024-04-09), Citalopram buildup (2024-04-30 → 2024-06-19), 30mg plateau (2024-06-20 → 2026-03-19), and afbouw (2026-03-20 → 2026-06-05). Three channels (`stress_mean_sleep` β=+0.43/mg; `all_day_stress_avg` β=+0.57/mg; `bb_lowest` β=-1.13/mg) have CONFIRMED dose-modulated level shifts at these transitions. **The pooled-LC E[L]\* under interpretation (ii) inherits intervention-induced level-shift contamination in the empirical ACF**: a non-stationary series with intervention-induced level shifts shows spurious long-range correlation reflecting the level shifts rather than within-phase autocorrelation. The same channels that triggered v1's HALT (`all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`) are the channels with the strongest documented dose-response and therefore the strongest pooled-LC ACF contamination. The v3 §4.8.1 within-stratum E[L]\* sensitivity arm (Series B; unmedicated stratum 2022-04-04 → 2024-04-08, no CPAP/Citalopram transitions; n=18 episodes' worth of LC days) is the **cleaner ACF anchor**; when Series A FAIL > 10.5 AND Series B PASS-real ∈ [3.5, 10.5], the v3 closure #1 binding rule rebinds the FAIL-override magnitude to Series B (closer-to-clean ACF). Result.md surfaces both magnitudes alongside the binding choice. The unmedicated-stratum sensitivity arm closes the L2.2 substantive fire from the v2 audit ([`reviews/HA-P6-2026-06-17-v2.md`](../../../reviews/HA-P6-2026-06-17-v2.md) §2 + §4 recommendation #1).

### v3 caveat: override magnitude cap at E[L]=21 (closure #3)

- **The per-channel E[L] override magnitude is capped at `min(round(E[L]*), 21)`**. Rationale: at n=29 episodes + 5-day window, an effective bootstrap block at E[L]=21 means one geometric block dominates ~70% of the window; beyond 21 the resampling collapses to a non-replacement subsample of one block, and the per-day median CI width becomes the resampling-resolution floor rather than the data-driven estimate. **Cap-binding cases** (where data-driven E[L]\* > 21) are flagged in result.md naming the channel + the cap-fire + the empirical Series A + Series B magnitudes + the effective resampling-resolution constraint. The cap-binding flag tells the downstream reader that the per-day CI is at the n=29-imposed resolution floor, not at the data-driven ACF reading; cap-binding does NOT change the channel's verdict (it remains FAIL with override; the override is just bounded). The cap closes the L1.3 minor fire from the v2 audit on unbounded override magnitude (§2 + §4 recommendation #3).

### v3 caveat: §4.8.4 day-level-E[L]-on-per-episode-summary granularity mismatch (closure #7; structural, inherited from v1)

- **The §4.8.4 secondary Spearman CIs use the per-channel `E[L]` from §4.8.1 at per-episode resampling within phase**, but the methodology MD's block-length policy was designed for **day-level inference**. Per-episode summaries (recovery-rate slope; recovery-completeness scalar; crash-duration count; next-crash-interval days) are not autocorrelated within an episode in the same way daily values are; the inter-episode autocorrelation that the §4.8.4 bootstrap should model is at the **inter-episode-interval level** (clusters of consecutive episodes within a season; gap patterns between distant episodes), not the day-level. **The day-level E[L] on per-episode resampling over-conservatively widens the per-episode-summary CIs by construction** — the bootstrap pretends consecutive episodes are autocorrelated at the same lag as consecutive days, which is structurally too strong for the n=29 sparse-event corpus. This is a **structural choice for cross-cell comparability**: using the same per-channel E[L] across all §4.8.x cells preserves cross-cell comparability of CIs at the cost of per-episode CI over-conservatism. The **per-episode-summary-aware block length** alternative (inter-episode interval structure; estimator on the sequence of inter-episode gaps; or treating per-episode summaries as i.i.d. for the sparse-event corpus) is **deferred to a methodology MD update + a v4 absorption** if the §4.8.4 Spearman CIs land conspicuously wide in the v3 result.md. This is inherited from v1 (the v1 audit did not catch it; the v2 audit's side observation surfaced it). v3 acknowledges + defers; result.md will name the structural choice in the §4.8.4 row header. Closes the v2 audit's §2 side observation + §4 recommendation #5.

## 9. What we do with each observation shape (locked from v1)

The §9 section enumerates pre-spec'd downstream implications per observation shape. **There are no SUPPORTED / NOT-SUPPORTED verdicts**; the result.md produces a trajectory characterisation, and the shape it produces triggers one or more of the following downstream propagations:

**Operational binding for the §9 first-branch trigger** ("statistically-distinguishable median trajectory from matched control"): per channel, the per-day block-bootstrap 95% CI on the median DIFFERENCE (crash trajectory minus matched-control trajectory, computed via the §4.8.1 paired stationary-bootstrap machinery at the **per-channel E[L]** from §4.8.1, B=10000) excludes 0 on **>= 2 of 5 primary-window days**. A sensitivity arm at the stricter **>= 3 of 5 days** threshold is reported alongside. The "channel is statistically distinguishable" predicate is evaluated PER channel; the "≥ 3 of 7 channels" gate in the first bullet then aggregates across channels. The trigger is evaluated only on the pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window cell per channel (per the single-cell lock below).

**Single-cell headline lock for §9 bullets 7 and 8 (secondary correlational propagations)**: the §4.8.4 secondary correlations are computed for every (channel × phase × matched-baseline-arm × detrend-arm) cell, but §9 bullets 7 and 8 fire on ONE pre-specified cell only — **pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window**. All other cells are reported but cannot fire §9 bullets 7 or 8 independently. This matches the HA-C4b r2 + HA-P7 r2 single-cell-lock pattern per [hypothesis_lock_process MD §4.2 closure (a)](../../../methodology/hypothesis_lock_process.md#42-layer-3-substantive--multi-comparison-discipline). Cells outside the locked cell that show CI excludes 0 on §4.8.4 are reported in the result CSV under a `secondary_cell_signal` column but flagged as diagnostic-only.

- **Distinct recovery shape across multiple channels (≥ 3 of 7 channels in the pooled LC × Arm-A × no-detrend cell show statistically-distinguishable median trajectory from matched control, per the §9-head operational binding)** → **P6 has characterised a real post-crash signature**. Downstream propagations:
  - Update the [`crash_episode_descriptive.md`](../../../methodology/crash_episode_descriptive.md) MD with the empirical per-channel timing estimates from §4.8.2.
  - Emit a per-channel timing table (channel × phase × recovery-completion-day-estimate) for downstream hypothesis-test mechanism-matching.
  - Inform HA-P7's window-length assumption: if the median recovery-completion-day-estimate across channels falls within `[3, 5]` days, P7's 14d window is a *generic period covering recovery* + further; if it extends to 7-10+ days, P7's 14d window is *recovery-specific*.

- **Recovery shape matches matched-baseline (Arm A median trajectory) on the majority of (channel × phase) cells** → **RTM dominates; no autonomic-specific recovery signature distinguishable from generic-low-score-day recovery**. Downstream propagations:
  - P7's 14d window assumption is empirically validated as a *generic recovery period*, NOT a crash-specific one. The recovery-debt mechanism claim in P7's caveat 1 weakens (a NOT-SUPPORTED P7 verdict would have an additional explanation here).
  - The lived-experience "the days after a crash feel different" framing has limited empirical support at the autonomic-channel level. Document for the [garmin_pacing_practice.md](../../../methodology/garmin_pacing_practice.md) operational protocol.
  - Channel-specific exceptions (cells where the crash trajectory IS distinguishable from RTM) are flagged as individual findings worth follow-up.

- **Recovery shape fails §3.7 detrend on consolidation only (the consolidation-phase trajectory disappears under detrending; unmedicated and afbouw phases survive)** → **the consolidation-phase apparent recovery was the LC trajectory leaking through; the unmedicated baseline characterisation is the truthful one**. Downstream propagations:
  - The consolidation-phase recovery-completion-day estimates per channel are NOT useable as priors for downstream tests; only the unmedicated estimates are trustworthy.
  - The buildup-vs-afbouw asymmetry hypothesis being explored in [phase_stratification §8.4](../../../methodology/citalopram_phase_stratification.md#84-the-buildup-and-afbouw-magnitude-asymmetry-as-a-research-question) gains a documentation point: dose-state matters for the recovery-shape characterisation.
  - The §4.6 detrend per phase is the load-bearing read; the result.md leads with this when this finding pattern emerges.

- **Per-channel timing differences observed (≥ 2 channels show recovery-completion-day estimates differing by ≥ 2 days, e.g. bb_lowest recovers in 2 days while stress_mean_sleep recovers in 5)** → **flag for downstream mechanism-matching**. Downstream propagations:
  - Future hypothesis tests with a specific mechanism claim should pick the channel whose recovery timing matches the claimed mechanism (per Wiggers H5).
  - Update [`methodology/time_resolution.md` §2.3](../../../methodology/time_resolution.md) with per-channel timing notes — the situational-multi-day-window category gets per-channel timing anchors.
  - The recovery-completion-day table per channel becomes a reference asset for the project, queued for citation in subsequent pre-regs.

- **Arm A and Arm B baselines diverge substantially** (concordance < 50% of (channel × phase) cells) → **methodological finding worth documentation**. Document in §9 of the result.md; possibly investigate which arm is more trustworthy on this corpus + flag for the [hypothesis_lock_process MD](../../../methodology/hypothesis_lock_process.md) as a project-pattern question.

- **t0-sensitivity arms (episode-end vs last-below-threshold-day) diverge substantially** → **t0 definition matters**. Report which anchor produces the stronger / cleaner shape per channel. The crash_v2 episode-end definition might need refinement (queued for crash_v3).

- **Secondary correlational sub-hypothesis (§4.8.4) finds OR (CI excludes 0) on recovery-rate ↔ crash-duration** → **recovery shape carries information about same-episode dynamics**. Document; emit for the downstream P7 covariate-sensitivity (§4.5.4 of HA-P7) as a candidate non-`crash_count_14d` covariate.

- **Secondary correlational sub-hypothesis (§4.8.4) finds OR on recovery-completeness ↔ next-crash-interval** → **recovery debt is empirically supported**. Document; this is the strongest single result HA-P6 can produce, because it directly addresses the §1.2 secondary sub-hypothesis's predictive intent. Inform P7's recovery-debt-vs-shared-cause caveat 1 disambiguation.

- **Spec sanity-check halts on dry-run** (pooled n outside `[25, 35]`; `bb_overnight_gain` zero post-2024-09-18 episodes; any of the five "PASS-real-expected" channels FAIL under interpretation (ii)) → DO NOT run the full characterisation. Document the failure in the dry-run report; revise the spec (creating HA-P6-v3 with audit trail).

## 10. Detection script architecture (locked from v1; v2 modifications to §10.1 + §10.2)

The script is single-stage; no extraction required (labels + per-day channels both in `per_day_master.csv`).

### 10.1 Stage 1 — characterisation script (`HA-P6/script.py`, to be written / revised in next session)

Loads `per_day_master.csv` + derives `is_crash` episode boundaries (contiguous-run detection); applies §4.2 + §4.3 + §4.4 + §4.5 + §4.6 + §4.7 filters per (channel × phase × baseline_arm × detrend_arm × window_arm × t0_anchor) cell; computes per-day median + IQR + block-bootstrap CIs at the **per-channel E[L] from §4.8.1** (§4.8.1) + recovery-completion-day estimates (§4.8.2) + qualitative shape classifications (§4.8.3) + secondary correlations with **per-episode completeness threaded from the cell** (§4.8.4).

**v3 implementation discipline notes for the test-session author** (v2 notes refined per v3 closures #1, #2, #3, #4):
- The **`completeness_per_episode` array** must be computed and stored in the cell during the §4.8.1 trajectory pass (not in `secondary_correlations`); the array shape is `(n_eligible_episodes,)`, with NaN for episodes where the v2 ε-undefined rule fires (v2 carry-forward; unchanged in v3).
- The **per-channel E[L] verdict** is computed once per channel in `sanity_checks()` using `compute_data_driven_block_length` on **two input series** (v3 closure #1): **Series A** (pooled-LC daily series, no same-phase restriction; the headline E[L]\*) and **Series B** (unmedicated-stratum-only daily series, 2022-04-04 → 2024-04-08; the sensitivity arm). The result is stored in a dict mapping channel → {verdict: PASS-real/PASS-fallback-degenerate/PASS-fallback-no-cutoff/FAIL, el_star_pooled: float, el_star_unmedicated: float, el_used: int, binding_series: "A" or "B", cap_binding: bool, note_pooled: str, note_unmedicated: str}; the `el_used` value is then threaded into every `run_cell` call for that channel for the per-day CI bootstrapping.
- **Four-verdict assignment per channel** (v3 closure #2): map the estimator's `note` field to the right sub-verdict:
  - `note in {"", "ok"} AND 3.5 <= el_star <= 10.5` → PASS-real → el_used = 7
  - `note matches "Closed-form" OR note matches "n<30"` → PASS-fallback-degenerate → el_used = 7
  - `note matches "No clear ACF cutoff" OR note matches "all lags"` → PASS-fallback-no-cutoff → el_used = 14
  - `note in {"", "ok"} AND (el_star < 3.5 OR el_star > 10.5)` → FAIL → see Series B cross-check + cap (v3 closures #1 + #3)
- **Series B cross-check on FAIL** (v3 closure #1): if Series A FAIL on upper end (`el_star_pooled > 10.5`) AND Series B PASS-real (`3.5 <= el_star_unmedicated <= 10.5`): `el_used = min(round(el_star_unmedicated), 21)`; `binding_series = "B"`. Otherwise: `el_used = min(round(el_star_pooled), 21)`; `binding_series = "A"`. `cap_binding = (round(el_star) > 21)`.
- **Paired-by-episode bootstrap for §9 first-branch trigger** (v3 closure #4): for the §9 first-branch evaluation on the locked headline cell (pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window), the per-day median DIFFERENCE CI is computed via a paired stationary-bootstrap: episode-pair indices `(crash_i, matched_control_i)` are resampled jointly via stationary-bootstrap on the paired-index sequence at the channel's `el_used`; per-day median DIFFERENCE is computed on the paired-resample distribution; CI excludes 0 per the §9 head trigger binding.
- The **§4.5 step 7 ε rule** is per-channel-aware via σ_ch; `ε = 0.5 * baseline['sigma']` per (channel, episode) cell; per-episode completeness is set to NaN when the denominator falls under ε (v2 carry-forward; unchanged in v3).
- **Halt conditions** (v3 narrower than v2): pooled n outside [25, 35] (unchanged); bb_overnight_gain zero post-2024-09-18 (unchanged); **FAIL on any of `stress_mean_sleep`, `bb_overnight_gain`, `gevoelscore`** (the three v3-PASS-real-expected channels under interpretation (ii)); halt fires only if BOTH Series A AND Series B FAIL for any of those three.
- **No halt** on PASS-fallback-degenerate (any channel); no halt on PASS-fallback-no-cutoff (any channel; mechanically dispositioned to E[L]=14); no halt on FAIL for the two pre-spec'd-FAIL-override channels (`all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`) or the two PASS-fallback-no-cutoff-or-FAIL channels (`bb_lowest`, `resting_hr`).

Outputs:
- `dry-run-report.md` per §10.2 (replaces the v1 archived dry-run report).
- `result.md` with headline summary table + **per-channel E[L] verdict table** (v2 §5 #2) + per-channel trajectory plots (matplotlib) + per-phase qualitative descriptions + observation-shape outcome propagations per §9.
- `result.csv` with full multi-arm per-day-per-cell trajectory data + per-channel `completeness_per_episode` arrays.
- `result-data.json` with per-cell payload including the v2 per-episode arrays.
- `plots/` folder with per-channel × phase trajectory PNGs (median + IQR band + individual traces).

### 10.2 Dry-run mode (`script.py --dry-run`)

Prints:
- Pooled-LC + per-phase episode counts after §6 exclusions.
- Per-channel × per-phase sample sizes (n episodes contributing to each cell).
- **Per-channel E[L]\* under interpretation (ii) — TWO series** (v3 closure #1): Series A pooled-LC E[L]\* + Series B unmedicated-stratum E[L]\* + per-channel four-verdict disposition (PASS-real / PASS-fallback-degenerate / PASS-fallback-no-cutoff / FAIL) per §4.8.1 + estimator's `note` field per series + binding-series choice (A or B) + cap-binding flag (yes/no) per channel.
- **Per-channel undefined-completeness episode count** (v2 closure (b)) — separate from missing-baseline counts.
- Sanity-check ranges per §7 (n=29 ± 2 pooled; per-channel timing estimates roughly in expected ranges; Series A E[L]\* per channel within [3.5, 10.5] for the three v3-PASS-real-expected channels: `stress_mean_sleep`, `bb_overnight_gain`, `gevoelscore`).

**If any halt sanity check fails → halt + revise spec → HA-P6-v4.** Halt is narrower in v3 than v2: the two pre-spec'd-FAIL-override channels (`all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`) do NOT halt; the two PASS-fallback-no-cutoff-or-FAIL channels (`bb_lowest`, `resting_hr`) do NOT halt either (v3 closure #2 absorbs them); only the three v3-PASS-real-expected channels FAILing on BOTH Series A AND Series B would halt.

### 10.3 Stage 2 — `result.md`

Headline section: per-channel summary table (7 rows × pooled LC × Arm-A × no-detrend) with median recovery-completion-day-estimate + qualitative shape + concordance vs Arm-A baseline. **Immediately followed by the per-channel E[L] verdict table** per §5 #2 (v3 refinement): one row per channel naming the **four-verdict** disposition (PASS-real / PASS-fallback-degenerate / PASS-fallback-no-cutoff / FAIL), **Series A pooled-LC empirical `E[L]*`**, **Series B unmedicated-stratum empirical `E[L]*`** (v3 closure #1), the binding-magnitude choice (A or B), the **cap-binding flag** (yes/no per v3 closure #3), the rationale per §4.8.1 disposition table, and the E[L] value used for that channel's per-day CIs.

Subsequent sections: per-phase tables; matched-baseline-arm comparison tables; §3.7 detrend sensitivity per cell; secondary correlational sub-hypothesis outputs with **per-channel undefined-completeness exclusion counts** (v2 carry-forward) + **§4.8.4 row header naming the day-level-E[L]-on-per-episode-summary structural mismatch** (v3 closure #7); observation-shape outcome propagations per §9.

Caveats section per §8 + the §3.4 inapplicable-to-primary dispatch + the v2 (a) autocorrelation-honesty bullet + the v2 (b) completeness-source-disambiguation bullet + the v3 (#1) pooled-LC stationarity contamination bullet + the v3 (#3) cap-binding bullet + the v3 (#7) §4.8.4 granularity-mismatch bullet.

### 10.4 Run protocol

1. **Dry-run** (`python script.py --dry-run`): prints sample sizes + Series A + Series B E[L]\* + per-channel four-verdict + Series B binding choice + cap-binding flag + sanity checks per §7. **If any halt sanity check fails → halt + revise spec → HA-P6-v4.** PASS-fallback (both sub-categories) and pre-spec'd-FAIL-override channels (the four channels: `all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`, `bb_lowest`, `resting_hr`) do NOT halt; the dry-run emits the verdicts and proceeds-ready.
2. **Full run** (`python script.py`): emits `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-P6-v4 with the v3 result archived (per the project's locked-pre-reg discipline + the [hypothesis_lock_process MD §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock)).

**Estimated test script length (v3 closure #8 — arithmetic-consistent rewording)**: v3 is a planned rewrite at ~450 lines. v1's [`script-v1-archived.py`](script-v1-archived.py) is 1842 lines (the v1 report-emit + dry-run logic + per-cell trajectory pass + bootstrap machinery + Arm A matching + classification + plotting; the file size reflects v1's monolithic single-file architecture). v3 targets a leaner architecture that drops the v1 report-emit bloat into helper modules; the v3-specific closure-driven new logic adds roughly: ~30 lines for completeness threading (v2 carry-forward; closure (b)); ~40 lines for the four-verdict E[L] policy + the Series A / Series B input construction + the Series B cross-check on FAIL (v2 closure (c) + v3 closures #1, #2, #5, #6); ~10 lines for the cap (v3 closure #3); ~20 lines for the paired-by-episode bootstrap binding for the §9 first-branch trigger (v3 closure #4). Total v3-NEW logic ≈ 100 lines added relative to a hypothetical v1-clean-rewrite at ~350 lines = v3 ~450 lines.

---

*Pre-registration v3 drafted 2026-06-17 by Claude (Opus 4.7 1M) in reviewer-mode-with-authorization, in response to the v2 fresh-session audit at [`reviews/HA-P6-2026-06-17-v2.md`](../../../reviews/HA-P6-2026-06-17-v2.md) (verdict: PASS with caveats; 8 named closures absorbed). v2 archived at [`hypothesis-v2-archived.md`](hypothesis-v2-archived.md). Lock requires user acceptance. Optional second-iteration fresh-session [`/research-review`](../../../reviews/README.md) on v3 after lock per CONVENTIONS §1.2 + [`feedback_pre_reg_writer_role.md`](C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_pre_reg_writer_role.md) — if invoked, lands at `reviews/HA-P6-2026-06-17-v3.md`; the user may also skip the second iteration given the mechanical-extension character of the v3 closures.*
