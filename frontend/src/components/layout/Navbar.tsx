import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from '@/components/theme/ThemeToggle';
import { UserNav } from '@/components/auth/UserNav';

export default function Navbar(): JSX.Element {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="hidden font-bold sm:inline-block">MyDivinations</span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <Link
              href="/birth-chart"
              className="transition-colors hover:text-foreground/80 text-foreground"
            >
              Birth Chart
            </Link>
            <Link
              href="/transits"
              className="transition-colors hover:text-foreground/80 text-foreground"
            >
              Transits
            </Link>
            <Link
              href="/symbols"
              className="transition-colors hover:text-foreground/80 text-foreground"
            >
              Path of Symbols
            </Link>
            <Link
              href="/readings"
              className="transition-colors hover:text-foreground/80 text-foreground"
            >
              Readings
            </Link>
          </nav>
        </div>
        <div className="ml-auto flex items-center space-x-4">
          <ThemeToggle />
          <UserNav />
        </div>
      </div>
    </header>
  );
}