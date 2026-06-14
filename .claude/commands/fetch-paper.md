---
description: Fetch an open-access research paper PDF, store it in docs/research/literature/ with the project naming convention, and add a one-line entry to the literature README index. Use when the user asks to "download this paper", "get the PDF for X", or to fetch a batch of references.
---

# Fetch Paper

Workflow for pulling an OA research paper into [docs/research/literature/](../../docs/research/literature/) with the project's naming + indexing convention, and for failing fast on paywalled refs instead of wasting effort.

## When to use

- User gives one or more citations / DOIs / titles to download.
- User asks "can you fetch the PDFs for the tier-1 refs?" after a literature scan.
- A new external paper is mentioned in another doc and needs to be archived locally.

**Do NOT use this for**: writing literature reviews, summarising papers, generating citations, or anything other than retrieving + filing the PDF.

## Inputs

One of:
- A DOI: `10.1038/s41746-026-02543-3`
- A full citation: `Aitken et al. (2026), npj Digital Medicine 9:257`
- A title + author + year
- A list of any of the above (batch mode — parallelise)

If the input is ambiguous, ask before downloading.

---

## Storage convention (DO NOT vary)

- **Location**: `docs/research/literature/`
- **Filename**: `firstauthor_year_short_topic.pdf` — snake_case, lowercase, short topic 3-6 words.
  - ✅ `aitken_2026_visible_biomarkers_symptom_prediction.pdf`
  - ✅ `quer_2020_daily_rhr_variability_n92k.pdf`
  - ❌ `Aitken-2026.pdf` / `paper.pdf` / `doi_10_1038_s41746...`
- **Indexing**: every successful download gets ONE row appended to [docs/research/literature/README.md](../../docs/research/literature/README.md) — author + year + journal/venue + concise relevance hook + (PMC ID if route was Europe PMC, COI flag if relevant).
- **Match existing row format** in that README. Don't invent a new column structure.

---

## Step-by-step

### 1. Identify the paper

If you only have a title/author/year, get the DOI first:

```bash
curl -sL -A "Mozilla/5.0" "https://api.crossref.org/works?query.title=<TITLE>&query.author=<AUTHOR>&rows=3"
```

Crossref has no auth and effectively no rate limit. Confirm DOI + journal + year + first author match.

### 2. Pick the route

Try these in order. STOP at the first that returns a valid PDF.

| Publisher / venue | URL pattern | Notes |
|---|---|---|
| **PLOS** | `https://journals.plos.org/plosone/article/file?id=<DOI>&type=printable` | Reliable, no auth |
| **Nature family** (Nature, Nat Commun, Sci Rep, npj *) | `https://www.nature.com/articles/<doi-suffix>.pdf` | curl handles the auth-cookie redirect transparently with `-L`. WebFetch fails on the IDP redirect — use Bash curl |
| **Frontiers** | `https://www.frontiersin.org/articles/<DOI>/pdf` | Reliable |
| **BMJ** | `https://<subdomain>.bmj.com/content/<vol>/<issue>/<id>.full.pdf` | e.g. `gh.bmj.com` for BMJ Global Health |
| **JMIR** | `https://<subjournal>.jmir.org/<year>/<issue>/<eid>/PDF` | e.g. `medinform.jmir.org` |
| **MDPI direct** | ❌ Akamai-blocks `curl`. **Skip and go straight to Europe PMC** | |
| **Elsevier / Cell (OA papers)** | ❌ ScienceDirect blocks `curl`. **Use Europe PMC for NIH-funded papers** | |
| **Wiley (BRONZE-OA)** | ❌ Anti-bot blocks even free papers. Last resort only | |
| **Project Euclid** (Annals of Statistics, Annals of Probability, IMS journals) | ❌ Imperva Incapsula blocks `curl`. Annals papers are Bronze-OA in a real browser but not via `curl`. No Europe PMC fallback (these aren't biomedical) — flag for manual browser download | |
| **BMJ direct** (main journal, not BMJ Glob Health) | ❌ Anti-bot on `bmj.com/content/.../full.pdf`. **Use Europe PMC** — BMJ papers get PMC IDs | |
| **arXiv** | `https://arxiv.org/pdf/<arxiv-id>` (no `.pdf` suffix needed) | ✅ Reliable, no auth. Often the best route for math/stats/CS/physics papers — Unpaywall surfaces it as `oa_status: green`. Older final-published versions may differ in section numbering from the preprint; flag this when section/page references matter | |
| **Medical Research Archives (esmed.org)** | Hit the landing page, grep `citation_pdf_url` meta tag for the direct file URL | |

### 3. Europe PMC fallback (the workhorse)

When publisher-direct fails on MDPI / Elsevier / any closed-stack journal: find the PMC ID via DOI, then hit Europe PMC's getPdf API. **This is the single most useful trick in this skill.**

```bash
# Step A: DOI → PMC ID
curl -sL -A "Mozilla/5.0" \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=<DOI>&retmode=json"
# → "idlist":["10137929"] means PMC10137929

# Step B: PMC ID → PDF
curl -sL -A "Mozilla/5.0" -o <filename>.pdf \
  "https://europepmc.org/api/getPdf?pmcid=PMC<ID>"
```

**Why this works when PMC itself doesn't:** the canonical PMC PDF URL (`pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx/pdf/`) now serves a JavaScript proof-of-work challenge that blocks `curl`. The Europe PMC mirror at `europepmc.org/api/getPdf?pmcid=...` serves the same NIH-deposited PDFs directly without challenge.

This route works for: MDPI papers (they deposit to PMC), NIH-funded Cell/Elsevier papers (deposited as `nihms-XXXXXXX.pdf` manuscript copies), and most other PMC-indexed papers.

### 4. Verify EVERY download

Curl always returns exit 0 for HTTP 200 even if the body is an HTML error page. Magic-byte check is non-negotiable:

```bash
head -c 5 <filename>.pdf | xxd
# ✅ Expect: 2550 4446 2d  ("%PDF-")
# ❌ "<HTML" or "....<" (0a0a0a0a3c) means HTML stub — retry with a different route
```

Common stub signatures:
- `<HTML>...Access Denied` (≤500 bytes) → MDPI Akamai block
- `<html>...Preparing to download...` (1817 bytes) → PMC proof-of-work challenge
- `<html style="height:100%">...Incapsula_Resource` (~1.2 KB) → Project Euclid (and other Imperva-fronted) anti-bot wall
- `<!DOCTYPE html>...<html lang="en"` (50+ KB) → Wiley landing page
- HTML <100 KB starting with `<!DOC` → almost any government / publisher landing page where `curl` followed a wrong link
- `0a0a0a0a3c` magic ("\n\n\n\n<") → any JS-heavy landing page

### 5. Unpaywall — upfront OA discovery, not just last-resort

Unpaywall can be called **before** or **after** the publisher-direct attempt. Calling it upfront is especially valuable for math / stats / CS / physics — it surfaces arXiv preprints (`oa_status: green`) you'd otherwise miss, and tells you when a paper is `bronze` at a publisher that anti-bot-blocks (saves a wasted attempt).

```bash
curl -sL "https://api.unpaywall.org/v2/<DOI>?email=<user_email>"
# Look for: "oa_status", "best_oa_location.url_for_pdf", "has_repository_copy"
```

Interpreting `oa_status`:
- `gold` → publisher OA, fully open (PLOS, Frontiers, BMC, Nature Comm, Sci Rep, npj). Use the publisher direct route.
- `hybrid` → paywalled journal but this specific article is OA. Publisher direct usually works (BMJ Statements, Elsevier OA, etc.).
- `green` → preprint exists in a repository (arXiv, institutional repo, ResearchGate via author). Often the easiest route to fetch.
- `bronze` → free at the publisher but no license. Often anti-bot-blocked (Wiley, Project Euclid). Flag for manual browser download.
- `closed` → genuinely paywalled. Stop and report.

If Unpaywall returns `is_oa: false` OR every listed URL is the same blocked publisher endpoint we already tried, **report the paper as paywalled and stop**. Do NOT attempt Sci-Hub, LibGen, or any other piracy route. Offer the user three legitimate alternatives:

1. Open the publisher landing page in a browser — anti-bot blocks affect `curl`, not real browsers.
2. Use institutional access (university library proxy, NWO, etc.).
3. Email the corresponding author — academic reprint requests are normal and usually answered within a day.

For chemistry, physics, math, stats, CS papers specifically: also check Semantic Scholar's `openAccessPdf.status` — sometimes it knows about an author preprint that Unpaywall has not crawled yet.

### 6. Index in the README

Append ONE row to [docs/research/literature/README.md](../../docs/research/literature/README.md) right after the last existing row. Use the same Markdown table format as the surrounding rows. Include:

- The local filename as a clickable link.
- Author(s), year, journal, volume/page.
- A one-line **relevance hook for this project** — what hypothesis it bears on, which existing methodology doc it anchors, or what mechanism it covers. Not a general abstract.
- PMC ID if the route was Europe PMC (so a future fetch knows the fallback worked).
- COI / conflict-of-interest flag if relevant (e.g. company-employee authorship).

Mirror the tone of existing rows — concise, scannable, project-specific.

### 7. Cleanup

- If a previous failed attempt left a stub file with the same name, your successful download already overwrites it.
- Stray test files belong in `c:\tmp\`, never in `docs/research/literature/`.
- Don't delete pre-existing files without asking — `rm` may be denied (it has been before).

---

## Batch mode

When the user gives 5+ papers, structure the work:

1. **One TodoWrite task per paper** (and one for the README index update at the end). Helps the user follow progress.
2. **Parallelise downloads** — same-host concurrency is fine, but cap at ~6 simultaneous to be polite to publisher servers.
3. **Verify each as it lands**, don't batch verifications at the end — easier to retry route per-paper.
4. **Single README update at the end**, after all verifications. One Edit, multiple rows. Don't update the README per-paper.
5. **Report a final summary table** to the user: filename / size / route / status (✅ / ❌ paywalled / ⚠️ stub).

---

## What to report back

For each paper:
- Filename + size + magic-byte confirmation
- Route used (which of steps 2-3 succeeded)
- For paywalled ones: which OA databases were checked (Unpaywall, Semantic Scholar, Crossref, NCBI) and what they said. Do not silently drop a failed paper.

For the batch as a whole:
- Total successful / failed / skipped
- README rows added
- Any noteworthy methodological hits (e.g. "Aitken 2026 directly tests the same within-person HRV→symptom direction as Wiggers register A1–B3")

---

## Anti-patterns to avoid

- ❌ Writing a literature review along with the download — that's the user's call afterwards, not part of fetching.
- ❌ Generating filenames from the title rather than the first-author + year + topic short form.
- ❌ Downloading without magic-byte verification (curl exit 0 doesn't mean success).
- ❌ Retrying the same blocked URL with cosmetic header tweaks — pivot to Europe PMC fast.
- ❌ Asking the user "shall I download?" for refs they've already named — just do it.
- ❌ Bulk-deleting or moving existing files in `docs/research/literature/` without explicit instruction.
- ❌ Attempting Sci-Hub / LibGen / shadow libraries when a paper is paywalled. Use the three legitimate alternatives in step 5 instead.

---

## Session-learnt URL patterns (quick reference)

Confirmed-working PDF endpoints for journals already used in this project:

| Journal | URL pattern |
|---|---|
| PLOS ONE | `https://journals.plos.org/plosone/article/file?id=<DOI>&type=printable` |
| npj Digital Medicine | `https://www.nature.com/articles/<doi-suffix>.pdf` |
| Nature Communications | `https://www.nature.com/articles/<doi-suffix>.pdf` |
| Scientific Reports | `https://www.nature.com/articles/<doi-suffix>.pdf` |
| Frontiers in Public Health | `https://www.frontiersin.org/articles/10.3389/fpubh.YYYY.NNNNNN/pdf` |
| Frontiers in Psychiatry | `https://www.frontiersin.org/articles/10.3389/fpsyt.YYYY.NNNNNN/pdf` |
| Frontiers in Cardiovascular Medicine | `https://www.frontiersin.org/articles/10.3389/fcvm.YYYY.NNNNNN/pdf` |
| BMJ Global Health | `https://gh.bmj.com/content/<vol>/<issue>/<id>.full.pdf` |
| JMIR Medical Informatics | `https://medinform.jmir.org/<year>/<issue>/<eid>/PDF` |
| Medical Research Archives (esmed.org) | `https://esmed.org/MRA/mra/article/download/<artid>/<galleyid>` — find galleyid in landing page `citation_pdf_url` meta tag |
| arXiv (math, stats, CS, physics preprints) | `https://arxiv.org/pdf/<arxiv-id>` — no auth, no `.pdf` suffix needed. Often the only OA route for math/stats. **Caveat**: arXiv version may differ from journal version in section numbering — flag if section/page references are load-bearing in the citation |
| US government docs (IES, NIH, CDC) | Hit the topic landing page (e.g. `ies.ed.gov/ncee/wwc/handbooks`), grep `href="...\.pdf"` for the actual PDF URL — landing pages often link to multiple versions (v4.1 vs v5.0 of the WWC handbook, etc.). Don't trust WebFetch's URL guess; verify by fetching the index page first |
| MDPI (any journal: Healthcare, Pathophysiology, etc.) | **Skip direct.** Go via Europe PMC: `https://europepmc.org/api/getPdf?pmcid=PMC<id>` |
| BMJ main journal (not BMJ Glob Health) | **Skip direct.** Go via Europe PMC — BMJ papers have PMC IDs |
| Cell / Elsevier OA (NIH-funded) | **Skip ScienceDirect.** Go via Europe PMC `nihms-XXXXXXX.pdf` manuscript copy |
| Project Euclid (Annals of Statistics / Probability, IMS journals) | **Imperva Incapsula blocks `curl`** — no `curl` workaround. Flag for manual browser download; the PDF IS Bronze-OA in a real browser. Paste the Project Euclid URL Unpaywall gives you straight into the user's browser bar |
| Wiley (any journal, including BRONZE-OA) | Anti-bot blocks `curl` even on free papers. Flag for manual browser download or check if the paper has a PMC mirror |

Update this table when you learn a new working pattern.

## Routes by Unpaywall `oa_status`

When you do call Unpaywall upfront, the `oa_status` field tells you which sub-routine of the route table to enter:

| oa_status | What it means | Where to go |
|---|---|---|
| `gold` | OA journal | Publisher direct URL (PLOS, Frontiers, BMC, npj, Nat Commun, Sci Rep) |
| `hybrid` | Paywalled journal, this article is OA | Publisher direct usually works (BMJ Statements, Elsevier OA, Wiley Online Open) |
| `green` | Preprint in a repository | arXiv / institutional repo. Check `oa_locations[].url_for_pdf` for the canonical preprint URL |
| `bronze` | Free at publisher, no license | Often anti-bot-blocked. Try publisher direct once; if blocked, manual browser download |
| `closed` | Genuinely paywalled | Stop. Suggest author reprint / institutional access |

If multiple OA locations exist, prefer in this order: **repository (green) → publisher OA (gold/hybrid) → publisher bronze**. Repository copies are almost never anti-bot-blocked.
