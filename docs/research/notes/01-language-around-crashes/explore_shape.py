"""Quick exploration of the notes corpus: when were notes taken,
how long are they, what's the crash-day breakdown."""
from __future__ import annotations

import collections
import json
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "day_entries_with_notes.json"

# Same crash_v1 detection as everywhere else
LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)


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
    print(f"total entries: {len(entries)}")

    day_scores = {date.fromisoformat(e["date"]): e["score"] for e in entries if e.get("score") is not None}
    day_notes: dict[date, str] = {}
    for e in entries:
        if e.get("note") and e["note"].strip():
            day_notes[date.fromisoformat(e["date"])] = e["note"].strip()
    print(f"  with score: {len(day_scores)}  with note: {len(day_notes)}")

    # Notes by year
    print("\n--- notes per year ---")
    by_year = collections.Counter()
    for d in day_notes: by_year[d.year] += 1
    for y in sorted(by_year):
        days_in_year = sum(1 for d in day_scores if d.year == y)
        pct = 100 * by_year[y] / days_in_year if days_in_year else 0
        print(f"  {y}: {by_year[y]:>4} notes of {days_in_year:>4} day entries ({pct:.0f}%)")

    # Note length distribution
    lengths = [len(n) for n in day_notes.values()]
    word_counts = [len(n.split()) for n in day_notes.values()]
    print("\n--- note length ---")
    print(f"  chars: median={statistics.median(lengths)}  mean={statistics.mean(lengths):.0f}  p25={sorted(lengths)[len(lengths)//4]}  p75={sorted(lengths)[3*len(lengths)//4]}  max={max(lengths)}")
    print(f"  words: median={statistics.median(word_counts)}  mean={statistics.mean(word_counts):.0f}  p25={sorted(word_counts)[len(word_counts)//4]}  p75={sorted(word_counts)[3*len(word_counts)//4]}  max={max(word_counts)}")

    # crash_v1 episodes
    episodes = find_crash_episodes(day_scores)
    print(f"\ncrash_v1 episodes: {len(episodes)}")

    # Days that fall inside an episode (any day with score <= 3 between episode start and end)
    crash_days: set[date] = set()
    for ep in episodes:
        d = ep["start"]
        while d <= ep["end"]:
            if d in day_scores and day_scores[d] <= LOW_THRESHOLD:
                crash_days.add(d)
            d += timedelta(days=1)
    crash_days_with_notes = sum(1 for d in crash_days if d in day_notes)
    print(f"  total crash days (score <= 3 within episode): {len(crash_days)}")
    print(f"  crash days with notes: {crash_days_with_notes} ({100*crash_days_with_notes/len(crash_days):.0f}%)")

    # Lead-up days: 3 days before each episode (per H02b protocol)
    leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, 4):
            leadup_days.add(ep["start"] - timedelta(days=i))
    leadup_days &= set(day_scores.keys())  # only days with score
    leadup_days_with_notes = sum(1 for d in leadup_days if d in day_notes)
    print(f"\n  lead-up days (3 before each crash): {len(leadup_days)}")
    print(f"  lead-up days with notes: {leadup_days_with_notes} ({100*leadup_days_with_notes/len(leadup_days):.0f}%)")

    # Show 5 example crash-day notes (with their score)
    print("\n--- 5 example crash-day notes (chronological) ---")
    sample = sorted(crash_days & set(day_notes.keys()))[:5]
    for d in sample:
        note = day_notes[d]
        note_short = note if len(note) < 200 else note[:200] + "…"
        print(f"\n  [{d.isoformat()}  score={day_scores[d]}]")
        print(f"  {note_short}")

    # And 5 lead-up day notes
    print("\n--- 5 example crash lead-up day notes ---")
    sample_l = sorted(leadup_days & set(day_notes.keys()))[:5]
    for d in sample_l:
        note = day_notes[d]
        note_short = note if len(note) < 200 else note[:200] + "…"
        print(f"\n  [{d.isoformat()}  score={day_scores[d]}]")
        print(f"  {note_short}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
