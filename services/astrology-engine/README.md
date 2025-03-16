# Astrology Engine Service

The Astrology Engine Service provides accurate astrological calculations using Swiss Ephemeris as its foundation. It serves as the primary data source for archetypal mapping, supplying planetary positions, aspects, and other astrological data needed for personalized user experiences throughout the MyDivinations platform.

## Current Implementation Status

The service is currently in its initial setup phase with the following components implemented:

- Basic FastAPI application structure
- Health check endpoint (`/health`)
- Welcome endpoint (`/`)
- Docker containerization
- Redis integration
- Basic project structure

## Tech Stack

- **Framework**: FastAPI (0.109.1)
- **Language**: Python 3.9
- **Cache**: Redis 7.2
- **Core Libraries**:
  - FastAPI
  - Uvicorn[standard]
  - Pydantic
  - Redis
- **Future Dependencies**:
  - pyswisseph (Python wrapper for Swiss Ephemeris)
  - NumPy (for numerical operations)
  - GeoPy (for geocoding)

## API Endpoints

### Currently Implemented

```
GET /health
```
Health check endpoint that returns service status

```
GET /
```
Welcome endpoint that returns a greeting message

### Planned Endpoints

```
POST /birth_chart
```
Calculate a complete natal chart from birth information

```
GET /planets
```
Get positions of specific planets at a given date and time

```
POST /aspects
```
Calculate aspects between planets

```
POST /transits
```
Calculate current transits to natal chart

```
POST /progressions
```
Calculate progressed chart positions

## Development Setup

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Swiss Ephemeris data files (for future implementation)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Digidinc/Mydiv.git
cd Mydiv/services/astrology-engine
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
```

5. Run the development server:
```bash
uvicorn src.main:app --reload
```

### Using Docker

1. Build and start the containers:
```bash
docker-compose up -d --build
```

2. View logs:
```bash
docker-compose logs -f
```

3. Stop the containers:
```bash
docker-compose down
```

## Current Project Structure

```
/astrology-engine/
├── src/
│   └── main.py             # Application entry point with basic endpoints
├── ephe/                   # Directory for ephemeris data files
├── Dockerfile             # Container definition
├── docker-compose.yml     # Container orchestration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # Service documentation
```

## Environment Variables

The following environment variables are currently used:

```
REDIS_URL=redis://redis:6379/0
```

## Testing

The service includes basic health checks in the Docker configuration. More comprehensive testing will be implemented as the service grows.

## Documentation

API documentation will be available at `/docs` when the service is running (Swagger UI).

## Next Steps

1. Implement Swiss Ephemeris integration
2. Add birth chart calculation endpoints
3. Implement planetary position calculations
4. Add aspect calculation functionality
5. Implement transit and progression calculations
6. Add comprehensive test suite
7. Implement caching strategy with Redis
8. Add proper error handling and validation

---

*Last Updated: March 16, 2025 | 06:55 UTC*  
*Maintained by: MyDiv BEA (Backend Architect)*