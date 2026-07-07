# PEM vs POTS mechanism framing: separability markers + catalog labeling (methodology)

## Authorship

- **Drafted**: 2026-07-07 by Claude (Opus 4.8), producer-mode, under explicit
  authorization from the participant-researcher (repo owner).
- **Status**: **ACCEPTED 2026-07-07** (peer-reviewed + literature-updated). The
  independent fresh-context review
  ([`reviews/pem-pots-reframing-2026-07-07.md`](../reviews/pem-pots-reframing-2026-07-07.md),
  MAJOR-REVISIONS folded) was accepted as the section-1.2 independent review. A
  subsequent **external PubMed review**
  ([`literature/reviews/pots_operationalisation_wearable_review.md`](../literature/reviews/pots_operationalisation_wearable_review.md),
  the section-2.2 input-2 literature leg) then **capped the POTS-marker language one
  notch further** (no orthostatic precedent, off-polarity, watch blind to the
  defining orthostatic axis); that ceiling is folded into section 3.1 + section 6.
- **Why this MD exists**: the 2026-07-07 Wiggers-guide re-read surfaced that the
  guide distinguishes two watch-visible mechanisms - **PEM** and **POTS /
  orthostatic** - and that the project catalog is almost entirely PEM-framed. Two
  new major operationalisation choices follow (per
  [CONVENTIONS section 2.2](../CONVENTIONS.md)): (a) how we mark a "POTS-signature"
  vs "PEM-signature" day in the watch data for descriptive separability, and (b)
  how we label existing catalog hypotheses PEM / POTS / both. Both have cascading
  downstream consequences (a research note, a public website reframing, catalog
  edits), so they clear the section-2.2 bar and are reasoned here before locking.

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress. Load-bearing here: the PEM marker is an HRV proxy via overnight stress.

---

## 1. What this MD operationalises (and what it does NOT)

### 1.1 It operationalises

1. Two **descriptive watch signals** at the day level, for *descriptive*
   separability / timing / felt-state reads (analysis at
   [`analyses/descriptive/pem_pots_separability/`](../analyses/descriptive/pem_pots_separability/)):
   the **overnight stress-load signal** (`stress_mean_sleep` z) and the **within-day
   U-dip signal** (`u_dip_count` z).
2. A **mechanism label** (`PEM` / `POTS` / `both` / `neither`) applied to each
   Wiggers-catalog hypothesis, tagging which of the guide's mechanisms a statement is
   about, so the catalog stops being implicitly PEM-only.

**Naming discipline (added 2026-07-07).** We call these two things **signals /
patterns**, not "markers." "PEM marker" / "POTS marker" would imply the watch
*detects a condition*; "management-relevant" would imply a *mechanism* (that the
state worsens if unmanaged, and that managing it helps) - neither is tested, and for
the U-dip our own null (U-dip days are not lower in felt-state) argues against the
"worsens" premise. So `PEM` and `POTS` here name **Wiggers' two management threads**
(she paces for load; she takes electrolytes for the U-dip), and any *management* is
attributed to her lived practice, never asserted by us.

### 1.2 It does NOT

- Diagnose PEM or POTS, or claim the watch detects either. The two things are
  descriptive watch signals, not clinical labels or detectors; a true orthostatic
  read needs positional / standing-HR data this device (FR245) does not record.
- Assume a mechanism. It does not claim that either state, unmanaged, worsens, nor
  that management changes it - both are untested causal / interventional claims.
- Lock a *predictive* (hypothesis-test) claim. Everything here is Layer-1
  descriptive per [CONVENTIONS section 2.1](../CONVENTIONS.md); any forecast test is
  a separate pre-registered, reviewer-mode, fresh-session-reviewed artefact.
- Re-derive the HRV-proxy validity ([`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md))
  or the U-dip primitive ([`stress_low_motion_primitive.md`](stress_low_motion_primitive.md)
  + HA11).

### 1.3 Provenance of the labels (three corrections, honest record)

The label on the second signal was walked back three times, each removing an
implicit claim it was never entitled to:

1. Wiggers has POTS and manages the U-dip with electrolytes; the participant,
   following her, asked to "look for POTS-related findings, mainly descriptive."
   Neither Wiggers nor that ask calls the U-dip a "POTS marker" - she *manages* a
   felt pattern, she does not claim the watch *detects* POTS.
2. This MD's first draft over-reached, building a "POTS-signature marker / axis" from
   `u_dip_count`. The independent peer review cut "axis" to "signal".
3. The external PubMed review ([`pots_operationalisation_wearable_review.md`](../literature/reviews/pots_operationalisation_wearable_review.md))
   then cut "POTS marker" to "as-if-orthostatic" (no precedent, off-polarity,
   posture-blind).
4. The participant then flagged that even "management-relevant signal" over-reaches -
   it presumes a mechanism (unmanaged -> worse) our own null contradicts. **Final
   floor: two distinct descriptive patterns; management is Wiggers' practice, not our
   claim.**

---

## 2. The substantive distinction being framework-ised

Wiggers (who has ME/CFS **and** POTS) interleaves two watch-visible mechanisms.
From the clean guide extraction
(`literature/wiggers_pacing_handleiding.txt`, pdftotext -raw):

- **PEM signatures** - the *load / recovery* axis: elevated resting HR after
  overexertion, HRV drop (day-over-day and multi-day even with rest), more orange
  night stress, the parasympathetic swing, longer sleep. These are the guide's
  well-structured, mostly next-day-to-multi-day patterns.
- **POTS / orthostatic signatures** - the *blood-volume / positional* axis:
  resting HR rising while lying still ("you needed more blood flow"), the stress
  **U-dip** (a sharp stress dip while body-battery rises, tied to blood volume and
  resolved with ORS / electrolytes / salt), stress that stays high on standing /
  after eating, standing-HR rise, low-blood-volume-driven dizziness. Wiggers treats
  these largely **descriptively** and notes they are managed (electrolytes,
  compression, salt) and thus **wax and wane** as symptoms change.

The project catalog captured the PEM axis and left the POTS axis almost entirely
implicit (see the labeling in section 5 and the gaps in the research note). This
MD makes the split explicit and gives it a measurement.

---

## 3. The markers (section 2.2 core choice)

### 3.1 The within-day U-dip signal (Wiggers' as-if-orthostatic side) = `u_dip_count` z

**Choice**: elevate `u_dip_count` (the per-day count of within-day stress U-dips)
against the personal lagged [d-90, d-30] trimmed baseline; a signature day = z >= 1.0.

**Label ceiling (added 2026-07-07 per the external literature review below):** this
is **NOT a validated POTS marker.** The defensible label is *"a within-day
autonomic-variability event the participant manages as if orthostatic,"* not "a POTS
marker," "a POTS axis," or "the orthostatic signal." The Wiggers link is a patient
management heuristic, not an instrument reading.

**Reasoning (four inputs per section 2.2):**

1. **Best practice**: latent-mechanism operationalisation should use the
   most-specific available observable and state its proxy status. Among this
   corpus's watch signals, the U-dip is the one Wiggers ties specifically to the
   orthostatic / blood-volume mechanism (not to generic autonomic load), so it is
   the least-ambiguous *managed-as-if-orthostatic* proxy available - but see input 2
   for why "POTS proxy" itself overreaches.
2. **Literature / source**: two legs that pull in opposite directions.
   (i) the guide's own U-dip passage (`wiggers_pacing_handleiding.txt`,
   Orthostatic-Stress chapter): "I always notice a suspicious dip in my stress where
   my body battery rises... I take electrolytes as soon as I see a U dip" - her
   personal blood-volume-management trigger, characterised in HA11.
   (ii) the **external PubMed review**
   [`literature/reviews/pots_operationalisation_wearable_review.md`](../literature/reviews/pots_operationalisation_wearable_review.md)
   caps the label: POTS is defined *everywhere* by an orthostatic HR delta (>=30 bpm
   on standing/tilt) this posture-blind device cannot compute; the within-day
   stress-trough count has **no precedent** as a POTS / orthostatic marker; and its
   **polarity runs backwards** - a stress U-dip is a transient HRV *rise* (vagal
   blip), whereas the population POTS signature is HRV *withdrawal* (reduced RMSSD/HF,
   raised LF/HF), most sharply on standing (Inbaraj 2022; Orjatsalo 2020). So the
   U-dip is not merely un-validated as orthostatic, it points the *other way* from
   the canonical POTS autonomic pattern - strengthening HA11's own "HRV-shape, not
   orthostatic-specific" caveat into a substantive objection.
3. **Our tradeoff**: `u_dip_count` is specific but narrow - one within-day autonomic
   pattern, not POTS (standing-HR, blood pressure, cerebral blood flow, and the
   orthostatic delta itself are all off-instrument). We weight **specificity over
   coverage** because the question is *separability* (are two watch markers the same
   days or different days), for which a narrow mechanism-faithful marker is more
   honest than a broad "autonomic dysregulation" composite that blurs the two. The
   r ~ 0.09 separability survives on those terms; **only the label is capped.**
4. **Our limits**: n=1; **no posture / BP / blood-volume / cerebral-blood-flow
   channel**, so the variable that *defines* POTS cannot be formed; the marker's
   polarity is off-canonical (input 2); the overnight PEM channel looks at the time
   POTS is *quietest* (asleep HR ~ normal in POTS, burden is daytime / post-waking,
   Cai 2020 - echoed in-corpus by R30 rejecting resting HR as confounder-dominated);
   and the notes carry no orthostatic-symptom vocabulary (2 of 246 signature-days
   corroborated). The one channel that would let the watch speak to POTS on the
   literature's terms is a **posture / standing-HR or orthostatic-symptom tag** - a
   prospective-logging fix (queued), not something the current record supports.

### 3.2 The overnight stress-load signal (the load / PEM side) = `stress_mean_sleep` z

**Choice**: elevate `stress_mean_sleep` (the HRV proxy; higher stress = lower HRV)
against the same lagged baseline; "PEM-signature day" = z >= 1.0.
`stress_stdev_sleep` (variability) is a secondary read (it is the one single-pool
SUPPORTED crash discriminator, HA07d).

**Reasoning**: the overnight stress mean is the guide's central PEM-load signal
(the "more orange at night" / HRV-drop family), it is the project's validated HRV
proxy ([`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md)), and it is the *load*
axis distinct from the *orthostatic* U-dip. Using the mean (not the variability)
as the primary PEM marker keeps the two markers on clearly different constructs
(mean overnight load vs within-day orthostatic dip); the variability channel is
reported alongside so the reframing does not hinge on one operationalisation.

### 3.3 The threshold

z >= 1.0 defines a "signature day" for the contingency / rate / felt-state reads.
**The threshold is not the load-bearing quantity** - the primary separability
statistic is the *threshold-free correlation* between the two continuous markers.
The threshold is a readability device; a sensitivity sweep (z in {0.75, 1.0, 1.5})
is a reasonable review-requested addition but the correlation carries the claim.

### 3.4 Alternatives considered

- **A broad "autonomic dysregulation" composite** (stress + RHR + BB + U-dip
  pooled): rejected - it would collapse the PEM/POTS distinction we are testing,
  and its weights would be an unreasoned a-priori commitment.
- **resting_hr deviation as the POTS marker** (the standing-HR / lying-still-rise
  mechanism): rejected as *primary* - RHR is shared between PEM and POTS in the
  guide (both raise it), and R30 showed the RHR level is confounder-dominated
  (weight / aging), so it is a poor mechanism-discriminating marker. It can be a
  secondary POTS read if review wants one.
- **Positional / standing-HR**: not available on this corpus (no posture tags);
  flagged as the ideal-but-absent marker.

---

## 4. Descriptive-only status + the predictive door

Per [CONVENTIONS section 2.1](../CONVENTIONS.md), this framing supports
**descriptive** reads only: separability (are the two markers correlated),
timing (per recovery phase), felt-state association (gevoelscore by group), and
notes corroboration. It licenses **no** predictive verdict. The natural predictive
follow-ups (does a POTS-signature day forecast next-day felt-state or a crash;
does the electrolyte-intervention claim Q20 hold) are separate pre-registered,
reviewer-mode, fresh-session-reviewed artefacts, and must clear the single-pool
primacy + multiplicity + autocorrelation hooks in
[CONVENTIONS section 3](../CONVENTIONS.md).

---

## 5. The catalog mechanism-labeling scheme

Each Wiggers-catalog hypothesis gets one of `PEM` / `POTS` / `both` / `neither`
(where neither = data-quality or acute-illness). The label is a **framing tag, not
a verdict**; it says which mechanism the guide statement is about, so the catalog
can carry both axes and the POTS axis stops being invisible.

Rule for assignment (applied in the catalog edit; proposed labels from the
2026-07-07 re-read):

- **PEM** where the guide statement is about load / recovery / overexertion (most
  of A/B/C/D/E/F/H).
- **POTS** where it is about blood volume / orthostatic / positional / electrolyte
  (the new orthostatic-stress family; G4 positional SpO2).
- **both** where the guide names both mechanisms for one signal (A2 lower-RHR;
  C4 / C4b "PEM or low blood volume"; G3 pressure x low-blood-volume).
- **neither** for data-quality (I-block) and acute-illness (B5).

The empirical warrant for reading them as separate signals is the separability
finding: the two markers are only weakly correlated (r ~ 0.09, 95% CI [0.03, 0.15] -
excludes zero, so weakly positive, not independent; under 1% shared variance), so
they are largely distinct days, data-supported rather than a taxonomy preference.
The label is a **signal-level** distinction, not an "axis" claim - the POTS marker
(u_dip) is a thin, sparse substrate (43% zeros), so it is a low-resolution
discriminator, not a construct that could carry an "axis" on its own.

---

## 6. Caveats (carry to every consumer)

- **Proxy, not diagnosis** (section 3.1 / 3.2). Neither marker is a clinical label.
- **Descriptive, no causal marks** (section 4). Associations at n=1, wide error;
  the felt-state gaps are small on the 1-6 scale.
- **The POTS marker is narrow** - one orthostatic pattern (U-dip), not the whole
  POTS picture; standing-HR / postprandial / dizziness are off-instrument or
  absent.
- **Notes cannot corroborate** POTS episodes on the current record (vocabulary
  gap); a prospective orthostatic-symptom tag is the fix (queued).
- **The phase-timing read is descriptive variation, not a verdict** (R19
  discipline); the 4b -> 5 decline coincides with the citalopram boundary.
- **n=1 throughout; single-pool primacy** on any comparison that could read as a
  verdict.

---

## 7. Status + review hooks

- **Status**: DRAFT, unlocked, drafted 2026-07-07 producer-mode under
  authorization. Awaiting fresh-session peer review per section 1.2.
- **Review should push on**: the u_dip-as-POTS-proxy validity (is one orthostatic
  pattern enough to carry a "POTS axis" claim); the threshold-free correlation as
  the separability statistic (vs the thresholded contingency); the descriptive vs
  predictive boundary (that no forecast claim leaks into the reframing); whether
  the felt-state group-mean gaps (4.0-4.6) are within self-report noise.
- **Section-2.2 audit hooks engaged**: section 2.1 (descriptive-only), section 3.1
  (personal lagged baseline), section 3.6 (named counts in the analysis),
  section 4.1 (no interpretive marks).

---

## 8. Cross-references

- **Analysis this frames**: [`analyses/descriptive/pem_pots_separability/findings.md`](../analyses/descriptive/pem_pots_separability/findings.md).
- **HRV proxy**: [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md).
- **U-dip primitive**: [`stress_low_motion_primitive.md`](stress_low_motion_primitive.md);
  HA11 `analyses/hypotheses/HA11-stress-udip/result.md`.
- **Recovery-phase axis (timing)**: [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md).
- **Guide source**: `literature/wiggers_pacing_handleiding.txt` (clean -raw; the
  orthostatic-stress + U-dip chapters). Catalog `../wiggers_testable_hypotheses.md`.
- **Session research note**: `../note_2026-07-07_session_consolidation_pem_pots.md`.

---

*End of methodology MD (draft).*
