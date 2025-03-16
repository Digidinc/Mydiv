'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/services/api';
import { SymbolJourney, DailySymbol } from '@/types/symbols';
import SymbolGrid from '@/components/symbols/SymbolGrid';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Calendar, Trophy, Flame, Star } from 'lucide-react';

export default function PathOfSymbolsPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [journey, setJourney] = useState<SymbolJourney | null>(null);
  const [dailySymbol, setDailySymbol] = useState<DailySymbol | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login?redirect=/path-of-symbols');
      return;
    }

    const fetchData = async () => {
      try {
        const [journeyResponse, dailyResponse] = await Promise.all([
          api.getSymbolJourney(),
          api.getDailySymbol(),
        ]);
        setJourney(journeyResponse.data);
        setDailySymbol(dailyResponse.data);
      } catch (err) {
        setError('Failed to load your symbol journey. Please try again.');
        console.error('Error fetching journey data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    if (user) {
      fetchData();
    }
  }, [user, authLoading, router]);

  const handleSymbolInteraction = async (symbolId: string, type: 'study' | 'meditation' | 'practice' | 'insight') => {
    try {
      await api.recordSymbolInteraction({
        symbolId,
        type,
        timestamp: new Date(),
        duration: 0, // This would be set based on actual interaction time
      });

      // Refresh journey data to get updated progress
      const response = await api.getSymbolJourney();
      setJourney(response.data);
    } catch (err) {
      console.error('Error recording interaction:', err);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="container mx-auto py-8 flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error || !journey) {
    return (
      <div className="container mx-auto py-8 px-4">
        <Card className="max-w-lg mx-auto p-6 text-center">
          <h2 className="text-2xl font-bold mb-4">Error</h2>
          <p className="text-muted-foreground mb-6">{error || 'Failed to load journey data.'}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Level</CardTitle>
              <Star className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{journey.currentLevel}</div>
              <Progress
                value={(journey.unlockedSymbols / journey.totalSymbols) * 100}
                className="mt-2"
              />
              <p className="text-xs text-muted-foreground mt-2">
                {journey.unlockedSymbols} of {journey.totalSymbols} symbols unlocked
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Daily Streak</CardTitle>
              <Flame className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{journey.dailyStreak} days</div>
              <p className="text-xs text-muted-foreground mt-2">
                Last interaction: {new Date(journey.lastUnlock).toLocaleDateString()}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Achievements</CardTitle>
              <Trophy className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {journey.achievements.filter(a => a.unlockedAt).length}
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                {journey.achievements.length} total achievements
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Daily Symbol</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {dailySymbol && (
                <div className="space-y-2">
                  <div className="text-2xl font-bold">{dailySymbol.symbol.name}</div>
                  <Badge variant="secondary">{dailySymbol.symbol.category}</Badge>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {dailySymbol && (
          <Card>
            <CardHeader>
              <CardTitle>Today's Focus</CardTitle>
              <CardDescription>
                {dailySymbol.message}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-2">Daily Affirmation</h4>
                  <p className="italic">{dailySymbol.affirmation}</p>
                </div>
                {dailySymbol.challenge && (
                  <div>
                    <h4 className="font-semibold mb-2">Daily Challenge</h4>
                    <p>{dailySymbol.challenge.description}</p>
                    <Badge variant="outline" className="mt-2">
                      Reward: {dailySymbol.challenge.reward} XP
                    </Badge>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        <Tabs defaultValue="all" className="space-y-6">
          <TabsList>
            <TabsTrigger value="all">All Symbols</TabsTrigger>
            <TabsTrigger value="unlocked">Unlocked</TabsTrigger>
            <TabsTrigger value="locked">Locked</TabsTrigger>
            <TabsTrigger value="achievements">Achievements</TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="space-y-6">
            <SymbolGrid
              symbols={journey.symbols}
              onSymbolInteraction={handleSymbolInteraction}
            />
          </TabsContent>

          <TabsContent value="unlocked" className="space-y-6">
            <SymbolGrid
              symbols={journey.symbols.filter(s => s.unlocked)}
              onSymbolInteraction={handleSymbolInteraction}
            />
          </TabsContent>

          <TabsContent value="locked" className="space-y-6">
            <SymbolGrid
              symbols={journey.symbols.filter(s => !s.unlocked)}
              onSymbolInteraction={handleSymbolInteraction}
            />
          </TabsContent>

          <TabsContent value="achievements" className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {journey.achievements.map((achievement) => (
                <Card
                  key={achievement.id}
                  className={achievement.unlockedAt ? 'bg-primary/5' : ''}
                >
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{achievement.name}</CardTitle>
                      {achievement.unlockedAt && (
                        <Trophy className="h-5 w-5 text-primary" />
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-4">
                      {achievement.description}
                    </p>
                    <Progress
                      value={(achievement.progress / achievement.requiredProgress) * 100}
                    />
                    <p className="text-xs text-muted-foreground mt-2">
                      {achievement.progress} / {achievement.requiredProgress}
                    </p>
                    {achievement.unlockedAt && (
                      <Badge variant="outline" className="mt-4">
                        Unlocked {new Date(achievement.unlockedAt).toLocaleDateString()}
                      </Badge>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}