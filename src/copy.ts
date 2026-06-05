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
    // Step-1 today-card ongoing-episodes region (2026-06-02). Renders
    // below the Tags region when at least one episode is currently
    // active — end_date is null (lopend) OR in the future. The aria-
    // label drops the "lopend" qualifier so the same string works for
    // both fixed-end-in-the-future and open-ended episodes.
    ongoingRegionLabel: 'Loopt nu',
    ongoingEditAriaLabel: (label: string): string =>
      `${label}, tik om te bewerken`,
    // Step-2 Phase 2.D today-card events region (2026-06-05). Renders
    // between Tags and OngoingEpisodes when there are events overlapping
    // today with included_as_context=true. Heading mirrors the Context
    // tab's "Activiteiten" for the same surface naming across views.
    todayEvents: {
      regionLabel: 'Activiteiten',
      allDayLabel: 'Hele dag',
      expandMore: (n: number): string => `+ ${n} meer`,
      collapseLess: 'Minder',
    },
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
    // Step-1 timeline-episode-overlay: per-category visibility toggles
    // for the bands on the line chart + the stripes on the heatmap.
    episodeToggle: {
      groupAriaLabel: 'Periodes tonen',
      interventies: 'Interventies',
      periodes: 'Periodes',
    },
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
    // v1.6 — kalender-integration surface inside /settings, between
    // Account and Tag-beheer (placed above tag-beheer because it's a
    // setup activity; tag-beheer is ongoing cleanup).
    calendars: {
      heading: 'Kalenders',
      emptyState: 'Geen kalenders verbonden.',
      connectGoogle: 'Verbind Google Calendar',
      connectOther: '+ Verbind een andere kalender',
      otherComingSoon: 'Binnenkort: Outlook, Apple',
      // (email) — row label
      rowLabel: (email: string): string => email,
      statusActive: 'Verbonden',
      statusError: 'Fout',
      statusDisconnected: 'Ontkoppeld',
      // (relative) — e.g. "Gesynchroniseerd: 2 uur geleden"
      lastSyncedAt: (relative: string): string => `Gesynchroniseerd: ${relative}`,
      neverSynced: 'Nog niet gesynchroniseerd',
      refresh: 'Ververs nu',
      refreshing: 'Synchroniseren...',
      disconnect: 'Ontkoppel',
      disconnectConfirmPrompt:
        'Deze kalender ontkoppelen? Bestaande events worden verwijderd. De koppeling met Google wordt ingetrokken.',
      disconnectConfirmYes: 'Ja, ontkoppel',
      disconnectConfirmCancel: 'Annuleren',
      disconnecting: 'Ontkoppelen...',
      connectError: 'Verbinden lukte niet. Probeer opnieuw.',
      refreshError: 'Synchroniseren lukte niet. Probeer opnieuw.',
      disconnectError: 'Ontkoppelen lukte niet. Probeer opnieuw.',
      revokeFailedWarning:
        'Lokaal verwijderd, maar intrekken bij Google lukte niet. Trek de toegang handmatig in via myaccount.google.com.',
      // Context-tab events section (the list above Periodes).
      contextSection: {
        heading: 'Activiteiten',
        showExcluded: 'Toon overgeslagen events',
        excludedSuffix: '(overgeslagen)',
        allDayLabel: 'Hele dag',
        emptyAriaLabel: 'Geen activiteiten op deze dag',
      },
      // Per-event detail sheet (opened from Context tab + Today card).
      eventSheet: {
        sheetAriaLabel: 'Event details',
        close: 'Sluit',
        allDayLabel: 'Hele dag',
        timeRangeSeparator: '–', // en-dash for time ranges, NOT em-dash
        recurringBadge: 'Herhalend',
        linkTagButton: 'Koppel aan tag',
        linkedTagLabel: (label: string): string => `Tag: ${label}`,
        linkEpisodeButton: 'Koppel aan periode',
        linkedEpisodeLabel: (label: string): string => `Periode: ${label}`,
        excludeButton: 'Sluit uit als context',
        excludeRecurringButton: 'Sluit hele serie uit',
        reincludeButton: 'Weer meenemen',
        reincludeSeriesButton: 'Voeg hele serie weer toe',
        tagPickerTitle: 'Kies een tag',
        episodePickerTitle: 'Kies een periode',
        pickerBack: 'Terug',
        pickerNone: 'Geen',
        pickerEmptyTags: 'Geen tags beschikbaar.',
        pickerEmptyEpisodes: 'Geen periodes beschikbaar.',
        actionError: 'Actie lukte niet. Probeer opnieuw.',
      },
      // /settings/kalenders/choose screen — post-OAuth calendar selection.
      choose: {
        title: 'Kies kalenders',
        intro:
          'Vink aan welke kalenders meegenomen moeten worden als context. Je kunt dit later altijd aanpassen.',
        loading: 'Kalenders laden...',
        loadError: 'Kalenders ophalen lukte niet. Probeer opnieuw.',
        retryLoad: 'Opnieuw laden',
        primaryBadge: 'Hoofd',
        submit: 'Verbinden',
        submitting: 'Bezig...',
        cancel: 'Annuleren',
        submitError: 'Opslaan lukte niet. Probeer opnieuw.',
        // v1.6.1: when the user excludes a previously-included calendar
        // and we know it has existing events, ask explicitly whether to
        // remove those. Two-option confirm, defaulting to keep (data-
        // preserving). Counts are inserted as plain digits.
        excludeConfirm: {
          // (n) — total events about to be removed across all excluded calendars
          title: (n: number): string =>
            n === 1
              ? '1 event van een uitgesloten kalender'
              : `${n} events van uitgesloten kalenders`,
          body:
            'Je hebt kalenders uitgevinkt. Wil je de bestaande events van die kalenders verwijderen? Toekomstige syncs halen ze sowieso niet meer op.',
          // (name, n)
          row: (name: string, n: number): string =>
            n === 1 ? `${name}: 1 event` : `${name}: ${n} events`,
          rowUnknown: (n: number): string =>
            `Onbekende kalenders (oudere import): ${n} event${n === 1 ? '' : 's'}`,
          deleteButton: 'Ja, verwijder bestaande events',
          keepButton: 'Nee, alleen niet meer ophalen',
          cancelButton: 'Annuleren',
        },
      },
    },
    // Step v1.5b — tag-management surface inside /settings, between
    // Account and Data. Drill-down via TagFormSheet (BottomSheet).
    tagManagement: {
      heading: 'Tag-beheer',
      showArchivedToggle: 'Toon gearchiveerd',
      archivedSuffix: '(gearchiveerd)',
      emptyCorpus: 'Geen tags. Tags maak je in het Vandaag-scherm.',
      // (label, dutch category) — read by screen readers on tap-into-row
      rowAriaLabel: (label: string, categoryDutch: string): string =>
        `${label}, ${categoryDutch}, tik om te bewerken`,
      // (label, count, dutch-date) — read inside the form's Status block
      statusUsed: (count: number, dutchDate: string): string =>
        count === 1
          ? `1 keer gebruikt, laatst ${dutchDate}`
          : `${count} keer gebruikt, laatst ${dutchDate}`,
      statusNeverUsed: 'Nog niet gebruikt',
      // Dutch category labels — same set as TagPickerSheet's CATEGORY_LABEL
      categoryLabel: {
        mentaal: 'Mentaal',
        fysiek: 'Fysiek',
        overall: 'Overall',
        activiteit: 'Activiteit',
        gebeurtenis: 'Gebeurtenis',
        interventie: 'Interventie',
        project: 'Project',
        custom: 'Custom',
      },
      // TagFormSheet copy — the BottomSheet that opens on row-tap.
      form: {
        sheetAriaLabel: 'Tag bewerken',
        title: 'Tag bewerken',
        close: 'Sluit',
        labelField: 'Naam',
        categoryField: 'Categorie',
        parentField: 'Behoort bij',
        parentNone: 'Geen',
        save: 'Bewaar',
        saving: 'Even geduld…',
        archive: 'Archiveer',
        unarchive: 'Activeer opnieuw',
        delete: 'Verwijder',
        deleteHint: 'Alleen mogelijk als de tag nooit gebruikt is.',
        // inline confirm alertdialog (M5: focus lands on Annuleer)
        confirm: {
          prompt: (label: string): string =>
            `Tag "${label}" definitief verwijderen? Deze actie kan niet ongedaan gemaakt worden.`,
          cancel: 'Annuleer',
          confirm: 'Ja, verwijder',
        },
        error: {
          labelEmpty: 'Geef een naam.',
          labelTooLong: 'Maximaal 40 tekens.',
          labelTooManyWords: 'Maximaal 2 woorden.',
          categoryMissing: 'Kies een categorie.',
          serverError: 'Opslaan lukte niet, probeer opnieuw.',
          // Per-field server errors (M1 fix dividend)
          invalidLabel: 'Naam is ongeldig.',
          invalidCategory: 'Categorie is ongeldig.',
          invalidArchivedAt: 'Archiveerstatus is ongeldig.',
          invalidParent: 'Episode is ongeldig.',
          tagInUse: 'Tag is in gebruik en kan niet verwijderd worden.',
        },
      },
      // Tag-merge (v1.5c) — see docs/features/tag-merge/
      merge: {
        buttonLabel: 'Samenvoegen met...',
        sheetTitle: 'Samenvoegen met...',
        sheetAriaLabel: 'Tag samenvoegen',
        close: 'Sluit',
        emptyState: 'Geen andere tags in deze categorie om mee samen te voegen.',
        confirm: {
          prompt: (
            sourceLabel: string,
            usageCount: number,
            targetLabel: string,
          ): string =>
            `Tag "${sourceLabel}" samenvoegen met "${targetLabel}"? ${usageCount} ${usageCount === 1 ? 'dag waarop' : 'dagen waarop'} "${sourceLabel}" voorkomt ${usageCount === 1 ? 'krijgt' : 'krijgen'} "${targetLabel}". Daarna wordt "${sourceLabel}" definitief verwijderd.`,
          cancel: 'Annuleer',
          confirm: 'Ja, samenvoegen',
        },
        error: {
          sameTag: 'Dit is dezelfde tag.',
          sourceNotFound: 'Tag bestaat niet meer.',
          targetNotFound: 'Doel-tag bestaat niet meer.',
          sourceArchived: 'Deze tag is gearchiveerd. Activeer eerst opnieuw.',
          targetArchived: 'Doel-tag is gearchiveerd. Activeer eerst opnieuw.',
          categoryMismatch: 'Tags moeten in dezelfde categorie staan.',
          serverError: 'Samenvoegen lukte niet, probeer opnieuw.',
        },
      },
    },
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
