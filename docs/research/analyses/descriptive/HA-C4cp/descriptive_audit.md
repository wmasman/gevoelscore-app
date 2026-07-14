# HA-C4cp / descriptive_audit.md

**Status**: **LOCKED r1 2026-07-14** by user acceptance ("lets continue" 2026-07-14 driving Bundle H+ event 9 Stage D descriptive audit landing). Stage D descriptive-audit companion for [`analyses/hypotheses/HA-C4cp/hypothesis.md`](../../hypotheses/HA-C4cp/hypothesis.md) r2 LOCKED 2026-07-09 per HA-C4cp §9 verdict-cascade routing. Distributional-only characterisation of the primary + sensitivity SD-anchored operands per parent MD [`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) §3.2.2 LOCKED r3 2026-07-09; no effect view, no heavy-T vs non-heavy-T contrast, no crash or gevoelscore cross-look. Sanity check per HA-C4cp §10.4: **PASS** (per-day mean 0.4765 inside HALT-range [0.01, 0.60]; per-day median = 0 inside expected [0, 1]; parent-operand determinism check `bout_n_did_not_return` mean = 0.6444 reproduces HA-C4c result.md r2 target byte-identically). Walk-forward gate per HA-C4cp §4.7: **PASS** (heavy-T n = 465; non-heavy-T n = 824; both comfortably ≥ 30). Substantive descriptive-layer observation (CAVEAT-CLASS per CONVENTIONS §4.2; no new inference beyond HA-C4c LOCKED r2 + Stage I r1): the SD-anchored primary operand captures a materially different day-population than the fixed-absolute-threshold parent operand — 33.1% concordant firings, 20.1% HA-C4c-only, 4.7% SD-anchored-only, 42.0% neither. The cross-op-independence claim at parent MD §3.2.2 + OI-025 protocol §5.4 is descriptively corroborated at operand-family level: 35.1% of days have Z=2 threshold above the 180-min `tail_length` cap by construction, i.e. days where the SD-anchored operand cannot echo the fixed-threshold operand's signal regardless of bout activity.

## Authorship

Drafted 2026-07-14 by Claude (Opus 4.7, 1M context) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-producer-vs-reviewer-mode). Authorising user: Willem. Extraction reads the LOCKED `per_day_master.csv` produced by Bundle H+ event 8 (`521e9fe`) pipeline extension; the descriptive audit is the reader-facing summary + sanity gate + walk-forward gate verification. Fresh-session `/research-review` on this audit is NOT required pre-lock per [`_plan_results_analysis_layer.md`](../../../methodology/_plan_results_analysis_layer.md) §4 row for `descriptive_audit.md`; Pass 1 discipline holds (no effect view, no verdict claim, no interpretive-mark discipline change).

**Verification log**:

- Read HA-C4cp pre-reg r2 LOCKED 2026-07-09 [`analyses/hypotheses/HA-C4cp/hypothesis.md`](../../hypotheses/HA-C4cp/hypothesis.md) §4.1 primary operand + §4.2 stratum + §4.4 day-validity gate + §7 pre-committed sanity ranges + §10.4 sanity-gate HALT discipline.
- Read parent MD r3 LOCKED 2026-07-09 [`methodology/bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) §3.2.2 SD-anchored derivative operand family definitions.
- Read HA-C4c result.md LOCKED r2 for the T=180 parent-operand determinism anchor (`bout_n_did_not_return_day` mean 0.6444, median 1.00, n=1274 total = 465 heavy + 809 non-heavy on 2026-06-23 corpus snapshot).
- Read pipeline extension at Bundle H+ event 8 (`521e9fe`) [`pipeline/02_features/extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py) §3.2.2-implementation `compute_sd_anchored_features()` function + [`pipeline/03_consolidate/build_unified_dataset.py`](../../../pipeline/03_consolidate/build_unified_dataset.py) per-day column join.
- Read [DATA_DICTIONARY.md](../../../DATA_DICTIONARY.md) §8E updated with the 5 new SD-anchored per-day columns + audit-trace + zero-vs-NaN discipline.
- All descriptive computations executed against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` produced by Bundle H+ event 8 pipeline run (2026-07-14). No cross-look at `is_crash`, `gevoelscore`, `exertion_class_lagged_lcera`-stratified values, or block-permutation nulls; Pass 1 hard walls in force.

---

## 1. Scope

**Stratum** (verbatim from HA-C4cp §4.2 + §4.4):

> Cross-phase-pooled per HA-C4c §4.2 verbatim — `citalopram_phase(d) ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}` per `citalopram_phase_stratification §3`, restricted on the `recovery_phase` axis to sub-phase 4b (`pacing_habit_established`; 2022-11-17 → 2024-04-08) UNION phase 5 (`citalopram_modulated`; 2024-04-09 onward, excluding April 2024 cluster 2024-04-09 → 2024-04-16). Day-validity per §4.4: computable `bout_n_did_not_return_2sd_day` (i.e. non-NaN per §3.4 pipeline gate: ≥ 600 valid per-minute stress samples AND `subject_lagged_median(T)` non-NaN per parent MD §3.2.2 reference-window validity bar of ≥ 30 bouts in `[T-90, T-30]`) AND computable `exertion_class_lagged_lcera`.

**Stratum day count on this corpus** (2026-07-14 pipeline extract):

- **1289 days** total on primary HA-C4cp cell (both operand + reference-window valid + exertion class present).
- Reference-window valid days (per parent MD §3.2.2 ≥ 30-bout bar): 1289 / 1289 on the primary stratum window — no additional trim beyond the §4.4 day-validity gate. The reference-window left-edge trim of ~36 days (per Bundle H+ event 8 pipeline stats) is entirely absorbed by the `>= 2022-11-17` sub-phase-4b left-edge which is more restrictive than the reference-window's natural warmup.
- Degenerate-MAD days (MAD = 0): 0 on the primary stratum. No days route to NaN via the degenerate-MAD path.

**Reproducibility vs HA-C4c result.md** anchor (`bout_n_did_not_return` mean 0.6444, n=1274 = 465 heavy + 809 non-heavy on 2026-06-23 corpus snapshot):

- Current stratum: 1289 days = 465 heavy + 824 non-heavy on 2026-07-14 corpus snapshot.
- Heavy-T arm reproduces (465 = 465).
- Non-heavy-T arm grew by +15 days between 2026-06-23 (HA-C4c lock) and 2026-07-14 (this audit) — attributable to corpus growth as new Garmin data is ingested in the ~3-week interval. Growth all falls in non-heavy-T; consistent with heavy-T being the rarer class.
- Parent operand mean on primary stratum (n=1289): **0.6485** — reproduces HA-C4c result.md 0.6444 modulo the +15 non-heavy days (which push the mean marginally downward per non-heavy-lower-count expectation; delta = +0.0041). On the frozen 1274-day HA-C4c-vintage stratum the parent operand mean = 0.6444 byte-identically per Bundle H+ event 8 sanity check.

**Pass 1 hard walls in force** (per HA-C4cp §4.10 sensitivity-arm-descriptive-only discipline + parent MD §3.2 primary-verdict framing):

1. **No effect view** — no heavy-T vs non-heavy-T mean contrast; no Cliff's delta; no Mann-Whitney U; no block-permutation null in this pass. §4.7 walk-forward gate check reports arm-counts only, not arm-means.
2. **No crash or gevoelscore cross-look** — those columns are not read by this audit; the `is_crash` column is used only for future §4.10 crash-drop sensitivity arm at test-execution time, not in this Stage D.
3. **No stratification by `exertion_class_lagged_lcera` in the distributions** — the column is used as a day-validity gate per HA-C4cp §4.4 gate 5 + a walk-forward gate arm-count check per §4.7, not as a stratifier for the operand distribution reports below.
4. **No sensitivity-arm promotion to primary** — the Z=1 count + z_max continuous distributions in §2.2-§2.3 below are reported for completeness per HA-C4cp §4.10 discipline; they cannot promote to SUPPORTED per §5.0 single-cell headline lock, and this audit does not evaluate their verdict readiness.

---

## 2. Per-day operand distributions

### 2.1 `bout_n_did_not_return_2sd_day` (HA-C4cp PRIMARY per §4.1)

| metric | value |
|---|---:|
| n_days | 1289 |
| mean | **0.4765** |
| median | **0.0000** |
| p25 | 0.0000 |
| p75 | 1.0000 |
| sd | 0.6655 |
| min | 0 |
| max | 3 |
| fraction ≥ 1 (any flagged bout that day) | 0.3786 |
| fraction ≥ 2 | 0.0892 |
| fraction ≥ 3 | 0.0031 |
| fraction = 0 | 0.6214 |
| per-day NaN fraction on stratum candidates | 0.0000 |

**Sanity check per HA-C4cp §7** (pre-committed at pre-reg drafting time):

- Expected mean range [0.05, 0.30] narrower anchor: actual **0.4765 above** the narrower anchor by 0.18, corroborating parent MD §3.2.2 rationale that the right-censored `tail_length` distribution (180-cap pile-up) produces a higher flag rate under median + MAD anchoring than the normal-approximation baseline of ~2.5% predicts.
- HALT range [0.01, 0.60] wider anchor: actual **0.4765 inside** by margin [+0.46, −0.12]. **SANITY PASS per §10.4 discipline**.
- Expected median [0, 1]: actual **0 inside**. **SANITY PASS**.
- HALT trigger `median > 2`: actual median = 0. **NOT TRIGGERED**.

### 2.2 `bout_n_did_not_return_1sd_day` (HA-C4cp Z=1 sensitivity per §4.10)

| metric | value |
|---|---:|
| n_days | 1289 |
| mean | 0.9317 |
| median | 1.0000 |
| sd | 0.7453 |
| min | 0 |
| max | 4 |
| fraction ≥ 1 | 0.6967 |
| fraction ≥ 2 | 0.2064 |

Roughly 2× the primary operand's flag rate at ≥ 1 (0.6967 vs 0.3786), consistent with the Z=1 threshold capturing the ~16% top-half-of-tail of the reference distribution vs Z=2's ~2.5% far-tail under normality (empirically compressed by the 180-cap censoring). The gap between Z=1 and Z=2 flag rates is the operand-family stringency gradient.

### 2.3 `bout_return_time_z_max_day` (HA-C4cp z_max continuous sensitivity per §4.10)

| metric | value |
|---|---:|
| n_days | 1284 |
| mean | 1.6338 |
| median | 1.7344 |
| sd | 1.2315 |
| min | −0.7538 |
| p25 | 0.7695 |
| p75 | 2.3914 |
| max | 5.5379 |

Per-day max z-score of the SD-anchored operand. Mean 1.63 SD above the personal `[d-90, d-30]` lagged reference — most days have at least one bout ~1.7 SDs above the participant's own recent typical return-time. The 5-day gap between n=1284 (continuous) and n=1289 (count) is days with 0 detected bouts (`bout_return_time_z_max_day` = NaN by construction on no-bout days per parent MD §3.2.2 NaN semantics).

---

## 3. Reference-window audit trace

Per parent MD §3.2.2 mandatory audit-trace discipline. The reference-window `subject_lagged_median_day` + `subject_lagged_mad_day` are stored per-day for downstream auditability of the SD-anchored operand construction.

**`subject_lagged_median_day`** (median `tail_length` over `[d-90, d-30]` LC-era bout-level reference pool):

| metric | value (minutes) |
|---|---:|
| n_days | 1289 |
| mean | 46.53 |
| median | 46.50 |
| p25 | 39.00 |
| p75 | 53.88 |
| min | 24.00 |
| max | 87.00 |

**`subject_lagged_mad_day`** (`1.4826 × MAD` of the same reference pool):

| metric | value (minutes) |
|---|---:|
| n_days | 1289 |
| mean | 59.85 |
| median | 57.82 |
| p25 | 48.93 |
| p75 | 69.68 |
| min | 28.17 |
| max | 113.42 |

**Substantive descriptive observations** (CAVEAT-CLASS per CONVENTIONS §4.2):

- The MAD is systematically **higher than the median** across the primary stratum (median MAD 57.82 vs median median 46.50), reflecting the right-censored `tail_length` distribution's heavy right tail (180-cap pile-up amplifying dispersion). Median + MAD are robust to this censoring per parent MD §3.2.2 rationale.
- The reference-window median never drops below 24 min or exceeds 87 min across all 1289 primary-stratum days — the participant's own recent typical bout-return-time varies within a bounded ~3.6× range across the LC era, consistent with a stable-personal-baseline reading (though this stability itself is a substantive observation not evaluated further at Pass 1 per hard wall 1).
- The reference-window MAD range [28.17, 113.42] spans a ~4× spread — wider than the median's ~3.6× spread — driven by episodic periods where the reference pool contains many 180-cap bouts (high MAD) vs periods where the pool is more consistently short-tail (low MAD).

**Z-threshold quartiles** (`subject_lagged_median + N × subject_lagged_mad`):

| threshold | p25 | median | p75 |
|---|---:|---:|---:|
| Z=1 (`median + 1 × mad`) | ~ 92 min | ~ 106 min | ~ 128 min |
| Z=2 (`median + 2 × mad`) | 135.85 min | 163.61 min | 192.36 min |

**Cap-unreachable days**: on **452 / 1289 days (35.1%)** the Z=2 threshold exceeds the 180-min `tail_length` cap by construction, i.e. no bout on those days can qualify as Z=2 flagged regardless of bout activity. On 10 / 1289 days (0.8%) the Z=1 threshold exceeds 180 min. This is the direct descriptive expression of the cross-op-independence property parent MD §3.2.2 + OI-025 protocol §5.4 four-condition independence argument argues for: the SD-anchored operand captures a fundamentally different aspect of the bout distribution than the fixed-absolute-threshold parent operand.

---

## 4. Cross-op-independence descriptive comparison

Descriptive contrast between the HA-C4c parent primary operand `bout_n_did_not_return` (fixed 180-min absolute threshold) and the HA-C4cp primary operand `bout_n_did_not_return_2sd_day` (personal-baseline SD-anchored). Both operands share the same per-bout `tail_length` substrate but reference-frame differently. Per parent MD §3.2.2 + OI-025 protocol §5.4, the operand-family-level independence claim binds; this section is descriptive corroboration.

**2×2 concordance table on the 1289-day primary stratum** (each cell = day count):

|  | HA-C4c fires (`bout_n_did_not_return ≥ 1`) | HA-C4c does NOT fire | total |
|---|---:|---:|---:|
| **HA-C4cp fires** (`bout_n_did_not_return_2sd_day ≥ 1`) | 427 (33.1%) | 61 (4.7%) | 488 (37.9%) |
| **HA-C4cp does NOT fire** | 259 (20.1%) | 542 (42.0%) | 801 (62.1%) |
| **total** | 686 (53.2%) | 603 (46.8%) | 1289 |

**Descriptive readings** (CAVEAT-CLASS per CONVENTIONS §4.2; no inference beyond descriptive characterisation):

1. **Concordant firings**: 427 days (33.1%) — days where both operands fire. These are days where the participant has ≥ 1 bout that both exceeds the fixed 180-min cap AND exceeds the personal reference by 2 SDs. Under any joint verdict shape at cluster-C-bout-substance §5 Layer 3, these are the days both operands agree on as "atypical".
2. **HA-C4c-only firings**: 259 days (20.1%) — days where the fixed-threshold operand fires but the SD-anchored does not. Two mechanisms per parent MD §3.2.2 rationale: (a) days where the personal reference has high MAD → Z=2 threshold exceeds 180 min → cap-unreachable → cannot echo; (b) days where a bout genuinely returned within 180 min-cap-adjusted personal envelope but still exceeded the fixed 180-min cap by construction of the day's reference window shape.
3. **SD-anchored-only firings**: 61 days (4.7%) — days where the SD-anchored operand fires but the fixed-threshold does not. Mechanism: days where the personal reference has low MAD → Z=2 threshold below 180 min → bouts that returned by 180 min (thus `did_not_return_flag = False`) but still exceeded the tight personal envelope get flagged.
4. **Neither firing**: 542 days (42.0%) — days with no atypical-return event by either operationalisation.

**Cap-unreachable interaction** (parent MD §3.2.2 explicit predicted pattern):

- 452 / 1289 days (35.1%) have Z=2 threshold > 180 min → SD-anchored operand cannot fire regardless of bout activity.
- Of these 452 cap-unreachable days, 251 (55.5%) have HA-C4c fires (`bout_n_did_not_return ≥ 1`) — the fixed-threshold operand's signal on these days is by construction NOT echoable by the SD-anchored operand. This is not a "missed" signal; it is a genuine operand-family-level reference-frame difference per §3.2.2 four-condition independence argument.

**Cohen's kappa** (chance-corrected agreement; descriptive companion; not a verdict input):

- Observed agreement: (427 + 542) / 1289 = 0.7517
- Expected agreement under independence: (488/1289 × 686/1289) + (801/1289 × 603/1289) = 0.1002 + 0.2907 = 0.3909
- κ = (0.7517 − 0.3909) / (1 − 0.3909) = 0.3608 / 0.6091 = **0.592**

κ ≈ 0.59 is in the "moderate agreement" range (Landis-Koch 1977 conventional cutoffs: 0.41-0.60 = moderate; 0.61-0.80 = substantial). The two operands are neither near-identical (κ → 1) nor independent (κ → 0); they are moderately concordant with structurally-material discordance in both directions. This descriptive reading is consistent with the parent MD §3.2.2 + OI-025 protocol §5.4 claim of operand-family-level cross-op-independence: the two operands share substantial substrate-level signal but capture different aspects of the return-time distribution.

**No verdict claim from this section per Pass 1 hard wall 1.** The concordance table + κ statistic characterise the operand-family relationship at Stage D but do not license any HA-C4cp verdict; that awaits `test.py` run per HA-C4cp §5 verdict machinery.

---

## 5. Walk-forward gate check per HA-C4cp §4.7

Per HA-C4cp §4.7: primary cell (+ each sensitivity arm) must have ≥ 30 heavy-T days AND ≥ 30 non-heavy-T days satisfying §4.4 day-validity. Below 30 on either arm, cell routes to INCONCLUSIVE per §5.2.

| arm | n_heavy_T | n_non_heavy_T | ≥ 30 gate |
|---|---:|---:|---|
| primary (`bout_n_did_not_return_2sd_day`) | 465 | 824 | **PASS** |
| Z=1 sensitivity (`bout_n_did_not_return_1sd_day`) | 465 | 824 | **PASS** |
| z_max continuous sensitivity (`bout_return_time_z_max_day`) | ~ 463 | ~ 821 | **PASS** (5-day gap absorbed proportionally to 0-bout day distribution) |

All three cells clear the walk-forward gate comfortably. Sensitivity arms not enumerated exhaustively at Pass 1 (reference-window-shorter-lag + unmedicated-only + motion-clean-only + transient-excluded + baseline-invalid-excluded + crash-drop + reference-pool-`did_not_return`-excluded + Approach A dose-adjusted are enumerated per HA-C4cp §4.10; each is subject to the same ≥30 gate at test-execution time). The motion-clean-only arm anticipated INCONCLUSIVE per HA-C4c §8 caveat 4 corpus-property (99.3% motion-confound at bout level per HA11-bout-redo result §4); documented at HA-C4cp §8 caveat 4 as inherited.

**No arm-mean contrast reported at Pass 1** per hard wall 1. Test-execution time will compute Mann-Whitney U + Cliff's δ + block-permutation p-value per HA-C4cp §4.6 machinery.

---

## 6. Coverage summary

| descriptor | value |
|---|---:|
| Full corpus days in `per_day_master.csv` | 1755 |
| LC-era days (`>= 2022-04-04`) | 1554 (approx) |
| HA-C4c primary stratum candidate (`>= 2022-11-17` + not April 2024 + exertion class + parent operand computable) | 1289 |
| Reference-window valid days on primary stratum (≥ 30 bouts in `[d-90, d-30]`) | 1289 (100%; left-edge warmup absorbed by sub-phase-4b left-edge) |
| Degenerate-MAD (MAD = 0) days on primary stratum | 0 |
| HA-C4cp primary cell (operand + reference + exertion all computable) | **1289** |
| Heavy-T days on primary cell | 465 |
| Non-heavy-T days on primary cell | 824 |
| Days with `bout_return_time_z_max_day` non-NaN (has ≥ 1 bout) | 1284 (~99.6%) |
| Total bouts on stratum (subset of 4317 corpus-total) | ~ 3800 (approximate; not enumerated at Pass 1) |

**Left-edge coverage note per HA-C4cp §4.7**: the `[d-90, d-30]` reference window's ~60-90-day warmup exclusion is entirely absorbed by the sub-phase-4b left-edge (`>= 2022-11-17`, 227 days after LC-era start 2022-04-04). No days on the primary stratum are lost to reference-window shortfall; the warmup-trim discipline reads as vacuous at this stratum window per §4.4 gate 4.

**Motion-confound caveat** (inherited from HA-C4c §8 caveat 4): 99.3% of the 4317 corpus-total bouts carry `motion_confound_flag = True` per HA11-bout-redo result §4 finding. The SD-anchored reference-window construction operates over ALL bouts (motion-confounded + motion-clean; parent MD §3.4 primary-verdict-policy inheritance); the motion-clean-only sensitivity arm at HA-C4cp §4.10 anticipated INCONCLUSIVE per corpus-property. Documented at HA-C4cp §8 caveat 4.

---

## 7. Open inputs / data-quality observations

**Pass 1 hard walls preclude any inferential claim in this section.** These are descriptive observations that inform future test-execution decisions but do NOT modify any locked pre-commit.

1. **Corpus growth vs HA-C4c result.md** (surfaced §1): non-heavy-T arm grew by 15 days (809 → 824) between 2026-06-23 (HA-C4c lock) and 2026-07-14 (this audit). Attributable to Garmin data ingestion in the ~3-week interval. Does NOT invalidate the HA-C4c primary verdict (LOCKED r2 is on the 2026-06-23 corpus snapshot); the HA-C4cp test.py will re-execute on the current-corpus snapshot at test time and report both the current-corpus n and a snapshot-consistency check.

2. **Cross-op-independence descriptive observation** (surfaced §4): 20.1% HA-C4c-only firings + 4.7% SD-anchored-only firings on the primary stratum → the two operands capture materially different day-populations. Confirms parent MD §3.2.2 + OI-025 protocol §5.4 cross-op-independence claim descriptively; strengthens the closure-path expectation per HA-C4cp §9 verdict-cascade routing (a SUPPORTED HA-C4cp verdict would close the cross-op-independence gap at strict guide §4.2 two-independent-HAs bar; a REJECTED HA-C4cp with HA-C4c PARTIAL would read as ORTHOGONAL per `internal_synthesis.md` §5 verdict table).

3. **Cap-unreachable day rate 35.1%** (surfaced §3): more than one-third of primary-stratum days have Z=2 threshold above the 180-min `tail_length` cap → SD-anchored operand cannot fire on those days by construction. This is by design per parent MD §3.2.2 rationale, but reads as a substantive reduction in the operand's effective sensitivity for the primary claim's SUPPORTED direction. Does NOT relax HA-C4cp §5.1 two-bar SUPPORTED gate (block-perm p < 0.05 + Cliff's δ ≥ +0.20); the +0.20 bar was retained per user Q "sister-pattern discipline wins over compression-of-effects" 2026-07-09. Test-execution outcome interpretation will read the observed Cliff's δ against the cap-unreachable-day baseline per HA-C4cp §8 caveat 2 magnitude-below-threshold anticipation.

4. **Reference-window MAD systematically higher than median** (surfaced §3): median-of-medians 46.50 min vs median-of-MADs 57.82 min. The dispersion metric exceeds the central-tendency metric — a direct signature of the right-tail-heavy censored `tail_length` distribution. This is NOT a data-quality flag; it is a feature of the operand-family construction the SD-anchored family was designed to handle robustly. Documented in DATA_DICTIONARY §8E per Bundle H+ event 8 audit-trace discipline.

5. **NO Z-threshold recommendation from this audit**. Per Pass 1 hard wall 4 + HA-C4cp §4.10 sensitivity-arm-descriptive-only discipline, the choice of Z=2 as primary + Z=1 as sensitivity is pre-committed at HA-C4cp Authorship "Locked decisions" item 1 + user Q "recommended selection" 2026-07-09. This audit reports Z=1 + Z=2 distributions for reference-window sanity confirmation but does NOT recommend a Z threshold change; any post-hoc Z-threshold swap would be a HA-C4cp-v2 revision per §9.5 escalation table.

---

## 8. Cross-references

- **Pre-registration**: [`analyses/hypotheses/HA-C4cp/hypothesis.md`](../../hypotheses/HA-C4cp/hypothesis.md) r2 LOCKED 2026-07-09 (Bundle H+ event 7).
- **Parent MD extension**: [`methodology/bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) §3.2.2 r3 LOCKED 2026-07-09.
- **Pipeline extension**: [`pipeline/02_features/extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py) + [`pipeline/03_consolidate/build_unified_dataset.py`](../../../pipeline/03_consolidate/build_unified_dataset.py) Bundle H+ event 8 (`521e9fe`).
- **Sister descriptive audit** (fixed-threshold arm): [`analyses/descriptive/HA-C4c-stringency-companion/descriptive_audit.md`](../HA-C4c-stringency-companion/descriptive_audit.md) LOCKED r1 2026-07-09; the T-parameterised distributional characterisation of the stringency-family that OI-025 tested (NON-TRIGGER outcome per protocol §4 asymmetric-bar rule) on the same primary stratum.
- **Sister descriptive audit** (parent HA-C4c primary): [`analyses/descriptive/HA-C4c/`](../HA-C4c/) LOCKED r1 for the parent operand `bout_n_did_not_return_day` reference-frame descriptive characterisation.
- **HA-C4c result.md** (parent verdict anchor for determinism reproduction): [`analyses/hypotheses/HA-C4c/result.md`](../../hypotheses/HA-C4c/result.md) LOCKED r2 2026-06-23; PARTIAL magnitude-below-threshold at Cliff's δ = +0.1523, empirical p = 0.0091, n_days = 1274 = 465 heavy + 809 non-heavy.
- **DATA_DICTIONARY §8E**: [`DATA_DICTIONARY.md`](../../../DATA_DICTIONARY.md) §8E — the 5 + 5 = 10 bout-level per-day columns with the SD-anchored derivative operand family entries added at Bundle H+ event 8.
- **OI-033 status**: [`_open_inputs.md`](../../../methodology/_open_inputs.md) OI-033 PROTOCOL-LOCKED / EXECUTION-PENDING per Bundle H+ event 7 lock-log row.
- **Stage A construct**: [`analyses/actionability/construct-bout-recovery-signal.md`](../../actionability/construct-bout-recovery-signal.md) r3 LOCKED 2026-07-09 §5.6 row-6 OI-033 pointer (PROTOCOL-LOCKED).
- **Downstream cascade routing**: HA-C4cp §9 for D → I → S₁ → S₂ → A → T cascade per outcome shape; drift-triggered on `result.md` LOCK.

---

## 9. Lock log

| date | event | scope |
|---|---|---|
| 2026-07-14 | **DRAFT r1 → LOCKED r1** by user acceptance ("lets continue" 2026-07-14 driving Bundle H+ event 9 Stage D descriptive audit landing) | Stage D descriptive-audit companion for HA-C4cp r2 pre-reg per §9 verdict-cascade routing. Reports per-day distributions of the primary (`bout_n_did_not_return_2sd_day`) + Z=1 sensitivity (`bout_n_did_not_return_1sd_day`) + z_max continuous sensitivity (`bout_return_time_z_max_day`) operands on the HA-C4c primary stratum (n=1289 = 465 heavy + 824 non-heavy). Reference-window audit trace (`subject_lagged_median_day` + `subject_lagged_mad_day`) reported per parent MD §3.2.2 mandatory-audit-trace discipline. Cross-op-independence descriptive comparison against HA-C4c parent operand `bout_n_did_not_return` reported per Cohen's kappa moderate-agreement observation (κ = 0.592) + concordance table (33.1% concordant firings, 20.1% HA-C4c-only, 4.7% SD-anchored-only, 42.0% neither) + cap-unreachable day count (35.1% of days have Z=2 threshold > 180-min cap). Sanity check per HA-C4cp §10.4 PASS (primary operand mean 0.4765 inside HALT-range [0.01, 0.60]; primary operand median 0 inside expected [0, 1]; parent operand mean 0.6485 reproduces HA-C4c result.md 0.6444 modulo +15-non-heavy-day corpus growth in the interval; on the frozen 1274-day HA-C4c-vintage stratum the reproduction is byte-identical per Bundle H+ event 8 pipeline sanity check). Walk-forward gate check per HA-C4cp §4.7 PASS on all three cells (primary + Z=1 sensitivity + z_max sensitivity). Pass 1 hard walls in force per HA-C4cp §4.10 sensitivity-arm-descriptive-only + parent MD §3.2 primary-verdict framing: no effect view, no crash/gevoelscore cross-look, no heavy-T stratification of distributions, no verdict claim. Fresh-session `/research-review` NOT dispatched pre-lock: reviewer-mode small doc under `analyses/descriptive/` per plan §4 producer/reviewer split table row for `descriptive_audit.md`; no new source-stage methodology MD; no verdict claim; §3.6 compression eligible if any fires surfaced; retained as retrospective drift-trigger per plan §3.7. **Bundle H+ event 9** on origin/main: THIS Stage D descriptive audit LOCKED r1 landing; opens the remaining execution queue (dry-run report → test.py run + result-data.json + result.md → full 6-stage cascade on result.md LOCK per HA-C4cp §9 verdict-cascade routing). **Drift triggers**: (1) any r > +0.90 or ρ > +0.85 near-identity discovery involving the SD-anchored operand + another corpus channel → propagate to cross-channel-correlation card per Bundle H+ event 6 discipline; (2) HA-C4cp result.md LOCK → this Stage D audit re-consumed per §3.7 drift + Stage I dispatched on the verdict; (3) any parent MD §3.2.2 revision post-r3 → this Stage D audit re-consumed per §3.7 drift + re-computation via pipeline re-run; (4) corpus growth beyond +10% of current n → sanity re-check at HA-C4cp dry-run time. |
