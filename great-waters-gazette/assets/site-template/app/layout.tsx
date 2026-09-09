import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Great Waters Gazette',
  description: 'A concise daily digest of weather, technology, lighting, local news and more.',
  manifest: '/site.webmanifest',
  icons: {
    icon: [
      { url: '/favicon-32.png', sizes: '32x32', type: 'image/png' },
      { url: '/app-icon-192.png', sizes: '192x192', type: 'image/png' },
    ],
    apple: [{ url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' }],
  },
  openGraph: {
    title: 'Great Waters Gazette',
    description: 'A concise morning digest',
    images: [{ url: '/og.png', width: 1200, height: 630, alt: 'Great Waters Gazette' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Great Waters Gazette',
    description: 'A concise morning digest',
    images: ['/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
