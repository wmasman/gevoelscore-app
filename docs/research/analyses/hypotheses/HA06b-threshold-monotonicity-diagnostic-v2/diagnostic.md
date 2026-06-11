# HA06b threshold-monotonicity diagnostic v2

**Pre-registration locked 2026-06-07** per the user-locked Option C
tightened. HA06b had **no v1 diagnostic**; v2 is the first
threshold-monotonicity diagnostic applied to HA06b. Locked
symmetrically with HA10, HA07d, HA11 v2 diagnostics to prevent
selective application.

**Criteria source**: [v2 methodology document](../../methodology/threshold-sweep-rescue-criteria-v2.md).

## 1. What this diagnostic evaluates

**Test under diagnostic**: HA06b (nightly RHR z-score against
lagged baseline; locked train SUPPORTED at primary 4d
bidirectional N_std=1.5 +18.9 pp; validate refuted).

**v2 question**: Under the v2 five-category shape rule, does
HA06b's train bidirectional primary arm fall into a PASS category
or a FAIL category?

Validate-era is evaluated descriptively (refuted at v1 primary;
the diagnostic shape may inform whether the refutation is robust
across thresholds or is itself threshold-tier-specific).

## 2. Data sources and machinery

Same as HA06b test: morning nightly RHR from Garmin UDS
`restingHeartRate` field; 1722 valid days; lagged baseline
[d-90, d-30]; 4d primary; null sample seed `20260605`.

Fine N_std grid: [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5,
2.75, 3.0, 3.5, 4.0] — same 13-tier grid as HA10/HA07d v1
diagnostics.

The HA06b v2 diagnostic **requires running the test machinery on
the fine grid** (HA06b's locked result.md only reports 1.5/2.0/2.5
tiers). New computation, not just re-reading existing data.

## 3. v2 verdict logic

Apply [v2 methodology §3](../../methodology/threshold-sweep-rescue-criteria-v2.md#3-the-five-category-shape-rule)
to HA06b's TRAIN bidirectional primary curve. RESCUE / CLOSE /
AMBIGUOUS verdict.

Validate curve also computed and reported in result-data.json
for descriptive completeness; v2 verdict applies to train only
(matching where the locked SUPPORTED verdict is).

## 4. Test-specific notes

- HA06b is the **third autonomic-channel test** to undergo v2
  diagnostic. If HA06b train RESCUES, the train-era multi-channel
  convergence narrative is strengthened (RHR z-score holds as
  load-bearing alongside whatever HA10 / HA07d / HA11 v2 produce).
- HA06b's locked SUPPORTED verdict at +18.9 pp train remains on
  record regardless of v2 outcome.
- Symmetric application: HA06b cannot be exempt from v2 diagnostic
  just because it wasn't in the original v1 round. The peer-review
  channel-independence critique flagged that HA06b shares
  underlying physiology with HA07d et al.; the diagnostic
  framework must apply equally.

## 5. Pre-registered restoration / demotion actions

### If train RESCUE under v2

- HA06b train confirms as load-bearing finding for the
  pre-cliff autonomic-deviation precursor signature.
- Six-channel train convergence narrative stays with HA06b
  intact.
- Card (b) train-era retrospective keeps HA06b as one of its
  anchors.

### If train CLOSE under v2

- HA06b train SUPPORTED verdict stays on record but synthesis-
  level framing demotes to non-load-bearing.
- Train-era six-channel narrative weakens; "five channels" if
  HA07d also closes train v2.
- Methodology lesson: v2 was applied symmetrically; HA06b
  doesn't get to be load-bearing just because it wasn't
  previously diagnosed.

### If validate descriptive arm

- Reported in result.md as supplementary.
- No verdict impact (HA06b validate was refuted at v1 primary;
  v2 cannot RESCUE a refuted test, only confirm/deny shape
  robustness of the refutation).

## 6. Outputs

- `result-data.json` — fine-grid discrimination table per era +
  direction; shape category match; train v2 verdict.
- `result.md` — verdict statement, synthesis-framing
  implications.

Result.md produced after ALL FOUR v2 diagnostics run.

---

*Locked 2026-06-07. First v2 diagnostic on HA06b. Symmetric
application with HA10 / HA07d / HA11 v2 diagnostics enforced.*
