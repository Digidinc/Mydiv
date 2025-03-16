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

- `/docs` - Project documentation
- `/services` - Individual microservices
- `/shared` - Shared libraries and utilities
- `/deploy` - Deployment configurations
- `/coordination` - AI agent coordination documents

## For AI Team Members

This project uses a coordinated AI agent approach. If you're an AI agent working on this project:

1. First read `/coordination/HowWeWork.md` to understand the collaboration protocol
2. Check your specific agent handoff document in `/coordination/handoffs/`
3. Review the recent changes in `/coordination/CHANGELOG.md`
4. Update these documents at the end of your session

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

## Microservices

| Service | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| Astrology Engine | Astrological calculations | Python/FastAPI | In Development |
| Archetypal Mapping | Maps astrology to archetypes | Node.js/Express | Planned |
| Fractal Visualization | Generates fractal parameters | Python/Flask | Planned |
| Content Generation | Creates personalized content | Node.js/Express | Planned |
| Audio Generation | Creates consciousness-aligned audio | Python/Flask | Planned |
| API Gateway | Unified API access point | Node.js/Express | Planned |

## Development Process

- Each service follows a documented specification
- Services are containerized for consistent development and deployment
- Integration happens through well-defined API contracts
- Changes are coordinated through our AI agent protocol

## License

This project is proprietary and confidential.

*Last updated: March 15, 2025*