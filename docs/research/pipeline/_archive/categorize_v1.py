"""Clause-level category labelling of all day_entries notes, using the
locked v1 dictionary as the deterministic map.

Parses category_dictionary.md directly (single source of truth — no
separate YAML conversion). For each note:
  1. Segment into clauses on . , ; and conjunctions (en, maar, want, dus, of)
  2. For each clause, find substring matches per category (case-insensitive)
  3. Aggregate per day (set of categories mentioned)
  4. Cross-tabulate against crash_v1 episode windows + eras

Outputs:
  - notes-categorized.csv : per-day categories
  - notes-categorized-clauses.csv : per-clause categories (debugging)
  - categories-analysis.md : human-readable summary of patterns
"""
from __future__ import annotations

import collections
import csv
import json
import re
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES_JSON = HERE.parent / "01-language-around-crashes" / "day_entries_with_notes.json"
DICT_FILE = HERE / "category_dictionary.md"
OUT_DAY = HERE / "notes-categorized.csv"
OUT_CLAUSE = HERE / "notes-categorized-clauses.csv"
OUT_SUMMARY = HERE / "categories-analysis.md"

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3
ANALYSIS_START = date(2022, 9, 3)
ERA_SPLIT = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 3

# Clause segmentation: split on . , ; ! ? and selected conjunctions
CLAUSE_SPLIT_RE = re.compile(
    r"[.,;!?]+|\s+(?:en|maar|want|dus|of|terwijl|omdat|doordat|hoewel)\s+",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────────────────────────
# Parse the dictionary MD directly
# ─────────────────────────────────────────────────────────────────
def load_dictionary(path: Path) -> dict[str, list[str]]:
    """Parse `## category_name` headers + their immediately-following
    fenced code blocks. Returns {category: [phrases]}.
    Skips H1, sections that aren't categories (e.g. ## Open questions).
    """
    out: dict[str, list[str]] = {}
    text = path.read_text(encoding="utf-8")
    # Find each `## name` followed by ``` ... ```
    pattern = re.compile(
        r"^## (?P<name>[a-z_]+)\b[^\n]*\n+(?:(?!```)[^\n]*\n)*```\n(?P<body>(?:[^\n]+\n)+?)```",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        name = m.group("name").strip()
        body = m.group("body")
        phrases = []
        for line in body.split("\n"):
            line = line.strip().lower()
            if not line or line.startswith("#"):
                continue
            phrases.append(line)
        if phrases:
            out[name] = phrases
    return out


def segment_clauses(note: str) -> list[str]:
    """Split a note on punctuation + clause-level conjunctions."""
    pieces = CLAUSE_SPLIT_RE.split(note)
    return [p.strip() for p in pieces if p and p.strip()]


def categorize_clause(clause: str, dictionary: dict[str, list[str]]) -> list[str]:
    """Substring match (case-insensitive) against every phrase per
    category. Returns sorted list of matching categories (multi-label).
    """
    c = clause.lower()
    matched: list[str] = []
    for cat, phrases in dictionary.items():
        for p in phrases:
            if p in c:
                matched.append(cat)
                break  # one match per category is enough
    return sorted(matched)


# ─────────────────────────────────────────────────────────────────
# crash_v1 (same as everywhere)
# ─────────────────────────────────────────────────────────────────
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
    print("Loading dictionary…")
    dictionary = load_dictionary(DICT_FILE)
    print(f"  {len(dictionary)} categories: {sorted(dictionary.keys())}")
    for cat, phrases in dictionary.items():
        print(f"    {cat}: {len(phrases)} phrases")

    print("\nLoading notes…")
    entries = json.loads(NOTES_JSON.read_text(encoding="utf-8"))
    day_scores = {date.fromisoformat(e["date"]): e["score"] for e in entries if e.get("score") is not None}
    day_notes = {date.fromisoformat(e["date"]): e["note"].strip() for e in entries if e.get("note") and e["note"].strip()}
    print(f"  {len(day_scores)} day_entries, {len(day_notes)} with notes")

    episodes = find_crash_episodes(day_scores)
    print(f"  {len(episodes)} crash_v1 episodes")

    # Crash days, lead-up days, non-crash days
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
    leadup_days -= crash_days
    non_crash_days = set(day_notes.keys()) - crash_days - leadup_days

    # ─── Categorize every note ───
    per_clause_rows = []
    per_day_categories: dict[date, set[str]] = {}
    for d in sorted(day_notes.keys()):
        note = day_notes[d]
        clauses = segment_clauses(note)
        day_cats: set[str] = set()
        for i, clause in enumerate(clauses):
            cats = categorize_clause(clause, dictionary)
            if not cats:
                cats = ["context_neutraal"]
            day_cats.update(cats)
            per_clause_rows.append({
                "date": d.isoformat(),
                "clause_idx": i,
                "clause": clause,
                "categories": "|".join(cats),
            })
        per_day_categories[d] = day_cats

    # Write per-clause CSV (for debugging / inspection)
    with OUT_CLAUSE.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "clause_idx", "clause", "categories"])
        w.writeheader()
        w.writerows(per_clause_rows)
    print(f"\nwrote {OUT_CLAUSE} ({len(per_clause_rows)} clauses)")

    # Write per-day CSV
    with OUT_DAY.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        cats_sorted = sorted(dictionary.keys()) + ["context_neutraal"]
        w.writerow(["date", "score", "in_crash_episode", "is_leadup", "era", "categories", *cats_sorted])
        for d in sorted(day_notes.keys()):
            cats = per_day_categories[d]
            era = "early" if d <= ERA_SPLIT else "late"
            in_crash = d in crash_days
            is_leadup = d in leadup_days
            row = [d.isoformat(), day_scores.get(d, ""), in_crash, is_leadup, era, "|".join(sorted(cats))]
            row.extend(1 if c in cats else 0 for c in cats_sorted)
            w.writerow(row)
    print(f"wrote {OUT_DAY}")

    # ─── Cross-tabulations ───
    def rate_per_group(group_days: set[date], cat: str) -> float:
        days_with_note = [d for d in group_days if d in per_day_categories]
        if not days_with_note: return 0.0
        return sum(1 for d in days_with_note if cat in per_day_categories[d]) / len(days_with_note)

    def n_with_notes(group_days):
        return sum(1 for d in group_days if d in per_day_categories)

    n_crash = n_with_notes(crash_days)
    n_leadup = n_with_notes(leadup_days)
    n_noncrash = n_with_notes(non_crash_days)
    n_all = n_with_notes(set(day_notes.keys()))
    print(f"\n  group note-coverage:  crash={n_crash}  leadup={n_leadup}  noncrash={n_noncrash}  all={n_all}")

    all_cats = sorted(dictionary.keys()) + ["context_neutraal"]

    rate_table = []
    for cat in all_cats:
        rate_table.append({
            "category": cat,
            "rate_crash": rate_per_group(crash_days, cat),
            "rate_leadup": rate_per_group(leadup_days, cat),
            "rate_noncrash": rate_per_group(non_crash_days, cat),
            "rate_all": rate_per_group(set(day_notes.keys()), cat),
        })

    # Era breakdown for crash days
    crash_early = {d for d in crash_days if d <= ERA_SPLIT}
    crash_late = {d for d in crash_days if d > ERA_SPLIT}
    leadup_early = {d for d in leadup_days if d <= ERA_SPLIT}
    leadup_late = {d for d in leadup_days if d > ERA_SPLIT}

    era_table = []
    for cat in all_cats:
        era_table.append({
            "category": cat,
            "crash_early": rate_per_group(crash_early, cat),
            "crash_late": rate_per_group(crash_late, cat),
            "leadup_early": rate_per_group(leadup_early, cat),
            "leadup_late": rate_per_group(leadup_late, cat),
        })

    # ─── Build summary markdown ───
    md = ["# Notes — categorized clauses (Goal A.5)", ""]
    md.append("Built from the locked v1 [category_dictionary.md](category_dictionary.md) by [categorize.py](categorize.py).")
    md.append("")
    md.append("## Group sizes (days with notes)")
    md.append("")
    md.append(f"- crash days: **{n_crash}**")
    md.append(f"- lead-up days: **{n_leadup}**")
    md.append(f"- non-crash days: **{n_noncrash}**")
    md.append(f"- total with notes: **{n_all}**")
    md.append("")
    md.append("## Per-day category presence rates (proportion of days mentioning the category)")
    md.append("")
    md.append("| category | crash | leadup | non-crash | all | ratio crash/all | ratio leadup/all |")
    md.append("|----------|-----:|------:|---------:|----:|---------------:|----------------:|")
    for row in rate_table:
        r_a = row["rate_all"]
        r_c = row["rate_crash"]; r_l = row["rate_leadup"]; r_nc = row["rate_noncrash"]
        ratio_c = (r_c / r_a) if r_a > 0 else 0
        ratio_l = (r_l / r_a) if r_a > 0 else 0
        # Mark interesting deviations
        crash_marker = " ⬆" if ratio_c >= 1.5 else (" ⬇" if ratio_c <= 0.66 and r_a > 0.05 else "")
        leadup_marker = " ⬆" if ratio_l >= 1.5 else (" ⬇" if ratio_l <= 0.66 and r_a > 0.05 else "")
        md.append(
            f"| {row['category']} | {r_c:.2f}{crash_marker} | {r_l:.2f}{leadup_marker} | {r_nc:.2f} | {r_a:.2f} | {ratio_c:.2f}x | {ratio_l:.2f}x |"
        )
    md.append("")
    md.append("Markers: ⬆ = ≥1.5x overall rate (category over-represented), ⬇ = ≤0.66x and base rate > 5% (under-represented).")
    md.append("")
    md.append("## Era comparison (the K## kind-of-crash thread, finally with note data)")
    md.append("")
    md.append("| category | crash_early | crash_late | shift | leadup_early | leadup_late | shift |")
    md.append("|----------|-----------:|----------:|:-----|------------:|----------:|:-----|")
    for row in era_table:
        c_e = row["crash_early"]; c_l = row["crash_late"]
        l_e = row["leadup_early"]; l_l = row["leadup_late"]
        c_shift = c_l - c_e
        l_shift = l_l - l_e
        c_marker = " ⬆" if c_shift >= 0.1 else (" ⬇" if c_shift <= -0.1 else "")
        l_marker = " ⬆" if l_shift >= 0.1 else (" ⬇" if l_shift <= -0.1 else "")
        md.append(f"| {row['category']} | {c_e:.2f} | {c_l:.2f} | {c_shift:+.2f}{c_marker} | {l_e:.2f} | {l_l:.2f} | {l_shift:+.2f}{l_marker} |")
    md.append("")
    md.append(f"Era split at {ERA_SPLIT.isoformat()} (analytical convenience, not a real phase boundary — see synthesis).")
    md.append("Markers: ⬆/⬇ = shift of ±10 percentage points between early and late.")
    md.append("")
    md.append("## How to read this")
    md.append("")
    md.append("- The first table answers: **which kinds of clauses are over-represented before vs during crashes?** vs the baseline of all notes.")
    md.append("- The second table answers: **has the user's *language about crashes* shifted across the stabilisation transition?** Direct K## evidence at the level of subjective experience.")
    md.append("- Both tables use **per-day category presence rates** (a day with the category mentioned in ≥1 clause counts as 1 for that category), not per-clause rates, because the day is the unit of analysis for crash labelling.")
    md.append("")
    md.append("## Caveats")
    md.append("")
    md.append("- **Note coverage is uneven across years** (18% in 2022 → 71% in 2024 → 44% in 2026). The era-shift table is affected by this: the late era's averages are computed over fewer notes. Significant shifts should still hold up; subtle ones may be noise.")
    md.append("- **Substring matching is imperfect** — \"emotioneel\" matches both `belasting_emotioneel` (via the phrase \"emotioneel\") and `symptoom_emotioneel` (some emotional symptoms). Multi-labeling absorbs this fine for category-presence rates but be aware when inspecting individual clauses.")
    md.append("- **Clause segmentation is naïve** — splits on punctuation + conjunctions. A clause like \"hoofdpijn en moe\" splits into [\"hoofdpijn\", \"moe\"], which is fine for category presence; a clause like \"slecht geslapen door spanning\" stays whole because there's no clause-splitter, which is also fine (both categories fire on the whole clause).")
    md.append("- **`context_neutraal` is the residual.** A high rate of context_neutraal in a group means many clauses in that group didn't match any positive category — could mean the dictionary is missing patterns, or that the group genuinely contains a lot of mundane day-shape content.")
    md.append("")

    OUT_SUMMARY.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {OUT_SUMMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
