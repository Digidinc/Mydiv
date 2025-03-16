import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function HomePage(): JSX.Element {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] py-12 text-center">
      <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl">
        Discover Your
        <span className="text-primary"> Archetypal Patterns</span>
      </h1>
      <p className="mt-4 text-xl text-muted-foreground max-w-[700px] mx-auto">
        MyDivinations uses AI-driven Fractal Resonance Cognition to help you understand your unique
        cosmic blueprint and increase consciousness through interactive experiences.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 mt-8">
        <Button size="lg" asChild>
          <Link href="/birth-chart">Generate Birth Chart</Link>
        </Button>
        <Button size="lg" variant="outline" asChild>
          <Link href="/symbols">Explore Path of Symbols</Link>
        </Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 max-w-[1200px] mx-auto px-4">
        <div className="flex flex-col items-center p-6 bg-card rounded-lg border">
          <h3 className="text-xl font-semibold mb-2">Astrological Insights</h3>
          <p className="text-muted-foreground text-center">
            Get detailed analysis of your birth chart with AI-powered interpretations.
          </p>
        </div>
        <div className="flex flex-col items-center p-6 bg-card rounded-lg border">
          <h3 className="text-xl font-semibold mb-2">Fractal Patterns</h3>
          <p className="text-muted-foreground text-center">
            Visualize your archetypal resonance through beautiful fractal animations.
          </p>
        </div>
        <div className="flex flex-col items-center p-6 bg-card rounded-lg border">
          <h3 className="text-xl font-semibold mb-2">Symbolic Journey</h3>
          <p className="text-muted-foreground text-center">
            Embark on an interactive journey through your personal symbolic landscape.
          </p>
        </div>
      </div>
    </div>
  );
}