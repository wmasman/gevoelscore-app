# ADR 0001: Use Expo (React Native) for v1

- **Status**: Accepted
- **Date**: 2026-05-26
- **Deciders**: Willem Masman (author), Claude (AI collaborator)

## Context

Choose a mobile framework for the gevoelscore-app. The choice must hold for v1 (score logging, tags, timeline, CSV import) and not block the v1.5 / v2 roadmap (Google Calendar read-only, Apple Health, Garmin via HealthKit, weather).

Decisive constraints from [REQUIREMENTS.md](../REQUIREMENTS.md) and the [brief](../app_brief_gevoelscore.md):

1. **Cardinal principle**: daily entry must not be more friction than the existing Google Sheet. One tap, ≤ 10 seconds, low cognitive load.
2. **Long COVID context**: the author works in bursts on good days and needs tools that don't require fighting muscle memory on bad days. Maintenance friction matters as much as ship friction.
3. **Author fluent in React / TypeScript** (TVO platform); not fluent in Swift.
4. **HealthKit is v2**, deferred ~12+ months. The hardest native integration is not a v1 concern.
5. **Cross-platform desirable but not required**. Author is on iPhone; no Android user committed yet.
6. **Open source from day 1**, MIT — wider contributor pool is a soft tiebreaker.
7. **Windows development machine** — Mac-required toolchains add friction.

## Options considered

### Native Swift / SwiftUI

- Best HealthKit access (no bridge layer)
- Best one-handed UX, battery, cold start, polish
- Author not Swift-fluent → reading code on brainfog days harder
- iOS lock-in; Android = full rewrite
- Requires Mac/Xcode toolchain
- Zero reuse with existing React stack

### Capacitor (Ionic)

- Maximum reuse of web/Next.js patterns
- Lowest learning curve given existing stack
- WebView UX has subtle responsiveness issues — risks violating the cardinal principle in ways hard to catch during prototyping
- HealthKit plugin ecosystem less mature
- Apple has historically scrutinized wrapped-WebView apps in review

### Expo (React Native) — chosen

- Author's fluent stack (JSX, TypeScript, hooks)
- Cross-platform free (Android comes along if ever wanted)
- Hot reload + type safety → brainfog-day friendly
- EAS Build means iOS compilation in the cloud (no Mac required)
- EAS Submit handles App Store uploads
- v1 has zero native deps → ships in managed workflow
- Large contributor pool

Accepted tradeoffs:
- HealthKit via `react-native-health` is a community bridge with occasional lag on newer metrics. Mitigation: write thin Swift native modules for any specific metric the bridge can't handle.
- Encrypted SQLite uses a community package (`op-sqlite` with SQLCipher, or similar) rather than first-party Apple primitives.
- Background tasks awkward in managed workflow — not a v1 problem; switch to a dev client when v1.5/v2 needs it.
- React Native major-version upgrades cost ~1 dev-day per year.

## Decision

**Use Expo (React Native) for v1, in the managed workflow.**

Switch to a custom Expo dev client (still Expo) when v1.5 or v2 needs native plugins (calendar, HealthKit). Write Swift native modules only for specific HealthKit metrics where the community bridge falls short.

## AI collaborator nuance

Claude (the AI collaborator on this project) is fluent in both Swift and React Native. This was considered explicitly and does not flip the decision because:

- The author still has to *read*, *maintain*, and *debug* the code on brainfog days. Code-writing speed is not the bottleneck.
- Cross-session memory continuity is weaker than a human teammate's.
- The Windows + cloud-build path is fundamentally simpler for Expo than for native Swift (Xcode dependency).
- The cardinal principle implicitly extends to maintenance friction, where Expo wins.

The AI fluency *does* lower the cost of writing Swift native modules later when v2 needs them — making the hybrid Expo + targeted Swift bridges the strong path.

## Consequences

### Positive
- v1 ships fast, in the author's strongest stack
- Architecture readiness for v1.5/v2 stays straightforward
- Cross-platform optionality preserved with zero up-front cost
- Mac never required for development or distribution

### Negative
- HealthKit edge-case metrics in v2 may require writing Swift bridges (1–2 days each)
- Encrypted SQLite uses community packages
- Cold start and battery slightly worse than native; acceptable for the use case

### Migration cost if revisited
- Full rewrite to native Swift, given v1 design already validated: ~6–8 weeks
- Partial migration via native bridges: 1–2 days per bridge
- User data: 100% portable via CSV / JSON / SQLite export (required by REQUIREMENTS.md)

## When to revisit

Revisit this ADR if any of these become true:

- HealthKit deep integration shifts from v2 to v1
- Author becomes Swift-fluent through another project
- An iOS-only human collaborator joins
- A real web/PWA companion becomes a primary goal
- React Native ecosystem stagnates relative to native iOS

## References

- [REQUIREMENTS.md](../REQUIREMENTS.md)
- [app_brief_gevoelscore.md](../app_brief_gevoelscore.md)
- [technisch_document.md](../technisch_document.md)
