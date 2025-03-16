'use client';

import { useState } from 'react';
import Image from 'next/image';
import { motion, AnimatePresence } from 'framer-motion';
import { Lock, Unlock, Star, Clock } from 'lucide-react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Symbol } from '@/types/symbols';
import { cn } from '@/lib/utils';

interface SymbolCardProps {
  symbol: Symbol;
  onInteract?: (type: 'study' | 'meditation' | 'practice' | 'insight') => void;
  className?: string;
}

export default function SymbolCard({ symbol, onInteract, className }: SymbolCardProps) {
  const [isFlipped, setIsFlipped] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  const handleFlip = () => {
    if (!symbol.unlocked) return;
    setIsFlipped(!isFlipped);
  };

  const handleInteraction = (type: 'study' | 'meditation' | 'practice' | 'insight') => {
    onInteract?.(type);
    setShowDetails(false);
  };

  return (
    <>
      <motion.div
        className={cn(
          'relative cursor-pointer perspective-1000',
          !symbol.unlocked && 'opacity-75 grayscale',
          className
        )}
        whileHover={{ scale: 1.02 }}
        onClick={handleFlip}
      >
        <AnimatePresence initial={false} mode="wait">
          <motion.div
            key={isFlipped ? 'back' : 'front'}
            initial={{ rotateY: isFlipped ? -180 : 0 }}
            animate={{ rotateY: isFlipped ? 0 : 180 }}
            exit={{ rotateY: isFlipped ? 180 : -180 }}
            transition={{ duration: 0.4 }}
            className="preserve-3d"
          >
            <Card className={cn(
              'w-full backface-hidden',
              isFlipped ? 'hidden' : 'block'
            )}>
              <CardHeader className="relative">
                {!symbol.unlocked && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black/50 rounded-t-lg">
                    <Lock className="w-8 h-8 text-white" />
                  </div>
                )}
                <div className="relative w-full aspect-square rounded-lg overflow-hidden">
                  <Image
                    src={symbol.imageUrl}
                    alt={symbol.name}
                    fill
                    className="object-cover"
                  />
                </div>
              </CardHeader>
              <CardContent>
                <CardTitle className="flex items-center justify-between">
                  {symbol.name}
                  <Badge variant="outline">{symbol.category}</Badge>
                </CardTitle>
                <CardDescription className="mt-2 line-clamp-2">
                  {symbol.description}
                </CardDescription>
              </CardContent>
              <CardFooter>
                <div className="w-full space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Progress</span>
                    <span>{symbol.progress}%</span>
                  </div>
                  <Progress value={symbol.progress} />
                </div>
              </CardFooter>
            </Card>

            <Card className={cn(
              'w-full absolute top-0 backface-hidden',
              !isFlipped ? 'hidden' : 'block'
            )}>
              <CardHeader>
                <CardTitle>{symbol.name}</CardTitle>
                <div className="flex flex-wrap gap-2 mt-2">
                  {symbol.keywords.map((keyword) => (
                    <Badge key={keyword} variant="secondary">
                      {keyword}
                    </Badge>
                  ))}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-1">Associations</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    {Object.entries(symbol.associations).map(([key, value]) => (
                      <div key={key} className="flex items-center gap-2">
                        <span className="text-muted-foreground capitalize">{key}:</span>
                        <span>{Array.isArray(value) ? value.join(', ') : value}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <Button
                  className="w-full"
                  onClick={() => setShowDetails(true)}
                >
                  Learn More
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </AnimatePresence>
      </motion.div>

      <Dialog open={showDetails} onOpenChange={setShowDetails}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              {symbol.name}
              <Badge variant="outline">{symbol.category}</Badge>
            </DialogTitle>
            <DialogDescription>
              Explore the deeper meaning and practice with this symbol
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-6">
            <div className="aspect-video relative rounded-lg overflow-hidden">
              <Image
                src={symbol.imageUrl}
                alt={symbol.name}
                fill
                className="object-cover"
              />
            </div>
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Meaning</h4>
                <div className="space-y-2">
                  <p><strong>General:</strong> {symbol.meaning.general}</p>
                  <p><strong>Spiritual:</strong> {symbol.meaning.spiritual}</p>
                  <p><strong>Personal:</strong> {symbol.meaning.personal}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleInteraction('study')}
                >
                  <Star className="w-4 h-4 mr-2" />
                  Study
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleInteraction('meditation')}
                >
                  <Clock className="w-4 h-4 mr-2" />
                  Meditate
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleInteraction('practice')}
                >
                  <Unlock className="w-4 h-4 mr-2" />
                  Practice
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleInteraction('insight')}
                >
                  <Star className="w-4 h-4 mr-2" />
                  Record Insight
                </Button>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}