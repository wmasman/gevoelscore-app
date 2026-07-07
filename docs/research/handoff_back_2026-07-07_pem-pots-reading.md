# Handoff back to the site: PEM/POTS review + `/reading` sources

**Status**: Stage-T (translation-to-audience) handoff from the research team back
to the site (`wiggers_research_story`). Hands off (a) the cleared PEM/POTS card,
(b) the external literature check that backs its POTS honesty-floor, and (c) a
curated set of paste-ready `/reading` source entries. Drafted 2026-07-07 by Claude
(Fable 5), producer-mode, for the participant-researcher (repo owner). Everything
below is aggregated / date-free and privacy-safe (external literature + framing
only; no corpus values).

Pairs with the site card
[`analyses/garmin_exploration/cards/pem-and-pots-mechanisms-export.md`](analyses/garmin_exploration/cards/pem-and-pots-mechanisms-export.md)
(**CLEARED FOR THE SITE 2026-07-07**), whose section 3 and section-5 honesty floor
already cite the review below. This handoff gives the site team the **reading-page**
half: the sources behind that caveat, in the site's `sources.json` shape.

---

## 1. What this hands off

The 2026-07-07 PEM/POTS reframing produced a new external-literature check on the
**POTS side** of the two-mechanism card:

> [`literature/reviews/pots_operationalisation_wearable_review.md`](literature/reviews/pots_operationalisation_wearable_review.md)
> — a PubMed operationalisation + external-validity review asking whether the
> within-day stress **U-dip** is a POTS marker others use, which POTS a wrist watch
> can see, and what it is blind to.

Its three findings are already folded into the card's honesty floor (do not
re-litigate them here; they are the copy's backing):

1. **No precedent** for a within-day stress-trough count as a POTS/orthostatic
   marker; POTS is defined by a standing heart-rate jump the FR245 cannot see (no
   posture sensor).
2. **The polarity runs backwards** — the U-dip is a transient HRV *rise* (a calming
   blip); the established POTS signature is HRV *withdrawal*.
3. **Which POTS the watch sees**: only the hyperadrenergic tonic pattern, and only
   non-specifically; the hypovolemic mechanism the U-dip is *named* for is real but
   has no device channel. **Blind to**: the orthostatic HR delta, blood pressure,
   cerebral blood flow (which falls on standing in ME/CFS + long COVID even at normal
   HR/BP), and orthostatic intolerance without tachycardia.

---

## 2. Placement decision (please pick; recommendation given)

Two different site layers are involved, and it matters which gets what:

- **The review itself → `/workings`, not `/reading`.** The reading page's own
  `_comment` scopes it to *external works the site leans on* ("Grounded in the
  research repo's `literature/README.md` bibliography"). The POTS review is an
  **internal synthesis artefact**, so it belongs with the other workings links (the
  card already points to it; the research-layer package
  [`research-layer-package-export.md`](analyses/garmin_exploration/cards/research-layer-package-export.md)
  §4 is where `/workings` collates internal reviews). **Recommendation:** link the
  review from the PEM/POTS card's "the analysis behind this" affordance and from the
  `/workings` reading list of internal reviews — **not** as a `sources.json` entry.
- **The external papers it cites → `/reading`.** These are the seven works in §3,
  ready to paste into `data/sources.json`.

If you would rather surface the review *on* `/reading` too (as a "read the full
check" pointer), that is a site call — flag it and I will shape an entry, but the
honest home is `/workings`.

---

## 3. Paste-ready `/reading` sources (`data/sources.json`)

"Some of its sources" — the review cites 17; these **seven** are the load-bearing,
general-reader-appropriate ones that back the card's claims. All URLs are canonical
DOI/PMC/publisher homes; **per `standards.md`, verify each returns HTTP 200 and
prefer the open-access (PMC) home where noted before shipping.**

### 3a. New topic family (recommended)

There is no orthostatic/POTS family yet (the closest are `hrv` and `lc`). Seven
sources justify a dedicated one. **Add to `families`** (suggested position: right
after `hrv`, before `watch`):

```json
{
  "id": "pots",
  "title": "Orthostatic intolerance & POTS",
  "blurb": "The circulation-on-standing side of the story: what POTS is, how it's diagnosed, and why a wrist watch can flag a pattern but never see the thing that actually defines it."
}
```

*Fallback if you prefer not to add a family:* slot the entries into existing
families instead — `mar-2019`, `low-2009`, `inbaraj-2022`, `ruzieh-2017` → `hrv`;
`khan-2025` → `lc`; `alfonso-2022`, `kranck-2025` → `watch`. (Change each entry's
`"family"` accordingly.)

### 3b. Entries (append to `entries`)

```json
{
  "id": "mar-2019",
  "title": "Postural Orthostatic Tachycardia Syndrome: Mechanisms and New Therapies",
  "authors": "Mar & Raj",
  "year": 2019,
  "venue": "Annual Review of Medicine 71:235-248",
  "type": "paper",
  "family": "pots",
  "key": true,
  "url": "https://doi.org/10.1146/annurev-med-041818-011630",
  "summary": "A clear map of what POTS actually is: an excessive heart-rate rise on standing, driven by one (or more) of three mechanisms, low blood volume, over-active sympathetic drive, or partial nerve damage. It is why 'POTS' on this site means a circulation-on-standing problem, and why a single watch signal can't tell the subtypes apart."
},
{
  "id": "inbaraj-2022",
  "title": "Resting heart rate variability as a diagnostic marker of cardiovascular dysautonomia in POTS",
  "authors": "Inbaraj et al.",
  "year": 2022,
  "venue": "J Basic Clin Physiol Pharmacol 34:103-109",
  "type": "paper",
  "family": "pots",
  "key": true,
  "url": "https://doi.org/10.1515/jbcpp-2022-0069",
  "summary": "Why the site is careful with the word 'POTS.' In POTS the resting autonomic balance tips toward stress, heart-rate variability sits lower, not higher. The watch pattern the guide calls a 'U-dip' is a brief move the other way (a calming blip), so it can't be read as a POTS signal; it's a pattern the participant learned to manage as if it were one."
},
{
  "id": "khan-2025",
  "title": "Cerebral Blood Flow in Orthostatic Intolerance",
  "authors": "Khan et al.",
  "year": 2025,
  "venue": "J Am Heart Assoc 14:e036752",
  "type": "paper",
  "family": "pots",
  "key": true,
  "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12074713/",
  "summary": "The honest limit, in one paper: in ME/CFS and long COVID, blood flow to the brain can fall on standing even when heart rate and blood pressure look completely normal. A wrist watch reads heart rate, so it is blind to this whole class of orthostatic trouble, the reason this site never claims the watch 'sees your POTS.'"
},
{
  "id": "low-2009",
  "title": "Postural tachycardia syndrome (POTS)",
  "authors": "Low et al.",
  "year": 2009,
  "venue": "J Cardiovasc Electrophysiol 20:352-8",
  "type": "paper",
  "family": "pots",
  "key": false,
  "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3904426/"
},
{
  "id": "ruzieh-2017",
  "title": "Effects of intermittent intravenous saline infusions in postural tachycardia syndrome",
  "authors": "Ruzieh et al.",
  "year": 2017,
  "venue": "J Interv Card Electrophysiol 48:255-260",
  "type": "paper",
  "family": "pots",
  "key": false,
  "url": "https://doi.org/10.1007/s10840-017-0225-y"
},
{
  "id": "alfonso-2022",
  "title": "Agreement between two photoplethysmography wearables for heart rate across body positions",
  "authors": "Alfonso et al.",
  "year": 2022,
  "venue": "Scientific Reports 12:15448",
  "type": "paper",
  "family": "watch",
  "key": false,
  "url": "https://www.nature.com/articles/s41598-022-18356-9"
},
{
  "id": "kranck-2025",
  "title": "Monitoring cardiorespiratory vagal desynchrony using smartwatch ECG biomarkers in long COVID",
  "authors": "Kranck et al.",
  "year": 2025,
  "venue": "Eur Heart J Case Rep 9:ytaf425",
  "type": "paper",
  "family": "watch",
  "key": false,
  "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12495029/"
}
```

### 3c. Which card claim each source backs (for `sourceRefs` wiring)

The PEM/POTS card can cite these by id (`sourceRefs: ["mar-2019", ...]` → renders as
`/reading#source-<id>`). Suggested wiring for the card's section 3 + section-5
honesty floor:

| Card claim | Source id(s) |
|---|---|
| "POTS is a standing heart-rate jump the watch can't see" | `mar-2019`, `low-2009` |
| "the U-dip's direction runs *opposite* the textbook POTS pattern" | `inbaraj-2022` |
| "the watch is blind to it (no posture); CBF can drop at normal HR/BP" | `khan-2025` |
| "which Wiggers manages with salt, electrolytes" (blood-volume mechanism is real) | `ruzieh-2017`, `mar-2019` |
| "the watch is least reliable exactly at the standing transition" | `alfonso-2022` |
| "how wearable POTS monitoring is actually done (a deliberate sit-then-stand)" | `kranck-2025` |

---

## 4. Honest-framing guidance (the floor that must travel to `/reading`)

The `key` summaries above already carry it, but three rules for whoever edits the
reading copy:

1. **Never let a POTS source imply the site detects POTS.** Every summary must keep
   the "the watch can't see the defining sign" framing. `khan-2025` and `mar-2019`
   are chosen precisely because they make the blind spot concrete; keep that.
2. **The `inbaraj-2022` summary is load-bearing, not background.** It is the one that
   makes the polarity honest (the U-dip is a *calming* blip, POTS is the reverse). If
   the reading page ever trims summaries, this one stays.
3. **"Managed with salt and electrolytes" is a real mechanism, not a watch reading.**
   `ruzieh-2017` backs that low blood volume is a genuine POTS driver treated with
   volume, but the site must not slide from "the mechanism is real" to "the watch
   measured her blood volume." The card's section 3 already draws that line; the
   reading copy should not blur it.

---

## 5. Cross-references

- Review (the `/workings` source of truth): [`literature/reviews/pots_operationalisation_wearable_review.md`](literature/reviews/pots_operationalisation_wearable_review.md) — committed `15b9569`, its full 17-source `/reading` block is in §9 there if you want more than the seven.
- Card (already cleared): [`analyses/garmin_exploration/cards/pem-and-pots-mechanisms-export.md`](analyses/garmin_exploration/cards/pem-and-pots-mechanisms-export.md).
- Methodology (still DRAFT-unlocked): [`methodology/pem_pots_mechanism_framing.md`](methodology/pem_pots_mechanism_framing.md).
- Bibliography index the sources should also land in: [`literature/README.md`](literature/README.md).
- Site reading page + data: `wiggers_research_story/site/src/pages/reading.astro`, `wiggers_research_story/site/data/sources.json` (families + entries), tiering in `src/data/index.ts`.
