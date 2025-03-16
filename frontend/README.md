# MyDivinations Frontend

This is the web frontend for MyDivinations, built with Next.js 14 and modern web technologies.

## Tech Stack

- **Framework:** Next.js 14 (React)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui
- **State Management:** 
  - React Query (Server State)
  - Zustand (Client State)
- **HTTP Client:** Axios
- **Testing:** Jest + React Testing Library
- **E2E Testing:** Cypress
- **Code Quality:**
  - ESLint
  - Prettier
  - Husky
  - lint-staged

## Project Structure

```
frontend/
├── src/
│   ├── app/             # Next.js app router pages
│   ├── components/      # Reusable UI components
│   │   ├── ui/         # Base UI components
│   │   └── shared/     # Shared components
│   ├── features/        # Feature-specific components
│   │   ├── auth/       # Authentication
│   │   ├── charts/     # Birth charts
│   │   └── profile/    # User profile
│   ├── hooks/          # Custom React hooks
│   ├── lib/            # Utilities and configurations
│   ├── services/       # API service layer
│   └── types/          # TypeScript definitions
├── public/             # Static assets
└── tests/              # Test files
```

## Getting Started

1. **Prerequisites**
   - Node.js 18+
   - npm or yarn
   - Git

2. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/Digidinc/Mydiv
   cd Mydiv/frontend

   # Install dependencies
   npm install
   # or
   yarn install
   ```

3. **Environment Setup**
   ```bash
   # Copy example env file
   cp .env.example .env.local

   # Update environment variables
   ```

4. **Development**
   ```bash
   # Start development server
   npm run dev
   # or
   yarn dev
   ```

5. **Build**
   ```bash
   # Create production build
   npm run build
   # or
   yarn build
   ```

## Development Guidelines

1. **Code Style**
   - Follow the ESLint configuration
   - Run Prettier before committing
   - Use TypeScript strictly

2. **Components**
   - Create reusable components in `/components`
   - Feature-specific components go in `/features`
   - Use shadcn/ui components when possible

3. **State Management**
   - Use React Query for API data
   - Use Zustand for global UI state
   - Prefer local state when possible

4. **Testing**
   - Write unit tests for utilities
   - Write integration tests for components
   - Add E2E tests for critical flows

## Available Scripts

- `dev`: Start development server
- `build`: Create production build
- `start`: Start production server
- `test`: Run Jest tests
- `test:e2e`: Run Cypress tests
- `lint`: Run ESLint
- `format`: Run Prettier
- `type-check`: Run TypeScript compiler

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Create a pull request
5. Wait for review

## License

This project is proprietary and confidential.

---

*Last updated: March 16, 2025*