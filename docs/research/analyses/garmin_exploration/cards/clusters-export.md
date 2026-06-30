# Clusters export — R25 site artefact (inter-signal structure)

**Producer-mode export artefact.** Assembles the channel×channel correlation matrix, the derived effective-N, and the per-signal cluster status into the export-shaped object feeding the site's `data/clusters.json`. Read-only on existing results; this card writes nothing back into them.

**Request**: R25 ("the export behind 'seven signals collapse to one factor'") per [`_rollout_order_site_delivery_2026-06-30.md:96`](../../../methodology/_rollout_order_site_delivery_2026-06-30.md). Wave-1 (trust + structure exports).

**Single source**: [`cross-channel-correlation.md`](cross-channel-correlation.md) — computed 2026-06-08, analysis window 2022-09-03 → 2026-06-05. The matrix + effective-N + cluster assignments below are lifted from that card; citations are by `file:line` against it.

**Scope boundary**: R25 is INTER-signal structure (channel×channel coherence + effective independent-count + cluster membership). It is NOT R2 (per-signal trust metrics). The site's `data/clusters.json` carries structure only; trust lives in a sibling export.

> The cohort-topology factor definition was sought: [`descriptive/trajectory/cohort_topology/findings.md`](../../descriptive/trajectory/cohort_topology/findings.md) is event-topology + recovery-window work (crash/dip geometry), NOT the inter-signal factor definition. There is no separate `cohort_topology` factor doc to fold in; the cross-channel card is the whole factor substrate for R25.

---

## 1. HONESTY GUARDRAIL (load-bearing — read before using this export)

**The collapse IS the finding.** A fuller-looking 7×7 matrix must NOT be read as seven independent witnesses. The headline the site must carry:

> **Coherence + grading, NOT seven independent witnesses.** The seven per-day primitives behind "seven train-era SUPPORTED on six channels" represent roughly **3–4 effectively independent signal clusters**, not seven.

Two collapses are exact and must survive any rendering of this export — do not let downstream presentation re-inflate the channel count:

- **H02b ≡ H02d** (Spearman ρ = +1.000, Pearson r = +1.000). The 1737 shared valid days carry identical `max_spike_minutes`; H02d's discrimination edge comes entirely from window-length + validity rules, not a distinct signal. H02d is the SAME primitive at a different window. ([`cross-channel-correlation.md:7`](cross-channel-correlation.md), [`:48-49`](cross-channel-correlation.md)).
- **HA10 ≡ −HA07c** (Spearman ρ = −0.922, Pearson r = −0.863). Morning BB peak and sleep stress mean are the same autonomic-state signal in opposite sign — structural in Garmin's BB algorithm (BB falls when stress rises). NOT independent channels. ([`cross-channel-correlation.md:9`](cross-channel-correlation.md), [`:52-54`](cross-channel-correlation.md)).

Consequence for multi-comparison: effective N ≈ 3–4 ⇒ honest Bonferroni α ≈ 0.05/4 ≈ 0.0125 (not 0.05/11 ≈ 0.0045). H02d/H02b is the only primary verdict that survives an honest effective-N correction, and the H02b/H02d collinearity means it counts as one finding ([`cross-channel-correlation.md:23`](cross-channel-correlation.md)). **The site copy must say "graded coherence among a few signals", never "seven agreeing signals".**

---

## 2. Assembled matrix (Spearman ρ — primary; monotonic)

Source: [`cross-channel-correlation.md:46-54`](cross-channel-correlation.md). Per-day raw primitives, inner-joined on calendar date within 2022-09-03 → 2026-06-05, min N=30 per pair.

| | H02b | H02d | HA11 | HA06b | HA07c | HA07d | HA10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **H02b** (max_spike_min) | 1.000 | +1.000 | +0.377 | -0.005 | -0.045 | +0.048 | +0.047 |
| **H02d** (bridge_spike_min) | +1.000 | 1.000 | +0.377 | -0.005 | -0.045 | +0.048 | +0.047 |
| **HA11** (u_dip_count) | +0.377 | +0.377 | 1.000 | +0.047 | +0.054 | +0.073 | -0.084 |
| **HA06b** (resting_hr_bpm) | -0.005 | -0.005 | +0.047 | 1.000 | +0.377 | +0.073 | -0.393 |
| **HA07c** (sleep_stress_mean) | -0.045 | -0.045 | +0.054 | +0.377 | 1.000 | +0.501 | -0.922 |
| **HA07d** (sleep_stress_stdev) | +0.048 | +0.048 | +0.073 | +0.073 | +0.501 | 1.000 | -0.366 |
| **HA10** (morning_bb_peak) | +0.047 | +0.047 | -0.084 | -0.393 | -0.922 | -0.366 | 1.000 |

**Pearson r matrix** (linear — secondary, ship for completeness): [`cross-channel-correlation.md:58-66`](cross-channel-correlation.md). Same shape; key cells H02b≡H02d r=+1.000, HA10≡−HA07c r=−0.863, HA07c↔HA07d r=+0.602.

**Pairwise N** (intersection of valid days, range 1334–1365): [`cross-channel-correlation.md:70-78`](cross-channel-correlation.md). All cells N≥1334 — every pairwise estimate is on >1300 days, far above the N=30 floor.

**Mean |ρ| per channel** (centrality — high = shares variance with many): HA07c 0.324 and HA10 0.310 are central; H02b/H02d 0.254; HA07d 0.185; HA11 0.169; HA06b 0.150 ([`cross-channel-correlation.md:84-92`](cross-channel-correlation.md)).

---

## 3. Effective-N

**Effective independent channel count ≈ 3–4** (vs nominal 7 primitives / "six channels") ([`cross-channel-correlation.md:17`](cross-channel-correlation.md)).

Cluster decomposition ([`cross-channel-correlation.md:18-21`](cross-channel-correlation.md)):

- **Cluster 1 — within-day stress**: H02b / H02d + HA11 (H02b↔HA11 ρ ≈ +0.38).
- **Cluster 2 — autonomic state**: HA07c + HA10 (ρ ≈ −0.92) ± HA06b (ρ ≈ +0.36 to −0.39).
- **Cluster 3 — autonomic variability**: HA07d (tied to Cluster 2 via HA07c at +0.50; moderate, treated as a distinct facet — level vs variability).
- HA08c (omitted as a row) is a trailing-5-day OLS slope of HA07c's primitive, adds little independent variance ([`cross-channel-correlation.md:21`](cross-channel-correlation.md), [`:32`](cross-channel-correlation.md)).

**effective_N = 3** (conservative; HA07d folded toward Cluster 2) **to 4** (HA07d as its own thin cluster). Site should ship the range `3–4`, not a false-precise single integer.

---

## 4. Per-signal cluster status

| channel | primitive | cluster_id | cluster_status | note |
|---|---|---|---|---|
| H02b | max_spike_min | C1 | primary | within-day stress; Cluster-1 anchor |
| H02d | bridge_spike_min | C1 | redundant (≡ H02b, ρ=1.00) | NOT a separate witness; same primitive, different window ([`:7`](cross-channel-correlation.md)) |
| HA11 | u_dip_count | C1 | member | ρ≈+0.38 to H02b; related-but-distinct within-day stress |
| HA06b | resting_hr_bpm | C2 | peripheral | ρ≈+0.36/−0.39 to Cluster-2 core; most independent (mean \|ρ\|=0.150) |
| HA07c | sleep_stress_mean | C2 | primary | Cluster-2 anchor; central (mean \|ρ\|=0.324) |
| HA10 | morning_bb_peak | C2 | redundant (≡ −HA07c, ρ=−0.92) | same autonomic signal, opposite sign; structural in BB algorithm ([`:9`](cross-channel-correlation.md)) |
| HA07d | sleep_stress_stdev | C3 | member (Cluster-2-adjacent) | ρ=+0.50 to HA07c; level-vs-variability facet |
| HA08c | (slope of HA07c) | C2 | derived (omitted as row) | trailing OLS slope of HA07c; no independent variance ([`:32`](cross-channel-correlation.md)) |

`cluster_status` vocabulary: `primary` (cluster anchor) · `member` (distinct contributor) · `peripheral` (weak/cross-cluster tie) · `redundant` (collapses onto an anchor — count once) · `derived` (transform of an anchor).

---

## 5. Proposed `data/clusters.json` shape

```json
{
  "request_id": "R25",
  "title": "Inter-signal structure: coherence and grading, not seven witnesses",
  "analysis_window": { "start": "2022-09-03", "end": "2026-06-05" },
  "computed": "2026-06-08",
  "source_card": "docs/research/analyses/garmin_exploration/cards/cross-channel-correlation.md",
  "effective_N": { "low": 3, "high": 4, "nominal_channels": 7 },
  "matrix": {
    "method_primary": "spearman",
    "method_secondary": "pearson",
    "channels": ["H02b", "H02d", "HA11", "HA06b", "HA07c", "HA07d", "HA10"],
    "spearman": [
      [1.000, 1.000, 0.377, -0.005, -0.045, 0.048, 0.047],
      [1.000, 1.000, 0.377, -0.005, -0.045, 0.048, 0.047],
      [0.377, 0.377, 1.000, 0.047, 0.054, 0.073, -0.084],
      [-0.005, -0.005, 0.047, 1.000, 0.377, 0.073, -0.393],
      [-0.045, -0.045, 0.054, 0.377, 1.000, 0.501, -0.922],
      [0.048, 0.048, 0.073, 0.073, 0.501, 1.000, -0.366],
      [0.047, 0.047, -0.084, -0.393, -0.922, -0.366, 1.000]
    ],
    "pairwise_n_min": 1334,
    "pairwise_n_max": 1365
  },
  "collapses": [
    { "pair": ["H02b", "H02d"], "rho": 1.00, "kind": "identity",
      "note": "same primitive, different window/validity rules" },
    { "pair": ["HA10", "HA07c"], "rho": -0.92, "kind": "sign-flip-identity",
      "note": "morning BB peak is -1 * autonomic stress; structural in Garmin BB" }
  ],
  "clusters": [
    { "cluster_id": "C1", "label": "within-day stress",
      "members": ["H02b", "HA11"], "redundant": ["H02d"] },
    { "cluster_id": "C2", "label": "autonomic state",
      "members": ["HA07c"], "peripheral": ["HA06b"], "redundant": ["HA10"],
      "derived": ["HA08c"] },
    { "cluster_id": "C3", "label": "autonomic variability",
      "members": ["HA07d"], "adjacent_to": "C2" }
  ],
  "per_signal": [
    { "channel": "H02b",  "primitive": "max_spike_min",     "cluster_id": "C1", "cluster_status": "primary" },
    { "channel": "H02d",  "primitive": "bridge_spike_min",  "cluster_id": "C1", "cluster_status": "redundant" },
    { "channel": "HA11",  "primitive": "u_dip_count",       "cluster_id": "C1", "cluster_status": "member" },
    { "channel": "HA06b", "primitive": "resting_hr_bpm",    "cluster_id": "C2", "cluster_status": "peripheral" },
    { "channel": "HA07c", "primitive": "sleep_stress_mean", "cluster_id": "C2", "cluster_status": "primary" },
    { "channel": "HA10",  "primitive": "morning_bb_peak",   "cluster_id": "C2", "cluster_status": "redundant" },
    { "channel": "HA07d", "primitive": "sleep_stress_stdev","cluster_id": "C3", "cluster_status": "member" },
    { "channel": "HA08c", "primitive": "sleep_stress_slope","cluster_id": "C2", "cluster_status": "derived" }
  ],
  "headline": "coherence + grading, not seven independent witnesses"
}
```

The Pearson array is omitted from the snippet for brevity; ship it as a sibling `pearson` field with the same shape ([`cross-channel-correlation.md:58-66`](cross-channel-correlation.md)).

---

## 6. Privacy statement (stated; not script-run — user gates the audit)

This export carries **aggregated correlation coefficients, day-count integers, and categorical cluster labels only**. Specifically:

- **No dated values.** The only dates present are the two analysis-window endpoints (2022-09-03, 2026-06-05) and the compute date (2026-06-08) — boundary metadata, not observations.
- **No per-day series.** The per-day raw primitives that the correlations were computed FROM are not in this artefact; only the correlation reductions over them are.
- **No raw biometrics.** No HR/HRV/stress/BB values, no gevoelscore values, no per-event rows.
- **Counts are corpus-level aggregates** (pairwise N 1334–1365; per-primitive day counts 1339–1365) — they reveal coverage, not content.

Conclusion: **R25 is privacy-safe for the site as assembled.** Nothing here is dated-raw or per-day reconstructable. (The user gates `audit_for_publication.py`; this is the producer's pre-statement, not a substitute for that run.)

---

## 7. Analysis window + Stratum-4 recommendation

**Window the matrix was computed on**: 2022-09-03 → 2026-06-05 (full gevoelscore-corpus span), n per pair 1334–1365 valid days ([`cross-channel-correlation.md:28`](cross-channel-correlation.md), [`:70-78`](cross-channel-correlation.md)).

**Recommendation: a Stratum-4-only re-confirmation is NOT needed for R25. The existing full-window matrix is acceptable for the site.** Reasoning:

1. **R25 measures inter-signal biological/structural co-variation, not crash discrimination.** Stratum-4 (the single-pool n=29 crashes substrate per [`single_pool_reanchor/findings.md`](../../descriptive/operationalisation_support/single_pool_reanchor/findings.md)) is the crash-event stratification used to re-anchor *discrimination* verdicts (R2-class trust). The two collapses (H02b≡H02d, HA10≡−HA07c) are properties of the per-day signal algebra and Garmin's BB construction — they do not change under a crash-conditioned subset; they are structural, not discrimination-dependent.
2. **The estimates are already on >1300 days per pair.** A Stratum-4 restriction (n=29 event windows) would shrink N by ~50× and widen every CI, *weakening* the structural read for no gain in validity. The full-window estimate is the correct denominator for "are these signals the same underlying thing".
3. **The load-bearing collapses are near-degenerate** (ρ=1.00 exact; ρ=−0.92). These will not flip on any reasonable subset; re-running on Stratum-4 risks introducing subset noise into a finding that is presently clean.

**Caveat to carry, not block on**: the matrix is unstratified across recovery phases / citalopram eras. If the site ever claims the cluster *structure* is invariant across eras, that needs a per-phase re-computation (a genuinely uncovered run — see §8). For the R25 headline as scoped ("seven collapse to ~3–4"), the pooled full-window matrix is sufficient and is the honest denominator.

The rollout note's "re-confirm Stratum-4" flag ([`:96`](../../../methodology/_rollout_order_site_delivery_2026-06-30.md), [`:125`](../../../methodology/_rollout_order_site_delivery_2026-06-30.md)) is best read as **"confirm R25 doesn't silently inherit a stale split"** — it doesn't, because the matrix was never split-conditioned. Mark the flag **resolved: not-applicable (structural finding, full-window correct)**, pending user concurrence.

---

## 8. Open questions (anything needing fresh computation)

1. **Per-phase / per-era cluster-structure invariance** (NOT computed). The matrix is pooled across recovery phases + citalopram eras. If the site asserts the 3–4-cluster structure is era-stable, a per-phase re-computation of the 7×7 is required. Recommend: do NOT claim invariance on the site without it; ship the pooled structure with a "computed across the full window" caveat. *(Fresh run.)*
2. **HA08c numeric correlation row** (omitted by design). HA08c is asserted ≡ HA07c at the raw-primitive level ([`:32`](cross-channel-correlation.md)) but no explicit ρ row exists in the source card. If the site renders HA08c as `derived`, that is supported by construction; if it ever needs a printed coefficient, that cell must be computed. *(Fresh run, low priority.)*
3. **CI / significance on the correlation cells** (not in source card). The card reports point ρ/r and N but no per-cell CI. For the two load-bearing collapses this is moot (degenerate), but if the site renders the moderate cells (ρ≈0.38, 0.50) as graded ties, a bootstrap CI per cell would harden them. *(Fresh run, optional.)*
4. **Reconciliation of "six channels" vs "seven primitives" labelling** (editorial, not compute). Source card uses both "six channels / seven SUPPORTED tests" and a 7-primitive matrix. The site copy must pick one frame and state the H02d/H08c collapses explicitly so the count is never ambiguous. *(No compute; copy discipline.)*

---

*Producer-mode assembly. No new analysis run; all numbers lifted from [`cross-channel-correlation.md`](cross-channel-correlation.md) (computed 2026-06-08). Does not modify the source card or any locked artefact. Audit gated to user.*
