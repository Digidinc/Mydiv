import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import RootLayout from '@/components/layout/RootLayout';
import { cn } from '@/lib/utils';
import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'MyDivinations - Discover Your Archetypal Patterns',
  description:
    'MyDivinations is an AI-driven divination platform that uses Fractal Resonance Cognition (FRC) to help users discover archetypal patterns and increase consciousness through interactive experiences.',
  keywords: [
    'astrology',
    'divination',
    'birth chart',
    'archetypal patterns',
    'consciousness',
    'fractal resonance',
    'AI divination',
  ],
};

export default function Layout({ children }: { children: React.ReactNode }): JSX.Element {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn('min-h-screen bg-background font-sans antialiased', inter.className)}>
        <RootLayout>{children}</RootLayout>
      </body>
    </html>
  );
}