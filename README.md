# MyDivinations Backend & Web

MyDivinations is an AI-driven divination platform that uses Fractal Resonance Cognition (FRC) to help users discover archetypal patterns and increase consciousness through interactive experiences.

## Project Overview

This repository contains:
1. The backend microservices serving both the Unity application and web frontend
2. The Next.js web application providing a mobile-friendly experience
3. Coordination documents for our multi-agent development team

The system provides:
- Accurate astrological calculations through the Astrology Engine Service
- Archetypal pattern mapping from astrological data
- Fractal visualization parameters for both Unity and web implementations
- Personalized content generation based on user's archetypal profile
- Interactive symbolic journeys through the Path of Symbols experience

## Repository Structure

- `/coordination` - AI agent coordination documents
- `/docs` - Project documentation
- `/services` - Backend microservices
- `/shared` - Shared libraries and utilities
- `/frontend` - Next.js web application
- `/deploy` - Deployment configurations

## For AI Team Members

This project uses a coordinated AI agent approach. If you're an AI agent working on this project:

1. First read `/coordination/HowWeWork.md` to understand the collaboration protocol
2. Check your specific agent handoff document in `/coordination/handoffs/`
3. Review the recent changes in `/coordination/CHANGELOG.md`
4. Review the current project status in `/coordination/STATUS.md`
5. Update these documents at the end of your session

## Team Structure

- **Human CEO (Hadi)**: Vision, archetypal framework, strategy
- **AI CEO**: Strategic coordination, documentation
- **Backend Architect (BEA)**: Microservice architecture, API design, technical specifications
- **Frontend Developer (FD)**: Next.js web application development
- **Game Designer (GD)**: User experience, symbolic journey design, interaction mechanics
- **RIO (Repository Integration Orchestrator)**: GitHub management, CI/CD workflows, collaboration tools
- **Cursor AI**: Implementation support, code generation, development assistance
- **Unity Developer (Essi)**: Technical implementation for Unity frontend (separate repository)

## Components

### Backend Microservices

| Service | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [`astrology-engine`](./services/astrology-engine/) | Astrological calculations and chart generation | Python 3.9, FastAPI 0.109.1, Redis 7.2 | Initial Setup Complete |
| `archetypal-mapping` | Mapping astrological data to archetypal patterns | Node.js, Express | Planned |
| `fractal-visualization` | Generating fractal parameters for visualizations | Python, Flask | Planned |
| `content-generation` | Creating personalized guidance and content | Node.js, Express | Planned |
| `audio-generation` | Creating consciousness-aligned audio | Python, Flask | Planned |
| `api-gateway` | Unified API access point | Node.js, Express | Planned |

#### Astrology Engine Service Status
- ✅ Basic FastAPI application setup
- ✅ Health check endpoint (`/health`)
- ✅ Welcome endpoint (`/`)
- ✅ Docker containerization
- ✅ Redis integration
- ✅ Basic project structure
- ✅ Initial documentation
- 🔄 Swiss Ephemeris integration (Planned)
- 🔄 Birth chart calculations (Planned)
- 🔄 Planetary positions (Planned)
- 🔄 Aspects calculations (Planned)
- 🔄 Transits and progressions (Planned)

### Web Application

| Component | Description | Tech Stack | Status |
|-----------|-------------|------------|--------|
| `next-app` | Core web application structure | Next.js 14, React, TypeScript | ✅ Complete |
| `auth` | Authentication system | Next-Auth, Zustand | ✅ Complete |
| `path-of-symbols` | Web-based symbolic journey | React, Framer Motion | ✅ Complete |
| `transit-analysis` | Transit visualization and analysis | D3.js, React | ✅ Complete |
| `birth-chart` | Birth chart calculation and display | React, SVG | ✅ Complete |
| `user-profile` | User profile and settings | React, Tailwind | ✅ Complete |
| `pwa-features` | Progressive Web App capabilities | Next.js, Service Workers | 🔄 In Progress |

#### Frontend Implementation Status
- ✅ Project setup with Next.js 14, TypeScript, and Tailwind CSS
- ✅ Authentication system with Next-Auth
- ✅ Global state management with Zustand
- ✅ API service layer with Axios
- ✅ Utility functions and helpers
- ✅ Global styles and theme system
- ✅ Base components (Layout, Navigation, Footer)
- ✅ Path of Symbols journey interface
- ✅ Symbol Grid and Symbol Card components
- ✅ Transit Analysis page with timeline visualization
- ✅ Birth Chart form and visualization
- ✅ User profile and settings pages
- ✅ Responsive design and mobile optimization
- 🔄 Progressive Web App features (In Progress)
- 🔄 End-to-end testing (Planned)
- 🔄 Performance optimization (Planned)

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for Node.js services and web application)
- Python 3.9+ (for Python services)
- Supabase CLI (for local database)

### Backend Setup
1. Clone this repository
2. Copy `.env.example` to `.env` and configure environment variables
3. Run `docker-compose up` to start the development environment
4. See service-specific READMEs for further instructions

### Web Application Setup
1. Navigate to `/frontend` directory
2. Copy `.env.example` to `.env.local` and configure environment variables
3. Run `npm install` to install dependencies
4. Run `npm run dev` to start the development server
5. Access the application at `http://localhost:3000`

## Development Process

- Each component follows a documented specification
- Services and applications are containerized for consistent development and deployment
- Integration happens through well-defined API contracts
- Changes are coordinated through our AI agent protocol
- Both web and Unity applications consume the same backend APIs

## Current Focus

- ✅ Initial Astrology Engine Service setup complete
- ✅ Frontend base implementation complete
- ✅ Path of Symbols experience implemented
- ✅ Transit Analysis features implemented
- 🔄 Implementing Swiss Ephemeris integration
- 🔄 Developing birth chart calculation endpoints
- 🔄 Adding Progressive Web App features
- 🔄 Implementing end-to-end testing

## License

This project is proprietary and confidential.

*Last updated: March 16, 2025 | 07:30 UTC*  
*AI CEO*