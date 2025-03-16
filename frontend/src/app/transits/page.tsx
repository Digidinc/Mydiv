'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { format, addMonths, subMonths } from 'date-fns';
import { motion, AnimatePresence } from 'framer-motion';
import { Settings2, Bell, Calendar } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/services/api';
import { Transit, TransitPeriod, TransitSettings, TransitAlert } from '@/types/transits';
import TransitTimeline from '@/components/transits/TransitTimeline';
import TransitDetail from '@/components/transits/TransitDetail';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { DatePicker } from '@/components/ui/date-picker';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function TransitsPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [transitPeriod, setTransitPeriod] = useState<TransitPeriod | null>(null);
  const [selectedTransit, setSelectedTransit] = useState<Transit | null>(null);
  const [settings, setSettings] = useState<TransitSettings | null>(null);
  const [alerts, setAlerts] = useState<TransitAlert[]>([]);
  const [startDate, setStartDate] = useState(new Date());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login?redirect=/transits');
      return;
    }

    const fetchData = async () => {
      try {
        const [periodResponse, settingsResponse, alertsResponse] = await Promise.all([
          api.getTransitPeriod(startDate),
          api.getTransitSettings(),
          api.getTransitAlerts(),
        ]);
        setTransitPeriod(periodResponse.data);
        setSettings(settingsResponse.data);
        setAlerts(alertsResponse.data);
      } catch (err) {
        setError('Failed to load transit data. Please try again.');
        console.error('Error fetching transit data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    if (user) {
      fetchData();
    }
  }, [user, authLoading, router, startDate]);

  const handleDateChange = async (date: Date) => {
    setStartDate(date);
    setIsLoading(true);
    try {
      const response = await api.getTransitPeriod(date);
      setTransitPeriod(response.data);
    } catch (err) {
      setError('Failed to load transit data for the selected date.');
      console.error('Error fetching transit data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSettingsChange = async (newSettings: Partial<TransitSettings>) => {
    try {
      const response = await api.updateTransitSettings({
        ...settings!,
        ...newSettings,
      });
      setSettings(response.data);
    } catch (err) {
      console.error('Error updating settings:', err);
    }
  };

  const handleAlertRead = async (alertId: string) => {
    try {
      await api.markAlertRead(alertId);
      setAlerts(alerts.map(alert => 
        alert.id === alertId ? { ...alert, isRead: true } : alert
      ));
    } catch (err) {
      console.error('Error marking alert as read:', err);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="container mx-auto py-8 flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error || !transitPeriod || !settings) {
    return (
      <div className="container mx-auto py-8 px-4">
        <Card className="max-w-lg mx-auto p-6 text-center">
          <h2 className="text-2xl font-bold mb-4">Error</h2>
          <p className="text-muted-foreground mb-6">{error || 'Failed to load transit data.'}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </Card>
      </div>
    );
  }

  const unreadAlerts = alerts.filter(alert => !alert.isRead);

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">Transit Analysis</h1>
            <p className="text-muted-foreground">
              Explore how current planetary positions affect your birth chart
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">
                  <Calendar className="w-4 h-4 mr-2" />
                  {format(startDate, 'PP')}
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Choose Date</DialogTitle>
                  <DialogDescription>
                    Select a date to view transits
                  </DialogDescription>
                </DialogHeader>
                <DatePicker
                  date={startDate}
                  onDateChange={handleDateChange}
                />
                <div className="flex justify-between">
                  <Button
                    variant="outline"
                    onClick={() => handleDateChange(subMonths(startDate, 1))}
                  >
                    Previous Month
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => handleDateChange(addMonths(startDate, 1))}
                  >
                    Next Month
                  </Button>
                </div>
              </DialogContent>
            </Dialog>

            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">
                  <Settings2 className="w-4 h-4 mr-2" />
                  Settings
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Transit Settings</DialogTitle>
                  <DialogDescription>
                    Customize your transit analysis preferences
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-6">
                  <div>
                    <h4 className="font-medium mb-2">Notifications</h4>
                    <div className="flex items-center justify-between">
                      <span>Enable notifications</span>
                      <Switch
                        checked={settings.notifications.enabled}
                        onCheckedChange={(checked) => 
                          handleSettingsChange({
                            notifications: { ...settings.notifications, enabled: checked }
                          })
                        }
                      />
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Included Planets</h4>
                    <div className="flex flex-wrap gap-2">
                      {settings.includedPlanets.map((planet) => (
                        <Badge
                          key={planet}
                          variant="outline"
                          className="cursor-pointer"
                          onClick={() => {
                            const newPlanets = settings.includedPlanets.includes(planet)
                              ? settings.includedPlanets.filter(p => p !== planet)
                              : [...settings.includedPlanets, planet];
                            handleSettingsChange({ includedPlanets: newPlanets });
                          }}
                        >
                          {planet}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Included Aspects</h4>
                    <div className="flex flex-wrap gap-2">
                      {settings.includedAspects.map((aspect) => (
                        <Badge
                          key={aspect}
                          variant="outline"
                          className="cursor-pointer"
                          onClick={() => {
                            const newAspects = settings.includedAspects.includes(aspect)
                              ? settings.includedAspects.filter(a => a !== aspect)
                              : [...settings.includedAspects, aspect];
                            handleSettingsChange({ includedAspects: newAspects });
                          }}
                        >
                          {aspect}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </DialogContent>
            </Dialog>

            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">
                  <Bell className="w-4 h-4 mr-2" />
                  {unreadAlerts.length > 0 && (
                    <Badge variant="destructive" className="ml-2">
                      {unreadAlerts.length}
                    </Badge>
                  )}
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Transit Alerts</DialogTitle>
                  <DialogDescription>
                    Recent and upcoming transit events
                  </DialogDescription>
                </DialogHeader>
                <ScrollArea className="h-[400px]">
                  {alerts.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No alerts to display
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {alerts.map((alert) => (
                        <Card
                          key={alert.id}
                          className={alert.isRead ? 'opacity-70' : ''}
                        >
                          <CardHeader className="p-4">
                            <div className="flex items-center justify-between">
                              <Badge>
                                {format(alert.date, 'PP')}
                              </Badge>
                              {!alert.isRead && (
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleAlertRead(alert.id)}
                                >
                                  Mark as read
                                </Button>
                              )}
                            </div>
                            <CardTitle className="text-base">
                              {alert.message}
                            </CardTitle>
                          </CardHeader>
                        </Card>
                      ))}
                    </div>
                  )}
                </ScrollArea>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Transit Overview</CardTitle>
            <CardDescription>
              {format(transitPeriod.startDate, 'PP')} to {format(transitPeriod.endDate, 'PP')}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div>
                <h3 className="font-semibold mb-2">Major Themes</h3>
                <div className="flex flex-wrap gap-2">
                  {transitPeriod.summary.majorThemes.map((theme, i) => (
                    <Badge key={i} variant="secondary">{theme}</Badge>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="font-semibold mb-2">Significant Dates</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {transitPeriod.summary.significantDates.map((date, i) => (
                    <Card key={i} className="p-4">
                      <div className="font-medium">{format(date.date, 'PP')}</div>
                      <p className="text-sm text-muted-foreground mt-1">
                        {date.description}
                      </p>
                    </Card>
                  ))}
                </div>
              </div>

              <TransitTimeline
                transitPeriod={transitPeriod}
                onTransitClick={setSelectedTransit}
              />
            </div>
          </CardContent>
        </Card>

        <AnimatePresence>
          {selectedTransit && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
            >
              <TransitDetail
                transit={selectedTransit}
                onClose={() => setSelectedTransit(null)}
              />
            </motion.div>
          )}
        </AnimatePresence>

        <Tabs defaultValue="houses">
          <TabsList>
            <TabsTrigger value="houses">Houses</TabsTrigger>
            <TabsTrigger value="planets">Planets</TabsTrigger>
          </TabsList>
          <TabsContent value="houses">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {transitPeriod.houses.map((house) => (
                <Card key={house.number}>
                  <CardHeader>
                    <CardTitle>House {house.number}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span>Activity Level</span>
                        <span>{house.activity}/10</span>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {house.transits.length} active transits
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
          <TabsContent value="planets">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {transitPeriod.transits
                .reduce((acc, transit) => {
                  const planet = transit.transitingPlanet;
                  if (!acc[planet.name]) {
                    acc[planet.name] = {
                      ...planet,
                      transits: [],
                    };
                  }
                  acc[planet.name].transits.push(transit);
                  return acc;
                }, {} as Record<string, any>)
                .map((planet) => (
                  <Card key={planet.name}>
                    <CardHeader>
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">{planet.symbol}</span>
                        <CardTitle>{planet.name}</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div>
                          {planet.degree}° {planet.sign}
                          {planet.isRetrograde && (
                            <Badge variant="secondary" className="ml-2">
                              Retrograde
                            </Badge>
                          )}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {planet.transits.length} active aspects
                        </div>
                      </div>
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