import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import { copy } from '@/copy';
import './globals.css';

// Self-hosted via Next's font system — no runtime calls to Google Fonts at
// page load (so no third-party privacy leak). `display: swap` minimises FOUT
// while keeping body text readable from first paint.
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sans',
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
  themeColor: '#fdfcfa',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="nl" className={inter.variable}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
