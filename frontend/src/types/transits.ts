export interface Transit {
  id: string;
  transitingPlanet: {
    name: string;
    symbol: string;
    sign: string;
    degree: number;
    speed: number; // Positive for direct motion, negative for retrograde
    isRetrograde: boolean;
  };
  natalPlanet: {
    name: string;
    symbol: string;
    sign: string;
    degree: number;
    house: number;
  };
  aspect: {
    type: AspectType;
    orb: number;
    isApplying: boolean;
    exactDate?: Date;
  };
  influence: {
    strength: number; // 1-10
    nature: 'harmonious' | 'challenging' | 'neutral';
    duration: {
      start: Date;
      peak: Date;
      end: Date;
    };
  };
  interpretation: {
    general: string;
    opportunities: string[];
    challenges: string[];
    advice: string[];
  };
}

export type AspectType = 
  | 'conjunction'
  | 'opposition'
  | 'trine'
  | 'square'
  | 'sextile'
  | 'quincunx'
  | 'semisextile'
  | 'semisquare'
  | 'sesquisquare';

export interface TransitPeriod {
  id: string;
  userId: string;
  startDate: Date;
  endDate: Date;
  transits: Transit[];
  summary: {
    majorThemes: string[];
    significantDates: Array<{
      date: Date;
      description: string;
      importance: number; // 1-10
    }>;
    overallNature: 'harmonious' | 'challenging' | 'mixed' | 'neutral';
  };
  houses: Array<{
    number: number;
    activity: number; // 1-10
    transits: string[]; // Transit IDs
  }>;
}

export interface TransitSettings {
  aspectOrbs: {
    [key in AspectType]: {
      max: number;
      applying: number;
      separating: number;
    };
  };
  includedPlanets: string[];
  includedAspects: AspectType[];
  notifications: {
    enabled: boolean;
    threshold: number; // Minimum influence strength for notification
    types: Array<'exact' | 'applying' | 'separating'>;
  };
}

export interface TransitAlert {
  id: string;
  userId: string;
  transitId: string;
  type: 'exact' | 'applying' | 'separating';
  date: Date;
  message: string;
  isRead: boolean;
  importance: number; // 1-10
}