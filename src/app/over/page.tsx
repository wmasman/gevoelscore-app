import type { Metadata } from 'next';
import { copy } from '@/copy';

// Public landing / backer-recruitment page. No auth required — exempted in
// src/middleware.ts so anonymous visitors can read it. Static server-rendered;
// no client interactivity beyond the mailto link and native <details>.

export const metadata: Metadata = {
  title: 'Word core backer',
  description: copy.over.subtitle,
};

function buildMailto(): string {
  const { address, subject, bodyTemplate } = copy.over.email;
  const qs = new URLSearchParams({ subject, body: bodyTemplate });
  return `mailto:${address}?${qs.toString()}`;
}

export default function OverPage() {
  const mailtoHref = buildMailto();
  const { stat, story, principles, cta, profile, email } = copy.over;

  return (
    <main className="mx-auto flex max-w-[560px] flex-col gap-10 px-5 py-12 sm:px-6 sm:py-16">
      {/* Hero */}
      <header className="flex flex-col gap-3">
        <h1 className="text-3xl font-semibold tracking-tight">{copy.over.title}</h1>
        <p className="text-fg-muted">{copy.over.subtitle}</p>
      </header>

      {/* Stat — concrete proof point, the brief's "subtle accent elevation" pattern */}
      <div className="flex items-baseline gap-3">
        <span className="text-4xl font-semibold text-accent tabular-nums">
          {stat.number}
        </span>
        <span className="text-fg-muted">{stat.label}</span>
      </div>

      {/* Story — collapsed by default; reveals the September 2022 + Google Sheet narrative */}
      <details className="group">
        <summary className="flex cursor-pointer list-none items-center gap-2 [&::-webkit-details-marker]:hidden">
          <span
            aria-hidden="true"
            className="inline-block text-accent transition-transform duration-150 group-open:rotate-90"
          >
            ▸
          </span>
          <span className="font-medium text-accent underline-offset-4 group-hover:underline">
            {story.heading}
          </span>
        </summary>
        <div className="mt-3 flex flex-col gap-4 pl-6">
          <p>{story.body1}</p>
          <p>{story.body2}</p>
        </div>
      </details>

      {/* Principles — surface card adds visual weight without breaking the restrained tone */}
      <section
        aria-labelledby="principles-heading"
        className="flex flex-col gap-4 rounded-2xl border border-border bg-surface p-6 shadow-sm"
      >
        <h2 id="principles-heading" className="text-xl font-semibold">
          {principles.heading}
        </h2>
        <ul className="flex flex-col gap-3">
          {principles.items.map((item) => (
            <li key={item} className="flex gap-3">
              <span aria-hidden="true" className="select-none text-fg-subtle">
                ·
              </span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* CTA + profile */}
      <section aria-labelledby="cta-heading" className="flex flex-col gap-3">
        <h2 id="cta-heading" className="text-xl font-semibold">
          {cta.heading}
        </h2>
        <p>{cta.body}</p>
      </section>

      <section aria-labelledby="profile-heading" className="flex flex-col gap-3">
        <h2 id="profile-heading" className="text-xl font-semibold">
          {profile.heading}
        </h2>
        <ul className="flex flex-col gap-2">
          {profile.items.map((item) => (
            <li key={item} className="flex gap-3">
              <span aria-hidden="true" className="select-none text-fg-subtle">
                ·
              </span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* Button-style CTA — the page's single primary action */}
      <div className="flex justify-start pt-2">
        <a
          href={mailtoHref}
          className="inline-flex min-h-12 items-center gap-2 rounded-xl bg-accent px-6 py-3 font-medium text-surface shadow-sm transition-colors hover:bg-accent-hover focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
        >
          <span>
            {email.prefix}: {email.address}
          </span>
          <span aria-hidden="true">→</span>
        </a>
      </div>
    </main>
  );
}
