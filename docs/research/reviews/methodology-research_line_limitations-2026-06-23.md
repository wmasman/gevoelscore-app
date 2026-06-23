# Methodology review — research_line_limitations.md (r2, 2026-06-23)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session (no shared session context; doc-only knowledge of the artefact and its inputs).
**Target**: docs/research/methodology/research_line_limitations.md (r2, 2026-06-23)
**Review date**: 2026-06-23
**Standards applied**: CONVENTIONS §1.2, §2.2, §3, §4, §7; STROBE 2007, CENT-N-of-1 2015, SCRIBE 2016, Daza 2018, Natesan 2023, WWC 2022 SCED as applicable.

---

## 1. Overall verdict

**REVISION RECOMMENDED.** The doc is substantively sound at the architectural level — the seven systemic limitations cover the right ground; the per-L-section shape (What / Why / Manifestation / Forbids / Permits / Cited / Anchor) is the right shape; the §1.5 scope split, the §5 citation requirement table, and the §7 drift triggers all hold together. The doc deserves to lock once the items below are addressed. But the same-session self-review did not catch a substantive data-accuracy bug in L7 Example 3 (the `respiration_avg_sleep` fill-fraction is attributed to the source channel when it actually belongs to the lagged-z variant — and the framing of the missingness as "structural to FR245" is then itself wrong), it accepted a "pre-existing artefacts are not retroactively edited" rule for HAs that were locked on the *same day* as this MD (a missed-opportunity framing that the doc itself does not surface honestly), and it left the §8 downstream-citation table with a tracking mechanism that depends on a skill that does not yet exist. The L4 self-honesty caveat is good but stops one step short of what a fresh-session reviewer should say about the L4 mitigation reach. None of these block the doc's substantive utility; all of them are the kind of thing a fresh-session reviewer is structurally better placed to catch than the drafter was. Hence REVISION RECOMMENDED, not REJECT or ACCEPT.

---

## 2. Four-input bar findings (CONVENTIONS §2.2)

The four-input bar binds methodology MDs per §2.2. Per-input findings:

**Best-practices standards** — **PASS**. The doc anchors each L-section to the right body of best-practice (STROBE §12d for limitations reporting, STROBE §13a + §16 for missingness/confounders, CENT-N-of-1 item 21 for explicit N-of-1 limitations, SCRIBE for participant-as-researcher transparency, Daza 2018 + Natesan 2023 + WWC 2022 SCED for N-of-1-to-group inference reach, Nelson 2020 for consumer-wearable HR reporting standards, Moshe 2021 + O'Brien 2023 for self-report-vs-wearable and LC interoceptive context). The mapping is appropriate; each anchor is cited where its content actually bears on the limitation it backstops.

**Established literature** — **PARTIAL**. The literature anchors above are real and load-bearing where used. Two soft gaps: L5 explicitly flags "no curated reference in `literature/` at this revision; flagged for follow-up acquisition" (honest, but no path is named — `_pending_literature_fetch.md` would be the natural home and is not pointed at); L6 similarly flags "Direct citation of self-report reliability standards in PAIS-adjacent populations is sparse; flagged for follow-up literature acquisition per `_pending_literature_fetch.md` pattern" (this one *does* name the queue; good). The L1 anchors (Daza / CENT-N-of-1 / SCRIBE / Natesan / WWC) are the right N-of-1 inference-reach corpus. L7 anchors STROBE §13a, which is the right call for missingness in observational studies. PARTIAL because two of the seven L-sections name follow-up literature gaps without uniformly routing them to the existing `_pending_literature_fetch.md` queue mechanism.

**Tradeoff vision** — **PASS**. §2 "Alternatives considered" makes the choice explicit: per-HA caveat lists as the natural alternative; rejected for three named reasons (drift, omission, review burden); preserves the per-HA caveat layer as still-required-and-independent. This is the discipline §2.2 input 3 asks for: state the dimension being weighted (centralisation vs distribution of the limitation surface; review burden vs drift risk; commensurability vs per-artefact tailoring). The tradeoff is named honestly.

**Research limitations + objectives** — **PASS**. The doc is *about* the research limitations input — every L-section IS a limitation surfaced with its operational consequence. The objective ("provide a citable enumeration so downstream artefacts cite-by-reference rather than re-state from memory") is named in §2 and operationalised in §5. The doc is in a sense self-bootstrapping on this input: the methodology MD describes the limitations that bind every downstream artefact, and §2.2 input 4 is satisfied by virtue of the doc's purpose.

Summary: **3 PASS + 1 PARTIAL**, with the PARTIAL on literature being a soft "name the follow-up queue uniformly" gap rather than a substantive citation hole.

---

## 3. Structural findings

**Doc-level shape** — sound. Status header + caveat about the missing fresh-session review at top (honest); §1 purpose; §1.5 scope/exclusions (more disciplined than most methodology MDs in this folder; see §4 of this review on the "out of scope" framing); §2 why-binding + alternatives-considered; §3 the seven L-sections in the seven-field shape; §4 summary table; §5 citation requirement table (with example citations); §6 add-a-new-limitation process; §7 drift triggers (generic + project-specific); §8 lock log + downstream-citation count; §9 cross-references. This matches the established methodology-MD shape in this folder (`lc_era_temporal_segmentation.md`, `phase_axis_collapsibility_conventions.md`, `symptom_mention_asymmetry.md`).

**Consistency with other methodology MDs** — sound. The §6 "adding a new systemic limitation" process mirrors the version-and-lock discipline `phase_axis_collapsibility_conventions.md` uses (drafter + audit + user accept + lock log entry). The §7 drift triggers section is more developed than most methodology MDs and is a positive contribution to the folder's pattern.

**Dependency consistency** — sound but worth noting. The doc depends on `_plan_results_analysis_layer.md` §3.9 (the layer rule that mandates this doc's existence) and is cited reciprocally by the plan's §11 step 4. The reciprocal cite at the plan side is in place (the plan is r4 LOCKED 2026-06-23 with §11 step 4 producing this doc). The reciprocal-cite paragraphs in `lc_era_temporal_segmentation.md` and `phase_axis_collapsibility_conventions.md` are already present from the prior lock cycles of those MDs and continue to hold; this MD does not need to update them. **One concern**: this MD does not appear in `methodology/README.md` "Read these in order" list (the README is dated and only covers the older 9 methodology MDs). The README needs to be updated at lock time to add this MD to the index. The §6 process for adding new limitations should similarly note the README-index update as a step (currently absent).

---

## 4. Per-section findings

### Status header (lines 3-13)

**Adequate.** The status header is unusually honest about its review provenance: it explicitly flags "this MD did not receive a true fresh-session methodology-review (same-session self-review acknowledged as a weaker discipline; see L4 mitigation caveat for why this matters structurally)." That self-flag is exactly what a producer-mode artefact awaiting fresh-session review should say. Suggested tightening: name *this* review (when it lands) in the lock log at §8.

### §1 Purpose (lines 17-37)

**Adequate.** The systemic-vs-per-HA-caveat distinction is well-framed and consistent with the actual practice — per-HA caveats in `hypothesis.md` §8 are not displaced. The binding-rule blockquote is appropriately load-bearing.

### §1.5 Scope and exclusions (lines 39-70)

**Concerns (one substantive, one minor).** The four out-of-scope categories (per-HA caveats, layer-process limitations, infrastructure limitations, external-research limitations) are well-named. The reasoning for routing per-HA caveats out is clean. **Substantive concern**: "layer-process limitations" (the producer-vs-reviewer split's imperfect blinding; `/research-interpret` skill's interview-engine choices) is excluded by routing to `_plan_results_analysis_layer.md`. But the *imperfect blinding of the producer-vs-reviewer split* is in fact a substantive L4-territory limitation (analyst-is-subject manifested in the LLM-assistant + the same-session vs different-session split being the only available proxy for external independence). The doc's own L4 already says the LLM-assistant is *not* a substitute for external peer review; the producer-vs-reviewer split's imperfect blinding is the same concern under a different name and could legitimately be folded into L4 rather than excluded as "layer-process". The current scope line draws the boundary in a way that lets the most-honest version of L4 slip through. Recommended: either extend L4 to absorb "the producer-vs-reviewer split is a fresh-session-context check, not a fresh-LLM-instance check" (de facto already there in L4's caveat but not surfaced as part of L4's "Forbids/Permits"), OR add a note to §1.5 clarifying that the producer-vs-reviewer split's blinding limit is partially in L4's scope. The minor concern: the "exhaustive for the in-scope category as of 2026-06-23" claim is strong; §3 of this review identifies one candidate the doc considered and excluded (analyst-coder bias on the v24 dictionary itself, claimed covered by L4+L5) — that exclusion is defensible (the v24 dictionary IS analyst-coded by the project's author, and the L4+L5 combination does cover the propagating bias) but the reasoning should be in §1.5 explicitly rather than only in the brief that called this review.

### §2 Why this is a layer-level binding rule (lines 72-103)

**Adequate.** The three reasons for the centralised-vs-distributed choice (drift, omission, review burden) are well-named. The literature crosscut to STROBE §12d and CENT-N-of-1 item 21 is appropriate. The closing "Per-HA caveats remain valid and required at their level. This doc does not replace them; it sits underneath and applies independently." is exactly the right disambiguation.

### §3 L1 Single-subject reach (lines 122-166)

**Adequate.** Forbids/Permits split is right; the "convergence-with-consensus claims when this subject's finding agrees with group-level evidence (the corpus *adds* a data point, but does not *settle*)" is a subtle and important permitted-claim shape. Anchors are correct.

### §3 L2 Era confounds (lines 170-261)

**Adequate.** The "HARD BOUNDARIES" framing correctly cites `phase_axis_collapsibility_conventions.md` §3.4; cross-checking that source MD confirms the binding is accurately stated (the boundary rule says "phase 1 ↔ phase 2 ↔ LC era are NEVER pooled" with the same category-error rationale L2 invokes — "mixes healthy / acute-viral / chronic-illness states"). The Stratum 1-4 day-range table matches `lc_era_temporal_segmentation.md` §1's data-given strata table. The 2024-04 cluster citation (`CONVENTIONS §3.8` boundary-spacing minimum) correctly anchors the structurally-unanalyzable framing. Citalopram start 2024-04-09 + CPAP end 2024-04-16 are correct per CONVENTIONS line 461. Within-Stratum-4 sub-segmentation reference to `lc_recovery_phase_axis.md` §3.3-§3.5 with M1/M2 warrant is correct.

### §3 L3 Device generations (lines 266-318)

**Concerns (two: one substantive on REM-stage anchoring; one on HRV-proxy framing).**

The REM-stage claim is accurate: DATA_DICTIONARY §sleep_extras confirms "**No `sleep_rem_min` exists**: Forerunner 245 (Elevate V3 sensor) does not produce REM-stage classification; all non-deep / non-awake sleep aggregates into `sleep_light_min`." The L3 wording matches this faithfully.

**HRV-proxy framing concern**: L3 says "HA07c, HA08c, HA07d) already ran using sleep-stress as the HRV proxy per `hrv_proxy_via_stress.md`. The HA07-proxy / HA08-proxy successor slots reserved in the §11 step 5 synthesis-structure map (per `_descriptive_stocktake_2026-06-23.md` §9.4) continue that adaptation." Cross-checking `_descriptive_stocktake_2026-06-23.md` §9.4 confirms the HA07-proxy / HA08-proxy slot reservation — but the stocktake §9.4 ALSO explicitly says HA07 + HA08 originals are to be marked "SUPERSEDED" with the proxy successors taking over. L3's framing reads HA07c/HA08c/HA07d as already-ran sleep-stress proxies, which is correct, but the L3 wording should also note that the HA07 + HA08 originals are SUPERSEDED rather than just "ran a proxy on the side". Minor framing issue; not a substantive accuracy bug.

The "FR245 across the corpus. No hardware upgrade has occurred yet" claim is accurate per `garmin_indicators_audit.md` and `hrv_proxy_via_stress.md`.

### §3 L4 Analyst-is-subject (lines 322-389)

**Concerns (this is where the L4-self-honesty test bites).** The "Crucial mitigation caveat" paragraph (lines 346-359) is a good-faith disclosure: it acknowledges that "the LLM-assistant is not a substitute for external peer review" and that "Claude is part of the drafting pipeline as much as the reviewing pipeline; it has no independent identity across 'drafting session' vs 'fresh-session reviewer' beyond the session-context boundary itself." Good.

**Where it stops short**: the caveat names the fresh-session-review discipline as "a real check — but it is not equivalent to an external researcher with a different training set, different lived experience, and structurally different incentives." True. But the sentence that closes the caveat ("*true external check* on L4 is what external-research follow-ups ... and what future group-level researchers reading the translation artefacts ... can provide") risks reading as "L4 will be resolved when external researchers eventually read the translation outputs." That framing under-states the current-state limitation: as of 2026-06-23, **no external researcher has ever reviewed any artefact in this corpus**. The L4 caveat is structurally correct but operationally aspirational; it should be honest that the L4 mitigation as currently practiced reaches no further than (a) the producer/reviewer mode split + (b) the fresh-session discipline + (c) the L4 caveat itself surfacing the limitation. The L4 "Permits" bullet "The fresh-session review discipline acts as the imperfect-but-real external check" is the right framing of the *available* mitigation; the caveat paragraph should be tightened to match — replace the future-tense "what ... can provide" with present-tense "and what L4 explicitly acknowledges is not currently in place; until external review lands on translation artefacts, the L4 mitigation reach is exactly the session-context-boundary depth, no more."

The deeper L4-self-honesty test: the drafter wrote this caveat *about itself*. A fresh-session reviewer reading the caveat cold can confirm it is honest as far as it goes, but should also note: **the very fact that the drafter (Claude) wrote a caveat about Claude's limitations as a reviewer of Claude's own work, and then accepted the caveat as adequate self-mitigation, is itself an L4 instance** — analyst-is-subject manifested at the meta level (drafter-is-also-self-mitigation-author). This recursion is not flagged in the doc. A short paragraph at the end of L4's "Project-specific manifestation" would close this: "Including: the L4 mitigation paragraph in this MD was authored by the same agent (Claude) that L4 is about; the meta-recursion is itself an L4 manifestation, partially mitigated by the present fresh-session reviewer reading the caveat cold and accepting (or rejecting) its honesty."

The Forbids/Permits split is otherwise sound. The cite to CONVENTIONS §4.3 (prior-driven hypotheses are confirmatory) is correct and load-bearing.

### §3 L5 Presence-conditioned data layer (lines 393-457)

**Adequate, with one factual cross-check passing.** L5 correctly cites `symptom_mention_asymmetry.md` as the binding source; cross-checking that MD confirms the five-cause framing and the v24 / per_day_intensity scope. The "no HA in the current corpus runs a *primary* test on a v24-derived signal" claim is verifiable in `_descriptive_stocktake_2026-06-23.md` §7 — confirmed. The mention of "HA-C4b v3 §8 pacing-behaviour confounder caveat; various `cat_belasting_*` / `state_symptoom_*` caveats in older HAs" as descriptive-companion/caveat-class usages matches stocktake §7. The Forbids/Permits split is accurate. Literature-anchor honesty about "no curated reference in `literature/` at this revision" is the kind of disclosure §2.2 input 2 demands.

### §3 L6 Self-reporting (lines 461-512)

**Adequate.** The PAIS-interoceptive-disturbance framing for *why* this subject's self-report is potentially noisier than general-population is the right load-bearing reason to surface L6 (not just "self-report has biases"). The "noise floor" caveat under Forbids is good operational discipline. The Moshe 2021 + O'Brien 2023 anchors are appropriate; the honest flag for missing self-report-reliability standards in PAIS-adjacent populations is the right disclosure.

### §3 L7 Survivorship (lines 516-588)

**Substantive concern — Example 3 is wrong.** The two worked-example checks for Example 1 (HA-C3 unmedicated primary ~581 days, drop ~3 of ~584) and Example 2 (HA-C4 v2 chain-T+1 16 of 41 dropout) cross-check correctly: HA-C3 v2 hypothesis.md §4.3 confirms n=581; HA-C4 v2 result.md confirms n_heavy=25 (primary) vs n=41 (chain-relaxed) on validate Ch3, so 16 of 41 dropout is right.

**Example 3 is incorrectly attributed.** The target says:

> *Example 3*: `respiration_avg_sleep` source channel: ~23% fill on Stratum 4 (per DATA_DICTIONARY `*_lagged_lcera_z` table). The 77% missingness is structural to the FR245 (Elevate V3 doesn't reliably produce sleep respiration on every night) — a per-signal L7 manifestation that L3 (device generations) is the upstream cause of.

This is wrong on two counts:

1. The `respiration_avg_sleep` **source channel** has **~97.1% fill** (1704/1755 days per DATA_DICTIONARY §Section 11 — "Wave 3 add 2026-06-12. Wiggers G1..."). The ~23% fill belongs to the **`respiration_avg_sleep_lagged_lcera_z`** *lagged-z derivative*, not to the source channel. The target's wording "`respiration_avg_sleep` source channel: ~23% fill ... (per DATA_DICTIONARY `*_lagged_lcera_z` table)" mixes the channel name with the derivative's fill in a way that produces a factually incorrect attribution.

2. Because the source channel actually has ~97% fill, the 77% missingness in the lagged-z variant is NOT "structural to the FR245 (Elevate V3 doesn't reliably produce sleep respiration on every night)" — Elevate V3 produces sleep respiration on ~97% of nights, which is high. The 77% missingness in the lagged-z variant is mostly the **lagged-baseline window construction** (the variant requires baseline values from a `[d-90, d-30]` window, restricted to LC-era days; this construction lops off all pre-LC days and any day inside a 90-day Garmin gap, regardless of source-channel coverage). The "structural to the FR245" reading misroutes the cause from the lagged-variant construction to the device.

This is the kind of accuracy bug that same-session self-review is structurally weak at catching (the drafter conflated source-channel fill with derivative fill in their head and self-reviewed without re-reading DATA_DICTIONARY for the channel-vs-derivative distinction). It is also load-bearing for the doc's claim that L7 has "structural" manifestations downstream of L3: the example as written supports that claim but is factually wrong; the correct example would be (a) gevoelscore missing on subject-controlled non-entry days (which IS structural to L6, not L3), (b) Garmin nightly signals missing when the subject didn't wear the watch (which IS structural to L7 directly, not via L3), or (c) the lagged-z variants' missingness from baseline-window construction (which is structural to the methodology choice, not L3 device-generations). All three are honest L7 manifestations; the `respiration_avg_sleep` example as written is not.

**Required fix**: either replace Example 3 with one of the three honest candidates above, OR rewrite it as "the `respiration_avg_sleep_lagged_lcera_z` derivative: ~23% fill on Stratum 4, structural to the lagged-baseline window construction (per DATA_DICTIONARY note). The 77% missingness is not a device-coverage limitation (the source `respiration_avg_sleep` has ~97% fill) — it is a methodology-derived L7 manifestation propagating from the lagged-baseline discipline." That framing keeps the structural-missingness lesson but routes the cause to the right upstream (methodology choice, not device).

Beyond Example 3: the Forbids/Permits split is sound. The "Aggregating across signals without checking joint missingness" forbid is exactly the right thing to forbid. The STROBE §13a anchor is correct.

### §4 The seven limitations summarised table (lines 592-602)

**Adequate.** The summary table is internally consistent with the §3 sections. The "L7: ~1500 LC-era days; ~1390 Stratum 4 days" numbers match `lc_phase_descriptive.md` §1 snapshot (n=1500 on `lc_phase == 'lc'`); Stratum 4 ~1390 is derivable as 1500 minus the ~110-day Stratum-3 LC-pre-gevoelscore window (2022-04-04 → 2022-09-02 = 152 days, but `lc_phase` includes both Stratum 3 + 4 as `lc`, so 1500 − 152 ≈ 1348; the doc's ~1390 is close enough to be approximately right with the as-of-date moving slightly). Acceptable.

### §5 How downstream artefacts cite this doc (lines 604-646)

**Mostly adequate, with one concern on implementability (concern #5 in the brief).**

The citation requirement table is implementable manually for any of the artefact types — the rule "one-line acknowledgment with L-ID and one sentence on how this limitation applies" is operationally simple, and the example citation block (`Cites L2 (era confounds): this HA spans Stratum 4 unmedicated only;...`) is clear. The step 8 dry-run will be able to follow §5 manually without the (not-yet-built) `/research-interpret` skill. **No implementability concern at the artefact-author level.**

**Implementability concern is at the tracking level** (§8 downstream-citation count, see review §4.§8 below).

**Retroactive citation rule (lines 628-646; concern #6 in the brief).** The rule says "The four HAs ready for Stage D TRUSTED (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo) were pre-registered *before* this MD was authored. Their `hypothesis.md` and `result.md` files do not cite this doc — and per producer-vs-reviewer discipline, locked pre-regs are not retroactively edited." Cross-checking the four HAs:

- **HA-C3 v2** hypothesis.md is dated 2026-06-23 (locked r2 today, the *same day* as this MD). It already has §8 "Caveats `result.md` must explicitly acknowledge" with 12 items covering (caveat 2) "n=1 single-subject caveats per CONVENTIONS §3.1"; (caveat 3) "Citalopram-phase confound + chosen mitigation"; (caveat 4) "Crash-day inclusion structural fragility"; (caveat 5) "Within-subject shape, NOT between-subject prediction"; (caveat 7) "v2 scope is corpus-stress-range AS-REPRESENTED, NOT Wiggers' abstract register range" (which is partly an L1-flavored corpus-property limitation).
- **HA-C3p** hypothesis.md likewise dated 2026-06-23 (locked r2 today) with the same §8 caveat shape.
- **HA-C4c** hypothesis.md dated 2026-06-23 with §8 Caveats section.
- **HA11-bout-redo** dated 2026-06-22 with §8 Caveats (10 items per its §10.3 template note).

All four were locked **on or one day before** this MD's draft date. The "pre-existing artefacts are not retroactively edited" framing reads as if these HAs were drafted long before this MD; in fact they are coeval (HA-C3 v2, HA-C3p, HA-C4c are *exactly contemporaneous* — all locked 2026-06-23, same day as the target). Three concerns follow:

1. **The §5 framing reads more conservative than the situation warrants.** All four HAs already have §8 caveats sections that ARE the natural home for L-ID citations; adding a one-line "Cites L1 (single-subject reach), L2 (era confounds + unmedicated phase only), L3 (FR245 device generation), L6 (gevoelscore self-report)" entry to each HA's §8 would be a low-cost, high-honesty move that keeps the citation discipline uniform from pre-reg time forward (the doc's own §5 says "Future HAs pre-registered after this MD locks SHOULD cite the applicable L-IDs in their hypothesis.md §8 caveats section, so the citation enters at pre-reg time rather than waiting for interpretation"). The four ready HAs are at the *moment* of locking; arguing they are "pre-existing" because they pre-date the MD by hours is a thin technicality.

2. **The producer-vs-reviewer discipline argument cited (lines 631-632) is overstretched.** Reviewer-mode-with-authorization artefacts (which `hypothesis.md` is) are not editable post-lock except via the standard v→v+1 revision process. But the four HAs are being r2-absorbed today via §3.6 compression of the audit fires; a citation addition would naturally fold into an r3 or could be deferred. The doc's framing forecloses that conversation rather than naming it.

3. **The "interpretation.md will cite this doc per §5" path is sound** as a separation-of-concerns argument (pre-regs declare operationalisation; interpretations declare what verdicts mean given systemic context). This is defensible and consistent with §5's table. But the doc should acknowledge that the four ready HAs are *exactly* the boundary case — they were drafted in the same week as this MD and could have had L-ID citations added at the §3.6-compression r2 absorb that already happened today. The framing should be: "the four ready HAs are the boundary cases; their interpretation.md artefacts will carry the L-ID citations to maintain forward uniformity, but the §8 caveats sections of the four HA hypothesis.md files happen to already cite the substantive content of L1, L2, L3, L6 in different language. The choice to NOT add L-ID labels retroactively is a separation-of-concerns choice (pre-regs declare operationalisation; interpretations declare meaning), not a 'we cannot edit locked pre-regs' constraint." That is honest; the current framing reads as too-strict.

**Recommended action**: add a paragraph to §5 between current lines 627 and 628 acknowledging the boundary-case framing of the four ready HAs (drafted on the same day or one day before this MD; their §8 caveats already cover L1/L2/L3/L6 in different language; the no-retroactive-edit choice is a separation-of-concerns choice, not a hard constraint). This costs ~5 lines and prevents the rule from reading as a missed-opportunity blind spot.

### §6 Adding a new systemic limitation (lines 648-671)

**Adequate.** The 6-step process mirrors the methodology-MD lock discipline. The append-only framing is correct. **Suggested addition (per §3 structural concern above)**: add a step 2.5 "Update methodology/README.md index" so the doc surfaces in the canonical read-order.

### §7 Drift triggers (lines 673-711)

**Adequate.** The six project-specific triggers are well-named (new intervention, device upgrade, v24 version bump, new COVID infection/vaccination, new N-of-1 standards literature, layperson-test failure during translation). The generic 6-month cadence + cited-MD-version-change triggers from §3.7 of the plan are inherited correctly.

### §8 Lock log (lines 713-741)

**Concerns (one on the E1-E8 catch list; one on the §8 downstream-citation table implementability — concern #10 in the brief).**

The E1-E8 catch list demonstrates the same-session self-review did catch a substantial set of accuracy bugs (citalopram date, 2024-04 cluster expansion, Stratum boundaries, day counts, subject name neutralisation, cross-references, HRV-proxy framing). Good. **What it did NOT catch is the L7 Example 3 attribution bug above** — which a fresh-session reviewer is structurally better placed to find because the drafter held the channel-vs-derivative distinction in mind correctly while drafting r1 but then conflated it during self-review when summarising the example. A second-pass self-review by the same drafter who introduced the conflation will see what they intended to say, not what is on the page.

**§8 downstream-citation count table (lines 720-741).** The table is empty (all L-IDs at 0; "Last cited —") with a footer saying "entries updated mechanically by the `/research-interpret` skill's `--drift-check` helper (per `_plan_results_analysis_layer.md` §7 skill responsibility 6)". **The skill does not yet exist** (per the plan's §11 step 7; the skill is built in step 7 of the rollout, which is downstream of step 4 that produced this MD). The doc should either:

1. Explicitly say "this table will remain at zeros until §11 step 7 lands the skill; pre-skill-landing citations are tracked manually here" (and provide a stub mechanism for the four ready HAs' interpretation.md artefacts when they land in step 8 dry-run), OR
2. Defer the table to a separate operational artefact and leave §8 with just the lock log.

The current framing implies a tracking mechanism exists; it does not yet. This is exactly the kind of "looks-implemented-but-isn't" gap a fresh-session reviewer should catch.

### §9 Cross-references (lines 745-790)

**Adequate.** The cross-reference list is comprehensive — all methodology MDs the doc depends on are pointed at; CONVENTIONS §3.8 / §4.3 / §5 anchors are correct; DATA_DICTIONARY pointer is included (which IS load-bearing for L3 + L7); the `_descriptive_stocktake_2026-06-23.md` pointer is correct. The literature pointer block at the end is comprehensive.

---

## 5. What the self-review caught vs missed

**Caught** (per §8 E1-E8): 8 accuracy bugs across dates, day counts, subject-name neutralisation, cross-references, and HRV-proxy framing. Substantive content additions in r2: §1.5 scope-and-exclusions; §2 alternatives-considered paragraph; L4 LLM-not-substitute caveat; L5 companion/caveat usage acknowledgment; L7 worked examples; §5 retroactive-citation guidance; §7 project-specific triggers. This is a substantial r1 → r2 absorb and the self-review demonstrably did meaningful work.

**Missed** (a true fresh-session reviewer should add):

1. **L7 Example 3 attribution bug** (review §4 above): `respiration_avg_sleep` source channel fill is ~97%, not ~23%; the ~23% is the lagged-z derivative; the framing "structural to the FR245" is wrong. This is the most substantive thing missed.

2. **L4 self-honesty stops one step short**: the caveat names LLM-assistant ≠ external review well but lets the closing sentence drift into aspirational future-tense; doesn't surface the meta-recursion that the L4 caveat itself was authored by the L4-subject agent.

3. **§5 retroactive-citation rule under-acknowledges the boundary case**: the four ready HAs are coeval with this MD, not pre-existing in any meaningful sense; their §8 caveats already cover the substantive content of L1/L2/L3/L6 in non-L-ID language; the no-retroactive-edit framing is a separation-of-concerns choice, not a hard constraint, and should be named as such.

4. **§8 downstream-citation table tracking mechanism is vapor**: depends on the `/research-interpret` skill's `--drift-check` helper which does not yet exist (built in plan §11 step 7, downstream of this MD's step 4). The doc should say so explicitly or move the table to a separate live artefact.

5. **§1.5 scope-line on layer-process limitations lets a substantive L4 instance slip out**: the producer-vs-reviewer split's imperfect blinding is in fact an L4 manifestation, not a "layer-process" out-of-scope item. Recommend folding into L4 or noting the partial overlap in §1.5.

6. **methodology/README.md is not updated to index this new MD**: the §6 add-process should include a README-index-update step.

7. **§5 example citations are useful but only two are shown**: the doc would benefit from a third example showing a cross-cutting citation (e.g., a `cluster-*.md` cite that names L1+L2+L4 in one block per §5's "every limitation that touches any cluster member" rule, since clusters are the natural place L4 lived-experience-prior-reconciliation enters synthesis).

---

## 6. Cross-cutting concerns

**Reviewer-mode discipline holds.** This review does not edit the target; recommendations are stated in this report only, per CONVENTIONS §1.2.

**Same-session-review structural weakness was operative.** The drafter and self-reviewer were the same session; the L4 caveat in the doc itself flags this as structurally weaker than fresh-session review. The catches in §8's E1-E8 list show the self-review wasn't useless (it caught real bugs), but the substantive misses above (especially L7 Example 3) confirm the L4 framing: same-session self-review catches the surface bugs the drafter forgot to fix but misses the bugs that the drafter introduced *while* drafting and re-confirmed *as right* during self-review. Fresh-session review is the structural complement.

**Doc deserves to lock.** The required and recommended actions below are addressable in a single r3 absorb (1-2 hours of producer-mode work) without architectural change. The doc's structure, scope, alternatives-considered reasoning, citation framework, drift triggers, and lock-log discipline are all sound. The substantive limitations enumerated (L1-L7) are the right limitations. The §5 binding rule is the right binding rule. The MD is fit for purpose as the layer-level systemic-limitations source-of-truth that `_plan_results_analysis_layer.md` §3.9 mandates.

---

## 7. Required actions (must fix before lock)

1. **Fix L7 Example 3** — `respiration_avg_sleep` source channel fill is ~97% per DATA_DICTIONARY, NOT 23%. Either replace the example with one of the three honest L7 manifestations (subject-controlled gevoelscore missingness, Garmin no-wear missingness, or correctly-framed lagged-baseline window missingness), OR rewrite to "`respiration_avg_sleep_lagged_lcera_z` derivative ~23% fill, structural to lagged-baseline window construction (not the FR245 device — source channel is ~97% fill); methodology-derived L7 manifestation, not L3-derived." Rationale: load-bearing accuracy bug on a worked example; current framing is factually wrong on both fill-fraction attribution and missingness-cause attribution.

2. **Tighten L4's mitigation-caveat closing sentence** — replace the future-tense aspiration ("what external-research follow-ups propose and what future group-level researchers reading the translation artefacts can provide") with present-tense honesty ("As of 2026-06-23 no external researcher has reviewed any artefact in this corpus. The L4 mitigation reach is exactly the session-context-boundary depth of the fresh-session discipline; the listed external-review pathways are L4's planned future mitigation, not its current state."). Rationale: keeps the L4 caveat honest at the current-state level rather than drifting to aspirational framing.

3. **Acknowledge boundary-case framing of the four ready HAs in §5** — add 3-5 lines noting that HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo were locked on or one day before this MD's draft date; their §8 caveats already cover the substantive content of L1/L2/L3/L6 in non-L-ID language; the choice to not add L-ID labels retroactively is a separation-of-concerns choice (pre-regs declare operationalisation, interpretations declare meaning), not a hard "we cannot edit locked pre-regs" constraint. Rationale: prevents the rule from reading as a missed-opportunity blind spot; keeps the doc honest about the boundary case.

4. **Disclose §8 downstream-citation-table tracking-mechanism dependency** — add a one-sentence note that the table will remain at zeros until plan §11 step 7 lands the `/research-interpret` skill's `--drift-check` helper; until then, citations are tracked manually here or in a parallel live artefact. Rationale: prevents the table from reading as "looks-implemented-but-isn't"; preserves the table's intent while being honest about the current state.

---

## 8. Recommended actions (should consider)

1. **Add a §3 L4 paragraph acknowledging the meta-recursion** — that the L4 mitigation caveat in this MD was authored by the same agent (Claude) that L4 is about; the recursion is itself an L4 manifestation, partially mitigated by the present fresh-session reviewer reading the caveat cold. Rationale: closes the self-honesty loop the L4 caveat opens.

2. **Tighten §1.5 layer-process exclusion** — either fold "producer-vs-reviewer split's imperfect blinding" into L4 explicitly, or note in §1.5 that the layer-process exclusion does not fully cover the L4-territory blinding-limit concern. Rationale: prevents a substantive L4 instance from slipping out of the doc's scope.

3. **Update methodology/README.md "Read these in order"** at lock time to add this MD to the index; update §6's add-new-limitation process to include README-index-update as a step. Rationale: discoverability + future-add-process completeness.

4. **Route the L5 + L6 follow-up literature flags uniformly through `_pending_literature_fetch.md`** — L5 says "flagged for follow-up acquisition" without naming the queue; L6 correctly names `_pending_literature_fetch.md`. Make L5 match. Rationale: §2.2 input 2 discipline.

5. **Add a third example citation in §5** — covering a cross-cutting case (e.g., a `cluster-*.md` citing L1+L2+L4 together). Rationale: helps future artefact authors see the multi-cite case the table mandates.

6. **Name this review in §8's lock log when it lands** — current entry lists r1 draft + r1→r2 same-session absorb; r3 should add "Fresh-session methodology review 2026-06-23 (this report) → R3 absorb pending." Rationale: lock-log discipline.

7. **Consider whether HA-C4 v2 result.md, which has §-routing caveats and Ch3 INCONCLUSIVE n=25 routing, is the right Example 2 for L7** — the existing Example 2 (16 of 41 dropout triggering Ch3 validate INCONCLUSIVE) is accurate, but the "Substantial; the routing exists because the gate's missingness was load-bearing" framing under-states the lesson. A SUPPORTED reading might be "the §5.3 INCONCLUSIVE-aware triad logic is itself the survivorship-mitigation; the test was structured so that missingness drove a verdict-band, not a silent dropout." Rationale: tightens the Example 2 lesson, optional.

---

## 9. What is fine as-is

- The doc's overall architecture (seven L-sections in a uniform seven-field shape; summary table at §4; citation requirement table at §5; drift triggers + lock log at §7-§8).
- §1's systemic-vs-per-HA caveat distinction (correctly load-bearing).
- §2's alternatives-considered reasoning (the per-HA-restatement alternative is named and rejected for three substantive reasons: drift, omission, review burden).
- §3 L1 Single-subject reach (Forbids/Permits split is right; convergence-with-consensus permit is well-framed; literature anchors correct).
- §3 L2 Era confounds (HARD BOUNDARIES citation is accurate per `phase_axis_collapsibility_conventions.md` §3.4; Stratum 1-4 table matches `lc_era_temporal_segmentation.md` §1; 2024-04 cluster citation correct per CONVENTIONS §3.8 and the citalopram-2024-04-09 / CPAP-end-2024-04-16 dates are right).
- §3 L3 REM-stage anchoring (matches DATA_DICTIONARY §sleep_extras_daily exactly).
- §3 L5 (correctly cites `symptom_mention_asymmetry.md`; the "no HA uses v24 as primary signal" claim verifies against `_descriptive_stocktake_2026-06-23.md` §7; caveat-class usage acknowledgment is accurate).
- §3 L6 (PAIS-interoceptive-disturbance framing is the right load-bearing reason to surface L6).
- §3 L7 Examples 1 and 2 (HA-C3 581 days and HA-C4 v2 16-of-41 both cross-check correctly).
- §4 summary table (internally consistent with §3 sections; day counts verifiable).
- §5's per-artefact-type citation requirement table (operationally clean; the one-line cite + project-specific-application rule is implementable manually without the not-yet-built skill).
- §6's append-only add-process (mirrors `phase_axis_collapsibility_conventions.md` lock discipline; correct).
- §7 drift triggers (the six project-specific triggers are well-named; reciprocal-cite to plan §3.7 inheritance is correct).
- §8 lock log E1-E8 catch list (demonstrates the self-review caught real accuracy bugs; honest about r1 → r2 deltas).
- §9 cross-references (comprehensive; all dependencies named).
- Status-header self-flag about missing fresh-session review (exactly the right thing for a producer-mode artefact awaiting fresh-session review to say).

---

*Review authored 2026-06-23 in a fresh session by Claude (Opus 4.7, 1M context) per the dispatching session's brief. Reviewer had no shared context with the drafting session; read the target + the 9 dependency files (CONVENTIONS.md, the plan, the methodology README, lc_era_temporal_segmentation.md, phase_axis_collapsibility_conventions.md, symptom_mention_asymmetry.md, _descriptive_stocktake_2026-06-23.md, DATA_DICTIONARY.md, and the four ready HAs' hypothesis.md files) cold. No edits made to the target per CONVENTIONS §1.2 reviewer-mode discipline.*
