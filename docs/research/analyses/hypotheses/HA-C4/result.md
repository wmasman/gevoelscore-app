# HA-C4 v2 — RESULT: REJECTED (triad sum = 0.0 / 3.0)

Emitted by `test.py` per locked v2 hypothesis.md §10.3. **Headline cell**: unmedicated × {Ch1, Ch2, Ch3} × heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's δ × block-permutation null E[L]=7 × v2 §5.3 INCONCLUSIVE-aware triad verdict bands. **Random seed**: `RANDOM_SEED = 20260618`; **B** = 10000 bootstrap draws per cell. **Strength**: no triad signal.

## v2-specific caveats (prominent per §10.3 + §8)

1. **v1 → v2 transition disclosure**: v1 (LOCKED 2026-06-17 r2 commit `da79387`) was dry-run-halted on Ch3 validate n=25 < 30 (per §4.7 chain-T+1 exclusion dropping 16 of 41 validate heavy-T days); v1 §5.3 had no explicit INCONCLUSIVE-handling rule so the cell broke the binary triad logic. **v2 §5.3 introduces explicit handling**: INCONCLUSIVE cells contribute 0.5 (CONFIRMED-PARTIAL) at the per-channel aggregation layer when the OTHER era is SUPPORTED, blocking full credit but not refuting. The Wiggers 3-channel triad structure is preserved; Ch3 is NOT dropped from the triad. The v1 halt was the locked-pre-reg discipline working exactly as designed; v2 is the corrective draft.

2. **§7.3 arithmetic spec-bug fix (honest disclosure)**: v1 §7.3 implicitly assumed the 35-day pre-train buffer (Apr–Aug 2022 unmedicated heavy-T days) was already excluded from the heavy-T count; it asserted train heavy-T n = 206 when the correct value is n = 171. v2 §7.3 corrects this AND adds the per-channel chain-T+1 decomposition (Ch3 train n=117, Ch3 validate n=25). The bug-fix does NOT change the v1 halt verdict (the binding §7.5 gate-2 failure was on Ch3 validate, not on train Ch1/Ch2 at the corrected n=171, which comfortably clears the ≥30 bar).

3. **§4.11.3 sensitivity arm framing (chain-T+1 relaxation)**: the v2 §4.11.3 chain-relaxed Ch3 validate cell (n=41) is **descriptive sensitivity only**; it does NOT promote to the primary verdict. The §4.7 chain-T+1 rule is preserved for the headline because asymmetric chain-discipline (relaxing for validate only) is methodologically awkward as a primary. The reader sees what the cell would look like without the chain rule, but the primary verdict honors the chain rule.

4. **Audit Layer-2.5 v2 disposition (pragmatic pre-registration acknowledgment)**: v2 was drafted with knowledge that Ch3 validate has the n=25 boundary issue + Ch3 train passes at n=117. The triage analysis (which option to choose from the five identified in the v1 dry-run report) was done in a separate fresh session per `hypothesis_lock_process.md` §3.2; this drafting session was given only the composite-path recommendation and no per-day data values from the v1 test (the v1 full run never executed because of the halt). The §3.2-clause shared-context concern from v1 r2 (user-accepted as priced-in per audit L2.5 disposition) remains the documented boundary; v2 does not introduce new exposure to per-day per-channel values. Per L2.5 lock-stage call, the v1 r2 priced-in disposition carries forward to v2.

5. **L4.5 minor inherited carry-forward (Ch3 mean-vs-spike)**: the v2 audit flagged that Channel 3's `awake_stress_avg` is a mean while the Wiggers wording ("stress spikes much faster") suggests a spike-reading; the §4.11.2 spike-companion (`stress_high_duration_min` on T+1) is the descriptive companion. If the primary Ch3 and spike-companion diverge, the divergence is informative for §9 interpretation.

## Data-exposure context (inherited from v1 §Authorship)

HA-C4 v1 r2 was drafted, audited (fresh-session, verdict `REVISION RECOMMENDED`), revised, and **LOCKED 2026-06-17 by user acceptance** in a session that had already executed sister test HA-C4b (v1 → v2 → v3, NOT-SUPPORTED). The v1 drafter knew the identity of 10 unmedicated heavy-T crash days, but NOT the per-day per-channel values for the HA-C4 channels (different aggregations of the same underlying monitoring_b data). The fresh-session v1 audit verified no operational choices in §4 / §5 were biased by knowledge of the 10 crash-day identities; the L2.5 substantive concern was **priced-in by user acceptance**. The §4.11.1 crash-drop sensitivity arm (added v1 r2) further insulates the spec; readings reported below. **v2 drafted 2026-06-18 fresh-session**, audited fresh-session (PASS-with-caveats), and **LOCKED 2026-06-18 by user acceptance** at r2.

**Test execution session**: this `test.py` was implemented and run in a FRESH Claude session per the locked-pre-reg discipline. The session received only the LOCKED v2 spec + the v1 archive + the dry-run-report cell counts + the audit reports — not the per-day per-channel values, which become visible only when test.py executes.

## §7.5 sanity-gate compliance (top-of-report, v2 routing)

Gates 1 + 3 (HALT-eligible) passed at dry-run. Gate 2 (sub-30 cells per arm) flagged 1 cell(s) as INCONCLUSIVE per v2 §5.4 + §5.3 (not halt). See `dry-run-report.md` for per-gate detail.

| gate | result | v2 routing |
|---|---|---|
| Full-pool median within ±30% of §7.1 (×4 channels) | PASS | halt on failure |
| Per-channel × per-era arm sizes ≥ 30 (×6 cells) | 5 PASS / 1 INCONCLUSIVE | sub-30 → §5.4 INCONCLUSIVE (not halt) |
| Ch1 NaN fraction in [12%, 25%] | PASS (observed 0.1807) | halt on failure |

## §5.3 triad verdict (v2 INCONCLUSIVE-aware bands)

**Verdict: REJECTED** (triad sum = 0.0 of 3.0; no triad signal).

| channel | train | validate | channel verdict | contribution | label |
|---|---|---|---|---:|---|
| Ch1 | REFUTED | SUPPORTED | REFUTED | 0.0 | REFUTED (supported one era, refuted other) |
| Ch2 | REFUTED | SUPPORTED | REFUTED | 0.0 | REFUTED (supported one era, refuted other) |
| Ch3 | REFUTED | INCONCLUSIVE | REFUTED | 0.0 | REFUTED (one era refuted, other inconclusive) |

Per v2 §5.2 + §5.3 scoring rule: CONFIRMED (SUPPORTED both eras) → 1.0; CONFIRMED-PARTIAL (SUPPORTED one era + INCONCLUSIVE the other) → 0.5; REFUTED (any other combination, including SUPPORTED+REFUTED) → 0.0. Triad sum bands: 3.0 → **SUPPORTED (strong)**; 2.0–2.5 → **SUPPORTED**; 1.0–1.5 → **PARTIAL**; < 1.0 → **REJECTED**.

## §5.1 + §5.2 per-channel × per-era contingency table (primary)

Per-cell: Mann-Whitney U + Cliff's δ + block-permutation null at E[L]=7. **(a) discrimination**: empirical p < 0.05. **(b) effect size**: δ > +0.20 in predicted direction (heavy-T > non-heavy-T). Channel × era verdict: **SUPPORTED** iff (a) AND (b); **REFUTED** iff (a) fails or (b) fails (or wrong direction); **INCONCLUSIVE** iff either arm n < 30.

| ch | era | n_heavy | n_non | heavy med [p25–p75] | non med [p25–p75] | Cliff's δ | p-value | (a) | (b) | verdict |
|---|---|---:|---:|---|---|---:|---:|:---:|:---:|:---:|
| Ch1 | train | 171 | 314 | 143.00 [64.50–317.00] | 111.00 [47.00–300.50] | +0.056 | 0.1797 | fail | fail | REFUTED |
| Ch1 | validate | 41 | 58 | 98.00 [59.00–177.00] | 67.50 [34.25–113.75] | +0.238 | 0.0245 | PASS | PASS | SUPPORTED |
| Ch2 | train | 171 | 311 | 89.00 [53.50–127.50] | 67.00 [38.00–105.00] | +0.193 | 0.0004 | PASS | fail | REFUTED |
| Ch2 | validate | 41 | 58 | 79.00 [45.00–107.00] | 51.50 [34.25–73.75] | +0.356 | 0.0015 | PASS | PASS | SUPPORTED |
| Ch3 | train | 117 | 311 | 46.00 [41.00–50.00] | 46.00 [41.00–53.00] | -0.080 | 0.8546 | fail | fail | REFUTED |
| Ch3 | validate | 25 | 58 | — | — | — | — | — | — | INCONCLUSIVE |

*Channel 1 NaN-as-positive encoding (§4.5)*: 90 train + 8 validate days had `stress_post_peak_time_to_rest_min` NaN and were recoded to 1080 min for the Mann-Whitney + Cliff's δ computation.

## §4.11.3 Ch3 validate chain-relaxed sensitivity arm (v2 NEW, descriptive)

Per v2 §4.11.3: re-compute the Ch3 validate cell with the §4.7 chain-T+1 exclusion **relaxed for the heavy-T arm only** (n=41 vs primary n=25). Non-heavy-T arm is byte-identical to the primary (n=58; the §4.7 chain rule was always heavy-T-only by construction). **Descriptive sensitivity only; does NOT modify the §5.3 verdict** per §4.11.3 reporting rule.

| variant | n_heavy | n_non | Cliff's δ | p-value | verdict |
|---|---:|---:|---:|---:|:---:|
| Ch3 validate (primary, §4.7 chain applied) | 25 | 58 | NA | NA | INCONCLUSIVE |
| Ch3 validate (chain-relaxed §4.11.3) | 40 | 58 | -0.181 | 0.9194 | REFUTED |

**Reading**: primary Ch3 validate is INCONCLUSIVE (n_heavy=25 < 30 per §5.4). Chain-relaxed cell diverges from Ch1 + Ch2 validate (conflicting descriptive context). Per §4.11.3, descriptive context only; the §5.3 verdict applies CONFIRMED-PARTIAL to Ch3 if Ch3 train is SUPPORTED.

## §5.5 Holm step-down per era (multiplicity sensitivity, secondary)

Holm step-down at α=0.05 on the per-era p-values. Per v2 §5.5, **INCONCLUSIVE cells are omitted from the per-era Holm ordering** — a 2-of-2-comparison Holm uses cutoffs α/2 and α/1 (vs. 3-of-3's α/3, α/2, α/1) and is therefore less stringent. The annotation column surfaces the reduced-comparisons disclosure. **Per §5.0, Holm is a secondary report**; the §5.3 verdict uses the uncorrected per-channel p-values.

| era | Ch1 raw p | Ch2 raw p | Ch3 raw p | Ch1 adj p | Ch2 adj p | Ch3 adj p | Holm-rejected | annotation |
|---|---:|---:|---:|---:|---:|---:|---|---|
| train | 0.1797 | 0.0004 | 0.8546 | 0.3594 | 0.0012 | 0.8546 | Ch2 | Holm (3-of-3 comparisons) |
| validate | 0.0245 | 0.0015 | INC | 0.0245 | 0.0030 | INC | Ch1, Ch2 | Holm (2-of-2 comparisons; Ch3 INCONCLUSIVE) |

## §4.11.1 Crash-drop sensitivity (CONVENTIONS §3.4)

Per §4.11.1 + audit L4.4 closure: re-run the Mann-Whitney + Cliff's δ with `is_crash == True` dropped from BOTH arms. Flag if |Δ Cliff's δ| > 0.1 on any channel ("the channel's signal is crash-driven, not robust across the broader heavy-T pool").

| channel | era | primary δ | crash-dropped δ | Δ δ (dropped − primary) | n_heavy (dropped) | flag |
|---|---|---:|---:|---:|---:|:---:|
| Ch1 | train | +0.056 | +0.094 | +0.038 | 157 | ok |
| Ch1 | validate | +0.238 | +0.221 | -0.017 | 34 | ok |
| Ch2 | train | +0.193 | +0.213 | +0.020 | 157 | ok |
| Ch2 | validate | +0.356 | +0.397 | +0.041 | 34 | ok |
| Ch3 | train | -0.080 | -0.040 | +0.039 | 107 | ok |
| Ch3 | validate | NA | NA | — | — | NA |

## §4.11.2 Channel 3 spike-metric companion (CONVENTIONS §3.5)

Per §4.11.2 + audit L4.5 closure: parallel Mann-Whitney on `stress_high_duration_min` on T+1 (spike-count companion) alongside the primary `awake_stress_avg` on T+1 (mean). If both agree (same verdict direction and approximate effect size), the average-vs-spike question is closed; if they diverge, the divergence is informative for §9 interpretation.

| era | primary Ch3 (awake-mean T+1) δ | spike companion (high_dur T+1) δ | primary p | spike p | primary verdict | spike verdict |
|---|---:|---:|---:|---:|:---:|:---:|
| train | -0.080 | -0.081 | 0.8546 | 0.8609 | REFUTED | REFUTED |
| validate | NA | NA | NA | NA | INCONCLUSIVE | INCONCLUSIVE |

## §4.11 Channel 1 secondary companions + NaN-fraction contrast

Per §4.11: parallel Mann-Whitney on `stress_post_peak_drop_avg` (Ch1 secondary aggregate) and `stress_recovery_pct_within_2h` (direct rate-of-recovery metric). The Ch1 NaN-fraction descriptive contrast (heavy-T vs non-heavy-T) is the alternative to the §4.5 1080-min encoding; per §7.2 the unmedicated baseline shows these are essentially tied at ~18% — companion reported anyway as the encoding-fragility check.

| companion | era | n_heavy | n_non | Cliff's δ | p-value | verdict |
|---|---|---:|---:|---:|---:|:---:|
| drop_avg | train | 168 | 310 | +0.210 | 0.0009 | SUPPORTED |
| drop_avg | validate | 41 | 57 | +0.364 | 0.0012 | SUPPORTED |
| recovery_pct_within_2h | train | 143 | 275 | -0.100 | 0.9268 | REFUTED |
| recovery_pct_within_2h | validate | 37 | 53 | -0.086 | 0.7301 | REFUTED |

### Ch1 NaN-fraction contrast (heavy-T vs non-heavy-T)

| era | heavy-T NaN frac | non-heavy-T NaN frac | pp contrast |
|---|---|---|---:|
| train | 0.1813 (31/171) | 0.1879 (59/314) | -0.66 |
| validate | 0.0976 (4/41) | 0.0690 (4/58) | +2.86 |

Per §4.11: if heavy-T NaN fraction is > 10 pp higher than non-heavy-T, that is direct C4-positive descriptive evidence independent of the 1080-encoded Mann-Whitney result. Per §7.2 the unmedicated baseline is essentially tied — the directional signal (if any) comes from the non-NaN distribution shift.

## §4.9 Data-driven E[L]* companion (factor-of-2 flag)

Per §4.9 + audit L3.1 closure: data-driven `E[L]*` (Politis-White automatic block-length, Patton-Politis-White correction for the stationary bootstrap) computed on BOTH (a) each channel's value series AND (b) the heavy-T label sequence. Flag fires if `|E[L]* − 7| / 7 > 0.5` on either. **Per the methodology MD, the flag is verdict-relevant only on SUPPORTED verdicts; for PARTIAL or REJECTED, the flag is descriptive context only.**

Triad verdict: **REJECTED**. Flag status: no flags.

| channel | era | E[L]* on values | flag (values) | E[L]* on labels | flag (labels) |
|---|---|---:|:---:|---:|:---:|
| Ch1 | train | 7.00 | ok | 7.00 | ok |
| Ch1 | validate | 7.00 | ok | 7.00 | ok |
| Ch2 | train | 7.00 | ok | 7.00 | ok |
| Ch2 | validate | 7.00 | ok | 7.00 | ok |
| Ch3 | train | 7.00 | ok | 7.00 | ok |
| Ch3 | validate | 7.00 | ok | 7.00 | ok |

## Sister-test cross-reference

| hypothesis | status | one-line note |
|---|---|---|
| HA-C4b v3 | NOT-SUPPORTED (2026-06-17) | motion-filter crash-precursor framing; (a)=40%, (b)=−10pp, (c)=+1.21 |
| HA11 | SUPPORTED on train (+22.8 pp) | U-dip sister channel (calm-day signal); validate inconclusive on original spec |

Per §9 cross-references: **HA-C4 SUPPORTED + HA-C4b NOT-SUPPORTED** supports the protective-rather-than-predictive reading from HA-C4b §9 (the Wiggers pattern IS real on this corpus, but the participant's real-time use of it as a pacing trigger prevents the crashes the precursor test would have caught). **HA-C4 REJECTED + HA-C4b NOT-SUPPORTED + HA11 SUPPORTED** would mean the Wiggers C4 framework doesn't operationalise cleanly on this corpus at either the descriptive or precursor level, but the U-dip (HA11) sister channel does — C4 mechanism would need different operationalisation (e.g. bout-level recovery curves) to be testable. **HA-C4 PARTIAL** outcomes name the specific channel(s) that confirmed; the substantive read follows the channel-set.

## §8 Caveats (v1 inherited)

- **Power-calc dispatch**: power calculation is inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design. The block-permutation null at E[L]=7 (§4.9) is the within-subject inferential machinery; the §5.1 (a) + (b) gates determine per-cell verdict rather than a power-thresholded p-value. The v2 §5.3 INCONCLUSIVE handling does NOT introduce a separate power-calc requirement: the ≥30-per-arm bar (§5.4) inherits from v1.
- **NaN-as-positive encoding for Channel 1** (§4.5): the 1080-min coding is one operationalisation; the NaN-fraction descriptive contrast (table above) is the alternative. If the verdict depends on the encoding choice, flag as encoding-fragile. Per §7.2 the unmedicated baseline shows essentially tied NaN fractions across arms (~18% both), so the encoding's impact on the Mann-Whitney verdict is small.
- **Chained-regime adjustment for Channel 3** (§4.7): heavy-T-followed-by-heavy-T+1 days are excluded from the Channel 3 primary arm (train: 117 of 171; validate: 25 of 41). v2 §5.3 + §4.11.3 explicitly handle the validate sub-30 case (CONFIRMED-PARTIAL contribution at the channel-aggregation layer; chain-relaxed descriptive sensitivity arm above).
- **Citalopram dose-modulation** (§4.4): the primary scope is unmedicated only specifically to avoid the dose-confound on the stress channel ([`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md)). Cross-phase sensitivity arms are not run in this v2 — that scope is queued.
- **No motion filter** (unlike HA-C4b): HA-C4 tests channels without conditioning on motion. Garmin stress is partly motion-sensitive per [`hrv_proxy_via_stress.md`](../../../methodology/hrv_proxy_via_stress.md). Some channel signal may be motion-artefact rather than true sympathetic load; cross-reference HA-C4b's motion-filter result.
- **Unmedicated = pre-citalopram corpus, not 'no medication overall'**: participant had other lived-experience interventions in the 2022-04 → 2024-04 window (CPAP started 2024-01-10; ergotherapy 2022-06-17 → 2023-03-10; PWC reintegratie 2023-03-06 → 2023-11-28). The unmedicated headline is 'no SSRI' not 'no intervention'.
- **Pacing-behaviour confounder** (inherited from HA-C4b v3 §8): `exertion_class_lagged_lcera` captures physical exertion only. Cognitive, emotional, and orthostatic exertion are not in the classification. A 'non-heavy-T' day in this test could include high cognitive / emotional load days that are physiologically demanding. Mis-classifying them as non-heavy-T arm would dilute the contrast (directional bias toward false-NOT-SUPPORTED).
- **Single-subject n=1**: thresholds in §5.1 (p < 0.05, |δ| > 0.20) are calibrated to the participant's distribution. The Mann-Whitney is non-parametric so the threshold-on-effect-size choice is the binding decision; a stricter Cliff's δ threshold (e.g. 0.33 for 'medium' effect) would shift the gate.
- **HA11 / HA-C4b cross-references**: see sister-test table above.
- **Block-permutation under stationary bootstrap of labels**: the bootstrap does not preserve the marginal n_heavy count (observed mean n_heavy_null is reported in `result-data.json` per cell). At B = 10000 the empirical-p noise from this shift is small.

---

*test.py run with `RANDOM_SEED = 20260618`, `BOOTSTRAP_E_L = 7`, B = 10000 draws per cell. Source data: `per_day_master.csv` from `$GEVOELSCORE_DATA_PATH`. Spec commit: `(unmerged-working-tree)`. `result-data.json` is the machine-readable companion (gitignored per `docs/research/**/*.json`).*
