# HA07d v2 diagnostic — result

**Verdicts per locked v2 criteria: RESCUE both eras.**
- Train bidirectional: **RESCUE** via Cat 3 (rising/late-peak).
- Validate bidirectional: **RESCUE** via Cat 2 (stable plateau)
  AND Cat 3 (rising/late-peak).

HA07d's locked OVERALL-SUPPORTED verdict at primary 4d
bidirectional N_std=1.5 (train +19.6 pp, validate +21.7 pp) stays
on record. Under v2 the synthesis-level demotion is **reversed**
in both eras. HA07d restored to **load-bearing overall-SUPPORTED
test** — the project's first to clear both eras at primary under
v2 criteria.

This is the consequential restoration the worked-walkthrough
predicted: the discipline binds against the researcher's earlier
intuition that train would CLOSE under v2. **Both eras RESCUE.**

## Train bidirectional shape analysis

| stat | value | criterion check |
|---|---:|---|
| peak N_std | 1.75 | Cat 3 requires > 1.5 ✓ |
| peak disc | +21.4 pp | Cat 3 requires ≥ +15 ✓ |
| disc at N_std=2.0 | +15.5 pp | Cat 3 requires ≥ +10 ✓ |
| sign-changes (zero-crossings in [1.0, 3.0]) | 0 | Cat 3 requires ≤ 1 ✓ |
| positive across [1.0, peak] | yes (all positive in [1.0, 1.75]) | Cat 3 ✓ |
| Spearman rho | −0.250 | (Cat 1 needs ≤ −0.3, fails; Cat 3 has no rho requirement) |
| direction reversals (descriptive only) | 4 | not used in verdict |
| max negative disc | +2.8 (positive throughout meaningful range) | Cat 4 requires ≤ −10 ✗ |

**Verdict**: Cat 3 PASS, no FAIL triggers → **RESCUE**.

## Validate bidirectional shape analysis

| stat | value | criterion check |
|---|---:|---|
| peak N_std | 1.75 | Cat 3 requires > 1.5 ✓ |
| peak disc | +31.2 pp | Cat 2 needs > +15; Cat 3 needs ≥ +15 ✓ |
| disc at N_std=2.0 | +27.3 pp | Cat 3 requires ≥ +10 ✓ |
| sign-changes | 0 | Cat 2 and Cat 3 both require ≤ 1 ✓ |
| longest contiguous run > +15 pp | 8 tiers [1.0 → 2.75] | Cat 2 requires ≥ 4 ✓ |
| run includes [1.0, 1.5] and [2.0, 2.5] | yes ✓ ✓ | Cat 2 ✓ |
| plateau variation (max−min)/max | 36% | Cat 2 requires ≤ 50% ✓ |
| Spearman rho | −0.283 | |
| direction reversals (descriptive only) | 5 | not used |
| max negative disc | +13.0 (positive throughout meaningful range) | Cat 4 ✗ |

**Verdict**: Cat 2 PASS AND Cat 3 PASS, no FAIL triggers →
**RESCUE**.

## What this changes

**HA07d's overall-SUPPORTED status is restored.** Under v2, HA07d
remains the first pre-registered test to SUPPORT in BOTH eras at
the strict locked rule — and now under the more rigorous v2
diagnostic that also captures non-canonical robust shapes.

Per the locked v2 §4 verdict logic and §5 application rules:

- HA07d both eras restored to **load-bearing** in synthesis-level
  framing.
- Card (b2) validate-era retrospective: HA07d restored as **sole
  primary anchor** (HA10 returns as corroborating-secondary after
  HA10 v2 RESCUE).
- The era-as-moderator narrative anchored on HA07d's single-channel
  both-eras-SUPPORTED-with-opposite-direction finding **is
  restored**.
- D7 single-mechanism-two-regimes reframe: empirical anchor on
  HA07d restored. Wiggers' "freeze" pattern empirically population-
  level visible at the load-bearing level.

## Comparison to v1 + the discipline lesson

v1 CLOSE both eras was driven by:
- Peak at 1.75 outside the v1 rescue window [1.0, 1.5]
- Train Spearman rho near zero (+0.005) and 4 sign-changes (in
  full grid)
- Validate Spearman rho positive (+0.170) — penalised by v1 even
  though signal was sustained

v2 explicitly addresses each:
- Cat 3 allows peak > 1.5
- Sign-changes restricted to meaningful range [1.0, 3.0] gives 0
  for both eras (the train sign-changes happened at N_std < 1.0
  and N_std > 3.0)
- Cat 3 has no Spearman requirement (rising signal can have
  positive Spearman)

The discipline working as designed:
1. v1 paid the demotion cost.
2. v2 was locked symmetrically, with criteria designed against
   the data-shape categories that emerged.
3. v2 verdict honestly applies the locked criteria.
4. The restoration is principled — Cat 3 captures a robust shape
   v1 missed.

The reviewer was right that this consequence needed surfacing
before v2 ran. It is now confirmed.

## What this does NOT change

- The peer-review §3 channel-independence caveat still applies:
  HA07d is one of three primitives on the same sleep-stress
  channel. The "convergence" framing across HA07c/HA08c/HA07d
  is multiple operationalisations of the same construct.
- The card (b2) specificity caveat still applies: posterior
  probability per fire ≈ 2.3% under base rate. Card text must
  use specificity language.
- The pre-registered diagnostic produced an honest verdict that
  could have gone either way; the restoration is not a vindication
  of the project's intuition — it is the discipline applied as
  written.

---

*v2 diagnostic locked at [diagnostic.md](diagnostic.md); v2 criteria
locked at [methodology/threshold-sweep-rescue-criteria-v2.md](../../methodology/threshold-sweep-rescue-criteria-v2.md).
Same v1 fine-grid data; no new computation needed.*
