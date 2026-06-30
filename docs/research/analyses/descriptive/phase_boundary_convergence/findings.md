# Findings -- phase-boundary convergent-validity status (R27 assemble)

**Strand**: site-assemble (Wiggers page). Producer-mode assemble (NOT a re-run) of the
already-landed Q4.3 `era_boundaries` analysis into a date-free, per-boundary
convergent-validity note for the public Wiggers site.

**Question R27 answers**: do the lived recovery-phase boundaries (defined in
`lc_recovery_phase_axis.md`, **never tuned to the watch data**) show up in the Garmin watch
data without being tuned to it?

**Scope**: the 6 lived recovery-phase boundaries only (rp1-rp6 per
`lc_recovery_phase_axis.md` sec 2). The 5 citalopram-phase boundaries + 1 retired
2023-12-31 train/validate split from the Q4.3 source are NOT part of this convergence note
(they are intervention/historical boundaries, not lived recovery-phase boundaries).

---

## THE DISCLAIMER (binding; must travel with any site use of this material)

**The lived recovery-phase boundaries were NOT derived from the watch data.** They are
**M1 lived-experience boundaries** (and, for the first two, data-given clinical events):
fixed from the lived recovery story and documented clinical/intervention events
*before* any watch channel was looked at, and locked in
[`lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) (r2 LOCKED
2026-06-19). Per that MD sec 5.1, the only "duration rule" boundary (rp4 at 8 weeks
post-ergotherapie-start) is anchored to a documented event + a duration *named in the lived
report* -- never extracted from a Garmin channel.

This note reports **descriptive convergent validity ONLY**: it asks whether those
independently-fixed lived boundaries *happen to* coincide with shifts in the watch data.
A boundary that converges is **corroboration**, not derivation. A boundary that does **not**
converge (a "quiet seam") is an **allowed, honest outcome** -- a lived change that left no
watch signature is still a real lived change. Nothing in this note may be read, or presented
on the site, as a claim that the boundaries were found in, tuned to, or chosen because of the
data.

Source of all numbers below:
[`trajectory/era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md)
sec 2 (per-boundary distribution-shift) + sec 5 (per-recovery-phase-boundary defensibility),
user-LOCKED operationalisation per Strand B sec 7c interview 2026-06-25.

---

## Headline line for the page

**Five of the six lived recovery-phase boundaries -- fixed from the recovery story, never
from the watch -- independently show up as shifts in the Garmin data; the sixth is too
recent to read.**

(Alternative shorter form, if the page needs one line:
*"The recovery phases were drawn from lived experience, not the watch -- yet five of six
boundaries surface in the watch data on their own."*)

---

## Per-boundary convergence table

Convergence call per boundary (date-free; the lived label, not the date, is the unit the site
shows). Read = Stage 2 multi-channel distribution-shift (n channels with shift / n tested) +
Stage 5 data-driven change-point confirmation (n channels with an independent change-point
within +-21d).

| boundary_id | lived transition | converges | note |
|---|---|---|---|
| `rp1_pre_illness_to_acute` | pre-illness health -> acute infection | **yes** | Strong multi-channel shift (4 of 6 channels). The body's autonomic-load signals move sharply as the infection begins -- the watch sees the start of illness on its own. |
| `rp2_acute_to_lc_pre_ergo` | acute infection -> Long COVID settling in | **yes** | Strong multi-channel shift (4 of 6 channels), with independent change-points landing on the seam on 4 of 7 channels. The transition into the chronic phase is visible in the data. |
| `rp3_lc_pre_ergo_to_4a` | before pacing -> learning to pace (ergotherapy starts) | **yes** | Multi-channel shift (4 of 7 channels); 3 channels show an independent change-point near the seam. The onset of pacing practice coincides with a readable shift. |
| `rp4_4a_to_4b` | learning to pace -> pacing habit established | **yes** | Multi-channel shift (4 of 7 channels); 4 channels confirm independently. This is the boundary the prior resting-HR finding flagged (a clear, narrow heart-rate shift); the broader read reproduces and extends it. The single most-corroborated lived seam. |
| `rp5_4b_to_citalopram_modulated` | pacing habit -> medication era begins | **yes** (with caveat) | Strongest shift of all (5 of 7 channels; 5 confirm independently). CAVEAT: this date coincides with the start of citalopram (and sits days from a CPAP-end event), so the watch shift is NOT attributable to the lived pacing-to-medication transition alone -- it is a genuine seam in the data, but a confounded one. Honest convergence, ambiguous cause. |
| `rp6_citalopram_modulated_to_post_afbouw` | medication era -> post-taper | **quiet / unread** | NOT finalized. This boundary (2026-06-06) is 2 days after the data corpus ends (2026-06-04), so there were zero post-boundary days to test. No convergence read exists; this is unread, not a quiet seam in the honest sense and not a failure -- there is simply no data yet. Refresh when post-taper data accrues. |

**Tally**: 5 converges = **yes** (one of those, rp5, flagged with a confound caveat) /
0 = **partial** / 1 = **quiet-unread** (rp6, out-of-corpus, never finalized).

No boundary in this set is a true "quiet seam" (a lived change tested against data and found
silent). The only non-converging boundary, rp6, is **unread for lack of data**, not silent.
Per the guardrail, it is marked quiet/unread rather than given an invented convergence call.

---

## Which boundaries lack a finalized convergence read

- **rp6 (`citalopram_modulated_to_post_afbouw`, 2026-06-06)**: convergence was **never
  finalized** in the Q4.3 source. The boundary is out-of-corpus (2 days past the
  2026-06-04 data end), so Stage 2 returned `n_post = 0` and the per-cell tests skipped
  (Q4.3 `findings.md` sec 2 row rp6 = `0 / 0`; sec 5 = `0 / 0` and `0 / 7`; Limitation 8).
  It is included in the lived 6-phase scope but carries no watch read. Marked **quiet/unread**
  here per the R27 guardrail.

All other five lived boundaries (rp1-rp5) have a finalized, multi-channel convergence read in
the Q4.3 source.

---

## Provenance / citations (file:line into the Q4.3 source)

All reads assembled from the locked Q4.3 artefact; no re-computation performed.

- Per-boundary distribution-shift table (rp1-rp6 rows):
  [`trajectory/era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md):65-70
  (sec 2 multi-channel synthesis).
- Per-recovery-phase-boundary defensibility chart (Stage 2 shift + Stage 4 confirming):
  [`trajectory/era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md):258-263
  (sec 5).
- rp4 load-bearing resting-HR reproduce/extend note (the +3.0 bpm CI [+2.0,+4.0] prior
  finding): [`trajectory/era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md):95
  + sec 6 LOAD-BEARING cross-references line 282.
- rp5 / 2024-04 boundary-collision caveat (citalopram-start + CPAP-end coincide):
  [`trajectory/era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md):71
  (cp1 row, same 2024-04-09 date) + `lc_recovery_phase_axis.md` sec 3.6 (boundary collision).
- rp6 out-of-corpus / unread status:
  [`trajectory/era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md):70,263,314
  (sec 2 + sec 5 zero rows + Limitation 8).
- "boundaries are lived M1, never data-tuned" framing:
  [`trajectory/era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md):7
  (CRITICAL USER FRAMING) + [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md):109-159
  (sec 3.3-3.4 M1 lived-experience warrants) + :201 (sec 5.1 M1 carve-out, duration named in
  lived report not extracted from a channel).
- Convergent-validity-not-derivation discipline:
  [`trajectory/era_boundaries/findings.md`](../trajectory/era_boundaries/findings.md):307-308
  (Limitations 1-2: no "boundary unjustified" / no "data-driven candidate is a better
  boundary" claims).

---

## Guardrail compliance (this assemble)

1. **Descriptive convergent validity only** -- no claim, anywhere, that boundaries were
   derived from data. The disclaimer block is binding and must travel with the material.
2. **A quiet seam is honest, not a failure** -- stated explicitly; rp6 is marked quiet/unread
   (lack of data), not failed.
3. **No invention** -- rp6's missing convergence read is reported as "never finalized,"
   not filled with a fabricated call.
4. **Assemble, not re-run** -- every number traces to a Q4.3 `findings.md` line; nothing was
   recomputed.
5. **No site repo / locked result.md touched**; no push/git/audit performed.

---

*Assembled 2026-06-30 (R27) in producer-mode from the LOCKED Q4.3 `era_boundaries` artefact.
Date-free per-boundary convergence note for the Wiggers site. No data recomputation; no
methodology-MD or HA-artefact modification; no push/audit.*
