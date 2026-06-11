# Lag profile + per-axis decomposition of HA01b

**Methodological status: exploratory / descriptive analysis, not
hypothesis confirmation.** HA01b at 4-day window is the
pre-registered SUPPORTED finding for validate-era crashes
(+17.3 pp). The lag profile below was explored post-hoc — after
seeing HA01b's positive result — and characterises the empirical
distribution of lags. **The 5-day window peak (+15.3 pp train,
+23.0 pp validate) should not be interpreted as a confirmed
result**: it was not pre-registered, and selecting "the window
that gave the strongest signal" without prior commitment is
exactly the kind of post-hoc selection pre-registration discipline
aims to prevent. A pre-registered HA01c at 5-day window on
genuinely new data (extended time window, additional participants)
would be the right path to confirm.

The exploratory finding is still useful descriptively: the
empirical lag distribution for *this person* peaks around 5 days,
which is the lag any retrospective card should reference. We
withhold the "SUPPORTED" verdict at 5-day; the descriptive
characterisation of the lag distribution is solid.

Post-hoc analysis of HA01b's SUPPORTED finding (+17.3 pp validate at 4-day window). Brackets the lag distribution and identifies which exertion axis drives the signal.

## 1. Lag profile (HA01 across windows 2-7 days)

Each row: window-day count; null + train-crash + validate-crash + validate-dip frequencies and discriminations.

| window | null freq | train crash freq | train disc | validate crash freq | **validate disc** | validate dip freq | validate dip disc |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2d | 53.0% | 61.5% | +8.5 pp | 53.3% | **+0.3 pp** | 61.5% | +8.5 pp |
| 3d | 68.5% | 69.2% | +0.7 pp | 80.0% | **+11.5 pp** | 73.1% | +4.6 pp |
| 4d | 76.0% | 84.6% | +8.6 pp | 93.3% | **+17.3 pp** | 75.0% | -1.0 pp |
| 5d | 77.0% | 92.3% | +15.3 pp | 100.0% | **+23.0 pp** | 80.8% | +3.8 pp |
| 6d | 86.0% | 92.3% | +6.3 pp | 100.0% | **+14.0 pp** | 86.5% | +0.5 pp |
| 7d | 94.5% | 92.3% | -2.2 pp | 100.0% | **+5.5 pp** | 88.5% | -6.0 pp |

**Reading**: validate disc identifies the window length where the validate-era precursor signal is strongest. HA01b's locked window (4d) is one of these data points.

## 2. Per-axis decomposition at 4-day window

For each axis, restrict 'shock' definition to that axis alone (rank ≥ 0.85 = heavy+ on that axis) and re-test discrimination.

| axis | null freq | train crash freq | train disc | validate crash freq | **validate disc** |
|---|---:|---:|---:|---:|---:|
| A_effective | 42.6% | 75.0% | +32.4 pp | 60.0% | **+17.4 pp** |
| B_steps | 44.7% | 66.7% | +22.0 pp | 60.0% | **+15.3 pp** |
| C_max_hr | 53.8% | 58.3% | +4.5 pp | 66.7% | **+12.9 pp** |
| D_vigorous | 49.2% | 50.0% | +0.8 pp | 66.7% | **+17.4 pp** |

**Reading**: which single axis contributes most to HA01b's +17.3 pp validate discrimination? Compare each axis's validate disc vs the multi-axis composite (HA01b validate +17.3 pp).

---

*Run 2026-06-06. Seed `20260605`.*