# MyDivinations Microservices

This directory contains the individual microservices that make up the MyDivinations backend.

## Service Directory

| Service | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [`astrology-engine`](./astrology-engine/) | Astrological calculations and chart generation | Python 3.9, FastAPI 0.109.1, Redis 7.2 | Initial Setup Complete |
| `archetypal-mapping` | Mapping astrological data to archetypal patterns | Node.js, Express | Planned |
| `fractal-visualization` | Generating fractal parameters for Unity visualization | Python, Flask | Planned |
| `content-generation` | Creating personalized guidance and content | Node.js, Express | Planned |
| `audio-generation` | Creating consciousness-aligned audio | Python, Flask | Planned |
| `api-gateway` | Unified API access point | Node.js, Express | Planned |

### Astrology Engine Service Status
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

## Development Guidelines

### Service Structure

Each service should follow this structure:

```
/service-name/
├── src/                 # Source code
│   ├── api/             # API endpoints
│   ├── core/            # Core business logic
│   ├── models/          # Data models
│   ├── services/        # Business services
│   └── utils/           # Utility functions
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
├── docs/                # Service-specific documentation
├── Dockerfile           # Container definition
├── docker-compose.yml   # Local development setup
├── .env.example         # Example environment variables
└── README.md            # Service-specific instructions
```

### Technology Selection

- **Python Services**: FastAPI or Flask based on performance needs
- **Node.js Services**: Express with TypeScript
- **Database Access**: Repository pattern with ORM
- **Authentication**: JWT-based through API Gateway
- **Testing**: pytest for Python, Jest for Node.js
- **Documentation**: OpenAPI/Swagger for all APIs
- **Caching**: Redis for high-performance caching

### Development Workflow

1. Start from the service specification in `/docs/specifications/`
2. Create the service structure following the guidelines
3. Implement core functionality with tests
4. Document APIs using OpenAPI/Swagger
5. Create Docker configurations
6. Submit PR with reference to implementation checklist

### Communication Patterns

- All services should implement the patterns defined in `/docs/architecture/service-communication-patterns.md`
- Error responses should follow the standardized format
- Authentication should be handled through the API Gateway
- Services should use the circuit breaker pattern for external dependencies
- Redis should be used for caching where appropriate

## Service Launch Checklist

Before a service is considered ready for deployment, ensure:

- [ ] All specified functionality implemented
- [ ] Unit test coverage > 80%
- [ ] Integration tests for all endpoints
- [ ] Documentation completed
- [ ] Performance testing completed
- [ ] Security review completed
- [ ] Docker configuration tested
- [ ] CI/CD pipeline configured
- [ ] Health checks implemented
- [ ] Monitoring configured
- [ ] Caching strategy implemented

## Deployment

Services are deployed using Docker containers orchestrated through Docker Compose:

1. Each service has its own container
2. Shared resources (Redis, etc.) are in separate containers
3. API Gateway handles routing and authentication
4. Monitoring through Prometheus/Grafana
5. Logging through structured JSON logs

## Current Focus

- ✅ Initial Astrology Engine Service setup complete
- 🔄 Implementing Swiss Ephemeris integration
- 🔄 Developing birth chart calculation endpoints
- 🔄 Setting up service monitoring and logging
- 🔄 Implementing caching strategies

---

*Last Updated: March 16, 2025 | 07:15 UTC*  
*Maintained by: AI CEO*