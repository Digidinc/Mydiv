# Astrology Engine API Documentation

## Overview

The Astrology Engine API provides astrological calculations and data for the MyDivinations platform. This document describes the available endpoints, their request/response formats, and usage examples.

## Base URL

```
http://localhost:8000
```

## Authentication

Authentication will be implemented in future versions.

## API Endpoints

### Currently Implemented

#### Health Check

```http
GET /health
```

Checks the health status of the service.

**Response**
```json
{
    "status": "healthy"
}
```

**Status Codes**
- 200: Service is healthy
- 503: Service is unhealthy

#### Welcome

```http
GET /
```

Returns a welcome message.

**Response**
```json
{
    "message": "Welcome to Astrology Engine API"
}
```

**Status Codes**
- 200: Success

### Planned Endpoints

The following endpoints are planned for future implementation:

#### Calculate Birth Chart

```http
POST /birth_chart
```

Will calculate a complete natal chart from birth information.

**Request Body** (planned)
```json
{
    "date": "1990-01-01",
    "time": "12:00:00",
    "latitude": 51.5074,
    "longitude": -0.1278,
    "timezone": "Europe/London"
}
```

#### Get Planetary Positions

```http
GET /planets
```

Will return positions of specified planets at a given date and time.

**Query Parameters** (planned)
```
date: YYYY-MM-DD
time: HH:MM:SS
planets: comma-separated list of planets
```

#### Calculate Aspects

```http
POST /aspects
```

Will calculate aspects between planets.

**Request Body** (planned)
```json
{
    "date": "2025-03-16",
    "time": "12:00:00",
    "aspects": ["conjunction", "opposition", "trine"],
    "orb": 2
}
```

#### Calculate Transits

```http
POST /transits
```

Will calculate current transits to natal chart.

**Request Body** (planned)
```json
{
    "birth_date": "1990-01-01",
    "birth_time": "12:00:00",
    "transit_date": "2025-03-16"
}
```

#### Calculate Progressions

```http
POST /progressions
```

Will calculate progressed chart positions.

**Request Body** (planned)
```json
{
    "birth_date": "1990-01-01",
    "birth_time": "12:00:00",
    "progression_date": "2025-03-16"
}
```

## Error Handling

### Error Response Format

```json
{
    "detail": "Error message"
}
```

### Common Error Codes

- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error
- 503: Service Unavailable

## Rate Limiting

Rate limiting will be implemented in future versions.

## Caching

Redis is integrated for caching, but specific caching strategies are yet to be implemented.

## API Versioning

API versioning will be implemented in future versions.

## Testing the API

You can test the API using curl:

```bash
# Health check
curl http://localhost:8000/health

# Welcome message
curl http://localhost:8000/
```

Or use the Swagger UI documentation at:
```
http://localhost:8000/docs
```

## Future Enhancements

1. Authentication and authorization
2. Rate limiting
3. API versioning
4. Request validation
5. Response caching
6. Comprehensive error handling
7. Detailed response schemas
8. Batch processing endpoints

---

*Last Updated: March 16, 2025 | 07:00 UTC*