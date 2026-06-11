"""v2 — three-layer clause categorizer.

Layer 1 (categories) — same as v1, with verification-surfaced gaps fixed.
Layer 2 (modifiers) — negation + severity_mild + severity_severe.
  Apply when a `symptoom_*` phrase matches: look at the 3 words BEFORE
  the matched phrase in the same clause for negation / severity_*
  modifiers. Sets symptom_state to absent / mild / present (default) /
  severe.
Layer 3 (polarity) — clause-level positive / negative valence based on
  independent polarity-marker phrases anywhere in the clause.
  Negation of a symptom boosts clause polarity toward positive.

Outputs:
  - notes-categorized-v2-clauses.csv  : per clause: categories, symptom_states, polarity
  - notes-categorized-v2.csv          : per day aggregates
  - categories-analysis-v2.md         : updated cross-tabs vs v1
"""
from __future__ import annotations

import collections
import csv
import json
import re
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES_JSON = HERE.parent / "01-language-around-crashes" / "day_entries_with_notes.json"
DICT_FILE = HERE / "category_dictionary_v2.md"
OUT_DAY = HERE / "notes-categorized-v2.csv"
OUT_CLAUSE = HERE / "notes-categorized-v2-clauses.csv"
OUT_SUMMARY = HERE / "categories-analysis-v2.md"

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3
ANALYSIS_START = date(2022, 9, 3)
ERA_SPLIT = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 3
NEGATION_WINDOW_WORDS = 3

CLAUSE_SPLIT_RE = re.compile(
    r"[.,;!?]+|\s+(?:en|maar|want|dus|of|terwijl|omdat|doordat|hoewel)\s+",
    re.IGNORECASE,
)

# Names that distinguish layers (must match the ### headings in dictionary v2)
# v2.1 additions 2026-06-10: added `medicatie` for naproxen et al.
CATEGORY_NAMES = {
    "belasting_fysiek", "belasting_cognitief", "belasting_emotioneel",
    "belasting_sociaal", "belasting_gezin",
    "symptoom_fysiek", "symptoom_cognitief", "symptoom_emotioneel",
    "recovery_actie", "triggers_extern", "medicatie", "context_neutraal",
}
SYMPTOM_CATEGORIES = {"symptoom_fysiek", "symptoom_cognitief", "symptoom_emotioneel"}
MODIFIER_NAMES = {"negation", "severity_mild", "severity_severe"}
POLARITY_NAMES = {"polarity_positive", "polarity_negative"}

# Severity ordering for day-level aggregation
SEVERITY_ORDER = {"absent": 0, "mild": 1, "present": 2, "severe": 3}


def load_dictionary(path: Path) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    """Returns (categories, modifiers, polarity_markers).

    Manual parse: scan line by line. Each `### name` heading opens a section;
    the first fenced ``` block that appears before the NEXT `### ` heading or
    `## ` heading is that section's body. Sections without a code block
    (like context_neutraal which is purely residual) have no phrases.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    all_lists: dict[str, list[str]] = {}

    heading_re = re.compile(r"^### (?P<name>[a-z_]+)\b")
    h2_re = re.compile(r"^## ")
    in_code = False
    current_section: str | None = None
    current_phrases: list[str] = []

    for line in lines:
        # New ## section ends any current ### subsection (no code block claimed → no entry)
        if h2_re.match(line):
            current_section = None
            current_phrases = []
            in_code = False
            continue
        # New ### subsection starts
        m = heading_re.match(line)
        if m:
            current_section = m.group("name")
            current_phrases = []
            in_code = False
            continue
        # Code fence toggle
        if line.strip().startswith("```"):
            if not in_code and current_section is not None:
                in_code = True
                current_phrases = []
            elif in_code and current_section is not None:
                # closing fence — commit phrases for this section if any
                if current_phrases:
                    all_lists[current_section] = current_phrases[:]
                in_code = False
                current_section = None  # only first code block per ### is taken
                current_phrases = []
            continue
        if in_code and current_section is not None:
            ln = line.strip().lower()
            if ln and not ln.startswith("#"):
                current_phrases.append(ln)

    categories = {n: all_lists[n] for n in CATEGORY_NAMES if n in all_lists}
    modifiers = {n: all_lists[n] for n in MODIFIER_NAMES if n in all_lists}
    polarity = {n: all_lists[n] for n in POLARITY_NAMES if n in all_lists}
    return categories, modifiers, polarity


def segment_clauses(note: str) -> list[str]:
    pieces = CLAUSE_SPLIT_RE.split(note)
    return [p.strip() for p in pieces if p and p.strip()]


def find_phrase_positions(clause: str, phrase: str) -> list[int]:
    """Return character positions where phrase occurs in clause (case-insensitive)."""
    c = clause.lower()
    out = []
    start = 0
    while True:
        idx = c.find(phrase, start)
        if idx == -1:
            return out
        out.append(idx)
        start = idx + 1


def words_before(clause: str, char_pos: int, n_words: int) -> str:
    """Return up to n_words preceding the character position (in original casing, lowercased on return)."""
    prefix = clause[:char_pos].lower().strip()
    tokens = re.findall(r"[a-zàâäéèêëìîïòôöùûüç]+", prefix)
    return " ".join(tokens[-n_words:]) if tokens else ""


def analyse_clause(
    clause: str,
    categories: dict[str, list[str]],
    modifiers: dict[str, list[str]],
    polarity: dict[str, list[str]],
) -> dict:
    """Return {categories: [list], symptom_states: {cat: state}, polarity: str}."""
    c_lower = clause.lower()
    matched_cats: list[str] = []
    symptom_states: dict[str, str] = {}
    polarity_boost_from_negation = False

    # Layer 1 + Layer 2: per-category match, with per-symptom modifier detection
    for cat, phrases in categories.items():
        if cat == "context_neutraal":
            continue
        match_pos: int | None = None
        matched_phrase: str | None = None
        for p in phrases:
            positions = find_phrase_positions(c_lower, p)
            if positions:
                # take the first occurrence
                if match_pos is None or positions[0] < match_pos:
                    match_pos = positions[0]
                    matched_phrase = p
        if match_pos is None:
            continue
        matched_cats.append(cat)
        if cat in SYMPTOM_CATEGORIES:
            # Layer 2: look at the 3 words before for negation / severity_*
            preceding = words_before(clause, match_pos, NEGATION_WINDOW_WORDS)
            state = "present"  # default
            if any(neg in preceding for neg in modifiers.get("negation", [])):
                state = "absent"
                polarity_boost_from_negation = True
            elif any(sev in preceding for sev in modifiers.get("severity_severe", [])):
                state = "severe"
            elif any(sev in preceding for sev in modifiers.get("severity_mild", [])):
                state = "mild"
            symptom_states[cat] = state

    # Layer 3: clause polarity
    has_positive = any(p in c_lower for p in polarity.get("polarity_positive", []))
    has_negative = any(p in c_lower for p in polarity.get("polarity_negative", []))

    if has_positive and has_negative:
        pol = "mixed"
    elif has_positive:
        pol = "positive"
    elif has_negative:
        pol = "negative"
    elif polarity_boost_from_negation:
        pol = "positive"
    else:
        pol = "neutral"

    if not matched_cats:
        matched_cats = ["context_neutraal"]

    return {
        "categories": sorted(matched_cats),
        "symptom_states": symptom_states,
        "polarity": pol,
    }


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
    print("Loading dictionary v2…")
    categories, modifiers, polarity = load_dictionary(DICT_FILE)
    print(f"  categories: {len(categories)}  -- {sorted(categories.keys())}")
    print(f"  modifiers : {len(modifiers)}   -- {sorted(modifiers.keys())}")
    print(f"  polarity  : {len(polarity)}    -- {sorted(polarity.keys())}")
    for sec_name, sec in [("categories", categories), ("modifiers", modifiers), ("polarity", polarity)]:
        for name, phrases in sec.items():
            print(f"    {name}: {len(phrases)} phrases")

    print("\nLoading notes…")
    entries = json.loads(NOTES_JSON.read_text(encoding="utf-8"))
    day_scores = {date.fromisoformat(e["date"]): e["score"] for e in entries if e.get("score") is not None}
    day_notes = {date.fromisoformat(e["date"]): e["note"].strip() for e in entries if e.get("note") and e["note"].strip()}
    print(f"  {len(day_scores)} day_entries, {len(day_notes)} with notes")

    episodes = find_crash_episodes(day_scores)
    print(f"  {len(episodes)} crash_v1 episodes")

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

    # ─── Per-clause analysis ───
    per_clause_rows = []
    per_day = {}
    for d in sorted(day_notes.keys()):
        note = day_notes[d]
        clauses = segment_clauses(note)
        day_record = {
            "categories": set(),
            "cat_polarities": collections.defaultdict(lambda: collections.Counter()),  # cat -> {polarity: count}
            "symptom_states": {},  # symptom -> worst severity (max ordering)
            "polarities": collections.Counter(),  # clause polarity counts
        }
        for i, clause in enumerate(clauses):
            result = analyse_clause(clause, categories, modifiers, polarity)
            day_record["polarities"][result["polarity"]] += 1
            for cat in result["categories"]:
                day_record["categories"].add(cat)
                if cat != "context_neutraal":
                    day_record["cat_polarities"][cat][result["polarity"]] += 1
            for sym, state in result["symptom_states"].items():
                existing = day_record["symptom_states"].get(sym)
                if existing is None or SEVERITY_ORDER[state] > SEVERITY_ORDER[existing]:
                    day_record["symptom_states"][sym] = state
            per_clause_rows.append({
                "date": d.isoformat(),
                "clause_idx": i,
                "clause": clause,
                "categories": "|".join(result["categories"]),
                "symptom_states": ";".join(f"{k}={v}" for k, v in result["symptom_states"].items()),
                "polarity": result["polarity"],
            })
        per_day[d] = day_record

    # Write per-clause CSV
    with OUT_CLAUSE.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "clause_idx", "clause", "categories", "symptom_states", "polarity"])
        w.writeheader()
        w.writerows(per_clause_rows)
    print(f"\nwrote {OUT_CLAUSE} ({len(per_clause_rows)} clauses)")

    # Per-day CSV
    cats_sorted = sorted(c for c in categories.keys() if c != "context_neutraal") + ["context_neutraal"]
    with OUT_DAY.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        header = ["date", "score", "in_crash", "is_leadup", "era",
                  "n_pos_clauses", "n_neg_clauses", "n_mixed_clauses", "n_neutral_clauses",
                  "day_dominant_polarity",
                  *[f"cat_{c}" for c in cats_sorted],
                  *[f"state_{s}" for s in sorted(SYMPTOM_CATEGORIES)]]
        w.writerow(header)
        for d in sorted(day_notes.keys()):
            rec = per_day[d]
            era = "early" if d <= ERA_SPLIT else "late"
            in_crash = d in crash_days
            is_leadup = d in leadup_days
            pos = rec["polarities"]["positive"]
            neg = rec["polarities"]["negative"]
            mix = rec["polarities"]["mixed"]
            neu = rec["polarities"]["neutral"]
            dom = "positive" if pos > neg and pos > neu else "negative" if neg > pos and neg > neu else "mixed" if mix > 0 else "neutral"
            row = [d.isoformat(), day_scores.get(d, ""), in_crash, is_leadup, era,
                   pos, neg, mix, neu, dom]
            row.extend(1 if c in rec["categories"] else 0 for c in cats_sorted)
            row.extend(rec["symptom_states"].get(s, "") for s in sorted(SYMPTOM_CATEGORIES))
            w.writerow(row)
    print(f"wrote {OUT_DAY}")

    # ─── Cross-tabs ───
    def group_rates(group_days: set[date]) -> dict:
        """For a group, compute per-category presence rates AND polarity-segmented presence rates."""
        days_with_note = [d for d in group_days if d in per_day]
        n = len(days_with_note)
        if n == 0: return {"n": 0}
        r = {"n": n}
        for cat in cats_sorted:
            r[f"{cat}_present"] = sum(1 for d in days_with_note if cat in per_day[d]["categories"]) / n
            r[f"{cat}_pos"] = sum(1 for d in days_with_note if per_day[d]["cat_polarities"][cat]["positive"] > 0) / n
            r[f"{cat}_neg"] = sum(1 for d in days_with_note if per_day[d]["cat_polarities"][cat]["negative"] > 0) / n
        # symptom state breakdown for symptoom_fysiek (the dominant symptom category)
        # NOTE: key is `{sym}_state_{state}` to avoid clashing with the category `{cat}_present`
        # naming above (e.g. `symptoom_fysiek_present` would otherwise be ambiguous).
        for sym in sorted(SYMPTOM_CATEGORIES):
            for state in ["absent", "mild", "present", "severe"]:
                r[f"{sym}_state_{state}"] = sum(1 for d in days_with_note if per_day[d]["symptom_states"].get(sym) == state) / n
        # clause-polarity day-level dominant counts
        r["day_dom_positive"] = sum(1 for d in days_with_note
                                    if per_day[d]["polarities"]["positive"] > per_day[d]["polarities"]["negative"]) / n
        r["day_dom_negative"] = sum(1 for d in days_with_note
                                    if per_day[d]["polarities"]["negative"] > per_day[d]["polarities"]["positive"]) / n
        return r

    g_crash = group_rates(crash_days)
    g_leadup = group_rates(leadup_days)
    g_noncrash = group_rates(non_crash_days)
    g_all = group_rates(set(day_notes.keys()))

    g_crash_early = group_rates({d for d in crash_days if d <= ERA_SPLIT})
    g_crash_late = group_rates({d for d in crash_days if d > ERA_SPLIT})
    g_leadup_early = group_rates({d for d in leadup_days if d <= ERA_SPLIT})
    g_leadup_late = group_rates({d for d in leadup_days if d > ERA_SPLIT})

    # ─── Summary markdown ───
    md = ["# Notes — categorized clauses v2 (3-layer model)", ""]
    md.append("Built from locked [category_dictionary_v2.md](category_dictionary_v2.md) by [categorize_v2.py](categorize_v2.py).")
    md.append("Each clause now has: categories (layer 1), symptom_states (layer 2 via negation+severity modifiers), polarity (layer 3).")
    md.append("")
    md.append("## Group sizes")
    md.append("")
    md.append(f"- crash days: **{g_crash['n']}** (early {g_crash_early['n']}, late {g_crash_late['n']})")
    md.append(f"- lead-up days: **{g_leadup['n']}** (early {g_leadup_early['n']}, late {g_leadup_late['n']})")
    md.append(f"- non-crash days: **{g_noncrash['n']}**")
    md.append(f"- total with notes: **{g_all['n']}**")
    md.append("")

    # ─── Polarity rates across groups (NEW in v2) ───
    md.append("## Polarity at the clause-level: dominant polarity per day")
    md.append("")
    md.append("How often does each group end up with a positive- vs negative-dominant day?")
    md.append("")
    md.append("| group | day positive-dominant | day negative-dominant |")
    md.append("|-------|---------------------:|---------------------:|")
    for label, g in [("crash", g_crash), ("lead-up", g_leadup), ("non-crash", g_noncrash), ("all", g_all)]:
        if g["n"] > 0:
            md.append(f"| {label} (n={g['n']}) | {g['day_dom_positive']:.2f} | {g['day_dom_negative']:.2f} |")
    md.append("")
    md.append("Era breakdown (crash + lead-up only):")
    md.append("")
    md.append("| group | day positive-dom | day negative-dom |")
    md.append("|-------|----------------:|----------------:|")
    for label, g in [("crash early", g_crash_early), ("crash late", g_crash_late),
                     ("lead-up early", g_leadup_early), ("lead-up late", g_leadup_late)]:
        if g["n"] > 0:
            md.append(f"| {label} (n={g['n']}) | {g['day_dom_positive']:.2f} | {g['day_dom_negative']:.2f} |")
    md.append("")

    # ─── Category presence + polarity split (the main analysis) ───
    md.append("## Category rates with polarity split")
    md.append("")
    md.append("For each category: presence (any clause), positive-polarity presence, negative-polarity presence.")
    md.append("`crash_p`/`crash_n` = % of crash days where this category appears in a positive / negative clause.")
    md.append("")
    md.append("| category | crash | crash_p | crash_n | leadup | leadup_p | leadup_n | non-crash |")
    md.append("|----------|-----:|-------:|-------:|------:|--------:|--------:|---------:|")
    for cat in cats_sorted:
        if cat == "context_neutraal": continue
        cp = g_crash.get(f"{cat}_present", 0); cpp = g_crash.get(f"{cat}_pos", 0); cpn = g_crash.get(f"{cat}_neg", 0)
        lp = g_leadup.get(f"{cat}_present", 0); lpp = g_leadup.get(f"{cat}_pos", 0); lpn = g_leadup.get(f"{cat}_neg", 0)
        ncp = g_noncrash.get(f"{cat}_present", 0)
        md.append(f"| {cat} | {cp:.2f} | {cpp:.2f} | {cpn:.2f} | {lp:.2f} | {lpp:.2f} | {lpn:.2f} | {ncp:.2f} |")
    md.append("")

    # ─── Era comparison with polarity (NEW richer view) ───
    md.append("## Era comparison: crash-day polarity-split shifts")
    md.append("")
    md.append("Looking at categories where polarity changes the story between early-era and late-era crashes.")
    md.append("")
    md.append("| category | early_p | late_p | shift_p | early_n | late_n | shift_n |")
    md.append("|----------|--------:|------:|:-------|--------:|------:|:-------|")
    for cat in cats_sorted:
        if cat == "context_neutraal": continue
        ep = g_crash_early.get(f"{cat}_pos", 0); lp = g_crash_late.get(f"{cat}_pos", 0)
        en = g_crash_early.get(f"{cat}_neg", 0); ln = g_crash_late.get(f"{cat}_neg", 0)
        shift_p = lp - ep; shift_n = ln - en
        m_p = " ⬆" if shift_p >= 0.1 else (" ⬇" if shift_p <= -0.1 else "")
        m_n = " ⬆" if shift_n >= 0.1 else (" ⬇" if shift_n <= -0.1 else "")
        md.append(f"| {cat} | {ep:.2f} | {lp:.2f} | {shift_p:+.2f}{m_p} | {en:.2f} | {ln:.2f} | {shift_n:+.2f}{m_n} |")
    md.append("")

    # ─── Symptom state breakdown (NEW — replaces the v1 92% finding with a richer one) ───
    md.append("## symptoom_fysiek state breakdown (the new view of the v1 92% finding)")
    md.append("")
    md.append("v1 said \"92% of crash days mention symptoom_fysiek\" — but conflated 'geen hoofdpijn' with 'hoofdpijn'.")
    md.append("v2 separates by state (absent / mild / present / severe). The day's symptom_fysiek state is the worst observed across its clauses.")
    md.append("")
    md.append("| group | absent | mild | present | severe | total mentioned |")
    md.append("|-------|------:|----:|-------:|------:|--------------:|")
    for label, g in [("crash", g_crash), ("lead-up", g_leadup), ("non-crash", g_noncrash), ("all", g_all)]:
        if g["n"] > 0:
            ab = g.get("symptoom_fysiek_state_absent", 0)
            mi = g.get("symptoom_fysiek_state_mild", 0)
            pr = g.get("symptoom_fysiek_state_present", 0)
            sv = g.get("symptoom_fysiek_state_severe", 0)
            tot = ab + mi + pr + sv
            md.append(f"| {label} (n={g['n']}) | {ab:.2f} | {mi:.2f} | {pr:.2f} | {sv:.2f} | {tot:.2f} |")
    md.append("")

    md.append("## Era comparison: symptoom_fysiek state shifts on crash days")
    md.append("")
    md.append("| state | early | late | shift |")
    md.append("|-------|-----:|----:|:-----|")
    for state in ["absent", "mild", "present", "severe"]:
        e = g_crash_early.get(f"symptoom_fysiek_state_{state}", 0)
        l = g_crash_late.get(f"symptoom_fysiek_state_{state}", 0)
        shift = l - e
        marker = " ⬆" if shift >= 0.1 else (" ⬇" if shift <= -0.1 else "")
        md.append(f"| {state} | {e:.2f} | {l:.2f} | {shift:+.2f}{marker} |")
    md.append("")

    md.append("## How v2 changes the picture (informal)")
    md.append("")
    md.append("Compare to v1's [categories-analysis.md](categories-analysis.md):")
    md.append("")
    md.append("- **Polarity gives lead-up days a signal v1 missed.** Lead-up days were 80% context_neutraal in v1 — those clauses now have polarity even without a category match (\"matig\" → negative; \"redelijk\" → positive).")
    md.append("- **`symptoom_fysiek` on crashes is no longer 92% blindly**. Now broken into absent / mild / present / severe — the 92% becomes a more useful distribution.")
    md.append("- **`belasting_emotioneel` and `belasting_gezin` get polarity-split** so we can see whether they're recovery-supportive (positive) or load-additive (negative) in each group.")
    md.append("- **Era comparison gains polarity dimension** — for each category we can ask not just \"did rate shift\" but \"did *positive* presence shift differently from *negative* presence?\"")
    md.append("")

    OUT_SUMMARY.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {OUT_SUMMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
