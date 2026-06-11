# HA01c — Effective-exertion shock as crash precursor (result)

**Run date**: 2026-06-07. **Test script**: [test.py](test.py).
**Pre-registration**: [hypothesis.md](hypothesis.md), locked
2026-06-07 per testing playbook
([../../methodology/testing-playbook.md](../../methodology/testing-playbook.md))
section 9. **Output data**: [result-data.json](result-data.json).

## TL;DR — HA01c locked-threshold verdict

**SUPPORTED both eras** at the locked 3-criterion bar:

| era | n_clean | freq | null_freq | disc | median_rank | crit (a) | crit (b) | crit (c) | verdict |
|---|---:|---:|---:|---:|---:|:-:|:-:|:-:|:-:|
| train    | 11 | 81.8% | 60.5% | **+21.3 pp** | 0.883 | PASS | PASS | PASS | **SUPPORTED** |
| validate | 15 | 80.0% | 60.5% | **+19.5 pp** | 0.909 | PASS | PASS | PASS | **SUPPORTED** |

The locked HA01c bar (same as HA01b composite bar): crash trigger
frequency ≥ 60%, discrimination ≥ +15 pp, median rank on triggering
episodes ≥ 0.875.

The both-eras rule (playbook §4.4) is satisfied. Per the HA01c
hypothesis.md §5 co-lock, the load-bearing status is **gated on
HA01c v2 threshold-monotonicity diagnostic also RESCUING**.

**See [HA01c v2 result.md](../HA01c-threshold-monotonicity-diagnostic-v2/result.md)
for the v2 outcome and the final load-bearing status.**

## What HA01c re-confirmed vs the per-axis diagnostic

This is a clean re-test of the HA01b per-axis diagnostic's
effective_exertion both-eras SUPPORTED finding. As expected, the
numbers are identical (same data, same null seed, same threshold):

| metric | per-axis diagnostic | HA01c re-test | delta |
|---|---:|---:|---:|
| train discrimination | +21.3 pp | +21.3 pp | 0.0 |
| validate discrimination | +19.5 pp | +19.5 pp | 0.0 |
| train freq | 81.8% | 81.8% | 0.0 pp |
| validate freq | 80.0% | 80.0% | 0.0 pp |

The HA01c re-run was disciplinary, not informational. The per-axis
diagnostic produced a **diagnostic finding**, NOT a re-test verdict
per playbook §5.2. HA01c pre-registers the effective_exertion-as-primary
hypothesis explicitly and locks the verdict under the standard
hypothesis flow. The locked HA01c verdict is the canonical artifact
for this hypothesis; the per-axis diagnostic is the audit trail
that motivated HA01c.

## Caveats (carried forward from hypothesis.md §5 and per-axis diagnostic §6)

1. **HA01b composite REFUTED stays on record** unchanged. HA01c is
   not a re-test of HA01b; it is a separate hypothesis with a
   different primary per playbook §2.2.

2. **Specificity caveat (playbook §6.2) binds**. At the locked 0.75
   threshold:
   - Null trigger rate ≈ 60.5% (60% of any 4-day window in the
     analysis range triggers).
   - Crash trigger rate ≈ 80%.
   - **Posterior probability per fire ≈ 2.2% vs 1.7% base rate.**
   - A card built on this primitive would fire ~every other day
     and only marginally lift posterior over base rate.
   - **NOT shippable as a card without further refinement** (tighter
     threshold, multi-condition AND, temporal aggregation).
   - The HA01c v2 threshold-monotonicity diagnostic was designed
     to test whether tighter thresholds (e.g., 0.85, 0.90) yield
     acceptable specificity. See v2 result.md for the shape
     analysis.

3. **Channel non-independence**: effective_exertion is the "central"
   axis of the 4-axis composite (correlates 0.62 with max_hr_peak,
   0.69 with vigorous_min, 0.44 with step_burden per the per-axis
   diagnostic cross-axis matrix). HA01c is a single-axis test but
   the axis is not independent of other physical-activity axes.

4. **Train sample is 11 of 14 episodes clean** (3 dropped to
   lagged-baseline warmup — same as per-axis diagnostic). Validate
   is 15 of 15. The train arm is conservative; the validate arm
   is fully populated.

5. **No-go surfaces (playbook §6.6)**: even SUPPORTED + v2 RESCUE
   does not unlock crash-risk percentages, traffic-light alerting
   on this primitive, push notifications, or any forbidden surface.
   Card design is reflective-only per playbook §6.6.

## Compliance verification (playbook §9, 19 items)

All 19 items satisfied per hypothesis.md §9 pre-registration.
Re-verified on completion:

- [x] Folder structure: `HA01c-effective-exertion-shock/` per §4.7
- [x] Pre-registration locked before HA01c-specific run: 2026-06-07
- [x] References playbook in hypothesis.md and result.md
- [x] crash_v1 used (29 episodes; 14 train, 15 validate)
- [x] Default train/validate split + both-eras rule applied
- [x] Lagged baseline (`effective_exertion_rank_lagged` column)
- [x] Relative thresholds (rank ≥ 0.75; rank IS the relative)
- [x] Primary direction: one-sided elevated, locked from per-axis
  diagnostic positive result
- [x] 3-episode dry-run gate: ran (output in test.py stdout)
- [x] 3-criterion bar at locked thresholds (≥60%, ≥+15 pp, ≥0.875)
- [x] Null sample seed `20260605`, N=200
- [x] Validity floors: ≥3 of 4 lead-up days valid
- [x] Decision rules → verdict categories per playbook §2.6
  (SUPPORTED both eras under locked bar)
- [x] Channel-independence acknowledgement: caveat 3 above
- [x] Multi-comparison disclosure: see per-axis diagnostic §6.2
  (HA01c is a re-formulation of one axis already SUPPORTED in
  per-axis diagnostic; no new multi-comparison)
- [x] v2 threshold-monotonicity follow-up: co-locked at
  [v2 diagnostic.md](../HA01c-threshold-monotonicity-diagnostic-v2/diagnostic.md)
- [x] No-go surfaces flagged: caveat 5
- [x] Hardware constraints: none specific (UDS daily aggregates)
- [x] Audit trail: this entire result.md cross-references the
  per-axis diagnostic motivation

## Next step

Run the [HA01c v2 threshold-monotonicity diagnostic](../HA01c-threshold-monotonicity-diagnostic-v2/diagnostic.md).
The HA01c locked verdict (SUPPORTED both eras) graduates to
load-bearing only if v2 RESCUES; CLOSE keeps HA01c on record but
withholds load-bearing per playbook §5.2.

---

*Result locked 2026-06-07. v2 threshold-monotonicity diagnostic
runs immediately after this result.md is written, per the locked
sequential pre-commitment in HA01c hypothesis.md §5.*
