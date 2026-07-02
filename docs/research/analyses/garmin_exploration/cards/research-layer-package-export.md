# Research-layer package export (R8)

**Status**: producer-mode assembly for site request **R8** (the Layer-4
"un-interpreted floor" — the pre-registration cycle, the fresh-session audits,
the closed-hypothesis ledger with real statistics, and the link to the repo).
Aggregated and privacy-safe. No new analysis: this collates already-locked
results. Drafted 2026-07-02 by Claude (Opus 4.8), producer-mode, for the
participant-researcher (repo owner).

## 1. What this is

The research layer's honest floor: how the work was disciplined, what the
scorecard signals actually scored under the current (single-pool) framing, and
where the un-abridged record lives. It is the "show the work" layer beneath
the field guide.

## 2. The discipline (five gates every result passed)

1. **Pre-registration before data.** Each hypothesis has a locked
   `hypothesis.md` written before the outcome was seen; any change spawns a
   versioned successor. The crash definition (`crash_v1` / `crash_v2`) is
   fixed once so verdicts are comparable.
2. **Fresh-session peer review.** Every reviewer-mode artefact (pre-reg,
   verdict, methodology choice) is drafted in one session and reviewed cold in
   a different session, document-only. Reviews land in
   `docs/research/reviews/`.
3. **Audit-before-push privacy gate.** `audit_for_publication.py` must PASS
   before any commit: it scans for names, emails, and dated raw values.
   Nothing dated or personal ships.
4. **Single-pool primacy.** The old 2023-12-31 train/validate split is retired
   as primary; verdicts run on the full pool of all 29 crashes with a
   block-permutation null and stationary-bootstrap CIs. Any over-time
   difference ships as a number with wide error, never a per-era verdict.
5. **Honest verdict categories.** Every result uses the same labels
   (SUPPORTED / NOT-SUPPORTED / REJECTED / inconclusive); a NOT-SUPPORTED
   result is published as readily as a SUPPORTED one.

## 3. The scorecard ledger (single-pool)

The seven scorecard signals, single-pool primary verdict + usability metrics
(base rate = 29/1372 = **2.11%**). Verdicts are from the locked single-pool
re-anchor; usability metrics are actionability-layer, base-rate framed (a low
PPV at a 2% base rate is expected even for a good signal).

| signal | construct | single-pool verdict | sensitivity | specificity | lift |
|---|---|---|---:|---:|---:|
| **HA07d** | sleep-stress variability (stdev delta) | **SUPPORTED** | 88.0% | 31.7% | 1.28x |
| HA11 | within-day U-dip count | NOT-SUPPORTED | 58.3% | 58.5% | 1.39x |
| HA06b | resting-HR z-score | NOT-SUPPORTED | 61.5% | 45.1% | 1.12x |
| HA07c | sleep-stress mean delta | NOT-SUPPORTED | 60.0% | 50.8% | 1.21x |
| HA01b | exertion-class lead-up | NOT-SUPPORTED | 82.1% | 23.0% | 1.06x |
| HA10 | morning body-battery peak z | NOT-SUPPORTED | 76.9% | 27.1% | 1.05x |
| H02b | per-minute stress-spike count | NOT-SUPPORTED | 50.0% | 53.5% | 1.07x |

**The honest headline:** of seven pre-registered scorecard signals, **one
(HA07d) is single-pool SUPPORTED**; the other six are NOT-SUPPORTED. That is
the un-spun score, and publishing it is the point. Usability (sensitivity,
lift) and reality (the verdict) are different axes: a NOT-SUPPORTED signal can
still have non-trivial recall, and a SUPPORTED one still has a low PPV at a 2%
base rate.

## 4. The un-abridged record (links out)

The full closed-hypothesis ledger, with per-hypothesis pre-registration,
method, statistics, and caveats, is in the research repository (beyond the
seven scorecard signals: H01-H05, K01-K02, HA01c, HA07c/d, HA08c, HA10, HA11,
HA-C3/C4, HA-P6/P7, and more):

- **Hypothesis registry:** `docs/research/analyses/hypotheses/registry.md`
  (the full ledger) + per-hypothesis folders (`hypothesis.md` / `test.py` /
  `result.md`).
- **Methodology:** `docs/research/methodology/` (the pre-registration
  discipline, the single-pool reframe `train_validate_split_fate.md`, the null
  and block-length choices, the confounder framework).
- **Reviews:** `docs/research/reviews/` (the fresh-session peer reviews).
- **Conventions:** `docs/research/CONVENTIONS.md` (the role split, the rigor
  gates).

The site wires the actual GitHub URL for this repo into the `/workings`
layer; the paths above are stable within it.

## 5. Caveats

- **n=1 throughout.** Every statistic is one person's data; the CIs are wide
  (29 crashes) and are reported, not hidden. Nothing here generalises beyond
  this body.
- **Single-pool is the primary framing;** the retired train/validate contrast
  survives only as a descriptive overlay (a number, not a narrative).
- Usability metrics (PPV, lift) are life-usability measures, base-rate framed,
  and are NOT the hypothesis verdict (which is the discrimination test).

## 6. Cross-references

- Register R8 (research-layer package) + R2 (trust panel, the usability
  source) + R14 (single-pool verdicts).
- [`trust-panel-export.md`](trust-panel-export.md) (the full single-pool trust
  table with CIs).
- `docs/research/analyses/hypotheses/registry.md` (the full ledger).
