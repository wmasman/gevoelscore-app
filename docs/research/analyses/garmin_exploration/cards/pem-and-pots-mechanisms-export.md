# PEM and POTS: the two mechanisms the watch reads

## Authorship / status

- **Drafted** 2026-07-07 by Claude (Opus 4.8), producer-mode, under authorization.
- **Status: DRAFT - NOT for the site yet.** A synthesis card carrying claims; per
  [CONVENTIONS §1.2](../../../CONVENTIONS.md) it must clear a **fresh-session** peer
  review before it ships. It is staged for that review.
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
- **POTS / orthostatic** - the *blood-volume / positional* story: the heart racing
  on standing or lying still, the stress "U-dip," stress that stays high after
  eating - which Wiggers manages with salt, electrolytes, and compression, and which
  **comes and goes as symptoms change.**

The useful thing for the site: in this body's data these are **two different
things, on different days** - which is what the rest of this card shows.

## 2. They are separable

The two watch-markers (a POTS marker = the within-day stress U-dip; a PEM marker =
overnight stress load) correlate at only **r ≈ 0.09** - essentially independent.
Of the flagged days, most are one or the other: **169 POTS-only, 219 PEM-only, 77
both.** A reader can hold them as separate signals, not two names for one bad day.

## 3. Which POTS signal did we find, and when?

The one clearly-orthostatic signal on this watch is the **stress U-dip** (the
pattern Wiggers ties to blood volume and treats with electrolytes). We find it, and
it is **time-varying**: stronger in the earlier pacing-habit years (about 27% of
days) and **receding** in the recent medicated years (about 19%). That matches both
the earlier crash-discrimination result (HA11, where the U-dip separated crashes in
the early era and faded later) and the lived experience that the POTS picture eases
as it is managed. The standing-HR / lean-test orthostatic signals Wiggers describes
are **off-instrument** here (the watch has no posture data), so they are named as
"can't see on this device," not tested.

## 4. The counter-intuitive, honest bit

**POTS-signature days are NOT the low-felt-state days.** On days the orthostatic
U-dip fires, the felt-state (gevoelscore) is about the same as ordinary days (if
anything a touch higher). It is the **PEM** signature - the overnight load - that
coincides with feeling worse, and the worst days are when both fire together. This
is exactly Wiggers' "don't be fooled by good values": the orthostatic pattern is
*dysregulation that need not feel bad*, which is why it is easy to miss and worth
naming as its own thing.

## 5. Honesty floor (must ship with it)

- **Proxies, not diagnoses.** "POTS-signature" = the stress U-dip proxy;
  "PEM-signature" = the overnight HRV-proxy load. Neither is a clinical label, and
  a true orthostatic read would need standing-HR data this watch does not record.
- **Descriptive, n=1, wide error.** The felt-state differences are small on a 1-6
  scale; the separability is an association, not a mechanism.
- **The notes can't corroborate the POTS days** (the record has no
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
