# Agent-assisted import — early-stage feature sketch

*An idea for how the gevoelscore app could import a user's existing tracking data (typically a personal Excel/Google Sheet) by having an LLM interview the user about their file, design a mapping into our data model — score, tags, notes — and hand off to a deterministic importer. Relates to the "Import van bestaande tracking-data" line in the v1 scope of `app_brief_gevoelscore_v02.md`.*

> **Status: early-stage feature sketch, not a spec.** This is thinking captured while it's fresh — a direction and a set of design constraints, not a committed design or a build plan. Numbers, scope and flow will change. Nothing here is decided. It exists to be argued with by the founding cohort.

---

## 1. Why this feature is worth taking seriously

The most valuable potential users are the people who already track at home — in spreadsheets, paper diaries, Notion, or generic apps — often for years. Research and community evidence (see `pacing-and-crash-mitigation.md`) shows that despite dedicated apps like Visible and Bearable, **the spreadsheet remains the silent default** for long-haul daily logging, largely because existing apps demand too much daily input, paywall the data, or won't let people shape their own tags.

That population is exactly who this app is for, and their history is the asset: a multi-year daily series turns a brand-new user into a Tier 2/3 user (period comparisons, symptom signatures, PEM-lag) on **day one** instead of after six months of fresh logging. So a frictionless way to bring that history in is not a nice-to-have — it's an on-ramp that could decide whether an Excel veteran ever switches.

The catch is that every home-made spreadsheet is idiosyncratic: different scales (1–6 vs 1–10), date formats, mixed-language notes, tags buried in free text, a "notes" column that's really three columns. A fixed import wizard can't absorb that variety. Understanding an arbitrary, human-made schema and proposing a mapping is precisely the kind of task an LLM is genuinely good at — which is what makes this a real fit rather than AI-for-its-own-sake.

## 2. The core principle: the LLM is the cartographer, not the driver

The single most important design decision hides inside the phrase "the agent writes a script that translates the data." There are two very different versions:

- **LLM designs the mapping → deterministic code executes it.** The model interviews the user, inspects column names and sample rows, and produces a transformation *config or script* ("column C = score on a 1–10 scale; column D = free-text note; `#`-prefixed words in D = tags"). Plain code then runs the conversion. This is reproducible, inspectable, cheap, and structurally **cannot invent data**.
- **LLM transforms each row.** The model reads every row and writes the translated values. This is non-deterministic, expensive over thousands of rows, and *will* occasionally hallucinate a score or a tag.

For the dataset that is supposed to be the app's ground truth, only the first is acceptable. **Use the LLM to figure out the mapping; never to be the mapping.** This also satisfies the manifest directly — *AI is a workhorse, not an oracle*, and *the user has the last word*.

## 3. Sketch of the flow

1. **Drop the file.** User uploads their sheet/CSV.
2. **Interview.** The agent looks at headers and a handful of sample rows and asks a small number of plain-language questions: *Which column is your daily score? What scale did you use, and what did a high number mean? Which column is your note? Do you mark tags in any particular way? What's the date format?*
3. **Propose a mapping.** The agent emits a transformation config: column → field, scale interpretation, tag-extraction rule, date parsing.
4. **Preview / diff.** Before anything is committed, show the user a sample of the *result* — "this row became: score 4, note '…', suggested tags: headache, walk" — so they can correct the mapping. Reversible, confirmable.
5. **Deterministic import.** Plain code runs the confirmed mapping over the whole file. The **raw original is preserved** alongside the mapped fields, so nothing is lost and re-mapping is always possible.

## 4. Semantic landmines (all flagged by our own findings doc)

- **Scale normalisation.** Do **not** naively linear-rescale a 1–10 into our 1–6. `gevoelsscore-dashboard-findings.md` showed the user's nominal 1–10 behaved like a compressed 1–6, and that the *tails* carry the story — a dumb rescale would distort exactly the signal that matters. Detect the observed range, ask how the scale was used, and prefer importing the original scale verbatim with a documented mapping over forcing a conversion.
- **Free-text tags.** Tags extracted from old notes must be marked **inferred / suggested**, never asserted as if the user had tagged them at the time. The findings doc warns against trending symptom prevalence from free text (style drift) and against treating missing as absent — both apply here. **Notes are preserved verbatim.**
- **Provenance.** Keep the raw import next to the mapped fields. This is both a data-integrity safeguard and a direct expression of *the data is the user's*.

## 5. Privacy and security boundary

This is health data, so the manifest's security stance (local processing where possible; NEN 7510 / ISO 27001 controls where sensible) is in tension with sending years of personal notes to a cloud model. A clean split:

- The **structure interview** can use a hosted model on column names and a few sample rows.
- The **bulk transformation** runs **locally and deterministically** — the user's full note history never has to leave the device for the conversion step.

Whatever is decided, it should be stated explicitly in `SECURITY.md`. And generated transformation logic should be a **config the importer reads**, not arbitrary executable code run on the user's machine — executing LLM-generated scripts over personal files is a risk surface to avoid, not a convenience to lean on.

## 6. Scope discipline

- **Light version first.** "Agent writes and runs a script" is the most powerful *and* most dangerous form. A lighter form — LLM suggests column→field mappings and scale detection, user confirms, deterministic importer runs — likely delivers ~90% of the value at a fraction of the risk and build cost. Reserve true code-generation for genuinely weird formats, and even then have it emit a config rather than executable code.
- **One-time onboarding tool, firewalled from the daily flow.** This is an on-ramp, not part of the cardinal one-tap daily-input path. It must never bleed into the everyday entry experience.
- **Sequencing.** The v1 brief already lists import. This agentic layer is what could make import *delightful*; it can arrive with or shortly after basic import, but its weight should match its one-time nature.

## 7. Open questions

- How much should the importer try to infer tags at all on first import vs. leaving notes as-is and letting tags accrue going forward?
- Should imported history be visually marked as "imported / lower-confidence" in the dashboard, so analyses can weight it appropriately?
- Do we support re-import / merge when a user keeps their old sheet running in parallel for a while?
- What is the minimum viable interview — how few questions can reliably map the common cases (the 1–6/1–10 score + a notes column + ad-hoc tags)?

---

*Early-stage sketch, June 2026. Capture, not commitment. The load-bearing idea is the cartographer/driver split in §2; the rest is constraints to design within. Take to the founding cohort.*
