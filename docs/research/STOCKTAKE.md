# Research stocktake — cross-cutting view

*Living cross-cutting index of the Garmin × gevoelscore × notes research. Snapshot dated **2026-06-18**, revived from [`_archive/STOCKTAKE.md`](_archive/STOCKTAKE.md) (last snapshot 2026-06-06, archived 2026-06-13 in the "methodology wave" commit `32d9231` because per-card + per-MD outputs replaced it; revived 2026-06-16 because the cross-cutting view is now needed again — see §3 descriptive layer status).*

**This file is NOT a content store.** Canonical content lives in methodology MDs, hypothesis folders, per-card outputs. This file is the **map + status + synthesis** layer. Update protocol in §8.

---

## 1. The corpus

| dimension | value | source |
|---|---|---|
| Date range | 2021-08-16 → 2026-06-04 (98.8% Garmin coverage) | `per_day_master.csv` |
| Row count | 1755 rows (one per calendar day) | per_day_master |
| Column count | 88 (grouped by source: identity, subjective, manual triage, Garmin daily/HR/exertion/sleep-stress/spikes, notes categorisation, timeline events, PwC log + dossier, coverage flags) | [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) |
| Day_entries | 1372 with score (2022-09-03 → 2026-06-04, 100% on 1-6 scale) | Directus |
| Notes | 686 day_entries have written notes (50% coverage; uneven by year, peak 71% in 2024) | Directus |
| Crashes (`crash_v2` tier-1) | **29 episodes**, 101 crash-days | [`crash_v2-definition/`](analyses/hypotheses/crash_v2-definition/) |
| Dips (`crash_v2` tier-2) | **79 isolated single-day dips**; dip:crash ratio 1.9× train → 3.5× validate | `labels_crash_v2.csv` |
| Stratum 4 (LC + gevoelscore + crash labels) | 2022-09-03 → as-of-date; **primary analytic surface** | [`methodology/lc_era_temporal_segmentation.md`](methodology/lc_era_temporal_segmentation.md) |
| Citalopram-CONFIRMED-modulated channels | 3: `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest` (v3 2026-06-14) | [`methodology/citalopram_dose_response_stress_mean_sleep.md`](methodology/citalopram_dose_response_stress_mean_sleep.md) §5.6 |

---

## 2. Hypothesis pipeline status

### 2a. Register-only (operationalisation pending)

**Personal register** ([`personal_hypotheses.md`](personal_hypotheses.md)) — P1-P7. Status as of 2026-06-16:

| ID | claim | status |
|---|---|---|
| P1 | sleep-stress elevated on crashes | descriptively confirmed (d=+0.90 episode-level); no formal HA pre-reg by Personal-register discipline |
| P2 | exertion-axis signals in 4d pre-crash window | weakly supported via HA01b/HA01c; awaits Q10 single-pool recompute |
| P3 | within-day RHR recovery | **routed → Wiggers A4** (2026-06-14) |
| P4a, P4b | end-of-day BB floor / late-afternoon drain | **blocked** on per-minute BB primitive (H04b path C) |
| P5a | post-exertion rest-stress with motion filter | **routed → Wiggers C4b** (HA-C4b v3 NOT-SUPPORTED 2026-06-17, see §2d) |
| P5b | prevailing rest-stress with evening amplification | **blocked** on stress-with-motion-by-time-of-day primitive |
| P6 | post-crash recovery shape | **HA-P6 LOCKED, awaits run** (§2c) |
| P7 | recent-crash-density predicts crash | **HA-P7 NOT-SUPPORTED** (§2d) |

**Wiggers register** ([`wiggers_testable_hypotheses.md`](wiggers_testable_hypotheses.md)) — A-F sections per Wiggers PDF.

- **Tier 1**: **C3** (non-linear stress → fatigue) — no HA-folder yet, drafting pending. **C4** (3-channel stress decay triad) — **HA-C4 v1 drafted + r2 LOCKED 2026-06-17** (`da79387`); **dry-run halted 2026-06-17** (`19d33e4`) on Ch3 validate heavy n=25 < 30 sanity bar; v2 reframe in flight per [`session-c4-v2-reframe-handoff-2026-06-17.md`](file:///C:/Users/Gebruiker/.claude/plans/session-c4-v2-reframe-handoff-2026-06-17.md). Source-verified, columns ready.
- **Tier 2** (HA pre-reg pending, with stop-rules): **A1**, **A4**, **B1**, **H5**.
- **Tier 3** (descriptive prereq before pre-reg): **G3** (parked Q18), **H1** (HRV blocked on FR245), **H4** (needs reframing post HA10 ≡ −HA07c collapse).
- **Out-of-priority pool**: A2, A3, B2-B5, C1, C2, D1-D5, E1-E3, F1, F2, F4, G1, G4, H2, H3.

### 2b. Drafted but not yet locked

- **[HA-C4 v2](analyses/hypotheses/HA-C4/hypothesis.md)** — drafted 2026-06-18 (`59fae4b` + `73cb2d4`) per composite-path recommendation (Option A explicit-INCONCLUSIVE handling in §5.3 + §7.3 arithmetic rebuild + new §4.11.3 chain-T+1-relaxed sensitivity arm; Option B/D/E-second-half rejected). v1 archived (`hypothesis-v1-archived.md` + `test-v1-archived.py` + `dry-run-report-v1-archived.md`). **Next step in lock arc**: fresh-session `/research-review` audit per [`hypothesis_lock_process.md §3.4`](methodology/hypothesis_lock_process.md#34-audit-step-stage-2-of-the-arc).

### 2c. Historical lineage — locked + halted at dry-run (v1, archived; superseded by v2)

- **HA-C4 v1** — drafted (`b76b1e0`) + r2 LOCKED 2026-06-17 (`da79387`); dry-run HALTED 2026-06-17 (`19d33e4`) on Ch3 validate heavy n=25 < 30 sanity bar (the §5.4 inconclusive bar). §4.7 chain-T+1 exclusion dropped 16 of 41 validate heavy-T days → 25 remain. Triage analysis (fresh-session 2026-06-18) identified 5 v2 options + recommended composite path; superseded by v2 (see §2b). v1 stays archived for audit-trail continuity per the locked-pre-reg discipline.

### 2d. Tested with result

**Overall SUPPORTED under canonical both-eras bar (only one):**
- **[HA07d](analyses/hypotheses/HA07d-sleep-stress-variability/result.md)** — variability of sleep-stress, train +19.6 pp / validate +21.7 pp, RESCUE confirmed in v2 diagnostic. *First project test to clear both eras at primary.*

**Train-only SUPPORTED → overall NULL, RESCUED via diagnostic-v2 as load-bearing-train-only (4):** HA06b (RHR z-score), HA07c (sleep-stress mean delta), HA08c (sleep-stress slope), HA11 (stress u-dip).

**Validate-only SUPPORTED with directionality reversal (1):**
- **HA10** (BB overnight recharge) — train −20.5 pp / validate **+16.2 pp**. v2 diagnostic restored validate-era SUPPORTED.

**Diagnostic ambiguity → load-bearing WITHHELD:** HA01b (effective-exertion composite), HA01c (effective-exertion shock).

**NOT-SUPPORTED:**
- **[HA-P7](analyses/hypotheses/HA-P7/result.md)** — recent-crash-density. Pooled LC × W=14: OR 1.130 [0.875, 1.266], p=0.17. All 3 §5.1 criteria fail. **§4.5.4 covariate sensitivity diagnostic**: β_crash_count_14d attenuates to 0.941 when `gevoelscore_lagged_mean_14d` added → marginal signal reads as **recent-low-gevoelscore proxy**, NOT independent recovery-debt mechanism. Verdict robust across E[L] ∈ {7, 12, 14}.
- **[HA-C4b v3](analyses/hypotheses/HA-C4b/result.md)** — stress-with-low-motion minute count as crash precursor (unmedicated pooled headline). Pooled n=10 (8 train + 2 validate, with 2023-02-04 restored after v3's §4.3 1b.ii drop): (a) 40% **FAIL** (≥60%), (b) -10pp **FAIL** (≥+15pp; obs 40% vs null median 50%), (c) +1.21 PASS. RD -0.100; OR 0.67; p=0.6250 (one-sided, E[L]=7). Train-only (a)=50% (4/8); validate-only (a)=0% (0/2). LOO: k=4 BELOW BOUNDARY (k≤5); 0 load-bearing episodes (boundary-distance signal per §4.11.5). E[L]\*=3.34 (factor-of-2 flag but descriptive-only since verdict is NOT-SUPPORTED). v3 dropped §4.3 1b.ii and symmetrised the §10.2 dry-run / full-run gate; the 1b.ii drop is honestly framed as a deliberate override of a real 2023-02-04 catch (audit Layer 2.5 substantive concern named in §8). Per v3 §9 NOT-SUPPORTED branch: two alternative readings stay open — (i) the lived rest-stress trigger may be **PROTECTIVE rather than PREDICTIVE** (participant acts on it and prevents crashes); (ii) §4.2-admitted crashes may be disproportionately **emotionally / cognitively triggered with incidental physical exertion** in the lead-up (v3 §8 pacing-behaviour confounder). v2 lineage: v1 dry-run halted 2026-06-15; v2 INCONCLUSIVE 2026-06-16 (dropped 2023-02-04 under 1b.ii → n=9 < §5.3 bar; spec-design asymmetry, not data finding); v3 closed the asymmetry → NOT-SUPPORTED on the same byte-identical headline cell.

**Descriptive characterisation (Layer 1 per CONVENTIONS §2.1 — no SUPPORTED/NOT-SUPPORTED bar; findings-shape verdict):**
- **[HA-P6 v3](analyses/hypotheses/HA-P6/result.md)** — post-crash 7-channel recovery shape with Option C dual matched-baseline. Test-executed 2026-06-17 (`a980b1c`). **§9 first-branch fires** — 4/7 channels distinguishable from Arm-A matched control (matched deep-trough non-crash days): `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`, `stress_low_motion_min_count_S60_Mlow`. **§9 second branch does NOT fire** (36% of cells "Arm-A match", below implicit-majority 50% threshold for "RTM dominates"). Lineage: v1 (locked 2026-06-15) → v2 (`ef4f105`) → v3 (`97b74df`) → test (`a980b1c`) → reader's notes addendum (`bbcb478`). **Fresh-session result review 2026-06-18 verdict PASS** (the strongest in the project for autocorrelation discipline per [`reviews/HA-P6-2026-06-18-v3-result.md`](reviews/HA-P6-2026-06-18-v3-result.md); 5 minor recommendations, none blocking, NO v4 trigger). **4 §9 downstream propagations already landed**: `9103163` (register row update at `personal_hypotheses.md`), `94a4bb3` ([`crash_episode_descriptive.md §8`](methodology/crash_episode_descriptive.md) per-channel timing), `eb42888` ([`time_resolution.md §2.3`](methodology/time_resolution.md)), `a1395e1` (HA-P7 cross-test interpretive overlay on [`HA-P7/result.md`](analyses/hypotheses/HA-P7/result.md)). **Substantive recovery-shape signal exists**; informs HA-P7 NOT-SUPPORTED reinterpretation — see §6.

**Historical rejections** ([`REJECTED.md`](REJECTED.md)) — ~25 entries (H01-K02 + HA01-HA05 3d-variants + HA01b-recomputed lagged-baseline correction + intervention work INT-NARROW + RESP-SSRI + HA-P7).

---

## 3. Descriptive research programme — gap closing

**Status as of 2026-06-18**: descriptive research programme is **bootstrapped + first analysis landed**. The 2026-06-16 "no `analyses/descriptive/` folder" gap is closing:

- [`analyses/descriptive/README.md`](analyses/descriptive/README.md) — programme scoping doc **LOCKED 2026-06-18 r3** (commit `ccbd12e` under §3.6 compression). Two-strand framing: Strand A operationalisation-support + Strand B multi-year-trajectory (three-phase: pre-illness healthy → infection/acute → LC trajectory). 16+ research questions enumerated; Phase 1 first 3 analyses scoped.
- [`analyses/descriptive/operationalisation_support/stress_mean_sleep/`](analyses/descriptive/operationalisation_support/stress_mean_sleep/) — **first Strand A analysis LANDED 2026-06-18** (commit `84b9801`); answers Q3.1.a-i for the most-cited CONFIRMED-citalopram channel. Outputs: `README.md` + `findings.md` + `run.py` + `summary.json` + `plots/`. Interpretation pass pending.

### 3.1 Existing descriptive work (still scattered, but now indexed from programme README §5)

| location | content |
|---|---|
| [`_archive/S01-stabilisation-trajectories/`](analyses/hypotheses/_archive/S01-stabilisation-trajectories/) + [`_archive/S02-score-trajectory/`](analyses/hypotheses/_archive/S02-score-trajectory/) | 90d rolling autonomic + gevoelscore distribution shift; archived 2026-06-13 as descriptive-only; will be consolidated into `trajectory/recovery_arc/` (Phase 1 second analysis) |
| [`garmin_exploration/cards/`](analyses/garmin_exploration/cards/) | `cross-channel-correlation.md`, `card-b-train-specificity.md`, `card-b2-validate-specificity.md`, `primary-verdict-statistics.md`. **Decisive Tier 2 audits.** Indexed from descriptive/README §5 |
| [`garmin_exploration/hrv_proxy_validation/`](analyses/garmin_exploration/hrv_proxy_validation/) + [`stress_low_motion_viz/`](analyses/garmin_exploration/stress_low_motion_viz/) + [`activity-labels/`](analyses/garmin_exploration/activity-labels/) + [FIT taxonomy](analyses/garmin_exploration/README.md) | Primitive validation + viz runs; indexed |
| [`methodology/crash_episode_descriptive.md`](methodology/crash_episode_descriptive.md), [`methodology/crash_episode_prolonged.md`](methodology/crash_episode_prolonged.md), [`methodology/lc_era_temporal_segmentation.md`](methodology/lc_era_temporal_segmentation.md), [`methodology/lc_phase_descriptive.md`](methodology/lc_phase_descriptive.md), [`methodology/symptom_mention_asymmetry.md`](methodology/symptom_mention_asymmetry.md), [`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md) | Cohort topology + label semantics + Q3.x.a/h delegate targets |

### 3.2 Programme-status snapshot

| analysis | strand | status |
|---|---|---|
| [`operationalisation_support/stress_mean_sleep/`](analyses/descriptive/operationalisation_support/stress_mean_sleep/) | A | **LANDED 2026-06-18** (`84b9801`); answers Q3.1.a-i; interpretation pass pending |
| `trajectory/recovery_arc/` | B | pending — requires user operationalisation interview per descriptive/README §7b (4 choice points: COVID infection-date / acute-phase endpoint / channel set per phase / event overlays) |
| `operationalisation_support/stress_low_motion_min_count_S60_Mlow/` | A | pending — Strand A template-driven; handoff can be drafted on the same pattern as stress_mean_sleep |

### 3.3 Key audit findings from the existing scattered work (carry forward)

1. **Cross-channel correlation collapses the "6-channel convergence" reading.** H02b ≡ H02d at ρ=+1.000; HA10 ≡ −HA07c at ρ=−0.922. Load-bearing list is ~3-4 independent clusters, not 9.
2. **All 9 load-bearing anchors land in Tier C** (lift <2×, precision <5%) per specificity tables — retrospective-only surfaces, not prospective predictors.
3. **Only H02d clears honest effective-N Bonferroni** (α=0.0125).

**Programme companion plan**: see [`C:/Users/Gebruiker/.claude/plans/structured-descriptive-analysis-2026-06-16.md`](file:///C:/Users/Gebruiker/.claude/plans/structured-descriptive-analysis-2026-06-16.md) (v2 framing: research programme, not card-per-group documentation layer). Phased build-out: infrastructure (DONE) → index existing work (DONE) → first 2-3 analyses (1 of 3 landed; 2 pending) → lock-process integration (Phase 4; awaits ≥3 analyses).

---

## 4. Intervention findings — citalopram arc

The arc as of 2026-06-16 (canonical in [`methodology/intervention_effects_descriptive.md`](methodology/intervention_effects_descriptive.md) + [`methodology/citalopram_dose_response_stress_mean_sleep.md`](methodology/citalopram_dose_response_stress_mean_sleep.md) + [`methodology/citalopram_phase_stratification.md`](methodology/citalopram_phase_stratification.md)):

1. **Session C single-channel finding (2026-06-14)**: `stress_mean_sleep` × 2026-03-20 boundary, median diff −3.06, survives detrend at B={7,14,28}, marginal at B=42. Plausible direct SSRI-withdrawal effect. Only 2 of ~25 detrend-surviving channel-boundary pairs.

2. **INT-NARROW SUPERSEDED** (REJECTED.md, 2026-06-14): the pre-v3 narrow reading was widened by:

3. **v3 multi-channel confirmation (2026-06-14)** via `multi_channel_check.py`, 6 channels × three-pronged test (afbouw 2026 + buildup 2024 post-CPAP-buffer + spring 2025 control):
   - **CONFIRMED**: `stress_mean_sleep` (+0.43/mg, p=0.001), `all_day_stress_avg` (+0.57/mg, p=0.000), `bb_lowest` (−1.13/mg, p=0.000)
   - **REJECTED**: `respiration_avg_sleep` (β=−0.002, p=0.57) → **RESP-SSRI DESCRIPTIVE-FAIL** in REJECTED.md
   - Buildup S2 carries the case; afbouw alone marginal; spring 2025 control flat → seasonality alibi unsupported.

4. **`citalopram_phase_stratification.md` v2 (2026-06-14)**: operationalises four-phase axis (unmedicated / buildup / consolidation / afbouw / post_afbouw) with §5.A per-phase stratification + §5.B dose-adjusted predictor (recommended) + §5.C joint model. **§6 pre-registration template binds any new hypothesis MD touching a CONFIRMED channel.**

**Structural consequence**: every test crossing the 2024-04-09 or 2026-03-20 phase boundary on the 3 CONFIRMED channels now inherits a quantified-confound + §5.B treatment obligation. The "rolling lagged baseline absorbs everything" assumption is **empirically dead** on these channels.

---

## 5. Methodology lockings — structural map

~15 MDs at [`methodology/`](methodology/), grouped by what they lock:

| group | MDs |
|---|---|
| **Discipline + workflow** | `methodology.md`, `hypothesis_lock_process.md` (v1.1 — canonical 4-stage arc), `train_validate_split_fate.md` (single-pool primary) |
| **Statistical conventions** | `permutation_null_block_length.md` (E[L]=7 stationary bootstrap + block-permutation null project-wide), `time_resolution.md` |
| **Data semantics** | `nightly_attribution.md` (wake-up-date), `symptom_mention_asymmetry.md` (presence-conditioned vs daily-computed), `symptom_categorization_v24.md`, `garmin_indicators_audit.md` |
| **Cohort surfaces** | `lc_era_temporal_segmentation.md` (Stratum 4 = primary), `crash_episode_descriptive.md`, `crash_episode_prolonged.md` |
| **Proxies** | `hrv_proxy_via_stress.md` (sleep-window stress as HRV proxy), `bb_overnight_gain_proxy.md` (r=0.989 vs truth post-2024-09-18; sensitivity-only for 2024-07-08→2024-09-17 bridge), `stress_low_motion_primitive.md` (Session E lock) |
| **Operational** | `garmin_pacing_practice.md` (§7.4 intervention-period baseline-calibration now resolved) |
| **Intervention arc** | `intervention_effects_descriptive.md`, `citalopram_dose_response_stress_mean_sleep.md`, `citalopram_phase_stratification.md` (see §4) |
| **Queue** | `queued_work.md`, `_pending_literature_fetch.md` |

---

## 6. Cross-section synthesis

**The pattern across SUPPORTED-load-bearing tests** (HA07d + HA10's validate-side + HA11's train-side after diagnostic RESCUE) is more about **second-order autonomic flexibility — variability and reversal patterns** than about absolute level. All three had prior Wiggers + lived-experience motivation, so the SUPPORTED reads are **confirmatory per CONVENTIONS §4.1**, not originating from data peeking.

**Two calibration lessons now canonicalised:**
1. **HA01b-recomputed correction** → §3.1 personal-baseline must use **lagged**, not rolling-window-inclusive-of-day. Original v3.1 inflated +13.3 pp on the validate era; v3.2 lagged-baseline correction flipped verdict to REFUTED.
2. **HA-C4b v1 halt** → §7 anchor ranges must bind to **the exact column's descriptive card**, not a definitional cousin's distribution. Now §5 sanity-check row in [`hypothesis_lock_process.md`](methodology/hypothesis_lock_process.md).

**HA-P7's NOT-SUPPORTED is informative falsification.** The recovery-debt mechanism on a 14d window does not survive the §4.5.4 covariate-sensitivity check; what looked like crash-density predicting next-crash collapses to "recent-low-gevoelscore predicts next-low-gevoelscore", which is autocorrelation not mechanism.

**HA-P6 has now landed (4/7 channels distinguishable, 2026-06-17; fresh-session result review verdict PASS 2026-06-18) and answers the deferred HA-P7 question**: yes, a real measurable post-crash recovery signature exists on 4 of 7 channels. HA-P7's null was therefore NOT "no recovery mechanism exists" but rather "the 14d-crash-density count is too coarse an operationalisation to capture what the recovery trajectories actually do". The combined HA-P6 + HA-P7 + HA-C4b v3 reading: post-crash recovery has a real measurable shape (HA-P6 confirms), AND prospective precursor signals from PEM-pacing channels don't predict crashes in this corpus (HA-C4b v3 NOT-SUPPORTED + HA-P7 NOT-SUPPORTED). The body's recovery dynamics carry signal; the simple "more recent bad days → more upcoming bad days" mechanism does not. HA-C4b v3's PROTECTIVE-not-PREDICTIVE alternative reading (§9) is a third strand in this synthesis worth disambiguating in a fresh interpretation pass.

**Reader's Notes Note 2 nuance (2026-06-17 addendum, validated PASS by 2026-06-18 review)**: the §9 bullet 8 signal on `all_day_stress_avg` completeness↔next-interval (CI excludes 0: ρ=−0.338 [−0.493, −0.168], n=18) is in the **inverse direction** from naive recovery-debt expectations (naive: more complete recovery → longer next-interval; observed: more complete recovery → SHORTER next-interval). Three candidate mechanism readings stay open (exuberance / push-through; tight feedback loop; measurement artefact); the data alone does not pick between them. The §9 bullet 8 propagation should NOT be read as supporting recovery-debt mechanism for this channel. Combined with the empirical "almost-everywhere-fails-detrend" pattern on §3.7 (25/28 per-phase cells categorically shift under detrend — more pervasive than the spec's consolidation-only-failure anticipation): the LC recovery trajectory leaks through nearly all cells; the load-bearing finding is Arm-A's paired-diff §9 first-branch trigger, which is detrend-independent by construction (matched-control on same-phase non-crash day with similar pre-trajectory).

**Citalopram-as-confound for HA07c (caveat-class, not confirmatory):** HA07c's train SUPPORTED +23.2pp / validate REFUTED −6.0pp divergence straddles the 2024-04-09 buildup boundary. The v3 dose-response confirmation is now a non-rejected confound-class candidate for the divergence on this channel, **alongside** (not replacing) the era-as-moderator narrative. Forward citations of HA07c's "train SUPPORTED" sub-finding require explicit acknowledgement that the channel is dose-modulated.

**What's still open:**
- Exertion → crash family (P2 / HA01b / HA01c) awaits Q10 single-pool recompute.
- BB-floor + rest-stress P5b family (P4 / P5b) await per-minute primitive. HA-C4b v3 closed NOT-SUPPORTED 2026-06-17 (see §2d); the v3 §8 pacing-behaviour confounder on emotional / cognitive triggers is queued as a future primitive (methodology MD documenting construct validity + sparsity + how to read the `cat_belasting_emotioneel` / `cat_belasting_cognitief` / `state_symptoom_*` proxies; sparsity caveats per DATA_DICTIONARY §9).
- HA-P6's recovery-shape run is the load-bearing input to whether HA-P7's 14d window has any anchoring.
- Wiggers Tier 1 (C3, C4) have no HA-folder yet — natural next pre-regs per the Wiggers Tier 1 execution plan.

---

## 7. Open follow-ups + actionable next steps

### Actionable now (low activation energy)
1. **HA-C4 v2 fresh-session audit** — v2 drafted today (`59fae4b` + `73cb2d4`); next step in lock arc is `/research-review` on the v2 hypothesis.md per `hypothesis_lock_process.md §3.4` (fresh-session, doc-only knowledge). Audit report lands at `reviews/HA-C4-v2-2026-06-18.md`.
2. **stress_mean_sleep findings interpretation pass** — first Strand A analysis landed today (`84b9801`); needs a read + cross-test re-interpretation check (HA07c train/validate divergence in light of phase-stratified distribution is the obvious trigger). Could land as a small `reviews/` doc or fold into the larger cross-test pass.
3. **HA-C3 pre-reg drafting** — Tier 1 Wiggers, sister to HA-C4. No HA-folder yet. Use full v1.1 canonical 4-stage arc per `hypothesis_lock_process.md`. Bucket C.5 of the Wiggers Tier 1 plan.
4. **Phase 1 third analysis dispatch** — `operationalisation_support/stress_low_motion_min_count_S60_Mlow/` (Strand A template-driven; same pattern as stress_mean_sleep handoff).

### Actionable after user interview
5. **Phase 1 second analysis** `trajectory/recovery_arc/` — Strand B; requires user operationalisation interview per descriptive/README §7b (4 choice points: COVID infection-date / acute-phase endpoint / channel set per phase / event overlays). Interview happens here in main session; handoff drafted after lock.

### Actionable after HA-C4 v2 lock + test
6. **HA-C4 v2 lock** — after audit + r2 + (re-audit OR §3.6 compression) signals.
7. **HA-C4 v2 test execution** — separate post-lock session per §3.9.
8. **HA-C4 v2 result reading** — after test lands.

### Deferred per user — "full set of new sessions when we interpret the results of multiple hypotheses, in isolation and also in context of each other"
9. **Cross-test interpretation pass** — synthesis across HA-P6 (4/7 channels recovery-shape signal) + HA-C4b v3 (NOT-SUPPORTED, PROTECTIVE-not-PREDICTIVE reading) + HA-P7 (recent-low-gevoelscore proxy collapse) + stress_mean_sleep findings + HA-C4 v2 result when it lands.
10. **HA-C4b v3 §9 alternative-readings disambiguation** — folds into (9): (i) PROTECTIVE-rather-than-PREDICTIVE (testable on `crash_episode_descriptive.md` per-episode depth + duration); (ii) emotional / cognitive trigger confounder (queued primitive — see §6 "What's still open"). v3 result feeds [`methodology/garmin_pacing_practice.md`](methodology/garmin_pacing_practice.md) — operational rest-stress trigger remains useful as within-day pacing signal regardless of v3's precursor-aggregate verdict.

### Polish (non-blocking)
- **HA-P6 v3 result.md compressible recommendations** — 3 polish items per the [2026-06-18 review report](reviews/HA-P6-2026-06-18-v3-result.md) §4: complete §9 evaluation surface (4 missing bullets); add §4.8.4 spec-lock-identifier parenthetical; synthesise "almost-everywhere-fails-detrend" pattern. Non-blocking; can land any time.

### Open follow-ups in `hypothesis_lock_process.md` §8.3
- Audit-MD compression-record gap (binds prospectively only; existing HA-C4b/HA-P7 lock commits stand).
- `/research-audit HA-<id> [--second-pass]` slash-command ergonomic improvement (deferred).

### Open structural work
- **Descriptive research programme build-out** — see [`C:/Users/Gebruiker/.claude/plans/structured-descriptive-analysis-2026-06-16.md`](file:///C:/Users/Gebruiker/.claude/plans/structured-descriptive-analysis-2026-06-16.md) (v2 research-programme framing).
- **STOCKTAKE refresh discipline** — see §8.

---

## 8. Update protocol

This file is a **living cross-cutting view**, refreshed on these triggers:

| trigger | what to refresh |
|---|---|
| New HA-* result.md lands | §2d table row + §6 synthesis if cross-test pattern shifts |
| New HA-* pre-reg locked | §2c (locked-awaiting-run); §2a if it supersedes a register entry |
| New methodology MD locked OR existing MD revised (binding) | §5 structural map + §6 implications |
| Intervention arc revision (new dose-response / new channel CONFIRMED / new REJECTED) | §4 entirety + §6 citalopram-as-confound paragraph |
| Cross-channel correlation re-run shifts the independence story | §3 audit findings + §6 second-order autonomic flexibility synthesis |
| Quarterly snapshot | full refresh with date update in preamble |

**Refresh process** (per the v1.1 §3.2 reviewer-mode-with-authorization pattern, since STOCKTAKE is reviewer-mode per CONVENTIONS §1.2):

1. User explicitly requests refresh (or one of the triggers above clearly fires).
2. Read this file end-to-end + the canonical artefacts that have changed since last snapshot date.
3. Edit in-place; update preamble snapshot-date + add a one-line entry to the revision log below.
4. Lock with commit message naming the trigger.

### Revision log

- **2026-06-18 (third wave)** — HA-C4 v2 drafted (`59fae4b` + `73cb2d4`) per composite-path recommendation; v1 archived. stress_mean_sleep first Strand A descriptive analysis LANDED (`84b9801`); answers Q3.1.a-i; first analysis under the locked descriptive research programme. Descriptive programme README locked at `ccbd12e` earlier today + r3 closures + first analysis = programme bootstrapped. §1 corpus snapshot date bumped to 2026-06-18. §2b "drafted but not yet locked" no longer "None" (HA-C4 v2). §2c restructured to "Historical lineage" (HA-C4 v1 archived, superseded by v2). §3 restructured: "the structural gap" → "gap closing"; descriptive programme programme-status snapshot table added; first analysis landed; existing-work indexed via descriptive/README §5. §7 actionable steps re-numbered: HA-C4 v2 audit + stress_mean_sleep interpretation + HA-C3 drafting + Phase 1 third analysis at top of queue; cross-test interpretation explicitly deferred per user "for later when we are going to do a full set of new sessions". Trigger: "New HA-* pre-reg locked" + "New HA-* result.md lands" + "New descriptive analysis lands" per §8.
- **2026-06-18** — HA-P6 v3 fresh-session result review (`reviews/HA-P6-2026-06-18-v3-result.md`) verdict **PASS** (strongest in the project for autocorrelation discipline; 5 minor recommendations + 0 substantive; NO v4 trigger). 4 §9 downstream propagation commits identified: `9103163` (register row), `94a4bb3` (`crash_episode_descriptive.md §8` per-channel timing), `eb42888` (`time_resolution.md §2.3`), `a1395e1` (HA-P7 cross-test note); reader's notes addendum (`bbcb478`) absorbed. §2d HA-P6 v3 entry extended with the 4 distinguishable channels named + review verdict + 4 propagation commits + reader's notes addendum. §6 synthesis extended with Reader's Notes Note 2 nuance: `all_day_stress_avg` completeness↔next-interval signal (CI excludes 0) is INVERSE direction from naive recovery-debt (3 candidate mechanism readings stay open; data alone cannot pick); plus the empirical "almost-everywhere-fails-detrend" pattern (25/28 §3.7 cells shift under detrend, more pervasive than spec §9 bullet 3 anticipation; load-bearing finding is detrend-independent Arm-A trigger by construction). Trigger: "New HA-* result.md lands" per §8.
- **2026-06-17 (continued)** — HA-P6 v3 test-executed (`a980b1c`); §9 first-branch fires (4/7 channels distinguishable from Arm-A matched control). Lineage today: v1 (locked 2026-06-15) → v2 (`ef4f105`) → v3 (`97b74df`) → test (`a980b1c`). HA-C4 v1 drafted + r2 LOCKED (`da79387`) + dry-run HALTED (`19d33e4`) on Ch3 validate heavy n=25 < 30 bar; v2 reframe in flight per `session-c4-v2-reframe-handoff-2026-06-17.md`. §2a Wiggers Tier 1 C4 entry updated (no longer "no HA-folder yet"); §2c label changed from "Locked, awaiting test run" to "Locked, halted at dry-run (v2 redraft required)" — HA-P6 moved out to §2d (new descriptive-characterisation sub-bucket); HA-C4 v1 added to §2c; §6 HA-P7 paragraph extended with HA-P6 + HA-C4b v3 triangulation ("body's recovery dynamics carry signal; simple recent-bad-days→next-bad-days mechanism does not"); §7 restructured (HA-P6 test removed from "actionable now"; descriptive-programme lock + HA-C3 drafting now top of queue; HA-C4 v2 result reading + cross-test interpretation pass added). Trigger: "New HA-* result.md lands" + "New HA-* pre-reg locked" per §8.
- **2026-06-17** — HA-C4b v3 LOCKED + test-executed NOT-SUPPORTED (commits `32ba3b9` + `df05e83`). v3 dropped §4.3 1b.ii and symmetrised the §10.2 dry-run / full-run gate (closing v2's INCONCLUSIVE-by-spec-design-asymmetry); restored 2023-02-04 to the pooled cell; (a) 40% FAIL, (b) -10pp FAIL, (c) +1.21 PASS. §2c HA-C4b v2 entry removed (no longer awaiting); §2d NOT-SUPPORTED entry added; §6 "What's still open" updated; §7 actionable-now/after re-numbered with v3 downstream synthesis as the new HA-C4b follow-up. Trigger: "New HA-* result.md lands" per §8.
- **2026-06-16** — Revived from `_archive/STOCKTAKE.md` (archived 2026-06-13). New cross-cutting view structured around 5 buckets (corpus / pipeline / descriptive-gap / intervention / methodology) + synthesis. Captures: HA-C4b v2 locked + tested 2026-06-16; HA-P7 NOT-SUPPORTED; HA07d as only canonical-SUPPORTED; v3 citalopram multi-channel CONFIRMED 3 channels + REJECTED respiration; cross-channel collapse to 3-4 clusters; descriptive-layer structural gap surfaced. First worked example of the lock-process MD §3.8 register-row pointer discipline applied retroactively (the archived STOCKTAKE entry remains for audit trail).
- *2026-06-06 (archived)* — last snapshot before archiving; covered crash_v2 phase consolidation + activity-labels v3.1 lock + dip-cluster overlay. See `_archive/STOCKTAKE.md`.
