# MyDivinations Project

## Overview
MyDivinations is a comprehensive platform for astrological analysis and archetypal mapping. The project follows a microservices architecture with a Next.js frontend and various specialized backend services.

## Repository Structure
- `/services` - Backend microservices
- `/web` - Next.js web application
- `/coordination` - Project coordination documents
- `/docs` - Project documentation

## Team Roles
- Backend Development: FastAPI microservices
- Frontend Development: Next.js application
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

### Web Application
1. **Next.js Frontend** 🔄 Planning
   - Description: User interface for the platform
   - Tech Stack: Next.js, TypeScript, Tailwind CSS
   - Status: Planning phase

2. **Admin Dashboard** 🔄 Planning
   - Description: Administrative interface
   - Tech Stack: Next.js, TypeScript, Tailwind CSS
   - Status: Planning phase

## Prerequisites
- Docker and Docker Compose
- PostgreSQL 15+
- Node.js 18+
- Python 3.9+
- Redis 7.2+

## Development
1. Clone the repository
2. Set up the required databases (see Database Configuration section)
3. Start the required services using Docker Compose
4. Follow service-specific README files for detailed setup instructions

## Current Focus
- Implementing Swiss Ephemeris integration in the astrology-engine service
- Setting up the Next.js web application infrastructure
- Defining the data models for the archetypal mapping service

For detailed information about database configuration and available services, please refer to the root README.md file in the repository.

---

*Last Updated: March 16, 2025*