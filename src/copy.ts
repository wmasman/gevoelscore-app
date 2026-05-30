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
      empty: 'Geen tags in deze categorie',
      none: 'Geen tags',
      extraToggle: 'Extra opties (Interventie, Project, etc)',
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
