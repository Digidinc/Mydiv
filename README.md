# MyDivinations Project

## Overview
MyDivinations is a comprehensive platform for astrological analysis and archetypal mapping. The project follows a microservices architecture with backend services and planned frontend components.

## Repository Structure
- `/services` - Backend microservices
- `/coordination` - Project coordination documents
- `/docs` - Project documentation

## Team Roles
- Backend Development: FastAPI microservices
- DevOps: Docker, CI/CD, deployment
- AI Integration: LLM integration, vector embeddings

## Components

### Backend Microservices
1. **Astrology Engine** ✅ Initial Setup Complete
   - Description: Handles astrological calculations and chart generation
   - Tech Stack: Python 3.9, FastAPI, Redis, Swiss Ephemeris
   - Status: Basic setup complete, health check endpoint implemented
   - Next Steps: Swiss Ephemeris integration, chart calculations

2. **Archetypal Mapping** 🔄 Planning
   - Description: Maps astrological data to archetypal patterns
   - Tech Stack: Python, FastAPI, pgvector
   - Status: Planning phase

3. **User Management** 🔄 Planning
   - Description: Handles user authentication and profile management
   - Tech Stack: Python, FastAPI, PostgreSQL
   - Status: Planning phase

4. **Content Management** 🔄 Planning
   - Description: Manages content and resources
   - Tech Stack: Python, FastAPI, PostgreSQL
   - Status: Planning phase

### Future Components (Planned)
1. **Web Application**
   - Description: User interface for the platform
   - Tech Stack: Next.js, TypeScript, Tailwind CSS
   - Status: Documentation and planning phase
   - Implementation: Scheduled after backend services mature

2. **Unity Integration**
   - Description: Mobile application for interactive experiences
   - Tech Stack: Unity, C#
   - Status: Planning phase
   - Implementation: Planned for Q3 2025

## Prerequisites
- Docker and Docker Compose
- PostgreSQL 15+
- Python 3.9+
- Redis 7.2+

## Development
1. Clone the repository
2. Set up the required databases (see Database Configuration section)
3. Start the required services using Docker Compose
4. Follow service-specific README files for detailed setup instructions

## Current Focus
- Implementing Swiss Ephemeris integration in the astrology-engine service
- Defining the data models for the archetypal mapping service
- Improving project documentation structure
- Establishing CI/CD pipelines for backend services

For detailed information about project status, refer to the `/coordination/STATUS.md` file.

---

*Last Updated: March 17, 2025*