// Centralised Dutch UI strings. Components import from here rather than
// inline strings so future copy edits + the eventual i18n seam are tractable.
//
// Keep keys grouped by feature surface (app, daily, timeline, errors).

export const copy = {
  app: {
    title: 'Gevoelscore',
    description: 'Persoonlijke dagscore voor Long COVID — registreer in één tik.',
  },
  daily: {
    score: {
      label: 'Score',
      placeholder: 'Tik om te kiezen',
    },
    note: {
      label: 'Notitie',
      placeholder: 'Notitie (optioneel)',
    },
    tags: {
      label: 'Tags',
      empty: 'Geen tags in deze categorie',
      none: 'Geen tags',
    },
  },
  timeline: {
    title: 'Tijdlijn',
    range30: '30 dagen',
    range90: '90 dagen',
    edited: 'bewerkt',
    streak: (n: number): string =>
      n === 1 ? '1 dag achter elkaar' : `${n} dagen achter elkaar`,
  },
  errors: {
    notSaved: 'Niet opgeslagen — probeer nogmaals',
    generic: 'Er ging iets mis. Probeer opnieuw.',
    notFound: 'Pagina niet gevonden',
  },
} as const;
