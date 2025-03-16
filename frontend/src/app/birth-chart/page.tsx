'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import BirthChartForm from '@/components/BirthChartForm';

export default function BirthChartPage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login?redirect=/birth-chart');
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="container mx-auto py-8 flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">Calculate Your Birth Chart</h1>
          <p className="text-xl text-muted-foreground">
            Discover your astrological blueprint and understand your unique cosmic signature
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="flex flex-col items-center text-center p-6 rounded-lg bg-card">
            <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <span className="text-2xl">🌟</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Planetary Positions</h3>
            <p className="text-muted-foreground">
              See where the planets were at the exact moment of your birth
            </p>
          </div>
          
          <div className="flex flex-col items-center text-center p-6 rounded-lg bg-card">
            <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <span className="text-2xl">⚡</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Aspects</h3>
            <p className="text-muted-foreground">
              Understand the relationships between planets in your chart
            </p>
          </div>
          
          <div className="flex flex-col items-center text-center p-6 rounded-lg bg-card">
            <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <span className="text-2xl">🏠</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Houses</h3>
            <p className="text-muted-foreground">
              Explore how the zodiac influences different areas of your life
            </p>
          </div>
        </div>

        <BirthChartForm />

        <div className="mt-12 text-center text-sm text-muted-foreground">
          <p>
            For the most accurate birth chart reading, please ensure you have your exact birth time and location.
            If you don't have your exact birth time, use 12:00 PM, but note that this will affect the accuracy of house placements and aspects.
          </p>
        </div>
      </div>
    </div>
  );
}