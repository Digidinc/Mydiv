# Astrology Engine Service

The Astrology Engine Service provides accurate astrological calculations using Swiss Ephemeris as its foundation. It serves as the primary data source for archetypal mapping, supplying planetary positions, aspects, and other astrological data needed for personalized user experiences throughout the MyDivinations platform.

## Implementation Status

The service has been significantly expanded from its initial setup and now offers comprehensive astrological calculations:

✅ Basic FastAPI application structure
✅ Health check endpoint (`/health`)
✅ Welcome endpoint (`/`)
✅ Docker containerization
✅ Redis integration
✅ Swiss Ephemeris integration
✅ Birth chart calculations
✅ Planetary positions and tracking
✅ Aspects calculations
✅ Transits calculations with 5-year forecasting
✅ Progressions (Secondary, Tertiary, Solar Arc, Minor)
✅ Geocoding for location names
✅ Time zone determination

🔄 Upcoming Enhancements:
- Comprehensive test suite
- Performance optimization for large date ranges
- Expanded astrological interpretations
- Advanced caching strategy
- Improved error handling

## Tech Stack

- **Framework**: FastAPI (0.109.1)
- **Language**: Python 3.9
- **Cache**: Redis 7.2
- **Core Libraries**:
  - pyswisseph (2.10.3.2) - Swiss Ephemeris wrapper
  - Pydantic (2.5.2)
  - NumPy (1.24.3)
  - GeoPy (2.4.1)
  - Redis/aioredis
  - Loguru
  - pytest

## API Endpoints

The service now offers a comprehensive set of astrological calculation endpoints:

### Birth Chart

```http
POST /birth_chart
```
Calculate a complete natal chart from birth information, including planetary positions, house cusps, aspects, and dominant patterns.

```http
GET /birth_chart/{chart_id}
```
Retrieve a previously calculated birth chart by ID.

```http
GET /birth_chart
```
Get a summary of a birth chart (simplified version) with query parameters.

### Planets

```http
GET /planets
```
Get positions of specific planets at a given date and time.

```http
GET /planets/position-at-date
```
Track a planet's position over a date range.

```http
GET /planets/ingress
```
Find dates when planets enter new zodiac signs.

### Aspects

```http
POST /aspects
```
Calculate aspects between planet positions.

```http
POST /aspects/planetary-aspects
```
Calculate aspects between planets at two different times (useful for synastry).

```http
POST /aspects/aspect-timeline
```
Calculate a timeline of when a specific aspect becomes exact.

### Transits

```http
POST /transits
```
Calculate transit aspects to a natal chart.

```http
POST /transits/period
```
Calculate significant transits over a specified time period.

```http
GET /transits/five-year-forecast
```
Generate a comprehensive 5-year forecast of significant transits.

```http
GET /transits/current-transits
```
Get current planetary transits to a birth chart.

### Progressions

```http
POST /progressions
```
Calculate progressed chart positions using various progression methods.

```http
GET /progressions/secondary
```
Calculate secondary progressions (simplified endpoint).

```http
GET /progressions/progression-timeline
```
Calculate how progressed planets move over a specified period.

```http
GET /progressions/progressed-chart-with-transits
```
Calculate a progressed chart with current transits to both natal and progressed charts.

## Project Structure

```
/astrology-engine/
├── src/
│   ├── api/                # API routes
│   │   ├── aspects.py      # Aspects endpoints
│   │   ├── birth_chart.py  # Birth chart endpoints
│   │   ├── planets.py      # Planetary endpoints
│   │   ├── progressions.py # Progressions endpoints
│   │   └── transits.py     # Transit endpoints
│   ├── core/               # Core functionality
│   │   ├── calculator.py   # Calculation engine
│   │   └── ephemeris.py    # Swiss Ephemeris wrapper
│   ├── models/             # Data models
│   │   ├── aspects.py      # Aspect models
│   │   ├── birth_data.py   # Birth data models
│   │   ├── chart.py        # Chart models
│   │   ├── progressions.py # Progression models
│   │   └── transits.py     # Transit models
│   ├── services/           # Business logic
│   │   ├── aspects.py      # Aspect calculations
│   │   ├── birth_chart.py  # Birth chart calculations
│   │   ├── ephemeris.py    # Ephemeris operations
│   │   ├── geocoding.py    # Location to coordinates
│   │   ├── progressions.py # Progression calculations
│   │   └── transits.py     # Transit calculations
│   ├── config.py           # Configuration
│   └── main.py             # Application entry point
├── ephe/                   # Swiss Ephemeris data files
├── docs/                   # Documentation
├── Dockerfile              # Container definition
├── docker-compose.yml      # Container orchestration
├── requirements.txt        # Python dependencies
└── README.md               # Service documentation
```

## Development Setup

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Swiss Ephemeris data files

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

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download Swiss Ephemeris data files and place them in the `ephe` directory.

4. Set environment variables:
```bash
export REDIS_URL=redis://localhost:6379/0
export EPHEMERIS_PATH=./ephe
export TIMEZONE_DB_API_KEY=your_api_key  # Register at timezonedb.com (optional)
```

5. Run the development server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

```
REDIS_URL=redis://redis:6379/0
EPHEMERIS_PATH=/app/ephe
TIMEZONE_DB_API_KEY=your_api_key
LOG_LEVEL=INFO
DEBUG=False
```

## Testing

To run tests:
```bash
pytest
```

## Documentation

- Swagger UI Documentation - Available at `/docs` when the service is running
- ReDoc Documentation - Available at `/redoc` when the service is running

## Example Usage

### Calculate a Birth Chart

```python
import requests
import json

# API endpoint
url = "http://localhost:8000/birth_chart"

# Request data
data = {
    "birth_data": {
        "date": "1990-06-15",
        "time": "14:25:00",
        "location": {
            "latitude": 34.0522,
            "longitude": -118.2437,
            "location_name": "Los Angeles, CA"
        },
        "time_zone": "America/Los_Angeles"
    },
    "options": {
        "house_system": "placidus",
        "with_aspects": True,
        "with_dignities": True,
        "with_dominant_elements": True
    }
}

# Send request
response = requests.post(url, json=data)

# Print formatted response
print(json.dumps(response.json(), indent=2))
```

### Generate a 5-Year Transit Forecast

```python
import requests
import json

# API endpoint
url = "http://localhost:8000/transits/five-year-forecast"

# Query parameters
params = {
    "birth_date": "1990-06-15",
    "birth_time": "14:25:00",
    "birth_latitude": 34.0522,
    "birth_longitude": -118.2437
}

# Send request
response = requests.get(url, params=params)

# Print formatted response
print(json.dumps(response.json(), indent=2))
```

---

*Last Updated: March 17, 2025 | 01:10 UTC*  
*Maintained by: MyDiv BEA (Backend Architect)*