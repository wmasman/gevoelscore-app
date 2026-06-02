// Centralised Dutch UI strings. Components import from here rather than
// inline strings so future copy edits + the eventual i18n seam are tractable.
//
// Keep keys grouped by feature surface (app, daily, timeline, errors).

export const copy = {
  app: {
    title: 'Gevoelscore',
    description: 'Persoonlijke dagscore voor Long COVID. Registreer in één tik.',
  },
  daily: {
    score: {
      label: 'Score',
      placeholder: 'Tik om te kiezen',
    },
    note: {
      label: 'Notitie',
      placeholder: 'Schrijf hier je notitie…',
    },
    tags: {
      label: 'Tags',
      // `empty` removed 2026-06-01: inline tag creation replaces the
      // dead-end "Geen tags in deze categorie" with a "+ nieuw" chip.
      none: 'Geen tags',
      extraToggle: 'Extra opties (Interventie, Project, etc)',
      addAriaLabel: 'Voeg tag toe aan',
      newInputAriaLabel: 'Nieuwe tag',
      newInputPlaceholder: 'Nieuwe tag',
      addButton: 'Toevoegen',
      addChipLabel: '+ nieuw',
    },
    // Popout flow controls. The forward button label changes per
    // step; the back button reads from daily.{score,note}.label.
    flow: {
      nextNote: 'Volgende: notitie',
      nextTags: 'Volgende: tags',
      done: 'Klaar',
      close: 'Sluiten',
    },
  },
  home: {
    todayHeading: 'Vandaag',
    scoreRegionLabel: 'Gevoelscore',
    noteRegionLabel: 'Notitie',
    tagsRegionLabel: 'Tags',
    scoreEmpty: 'Nog niet gekozen',
    noteEmpty: 'Geen notitie',
    tagsEmpty: 'Geen tags',
    editAriaLabel: 'Bewerken',
    previousHeading: 'Vorige dagen',
    showMore: 'Toon meer',
    showLess: 'Toon minder',
    sheetAriaLabel: 'Dag-invoer',
    tabsAriaLabel: 'Schermen',
    // Caller is responsible for formatting the date in Dutch (the
    // function-vs-string call shape lets copy.ts stay free of cross-
    // module date-format imports).
    pastDayAriaLabel: (formattedDate: string, score: number): string =>
      `Vorige dag ${formattedDate}, score ${score}`,
  },
  context: {
    // Tab label + view aria-label for the v1.5 Context surface — the
    // LEFT tab in the bottom nav (Context / Vandaag / Tijdlijn).
    // Vandaag sits in the centre so daily-flow thumb-reach is balanced
    // left and right. Context holds Periodes today; v1.6 adds Calendar
    // bindings as a sibling section; v2 adds project context + patterns.
    // The folder slug verloop-and-episodes/ stays as an internal
    // identifier only.
    title: 'Context',
    ariaLabel: 'Context',
    periodes: {
      // Section within Context for multi-day Episodes (interventies +
      // levensgebeurtenissen).
      heading: 'Periodes',
      empty: 'Nog geen periodes.',
      section: {
        interventiesActive: 'Interventies (actief)',
        interventiesDone: 'Interventies (afgerond)',
        levensgebeurtenissenActive: 'Levensgebeurtenissen (actief)',
        levensgebeurtenissenDone: 'Levensgebeurtenissen (afgerond)',
      },
      // Caller passes already-formatted Dutch date strings. Separator
      // is an arrow (`→`), not an em-dash (forbidden in UI copy per
      // feedback-no-emdash-in-ui).
      dateRange: (startNl: string, endNl: string | null): string =>
        endNl === null ? `${startNl} → lopend` : `${startNl} → ${endNl}`,
    },
    // Step-4 launcher buttons. Label is "periode" not "levensgebeurtenis"
    // because the latter is too clinical for a button. The underlying
    // category stays `levensgebeurtenis` in storage.
    newInterventieButton: '+ Nieuwe interventie',
    newPeriodeButton: '+ Nieuwe periode',
    // Step-4 form copy. The same sheet handles create + edit; the title
    // varies by mode + category (four combinations).
    form: {
      titleNewInterventie: 'Nieuwe interventie',
      titleNewPeriode: 'Nieuwe periode',
      titleEditInterventie: 'Bewerk interventie',
      titleEditPeriode: 'Bewerk periode',
      sheetAriaLabel: 'Periode bewerken',
      labelField: 'Naam',
      labelCountSuffix: (n: number): string => `${n}/40`,
      startDateField: 'Begindatum',
      ongoingToggle: 'Lopend (geen einddatum)',
      endDateField: 'Einddatum',
      descriptionField: 'Beschrijving',
      descriptionPlaceholder: 'Optioneel',
      descriptionCountSuffix: (n: number): string => `${n}/10.000`,
      save: 'Bewaar',
      saving: 'Even geduld…',
      close: 'Sluit',
      requiredMarker: 'verplicht',
      // Inline error messages. role="alert" containers announce these
      // to screen readers when they appear.
      error: {
        labelEmpty: 'Geef een naam.',
        labelTooLong: 'Maximaal 40 tekens.',
        startDateInvalid: 'Kies een begindatum.',
        endDateInvalid: 'Kies een einddatum of zet "lopend" aan.',
        endBeforeStart: 'Einddatum moet ná de begindatum liggen.',
        descriptionTooLong: 'Maximaal 10.000 tekens.',
        serverError: 'Opslaan lukte niet, probeer opnieuw.',
      },
      // aria-label for each tappable list item in the Periodes section
      // (step-4 makes them buttons). Reads as a full episode summary so
      // screen readers can scan the list aloud.
      listItemAriaLabel: (
        label: string,
        start: string,
        end: string | null,
      ): string =>
        end === null
          ? `${label}, ${start} tot lopend, tik om te bewerken`
          : `${label}, ${start} tot ${end}, tik om te bewerken`,
    },
    archive: {
      button: 'Archiveer',
      // SaveAnnouncer copy fired after a successful archive PATCH.
      announced: 'Gearchiveerd.',
    },
    // Step-5: tag-to-episode linking surface. Renders inside the edit-mode
    // EpisodeFormSheet between description + action row. Picker is a nested
    // BottomSheet over the form; tagging from the daily flow is unchanged.
    tagLinking: {
      heading: 'Tags die hierbij horen',
      empty: 'Nog geen gekoppelde tags.',
      addButton: '+ Tag',
      // aria-label for each linked-tag chip's remove button. The chip
      // itself is non-tappable in v1.5 (no detail view); the ✕ is the
      // only affordance.
      unlinkAriaLabel: (label: string): string => `Verwijder koppeling: ${label}`,
    },
    tagPicker: {
      sheetAriaLabel: 'Tag kiezen of nieuw aanmaken',
      title: 'Kies of maak een tag',
      createButton: '+ Maak een nieuwe tag aan',
      // Suffix on rows whose tag is linked elsewhere — communicates the
      // silent re-parent ("you'll move this tag here on tap").
      bijSuffix: (otherEpisodeLabel: string): string => `(bij: ${otherEpisodeLabel})`,
      emptyCorpus: 'Nog geen andere tags. Maak er een aan.',
      // Mini-form for inline tag creation. Submits POST /api/tags with
      // parent_episode_id pre-set — one round-trip. Field label is
      // "Tag naam" (not "Naam") so it disambiguates from the episode
      // form's "Naam" field a screen reader would otherwise read twice.
      newTagLabelField: 'Tag naam',
      newTagLabelPlaceholder: 'Naam van de tag',
      newTagCategoryField: 'Categorie',
      newTagCategoryPlaceholder: 'Kies een categorie',
      // Submit is "Toevoegen" (not "Bewaar") so it differs from the
      // parent EpisodeFormSheet's save button — otherwise the same label
      // names two semantically different actions on screen at once.
      newTagSubmit: 'Toevoegen',
      cancel: 'Annuleer',
      close: 'Sluit',
      error: {
        labelEmpty: 'Geef een naam.',
        labelTooLong: 'Maximaal 40 tekens.',
        categoryMissing: 'Kies een categorie.',
        serverError: 'Opslaan lukte niet, probeer opnieuw.',
      },
    },
  },
  timeline: {
    title: 'Tijdlijn',
    todayTab: 'Vandaag',
    range30: '30 dagen',
    range90: '90 dagen',
    rangeAriaLabel: 'Bereik',
    viewChart: 'Lijn',
    viewHeatmap: 'Heatmap',
    viewAriaLabel: 'Weergave',
    maSubtitle: '7-daags voortschrijdend gemiddelde',
    edited: 'bewerkt',
    close: 'Sluit',
    streak: (n: number): string =>
      n === 1 ? '1 dag achter elkaar' : `${n} dagen achter elkaar`,
  },
  settings: {
    title: 'Instellingen',
    back: 'Terug',
    accountHeading: 'Account',
    logout: 'Uitloggen',
    logoutConfirmPrompt: 'Bevestigen.',
    logoutConfirmYes: 'Ja, uitloggen',
    logoutConfirmCancel: 'Annuleren',
    logoutError: 'Uitloggen lukte niet. Probeer opnieuw.',
    dataHeading: 'Data',
    dataSoon: 'Binnenkort',
    dataExport: 'Exporteren',
    dataDelete: 'Account verwijderen',
    iconLabel: 'Instellingen openen',
  },
  errors: {
    notSaved: 'Niet opgeslagen. Probeer nogmaals.',
    generic: 'Er ging iets mis. Probeer opnieuw.',
    notFound: 'Pagina niet gevonden',
    retry: 'Probeer opnieuw',
    backHome: 'Naar startpagina',
  },
  auth: {
    login: {
      title: 'Aanmelden',
      submit: 'Aanmelden',
      submitting: 'Even geduld…',
      emailLabel: 'E-mailadres',
      passwordLabel: 'Wachtwoord',
      errors: {
        rateLimited: 'Te veel pogingen. Probeer het straks opnieuw.',
        invalidCredentials: 'Onjuiste e-mail of wachtwoord.',
        unknown: 'Er ging iets mis. Probeer het opnieuw.',
        network: 'Verbindingsprobleem. Probeer het opnieuw.',
      },
    },
  },
  // Screen-reader-only announcements for the SaveAnnouncer's live region.
  // Visible feedback lives in the today-card pulse and the SaveStatus
  // error banner; these strings carry the same intent over assistive tech.
  announce: {
    saved: 'Opgeslagen.',
    notSaved: 'Niet opgeslagen. Probeer opnieuw.',
  },
  over: {
    title: 'Gevoelscore',
    subtitle:
      'Voor wie leeft met Long COVID, ME/CVS, POTS of fibromyalgie. Eén tik per dag. Geen oordeel, wel inzicht.',
    stat: {
      number: '1.363',
      label: 'dagen consistent, zonder gemiste dag',
    },
    story: {
      heading: 'Waarom ik dit bouw',
      body1:
        'Sinds september 2022 noteer ik elke dag een gevoelscore tussen 1 en 10. 1.363 dagen later, zonder gemiste dag, is dat de waardevolste dataset over mijn herstel.',
      body2:
        'Bijhouden gebeurt nu nog in een Google Sheet. Dat werkt, maar is niet gemaakt voor brainfog. Daarom bouw ik een app die specifiek doet wat ik dagelijks nodig heb: één tik om de dag vast te leggen. Klaar in een paar seconden.',
    },
    principles: {
      heading: 'De principes zijn hard',
      items: [
        'Eén tik en de dag is geregistreerd. Alles daarna is optioneel.',
        'Onder de 10 seconden, ook op een moeilijke dag.',
        'Geen analytics, geen tracking, geen advertenties.',
        'Jouw data blijft van jou. Exporteren en wissen zijn ingebouwd.',
      ],
    },
    cta: {
      heading: 'Ik zoek 20 mensen die mee willen testen',
      body: 'Geen kosten. Wel betrokken: af en toe een gesprek over wat werkt en wat niet, en wat je zelf nodig hebt in zo’n tool.',
    },
    profile: {
      heading: 'Wat ik zoek',
      items: [
        'Je hebt zelf ervaring met een chronische aandoening.',
        'Je weet wat pacing betekent in de praktijk.',
        'Je gelooft in een tool die niet commercieel is, maar specifiek gemaakt voor deze doelgroep.',
        'Je denkt graag mee. Niet alleen als gebruiker, maar als medeontwerper.',
      ],
    },
    email: {
      prefix: 'Mail me',
      address: 'Willem@brightpath-studio.nl',
      subject: 'Gevoelscore: interesse als core backer',
      bodyTemplate:
        'Hoi Willem,\n\nIk heb jouw pagina over Gevoelscore gelezen en wil graag meedoen.\n\n(Vertel iets over jezelf en je situatie als je wilt.)\n\nGroet,\n',
    },
  },
} as const;
