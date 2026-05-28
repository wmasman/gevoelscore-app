import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import { copy } from '@/copy';
import './globals.css';

// Font: Inter via next/font/google. Self-hosted (no Google Fonts CDN at
// runtime), subset to Latin, weights matched to the design-system scale
// (400/500/600). Picked over system-ui for cross-device consistency —
// without it, iOS renders SF Pro and Android/Windows render Roboto/Segoe.
// See docs/design/brief.md and .superdesign/design-system.md.
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  weight: ['400', '500', '600'],
  display: 'swap',
});

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
  themeColor: '#faf6f1',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="nl" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
