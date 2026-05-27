// Canonical tag-pattern map for the gevoelscore v1 dataset.
// Shared by analyze-notes.mjs, seed-tags.mjs, and import-real-history.mjs.
//
// Each entry: { label, category, patterns }
//   - label    is the canonical Tag.label that appears in Directus
//   - category is one of the locked v1 enum values (see data-model.md)
//   - patterns is an array of case-insensitive regexes; ANY match counts
//
// Pattern design rules (learned from the analyzer iteration):
//   - Use word boundaries (\b) to avoid false matches (e.g. \bmoe\b not /moe/ which matches "moeder")
//   - Multiple synonyms per tag: e.g. brainfog matches "brain fog" AND "hersenmist" AND "wattenhoofd"
//   - Don't be greedy: `\bkalm\b` is correct; `/rust/` over-matches "rustig aan", "uitrusten", etc.
//   - One canonical label per concept — synonyms collapse to the same Tag

export const TAG_PATTERNS = {
  mentaal: [
    { label: 'brainfog', patterns: [/\bbrainfog\b/i, /\bbrain[ -]?fog\b/i, /hersenmist/i, /wattenhoofd/i] },
    { label: 'emotioneel', patterns: [/emotioneel/i, /emotionele/i] },
    { label: 'overprikkeld', patterns: [/overprikkeld/i, /\bprikkel/i] },
    { label: 'stress', patterns: [/\bstress\b/i, /gestrest/i] },
    { label: 'somber', patterns: [/somber/i, /verdriet/i, /verdrietig/i] },
    { label: 'labiel', patterns: [/labiel/i] },
    { label: 'mentaal_doodop', patterns: [/mentaal doodop/i, /mentaal op/i, /mentaal moe/i] },
    { label: 'niet helder', patterns: [/niet helder/i, /niet scherp/i, /geen helder hoofd/i] },
    { label: 'helder', patterns: [/\bhelder\b/i, /\bscherp\b/i] },
    { label: 'kalm', patterns: [/\bkalm\b/i, /rust in (mijn |het )?hoofd/i] }, // narrowed: no longer matches "rustig aan"
    { label: 'goede focus', patterns: [/goede focus/i, /goed kunnen denken/i] },
  ],

  fysiek: [
    { label: 'hoofdpijn', patterns: [/hoofdpijn/i, /\bkoppijn\b/i] },
    { label: 'moe', patterns: [/\bmoe\b/i, /vermoeid/i, /\buitgeput\b/i, /\bdoodop\b/i, /heel moe/i, /erg moe/i] },
    { label: 'zware benen', patterns: [/zware benen/i, /zere benen/i, /pijnlijke benen/i] },
    { label: 'spierpijn', patterns: [/spierpijn/i] },
    { label: 'nekpijn', patterns: [/nekpijn/i, /zere nek/i, /pijn in (de |mijn )?nek/i] },
    { label: 'rugpijn', patterns: [/rugpijn/i, /rug overbelast/i, /pijn in (de |mijn )?rug/i] },
    { label: 'slecht geslapen', patterns: [/slecht geslapen/i, /onrustig geslapen/i, /slechte nacht/i, /matige nacht/i, /niet ?goed geslapen/i] },
    { label: 'goed geslapen', patterns: [/goed geslapen/i, /\buitgeslapen\b/i, /diep geslapen/i, /lang geslapen/i] },
    { label: 'middagslaap', patterns: [/geslapen tussen de middag/i, /geslapen (in )?de middag/i, /tussen de middag (geslapen|liggen slapen|liggen rusten)/i, /middag(.{0,10})(geslapen|gerust)/i, /'s middags geslapen/i] },
    { label: 'verkouden', patterns: [/verkouden/i, /\bsnot\b/i, /loopneus/i, /snotterig/i, /snotneus/i] },
    { label: 'hoesten', patterns: [/\bhoesten\b/i, /\bhoest\b/i] },
    { label: 'koorts', patterns: [/koorts/i, /verhoging/i] },
    { label: 'misselijk', patterns: [/misselijk/i] },
    { label: 'keelpijn', patterns: [/keelpijn/i, /zere keel/i] },
    { label: 'groggy', patterns: [/groggy/i, /gaar wakker/i, /\bgaar\b/i, /duizelig/i, /wonky/i, /wappie/i, /wazig/i, /wat brak\b/i, /\bbrak\b/i] },
    { label: 'tintelingen', patterns: [/tintelingen/i, /tintelend/i] },
    { label: 'koortslip', patterns: [/koortslip/i] },
    { label: 'pem', patterns: [/\bpem\b/i, /post.exertional/i] },
    { label: 'goede energie', patterns: [/goede energie/i, /energie over/i] },
    { label: 'goed wakker', patterns: [/goed wakker/i, /goed opgestaan/i, /fris wakker/i, /fris opgestaan/i, /\bfris\b/i] },
    { label: 'geen pijn', patterns: [/geen hoofdpijn/i, /geen pijn/i, /pijnvrij/i] },
    { label: 'verbeterend', patterns: [/opgeknapt/i, /weer wat beter/i, /weer beter/i, /steeds beter/i, /begin me weer/i, /een stuk beter/i, /aan het herstellen/i] },
  ],

  overall: [
    { label: 'goede dag', patterns: [/goede dag/i, /\blel van een dag\b/i, /\btop\b/i, /\bgeslaagde dag\b/i] },
    { label: 'rotdag', patterns: [/rotdag/i, /slechte dag/i, /matige dag/i, /mindere dag/i] },
    { label: 'lekker snel', patterns: [/lekker snel/i] },
    { label: 'redelijke dag', patterns: [/redelijke dag/i, /redelijk goed/i, /redelijk goede/i, /best aardig/i, /best ok\b/i, /\bok\b/i] },
    { label: 'te veel gedaan', patterns: [/te ?veel gedaan/i, /teveel gevraagd/i, /iets teveel/i, /toch teveel/i, /over (mijn |de )?grens/i] },
    { label: 'energie sparen', patterns: [/energie sparen/i, /energie save/i, /handrem/i, /rustig aan/i, /energie doseren/i, /balansdag/i, /balans dag/i, /kalm aan/i] },
  ],

  activiteit: [
    { label: 'rustdag', patterns: [/rustdag/i, /\brust ?dag\b/i] },
    { label: 'wandelen', patterns: [/wandelen/i, /wandeling/i, /gewandeld/i, /rondje gelopen/i] },
    { label: 'fietsen', patterns: [/\bfietsen\b/i, /gefietst/i, /op de fiets/i] },
    { label: 'zeilen', patterns: [/zeilen/i, /gezeild/i] },
    { label: 'hardlopen', patterns: [/hardlopen/i, /hardloop/i, /\brun\b/i] },
    { label: 'kantoor', patterns: [/\bkantoor\b/i, /naar amsterdam/i] },
    { label: 'klussen', patterns: [/\bklus(je)?\b/i, /klusjes/i, /klussen/i, /geklust/i, /werkbank/i] },
    { label: 'koken', patterns: [/\bkoken\b/i, /gekookt/i, /avondeten gemaakt/i, /eten gemaakt/i, /eten klaargemaakt/i, /eten kookt/i] },
    { label: 'hockey', patterns: [/hockey/i] },
    { label: 'zwemles', patterns: [/zwemles/i, /zwemmen/i] },
    { label: 'sociaal', patterns: [/koffie met/i, /koffie gedronken/i, /op bezoek/i, /uit eten/i, /gezellig/i, /met mat\b/i, /met hans\b/i, /met dirkjan/i, /met jantine/i, /met astrid/i] },
    { label: 'computerwerk', patterns: [/achter de computer/i, /computer werk/i, /computerwerk/i, /e-?mails/i, /\blaptop\b/i, /pwc/i, /programmeer/i] },
    { label: 'voorlezen', patterns: [/voorgelezen/i, /voorlezen/i] },
    { label: 'meditatie', patterns: [/mediteren/i, /meditatie/i, /\bzen\b/i, /\bmindful/i] },
    { label: 'oppassen', patterns: [/\boppassen\b/i, /gepast/i, /op (tobias|tijmen|de kids|de kinderen)/i, /\bkids\b.{0,30}\b(op )?gepast\b/i] },
  ],

  gebeurtenis: [
    { label: 'verjaardag', patterns: [/verjaardag/i, /\bjarig\b/i] },
    { label: 'huwelijk', patterns: [/huwelijk/i, /\btrouwen\b/i, /trouwerij/i, /trouwde/i] },
    { label: 'begrafenis', patterns: [/begrafenis/i, /uitvaart/i] },
    { label: 'vakantie', patterns: [/vakantie/i, /weekendje weg/i, /\bweekendje\b/i, /kamperen/i, /\bcamping\b/i] },
    { label: 'ziekenhuisbezoek', patterns: [/ziekenhuis/i, /huisartsenpost/i] },
    { label: 'huisarts', patterns: [/huisarts/i] },
    { label: 'therapeut', patterns: [/therapeut/i, /relatietherapeut/i, /\bcoaching\b/i, /\bcoach\b/i, /gezinscoach/i] },
    { label: 'bedrijfsarts', patterns: [/bedrijfsarts/i, /verzekeringsarts/i, /\buwv\b/i, /re-?integratie/i] },
    { label: 'familiebezoek', patterns: [/familie /i, /familiebezoek/i, /reeuwijk/i, /nijverdal/i, /muiderberg/i, /winterberg/i] },
    { label: 'logeren', patterns: [/logeren/i, /uit logeren/i] },
    { label: 'tandarts', patterns: [/tandarts/i, /wortelkanaal/i, /wortel kanaal/i] },
    { label: 'feest', patterns: [/\bfeest/i, /borrel/i, /barbecue/i] },
    { label: 'studiedag', patterns: [/studiedag/i] },
    { label: 'efteling', patterns: [/efteling/i, /pretpark/i, /archeon/i] },
    { label: 'bestuursweekend', patterns: [/bestuursweekend/i, /\bbestuur\b/i] },
    { label: 'bouwdorp', patterns: [/bouwdorp/i] },
    { label: 'museum', patterns: [/\bmuseum\b/i, /\bbios\b/i, /\bfilm\b/i] },
    { label: 'congres', patterns: [/congres/i, /redactievergadering/i, /redactie/i] },
    { label: 'partner_weg', patterns: [/jantine.{0,30}\b(bonaire|australia|reis|weg|vertrokken|naar de cariben)/i, /jantine is naar/i, /jantine.{0,30}cariben/i, /\bweg vanaf\b/i] },
  ],

  interventie: [
    { label: 'citalopram', patterns: [/citalopram/i, /\bssri\b/i] },
    { label: 'cpap', patterns: [/\bcpap\b/i, /apneu apparaat/i, /\bapneu\b/i] },
    { label: 'naproxen', patterns: [/naproxen/i] },
    { label: 'ibuprofen', patterns: [/ibuprofen/i, /pijnstiller/i, /paracetamol/i] },
    { label: 'breinvoeding', patterns: [/breinvoeding/i] },
    { label: 'heartmath', patterns: [/heartmath/i, /hrv ?oefening/i, /\bcoherence\b/i] },
    { label: 'ademhalingsoefening', patterns: [/ademhalingsoefening/i, /\bademhaling\b/i] },
    { label: 'q10_magnesium', patterns: [/\bq10\b/i, /magnesium/i, /l ?carnitine/i] },
    { label: 'mindfulness', patterns: [/mindful/i, /zen meditatie/i] },
    { label: 'biofeedback', patterns: [/biofeedback/i] },
  ],
};

/**
 * Match a note string against all patterns; return the set of matching tag labels.
 */
export function matchTags(noteText) {
  if (!noteText) return [];
  const matched = new Set();
  for (const [, candidates] of Object.entries(TAG_PATTERNS)) {
    for (const { label, patterns } of candidates) {
      if (patterns.some((p) => p.test(noteText))) {
        matched.add(label);
      }
    }
  }
  return Array.from(matched);
}

/**
 * Flat list of all tags in canonical order. Used by seed-tags.mjs.
 */
export function flatTagList() {
  const out = [];
  for (const [category, candidates] of Object.entries(TAG_PATTERNS)) {
    for (const { label } of candidates) {
      out.push({ label, category });
    }
  }
  return out;
}
