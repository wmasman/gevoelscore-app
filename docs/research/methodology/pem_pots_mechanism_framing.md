# PEM vs POTS mechanism framing: separability markers + catalog labeling (methodology)

## Authorship

- **Drafted**: 2026-07-07 by Claude (Opus 4.8), producer-mode, under explicit
  authorization from the participant-researcher (repo owner).
- **Status**: **DRAFT - NOT LOCKED.** Revisable freely until the participant
  accepts. Per [CONVENTIONS section 1.2](../CONVENTIONS.md) (drafting under
  reviewer-mode-with-authorization), the peer review of this MD must run in a
  **different session** (fresh cold read, doc-only knowledge) before it locks.
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

1. A **PEM-signature marker** and a **POTS-signature marker** at the day level, as
   watch-data proxies, for *descriptive* separability / timing / felt-state reads
   (the analysis at
   [`analyses/descriptive/pem_pots_separability/`](../analyses/descriptive/pem_pots_separability/)).
2. A **mechanism label** (`PEM` / `POTS` / `both` / `neither`) applied to each
   Wiggers-catalog hypothesis, so the catalog stops being implicitly PEM-only.

### 1.2 It does NOT

- Diagnose POTS or PEM. The markers are watch-signal proxies, not clinical labels;
  a true orthostatic read needs positional / standing-HR data this device (FR245)
  does not record.
- Lock a *predictive* (hypothesis-test) claim. Everything here is Layer-1
  descriptive per [CONVENTIONS section 2.1](../CONVENTIONS.md); any forecast test
  (e.g. "a POTS-signature day predicts next-day X") is a separate pre-registered
  artefact, reviewer-mode, fresh-session reviewed.
- Re-derive the HRV-proxy validity (that lives in
  [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md)) or the U-dip primitive
  (that lives in [`stress_low_motion_primitive.md`](stress_low_motion_primitive.md)
  + HA11).

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

### 3.1 POTS-signature marker = within-day stress U-dip (`u_dip_count` z)

**Choice**: elevate `u_dip_count` (the per-day count of within-day stress U-dips)
against the personal lagged [d-90, d-30] trimmed baseline; a "POTS-signature day"
= z >= 1.0.

**Reasoning (four inputs per section 2.2):**

1. **Best practice**: latent-mechanism operationalisation should use the
   *most-specific available observable*, and state its proxy status. Among this
   corpus's watch signals, the U-dip is the one Wiggers ties *specifically* to the
   orthostatic / blood-volume mechanism (not to generic autonomic load), so it is
   the least-ambiguous POTS proxy available.
2. **Literature / source**: the guide's own U-dip passage
   (`wiggers_pacing_handleiding.txt`, the Orthostatic-Stress chapter): "I always
   notice a suspicious dip in my stress where my body battery rises... I take
   electrolytes as soon as I see a U dip." The U-dip is her personal
   POTS-management trigger. The project already has HA11 characterising it.
3. **Our tradeoff**: `u_dip_count` is *specific but narrow* - it captures one
   orthostatic pattern, not the whole POTS picture (standing-HR, postprandial
   stress, dizziness are off-instrument or absent). We weight **specificity over
   coverage**: a narrow but mechanism-faithful marker is more honest for a
   separability claim than a broad "autonomic dysregulation" composite that would
   blur PEM and POTS together (which is exactly the thing we are trying to
   separate).
4. **Our limits**: n=1; no positional data; the notes carry no orthostatic-symptom
   vocabulary (2 of 246 signature-days corroborated), so the marker cannot be
   validated against felt orthostatic symptoms on the current record - a
   prospective-logging gap, stated, not hidden.

### 3.2 PEM-signature marker = overnight stress (`stress_mean_sleep` z)

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
