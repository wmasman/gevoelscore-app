# Methodology review — external_contextualisation.md r2 → r3 diff (2026-06-26)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the r2→r3 drafting session. Fresh session — no exposure to the drafting context; doc-only knowledge.
**Target**: [`docs/research/methodology/external_contextualisation.md`](../methodology/external_contextualisation.md) r3 DRAFT (status header + NEW §4.3.5 + §4.4 lead-in cross-reference + NEW §7.13 + §11 r3 lock-log entry).
**Scope**: r2 → r3 diff only. The r2 LOCKED baseline was reviewed and accepted at [`methodology-external_contextualisation-2026-06-24.md`](methodology-external_contextualisation-2026-06-24.md); re-reviewing r2 sections is out of scope.
**Review date**: 2026-06-26
**Standards applied**: [CONVENTIONS](../CONVENTIONS.md) §1.2, §2.1, §2.2; [plan](../methodology/_plan_results_analysis_layer.md) r5 §3.5, §3.6; [limitations doc](../methodology/research_line_limitations.md) r3 L3; [`research-interpret` SKILL.md](../../../.claude/skills/research-interpret/SKILL.md) r4 LOCKED 2026-06-25 (dispatch-mode placeholder vocabulary); [internal_synthesis](../methodology/internal_synthesis.md) r2 LOCKED §4.4 (default-on-ambiguity analogue); [descriptive_precondition_audit](../methodology/descriptive_precondition_audit.md) r2 LOCKED (Stage D scope check); [wiggers_testable_hypotheses.md](../wiggers_testable_hypotheses.md) §C C3 verbatim; [topic-stress-fatigue-pacing.md](../analyses/contextualisation/topic-stress-fatigue-pacing.md) LOCKED-r1 §4.4 + §4.8(b) (the miss to be prevented).

---

## 1. Overall verdict

**REVISION RECOMMENDED (mild).** The r2→r3 diff is methodologically sound and operationally implementable. §4.3.5 is the right discrete step at the right place; the §4.4 lead-in correctly constrains the Measurement fault-line list per §4.3.5 verdict; §7.13 is correctly pointer-style and routes cleanly back to §4.3.5. The worked-example claim that Wiggers's "stress score" = Garmin Connect Annual Stress Scores UI metric is warranted by the §C C3 verbatim. The interpolated-not-renumbered placement is correct given LOCKED-r2 downstream cross-references. Three findings drive REVISION RECOMMENDED rather than ACCEPT: one required (R1, dispatch-mode placeholder vocabulary inconsistency with SKILL.md r4), two recommended (A1, default-on-ambiguity divergence from §4.4 internal_synthesis analogue invites one sentence of explicit rationale; A2, L3 stretch on Firstbeat algorithm-version + population-calibration warrants a one-sentence flag for whether this is an L3-expansion or an L8-addition decision). None blocks user acceptance of r3; all three are one-revision-cycle fixes.

## 2. Summary of findings

| ID | Type | Section | Severity | One-line |
|---|---|---|---|---|
| R1 | REQUIRED | §4.3.5 Dispatch-mode placeholders | Mild | Invented `LITERATURE-GAP-FROM-§4.3` and `PROXY-CITED-USER-ACCEPTED-{date}` names diverge from SKILL.md r4's locked `LITERATURE-GAP` / `PROXY-CITED-IN-DRY-RUN` vocabulary; either reuse or cross-reference + justify. |
| A1 | RECOMMENDED | §4.3.5 hard rule 2 (default verdict) | Low | Default-to-CONSTRUCT-RELATED contradicts the internal_synthesis §4.4 default-to-CONFLICT discipline (most-conservative-divergence-preserving label); the choice may be right but warrants one sentence of explicit divergence-rationale. |
| A2 | RECOMMENDED | §4.3.5 worked example (L3 attribution) | Low | "Firstbeat algorithm-version drift" + "population-Firstbeat-calibration" fall under L3's "underlying algorithm updates" + "calibration drift" framing literally but stretch L3's intended within-vendor scope; flag whether this is an L3 expansion or an L8-addition decision for the limitations-doc maintainer. |

## 3. Required findings

### R1 — Dispatch-mode placeholder vocabulary diverges from SKILL.md r4

**(a) What's wrong.** §4.3.5's "Dispatch-mode placeholders" subsection invokes four placeholder names:

- `LITERATURE-GAP-FROM-§4.3` — invented (not in SKILL.md).
- `PROXY-CITED-USER-ACCEPTED-{date}` — invented (SKILL.md defines `PROXY-CITED-IN-DRY-RUN` for the proxy-cite case).
- `DEFAULTED-PENDING-USER-INPUT` — matches SKILL.md.
- `SKIPPED-AS-DRY-RUN-DEFAULT` — matches SKILL.md (correctly disallowed at §4.3.5).

SKILL.md r4 LOCKED 2026-06-25 names exactly four dispatch-mode placeholders (`DEFAULTED-PENDING-USER-INPUT`, `SKIPPED-AS-DRY-RUN-DEFAULT`, `DEFAULTED-TO-PRESERVE-PENDING-USER-INPUT`, `DRAFT-ON-DRAFT-DRY-RUN`) and one stage-S₂-specific proxy-cite marker (`PROXY-CITED-IN-DRY-RUN`) — the locked dispatch-mode vocabulary. §4.3.5's two invented names are not in that vocabulary.

**(b) Why it matters.** SKILL.md is the binding dispatch-mode framework cited verbatim in the §4.3.5 lead-in sentence ("consistent with ... the [`/research-interpret`](../../.claude/skills/research-interpret/SKILL.md) dispatch-mode framework"). Inventing two new placeholder names breaks the consistency claim — a future drafter following §4.3.5 will emit placeholders that the skill's gates do not recognise, and a future SKILL.md change will not propagate to §4.3.5. The §4.3.5 dispatch-mode framing reads as "this is the standard vocabulary" while in fact introducing two non-standard names.

**(c) Proposed fix.** Either:
- **Option α** (reuse the locked vocabulary): rename `LITERATURE-GAP-FROM-§4.3` to `LITERATURE-GAP` (the existing §4.3 fourth-label status; §4.3.5 inherits the upstream label rather than creating a derivative), and rename `PROXY-CITED-USER-ACCEPTED-{date}` to `PROXY-CITED-IN-DRY-RUN` (the SKILL.md-defined name) with the `{date}` provenance moved into the placeholder's accompanying one-sentence cite. Cleanest.
- **Option β** (justify the divergence): add a sentence explaining why §4.3.5 needs two distinct placeholder names beyond SKILL.md's vocabulary (e.g., "register-anchor-verification provenance is distinct from in-dry-run proxy-citation"), and propose adding them to SKILL.md as a future amendment so the vocabulary remains a single source of truth.

Option α is preferred because the substantive content of the two invented names is captured by the existing vocabulary plus a one-sentence cite.

## 4. Recommended findings

### A1 — Default-to-CONSTRUCT-RELATED diverges from internal_synthesis's default-to-CONFLICT analogue

**(a) What's wrong.** §4.3.5 hard rule 2 sets the default-on-ambiguity verdict to CONSTRUCT-RELATED (conservative middle), with the rationale that this "preserves a substrate caveat at §4.4 without asserting the source measures a wholly different construct." The cited analogue is internal_synthesis §4.4's "default to CONFLICT on ambiguity" — but internal_synthesis §4.4 actually defaults to CONFLICT (the most-conservative-divergence-preserving label, not the middle), per the verbatim "If no label fits cleanly, the cluster is CONFLICT (the default-to-preserve discipline)."

The strict analogue at §4.3.5 would be default-to-CONSTRUCT-DIFFERENT (the most-conservative-mismatch-preserving label, parallel to CONFLICT preserving the divergence). §4.3.5 chose a different default and used the "default-to-preserve" language that points to CONFLICT.

**(b) Why it matters.** The hard rule is defensible on the merits — defaulting to CONSTRUCT-DIFFERENT would force a NOT-COMPARABLE on §4.4 Measurement that may itself be a misframing of the ambiguity. The middle default is sound for the construct-identity question specifically because the failure mode the section is designed to prevent (asserting substrate-mismatch on weak inference) cuts both ways: defaulting to CONSTRUCT-DIFFERENT recreates the §7.13 failure mode in the opposite direction. But the rule as written cites an analogue that does not actually behave the way the rule claims — and a future reviewer reading the rule will be left with the design-divergence unexplained.

**(c) Proposed fix.** Add one sentence to hard rule 2 acknowledging the divergence from internal_synthesis §4.4's most-conservative default, e.g.: "Unlike internal_synthesis §4.4's default-to-CONFLICT (the most-conservative-divergence-preserving label), §4.3.5 defaults to CONSTRUCT-RELATED (the middle) because defaulting to CONSTRUCT-DIFFERENT would recreate the §7.13 substrate-mismatch-by-default failure mode in the opposite direction; the substrate-caveat-without-different-construct-assertion compromise is the right resting point for construct-identity ambiguity specifically."

### A2 — L3 attribution stretch in the worked example

**(a) What's wrong.** The worked-example's corrected CONSTRUCT-IDENTICAL verdict enumerates three residual fault-lines under L3:

- device-generation (FR245 vs Wiggers's source-data device pool) — clean L3 fit.
- Firstbeat algorithm-version drift (within-vendor calibration scope) — fits L3 literally per its "underlying algorithm updates can shift the semantics of derived signals" framing, but L3's project-specific-manifestation paragraph names hardware-upgrade scenarios (FR245 → FR255) as the trigger, not within-FR245 firmware/algorithm-version drift.
- population-Firstbeat-calibration (validated in athletes / healthy populations; LC-cohort response may differ) — this is a population-validity-of-vendor-algorithm question that L3 does not explicitly cover; it sits between L3 (signal-meaning device-bound) and a not-yet-existing limitation on vendor-population-calibration.

**(b) Why it matters.** L3 is being asked to cover three semantically distinct fault-lines under one citation. The worked example doesn't flag whether this is an intentional L3-expansion (the limitations-doc maintainer should formalise L3's scope to include intra-vendor algorithm-version drift + vendor-population-calibration) or an ad-hoc stretch that should later become a new L-ID (e.g., L8: vendor-algorithm-population-validity). Either reading is defensible, but the choice is currently silent in the worked example and downstream Stage S₂ artefacts will inherit it.

**(c) Proposed fix.** Add a single sentence to the worked-example's L3 enumeration: "These three sub-issues sit under L3 literally per its 'underlying algorithm updates' + 'calibration drift' framing, but stretch L3 past its hardware-upgrade-triggered project-specific manifestation; whether to expand L3 or add an L8 (vendor-algorithm-population-validity) is flagged to the limitations-doc maintainer as a separate decision." This preserves the worked example without binding the limitations doc to a not-yet-made decision.

## 5. Per-section assessment of the three changes

### §4.3.5 Construct-identity check (new section)

**Sound.** The three-label set covers the operationally distinct cases cleanly — CONSTRUCT-IDENTICAL captures same-construct-same-instrument-family (the failure mode the section closes); CONSTRUCT-RELATED captures related-construct-different-instrument (the canonical substrate-mismatch case); CONSTRUCT-DIFFERENT captures different-construct-under-same-or-similar-name (the inverse failure mode, e.g., source's "HRV" = nightly RMSSD vs project's `stress_mean_sleep` HRV proxy). I cannot identify a fourth distinct case the set misses.

The five-step procedure is mechanically applicable by a Stage S₂ drafter. Step 1 (identify named metrics; skip those the project does not measure) correctly routes unmatched metrics to NOT COMPARABLE at §4.4 without forcing a construct-identity verdict — sound. Step 2 (read source's operational definition or UI/instrument citation) correctly puts the burden on actually-reading-the-source (the §7.13 failure mode prevention). Steps 3-5 are bookkeeping. The procedure's placement of the per-subclaim-per-metric block is the right granularity.

The four hard rules are operationally implementable. Rule 1 (§4.3.5 fires only on CONSENSUS-EXISTS or COMPETING-POSITIONS subclaims) correctly inherits from §4.3 the consensus-existence status; LITERATURE-GAP and CONSENSUS-DOES-NOT-EXIST correctly do not fire because there is no source-side named metric to check. Rule 3 (substrate-mismatch is NOT a default assumption) is the load-bearing rule for the failure mode being closed. Rule 4 (§4.4 Measurement MUST cite §4.3.5 verdict) is the wiring discipline.

R1 + A1 above land on operational refinement, not on the section's substantive correctness.

### §4.4 lead-in cross-reference

**Sound.** The two-sentence lead-in correctly wires §4.3.5's verdict into §4.4's PARTIALLY COMPARABLE fault-line list — substrate-mismatch fault-lines enter only on CONSTRUCT-RELATED or CONSTRUCT-DIFFERENT; CONSTRUCT-IDENTICAL forbids substrate-mismatch in the fault-line enumeration. This is the right constraint: it prevents the §4.4 drafter from re-introducing substrate-mismatch as a fault-line after §4.3.5 has explicitly ruled it out. The lead-in does not duplicate §4.3.5 hard rule 4; it states the §4.4-side of the wiring.

### §7.13 Anti-pattern

**Sound.** The pointer-style brevity (~15 lines) is appropriate — §7.13 is operationally a routing rule ("when §4.4 asserts a substrate fault-line, the corresponding §4.3.5 block must contain the source's instrument-or-UI citation that warrants the verdict") rather than a new substantive failure-mode that needs §7.1-§7.5-style explanatory depth. The depth is consistent with §7.10 (uncited claims floating, ~12 lines) and §7.11 (re-routing in-stage, ~12 lines), both of which are similar routing-rule anti-patterns. The detect-and-route discipline back to §4.3.5 hard rule 3 + procedure step 2 is correct. The 2026-06-26 origin anchor in the §7.13 body is consistent with §7.1-§7.5 worked-example-anchor pattern.

## 6. Worked-example verification (Wiggers stress score = Garmin UI metric)

**Warranted.** I read the §C C3 verbatim in [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) lines 489-496:

> "Your **annual stress overview** includes a **stress score line**. If you've paid attention to your own **stress scores**, you might know that a day with a score of 40 is much more tiring than a day with a score of 30. Such a step appears very small on the graph, but it isn't. This graph shows a kind of stair step. This person has overexerted themselves and their health is deteriorating as a result." (PDF lines 1357-1368, Annual Stress Scores section)

Three independent textual anchors point at Garmin Connect UI:

1. **"annual stress overview"** — the Garmin Connect dashboard's exact UI feature name (Garmin Connect's "Annual Stress" view; not a generic phrase).
2. **"stress score line"** — Garmin's stress dashboard renders the daily stress score as a line graph; the phrasing matches the UI presentation, not a clinical instrument.
3. **"your own stress scores"** — second-person possessive on a wearable-derived auto-computed score; a subjective rating instrument would not be phrased this way, and an external pacing-app dashboard would need a separate name.

The Wiggers handleiding's audience is Long COVID patients using Garmin devices for pacing (the document's broader context, per §C heading "Stress score (Garmin daytime/night, HRV-derived)" in the testable-hypotheses table). Reading "stress score" as a subjective rating without instrument naming is the misreading the §C C3 verification log corrected on 2026-06-12 (USER-VERIFIED-VIA-REGISTER-ANCHOR-VERIFICATION). The CONSTRUCT-IDENTICAL verdict in the worked example is correct; CONSTRUCT-RELATED would be defensible-as-conservative only if one ignored the three textual anchors above, which §7.13 now forbids.

The worked-example's tone (cautionary tale + corrected verdict) is right — it makes the cost of the failure mode concrete in a way a generic same-domain example would not.

## 7. Design-choice verdicts

| Design choice | Verdict | One-sentence reasoning |
|---|---|---|
| Placement as §4.3.5 interpolated (vs renumbering §4.4-§4.10 to §4.5-§4.11) | **Sound.** | LOCKED-r2 downstream artefacts (`topic-stress-fatigue-pacing.md` r1 + future cluster-S₁ → topic-S₂ pipeline cites) already reference §4.4-§4.10 by number; interpolating preserves all those references without churn. |
| Default on ambiguity = CONSTRUCT-RELATED (vs CONSTRUCT-DIFFERENT or CONSTRUCT-IDENTICAL) | **Sound-with-concern.** | The middle is right on the merits because the §7.13 failure mode is bidirectional (both substrate-mismatch-by-default AND construct-identity-by-default are wrong on weak inference), but the rule cites an analogue (internal_synthesis §4.4) that defaults to the most-conservative label, not the middle — see A1. |
| Disallowing `SKIPPED-AS-DRY-RUN-DEFAULT` at §4.3.5 | **Sound.** | The 2026-06-26 miss was precisely a silent-skip; the check is small enough (one read + one verdict + two sentences per source-subclaim pair) that even dry-run dispatches can produce one of the three allowed dispatch placeholders. |
| Worked example as corrected miss (cautionary tale) vs generic same-domain example | **Sound.** | The cautionary tale makes the failure-mode-cost concrete via a verbatim cite trail (handleiding → §C verification log → corrected §4.3.5 verdict) that a generic example cannot match, and the Wiggers-stress × `all_day_stress_avg` pair is the exact pair the project's downstream Stage A actionability work will return to. |
| No new §8.x interview seed (folded into existing §8.2 Comparability check) | **Sound.** | §4.3.5 fires inside the §8.2 Comparability interview as a preliminary per-metric question; adding §8.5 would split a continuous interview flow into two prompts the user would experience as redundant. |

## 8. Faithfulness to upstream bindings

| Binding | Status | Notes |
|---|---|---|
| Plan §3.5 missing-inputs spec (`open_inputs` four-field shape) | **Concern.** | §4.3.5's dispatch-mode placeholder set is consistent with §3.5's missing-inputs discipline in spirit but invents two placeholder names not in SKILL.md r4's locked vocabulary — see R1. |
| Plan §3.6 map conflict-resolution | **Pass.** | §4.3.5 verdict's routing to §6 conflict rules is correct via the §4.4 wiring + the existing §6.2-§6.4 conflict-resolution structure; no new §6.x rule needed. |
| Plan §3.10 hard predictive gate | **Pass (no crossing).** | §4.3.5 makes no predictive claim; correctly stays inside the §3.10 boundary. |
| Plan §3.12 commentary layer | **Pass (no crossing).** | §4.3.5 produces a verdict + two one-sentence descriptions per metric; no §3.12 subject-narrative commentary; correctly stays inside the §7.7 anti-pattern boundary. |
| Limitations doc §3 L3 + §5 L-ID citation row | **Concern.** | The worked-example's three-way L3 attribution (device-generation + Firstbeat algorithm-version drift + population-Firstbeat-calibration) fits L3 literally per its "underlying algorithm updates" + "calibration drift" framing, but stretches L3's project-specific-manifestation paragraph past its hardware-upgrade scope — see A2. |
| CONVENTIONS §1.2 producer-vs-reviewer | **Pass (no crossing).** | §4.3.5 sits inside the Stage S₂ producer-mode interview; the verdict is the user's (per §8.2 framing); §4.3.5 does not promote the skill to reviewer-mode operations. |
| CONVENTIONS §2.1 descriptive-before-inference | **Pass.** | §4.3.5 is a descriptive verdict on the source's named metric vs the project's named metric; no inferential claim about the construct's substantive behaviour; correctly precedes §4.4-§4.6 inferential work. |
| SKILL.md r4 dispatch-mode vocabulary | **Concern.** | See R1. |
| descriptive_precondition_audit.md (Stage D construct-identity record) | **Pass.** | Stage D produces no construct-identity verdict in any form (a grep of the LOCKED-r2 guide shows no "construct" / "named metric" treatment); §4.3.5 is the first place the verdict lives, which is appropriate for the Stage S₂ external-source-vs-project pairing. |
| internal_synthesis.md §4.4 default-on-ambiguity analogue | **Concern.** | The cited analogue defaults to CONFLICT (most-conservative-divergence-preserving), not the middle; the §4.3.5 default-to-CONSTRUCT-RELATED is defensible on the merits but the analogy is loose — see A1. |

## 9. Anti-pattern fit assessment

§7.13's depth (~15 lines, pointer-style) is correct for what it is — a routing-rule anti-pattern, not a substantive new failure-mode. Comparable in depth to §7.10 (uncited claims floating, ~12 lines) and §7.11 (re-routing in-stage, ~12 lines), both routing-rule anti-patterns. The §7.1-§7.5 depth range (~25-40 lines) is for failure-modes that need explanatory worked-example detail; §7.13 instead routes back to §4.3.5's worked-example anchor, which is the right factoring.

The detect-and-route discipline ("when §4.4 asserts a substrate fault-line, the corresponding §4.3.5 block must contain the source's instrument-or-UI citation that warrants the verdict; if absent, the §4.3.5 verdict is unsupported and routes back to either re-read or DEFAULTED-PENDING-USER-INPUT") is operationally clean. The §4.3.5 hard-rule-3 + procedure-step-2 cross-reference is correct.

No duplication-creating-conflict between §7.13 and §4.3.5; §7.13 names the failure mode and routes to §4.3.5's binding rules rather than restating them.

## 10. Lock-log + status-header convention check

**Lock-log row.** The 2026-06-26 r3 row matches the format of the prior four rows (Date | Event | Note). The Event field "Drafted r2 → r3" parallels the prior "Drafted r1" and "Revised r1 → r2" patterns. The Note field is dense (~25 lines of unbroken prose) — comparable to the LOCKED-r2 entry's density. The three numbered changes (NEW §4.3.5; §4.4 lead-in cross-reference; NEW §7.13) match the status header's claim. The "no renumbering of §4.4-§4.10" justification is correctly captured. The "Pending user acceptance + (optionally) fresh-session `/research-methodology-review`" framing matches the r1 → r2 cycle's "fresh-session review" pattern.

A1-style scannability could compress the row to two-or-three short paragraphs (per A4 in the r1 review that did absorb at r2), but the LOCKED-r2 entry itself is similarly dense, so a separate density-discipline pass would have to revise both rows — not in r3 scope.

**Status header.** The r3 framing preserves the r2 history correctly: the "**r2 history (preserved for context)**" paragraph names the r1 → r2 cycle's two required + four recommended findings + the A1 deferral + the implementation hand-off to guide #5, all consistent with the LOCKED-r2 entry. The r3-specific changes are named with the right level of detail (three changes + Wiggers worked-example anchor). The "DRAFT r3 PENDING USER ACCEPTANCE 2026-06-26" status is correct for a pre-acceptance state.

## 11. Final recommendation

**Lock r3 after absorbing R1 (required); A1 + A2 are optional one-sentence absorptions that can also land in this cycle without dispatching a separate review.** R1 is the only finding that touches a binding-vocabulary consistency claim made in the §4.3.5 lead-in itself; not absorbing it leaves the dispatch-mode placeholder layer in a state where §4.3.5 and SKILL.md r4 disagree on placeholder names, which will cost a future Stage S₂ drafter or skill-maintainer time. A1 + A2 each add one sentence of provenance / decision-flag that strengthens the section without changing its substance.

If the user prefers a minimal r3 lock (R1 only), A1 + A2 can defer to a future r4 cycle with the same rationale the r2 cycle used for A1 density compression (deferred per reviewer "for a future revision pass" framing).

The §4.3.5 + §4.4 lead-in + §7.13 + lock-log changes are otherwise sound and ready to lock. The Wiggers worked-example claim is warranted. The interpolated-not-renumbered placement is correct. The §7.13 brevity is correct. The three-label verdict set is exhaustive. The procedure is mechanically applicable. No substantive revision is needed.
