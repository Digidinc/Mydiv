# Magician Service API Documentation

This document provides detailed specifications for the Magician service API endpoints. The service is hosted at `https://magician.mydivinations.com/api/v1`.

## API Overview

The Magician service provides the following API categories:

1. **User Profile Management**: Create and manage user psycho-spiritual profiles
2. **Personalized Insights**: Generate tailored interpretations and guidance
3. **Conversation**: Handle natural language interaction with the Magician
4. **Archetypal Analysis**: Analyze and map archetypal patterns
5. **Connection Management**: Manage connections with other MyDivinations services

## Authentication

All API endpoints require authentication via JWT tokens. Tokens should be included in the Authorization header:

```
Authorization: Bearer {token}
```

User authentication is handled through a separate authentication service.

## Common Response Format

All API responses follow this format:

```json
{
  "success": true|false,
  "data": {
    // Response data when success is true
  },
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional error details when available
    }
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `UNAUTHORIZED` | Authentication required or token invalid |
| `FORBIDDEN` | User does not have permission |
| `NOT_FOUND` | Requested resource not found |
| `VALIDATION_ERROR` | Request parameters invalid |
| `INTEGRATION_ERROR` | Error in external service integration |
| `PROFILE_ERROR` | Error in profile management |
| `PROCESSING_ERROR` | Error in insight generation |
| `RATE_LIMITED` | Too many requests |
| `SERVER_ERROR` | Internal server error |

## API Endpoints

### User Profile Management

#### Create User Profile

```http
POST /profiles
```

Create a new user psycho-spiritual profile.

**Request Body:**

```json
{
  "user_id": "string",
  "birth_data": {
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS",
    "location": {
      "latitude": float,
      "longitude": float,
      "location_name": "string"
    },
    "time_zone": "string"
  },
  "initial_preferences": {
    "interests": ["string"],
    "spiritual_background": "string",
    "consciousness_level": "string"
  }
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "profile_id": "string",
    "created_at": "ISO-8601 timestamp",
    "archetype_map": {
      "dominant_archetypes": [
        {
          "name": "string",
          "strength": float
        }
      ],
      "elements": {
        "fire": float,
        "earth": float,
        "air": float,
        "water": float
      },
      "modalities": {
        "cardinal": float,
        "fixed": float,
        "mutable": float
      }
    }
  }
}
```

#### Get User Profile

```http
GET /profiles/{profile_id}
```

Retrieve a user's psycho-spiritual profile.

**Response:**

```json
{
  "success": true,
  "data": {
    "profile_id": "string",
    "user_id": "string",
    "birth_data": {
      "date": "YYYY-MM-DD",
      "time": "HH:MM:SS",
      "location": {
        "latitude": float,
        "longitude": float,
        "location_name": "string"
      },
      "time_zone": "string"
    },
    "archetype_map": {
      "dominant_archetypes": [
        {
          "name": "string",
          "strength": float
        }
      ],
      "elements": {
        "fire": float,
        "earth": float,
        "air": float,
        "water": float
      },
      "modalities": {
        "cardinal": float,
        "fixed": float,
        "mutable": float
      }
    },
    "preferred_symbols": ["string"],
    "growth_areas": ["string"],
    "consciousness_trajectory": {
      "current_level": "string",
      "recent_shifts": ["string"],
      "growth_potential": ["string"]
    },
    "created_at": "ISO-8601 timestamp",
    "updated_at": "ISO-8601 timestamp"
  }
}
```

#### Update User Profile

```http
PATCH /profiles/{profile_id}
```

Update a user's psycho-spiritual profile.

**Request Body:**

```json
{
  "preferred_symbols": ["string"],
  "growth_areas": ["string"],
  "interests": ["string"],
  "consciousness_level": "string"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "profile_id": "string",
    "updated_at": "ISO-8601 timestamp"
  }
}
```

### Personalized Insights

#### Generate Transit Reading

```http
POST /insights/transit
```

Generate a personalized reading based on current transits.

**Request Body:**

```json
{
  "profile_id": "string",
  "date": "YYYY-MM-DD",
  "focus_area": "string",
  "detail_level": "brief|standard|detailed"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "insight_id": "string",
    "type": "transit",
    "title": "string",
    "content": "string",
    "significant_transits": [
      {
        "planet1": "string",
        "planet2": "string",
        "aspect": "string",
        "orb": float,
        "influence": float,
        "interpretation": "string"
      }
    ],
    "suggestions": [
      {
        "type": "practice|reflection|symbol",
        "content": "string"
      }
    ],
    "timestamp": "ISO-8601 timestamp"
  }
}
```

#### Generate Natal Chart Reading

```http
POST /insights/natal
```

Generate a personalized interpretation of a user's natal chart.

**Request Body:**

```json
{
  "profile_id": "string",
  "focus_area": "string",
  "detail_level": "brief|standard|detailed"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "insight_id": "string",
    "type": "natal",
    "title": "string",
    "content": "string",
    "significant_placements": [
      {
        "planet": "string",
        "sign": "string",
        "house": integer,
        "interpretation": "string"
      }
    ],
    "suggestions": [
      {
        "type": "practice|reflection|symbol",
        "content": "string"
      }
    ],
    "timestamp": "ISO-8601 timestamp"
  }
}
```

#### Generate Growth Forecast

```http
POST /insights/forecast
```

Generate a personalized growth forecast for a specific time period.

**Request Body:**

```json
{
  "profile_id": "string",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "focus_area": "string"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "insight_id": "string",
    "type": "forecast",
    "title": "string",
    "overview": "string",
    "periods": [
      {
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "title": "string",
        "content": "string",
        "key_transits": [
          {
            "planet1": "string",
            "planet2": "string",
            "aspect": "string",
            "date": "YYYY-MM-DD",
            "interpretation": "string"
          }
        ]
      }
    ],
    "suggestions": [
      {
        "type": "practice|reflection|symbol",
        "content": "string",
        "timing": "string"
      }
    ],
    "timestamp": "ISO-8601 timestamp"
  }
}
```

#### List User Insights

```http
GET /insights?profile_id={profile_id}&type={type}&limit={limit}&offset={offset}
```

Retrieve a list of previously generated insights for a user.

**Query Parameters:**

- `profile_id`: User profile ID (required)
- `type`: Insight type - "transit", "natal", "forecast" (optional)
- `limit`: Number of results to return (default: 10)
- `offset`: Pagination offset (default: 0)

**Response:**

```json
{
  "success": true,
  "data": {
    "insights": [
      {
        "insight_id": "string",
        "type": "string",
        "title": "string",
        "summary": "string",
        "timestamp": "ISO-8601 timestamp"
      }
    ],
    "pagination": {
      "total": integer,
      "limit": integer,
      "offset": integer
    }
  }
}
```

#### Get Insight

```http
GET /insights/{insight_id}
```

Retrieve a specific insight by ID.

**Response:**

```json
{
  "success": true,
  "data": {
    // Full insight object (varies by type)
  }
}
```

### Conversation

#### Start Conversation

```http
POST /conversations
```

Start a new conversation with the Magician.

**Request Body:**

```json
{
  "profile_id": "string",
  "context": "string",
  "focus_area": "string"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "conversation_id": "string",
    "greeting": "string",
    "suggestions": ["string"],
    "created_at": "ISO-8601 timestamp"
  }
}
```

#### Send Message

```http
POST /conversations/{conversation_id}/messages
```

Send a message to the Magician within an existing conversation.

**Request Body:**

```json
{
  "message": "string",
  "attachments": [
    {
      "type": "string",
      "content": "string"
    }
  ]
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "message_id": "string",
    "response": "string",
    "insights": [
      {
        "type": "string",
        "content": "string"
      }
    ],
    "suggestions": ["string"],
    "timestamp": "ISO-8601 timestamp"
  }
}
```

#### Get Conversation History

```http
GET /conversations/{conversation_id}/messages?limit={limit}&offset={offset}
```

Retrieve conversation history.

**Query Parameters:**

- `limit`: Number of messages to return (default: 20)
- `offset`: Pagination offset (default: 0)

**Response:**

```json
{
  "success": true,
  "data": {
    "conversation_id": "string",
    "profile_id": "string",
    "messages": [
      {
        "message_id": "string",
        "role": "user|magician",
        "content": "string",
        "timestamp": "ISO-8601 timestamp"
      }
    ],
    "pagination": {
      "total": integer,
      "limit": integer,
      "offset": integer
    }
  }
}
```

#### List Conversations

```http
GET /conversations?profile_id={profile_id}&limit={limit}&offset={offset}
```

List a user's conversations.

**Query Parameters:**

- `profile_id`: User profile ID (required)
- `limit`: Number of conversations to return (default: 10)
- `offset`: Pagination offset (default: 0)

**Response:**

```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "conversation_id": "string",
        "title": "string",
        "last_message": "string",
        "last_activity": "ISO-8601 timestamp",
        "message_count": integer
      }
    ],
    "pagination": {
      "total": integer,
      "limit": integer,
      "offset": integer
    }
  }
}
```

### Archetypal Analysis

#### Generate Archetypal Map

```http
POST /archetypes/map
```

Generate or update a user's archetypal map.

**Request Body:**

```json
{
  "profile_id": "string",
  "include_chart_data": boolean,
  "include_conversation_data": boolean
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "map_id": "string",
    "dominant_archetypes": [
      {
        "name": "string",
        "strength": float,
        "expression": "string",
        "source": "natal|transits|interactions"
      }
    ],
    "elements": {
      "fire": float,
      "earth": float,
      "air": float,
      "water": float
    },
    "modalities": {
      "cardinal": float,
      "fixed": float,
      "mutable": float
    },
    "polarities": {
      "masculine": float,
      "feminine": float
    },
    "visualization_data": {
      "nodes": [
        {
          "id": "string",
          "type": "archetype|planet|aspect",
          "value": float,
          "group": integer
        }
      ],
      "links": [
        {
          "source": "string",
          "target": "string",
          "strength": float
        }
      ]
    },
    "timestamp": "ISO-8601 timestamp"
  }
}
```

#### Get Archetypal Map History

```http
GET /archetypes/maps?profile_id={profile_id}&limit={limit}&offset={offset}
```

Retrieve the history of a user's archetypal maps to track evolution.

**Query Parameters:**

- `profile_id`: User profile ID (required)
- `limit`: Number of maps to return (default: 10)
- `offset`: Pagination offset (default: 0)

**Response:**

```json
{
  "success": true,
  "data": {
    "maps": [
      {
        "map_id": "string",
        "dominant_archetypes": [
          {
            "name": "string",
            "strength": float
          }
        ],
        "timestamp": "ISO-8601 timestamp"
      }
    ],
    "evolution": {
      "primary_shifts": [
        {
          "archetype": "string",
          "direction": "increasing|decreasing",
          "magnitude": float,
          "period": "string"
        }
      ],
      "stability_index": float
    },
    "pagination": {
      "total": integer,
      "limit": integer,
      "offset": integer
    }
  }
}
```

#### Get Archetype Information

```http
GET /archetypes/{archetype_name}
```

Get detailed information about a specific archetype.

**Response:**

```json
{
  "success": true,
  "data": {
    "name": "string",
    "description": "string",
    "keywords": ["string"],
    "associated_planets": ["string"],
    "associated_signs": ["string"],
    "shadow_aspects": ["string"],
    "growth_potential": ["string"],
    "recommendations": {
      "practices": ["string"],
      "symbols": ["string"],
      "reflections": ["string"]
    }
  }
}
```

### System

#### Health Check

```http
GET /health
```

Check the health status of the Magician service.

**Response:**

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "string",
    "dependencies": {
      "astrology_engine": "healthy|degraded|unavailable",
      "database": "healthy|degraded|unavailable",
      "vector_database": "healthy|degraded|unavailable"
    },
    "timestamp": "ISO-8601 timestamp"
  }
}
```

## Data Models

### Profile

The core user profile includes:

- Basic user information
- Birth chart data
- Archetypal makeup
- Preferences and interests
- Interaction history
- Growth trajectory

### Insight

Insights are personalized interpretations generated for users, including:

- Transit readings
- Natal chart readings
- Growth forecasts
- Specific question responses

### Conversation

Conversations represent interactive sessions with the Magician, including:

- User messages
- Magician responses
- Context and metadata
- Generated insights

### Archetype

Archetypes are foundational patterns in the collective unconscious, including:

- Core symbolic meanings
- Psychological expressions
- Astrological correspondences
- Growth potentials

## Rate Limiting

API endpoints are subject to the following rate limits:

| Endpoint | Rate Limit |
|----------|------------|
| POST /conversations/{id}/messages | 30 per minute |
| POST /insights/* | 10 per minute |
| Other endpoints | 60 per minute |

## Webhook Integration

For applications that need real-time updates, the Magician service supports webhooks:

```http
POST /webhooks
```

**Request Body:**

```json
{
  "url": "string",
  "events": ["profile.updated", "insight.generated", "conversation.message"],
  "secret": "string"
}
```

Webhook payloads will include event data and a signature header for verification.

## Integration with Other Services

The Magician service integrates with other MyDivinations services:

- **Astrology Engine**: For chart calculations and transit data
- **Authentication Service**: For user authentication and authorization
- **Game Services**: For experiences based on archetypal patterns

## Versioning

The API follows semantic versioning. The current version is v1.

---

*Last Updated: March 17, 2025*