# HA06b v2 diagnostic — result

**Verdict per locked v2 criteria: CLOSE** (train bidirectional
primary). Cat 4 (bumpy with sign changes) triggers. No PASS
category matches.

HA06b's locked train SUPPORTED verdict at primary 4d bidirectional
N_std=1.5 (+18.9 pp) stays on record per audit-trail discipline.
But the v2 diagnostic exposes a shape characteristic — 2
zero-crossings within the meaningful range [1.0, 3.0] — that
classifies the curve as non-robust under the locked criteria.

**HA06b train is permanently demoted to non-load-bearing** in
synthesis-level framing. This is the discipline applying
symmetrically: HA06b was demoted to "load-bearing pending v2"
under the interim asymmetry fix; v2 confirms the demotion is
warranted, not lifted.

## Train bidirectional shape analysis

| stat | value | criterion check |
|---|---:|---|
| peak N_std | 1.75 | |
| peak disc | +22.4 pp | (above the +15 threshold) |
| disc at N_std=2.0 | +21.3 pp | (above +10) |
| sign-changes (zero-crossings in [1.0, 3.0]) | **2** | Cat 4 trigger: ≥ 2 ✗ FAILS Cat 1, 2, 3 (all require ≤ 1) |
| direction reversals (descriptive only) | 3 | not used |
| Spearman rho | −0.017 | Cat 1 needs ≤ −0.3 — fails |
| max negative disc | −4.1 (at N_std=1.0) | Cat 4 trigger: not ≤ −10, but sign-changes is the dispositive failure |
| longest contiguous run > +15 pp | 4 tiers [1.5 → 2.5 with one dip] | Cat 2 requires no sign-change interruption — fails |
| positive across [1.0, peak] | NO (disc at 1.0 = −4.1) | Cat 3 requires positive across rise — fails |

**The curve**:
```
N_std    train_disc
0.50     +2.4
0.75     -7.4   ← negative
1.00     -4.1   ← negative (in meaningful range)
1.25     +5.4   ← positive (sign change 1)
1.50    +18.9
1.75    +22.4   ← peak
2.00    +21.3
2.25    +15.0
2.50    +20.0
2.75     +2.6
3.00     -2.1   ← negative (sign change 2 in meaningful range)
3.50     +2.4
4.00     +5.4
```

The two zero-crossings in [1.0, 3.0] dispositively trigger Cat 4.
**No PASS category matches**: Cat 1 fails on peak location AND rho;
Cat 2 fails because no 4-contiguous-tier run > +15 pp exists
without sign-crossing interruption; Cat 3 fails because disc at
N_std=1.0 is negative (not positive across rise).

**Verdict**: Cat 4 FAIL, no PASS → Rule (iii): FAIL only →
**CLOSE**.

## Validate descriptive (was already REFUTED at v1 primary)

Validate bidirectional curve is decisively negative for most of
the meaningful range (peak at N_std=1.5 = +0.8 pp; min at
N_std=2.25 = −21.7 pp). Spearman rho = −0.783 (strong negative
trend, but in the wrong direction — i.e., signal goes more
inverse as threshold tightens). Cat 4 triggers via max_neg = −21.7
≤ −10. CLOSE.

This confirms HA06b's validate refutation at v1 primary is robust
across thresholds — the inverse pattern in validate-era RHR is
genuine and threshold-stable.

## What this changes

Per the locked v2 §4 verdict logic and §5 application rules:

- HA06b train SUPPORTED verdict stays on record (locked).
- Synthesis-level framing: HA06b train **permanently demoted to
  non-load-bearing**. Was previously "load-bearing pending v2"
  under the interim asymmetry fix; v2 confirms the demotion is
  warranted.
- Card (b) train-era retrospective: HA06b anchor dropped from
  the load-bearing list. Remaining train anchors: H02b, H02d,
  HA11, HA07d (each pending its own v2 diagnostic where
  applicable). HA07c and HA08c not yet diagnosed under v2.
- The pre-cliff multi-channel narrative weakens: "six channels
  confirmed" → "five channels confirmed under v2 (with H02b /
  H02d still pending their own diagnostic; HA07c / HA08c
  pending too)." HA06b channel removed from confirmed list.

## Honest reflection — the discipline binding against pre-registered findings

HA06b train SUPPORTED at +18.9 pp was a project finding. The v2
diagnostic — designed in good faith with criteria locked
symmetrically — produces CLOSE for this finding. The reviewer's
"symmetric application" critique was correct: HA06b couldn't be
exempt from v2 just because it wasn't in the original v1 round.

The discipline binds in the demotion direction too. The other
restorations under v2 (HA10, HA07d, HA11) are vindicated by the
discipline applying consistently — including against findings
the project would have preferred to keep.

## What this does NOT change

- The locked HA06b result.md +18.9 pp SUPPORTED verdict is
  unchanged on record.
- The original peer-review caveat about HA06b's
  channel-non-independence with HA07c/HA08c/HA07d still applies.
- The HA06b validate refutation is **strengthened** by v2: the
  inverse pattern is threshold-robust (Spearman −0.783, max neg
  −21.7).

---

*v2 diagnostic locked at [diagnostic.md](diagnostic.md); v2 criteria
locked at [methodology/threshold-sweep-rescue-criteria-v2.md](../../methodology/threshold-sweep-rescue-criteria-v2.md).
First v2 fine-grid computation on HA06b (no v1 ran).*
