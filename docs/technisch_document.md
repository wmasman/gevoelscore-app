# Technisch document — passieve context-data en integraties

Aanvulling op `app_brief_gevoelscore.md`. Deze notitie behandelt alles wat **buiten de actieve invoer** ligt: data die automatisch wordt verzameld om de gevoelscore te verrijken, plus de reminder-flow.

## Scope-noot

**Niets in dit document zit in v1.** v1 is een soepele UI gelijkwaardig aan de huidige Excel-werkwijze (zie hoofdbrief). De integraties hier komen in v1.5 en v2.

**Wel in v1: de architectuur die dit mogelijk maakt zonder later te hoeven herbouwen.** Concreet betekent dat voor v1:

- `DayEntry` heeft al velden voor `garmin`, `health`, `weather`, `calendar_events` (nullable, leeg in v1)
- Een uitbreidbaar `Integration`-concept in de codebase: elke bron is een module met een gestandaardiseerde "fetch + aggregate + store per day" interface
- Lokale storage (SQLite) gekozen op basis van de eindstaat, niet de v1-staat
- iOS-framework gekozen met HealthKit-pad in gedachten (zie hieronder)

Daardoor is v1.5 een feature-toevoeging, geen architectuurwijziging.

## Hoofdprincipe

> Alles wat goede context geeft, zonder dat ik er energie in moet steken om het te verzamelen.

Concreet: passieve data wordt op de achtergrond opgehaald, per dag geaggregeerd opgeslagen, en getoond naast de dagscore. De **basis blijft onveranderd**: app openen, een getal en eventueel tekst/tags, en weer door. Niets in dit document mag de invoer-flow uit de hoofdbrief vertragen.

De passieve data dient twee doelen:
1. **Analyse**: correlaties tussen score en HR/HRV/slaap/activiteit/weer/gebeurtenissen
2. **Dagboek**: een rijkere context per dag om later mee uit te werken met therapeuten of jezelf — niet alles hoeft direct geanalyseerd te worden, het mag ook gewoon vastgelegd zijn

---

## Prioriteit van data-bronnen

### P0 (al in basis-brief, v1)
- **Google Agenda** — read-only sync, events per dag opslaan met titel/tijd

### P1 (target voor v1.5 of v2)
- **Apple Health / HealthKit** — slaap, hartslag, HRV, stappen, workouts, mindful minutes, hoeveelheid daglicht
- **Locatie/weer** — barometrische druk, luchtkwaliteit, temperatuur (eenvoudige weer-API op basis van locatie)
- **iOS Screen Time** — schermtijd als grove proxy voor cognitieve belasting

### P2 (target voor v2+)
- **Garmin Forerunner 245** — specifiek Body Battery, Stress score, slaapstadia, HRV
- **Apple Calendar** — naast Google
- **Workoutdata uit Strava** (alternatieve route voor Garmin)

### Niet doen
- Real-time biofeedback in de app
- Continue data-streams opslaan (alleen dagaggregaten)
- Email/Slack-activiteit als werklast-indicator (privacy en complexiteit veel te hoog voor de waarde)

---

## Garmin Forerunner 245

### Wat de Garmin meet dat relevant is voor Long COVID

| Metriek | Waarde voor herstel-tracking |
|---|---|
| **Resting heart rate** | Bekende vroege indicator van naderend infect of slechte recovery. Verhoogde RHR 1–2 dagen vóór subjectieve klachten is gedocumenteerd in ME/CFS-literatuur |
| **HRV / Body Battery** | Autonome belasting; nauw verbonden met PEM-risico. Body Battery aan het einde van de dag voorspelt vaak de volgende dag |
| **Sleep stages** | Diep/REM verdeling, niet alleen totaal — bij Long COVID is slaaparchitectuur vaak verstoord |
| **Stress score** | Garmins eigen 0–100 berekening op basis van HRV |
| **VO2max trend** | Lange-termijn conditie-indicator |
| **Workouts** | Bij geplande activiteit: duur, intensiteit, max HR — koppelen aan eventuele PEM op dag+1/+2 |

### Toegangspaden, van eenvoudig naar moeilijk

1. **Via Apple Health (aanbevolen voor individueel gebruik)** — Garmin Connect synct standaard met Apple Health. We hoeven dan alleen de HealthKit-integratie te bouwen en krijgen Garmin-data "gratis" mee.
   - Voordeel: één integratiepunt voor zowel Garmin als andere bronnen
   - Nadeel: Garmin-specifieke metrics (Body Battery, Stress score) komen niet altijd in HealthKit terecht. Voor RHR, slaap, HRV en workouts wel.

2. **Via Strava-koppeling** — Garmin-workouts kunnen automatisch naar Strava worden gepushed. Strava heeft een goede publieke API.
   - Voordeel: betrouwbare API, eenvoudige OAuth
   - Nadeel: alleen workouts, geen rust/slaap-data

3. **Garmin Connect API direct** — vereist toegang tot het Garmin Connect Developer Program (Health API kost ~30k/jr voor enterprise, Connect IQ is gratis voor watch-apps maar geen server-side data-toegang)
   - Voordeel: alle data inclusief Body Battery
   - Nadeel: bureaucratie, kosten, B2B-flow

4. **Garmin Connect web scraping** — onderlangs garmin.com inloggen en data ophalen. Bestaande bibliotheken zoals `python-garminconnect`.
   - Voordeel: alle data toegankelijk
   - Nadeel: fragiel, tegen Garmin TOS, login-onderbrekingen

**Voorgestelde aanpak voor v2**: route 1 (via Apple Health) als hoofdpad, met route 4 (`python-garminconnect`) als nightly Cloud Function fallback voor de Garmin-specifieke velden die HealthKit niet doorgeeft. Niets in de iOS-app zelf, want dat zou inloggegevens opslaan in de client.

### Op te slaan per dag (Garmin)

```
GarminDaily {
  date: Date
  rhr: number                 // resting heart rate
  hrv_overnight_avg: number   // overnight HRV in ms
  body_battery_morning: number
  body_battery_evening: number
  stress_avg: number          // 0-100
  sleep_total_min: number
  sleep_deep_min, sleep_rem_min, sleep_light_min, sleep_awake_min
  steps: number
  active_calories: number
  workouts: WorkoutSummary[]
  source: "apple_health" | "garmin_direct"
  fetched_at: timestamp
}
```

Aggregaten, geen raw streams. Tweede orde berekeningen (RHR-afwijking van 30-dagen baseline, HRV-trend) doen we tijdens analyse, niet bij opslag.

---

## Apple Health / HealthKit

### Relevante datatypes

- `HKQuantityTypeIdentifierHeartRate` — continue HR samples
- `HKQuantityTypeIdentifierRestingHeartRate` — daily summary
- `HKQuantityTypeIdentifierHeartRateVariabilitySDNN` — HRV samples
- `HKCategoryTypeIdentifierSleepAnalysis` — slaap inclusief stadia (iOS 16+)
- `HKQuantityTypeIdentifierStepCount`
- `HKQuantityTypeIdentifierActiveEnergyBurned`
- `HKCategoryTypeIdentifierMindfulSession` — als ik mindfulness-apps gebruik
- `HKQuantityTypeIdentifierAppleStandHour`
- `HKQuantityTypeIdentifierRespiratoryRate`
- `HKWorkoutType` — alle workouts (Garmin, andere apps)
- `HKQuantityTypeIdentifierTimeInDaylight` (iOS 17.2+) — daglicht in minuten

### Technische implicatie

HealthKit is **iOS-only**. Dat is een doorslaggevende constraint voor het framework:

- **Pure web-PWA werkt niet** voor HealthKit
- **Native iOS (Swift)** — beste integratie maar dubbel werk als ik ooit Android wil
- **React Native / Expo met `react-native-health` plugin** — goede balans
- **Flutter met `health` package** — werkt, maar minder mature voor HealthKit-edge cases
- **Capacitor (Ionic) met HealthKit plugin** — pragmatisch als de UI in webtech blijft

Voorstel: **Expo (React Native) met de `react-native-health` bridge**. Strookt met mijn bestaande React-stack.

### Permissions en privacy

- HealthKit-toestemming wordt per data-type gevraagd. Vraag alleen om de types die we daadwerkelijk gebruiken (geen brede `all`-toestemming)
- HealthKit-data verlaat de telefoon nooit zonder expliciete toestemming. Cloud sync van afgeleide aggregaten moet apart configureerbaar zijn
- De gebruiker (ik) moet kunnen zien welke types worden gelezen en dat per stuk kunnen uitschakelen

---

## Google Calendar (uitwerking van basis-brief)

### Wat per dag opslaan

```
CalendarEvent {
  id: string             // Google event id (stable)
  date: Date
  title: string
  start_time, end_time
  all_day: boolean
  calendar_source: string  // welke agenda
  attendees_count?: number
  location?: string
  relevance: "high" | "normal" | "hidden"
  category_hint?: string  // afgeleid: "werk", "sociaal", "afspraak", "reis", "verjaardag"
}
```

### Categorisering uit titel

Auto-tag events op basis van titel-keywords, gebruiker kan overrulen:
- `werk|kantoor|meeting|overleg|stand-?up` → `werk`
- `verjaardag|jarig` → `sociaal`
- `breinvoeding|huisarts|fysio|therapeut` → `afspraak_zorg`
- `weekend|vakantie|reis` → `reis`
- `kinderen|school|hockey|vioolles` → `gezin`

Eenvoudige regex-set, geen ML nodig. De gebruiker kan keywords bewerken in de settings.

### Authentication

- OAuth 2.0 met scope `https://www.googleapis.com/auth/calendar.readonly`
- Token refresh via standaard Google flow
- Eén account in v1; multi-account uitbreidbaar maken in data-model

---

## Weer en omgevingsdata

Eenvoudige integratie maar potentieel waardevol — barometrische drukverandering wordt door veel Long COVID-patiënten genoemd als triggerfactor.

```
WeatherDaily {
  date: Date
  temp_min, temp_max, temp_avg
  humidity_avg
  pressure_avg                  // hPa - belangrijk
  pressure_delta_24h            // verschil met gisteren - mogelijk triggerend
  precipitation_mm
  daylight_minutes
  uv_index_max
  air_quality_index?            // PM2.5
  location: { lat, lon, label }
}
```

Bron: Open-Meteo API (gratis, geen key nodig) op basis van locatie (uit iOS Location of vaste home-coordinaat).

---

## Storage model per dag — samengevoegd

De `DayEntry` uit de hoofdbrief wordt uitgebreid met passieve context-velden:

```
DayEntry {
  // existing fields uit basis-brief
  date, score, note, tags, project_entries, ...

  // passieve context (allemaal optional, gevuld door background jobs)
  garmin?: GarminDaily
  health?: HealthDaily         // Apple Health aggregaten
  weather?: WeatherDaily
  calendar_events: CalendarEvent[]
  
  // afgeleide indicatoren voor weergave (cached, herberekend bij wijziging)
  derived?: {
    rhr_vs_baseline_30d?: number   // bv. +5 bpm boven baseline
    hrv_vs_baseline_30d?: number   // bv. -10 ms onder baseline
    sleep_quality_score?: number   // 1-5 op basis van duur + diep%
    activity_load?: "rust" | "licht" | "matig" | "zwaar"
  }
}
```

De gebruiker ziet op het dagscherm (na het invoeren) **een korte samenvattende strook**: bv. "RHR 62 (+4), slaap 7u20 (62% efficiency), 8.300 stappen, 1 workout 45min". Niet om te beoordelen of het een goede dag was — die rol heeft de score — maar als achtergrond. Tap voor details.

---

## End-of-day reminder

Aanpassing op de "geen notificaties" regel uit de hoofdbrief: **één configureerbare reminder is wel gewenst**, maar met strakke voorwaarden.

Specificaties:
- Standaard uit, expliciet aan te zetten
- Eén tijd per dag instelbaar (default 21:00)
- Vuurt **alleen** als de score voor vandaag nog niet is ingevuld
- Stille notificatie zonder badge of geluid
- Eén tap op de notificatie opent direct het invoerscherm van vandaag
- Niet herhalen — als ik hem negeer is het klaar voor die dag
- Geen "streak verloren!" boodschap — geen FOMO of schuld-framing

Implementatie via iOS UNUserNotificationCenter, lokaal gepland, geen push-server nodig.

---

## Privacy en data-ownership

- **Lokaal-eerst**: alle ruwe data op het device, in encrypted SQLite (SQLCipher of CryptoKit-backed Core Data)
- **Cloud sync is opt-in**: alleen aggregaten en eigen invoer, niet de ruwe HealthKit-samples
- **Geen analytics, geen tracking, geen ads** — basisuitgangspunt voor een persoonlijke health-app
- **Export en delete**: ik moet altijd alles kunnen exporteren (CSV/JSON/SQLite-dump) en alles kunnen wissen
- **Onafhankelijk van leverancier**: als de app verdwijnt moet ik mijn data houden. Lokale SQLite-bestand is daarvoor de garantie.

---

## Open source en licensing

De intentie is om dit project **open source** te maken. Anderen met chronische condities zouden hier waarde uit kunnen halen, en het houdt het project transparant en duurzaam.

Praktische licentie-keuze:

- **Code**: een standaard software-licentie. Creative Commons is **niet bedoeld voor code** (de Creative Commons-organisatie raadt het zelf af). Opties:
  - **MIT** — maximaal permissief, breedste adoptie, ook commercieel hergebruik toegestaan
  - **Apache 2.0** — vergelijkbaar met MIT maar met expliciete patentclausule, geschikt voor grotere projecten
  - **GPL-3.0** — verplicht dat afgeleiden ook open source blijven (copyleft); past goed bij health-tools die niet in gesloten commerciële producten zouden moeten verdwijnen
  - **AGPL-3.0** — als GPL maar dwingt openheid ook af bij SaaS-gebruik over een netwerk
  - **Voorstel**: **MIT** voor maximale adoptie, of **AGPL-3.0** als het belangrijk is dat eventuele cloud-hosted varianten ook open blijven
- **Documentatie en niet-code content** (deze briefs, screenshots, designs): **Creative Commons BY-SA 4.0** of **CC BY 4.0** — daar is CC wél voor bedoeld
- **Mijn persoonlijke data** (de 1.363 dagen in dit voorbeeld): blijft van mij. Niet onder de open source-licentie. Voorbeeld-data of geanonimiseerde sample-data kan apart onder bv. **CC0** of **CC BY** worden gepubliceerd

Praktische implicaties voor de developer:

- Vanaf dag 1 publieke repo op GitHub (of GitLab)
- `LICENSE` en `LICENSE-DOCS` als aparte bestanden, met SPDX-headers in source files
- `CONTRIBUTING.md` en een minimale `CODE_OF_CONDUCT.md`
- Geen secrets in de repo: API keys, Google OAuth credentials etc. via environment variables of een config-systeem
- Gebruikersdata wordt nooit gepushed (lokale SQLite, eventueel cloud sync naar gebruiker's eigen account)
- Dependencies-check op licentiecompatibiliteit (geen GPL deps in een MIT-project bv.)

---

## Open vragen voor de developer

1. Welk framework: **Expo / React Native** met HealthKit-bridge of toch native Swift? Wat is jouw inschatting van de complexiteit van HealthKit via React Native voor onze use case?
2. Hoe lossen we de Garmin Body Battery / Stress score gat op? Acceptabel om alleen via Apple Health-pad te gaan en die metrics te missen?
3. Voor cloud sync: Supabase, Firebase, of zelfgehoste Postgres? Wat past het beste bij encrypted aggregaten van één gebruiker?
4. Hoe ver gaan we in v1 met passieve data? Voorstel: alleen Google Calendar (P0). Apple Health + weer in v1.5. Garmin native in v2.
5. Hoe ontwerpen we het uitbreidbare `context`-model in DayEntry zodat we later eenvoudig nieuwe bronnen kunnen toevoegen (CGM? Aura ring? Oura?) zonder schema-breaking changes?
6. Welke iOS-versie als minimum? `TimeInDaylight` vereist iOS 17.2, slaapstadia iOS 16. Acceptabel om iOS 17+ te eisen?
