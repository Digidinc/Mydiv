# MyDivinations Frontend

The web frontend for MyDivinations, built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

### Authentication
- Next-Auth integration with multiple providers
- Protected routes and middleware
- Persistent session management
- Password reset and email verification

### Path of Symbols
- Interactive symbol exploration interface
- Symbol Grid with search and filtering
- Symbol Cards with flip animation
- Progress tracking and achievements
- Daily symbol challenges

### Transit Analysis
- Interactive transit timeline visualization
- Detailed transit information cards
- House and planet activity tracking
- Customizable settings for transit analysis
- Real-time transit alerts and notifications

### Birth Chart
- Birth data input form with validation
- Interactive chart visualization
- Aspect grid and planet positions
- Detailed interpretations
- Chart saving and sharing

### User Profile
- Personal information management
- Preferences and settings
- Progress tracking
- Saved charts and analyses
- Notification settings

## Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **API Client**: Axios
- **Animations**: Framer Motion
- **Data Visualization**: D3.js
- **UI Components**: shadcn/ui
- **Form Handling**: React Hook Form
- **Validation**: Zod
- **Testing**: Jest, React Testing Library (planned)

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js app router pages
│   ├── components/          # React components
│   │   ├── auth/           # Authentication components
│   │   ├── birth-chart/    # Birth chart components
│   │   ├── symbols/        # Symbol-related components
│   │   ├── transits/       # Transit analysis components
│   │   └── ui/             # Shared UI components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utility functions
│   ├── services/           # API services
│   ├── store/              # Zustand store
│   ├── styles/             # Global styles
│   └── types/              # TypeScript types
├── public/                 # Static assets
└── tests/                 # Test files (planned)
```

## Components

### Base Components
- `RootLayout`: Main layout with navigation and theme
- `Navigation`: Responsive navigation bar
- `Footer`: Site footer with links and info
- `ThemeProvider`: Dark/light theme management
- `UserNav`: User-specific navigation

### Symbol Components
- `SymbolGrid`: Display and filter symbols
- `SymbolCard`: Individual symbol display
- `SymbolDetails`: Detailed symbol information
- `SymbolProgress`: Progress tracking

### Transit Components
- `TransitTimeline`: Visual transit display
- `TransitDetail`: Transit information card
- `HouseActivity`: House analysis display
- `PlanetStatus`: Planet position tracking

### Birth Chart Components
- `BirthChartForm`: Data input form
- `ChartVisualization`: SVG chart display
- `AspectGrid`: Aspect relationship grid
- `PlanetPositions`: Planet location display

## Getting Started

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Copy environment variables:
   ```bash
   cp .env.example .env.local
   ```
5. Start the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-key
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000
```

## Scripts

- `npm run dev`: Start development server
- `npm run build`: Build production version
- `npm run start`: Start production server
- `npm run lint`: Run ESLint
- `npm run test`: Run tests (planned)
- `npm run type-check`: Check TypeScript types

## Development Guidelines

1. **Component Structure**
   - Use functional components with TypeScript
   - Implement proper prop typing
   - Include JSDoc comments for complex components

2. **State Management**
   - Use Zustand for global state
   - Implement proper state persistence
   - Follow atomic state updates

3. **Styling**
   - Use Tailwind CSS utilities
   - Follow design system tokens
   - Implement responsive design

4. **Testing (Planned)**
   - Write unit tests for components
   - Include integration tests
   - Maintain good test coverage

## Current Status

### Completed
- ✅ Project setup and configuration
- ✅ Authentication system
- ✅ Base components and layout
- ✅ Path of Symbols implementation
- ✅ Transit Analysis features
- ✅ Birth Chart functionality
- ✅ User Profile management
- ✅ Global state management
- ✅ API integration
- ✅ Theme system
- ✅ Responsive design

### In Progress
- 🔄 Progressive Web App features
- 🔄 Performance optimization
- 🔄 Accessibility improvements

### Planned
- 📅 End-to-end testing setup
- 📅 CI/CD pipeline
- 📅 Analytics integration
- 📅 Error tracking
- 📅 Documentation website

## Contributing

1. Create a feature branch
2. Implement changes
3. Write/update tests
4. Submit pull request
5. Wait for review

## License

This project is proprietary and confidential.

*Last updated: March 16, 2025 | 07:30 UTC*