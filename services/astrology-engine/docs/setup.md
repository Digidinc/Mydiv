# Astrology Engine Setup Guide

This document provides detailed instructions for setting up and running the Astrology Engine service.

## Prerequisites

- Docker 24.0.0 or later
- Docker Compose 2.21.0 or later
- Git
- Python 3.9 or later (for local development)

## Docker Setup

### Container Configuration

The service uses two containers:

1. **astrology-engine**: The main FastAPI application
   - Base image: python:3.9-slim
   - Exposed port: 8000
   - Health check: HTTP GET /health
   - Environment variables:
     - REDIS_URL=redis://redis:6379/0

2. **redis**: Cache service
   - Image: redis:7.2-alpine
   - Exposed port: 6379
   - Persistence: Enabled with appendonly
   - Health check: redis-cli ping

### Building and Running

1. Build the containers:
```bash
docker-compose build
```

2. Start the services:
```bash
docker-compose up -d
```

3. Verify the services are running:
```bash
docker-compose ps
```

Expected output:
```
         Name                       Command                  State                      Ports               
------------------------------------------------------------------------------------------------------------
astrology-engine         uvicorn src.main:app --hos ...   Up (healthy)   0.0.0.0:8000->8000/tcp
astrology-engine-redis   docker-entrypoint.sh redis ...   Up (healthy)   0.0.0.0:6379->6379/tcp
```

4. Check the logs:
```bash
docker-compose logs -f
```

### Testing the Setup

1. Test the health check endpoint:
```bash
curl http://localhost:8000/health
```
Expected response:
```json
{"status":"healthy"}
```

2. Test the welcome endpoint:
```bash
curl http://localhost:8000/
```
Expected response:
```json
{"message":"Welcome to Astrology Engine API"}
```

## Local Development Setup

For local development without Docker:

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start Redis (required):
```bash
# Install Redis on your system or use Docker:
docker run -d -p 6379:6379 redis:7.2-alpine
```

4. Set environment variables:
```bash
export REDIS_URL=redis://localhost:6379/0
```

5. Start the development server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Common Issues

1. **Port conflicts**
   - Error: "port is already allocated"
   - Solution: Stop any services using ports 8000 or 6379, or modify the port mappings in docker-compose.yml

2. **Redis connection issues**
   - Error: Cannot connect to Redis
   - Solution: Verify Redis container is running and REDIS_URL is correct

3. **Container health check failures**
   - Issue: Containers show "(unhealthy)" status
   - Solution: Check container logs and verify services are running correctly

## Next Steps

After successful setup:

1. Access the API documentation at http://localhost:8000/docs
2. Review the main README.md for available endpoints
3. Begin implementing additional features as outlined in the project roadmap

---

*Last Updated: March 16, 2025 | 07:00 UTC*