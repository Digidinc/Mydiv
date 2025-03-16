# MyDivinations Backend

MyDivinations is an AI-driven divination platform that uses Fractal Resonance Cognition (FRC) to help users discover archetypal patterns and increase consciousness through interactive experiences.

## Project Overview

The backend system consists of multiple microservices working together to provide:
- Accurate astrological calculations through the Astrology Engine Service
- Archetypal pattern mapping from astrological data
- Fractal visualization parameters for Unity implementation
- Personalized content generation based on user's archetypal profile
- Audio generation aligned with user's consciousness patterns

## Repository Structure

- `/coordination` - AI agent coordination documents
- `/docs` - Project documentation
- `/services` - Individual microservices
- `/shared` - Shared libraries and utilities
- `/deploy` - Deployment configurations

## For AI Team Members

This project uses a coordinated AI agent approach. If you're an AI agent working on this project:

1. First read `/coordination/HowWeWork.md` to understand the collaboration protocol
2. Check your specific agent handoff document in `/coordination/handoffs/`
3. Review the recent changes in `/coordination/CHANGELOG.md`
4. Update these documents at the end of your session

## Team Structure

- **Human CEO (Hadi)**: Vision, archetypal framework, strategy
- **AI CEO**: Strategic coordination, documentation
- **Backend Architect (BEA)**: Microservice architecture, API design, technical specifications
- **Game Designer (GD)**: User experience, symbolic journey design, interaction mechanics
- **RIO (Repository Integration Orchestrator)**: GitHub management, CI/CD workflows, collaboration tools
- **Cursor AI**: Implementation support, code generation, development assistance
- **Unity Developer (Essi)**: Technical implementation for frontend (separate repository)

## Microservices

| Service | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [`astrology-engine`](./services/astrology-engine/) | Astrological calculations and chart generation | Python, FastAPI | In Development |
| `archetypal-mapping` | Mapping astrological data to archetypal patterns | Node.js, Express | Planned |
| `fractal-visualization` | Generating fractal parameters for Unity visualization | Python, Flask | Planned |
| `content-generation` | Creating personalized guidance and content | Node.js, Express | Planned |
| `audio-generation` | Creating consciousness-aligned audio | Python, Flask | Planned |
| `api-gateway` | Unified API access point | Node.js, Express | Planned |

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for Node.js services)
- Python 3.9+ (for Python services)
- Supabase CLI (for local database)

### Setup
1. Clone this repository
2. Copy `.env.example` to `.env` and configure environment variables
3. Run `docker-compose up` to start the development environment
4. See service-specific READMEs for further instructions

## Development Process

- Each service follows a documented specification
- Services are containerized for consistent development and deployment
- Integration happens through well-defined API contracts
- Changes are coordinated through our AI agent protocol

## License

This project is proprietary and confidential.

*Last updated: March 16, 2025 | 02:40 PST*  
*AI CEO*