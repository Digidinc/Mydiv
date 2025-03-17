# MyDivinations Astrology Engine API Documentation

This document provides comprehensive information for developers integrating with the MyDivinations Astrology Engine API. It includes endpoint references, request/response formats, and examples for all major operations.

## Base URL

```
https://api.mydivinations.com/astrology-engine
```

For local development:
```
http://localhost:8000
```

## Authentication

All API requests require authentication using an API key.

```http
X-API-Key: your_api_key_here
```

## Response Format

All responses are returned in JSON format with a consistent structure:

- Success responses include the requested data
- Error responses include error details and a status code

### Error Response Format

```json
{
  "error": {
    "message": "Detailed error message",
    "code": "ERROR_CODE"
  }
}
```

## Common HTTP Status Codes

- `200 OK`: The request was successful
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: The requested resource was not found
- `422 Unprocessable Entity`: Valid parameters but calculation not possible
- `500 Internal Server Error`: Server-side error

---

## Birth Chart Endpoints

### Calculate Birth Chart

Creates a complete astrological natal chart based on birth information.

```http
POST /birth_chart
```

#### Request Body

```json
{
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
    "with_aspects": true,
    "with_dignities": true,
    "with_dominant_elements": true
  }
}
```

#### Response

```json
{
  "birth_chart": {
    "planets": {
      "sun": {
        "sign": "Gemini",
        "degree": 24.83,
        "house": 10,
        "longitude": 84.83,
        "aspects": [...]
      },
      "moon": {
        "sign": "Libra",
        "degree": 22.53,
        "house": 2,
        "longitude": 202.53,
        "aspects": [...]
      },
      ...
    },
    "houses": {
      "1": { "sign": "Leo", "degree": 15.27 },
      "2": { "sign": "Virgo", "degree": 10.45 },
      ...
    },
    "ascendant": { "sign": "Leo", "degree": 15.27 },
    "mc": { "sign": "Taurus", "degree": 3.42 },
    "dominant_elements": {
      "fire": 35,
      "earth": 15,
      "air": 20,
      "water": 30
    },
    "dominant_modalities": {
      "cardinal": 40,
      "fixed": 30,
      "mutable": 30
    }
  }
}
```

### Get Chart Summary

Returns a simplified birth chart summary with query parameters.

```http
GET /birth_chart
```

#### Query Parameters

- `date` (required): Birth date in YYYY-MM-DD format
- `time` (optional): Birth time in HH:MM:SS format
- `latitude` (optional): Birth location latitude
- `longitude` (optional): Birth location longitude

#### Response

```json
{
  "summary": {
    "sun_sign": "Gemini",
    "moon_sign": "Libra",
    "ascendant": "Leo",
    "planets": {
      "sun": { "sign": "Gemini", "degree": 24.83 },
      "moon": { "sign": "Libra", "degree": 22.53 },
      ...
    }
  }
}
```

### Retrieve Stored Chart

Retrieves a previously calculated birth chart by ID.

```http
GET /birth_chart/{chart_id}
```

#### Response

Same format as the "Calculate Birth Chart" endpoint.

---

## Planetary Endpoints

### Get Planetary Positions

Returns positions of planets at a given date and time.

```http
GET /planets
```

#### Query Parameters

- `date` (required): Date in YYYY-MM-DD format
- `time` (optional): Time in HH:MM:SS format (defaults to 12:00:00)
- `latitude` (optional): Observer's latitude
- `longitude` (optional): Observer's longitude
- `planets` (optional): Comma-separated list of planets (defaults to all)

#### Response

```json
{
  "date": "2025-03-15",
  "time": "12:00:00",
  "planets": {
    "sun": {
      "sign": "Pisces",
      "degree": 24.67,
      "longitude": 354.67,
      "retrograde": false,
      "speed": 0.983
    },
    "moon": {
      "sign": "Libra",
      "degree": 15.34,
      "longitude": 195.34,
      "retrograde": false,
      "speed": 13.176
    },
    ...
  }
}
```

### Track Planet Position Over Time

Tracks a planet's position over a date range.

```http
GET /planets/position-at-date
```

#### Query Parameters

- `planet` (required): Planet name (sun, moon, mercury, etc.)
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format (defaults to start_date)
- `interval_days` (optional): Interval between calculations in days (default: 1)

#### Response

```json
{
  "planet": "mars",
  "start_date": "2025-01-01",
  "end_date": "2025-01-15",
  "interval_days": 5,
  "positions": [
    {
      "date": "2025-01-01",
      "sign": "Aries",
      "degree": 12.45,
      "longitude": 12.45,
      "retrograde": false
    },
    {
      "date": "2025-01-06",
      "sign": "Aries",
      "degree": 14.78,
      "longitude": 14.78,
      "retrograde": false
    },
    ...
  ]
}
```

### Find Sign Ingress Dates

Finds dates when a planet enters new zodiac signs.

```http
GET /planets/ingress
```

#### Query Parameters

- `planet` (required): Planet name (sun, moon, mercury, etc.)
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format (defaults to 1 year from start)
- `signs` (optional): Comma-separated list of signs to check ingress into (defaults to all)

#### Response

```json
{
  "planet": "mercury",
  "start_date": "2025-01-01",
  "end_date": "2025-06-30",
  "ingress_events": [
    {
      "date": "2025-01-15",
      "planet": "mercury",
      "sign": "Aquarius",
      "degree": 0.23,
      "retrograde": false
    },
    {
      "date": "2025-02-03",
      "planet": "mercury",
      "sign": "Pisces",
      "degree": 0.12,
      "retrograde": false
    },
    ...
  ]
}
```

---

## Aspects Endpoints

### Calculate Aspects

Calculates aspects between planetary positions.

```http
POST /aspects
```

#### Request Body

```json
{
  "planet_positions": {
    "sun": 84.83,
    "moon": 202.53,
    "mercury": 95.67,
    "venus": 110.23,
    "mars": 45.78
  },
  "options": {
    "aspects": ["conjunction", "opposition", "trine", "square", "sextile"],
    "orbs": {
      "conjunction": 8.0,
      "opposition": 8.0,
      "trine": 6.0,
      "square": 6.0,
      "sextile": 4.0
    }
  }
}
```

#### Response

```json
{
  "aspects": [
    {
      "planet1": "sun",
      "planet2": "mercury",
      "type": "conjunction",
      "orb": 4.78,
      "applying": false,
      "influence": 0.82
    },
    {
      "planet1": "moon",
      "planet2": "mars",
      "type": "square",
      "orb": 2.11,
      "applying": true,
      "influence": 0.95
    },
    ...
  ]
}
```

### Calculate Planetary Aspects

Calculates aspects between planets at two different times.

```http
POST /aspects/planetary-aspects
```

#### Request Body

```json
{
  "aspects_config": {
    "planets1": ["sun", "moon", "mercury", "venus", "mars"],
    "planets2": ["jupiter", "saturn", "uranus", "neptune", "pluto"],
    "aspects": ["conjunction", "opposition", "trine", "square"],
    "orbs": {
      "conjunction": 5.0,
      "opposition": 5.0,
      "trine": 4.0,
      "square": 4.0
    }
  },
  "date1": "1990-06-15",
  "time1": "14:25:00",
  "date2": "2025-03-15",
  "time2": "12:00:00"
}
```

#### Response

```json
{
  "date1": "1990-06-15",
  "time1": "14:25:00",
  "date2": "2025-03-15",
  "time2": "12:00:00",
  "aspects": [
    {
      "chart1_planet": "sun",
      "chart2_planet": "jupiter",
      "type": "trine",
      "orb": 3.45,
      "applying": false,
      "influence": 0.72
    },
    ...
  ]
}
```

### Calculate Aspect Timeline

Calculates when a specific aspect between two planets becomes exact.

```http
POST /aspects/aspect-timeline
```

#### Request Body

```json
{
  "planet1": "jupiter",
  "planet2": "saturn",
  "aspect_type": "conjunction",
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "orb": 1.0
}
```

#### Response

```json
{
  "planet1": "jupiter",
  "planet2": "saturn",
  "aspect_type": "conjunction",
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "orb": 1.0,
  "timeline": [
    {
      "date": "2025-02-20",
      "planet1": "jupiter",
      "planet2": "saturn",
      "aspect": "conjunction",
      "is_exact": true,
      "orb": 0.02,
      "planet1_sign": "Aries",
      "planet2_sign": "Aries",
      "planet1_retrograde": false,
      "planet2_retrograde": false
    },
    ...
  ]
}
```

---

## Transits Endpoints

### Calculate Transits

Calculates current transits to a natal chart.

```http
POST /transits
```

#### Request Body

```json
{
  "natal_positions": {
    "sun": 84.83,
    "moon": 202.53,
    "mercury": 95.67,
    "venus": 110.23,
    "mars": 45.78,
    "jupiter": 312.45,
    "saturn": 278.89
  },
  "transit_time": {
    "date": "2025-03-15",
    "time": "12:00:00",
    "time_zone": "UTC"
  },
  "options": {
    "aspects": ["conjunction", "opposition", "trine", "square", "sextile"],
    "orbs": {
      "conjunction": 1.5,
      "opposition": 1.5,
      "trine": 1.0,
      "square": 1.0,
      "sextile": 0.8
    },
    "planets": ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]
  }
}
```

#### Response

```json
{
  "transit_date": "2025-03-15",
  "transits": [
    {
      "transit_planet": "jupiter",
      "natal_planet": "venus",
      "aspect": "trine",
      "orb": 0.45,
      "applying": true,
      "exact_date": "2025-03-17",
      "influence": 0.92,
      "transit_sign": "Aries"
    },
    ...
  ]
}
```

### Calculate Transit Period

Calculates significant transits over a specified time period.

```http
POST /transits/period
```

#### Request Body

```json
{
  "natal_positions": {
    "sun": 84.83,
    "moon": 202.53,
    "mercury": 95.67,
    "venus": 110.23,
    "mars": 45.78,
    "jupiter": 312.45,
    "saturn": 278.89
  },
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "planets": ["jupiter", "saturn", "uranus", "neptune", "pluto"],
  "aspects": ["conjunction", "opposition", "square"],
  "orbs": {
    "conjunction": 1.0,
    "opposition": 1.0,
    "square": 0.8
  }
}
```

#### Response

```json
{
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "transit_timeline": [
    {
      "date": "2025-02-15",
      "transit_planet": "jupiter",
      "natal_planet": "sun",
      "aspect": "trine",
      "applying": false,
      "planet_retrograde": false
    },
    ...
  ]
}
```

### Generate Five-Year Forecast

Generates a comprehensive 5-year forecast of significant transits.

```http
GET /transits/five-year-forecast
```

#### Query Parameters

- `birth_date` (required): Birth date in YYYY-MM-DD format
- `birth_time` (optional): Birth time in HH:MM:SS format
- `birth_latitude` (optional): Birth location latitude
- `birth_longitude` (optional): Birth location longitude
- `start_date` (optional): Start date in YYYY-MM-DD format (defaults to current date)
- `transit_planets` (optional): Comma-separated list of transit planets to include

#### Response

```json
{
  "birth_date": "1990-06-15",
  "start_date": "2025-03-15",
  "end_date": "2030-03-15",
  "significant_transits": [
    {
      "date": "2025-04-23",
      "transit_planet": "jupiter",
      "natal_planet": "sun",
      "aspect": "conjunction",
      "applying": false,
      "planet_retrograde": false
    },
    ...
  ],
  "major_life_events": [
    {
      "date": "2026-02-15",
      "transit_planet": "saturn",
      "natal_planet": "sun",
      "aspect": "square",
      "description": "A period of challenge and restructuring in your core identity and purpose. May involve obstacles from authority figures or limitations on personal expression.",
      "significance": "significant"
    },
    ...
  ]
}
```

### Get Current Transits

Gets current planetary transits to a natal chart.

```http
GET /transits/current-transits
```

#### Query Parameters

- `birth_date` (required): Birth date in YYYY-MM-DD format
- `birth_time` (optional): Birth time in HH:MM:SS format
- `birth_latitude` (optional): Birth location latitude
- `birth_longitude` (optional): Birth location longitude
- `orb` (optional): Maximum orb in degrees (default: 1.0)

#### Response

```json
{
  "birth_date": "1990-06-15",
  "current_date": "2025-03-17",
  "active_transits": [
    {
      "transit_planet": "jupiter",
      "natal_planet": "venus",
      "aspect": "trine",
      "orb": 0.45,
      "applying": true,
      "influence": 0.92,
      "transit_sign": "Aries",
      "description": "A favorable period for relationships, finances, and creative pursuits. Brings optimism, growth, and opportunities in areas related to love and beauty."
    },
    ...
  ]
}
```

---

## Progressions Endpoints

### Calculate Progressions

Calculates progressed chart positions using various progression methods.

```http
POST /progressions
```

#### Request Body

```json
{
  "birth_data": {
    "date": "1990-06-15",
    "time": "14:25:00",
    "location": {
      "latitude": 34.0522,
      "longitude": -118.2437
    },
    "time_zone": "America/Los_Angeles"
  },
  "progression_date": "2025-03-15",
  "options": {
    "progression_type": "secondary",
    "planets": ["sun", "moon", "mercury", "venus", "mars"],
    "include_houses": true
  }
}
```

#### Response

```json
{
  "progression_date": "2025-03-15",
  "progressed_positions": {
    "sun": {
      "sign": "Leo",
      "degree": 5.67,
      "house": 12,
      "longitude": 125.67,
      "retrograde": false
    },
    "moon": {
      "sign": "Aquarius",
      "degree": 18.34,
      "house": 6,
      "longitude": 318.34,
      "retrograde": false
    },
    ...
  },
  "progressed_houses": {
    "1": { "sign": "Virgo", "degree": 2.45 },
    "2": { "sign": "Libra", "degree": 0.12 },
    ...
  }
}
```

### Calculate Secondary Progressions

Calculates secondary progressions (simplified endpoint).

```http
GET /progressions/secondary
```

#### Query Parameters

- `birth_date` (required): Birth date in YYYY-MM-DD format
- `birth_time` (optional): Birth time in HH:MM:SS format
- `birth_latitude` (optional): Birth location latitude
- `birth_longitude` (optional): Birth location longitude
- `progression_date` (optional): Progression date in YYYY-MM-DD format (defaults to current date)
- `planets` (optional): Comma-separated list of planets to include

#### Response

```json
{
  "birth_date": "1990-06-15",
  "progression_date": "2025-03-15",
  "progressed_positions": {
    "sun": {
      "sign": "Leo",
      "degree": 5.67,
      "longitude": 125.67,
      "retrograde": false
    },
    ...
  }
}
```

### Calculate Progression Timeline

Calculates how progressed planets move over a specified period.

```http
GET /progressions/progression-timeline
```

#### Query Parameters

- `birth_date` (required): Birth date in YYYY-MM-DD format
- `birth_time` (optional): Birth time in HH:MM:SS format
- `birth_latitude` (optional): Birth location latitude
- `birth_longitude` (optional): Birth location longitude
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `interval_months` (optional): Interval in months between calculations (default: 6)
- `planet` (optional): Specific planet to track (defaults to all major planets)

#### Response

```json
{
  "birth_date": "1990-06-15",
  "start_date": "2025-01-01",
  "end_date": "2030-01-01",
  "interval_months": 6,
  "progression_timeline": [
    {
      "date": "2025-01-01",
      "positions": {
        "sun": {
          "sign": "Leo",
          "degree": 4.78,
          "retrograde": false,
          "ingress": false
        },
        "moon": {
          "sign": "Aquarius",
          "degree": 12.45,
          "retrograde": false,
          "ingress": false
        },
        ...
      }
    },
    {
      "date": "2025-07-01",
      "positions": {
        "sun": {
          "sign": "Leo",
          "degree": 5.23,
          "retrograde": false,
          "ingress": false
        },
        "moon": {
          "sign": "Pisces",
          "degree": 2.67,
          "retrograde": false,
          "ingress": true
        },
        ...
      }
    },
    ...
  ]
}
```

### Calculate Progressed Chart With Transits

Calculates a progressed chart with current transits to both natal and progressed charts.

```http
GET /progressions/progressed-chart-with-transits
```

#### Query Parameters

- `birth_date` (required): Birth date in YYYY-MM-DD format
- `birth_time` (optional): Birth time in HH:MM:SS format
- `birth_latitude` (optional): Birth location latitude
- `birth_longitude` (optional): Birth location longitude
- `calculation_date` (optional): Calculation date in YYYY-MM-DD format (defaults to current date)

#### Response

```json
{
  "birth_date": "1990-06-15",
  "calculation_date": "2025-03-17",
  "progressed_positions": {
    "sun": {
      "sign": "Leo",
      "degree": 5.67,
      "longitude": 125.67,
      "retrograde": false
    },
    ...
  },
  "transits_to_natal": [
    {
      "transit_planet": "jupiter",
      "natal_planet": "venus",
      "aspect": "trine",
      "orb": 0.45,
      "applying": true,
      "influence": 0.92
    },
    ...
  ],
  "transits_to_progressed": [
    {
      "transit_planet": "saturn",
      "natal_planet": "progressed_sun",
      "aspect": "square",
      "orb": 0.78,
      "applying": false,
      "influence": 0.85
    },
    ...
  ]
}
```

---

## Code Examples

### JavaScript/TypeScript

```typescript
// Calculate Birth Chart
async function calculateBirthChart() {
  const response = await fetch('https://api.mydivinations.com/astrology-engine/birth_chart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your_api_key'
    },
    body: JSON.stringify({
      birth_data: {
        date: '1990-06-15',
        time: '14:25:00',
        location: {
          latitude: 34.0522,
          longitude: -118.2437,
          location_name: 'Los Angeles, CA'
        },
        time_zone: 'America/Los_Angeles'
      },
      options: {
        house_system: 'placidus',
        with_aspects: true,
        with_dignities: true,
        with_dominant_elements: true
      }
    })
  });
  
  const data = await response.json();
  return data;
}

// Get Five-Year Forecast
async function getFiveYearForecast(birthDate, birthTime, latitude, longitude) {
  const params = new URLSearchParams({
    birth_date: birthDate,
    birth_time: birthTime,
    birth_latitude: latitude,
    birth_longitude: longitude
  });
  
  const response = await fetch(
    `https://api.mydivinations.com/astrology-engine/transits/five-year-forecast?${params}`,
    {
      headers: {
        'X-API-Key': 'your_api_key'
      }
    }
  );
  
  const data = await response.json();
  return data;
}
```

### Python

```python
import requests

# Calculate Birth Chart
def calculate_birth_chart():
    url = "https://api.mydivinations.com/astrology-engine/birth_chart"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "your_api_key"
    }
    
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
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Get Five-Year Forecast
def get_five_year_forecast(birth_date, birth_time, latitude, longitude):
    url = "https://api.mydivinations.com/astrology-engine/transits/five-year-forecast"
    
    params = {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_latitude": latitude,
        "birth_longitude": longitude
    }
    
    headers = {
        "X-API-Key": "your_api_key"
    }
    
    response = requests.get(url, params=params, headers=headers)
    return response.json()
```

### Swift (iOS)

```swift
// Calculate Birth Chart
func calculateBirthChart() async throws -> [String: Any] {
    let url = URL(string: "https://api.mydivinations.com/astrology-engine/birth_chart")!
    
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.addValue("application/json", forHTTPHeaderField: "Content-Type")
    request.addValue("your_api_key", forHTTPHeaderField: "X-API-Key")
    
    let requestBody: [String: Any] = [
        "birth_data": [
            "date": "1990-06-15",
            "time": "14:25:00",
            "location": [
                "latitude": 34.0522,
                "longitude": -118.2437,
                "location_name": "Los Angeles, CA"
            ],
            "time_zone": "America/Los_Angeles"
        ],
        "options": [
            "house_system": "placidus",
            "with_aspects": true,
            "with_dignities": true,
            "with_dominant_elements": true
        ]
    ]
    
    let jsonData = try JSONSerialization.data(withJSONObject: requestBody)
    request.httpBody = jsonData
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let result = try JSONSerialization.jsonObject(with: data) as? [String: Any]
    
    return result ?? [:]
}
```

---

## Recommendations for Integration

### Web Applications

1. **Authentication**: Store API key securely in environment variables
2. **Caching**: Cache birth chart results to minimize API calls
3. **Error Handling**: Implement comprehensive error handling for all API calls
4. **Progressive Loading**: Show loading indicators during calculations
5. **Visualization**: Use chart.js or D3.js for visualizing astrological charts

### Mobile Applications

1. **Offline Mode**: Cache recent calculations for offline access
2. **Background Processing**: Perform lengthy calculations in background threads
3. **Permission Handling**: Request location permissions for current location calculations
4. **Battery Optimization**: Batch API requests and minimize network calls
5. **UI Responsiveness**: Use loading states and progressive disclosure

### Automation Systems

1. **Rate Limiting**: Respect API rate limits (default: 60 requests per minute)
2. **Webhook Integration**: Use webhooks for long-running calculations
3. **Idempotent Requests**: Use idempotent requests to prevent duplicate calculations
4. **Job Queuing**: Implement job queuing for batch calculations
5. **Monitoring**: Set up monitoring for API availability and response times

---

*Last Updated: March 17, 2025*