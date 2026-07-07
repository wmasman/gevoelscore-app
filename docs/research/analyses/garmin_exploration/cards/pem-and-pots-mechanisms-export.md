# PEM and POTS: the two mechanisms the watch reads

## Authorship / status

- **Drafted** 2026-07-07 by Claude (Opus 4.8), producer-mode, under authorization.
- **Status: CLEARED FOR THE SITE 2026-07-07.** The independent fresh-context review
  ([`../../../reviews/pem-pots-reframing-2026-07-07.md`](../../../reviews/pem-pots-reframing-2026-07-07.md),
  MAJOR-REVISIONS folded) was accepted as the [CONVENTIONS §1.2](../../../CONVENTIONS.md)
  review; the card's claims are review-corrected. Ready for the site team to consume,
  with the section-5 honesty floor kept intact.
- **This is descriptive input for a still-open story, not a story.** The site
  narrative is malleable; this card gives the site team what the data shows about
  two mechanisms so they can weave it in however the narrative wants. It does not
  prescribe a "we used to think X" beat.
- Aggregated, privacy-safe (no dated raw values). Methodology:
  [`methodology/pem_pots_mechanism_framing.md`](../../../methodology/pem_pots_mechanism_framing.md)
  (draft); analysis
  [`analyses/descriptive/pem_pots_separability/`](../../descriptive/pem_pots_separability/).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress. The "HRV" line the site draws is an **inverted overnight-stress proxy**
> (the FR245 has HRV Status hardware-blocked), not measured HRV - this caveat must
> travel with every chart.

## 1. The two mechanisms

Wiggers (who has ME/CFS **and** POTS) reads two different things off the watch, and
so can this body's data:

- **PEM** - the *load / recovery* story: overexertion shows up as elevated resting
  HR, dropping HRV, more orange night stress, the parasympathetic swing.
- **POTS / orthostatic** (Wiggers' framing) - the *blood-volume / positional* story:
  the heart racing on standing or lying still, the stress "U-dip," stress that stays
  high after eating - which Wiggers manages with salt, electrolytes, and compression,
  and which **comes and goes as symptoms change.** (Caveat carried below: the watch
  *signal* we can measure for this side is not a validated POTS reading - see
  section 3.)

The useful thing for the site: in this body's data these are **two different
things, on different days** - which is what the rest of this card shows.

## 2. They are largely distinct

The two watch-markers (the within-day stress U-dip - Wiggers' as-if-orthostatic
signal, see section 3; and a PEM marker = overnight stress load) correlate only
**weakly** (r ≈ 0.09; they share under 1% of variance). The correlation is faintly positive, not zero - so "largely distinct,"
not "independent." Of the flagged days, most are one or the other: **169 POTS-only,
219 PEM-only, 77 both.** A reader can hold them as largely-separate signals, not two
names for one bad day.

## 3. The second signal, and the honest limit on calling it "POTS"

The second watch signal is the **stress U-dip** - the pattern Wiggers ties to blood
volume and treats with electrolytes. **Be careful with the label.** An outside
literature check (see section 5) is clear that this is **not a validated POTS
reading**: the watch cannot see the thing that *defines* POTS (the heart-rate jump
on standing - there is no posture sensor), the within-day-stress-dip approach has no
precedent in the POTS research, and the U-dip's direction actually runs *opposite*
the textbook POTS autonomic pattern (a U-dip is a brief calming/vagal blip; POTS is
the reverse). So the honest description is *"a within-day pattern the participant has
learned to manage as if it were orthostatic,"* not "the POTS signal." With that
caveat: we do find the U-dip, and it appears **more in the earlier years (about 27%
of days) than the recent years (about 19%)** - but those recent years begin exactly
at the citalopram-medication onset, so this is a *suggestive* pattern, **not a clean
time-trend** (the timeline can't separate "it eased" from "the medication era"). The
standing-HR / lean-test signals Wiggers describes are **off-instrument** (no posture
data), named as "can't see on this device," not tested.

## 4. The counter-intuitive, honest bit

**U-dip days are NOT the low-felt-state days.** On days the U-dip fires, the
felt-state (gevoelscore) is about the same as ordinary days (if anything a touch
higher) - a **genuine null** (p = 0.19). It is the **PEM**
signature - the overnight load - that coincides with feeling worse (a real,
crash-drop-robust difference), which is exactly Wiggers' "don't be fooled by good
values": the orthostatic pattern is *dysregulation that need not feel bad*, which is
why it is easy to miss and worth naming as its own thing. (An earlier "both
mechanisms together = worst day" reading was **dropped on review** - it was an
artefact of crash days, not a real felt-state effect.)

## 5. Honesty floor (must ship with it)

- **The U-dip is NOT a validated POTS reading** (external literature check,
  `pots_operationalisation_wearable_review.md`). POTS is defined by a standing
  heart-rate jump the watch can't see (no posture sensor); the within-day-stress-dip
  approach has no precedent in POTS research; and the U-dip's direction runs
  *opposite* the textbook POTS autonomic pattern. Honest label: "a within-day pattern
  the participant manages as if orthostatic," not "a POTS marker." The site must not
  present it as "we can see your POTS."
- **Proxies, not diagnoses.** Both markers are proxies (stress U-dip; overnight
  HRV-proxy load), not clinical labels.
- **Descriptive, n=1, wide error.** The felt-state differences are small on a 1-6
  scale; the separability is an association, not a mechanism.
- **The notes can't corroborate the U-dip days** (the record has no
  orthostatic-symptom vocabulary) - so this rests on the watch pattern alone.
- **The "HRV" line is a stress proxy** (device limitation), labelled as such.

## 6. Site-consumable shape (offered, not prescribed)

The site story is still open; this is one honest way the two mechanisms could sit in
it, however the narrative ends up framed:

> Some of what the watch flags is your body running out of energy (PEM). Some of it
> is your circulation struggling with standing and blood volume (POTS) - a different
> problem, on different days, that eases when it's managed with salt and
> electrolytes. Tellingly, the circulation days don't necessarily feel bad, which is
> why they're easy to miss.

Confidence: moderate for the *separability* (a clean, if proxy-based, result);
lower for the felt-state gap (small magnitudes); the proxy + descriptive caveats
must travel with it.

## 7. Cross-references

- Analysis: [`analyses/descriptive/pem_pots_separability/findings.md`](../../descriptive/pem_pots_separability/findings.md).
- Methodology: [`methodology/pem_pots_mechanism_framing.md`](../../../methodology/pem_pots_mechanism_framing.md).
- POTS substrate: HA11 (`analyses/hypotheses/HA11-stress-udip/result.md`).
- Guide: `literature/wiggers_pacing_handleiding.txt` (orthostatic-stress + U-dip
  chapters); catalog `wiggers_testable_hypotheses.md` §J.
- Session note: `note_2026-07-07_session_consolidation_pem_pots.md`.
