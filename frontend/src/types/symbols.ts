export interface Symbol {
  id: string;
  name: string;
  description: string;
  category: SymbolCategory;
  imageUrl: string;
  keywords: string[];
  meaning: {
    general: string;
    spiritual: string;
    personal: string;
  };
  associations: {
    element?: string;
    planet?: string;
    zodiacSign?: string;
    number?: number;
    color?: string[];
  };
  unlocked: boolean;
  progress: number;
}

export type SymbolCategory = 
  | 'zodiac'
  | 'planet'
  | 'house'
  | 'aspect'
  | 'node'
  | 'element'
  | 'fixed_star';

export interface SymbolJourney {
  id: string;
  userId: string;
  currentLevel: number;
  totalSymbols: number;
  unlockedSymbols: number;
  lastUnlock: Date;
  dailyStreak: number;
  symbols: Symbol[];
  achievements: Achievement[];
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  imageUrl: string;
  unlockedAt?: Date;
  progress: number;
  requiredProgress: number;
  reward?: {
    type: 'symbol' | 'feature' | 'insight';
    value: string;
  };
}

export interface SymbolInteraction {
  id: string;
  userId: string;
  symbolId: string;
  type: 'study' | 'meditation' | 'practice' | 'insight';
  timestamp: Date;
  duration: number;
  notes?: string;
  progress: number;
}

export interface DailySymbol {
  symbol: Symbol;
  date: Date;
  message: string;
  affirmation: string;
  challenge?: {
    description: string;
    reward: number;
  };
}