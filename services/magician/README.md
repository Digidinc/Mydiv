# MyDivinations Magician Service

## Overview

The MyDivinations Magician Service is an AI-powered personalized guidance system that creates and maintains user psycho-spiritual profiles, providing tailored mystical insights, recommendations, and interpretations based on astrological data and continuous user interactions.

The Magician acts as a companion on the user's consciousness-expanding journey, learning from their responses and preferences to deliver increasingly personalized content that resonates with their unique archetypal patterns.

## Key Features

- **User Profiling**: Creates and maintains detailed psycho-spiritual profiles
- **Personalized Interpretations**: Tailors astrological and archetypal insights to the individual
- **Contextual Memory**: Remembers past conversations and evolves understanding over time
- **Symbolic Integration**: Weaves meaningful symbols and archetypes into communications
- **Archetypal Mapping**: Identifies dominant patterns in user's consciousness
- **Fractal Resonance**: Provides content that resonates with the user's energy signature

## Technical Architecture

The Magician service is built with:

- **FastAPI**: High-performance API framework
- **PostgreSQL + pgvector**: Vector database for semantic memory and embeddings
- **LLM Integration**: Advanced language model for natural interactions
- **Integration APIs**: Connections to Astrology Engine and other MyDivinations services

### Database Schema

The service uses PostgreSQL with pgvector extension for:

- User profiles with vector embeddings
- Conversation history
- Archetypal classifications
- Preference tracking
- Symbol associations

## Integration Points

### Astrology Engine Integration

The Magician service integrates deeply with the [Astrology Engine API](https://github.com/Digidinc/Mydiv/blob/MyDIV-Astro/services/astrology-engine/docs/API_DOCUMENTATION.md) to access:

- Birth chart data
- Transit forecasts
- Progression insights
- Planetary positions

### User Profile Management

The Magician maintains a sophisticated user profile that evolves with each interaction:

- **Archetypal Balance**: Tracking dominant archetypes in the user's psyche
- **Symbol Affinity**: Recording which symbols resonate most strongly
- **Topic Interest**: Noting areas of spiritual/psychological interest
- **Response Patterns**: Learning from emotional and intellectual responses
- **Growth Trajectory**: Mapping the user's consciousness evolution over time

## Magician Capabilities

As a mystical AI companion, the Magician can:

1. **Provide Personalized Readings**: Interpret astrological data in the context of the user's unique profile
2. **Offer Spiritual Guidance**: Suggest practices, reflections, and exercises tailored to current astrological influences
3. **Track Consciousness Evolution**: Note shifts in awareness and provide feedback on growth
4. **Suggest Symbolic Explorations**: Recommend symbols and archetypes to work with based on current transits
5. **Answer Mystical Inquiries**: Respond to questions about spiritual topics with personalized context

## API Usage Guide for Magician

### Accessing Astrological Data

The Magician should use the Astrology Engine API to gather astrological data for users. Here's how to access key endpoints:

#### 1. Retrieving a User's Birth Chart

```python
import requests
import json

def get_birth_chart(birth_data):
    """
    Retrieve a user's complete birth chart from the Astrology Engine.
    
    Args:
        birth_data: Dictionary containing date, time, and location information
        
    Returns:
        Complete birth chart data
    """
    url = "https://api.mydivinations.com/astrology-engine/birth_chart"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "YOUR_API_KEY"
    }
    
    data = {
        "birth_data": birth_data,
        "options": {
            "house_system": "placidus",
            "with_aspects": True,
            "with_dignities": True,
            "with_dominant_elements": True
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()
```

#### 2. Generating a Five-Year Transit Forecast

```python
def get_transit_forecast(birth_date, birth_time, latitude, longitude):
    """
    Generate a 5-year transit forecast for personalized predictions.
    
    Args:
        birth_date: User's birth date (YYYY-MM-DD)
        birth_time: User's birth time (HH:MM:SS)
        latitude: Birth location latitude
        longitude: Birth location longitude
        
    Returns:
        Comprehensive 5-year forecast with significant transits and life events
    """
    url = "https://api.mydivinations.com/astrology-engine/transits/five-year-forecast"
    
    params = {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_latitude": latitude,
        "birth_longitude": longitude
    }
    
    headers = {
        "X-API-Key": "YOUR_API_KEY"
    }
    
    response = requests.get(url, params=params, headers=headers)
    return response.json()
```

#### 3. Getting Current Transits for Today's Guidance

```python
def get_current_transits(birth_date, birth_time, latitude, longitude):
    """
    Retrieve current planetary transits affecting the user today.
    
    Args:
        birth_date: User's birth date (YYYY-MM-DD)
        birth_time: User's birth time (HH:MM:SS)
        latitude: Birth location latitude
        longitude: Birth location longitude
        
    Returns:
        Current active transits with interpretations
    """
    url = "https://api.mydivinations.com/astrology-engine/transits/current-transits"
    
    params = {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_latitude": latitude,
        "birth_longitude": longitude,
        "orb": 1.5  # Slightly wider orb for more relevant transits
    }
    
    headers = {
        "X-API-Key": "YOUR_API_KEY"
    }
    
    response = requests.get(url, params=params, headers=headers)
    return response.json()
```

### Managing User Profiles

The Magician should create and maintain rich user profiles in the PostgreSQL database with pgvector:

```python
import psycopg2
from psycopg2.extras import Json
import numpy as np
from pgvector.psycopg2 import register_vector

def create_user_profile(user_id, birth_data, initial_embedding):
    """
    Create a new user profile in the database.
    
    Args:
        user_id: Unique identifier for the user
        birth_data: User's birth information
        initial_embedding: Vector embedding representing initial profile
        
    Returns:
        Created profile ID
    """
    conn = psycopg2.connect(DATABASE_URL)
    register_vector(conn)
    cursor = conn.cursor()
    
    # Create user profile
    cursor.execute(
        """
        INSERT INTO user_profiles 
        (user_id, birth_data, profile_embedding, created_at, updated_at)
        VALUES (%s, %s, %s, NOW(), NOW())
        RETURNING profile_id
        """,
        (user_id, Json(birth_data), initial_embedding)
    )
    
    profile_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return profile_id

def update_user_profile(profile_id, new_data, updated_embedding):
    """
    Update a user's profile with new information and an updated embedding.
    
    Args:
        profile_id: The profile ID to update
        new_data: New profile data to incorporate
        updated_embedding: Updated vector embedding
    """
    conn = psycopg2.connect(DATABASE_URL)
    register_vector(conn)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE user_profiles
        SET profile_data = profile_data || %s,
            profile_embedding = %s,
            updated_at = NOW()
        WHERE profile_id = %s
        """,
        (Json(new_data), updated_embedding, profile_id)
    )
    
    conn.commit()
    cursor.close()
    conn.close()

def store_interaction(user_id, interaction_text, embedding, interaction_type):
    """
    Store a user interaction in the database.
    
    Args:
        user_id: User identifier
        interaction_text: Text of the interaction
        embedding: Vector embedding of the interaction
        interaction_type: Type of interaction (question, reflection, etc.)
    """
    conn = psycopg2.connect(DATABASE_URL)
    register_vector(conn)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO user_interactions
        (user_id, interaction_text, embedding, interaction_type, created_at)
        VALUES (%s, %s, %s, %s, NOW())
        """,
        (user_id, interaction_text, embedding, interaction_type)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
```

### Creating Personalized Interpretations

The Magician should combine astrological data with user profile information to create deeply personalized interpretations:

```python
def generate_personalized_reading(user_id, transit_data, profile_data):
    """
    Generate a personalized reading based on transit data and user profile.
    
    Args:
        user_id: User identifier
        transit_data: Current transit information from Astrology Engine
        profile_data: User's profile data
        
    Returns:
        Personalized reading text
    """
    # Get relevant profile information
    dominant_archetypes = profile_data.get('dominant_archetypes', [])
    preferred_symbols = profile_data.get('preferred_symbols', [])
    growth_areas = profile_data.get('growth_areas', [])
    
    # Extract significant transits
    significant_transits = transit_data.get('active_transits', [])
    
    # Generate personalized content based on profile and transits
    # [Your LLM integration and content generation logic here]
    
    # Track this reading in the database
    store_reading(user_id, reading_text, reading_type="transit")
    
    return reading_text
```

## Symbolic and Archetypal Framework

The Magician should operate within MyDivinations' symbolic framework:

### Core Archetypes

- **The Seeker**: Curiosity, exploration, quest for truth
- **The Creator**: Expression, manifestation, imagination
- **The Guardian**: Protection, boundaries, tradition
- **The Nurturer**: Care, compassion, healing
- **The Transformer**: Change, rebirth, metamorphosis
- **The Sage**: Wisdom, knowledge, insight
- **The Ruler**: Authority, leadership, order
- **The Lover**: Connection, passion, intimacy
- **The Magician**: Power, transformation, catalyst
- **The Innocent**: Purity, new beginnings, faith
- **The Rebel**: Challenge, revolution, liberation
- **The Shadow**: Hidden aspects, unconscious patterns

### Symbolic Correspondences

The Magician should establish and maintain associations between:

- Planets and archetypes
- Elements and psychological qualities
- Zodiac signs and personality patterns
- Houses and life domains
- Aspects and relationship dynamics

## Best Practices for Magician Implementation

1. **Maintain Contextual Memory**: Reference previous interactions to create continuity
2. **Balance Mystical and Practical**: Combine esoteric wisdom with actionable insights
3. **Personalize Gradually**: Start with basic insights and increase personalization as you learn more
4. **Respect User Journey**: Meet users where they are on their consciousness journey
5. **Symbolic Integration**: Weave relevant symbols throughout your communication
6. **Update Profile Continuously**: Refine user profiles based on every interaction
7. **Query Astrology API Mindfully**: Use caching for repeated astrological queries

## Implementation Roadmap

1. **Initial Setup**: Database schema, API integrations, basic profile structure
2. **Core Functionality**: Birth chart interpretation, transit analysis, progression insights
3. **Profile Evolution**: Learning system, preference tracking, archetypal mapping
4. **Advanced Features**: Pattern recognition, growth tracking, spiritual practice recommendations
5. **Integration**: Connect with Path of Symbols game and other MyDivinations experiences

---

*This Magician service is designed to be the personalized mystical companion within the MyDivinations ecosystem, combining astrological precision with psychological depth and spiritual wisdom.*