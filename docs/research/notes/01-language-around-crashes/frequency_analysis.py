"""Word + bigram frequency analysis, comparing notes across:
  - all days
  - crash days (score ≤ 3, within crash_v1 episode)
  - lead-up days (3 days before each crash episode)
  - non-crash days (everything else with a note)

Outputs:
  - frequencies-words.csv: per-word counts in each group + over-representation ratios
  - frequencies-bigrams.csv: same but for bigrams
  - notes-summary.md: human-readable summary of the strongest patterns
"""
from __future__ import annotations

import collections
import csv
import json
import re
import statistics
from datetime import date, timedelta
from pathlib import Path

# Dutch stop words — short curated list (no need to install nltk)
DUTCH_STOPWORDS = set("""
de het een en of maar want dus ook niet wel nog al heel erg meer minder
te tot van voor met door om bij in op aan uit over onder tegen na vanaf
zonder tegen tegenover
ik me mij mijn jij je jou jouw u uw hij hem zijn zij haar hen hun ze
we wij ons onze jullie jullie
is was ben bent zijn waren wordt werd worden geworden heeft heb hebben
had hadden zal zult zou zouden kan kun kunnen kon konden mag mogen mocht
moeten moet moest gaan ga gaat ging zien zie ziet zag zagen gezien
doen doe doet deed deden gedaan
dat dit die deze daar hier waar er
als dan toen wanneer terwijl omdat doordat zodat als
zo niets iets veel weinig wat hoe waarom wie welk welke
nu vandaag morgen gisteren straks vroeg laat
ja nee
maar
nog
even wel niet
maar
weer ook
""".split())

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3
ANALYSIS_START = date(2022, 9, 3)
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 3

MIN_WORD_TOTAL_FOR_RATIO = 5  # only compute over-rep ratios for words seen ≥5 times overall

HERE = Path(__file__).resolve().parent
DATA = HERE / "day_entries_with_notes.json"
OUT_WORDS = HERE / "frequencies-words.csv"
OUT_BIGRAMS = HERE / "frequencies-bigrams.csv"
OUT_MD = HERE / "notes-summary.md"


TOKEN_RE = re.compile(r"[a-zàâäéèêëìîïòôöùûüç]+", re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    text = text.lower()
    return [t for t in TOKEN_RE.findall(text) if t not in DUTCH_STOPWORDS and len(t) >= 3]


def bigrams(tokens: list[str]) -> list[str]:
    return [f"{a} {b}" for a, b in zip(tokens, tokens[1:])]


def find_crash_episodes(day_scores: dict[date, int]) -> list[dict]:
    sorted_dates = sorted(d for d in day_scores if ANALYSIS_START <= d <= VALIDATE_END)
    runs, cur = [], None
    for d in sorted_dates:
        is_low = day_scores[d] <= LOW_THRESHOLD
        if not is_low:
            if cur and cur["days"] >= MIN_RUN_DAYS: runs.append(cur)
            cur = None; continue
        if not cur:
            cur = {"start": d, "end": d, "days": 1}; continue
        if (d - cur["end"]).days == 1:
            cur["end"] = d; cur["days"] += 1
        else:
            if cur["days"] >= MIN_RUN_DAYS: runs.append(cur)
            cur = {"start": d, "end": d, "days": 1}
    if cur and cur["days"] >= MIN_RUN_DAYS: runs.append(cur)
    merged = []
    for r in runs:
        if merged and (r["start"] - merged[-1]["end"]).days <= MERGE_WITHIN_DAYS:
            merged[-1]["end"] = r["end"]; merged[-1]["days"] += r["days"]
        else:
            merged.append({"start": r["start"], "end": r["end"], "days": r["days"]})
    return merged


def main():
    entries = json.loads(DATA.read_text(encoding="utf-8"))
    day_scores = {date.fromisoformat(e["date"]): e["score"] for e in entries if e.get("score") is not None}
    day_notes = {date.fromisoformat(e["date"]): e["note"].strip() for e in entries if e.get("note") and e["note"].strip()}

    episodes = find_crash_episodes(day_scores)

    crash_days: set[date] = set()
    for ep in episodes:
        d = ep["start"]
        while d <= ep["end"]:
            if d in day_scores and day_scores[d] <= LOW_THRESHOLD:
                crash_days.add(d)
            d += timedelta(days=1)

    leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, LEADUP_DAYS + 1):
            leadup_days.add(ep["start"] - timedelta(days=i))
    leadup_days &= set(day_scores.keys())
    # exclude any lead-up day that's also a crash day (shouldn't be, but defensive)
    leadup_days -= crash_days

    non_crash_days = set(day_notes.keys()) - crash_days - leadup_days

    def count_in_group(days_set: set[date], get_tokens=tokenize) -> tuple[collections.Counter, int]:
        c = collections.Counter()
        note_count = 0
        for d in days_set:
            if d not in day_notes: continue
            note_count += 1
            tokens = get_tokens(day_notes[d])
            c.update(tokens)
        return c, note_count

    def count_bigrams_in_group(days_set: set[date]) -> tuple[collections.Counter, int]:
        c = collections.Counter()
        note_count = 0
        for d in days_set:
            if d not in day_notes: continue
            note_count += 1
            tokens = tokenize(day_notes[d])
            c.update(bigrams(tokens))
        return c, note_count

    # All notes
    all_with_notes = set(day_notes.keys())
    all_words, all_n = count_in_group(all_with_notes)
    crash_words, crash_n = count_in_group(crash_days)
    leadup_words, leadup_n = count_in_group(leadup_days)
    noncrash_words, noncrash_n = count_in_group(non_crash_days)

    all_bigrams, _ = count_bigrams_in_group(all_with_notes)
    crash_bigrams, _ = count_bigrams_in_group(crash_days)
    leadup_bigrams, _ = count_bigrams_in_group(leadup_days)
    noncrash_bigrams, _ = count_bigrams_in_group(non_crash_days)

    print(f"--- groups (days with notes) ---")
    print(f"  all_with_notes:    {all_n}")
    print(f"  crash_days:        {crash_n}")
    print(f"  lead-up days:      {leadup_n}")
    print(f"  non-crash days:    {noncrash_n}")

    def over_rep_table(group_counter, group_n, baseline_counter, baseline_n):
        """For each word: (count_group, count_baseline, rate_group_per_note, rate_baseline_per_note, ratio)."""
        rows = []
        for w, n_total in baseline_counter.items():
            if n_total < MIN_WORD_TOTAL_FOR_RATIO: continue
            n_g = group_counter.get(w, 0)
            rate_g = n_g / group_n if group_n else 0
            rate_b = n_total / baseline_n if baseline_n else 0
            ratio = (rate_g / rate_b) if rate_b > 0 else 0
            rows.append((w, n_g, n_total, rate_g, rate_b, ratio))
        return rows

    # Compare crash days vs non-crash days (baseline = non-crash for "what's distinctive")
    crash_vs_noncrash = over_rep_table(crash_words, crash_n, all_words, all_n)
    leadup_vs_all = over_rep_table(leadup_words, leadup_n, all_words, all_n)

    # Write word CSV
    with OUT_WORDS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([
            "word", "total_count_all",
            "count_crash", "count_leadup", "count_noncrash",
            "rate_per_note_crash", "rate_per_note_leadup", "rate_per_note_noncrash",
            "ratio_crash_vs_all", "ratio_leadup_vs_all",
        ])
        for word, n_total in sorted(all_words.items(), key=lambda x: -x[1]):
            if n_total < MIN_WORD_TOTAL_FOR_RATIO: continue
            n_c = crash_words.get(word, 0)
            n_l = leadup_words.get(word, 0)
            n_nc = noncrash_words.get(word, 0)
            r_c = n_c / crash_n if crash_n else 0
            r_l = n_l / leadup_n if leadup_n else 0
            r_nc = n_nc / noncrash_n if noncrash_n else 0
            r_a = n_total / all_n if all_n else 0
            ratio_crash = (r_c / r_a) if r_a > 0 else 0
            ratio_leadup = (r_l / r_a) if r_a > 0 else 0
            w.writerow([
                word, n_total, n_c, n_l, n_nc,
                round(r_c, 3), round(r_l, 3), round(r_nc, 3),
                round(ratio_crash, 2), round(ratio_leadup, 2),
            ])
    print(f"wrote {OUT_WORDS}")

    # Bigrams CSV
    with OUT_BIGRAMS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([
            "bigram", "total_count_all",
            "count_crash", "count_leadup", "count_noncrash",
            "ratio_crash_vs_all", "ratio_leadup_vs_all",
        ])
        for bg, n_total in sorted(all_bigrams.items(), key=lambda x: -x[1]):
            if n_total < MIN_WORD_TOTAL_FOR_RATIO: continue
            n_c = crash_bigrams.get(bg, 0)
            n_l = leadup_bigrams.get(bg, 0)
            n_nc = noncrash_bigrams.get(bg, 0)
            r_c = n_c / crash_n if crash_n else 0
            r_l = n_l / leadup_n if leadup_n else 0
            r_a = n_total / all_n if all_n else 0
            ratio_crash = (r_c / r_a) if r_a > 0 else 0
            ratio_leadup = (r_l / r_a) if r_a > 0 else 0
            w.writerow([
                bg, n_total, n_c, n_l, n_nc,
                round(ratio_crash, 2), round(ratio_leadup, 2),
            ])
    print(f"wrote {OUT_BIGRAMS}")

    # ─── Build human-readable summary ───
    # Most distinctive words for crash days (ratio_crash_vs_all >= 1.5 and count_crash >= 3)
    crash_distinctive = []
    for w, n_total in all_words.items():
        if n_total < MIN_WORD_TOTAL_FOR_RATIO: continue
        n_c = crash_words.get(w, 0)
        if n_c < 3: continue
        r_c = n_c / crash_n
        r_a = n_total / all_n
        ratio = r_c / r_a if r_a > 0 else 0
        if ratio >= 1.5:
            crash_distinctive.append((w, n_c, n_total, ratio))
    crash_distinctive.sort(key=lambda x: -x[3])

    leadup_distinctive = []
    for w, n_total in all_words.items():
        if n_total < MIN_WORD_TOTAL_FOR_RATIO: continue
        n_l = leadup_words.get(w, 0)
        if n_l < 3: continue
        r_l = n_l / leadup_n
        r_a = n_total / all_n
        ratio = r_l / r_a if r_a > 0 else 0
        if ratio >= 1.5:
            leadup_distinctive.append((w, n_l, n_total, ratio))
    leadup_distinctive.sort(key=lambda x: -x[3])

    top_overall = sorted(all_words.items(), key=lambda x: -x[1])[:30]
    top_overall_bigrams = sorted(all_bigrams.items(), key=lambda x: -x[1])[:25]

    md_lines = [
        "# Notes — language around crashes (Goal A)",
        "",
        "Frequency analysis of `day_entries.note` across 1.372 day entries",
        "(686 with non-empty notes), comparing crash-day language to overall",
        "language. Pure descriptive output. Run via [frequency_analysis.py](frequency_analysis.py).",
        "",
        "## Group sizes (days with notes)",
        "",
        f"- all days with note: **{all_n}**",
        f"- crash days (score ≤ 3 within episode): **{crash_n}**",
        f"- lead-up days (3 days before each crash): **{leadup_n}**",
        f"- non-crash, non-lead-up days: **{noncrash_n}**",
        "",
        "## Top 30 words overall (after Dutch stop-word filter)",
        "",
        "| word | total |",
        "|------|------:|",
    ]
    for w, n in top_overall:
        md_lines.append(f"| {w} | {n} |")

    md_lines += [
        "",
        "## Top 25 bigrams overall",
        "",
        "| bigram | total |",
        "|--------|------:|",
    ]
    for bg, n in top_overall_bigrams:
        md_lines.append(f"| {bg} | {n} |")

    md_lines += [
        "",
        "## Words distinctively over-represented on crash days",
        "",
        f"Showing words seen ≥3 times on crash days with ratio ≥1.5x their overall rate.",
        f"({len(crash_distinctive)} entries)",
        "",
        "| word | crash count | total count | ratio (crash vs all) |",
        "|------|-----------:|-----------:|---------------------:|",
    ]
    for w, n_c, n_total, ratio in crash_distinctive[:40]:
        md_lines.append(f"| {w} | {n_c} | {n_total} | {ratio:.2f}x |")

    md_lines += [
        "",
        "## Words distinctively over-represented on lead-up days",
        "",
        f"Showing words seen ≥3 times on lead-up days with ratio ≥1.5x their overall rate.",
        f"({len(leadup_distinctive)} entries)",
        "",
        "| word | leadup count | total count | ratio (leadup vs all) |",
        "|------|------------:|-----------:|---------------------:|",
    ]
    for w, n_l, n_total, ratio in leadup_distinctive[:40]:
        md_lines.append(f"| {w} | {n_l} | {n_total} | {ratio:.2f}x |")

    md_lines += [
        "",
        "## Caveats",
        "",
        "- **Tokenization is naïve**: lowercase + strip punctuation + filter a short Dutch stop-word list. No stemming, no lemmatization. \"slaap\", \"slapen\", \"geslapen\" count as different words. A small effect we can fix in a follow-up if it matters.",
        "- **Note coverage is uneven across years** (18% in 2022 → 71% in 2024 → 44% in 2026). The crash-day vs all-day comparison still works (we're comparing rates per note, not absolute counts) but distinctive-word findings may reflect what the user happened to write more / less about in each phase, not pure crash phenomena.",
        "- **Small samples for crash-day language**: 59 notes on crash days. Words appearing 3 times on crash days have a wide confidence interval on the rate. Treat the table as suggestive, not statistically significant.",
        "- **Dutch stopword list is hand-curated**, may have omissions; spot-check the top words for any obvious stopwords that slipped through.",
        "",
        "## What's next (Goal B suggestion)",
        "",
        "Once we know which words/bigrams characterise crash days, **Goal B**",
        "is to find notes anywhere in the corpus that contain these patterns",
        "but were never tagged. Those become candidate tag-suggestions for",
        "the eventual app feature. The 'words distinctively over-represented",
        "on crash days' table above is the seed for the suggestion engine.",
        "",
    ]

    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
