# MyDivinations API Integration Strategy

This document outlines the approach for integrating the MyDivinations web application with backend services, focusing on data models, API client architecture, error handling, and caching strategies.

## API Services Overview

The MyDivinations frontend will need to integrate with the following services:

1. **Astrology Engine Service**
   - Calculate natal charts and transits
   - Generate planetary positions and aspects
   - Provide astrological data for visualization

2. **Archetypal Mapping Service** (Planned)
   - Map astrological data to archetypal patterns
   - Generate archetypal profiles
   - Provide symbolic associations

3. **Content Generation Service** (Planned)
   - Create personalized guidance content
   - Generate insights based on archetypal profiles
   - Provide journey narratives

4. **User Management** (Through Auth.js)
   - Authentication and session management
   - User profile data storage and retrieval
   - Preferences and settings

## API Client Architecture

We'll implement a structured API client using Axios and React Query:

### Core API Client Structure

```typescript
// lib/api/client.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { getSession } from 'next-auth/react';

// Create API client instance
const createApiClient = (): AxiosInstance => {
  const client = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request interceptor
  client.interceptors.request.use(
    async (config) => {
      // Get session for authentication
      const session = await getSession();
      
      // Add auth header if session exists
      if (session?.accessToken) {
        config.headers.Authorization = `Bearer ${session.accessToken}`;
      }
      
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor
  client.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error: AxiosError) => {
      const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
      
      // Handle 401 authentication errors (token expired)
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        
        try {
          // Refresh token logic here
          // ...
          
          // Retry the original request
          return client(originalRequest);
        } catch (refreshError) {
          // Handle refresh failure (redirect to login)
          return Promise.reject(refreshError);
        }
      }
      
      return Promise.reject(error);
    }
  );

  return client;
};

export const apiClient = createApiClient();
```

### Service-Specific API Modules

Each backend service will have its own dedicated API module:

```typescript
// lib/api/astrologyEngine.ts
import { apiClient } from './client';
import { BirthData, NatalChart, Transit } from '@/types/astrology';

export const astrologyEngineApi = {
  // Calculate natal chart
  calculateNatalChart: async (birthData: BirthData): Promise<NatalChart> => {
    const response = await apiClient.post<NatalChart>('/astrology/natal-chart', birthData);
    return response.data;
  },
  
  // Get current transits
  getCurrentTransits: async (natalChartId: string): Promise<Transit[]> => {
    const response = await apiClient.get<Transit[]>(`/astrology/transits/${natalChartId}`);
    return response.data;
  },
  
  // Get planetary positions
  getPlanetaryPositions: async (date: string): Promise<any> => {
    const response = await apiClient.get('/astrology/planetary-positions', {
      params: { date }
    });
    return response.data;
  }
};
```

### React Query Integration

We'll use React Query to handle data fetching, caching, and synchronization:

```typescript
// hooks/useAstrology.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { astrologyEngineApi } from '@/lib/api/astrologyEngine';
import { BirthData, NatalChart } from '@/types/astrology';

// Hook for calculating natal chart
export function useNatalChart(birthData: BirthData) {
  return useQuery({
    queryKey: ['natalChart', birthData],
    queryFn: () => astrologyEngineApi.calculateNatalChart(birthData),
    enabled: !!birthData.date && !!birthData.time && !!birthData.location,
    staleTime: Infinity, // Natal chart doesn't change, so cache forever
  });
}

// Hook for current transits (changes regularly)
export function useCurrentTransits(natalChartId: string) {
  return useQuery({
    queryKey: ['transits', natalChartId],
    queryFn: () => astrologyEngineApi.getCurrentTransits(natalChartId),
    enabled: !!natalChartId,
    staleTime: 60 * 60 * 1000, // Stale after 1 hour
    refetchInterval: 24 * 60 * 60 * 1000, // Refetch every 24 hours
  });
}

// Hook for adding birth data
export function useAddBirthData() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (birthData: BirthData) => astrologyEngineApi.calculateNatalChart(birthData),
    onSuccess: (data) => {
      queryClient.setQueryData(['natalChart', data.birthData], data);
      queryClient.invalidateQueries({ queryKey: ['userProfile'] });
    },
  });
}
```

## Data Models

We'll define TypeScript interfaces for all API data models. Here are key examples:

### Astrology Models

```typescript
// types/astrology.ts
export interface Coordinates {
  latitude: number;
  longitude: number;
}

export interface BirthData {
  date: string; // ISO format
  time: string | null; // ISO format or null if unknown
  location: {
    name: string;
    coordinates: Coordinates;
  };
  timezoneOffset: number; // in minutes
}

export interface Planet {
  id: string;
  name: string;
  sign: string;
  degree: number;
  retrograde: boolean;
  house: number;
}

export interface House {
  id: number;
  sign: string;
  degree: number;
}

export interface Aspect {
  planet1: string;
  planet2: string;
  type: string;
  orb: number;
  influence: number; // -10 to 10 scale
}

export interface NatalChart {
  id: string;
  birthData: BirthData;
  planets: Planet[];
  houses: House[];
  aspects: Aspect[];
  ascendant: {
    sign: string;
    degree: number;
  };
  midheaven: {
    sign: string;
    degree: number;
  };
  createdAt: string;
}

export interface Transit {
  transitingPlanet: Planet;
  natalPosition: Planet;
  aspect: string;
  orb: number;
  startDate: string;
  peakDate: string;
  endDate: string;
  influence: number; // -10 to 10 scale
}
```

### Archetypal Models

```typescript
// types/archetypal.ts
export interface Archetype {
  id: string;
  name: string;
  description: string;
  influence: number; // 0-100
  symbols: string[];
  elements: string[];
  qualities: string[];
}

export interface ArchetypalProfile {
  id: string;
  userId: string;
  natalChartId: string;
  primaryArchetypes: Archetype[];
  secondaryArchetypes: Archetype[];
  currentInfluences: {
    archetype: string;
    transitingPlanet: string;
    influence: number;
    startDate: string;
    endDate: string;
  }[];
  createdAt: string;
  updatedAt: string;
}
```

### Journey Models

```typescript
// types/journey.ts
export interface Symbol {
  id: string;
  name: string;
  description: string;
  archetype: string;
  visualUrl: string;
}

export interface DecisionPoint {
  id: string;
  description: string;
  options: {
    id: string;
    text: string;
    symbol: Symbol;
    nextPointId: string | null;
  }[];
}

export interface Journey {
  id: string;
  userId: string;
  entryPoint: DecisionPoint;
  currentPoint: DecisionPoint;
  path: {
    pointId: string;
    selectedOptionId: string;
    timestamp: string;
  }[];
  status: 'active' | 'completed' | 'abandoned';
  startedAt: string;
  completedAt: string | null;
  fractalParameters: Record<string, any>; // Parameters for fractal visualization
}
```

## Error Handling Strategy

We'll implement a comprehensive error handling strategy:

### Error Types

```typescript
// types/errors.ts
export enum ErrorType {
  NETWORK = 'network',
  AUTHENTICATION = 'authentication',
  VALIDATION = 'validation',
  SERVER = 'server',
  NOT_FOUND = 'notFound',
  TIMEOUT = 'timeout',
  UNKNOWN = 'unknown',
}

export interface ApiError {
  type: ErrorType;
  status?: number;
  message: string;
  details?: Record<string, any>;
  originalError?: any;
}
```

### Error Handling Utilities

```typescript
// lib/api/errorHandling.ts
import { AxiosError } from 'axios';
import { ApiError, ErrorType } from '@/types/errors';

export const handleApiError = (error: unknown): ApiError => {
  // Handle Axios errors
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<any>;
    
    // Network errors
    if (!axiosError.response) {
      return {
        type: ErrorType.NETWORK,
        message: 'Unable to connect to the server. Please check your internet connection.',
        originalError: error,
      };
    }
    
    // Server errors with response
    const status = axiosError.response.status;
    const data = axiosError.response.data;
    
    switch (status) {
      case 401:
        return {
          type: ErrorType.AUTHENTICATION,
          status,
          message: 'Authentication required. Please log in again.',
          details: data,
          originalError: error,
        };
      case 403:
        return {
          type: ErrorType.AUTHENTICATION,
          status,
          message: 'You don\'t have permission to access this resource.',
          details: data,
          originalError: error,
        };
      case 404:
        return {
          type: ErrorType.NOT_FOUND,
          status,
          message: 'The requested resource was not found.',
          details: data,
          originalError: error,
        };
      case 422:
        return {
          type: ErrorType.VALIDATION,
          status,
          message: 'There was a problem with the submitted data.',
          details: data,
          originalError: error,
        };
      case 500:
      case 502:
      case 503:
      case 504:
        return {
          type: ErrorType.SERVER,
          status,
          message: 'The server encountered an error. Please try again later.',
          details: data,
          originalError: error,
        };
      default:
        return {
          type: ErrorType.UNKNOWN,
          status,
          message: 'An unexpected error occurred.',
          details: data,
          originalError: error,
        };
    }
  }
  
  // Handle non-Axios errors
  return {
    type: ErrorType.UNKNOWN,
    message: error instanceof Error ? error.message : 'An unknown error occurred',
    originalError: error,
  };
};
```

### Error Boundaries

We'll implement React Error Boundaries for UI error handling:

```typescript
// components/common/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  fallback?: ReactNode;
  children: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log error to monitoring service
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    // Call onError prop if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-boundary-fallback">
          <h2>Something went wrong</h2>
          <p>Please try refreshing the page or contact support if the issue persists.</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

## Caching Strategy

We'll implement a multi-tiered caching strategy using React Query:

### Caching Configuration

```typescript
// lib/react-query/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 24 * 60 * 60 * 1000, // 24 hours
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
    mutations: {
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});
```

### Resource-Specific Cache Configurations

Different resources will have different caching needs:

- **Static Data** (natal charts, birth data)
  - `staleTime: Infinity` - Data doesn't change
  - `cacheTime: Infinity` - Keep in cache indefinitely

- **Semi-Dynamic Data** (archetypal profiles)
  - `staleTime: 24 * 60 * 60 * 1000` - Consider fresh for 24 hours
  - `cacheTime: 7 * 24 * 60 * 60 * 1000` - Keep in cache for 7 days

- **Dynamic Data** (current transits, daily insights)
  - `staleTime: 60 * 60 * 1000` - Consider fresh for 1 hour
  - `refetchInterval: 24 * 60 * 60 * 1000` - Background refresh daily
  - `cacheTime: 24 * 60 * 60 * 1000` - Keep in cache for 24 hours

### Offline Support

For offline support, we'll:

1. Implement persistence with `createWebStoragePersister`
2. Store critical data in IndexedDB
3. Implement optimistic updates for mutations

```typescript
// lib/react-query/persistedQueryClient.ts
import { QueryClient } from '@tanstack/react-query';
import { createWebStoragePersister } from '@tanstack/query-persist-client-core';
import { persistQueryClient } from '@tanstack/react-query-persist-client';

import { queryClient } from './queryClient';

// Create a client-side persister
const persister = createWebStoragePersister({
  storage: window.localStorage,
});

// Set up persistence
persistQueryClient({
  queryClient,
  persister,
  maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
  buster: process.env.NEXT_PUBLIC_APP_VERSION,
  dehydrateOptions: {
    shouldDehydrateQuery: (query) => {
      // Only persist queries that we want available offline
      return query.queryKey[0] === 'natalChart' || 
        query.queryKey[0] === 'archetypalProfile' ||
        query.queryKey[0] === 'userProfile';
    },
  },
});
```

## Mock API Implementation

For development ahead of backend availability, we'll implement mock API handlers:

```typescript
// lib/mock-api/handlers.ts
import { rest } from 'msw';
import { natalChartData, transitsData } from './mockData';

export const handlers = [
  // Get natal chart
  rest.post('/api/astrology/natal-chart', (req, res, ctx) => {
    // Extract birth data from request
    const birthData = req.body;
    
    // Generate a deterministic ID based on birth data
    const id = generateMockId(birthData);
    
    // Return mock natal chart
    return res(
      ctx.delay(1500), // Simulate network delay
      ctx.status(200),
      ctx.json({
        id,
        birthData,
        ...natalChartData[id % natalChartData.length],
        createdAt: new Date().toISOString(),
      })
    );
  }),
  
  // Get current transits
  rest.get('/api/astrology/transits/:natalChartId', (req, res, ctx) => {
    const { natalChartId } = req.params;
    
    // Return mock transits
    return res(
      ctx.delay(800),
      ctx.status(200),
      ctx.json(transitsData)
    );
  }),
  
  // More mock endpoints...
];
```

### Mock Data Setup

```typescript
// lib/mock-api/mockData.ts
import { NatalChart, Transit } from '@/types/astrology';

export const natalChartData: Partial<NatalChart>[] = [
  {
    planets: [
      {
        id: 'sun',
        name: 'Sun',
        sign: 'Aries',
        degree: 15.5,
        retrograde: false,
        house: 10,
      },
      // More planets...
    ],
    houses: [
      {
        id: 1,
        sign: 'Cancer',
        degree: 25.5,
      },
      // More houses...
    ],
    aspects: [
      {
        planet1: 'sun',
        planet2: 'moon',
        type: 'conjunction',
        orb: 2.5,
        influence: 8,
      },
      // More aspects...
    ],
    ascendant: {
      sign: 'Cancer',
      degree: 25.5,
    },
    midheaven: {
      sign: 'Aries',
      degree: 15.5,
    },
  },
  // More mock charts...
];

export const transitsData: Transit[] = [
  {
    transitingPlanet: {
      id: 'jupiter',
      name: 'Jupiter',
      sign: 'Taurus',
      degree: 12.5,
      retrograde: false,
      house: 11,
    },
    natalPosition: {
      id: 'sun',
      name: 'Sun',
      sign: 'Aries',
      degree: 15.5,
      retrograde: false,
      house: 10,
    },
    aspect: 'trine',
    orb: 1.2,
    startDate: '2025-03-10T00:00:00Z',
    peakDate: '2025-03-20T00:00:00Z',
    endDate: '2025-03-30T00:00:00Z',
    influence: 7,
  },
  // More transits...
];
```

### Integrating Mock API

```typescript
// lib/mock-api/index.ts
import { setupWorker } from 'msw';
import { handlers } from './handlers';

// Conditionally setup the mock service worker
export const setupMockApi = () => {
  if (process.env.NEXT_PUBLIC_API_MOCKING === 'enabled') {
    if (typeof window === 'undefined') {
      console.warn('MSW cannot be initialized on the server side');
      return;
    }
    
    const worker = setupWorker(...handlers);
    
    worker.start({
      onUnhandledRequest: 'bypass', // Don't warn about unhandled requests
    });
    
    console.info('Mock API enabled');
    
    return worker;
  }
  
  return null;
};
```

## Next Steps and Implementation Plan

1. **Immediate Tasks (By March 19)**
   - Set up core API client structure
   - Create TypeScript interfaces for main data models
   - Implement error handling utilities
   - Configure React Query for data fetching

2. **Short-Term Tasks (By March 22)**
   - Create mock API handlers for Astrology Engine
   - Implement API hooks for birth data and natal charts
   - Set up caching strategy for core resources
   - Create error boundary components

3. **Medium-Term Tasks (By March 25)**
   - Integrate authentication with Auth.js
   - Implement offline support with persistence
   - Create loading and error states for API interactions
   - Document API client usage for the team

4. **Dependencies**
   - API contracts from Backend Architect
   - Authentication strategy alignment
   - Feedback on data model structures

---

*Last Updated: March 16, 2025 | 21:45 PST*  
*MyDiv FD*