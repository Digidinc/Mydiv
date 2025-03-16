# MyDivinations Architecture Documentation

This directory contains architectural documentation for the MyDivinations project.

## Contents

- `overview.md` - High-level architecture overview (planned)
- `backend-services.md` - Backend microservices architecture (planned)
- `frontend-architecture.md` - Frontend application architecture planning (not currently implemented)
- `data-flow.md` - System-wide data flow diagrams (planned)

## Architecture Overview

MyDivinations follows a microservices architecture with:

1. **Backend Services**:
   - Astrology Engine Service
   - Archetypal Mapping Service (planned)
   - User Management Service (planned)
   - Content Management Service (planned)

2. **Frontend Applications** (postponed until backend is more mature):
   - Next.js Web Application (planning documentation only)
   - Admin Dashboard (planning documentation only)
   - Unity-based Mobile Implementation (planned for Q3 2025)

3. **Data Stores**:
   - PostgreSQL for relational data
   - Redis for caching
   - pgvector for vector embeddings (planned)

## Key Architectural Principles

1. **Service Independence** - Each service should be independently deployable
2. **API-First Design** - Well-defined API contracts between services
3. **Stateless Services** - Stateless designs for horizontal scalability
4. **Domain-Driven Design** - Services aligned with business domains
5. **Backend First** - Focus on implementing core backend functionality before frontend

## Implementation Status

The current implementation focuses on backend services, particularly the Astrology Engine Service. Frontend development is in the planning stage only and implementation has been postponed until the backend services have matured sufficiently.

## Additional Resources

- See `/GameDesign/Implementation/Web_Implementation_Architecture.md` for frontend planning documentation (not currently implemented)
- See `/services/README.md` for backend services architecture

---

*Last Updated: March 17, 2025 | 10:05 PST*  
*MyDiv RIO*