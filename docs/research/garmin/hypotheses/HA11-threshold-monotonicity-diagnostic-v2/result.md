# HA11 v2 diagnostic — result

**Verdict per locked v2 criteria: RESCUE** (train one-sided elevated
primary). **Cat 1 (canonical decline) PASSES** — the textbook robust
shape. No FAIL category triggers.

HA11's locked train SUPPORTED verdict at primary 4d one-sided
elevated N_std=1.5 (+22.8 pp) stays on record AND under v2 the
synthesis-level framing is confirmed as **load-bearing**. HA11
was demoted to "load-bearing pending v2" under the interim
asymmetry fix; v2 RESCUES it. Restored to load-bearing.

This is the cleanest RESCUE in the v2 round — Cat 1 (canonical
decline) is the shape v1 criteria were specifically designed to
detect. HA11's curve is textbook.

## Train one-sided elevated shape analysis

| stat | value | criterion check |
|---|---:|---|
| peak N_std | **1.25** | Cat 1 requires ∈ [1.0, 1.5] ✓ |
| peak disc | +45.4 pp | (very strong) |
| disc at N_std=2.0 | +17.5 pp | Cat 1 requires ≥ +10 ✓ |
| disc at N_std=2.5 | +20.4 pp | Cat 1 requires ≥ +7 (raised in v2) ✓ |
| Spearman rho | −0.683 | Cat 1 requires ≤ −0.3 ✓ (strongly monotonic decline) |
| sign-changes | 0 | Cat 1 requires ≤ 1 ✓ |
| direction reversals (descriptive only) | 3 | not used in verdict |
| max negative disc | +7.9 (lowest is +7.9 at N_std=3.0; positive throughout meaningful range) | Cat 4 ✗ |

**The curve**:
```
N_std    train_disc
0.50    +26.5
0.75    +34.0
1.00    +44.0
1.25    +45.4  ← peak
1.50    +22.8  (locked v1 primary verdict)
1.75    +18.1
2.00    +17.5
2.25    +25.0
2.50    +20.4
2.75    +18.2
3.00     +7.9
3.50     +1.1
4.00     +2.1
```

Peak at N_std=1.25 within the rescue window [1.0, 1.5]; smooth
decline (with one mild bump at N_std=2.25 — but no sign change);
discrimination stays positive across the entire grid; magnitude
remains above the +7 pp Cat 1 floor at N_std=2.5.

**Verdict**: Cat 1 PASS, no FAIL triggers → Rule (ii): PASS only
→ **RESCUE**.

## Validate descriptive (already REFUTED inverse at v1 primary)

Validate one-sided elevated curve is uniformly negative across
the meaningful range (min −17.5 at N_std=1.0; max −5.8 at
N_std=3.0). Spearman rho +0.767 in restricted range — the
signal does monotonically rise toward zero as threshold tightens
(consistent with "less inverse signal at strict tiers because
fewer samples"). Cat 4 triggers via max_neg = −17.5 ≤ −10. CLOSE.

The validate inverse-direction signal (HA11 v1 finding that
validate-era crashes have FEWER U-dip events than typical) is
threshold-robust at the descriptive level — the inverse pattern
holds across the grid.

## What this changes

Per the locked v2 §4 verdict logic and §5 application rules:

- HA11 train one-sided elevated **confirmed as load-bearing**
  via v2 Cat 1 RESCUE.
- Synthesis-level framing: HA11 returns to load-bearing for the
  pre-cliff multi-channel narrative.
- Card (b) train-era retrospective: HA11 retained as one of
  the converging empirical anchors.

## Cross-test note

HA11's Cat 1 RESCUE is the cleanest robust shape in the v2
round:
- HA10 validate Cat 3 (rising/late-peak) — robust but peak past
  the canonical window.
- HA07d both eras Cat 2/3 (stable plateau / rising) — robust but
  same.
- HA11 train Cat 1 (canonical decline) — textbook robust.

The U-dip count z-score is the train-era channel where the
discrimination curve most cleanly matches the classical
signal-detection theory expectation.

## What this does NOT change

- The peer-review §3 caveat that HA11's U-dip detector has
  parameter degrees of freedom not externally anchored remains
  — that's a separate diagnostic (HA11 parameter sensitivity,
  queued as Tier 2 action item).
- HA11's validate inverse-direction finding (refuted at v1
  primary) is unaffected; v2 confirms the inverse pattern is
  threshold-robust descriptively.

---

*v2 diagnostic locked at [diagnostic.md](diagnostic.md); v2 criteria
locked at [methodology/threshold-sweep-rescue-criteria-v2.md](../../methodology/threshold-sweep-rescue-criteria-v2.md).
First v2 fine-grid computation on HA11 (no v1 ran).*
