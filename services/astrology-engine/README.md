# Astrology Engine Service

The Astrology Engine Service provides accurate astrological calculations using Swiss Ephemeris as its foundation. It serves as the primary data source for archetypal mapping, supplying planetary positions, aspects, and other astrological data needed for personalized user experiences throughout the MyDivinations platform.

## Features

- Calculate precise natal charts from birth date, time, and location data
- Determine planetary positions, aspects, houses, and other astrological elements
- Calculate transits, progressions, and other time-based astrological data
- Provide dominant elements and modalities analysis for archetypal mapping
- Support multiple house systems with Placidus as the primary default

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database**: None (stateless service)
- **Core Libraries**:
  - pyswisseph (Python wrapper for Swiss Ephemeris)
  - Pydantic (for data validation)
  - NumPy (for numerical operations)
  - GeoPy (for geocoding)
- **External Dependencies**:
  - Swiss Ephemeris ephemeris data files

## API Endpoints

### Birth Chart Calculation
```
POST /birth_chart
```
Calculate a complete natal chart from birth information

### Planetary Positions
```
GET /planets
```
Get positions of specific planets at a given date and time

### Aspects Calculation
```
POST /aspects
```
Calculate aspects between planets

### Transits Calculation
```
POST /transits
```
Calculate current transits to natal chart

### Progressions Calculation
```
POST /progressions
```
Calculate progressed chart positions

## Development Setup

### Prerequisites
- Python 3.9+
- Docker and Docker Compose (for containerized development)
- Swiss Ephemeris data files

### Local Development

1. Clone the repository:
```
git clone https://github.com/Digidinc/Mydiv.git
cd Mydiv/services/astrology-engine
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create .env file:
```
cp .env.example .env
```

5. Run the development server:
```
uvicorn src.main:app --reload
```

### Using Docker

1. Build and start the container:
```
docker-compose up -d
```

2. View logs:
```
docker-compose logs -f
```

3. Stop the container:
```
docker-compose down
```

## Project Structure

```
/astrology-engine/
├── src/
│   ├── api/                # API endpoints
│   │   ├── __init__.py
│   │   ├── birth_chart.py  # Birth chart endpoints
│   │   ├── planets.py      # Planetary position endpoints
│   │   ├── aspects.py      # Aspect calculation endpoints
│   │   ├── transits.py     # Transit calculation endpoints
│   │   └── progressions.py # Progression calculation endpoints
│   ├── core/               # Core calculation engine
│   │   ├── __init__.py
│   │   ├── ephemeris.py    # Ephemeris provider interface
│   │   ├── calculator.py   # Main calculation service
│   │   ├── aspects.py      # Aspect calculation
│   │   └── coordinates.py  # Coordinate transformations
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   ├── birth_data.py   # Birth data models
│   │   ├── chart.py        # Chart data models
│   │   ├── planets.py      # Planetary data models
│   │   └── aspects.py      # Aspect data models
│   ├── services/           # Business logic services
│   │   ├── __init__.py
│   │   ├── birth_chart.py  # Birth chart service
│   │   ├── transit.py      # Transit service
│   │   └── progression.py  # Progression service
│   ├── utils/              # Utility functions
│   │   ├── __init__.py
│   │   ├── date.py         # Date handling utilities
│   │   ├── logging.py      # Logging configuration
│   │   └── errors.py       # Error handling utilities
│   ├── config.py           # Configuration management
│   └── main.py             # Application entry point
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test fixtures
├── docs/                   # Service-specific documentation
├── Dockerfile              # Container definition
├── docker-compose.yml      # Local development setup
├── requirements.txt        # Python dependencies
├── requirements-dev.txt    # Development dependencies
├── .env.example            # Example environment variables
└── README.md               # Service documentation
```

## Testing

Run the test suite:
```
pytest
```

Run with coverage:
```
pytest --cov=src
```

## Documentation

API documentation is available at `/docs` when the service is running.

## Performance Considerations

- Birth chart calculations are cached to avoid recalculation
- Planetary positions for common dates are cached
- Computation-heavy operations are optimized

## References

- [Swiss Ephemeris Documentation](https://www.astro.com/swisseph/swephinfo_e.htm)
- [PySwissEph Documentation](https://github.com/astrorigin/pyswisseph)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

*Last Updated: March 15, 2025 | 22:45 PST*  
*Maintained by: MyDiv BEA (Backend Architect)*