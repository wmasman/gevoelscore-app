# Notitie voor app developer — Gevoelscore tracking-app

## Context

Sinds 3 september 2022 houd ik dagelijks een subjectieve gevoelscore bij in een Google Sheet (Long COVID herstel-traject). Dit zijn nu 1.363 opeenvolgende dagen, **100% coverage, geen ontbrekende dagen**. Bij ongeveer de helft van de dagen schrijf ik er een korte notitie bij.

Deze data is voor mij waardevol gebleken (zie aparte analyse `gevoelscore_analyse.html` en de verrijkte dataset `gevoelscore_verrijkt.xlsx`). Het sheet zelf begint krap te worden: filteren, taggen, lopende interventies bijhouden en patronen vinden gaat moeizaam, en mobile invoer is suboptimaal. Ik wil het ombouwen naar een app die specifiek voor mijn manier van bijhouden is gemaakt.

### Bestanden bij deze brief

Alle documenten staan in `programmeerprobeer/gevoelscore-app/`:

- `app_brief_gevoelscore.md` — deze brief
- `technisch_document.md` — uitwerking van passieve context-data (Garmin, Apple Health, weer), reminder-flow en privacy
- `gevoelscore_analyse.html` — interactief dashboard met crash-detectie, energie-envelope, interventie-markers en seizoenseffecten over 3,7 jaar data
- `gevoelscore_verrijkt.xlsx` — alle 1.363 dagen met aparte kolommen voor fysiek / mentaal / positief / activiteit / interventie (drie tabbladen: data, tag-samenvatting, spierpijn-analyse)
- `gevoelscore_verrijkt.csv` — dezelfde data als importbron voor de app

## Cardinaal principe

**De dagelijkse invoer mag niet complexer worden dan wat ik nu doe.** Mijn 100% coverage komt door drempelloze invoer: open sheet, typ getal, optioneel een zinnetje, klaar — onder de 10 seconden op een goede dag. Als de app een formulier wordt met verplichte velden, dropdowns en sliders, ga ik dagen overslaan en hebben we niets gewonnen.

Concreet: **de minimale flow moet "1 tap voor score, klaar" zijn**. Alles daarna is optioneel en mag het hoofdscherm niet bezetten als ik het niet wil.

---

## Scope

**v1 is een soepele UI die doet wat ik nu in Excel doe, beter.** Niets meer. De projecten, agenda-koppeling, Apple Health en Garmin uit de rest van dit document zijn vanaf v1.5 en verder. Liever een v1 die ik daadwerkelijk dagelijks gebruik dan een v1 vol features die ik nog niet aanraak.

**Wat v1 wel doet:**

- Dagelijkse invoer: overall score (1–6) + open tekstveld + chip-tags
- Tags-systeem dat met me meegroeit (persoonlijk, op basis van mijn gebruik)
- Tijdlijn-view (laatste 30/90 dagen, simpele lijngrafiek)
- Streak counter
- Import van de bestaande Google Sheet (1.363 dagen)
- Export naar CSV

**Wat v1 nog niet doet (maar wel volgt):**

- Projecten/interventies met eigen notitievelden (v1.5)
- Google Agenda integratie (v1.5)
- Apple Health / HealthKit (v2)
- Garmin (v2)
- Weer / omgevingsdata (v2)
- Sub-scores, end-of-day reminder, bonus-velden (later)

**Wat v1 in de architectuur al wél heeft:**

Het data model en de codestructuur moeten vanaf dag 1 zo zijn opgezet dat de uitbreidingen toegevoegd kunnen worden zonder schema-migraties of grote refactors. Concreet:

- `DayEntry` heeft al velden voor `project_entries`, `calendar_events`, `health` en `garmin` — leeg in v1, gevuld vanaf v1.5/v2
- `Project`, `ProjectEntry`, `ProjectFieldConfig` schemas bestaan en kunnen leeg blijven
- Tag-categorieën inclusief `project:<id>` en `custom` zijn al ondersteund
- Integraties als modules ontworpen, geen ingebakken aannames over één bron
- Lokale opslag (SQLite) + sync-strategie kiezen die later cloud-aggregaten van passieve data aankan zonder restructuring

Het volledige data model in deze brief is dus v1-schema, ook al gebruikt v1 maar een deel van de velden.

---

## Huidige werkwijze (referentie)

Sheet `Samenvatting activiteitenlijsten`, tab `overall`:
- Kolom A: datum (één rij per dag, vooraf ingevuld)
- Kolom B: score 1–10 (in praktijk 1–6, zie analyse)
- Kolom C: vrije tekst (~50% van de dagen ingevuld, 1–3 zinnen)

Schaal-definitie staat in tab `dashboard`. Niveau 7–10 zijn in 3,7 jaar nooit gebruikt — de schaal werkt feitelijk als 1–6.

Notities bevatten een mix van fysieke klachten, mentale klachten, positieve indicaties, activiteiten, interventies. Deze categorieën zijn nu retro-actief uit de vrije tekst gehaald met regex-parsing en zitten in `gevoelscore_verrijkt.xlsx`.

---

## De invoer-flow (kern van de app)

Het dagelijkse invoerscherm is opgebouwd uit **gelaagde blokken** die meegroeien met wat ik die dag nodig heb. Elk volgend blok is optioneel. Per blok staat erbij in welke versie het beschikbaar komt.

### Blok 1: overall score — v1 (verplicht, altijd zichtbaar)

- 6 grote knoppen 1 t/m 6, eventueel met halve waarden (4.5 toelaten)
- Eén tap = invoer opgeslagen
- Dit alleen is genoeg om de dag te laten tellen voor streak en analyse

### Blok 2: vrije tekst + tags — v1 (optioneel, altijd zichtbaar maar leeg-startend)

- Eén open tekstveld zoals nu — geen lengte-limiet
- Daaronder een rij **chip-tags** die ik tikkend kan toevoegen/verwijderen
- Tags-set is **persoonlijk en dynamisch**: gebaseerd op wat ik historisch invul. Vaak gebruikt = bovenaan en zichtbaar. Nooit gebruikt = uit het zicht.
- Ik moet zelf tags kunnen toevoegen ("lekker snel", "goede dag", "hoofdpijn", "spierpijn") en bestaande hernoemen/samenvoegen
- Tag-clusters voor de seed-set (gebaseerd op mijn historische data):
  - **Fysiek:** hoofdpijn, brainfog, moe, zware benen, spierpijn, slecht geslapen, verkouden, koorts, misselijk, keelpijn, nekpijn
  - **Mentaal:** emotioneel, overprikkeld, stress, somber
  - **Positief:** goed geslapen, goede energie, geen hoofdpijn, helder, lekker snel, goede dag
  - **Activiteit-zwaarte:** rustdag, licht, matig, zwaar
- Tags zijn aanvullend, niet vervangend. Vrije tekst en tags kunnen naast elkaar bestaan, of een van beide alleen.

### Blok 3: actieve interventies / projecten — v1.5 (alleen zichtbaar als er een loopt)

Dit is het belangrijkste nieuwe concept. **Een interventie of project is iets met een start- en (open) einddatum dat ik tijdelijk wil volgen**. Voorbeelden uit mijn situatie nu:

- *Citalopram afbouw* (gestart 20 mrt 2026, loopt nu)
- *Breinvoeding traject* (1 mei 2026, 6 sessies)
- *Naproxen-gebruik* (sinds 27 mrt 2025, op-verzoek-basis)
- *Heartmath HRV-oefening* (sinds mei 2026, dagelijks)

Als er één of meer actieve projecten zijn, verschijnt voor elk project op het dagscherm een **eigen klein blok** met:
- Naam van het project (header)
- Kort open tekstveld voor die dag (project-specifieke notitie)
- Project-specifieke tags (bv. voor Breinvoeding: "ademhalingsoefening gedaan", "coherence laag", "HRV goed")
- Optioneel: 1–2 numerieke velden afhankelijk van project-settings (bv. "dosis vandaag", "minuten geoefend", "HRV-score")

Belangrijk: als ik niets bij een project invul gaat de dag gewoon door. Standaard leeg, niet-blokkerend.

**Elders in de app** (apart scherm "Projecten"):
- Lijst van alle projecten (actief + gearchiveerd)
- Per project: naam, type, startdatum, optionele einddatum, beschrijving, instellingen welke velden ik per dag wil bijhouden (alleen tekst? + tags? + 1 numeriek veld?)
- Een project starten / stoppen / pauzeren

### Blok 4: bijzonderheden uit de agenda — v1.5 (automatisch, alleen tonen als relevant)

Als er die dag iets bijzonders is, wil ik dat als context kunnen zien zonder het apart te hoeven invullen. De app moet **Google Agenda kunnen importeren**:

- Read-only sync met één of meer Google-agendas
- Per dag: een lijstje events op die dag (titel + tijd), getoond bovenaan het dagscherm als referentie
- Ik kan events markeren als "relevant voor mijn herstel" — dan blijven ze in de analyse meegenomen. Onbelangrijke events (terugkerend werkblok bv.) kan ik standaard verbergen of filteren op kalender
- Optioneel: handmatig "iets speciaals" veld voor dingen die niet in de agenda staan ("avondvierdaagse afgerond", "Jantine weg")

Voorbeelden uit mijn data die hieruit relevant zouden zijn: kantoorbezoek, redactievergadering, weekendje weg, verjaardag, ziekenhuisbezoek, mediation-gesprek, Breinvoeding-afspraak.

### Blok 5: bonus-velden — v2+ (alleen als ik tap om uit te klappen)

Niet standaard zichtbaar. "Meer..." om uit te klappen:
- Sub-scores: cognitief / fysiek / sociaal-mentaal (1–6, optioneel)
- Slaapduur
- Stemming als aparte 1–6 score
- Foto

### Backfill

- Kalenderview met lege/oranje gemarkeerde dagen, één tap om in te vullen
- Bij eerste gebruik moet de app de 1.363 bestaande dagen kunnen importeren uit het Google Sheet (CSV/xlsx). Mapping: kolom B → score, kolom C → vrije notitie. Tag-extractie achteraf is al gedaan in `gevoelscore_verrijkt.xlsx`.

---

## Data model (suggestie)

```
DayEntry {
  date: Date (primary key, één entry per dag)
  score: number (1.0 - 6.0)
  note: string (vrije tekst, optional)
  tags: TagRef[]
  sub_scores?: { cognitive?, physical?, mental? }
  sleep_hours?: number
  project_entries: ProjectEntry[]
  special_event?: string (handmatig invulbaar)
  created_at, updated_at
}

ProjectEntry {
  project_id: UUID
  note?: string
  tags: TagRef[]
  numeric_values: { [field_key]: number }   // e.g. { dose_mg: 20, hrv_score: 78 }
}

Project {
  id: UUID
  name: string                              // e.g. "Citalopram afbouw"
  type: "medicatie" | "therapie" | "oefening" | "anders"
  start_date: Date
  end_date?: Date
  status: "active" | "paused" | "completed" | "archived"
  description?: string
  fields: ProjectFieldConfig[]              // welke velden ik dagelijks wil invullen
}

ProjectFieldConfig {
  key: string
  label: string
  type: "text" | "tag_set" | "number"
  unit?: string                             // e.g. "mg", "min"
  default_visible: boolean
}

Tag {
  id: UUID
  label: string
  category: "fysiek" | "mentaal" | "positief" | "activiteit" | "interventie" | "project:<id>" | "custom"
  usage_count: int
  archived: boolean
}

CalendarEvent {
  id: string                                // Google event id
  date: Date
  title: string
  start_time, end_time
  calendar_source: string
  relevance: "high" | "normal" | "hidden"
}
```

Belangrijke eigenschappen:
- Datum is primary key voor `DayEntry` — overschrijven mag, geen dubbele entries
- `ProjectEntry` is een sub-record per project per dag — dit maakt analyse per project triviaal (bv. "hoe waren mijn scores op dagen dat ik ademhalingsoefening deed?")
- Tags zijn references, niet ingebakken strings — voor latere hernoeming/samenvoeging
- Calendar events worden gesynchroniseerd, niet gekopieerd — als ik in Google Agenda iets aanpas klopt het in de app ook

---

## Versie-roadmap

### v1 (eerste oplevering)
- Blok 1 + 2: score, vrije tekst, persoonlijke tags
- Tijdlijn-view (laatste 30/90 dagen)
- Streak counter
- Import bestaande Google Sheet (1.363 dagen)
- Export naar CSV
- Volledig data model en code-architectuur klaar voor v1.5/v2 uitbreidingen

### v1.5
- Blok 3: projecten / interventies met eigen notitievelden en tags
- Blok 4: Google Agenda read-only sync, "iets speciaals" veld
- Project-beheer scherm

### v2
- Apple Health / HealthKit (slaap, HR, HRV, workouts)
- Garmin (via HealthKit; Garmin-specifieke metrics later via aparte job)
- Weer- en omgevingsdata
- End-of-day reminder (configureerbaar)
- Blok 5: sub-scores en bonus-velden

### Expliciet niet (in geen enkele versie)
- Sociale features, delen, multi-user
- AI/chat-functies in de app
- Symptoom-encyclopedie of medische uitleg
- Schrijven naar Google Agenda (alleen lezen)
- Analytics, tracking, ads

---

## Platform-overweging

- **Mobile-first**, want invoer gebeurt 's avonds of vroeg in de ochtend, vaak in bed
- iOS is mijn dagelijks device, maar een PWA / Flutter / React Native met cross-platform support voorkomt later vendor lock-in
- Lokale opslag (SQLite of vergelijkbaar) met optionele cloud sync (Supabase, Firebase, of self-hosted Postgres)
- Werkt offline — invoer zonder netwerk moet kunnen, kalender-sync gebeurt zodra er verbinding is
- Google Agenda integratie via Google Calendar API (read-only OAuth scope `calendar.readonly`)

---

## Persoonlijke context die het ontwerp beïnvloedt

- Ik ben Long COVID-patiënt; brainfog hoort bij het beeld. De UI moet werken op een 4-uit-6 dag: weinig cognitieve belasting, geen "drie schermen vooruit klikken om iets simpels te doen"
- Op mijn slechtste dagen kan een hoog-prikkel interface me weerhouden. Vermijd flitsende kleuren, animaties die niet nodig zijn, geluid
- Ik programmeer zelf in Next.js/React met TypeScript en heb een eigen platform gebouwd (TvO), dus technische details mogen direct besproken worden

## Gespreksvragen

1. Welk framework heeft de voorkeur voor mobile-first met snelle iteratie en goede offline support?
2. Hoe lossen we sync + offline op zonder ingewikkeld account-systeem?
3. Ervaring met Google Calendar API integratie? Hoe gaan we om met het ophalen + filteren van events?
4. Hoe ontwerpen we het project-concept zodat het uitbreidbaar is (later een HRV-device koppelen, of een eigen vragenlijst per project) zonder elke keer een nieuwe schermflow?
5. Wat is een realistische scope voor v1?
6. Hoe houden we het "5-seconden invoer" principe overeind nu het invoerscherm meerdere optionele blokken heeft? Wat is de aanpak voor progressive disclosure?
