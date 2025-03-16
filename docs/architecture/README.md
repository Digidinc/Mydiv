# MyDivinations Architecture Documentation

This directory contains architectural documentation for the MyDivinations project.

## Contents

- `overview.md` - High-level architecture overview (planned)
- `backend-services.md` - Backend microservices architecture (planned)
- `frontend-architecture.md` - Frontend application architecture (planned)
- `data-flow.md` - System-wide data flow diagrams (planned)

## Architecture Overview

MyDivinations follows a microservices architecture with:

1. **Backend Services**:
   - Astrology Engine Service
   - Archetypal Mapping Service
   - User Management Service
   - Content Management Service

2. **Frontend Applications**:
   - Next.js Web Application
   - Admin Dashboard
   - Unity-based Mobile Implementation (planned)

3. **Data Stores**:
   - PostgreSQL for relational data
   - Redis for caching
   - pgvector for vector embeddings

## Key Architectural Principles

1. **Service Independence** - Each service should be independently deployable
2. **API-First Design** - Well-defined API contracts between services
3. **Stateless Services** - Stateless designs for horizontal scalability
4. **Domain-Driven Design** - Services aligned with business domains
5. **Progressive Enhancement** - Core functionality works in all environments

## Additional Resources

- See `/GameDesign/Implementation/Web_Implementation_Architecture.md` for detailed frontend architecture
- See `/services/README.md` for backend services architecture

---

*Last Updated: March 17, 2025 | 09:50 PST*  
*MyDiv RIO*