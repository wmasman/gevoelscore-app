"""Merge calendar triage CSV into annotations.yaml.

Reads the user-triaged calendar CSV (keep_yn=y rows + per-event
cognitive/physical/emotional load 1-3 + notes), applies the
agreed load to category mapping, deduplicates against existing
hand-curated entries, and writes a clean chronological
annotations.yaml.

Load to category mapping:
- any load = 3                       -> high_intensity
- max load = 2                       -> levensgebeurtenis
- all loads empty or 1               -> levensgebeurtenis (subtle)

Triage CSVs supported (drop in additional files when other years are
triaged):
- data/calendar_2022_triage.csv
"""
from __future__ import annotations

import csv
import re
import unicodedata
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
ANNOTATIONS = DATA / "annotations.yaml"
TRIAGE_CSVS = sorted(DATA.glob("calendar_*_triage.csv"))


# ---- Hand-curated annotations that pre-date / sit outside calendar coverage.
HAND_CURATED_MARKERS = [
    {
        "date": "2022-05-06",
        "label": "Long COVID diagnose",
        "category": "medical",
        "note": "Huisarts stelt long covid vast.",
    },
]

HAND_CURATED_SPANS = [
    {
        "start": "2021-08-16",
        "end": "2022-03-22",
        "label": "Training-periode (hardlopen + fietsen, voorbereiding Ardennen)",
        "category": "levensgebeurtenis",
        "note": "Garmin gekocht voor trainings-tracking. Doel: fietsweekend Ardennen 01-04-2022. Activities-data: gemiddeld 130-280 min/week running + cycling, met initiele piek aug 2021 (W33-W35: 573/162/893 min) en daarna stabiel. Week 12 (21-27 mrt) heeft 0 minuten training, consistent met corona-ziek-week.",
    },
    {
        "start": "2022-03-23",
        "end": "2022-03-30",
        "label": "Corona-infectie",
        "category": "trigger",
        "note": "Een aantal dagen op bed met koorts. Donderdag 31-03 voelt over de infectie heen. Trigger voor long-covid onset. Bevestigd door 0 training-activities in week 12.",
    },
    {
        "start": "2022-04-01",
        "end": "2022-04-03",
        "label": "Fietsweekend Ardennen",
        "category": "high_intensity",
        "note": "Weekendje fietsen met vrienden, net een dikke week na corona. Niet veel op de fiets gezeten. Eerste nacht heel diep geslapen, herken ik nu als diepe long-covid-slaap bij overexertion.",
    },
    {
        "start": "2022-04-28",
        "end": "2022-05-02",
        "label": "Zuna periode (high intensity)",
        "category": "high_intensity",
        "note": "In Zuna; merkt dat er echt iets mis is, slaapt superveel, eerste herkenbare grote crash volgde (zie crash-band uit research-data).",
    },
    {
        "start": "2022-05-15",
        "end": "2022-05-21",
        "label": "Jantine op Bonaire (alleen thuis met zorgtaken)",
        "category": "levensgebeurtenis",
        "note": "Jantine op Bonaire; veel zelf in huis doen. Mogelijk hulp van Jantines ouders (TODO: bevestigen). Pre-2022-06-17 dus niet uit calendar te halen.",
    },
    {
        "start": "2022-06-04",
        "end": "2022-06-06",
        "label": "Pinkster campinglife 2022",
        "category": "high_intensity",
        "note": "Door gebruiker bevestigd; pinksterzondag 2022 was 5 juni. Niet uit calendar (coverage start 17-06).",
    },
    {
        "start": "2022-07-08",
        "end": "2022-07-10",
        "label": "Zuna feest juli 2022",
        "category": "high_intensity",
        "note": "Door gebruiker bevestigd. Geen specifieke calendar-entry teruggevonden.",
    },
]

# Recurring high-intensity events found earlier in calendar (>2022).
# Plus narrative umbrella periods (long levensgebeurtenis spans that
# contextualise dense clusters of individual events within them).
HAND_CURATED_SPANS_POST_2022 = [
    # ------------------------------------------------------------------
    # 2024 umbrella narrative periods
    # ------------------------------------------------------------------
    {
        "start": "2024-04-01",
        "end": "2024-11-08",
        "label": "Mirjam-periode (Angela tensions + relatiecoach met Jantine)",
        "category": "levensgebeurtenis",
        "note": "Umbrella-periode. Aanloop: oplopende spanningen met Angela (schoonmoeder), wat ook de relatie met Jantine raakte. Vanaf 24-06 vier sessies relatiecoach Mirjam (zie individuele entries). Belangrijk maar zwaar. Einde met de moeilijke sessie samen met Angela 08-11-2024.",
    },
    {
        "start": "2024-04-01",
        "end": "2024-07-18",
        "label": "Werk-transitie (afbouw + afscheid)",
        "category": "levensgebeurtenis",
        "note": "Umbrella-periode. Voorjaar 2024 aanloop. Spullen inleveren op kantoor Utrecht 27-06. Afscheid op kantoor (Mark 60) 18-07.",
    },
    # ------------------------------------------------------------------
    # 2025-2026 umbrella narrative periods (work + family processes)
    # ------------------------------------------------------------------
    {
        "start": "2025-09-17",
        "end": "2026-06-05",  # ongoing; capped at timeline end
        "label": "Werk-reintegratietraject met Wilco (ongoing)",
        "category": "levensgebeurtenis",
        "note": "Umbrella-periode. Formeel reintegratie-traject naar werk via Wilco. Gestart met kennismaking 17-09-2025; meerdere afspraken sep 2025 t/m juni 2026. Ongoing - einddatum hier gezet op timeline-einde, pas aan wanneer het traject afsluit.",
    },
    {
        "start": "2025-06-23",
        "end": "2026-05-04",
        "label": "TVO/TVOO project (jun 2025 -> mei 2026 afronding)",
        "category": "levensgebeurtenis",
        "note": "Umbrella-periode. Eigen project rond TVO/TVOO. Eerste TVO-event 23-06-2025 (Koffie met Ria). Officiele lancering 12-02-2026. Afronding ~04-05-2026 ('laatste gesprek met eric voordat tvoo/tvo...').",
    },
    {
        "start": "2026-03-10",
        "end": "2026-08-31",
        "label": "Breinvoeding-interventie (6 sessies, mar -> ~aug 2026)",
        "category": "interventie",
        "note": "Formele Breinvoeding-interventie. Eerste consult 10-03-2026. Reeks van 6 sessies; eind-datum schatting op basis van ~3 weken tussen sessies. Pas aan zodra echt aantal/laatste sessie bekend.",
    },
    {
        "start": "2026-04-20",
        "end": "2026-06-05",  # ongoing
        "label": "Gezinscoaching / Groeihelden + Opvoedcoach (ongoing)",
        "category": "levensgebeurtenis",
        "note": "Umbrella-periode. Gestart met Start Groeihelden Kindercoaching intake 20-04-2026, plus Opvoedcoach-sessies voor Willem & Jantine als ouders vanaf 11-05-2026. Combineert beide coaching-strands. Ongoing - einddatum hier gezet op timeline-einde.",
    },
    # ------------------------------------------------------------------
    # CPAP-interventie (uit day_entries notes geverifieerd, jan-feb 2024)
    # ------------------------------------------------------------------
    {
        "start": "2024-01-10",
        "end": "2024-02-28",
        "label": "CPAP-interventie",
        "category": "interventie",
        "note": "Uit day_entries notes geverifieerd. 10-01-2024 instructie cpap-apparaat; 11-01-2024 eerste nacht; tot 31-01-2024 dagelijks gebruik ('eindelijk te wennen'). Daarna geen verdere vermelding in notes. Einddatum schatting eind feb 2024. NB: was niet jan-mar 2025 zoals eerder geschat.",
    },
    # ------------------------------------------------------------------
    # Naproxen-interventie (uit day_entries notes; start 2025-03-27, ongoing)
    # ------------------------------------------------------------------
    {
        "start": "2025-03-27",
        "end": "2026-06-10",  # ongoing; capped at current timeline end
        "label": "Naproxen-interventie (ongoing, ad-hoc gebruik bij hoofdpijn)",
        "category": "interventie",
        "note": "Eerste vermelding 27-03-2025: 'voor het eerst naproxen geslikt tegen de hoofdpijn. Eerder niet gedaan'. Daarna 19 vermeldingen verspreid t/m mei 2026 (clusters: mar-apr 2025, jul 2025, mei 2026). Ongoing intervention; per-day usage tagged separately via v2 dictionary 'medicatie' category. Niet een continue dagelijkse medicatie maar ad-hoc bij symptomen.",
    },
    # ------------------------------------------------------------------
    # Citalopram-traject (uit day_entries notes geverifieerd)
    # Een umbrella + 6 dose-fase sub-spans, allemaal interventie.
    # ------------------------------------------------------------------
    {
        "start": "2024-04-09",
        "end": "2026-06-05",  # ongoing; capped at timeline end
        "label": "Citalopram-traject (umbrella, 2024-04 -> ongoing)",
        "category": "interventie",
        "note": "Umbrella over het hele Citalopram-traject. Start 09-04-2024 (10mg, na huisarts-bezoek 08-04). Plateau 30mg ~21 maanden. Afbouw vanaf 20-03-2026. Ongoing op 8mg druppelvorm vanaf 27-05-2026. Zie 6 sub-fase spans voor detail.",
    },
    {
        "start": "2024-04-09",
        "end": "2024-04-30",
        "label": "Citalopram fase 1: 10mg buildup",
        "category": "interventie",
        "note": "Uit notes: start 09-04-2024 ('Morgen starten met ssri'). Drie weken op 10mg voordat ophogen op 30-04-2024.",
    },
    {
        "start": "2024-04-30",
        "end": "2024-06-20",
        "label": "Citalopram fase 2: 20mg",
        "category": "interventie",
        "note": "Uit notes 30-04-2024: 'voor het eerst citalopram opgehoogd naar 20mg'. Zeven weken op 20mg.",
    },
    {
        "start": "2024-06-20",
        "end": "2026-03-20",
        "label": "Citalopram fase 3: 30mg plateau (~21 maanden)",
        "category": "interventie",
        "note": "Uit notes 20-06-2024: 'Eerste dag op 30mg citalopram'. Plateau van ~21 maanden tot afbouw start 20-03-2026.",
    },
    {
        "start": "2026-03-20",
        "end": "2026-04-17",
        "label": "Citalopram fase 4: afbouw 30 -> 20mg",
        "category": "interventie",
        "note": "Uit notes 20-03-2026: 'Begonnen met afbouwen van citalopram van 30 naar 20'.",
    },
    {
        "start": "2026-04-17",
        "end": "2026-05-27",
        "label": "Citalopram fase 5: afbouw 20 -> 10mg",
        "category": "interventie",
        "note": "Uit notes 18-04-2026: 'Gisteren bij huisarts geweest, nu terug naar 10 mg citalopram'. Dus dose-change was 17-04-2026.",
    },
    {
        "start": "2026-05-27",
        "end": "2026-06-05",  # ongoing
        "label": "Citalopram fase 6: afbouw 10 -> 8mg druppelvorm (ongoing)",
        "category": "interventie",
        "note": "Uit notes 27-05-2026: 'Citalopram afbouw: vandaag voor het eerst 8mg in druppelvorm'. Ongoing afbouw; einddatum capped op timeline end.",
    },
    # ------------------------------------------------------------------
    # Recurring high-intensity events found earlier in calendar (>2022).
    # ------------------------------------------------------------------
    {
        "start": "2023-05-18",
        "end": "2023-05-22",
        "label": "Zuna (hemelvaart-weekend?)",
        "category": "high_intensity",
        "note": "Calendar event: 'Zuna' 5 dagen.",
    },
    {
        "start": "2023-05-20",
        "end": "2023-05-21",
        "label": "Afscheidsfeest Zuna",
        "category": "high_intensity",
        "note": "Calendar event. Valt binnen Zuna-periode 18-22 mei.",
    },
    {
        "start": "2023-05-26",
        "end": "2023-05-30",
        "label": "Pinkster campinglife",
        "category": "high_intensity",
        "note": "Calendar event: 4 dagen camping rond pinksteren.",
    },
    {
        "start": "2023-06-09",
        "end": "2023-06-12",
        "label": "Zuna klustival",
        "category": "high_intensity",
        "note": "Calendar event: 4 dagen klus-festival.",
    },
    {
        "start": "2025-03-09",
        "end": "2025-03-10",
        "label": "Zuna (lente)",
        "category": "high_intensity",
        "note": "Calendar event: 2 dagen.",
    },
    {
        "start": "2025-06-06",
        "end": "2025-06-10",
        "label": "Pinkster campinglife 2025",
        "category": "high_intensity",
        "note": "Calendar event: 4 dagen camping rond pinksteren.",
    },
    {
        "start": "2026-05-22",
        "end": "2026-05-26",
        "label": "Pinkster campinglife 2026",
        "category": "high_intensity",
        "note": "Calendar event: meest recent.",
    },
]


def clean_title(title: str) -> str:
    """Strip mojibake emoji-replacement bytes; keep readable text."""
    if not title:
        return ""
    # Common mojibake -> readable replacements
    replacements = {
        "ð": "",          # corrupted pin / party emoji
        "â¤ï¸": "",       # corrupted heart
        "ð¥³": "",        # corrupted party
        "Ã«": "e",         # corrupted e-umlaut (Australie)
        "Ã©": "e",
        "Ã¨": "e",
    }
    out = title
    for bad, good in replacements.items():
        out = out.replace(bad, good)
    # Strip orphan non-ASCII high-bit characters that survived mojibake
    out = "".join(ch for ch in out if (ord(ch) < 128 or ch.isalpha()))
    # Collapse repeated whitespace
    out = re.sub(r"\s+", " ", out).strip()
    return out


def parse_load(v: str) -> int | None:
    if v is None:
        return None
    v = v.strip()
    if v in ("", "y", "n"):  # accidental y/n in load columns
        return None
    try:
        n = int(v)
        if 1 <= n <= 3:
            return n
    except ValueError:
        pass
    return None


def map_category(cog: int | None, phy: int | None, emo: int | None) -> str:
    loads = [n for n in (cog, phy, emo) if n is not None]
    if not loads:
        return "levensgebeurtenis"
    mx = max(loads)
    if mx >= 3:
        return "high_intensity"
    return "levensgebeurtenis"


def load_summary(cog: int | None, phy: int | None, emo: int | None) -> str | None:
    parts = []
    if cog is not None:
        parts.append(f"cog={cog}")
    if phy is not None:
        parts.append(f"phy={phy}")
    if emo is not None:
        parts.append(f"emo={emo}")
    return "/".join(parts) if parts else None


def read_triage(csv_path: Path) -> list[dict]:
    """Read one triage CSV; return entries to add."""
    entries: list[dict] = []
    seen_titles: dict[tuple[str, str, str], int] = {}
    for r in csv.DictReader(csv_path.open(encoding="utf-8")):
        if (r.get("keep_yn") or "").strip().lower() != "y":
            continue
        title = clean_title(r.get("title", ""))
        if not title:
            continue
        start = (r.get("date_start") or "").strip()
        end = (r.get("date_end") or "").strip() or start
        cog = parse_load(r.get("cognitive_load", ""))
        phy = parse_load(r.get("physical_load", ""))
        emo = parse_load(r.get("emotional_load", ""))
        notes = (r.get("notes") or "").strip()
        # Skip duplicates within the CSV
        key = (start, end, title)
        if key in seen_titles:
            continue
        seen_titles[key] = 1

        category = map_category(cog, phy, emo)
        # Special-case: pinned "interventie" titles (the markers)
        title_lower = title.lower()
        if "ergotherapie" in title_lower or "fysiotherapie" in title_lower:
            category = "interventie"
        elif title_lower.startswith("huisarts") or "verwijzing" in title_lower:
            category = "medical"
        # Compose note
        # Per methodology §2a: loads are per-day, not per-multi-day-event.
        # Strip the `load:` prefix from multi-day spans so a generic per-event
        # rating does not get implicitly attributed to every day in the span.
        # The CSV row still carries the raw load values for traceability.
        is_multi_day = end and start and end != start
        note_parts = []
        loads_str = load_summary(cog, phy, emo)
        if loads_str and not is_multi_day:
            note_parts.append(f"load: {loads_str}")
        if notes:
            note_parts.append(notes)
        note = "; ".join(note_parts) if note_parts else None
        entries.append({
            "start": start,
            "end": end,
            "label": title,
            "category": category,
            "note": note,
        })
    return entries


def read_triage_events(csv_path: Path) -> list[dict]:
    """Read triage_events.csv produced by process_triage_actions.py.

    Different column names from calendar triage CSVs: date_start/date_end/label
    + category override (not derived from loads) + source for provenance.
    """
    if not csv_path.exists():
        return []
    entries = []
    for r in csv.DictReader(csv_path.open(encoding="utf-8")):
        start = (r.get("date_start") or "").strip()
        end = (r.get("date_end") or "").strip() or start
        label = (r.get("label") or "").strip()
        if not start or not label:
            continue
        category = (r.get("category") or "levensgebeurtenis").strip()
        cog = parse_load(r.get("cognitive_load", ""))
        phy = parse_load(r.get("physical_load", ""))
        emo = parse_load(r.get("emotional_load", ""))
        loads_str = load_summary(cog, phy, emo)
        user_note = (r.get("note") or "").strip()
        source = (r.get("source") or "").strip()
        # Multi-day rule from methodology section 2b: only single-day events get loads in note
        is_multi_day = end and start and end != start
        note_parts = []
        if loads_str and not is_multi_day:
            note_parts.append(f"load: {loads_str}")
        if user_note:
            note_parts.append(user_note)
        if source:
            note_parts.append(f"source: {source}")
        note = "; ".join(note_parts) if note_parts else None
        entries.append({
            "start": start, "end": end,
            "label": label,
            "category": category,
            "note": note,
        })
    return entries


def main():
    # Gather all entries
    spans = list(HAND_CURATED_SPANS)

    # CSV-derived entries
    for csv_path in TRIAGE_CSVS:
        print(f"Reading {csv_path.name}...")
        new = read_triage(csv_path)
        print(f"  {len(new)} entries (keep_yn=y after dedupe)")
        spans.extend(new)

    spans.extend(HAND_CURATED_SPANS_POST_2022)

    # Events extracted from triage notes (via process_triage_actions.py)
    triage_events_csv = DATA / "triage_events.csv"
    triage_event_entries = read_triage_events(triage_events_csv)
    if triage_event_entries:
        print(f"Reading {triage_events_csv.name}...")
        print(f"  {len(triage_event_entries)} entries from triage-notes-derived events")
        spans.extend(triage_event_entries)

    # Deduplicate spans by (start, end, label) — favouring earlier-added
    # (which prefers hand-curated over CSV-derived).
    deduped = []
    seen = set()
    for s in spans:
        key = (s.get("start"), s.get("end"), s.get("label", "").strip())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(s)

    # Sort chronologically
    def sort_key(s):
        d = s.get("start") or s.get("date")
        return d if d else "9999-12-31"
    deduped.sort(key=sort_key)

    markers_sorted = sorted(HAND_CURATED_MARKERS, key=lambda m: m["date"])

    header = (
        "# annotations.yaml - user-curated context for the research timeline.\n"
        "# Hand-curated entries + calendar-triage CSV merged by\n"
        "# scripts/merge_calendar_triage.py\n"
        "# Re-render with: python docs/research/timeline/scripts/build_timeline.py\n\n"
    )
    # Build a single YAML document so quoting / escaping is handled correctly.
    doc = {
        "markers": [
            {k: v for k, v in m.items() if v is not None}
            for m in markers_sorted
        ],
        "spans": [
            {k: v for k, v in s.items() if v is not None}
            for s in deduped
        ],
    }
    body = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                          default_flow_style=False, width=120)
    ANNOTATIONS.write_text(header + body, encoding="utf-8")
    print(f"\nWrote {ANNOTATIONS}")
    print(f"Total spans: {len(deduped)}")
    print(f"Total markers: {len(markers_sorted)}")

    # Summary of CSV-derived categories
    csv_by_cat: dict[str, int] = {}
    for s in deduped:
        csv_by_cat[s["category"]] = csv_by_cat.get(s["category"], 0) + 1
    print("\nSpan categories:")
    for cat, n in sorted(csv_by_cat.items(), key=lambda kv: -kv[1]):
        print(f"  {cat:20} {n}")


if __name__ == "__main__":
    main()
