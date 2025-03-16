'use client';

import { format } from 'date-fns';
import { motion } from 'framer-motion';
import { AlertTriangle, CheckCircle, Clock, Info, Star } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Transit } from '@/types/transits';

interface TransitDetailProps {
  transit: Transit;
  onClose: () => void;
}

const NATURE_ICONS = {
  harmonious: CheckCircle,
  challenging: AlertTriangle,
  neutral: Info,
};

export default function TransitDetail({ transit, onClose }: TransitDetailProps) {
  const NatureIcon = NATURE_ICONS[transit.influence.nature];
  const progress = calculateProgress(transit);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
    >
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{transit.transitingPlanet.symbol}</span>
              <span className="text-xl">
                {getAspectSymbol(transit.aspect.type)}
              </span>
              <span className="text-2xl">{transit.natalPlanet.symbol}</span>
            </div>
            <Button variant="ghost" size="icon" onClick={onClose}>
              ×
            </Button>
          </div>
          <CardTitle className="flex items-center gap-2 mt-2">
            {transit.transitingPlanet.name} {transit.aspect.type}{' '}
            {transit.natalPlanet.name}
            <Badge
              variant={transit.influence.nature === 'challenging' ? 'destructive' : 'default'}
              className="ml-2"
            >
              <NatureIcon className="w-4 h-4 mr-1" />
              {transit.influence.nature}
            </Badge>
          </CardTitle>
          <CardDescription>
            Strength: {transit.influence.strength}/10
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <h3 className="font-semibold">Current Status</h3>
            <div className="flex items-center justify-between text-sm mb-2">
              <span>Progress</span>
              <span>{progress}%</span>
            </div>
            <Progress value={progress} />
            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="text-center">
                <div className="text-sm text-muted-foreground">Start</div>
                <div>{format(transit.influence.duration.start, 'PP')}</div>
              </div>
              <div className="text-center">
                <div className="text-sm text-muted-foreground">Peak</div>
                <div>{format(transit.influence.duration.peak, 'PP')}</div>
              </div>
              <div className="text-center">
                <div className="text-sm text-muted-foreground">End</div>
                <div>{format(transit.influence.duration.end, 'PP')}</div>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="font-semibold">Planetary Positions</h3>
            <div className="grid grid-cols-2 gap-4">
              <Card className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">{transit.transitingPlanet.symbol}</span>
                  <span className="font-medium">{transit.transitingPlanet.name}</span>
                </div>
                <div className="space-y-1 text-sm">
                  <div>
                    {transit.transitingPlanet.degree}° {transit.transitingPlanet.sign}
                  </div>
                  {transit.transitingPlanet.isRetrograde && (
                    <Badge variant="secondary">Retrograde</Badge>
                  )}
                </div>
              </Card>
              <Card className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">{transit.natalPlanet.symbol}</span>
                  <span className="font-medium">{transit.natalPlanet.name}</span>
                </div>
                <div className="space-y-1 text-sm">
                  <div>
                    {transit.natalPlanet.degree}° {transit.natalPlanet.sign}
                  </div>
                  <div>House {transit.natalPlanet.house}</div>
                </div>
              </Card>
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="font-semibold">Aspect Details</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Type:</span>{' '}
                {transit.aspect.type} ({transit.aspect.orb}°)
              </div>
              <div>
                <span className="text-muted-foreground">Direction:</span>{' '}
                {transit.aspect.isApplying ? 'Applying' : 'Separating'}
              </div>
              {transit.aspect.exactDate && (
                <div className="col-span-2">
                  <span className="text-muted-foreground">Exact on:</span>{' '}
                  {format(transit.aspect.exactDate, 'PPP')}
                </div>
              )}
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="font-semibold mb-2">Interpretation</h3>
              <p className="text-sm">{transit.interpretation.general}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card className="p-4">
                <h4 className="font-medium flex items-center gap-2 mb-2">
                  <Star className="w-4 h-4 text-primary" />
                  Opportunities
                </h4>
                <ul className="list-disc list-inside text-sm space-y-1">
                  {transit.interpretation.opportunities.map((opp, i) => (
                    <li key={i}>{opp}</li>
                  ))}
                </ul>
              </Card>

              <Card className="p-4">
                <h4 className="font-medium flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-4 h-4 text-destructive" />
                  Challenges
                </h4>
                <ul className="list-disc list-inside text-sm space-y-1">
                  {transit.interpretation.challenges.map((challenge, i) => (
                    <li key={i}>{challenge}</li>
                  ))}
                </ul>
              </Card>
            </div>

            <Card className="p-4">
              <h4 className="font-medium flex items-center gap-2 mb-2">
                <Info className="w-4 h-4" />
                Advice
              </h4>
              <ul className="list-disc list-inside text-sm space-y-1">
                {transit.interpretation.advice.map((advice, i) => (
                  <li key={i}>{advice}</li>
                ))}
              </ul>
            </Card>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

function calculateProgress(transit: Transit): number {
  const now = new Date();
  const { start, end } = transit.influence.duration;
  const total = end.getTime() - start.getTime();
  const current = now.getTime() - start.getTime();
  return Math.max(0, Math.min(100, (current / total) * 100));
}

function getAspectSymbol(aspect: string): string {
  const symbols: Record<string, string> = {
    conjunction: '☌',
    opposition: '☍',
    trine: '△',
    square: '□',
    sextile: '⚹',
    quincunx: '⚻',
    semisextile: '⚺',
    semisquare: '∠',
    sesquisquare: '⚼',
  };
  return symbols[aspect] || aspect;
}