# Contributing

This is primarily a personal project, but contributions are welcome.

## Scope guardrails

Before opening a PR or issue, read [README.md](README.md) and [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md). The cardinal principle is **daily entry must not get more complex**. Features that add friction to the one-tap daily flow will be declined regardless of how clever they are.

## Good first contributions

- Typos or clarifications in the docs
- Test coverage for existing behavior
- Bug reports with reproducible steps
- Discussion issues for v1.5 / v2 features (calendar, HealthKit, Garmin)

## Things that probably won't be accepted

- Social features, sharing, multi-user
- AI / chat features inside the app
- Symptom encyclopedia or medical-advice content
- Analytics, tracking, ad code
- Unsolicited notifications (default-on reminders, re-engagement push, marketing). Opt-in reminders are allowed — currently scoped to the v2 end-of-day score reminder.

## Code style

To be determined once a framework is chosen. Until then, no code lives here yet.

## Reporting security issues

Don't open a public issue for security vulnerabilities. Email the maintainer (see git history for contact) and allow time for a fix before disclosure.

## Personal data

Never include real personal health data in PRs, issues or commits. Use the anonymized sample in `docs/sample-data.csv` for development.
