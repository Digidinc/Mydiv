# MyDivinations Web Application Architecture

This document outlines the architecture for the MyDivinations web application, detailing the technology stack, component structure, state management approach, and other implementation considerations.

## Technology Stack

### Core Technologies
- **Framework**: Next.js 13+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Auth.js (formerly NextAuth.js)
- **State Management**: React Context API + Zustand
- **API Client**: Axios with React Query
- **Visualization**: 
  - Data visualization: D3.js
  - Fractal generation: Three.js
- **Animation**: Framer Motion
- **Forms**: React Hook Form with Zod validation
- **Testing**: Jest, React Testing Library
- **Deployment**: Vercel

## Directory Structure

```
/app                             # Next.js App Router structure
  /api                           # API routes
  /(auth)                        # Authentication routes & components
    /login/page.tsx              # Login page
    /signup/page.tsx             # Signup page
  /(profile)                     # User profile routes & components
    /page.tsx                    # Profile page
    /edit/page.tsx               # Edit profile page
  /(journey)                     # Path of Symbols journey
    /page.tsx                    # Journey entry point
    /[id]/page.tsx               # Specific journey page
  /layout.tsx                    # Root layout
  /page.tsx                      # Home page

/components                      # Reusable components
  /common                        # Common UI components
    /Button.tsx
    /Card.tsx
    /Input.tsx
  /layout                        # Layout components
    /Header.tsx
    /Footer.tsx
    /Navigation.tsx
  /journey                       # Journey-specific components
    /SymbolSelector.tsx
    /JourneyProgress.tsx
    /DecisionPoint.tsx
  /visualization                 # Visualization components
    /FractalRenderer.tsx
    /ArchetypalChart.tsx
  /forms                         # Form components
    /BirthDataForm.tsx
    /ProfileForm.tsx

/lib                             # Utility libraries
  /api                           # API client setup
  /auth                          # Authentication utilities
  /hooks                         # Custom hooks
  /utils                         # Utility functions
  /constants                     # Constants and configuration

/store                           # State management
  /userStore.ts                  # User-related state
  /journeyStore.ts               # Journey-related state
  /settingsStore.ts              # Application settings

/types                           # TypeScript type definitions
  /api.ts                        # API response types
  /models.ts                     # Domain model types
  /store.ts                      # State store types

/styles                          # Global styles
  /globals.css                   # Global CSS and Tailwind imports

/public                          # Static assets
  /images                        # Images
  /icons                         # Icons
  /fonts                         # Fonts
```

## Component Architecture

The component architecture follows a hierarchical structure with clear separation of concerns:

### Component Types

1. **Page Components**
   - Correspond to routes in the application
   - Handle data fetching with React Query
   - Manage page-level state
   - Coordinate layout and component composition

2. **Layout Components**
   - Handle page structure and shared UI elements
   - Manage navigation and transitions
   - Provide consistent user experience across pages

3. **Feature Components**
   - Implement specific feature requirements
   - Combine multiple UI components
   - Handle feature-specific business logic
   - Often have internal state

4. **UI Components**
   - Basic, reusable UI elements
   - Stateless whenever possible
   - Follow design system guidelines
   - Accept props for customization

5. **Visualization Components**
   - Handle rendering of fractal patterns
   - Implement interactive data visualizations
   - Optimize for performance
   - Responsive across device sizes

### Component Design Principles

- **Single Responsibility**: Each component should have one clear purpose
- **Composition Over Inheritance**: Favor component composition for reuse
- **Prop Drilling Avoidance**: Use React Context or Zustand for shared state
- **Consistent Props API**: Follow consistent patterns for component props
- **Performance Awareness**: Memoize expensive computations and renders
- **Accessibility First**: Ensure all components meet accessibility guidelines

## State Management

We'll use a hybrid approach to state management:

### React Context API
- Used for global UI state, theme settings, and authentication state
- Context providers wrapped around the application in appropriate layers
- Used when state needs to be accessed by many components across the tree

### Zustand
- Used for more complex global state management
- Particularly for journey-related state, user profile, and application settings
- Benefits from immutable updates and middleware support
- Provides better performance than Context for frequent updates

### Local Component State
- Used for component-specific state that doesn't need to be shared
- Managed with useState or useReducer depending on complexity

### State Architecture Diagram

```
┌─────────────────────────────────────────┐
│ App-wide State (React Context)          │
│ - Authentication Status                 │
│ - Theme/Preferences                     │
│ - Global UI State (modals, alerts)      │
└─────────────────────────────────────────┘
            ┌───────────────┐
            │ Zustand Stores │
            └───────────────┘
                   │
     ┌─────────────┼─────────────┐
     │             │             │
┌────▼────┐   ┌────▼────┐   ┌────▼────┐
│ User    │   │ Journey  │   │ Settings │
│ Store   │   │ Store    │   │ Store    │
└────┬────┘   └────┬─────┘   └────┬────┘
     │             │              │
     └─────────────┼──────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ Component Local State                    │
│ - Form input values                      │
│ - UI control state                       │
│ - Ephemeral visual state                 │
└─────────────────────────────────────────┘
```

## API Integration

The application will communicate with backend services using the following approach:

### API Client Configuration
- Axios instance with base configuration
- Request/response interceptors for:
  - Authentication headers
  - Error handling
  - Response transformation

### React Query Integration
- Data fetching with React Query for:
  - Caching
  - Background refetching
  - Optimistic updates
  - Mutation handling

### API Modules
- Organized by domain (user, astrology, journey, etc.)
- Each endpoint wrapped in a custom hook
- Proper typing of request/response objects

### Mock API Services
- For development ahead of backend availability
- Consistent with API contracts
- Simulates realistic response timing and errors

## Authentication Strategy

We'll implement authentication using Auth.js (formerly NextAuth.js):

### Authentication Methods
- Email/Password authentication
- Magic link authentication (passwordless)
- OAuth providers (Google, Apple) for social login

### Session Management
- JWT-based sessions stored in HTTP-only cookies
- Automatic token rotation for security
- Session expiration and renewal handling

### Protected Routes
- Route protection using middleware
- Redirect to login for unauthenticated users
- Role-based access control where necessary

### User Profile Integration
- Linking authentication with user profile data
- Secure storage of user preferences
- Birth data management and validation

## Progressive Web App (PWA) Implementation

To enable offline functionality and enhance mobile experience:

### Service Worker
- Caching strategies for different asset types
- Offline fallback pages
- Background sync for data submission

### Manifest Configuration
- App installation capabilities
- Custom icons and splash screens
- Theme color and display mode

### Offline First Approach
- Local storage for user preferences
- IndexedDB for journey data
- Synchronization on reconnection

## Performance Optimization

Performance is critical for mobile users:

### Code Splitting
- Route-based code splitting with Next.js
- Dynamic imports for large components
- Load non-critical components lazily

### Asset Optimization
- Image optimization with Next.js Image component
- Font loading optimization with `next/font`
- SVG optimization and sprite usage

### Rendering Strategies
- Static Generation for static content
- Incremental Static Regeneration for semi-dynamic content
- Server Components for dynamic database-dependent pages
- Client Components only where interactivity is required

### Performance Monitoring
- Core Web Vitals tracking
- Performance budgets
- Lighthouse CI integration

## Responsive Design Strategy

The application will follow a mobile-first approach:

### Breakpoint System
- Mobile: 0-639px (default)
- Tablet: 640px-1023px
- Desktop: 1024px+

### Responsive Patterns
- Fluid typography with clamp()
- Grid-based layouts with appropriate responsive changes
- Component adaptation based on screen size
- Touch-friendly UI on mobile devices

### Device-specific Optimizations
- Touch input handling for mobile
- Hover states for desktop
- Keyboard navigation support

## Accessibility Implementation

We'll ensure the application is accessible to all users:

### WCAG Compliance
- Target WCAG 2.1 Level AA compliance
- Regular accessibility audits
- Keyboard navigation testing

### Screen Reader Support
- Proper ARIA attributes
- Semantic HTML structure
- Focus management for dynamic content

### Visual Accessibility
- Sufficient color contrast
- Text scaling support
- Reduced motion option for animations

## Development Workflow

### Component Development Process
1. Define component requirements and API
2. Create component with basic functionality
3. Implement styling and responsive behavior
4. Add interactions and animations
5. Write tests and documentation
6. Review and iterate

### Testing Strategy
- Unit tests for utility functions and hooks
- Component tests with React Testing Library
- End-to-end tests for critical user flows
- Snapshot testing for UI regression

### Documentation
- Component API documentation with JSDoc
- Usage examples
- Performance considerations
- Accessibility notes

---

*Last Updated: March 16, 2025 | 21:25 PST*  
*MyDiv FD*