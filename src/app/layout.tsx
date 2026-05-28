import type { Metadata, Viewport } from 'next';
import { copy } from '@/copy';
import './globals.css';

// Font: system-ui stack (defined in globals.css). next/font/google was
// considered but the cold-load delay in dev mode added latency on top
// of the existing dev-server compile; system-ui is high-legibility and
// zero-cost. Revisit if a custom self-hosted font becomes a priority.

export const metadata: Metadata = {
  title: {
    default: copy.app.title,
    template: `%s | ${copy.app.title}`,
  },
  description: copy.app.description,
  applicationName: copy.app.title,
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  // viewport-fit=cover lets us paint to the edge on notched phones.
  viewportFit: 'cover',
  // Matches --color-bg in globals.css; keeps the browser chrome blended.
  themeColor: '#fdfcfa',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="nl">
      <body>{children}</body>
    </html>
  );
}
