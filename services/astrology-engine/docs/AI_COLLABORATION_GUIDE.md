# AI Collaboration Guide for Astrology Engine

This guide is designed to help AI coding assistants (like Cursor AI) contribute effectively to the MyDivinations Astrology Engine. It outlines the project structure, coding standards, and specific tasks that AI assistants should focus on.

## Project Overview

The Astrology Engine is a FastAPI-based service that provides astrological calculations using the Swiss Ephemeris library. It serves as the backend for the MyDivinations platform, offering functionality for birth charts, planetary positions, aspects, transits, and progressions.

## Key Components

1. **API Endpoints** (`src/api/`): FastAPI route definitions
2. **Core Calculations** (`src/core/`): Swiss Ephemeris wrapper and calculation engine
3. **Data Models** (`src/models/`): Pydantic models for request/response validation
4. **Business Logic** (`src/services/`): Service layer implementations
5. **Configuration** (`src/config.py`): Application settings

## Coding Standards

When working on the project, follow these guidelines:

### Python Style

- Use PEP 8 guidelines
- Type hints for all function parameters and return types
- Docstrings for all functions, classes, and modules
- Async/await for I/O-bound operations

### Structure

- Maintain separation of concerns between API, services, and models
- Keep endpoints clean by moving business logic to service layer
- Use dependency injection for services

### Error Handling

- Use structured error responses
- Validate input data with Pydantic models
- Include appropriate HTTP status codes
- Log errors with context information

### Astrology-Specific Guidelines

- Follow astrological conventions for calculations
- Comment complex astrological formulas for clarity
- Include source references for specialized calculations
- Handle edge cases (retrograde planets, aspect patterns, etc.)

## Tasks for AI Assistance

AI assistants can help with the following tasks:

### 1. Code Implementation

```python
# Example task: Implement a service method to calculate planetary ingress
async def calculate_planet_ingress(
    self,
    planet: str,
    start_date: str,
    end_date: Optional[str] = None,
    signs: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Calculate when a planet enters new zodiac signs.
    
    Args:
        planet: Planet name
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format (defaults to 1 year from start)
        signs: List of specific signs to check (defaults to all)
        
    Returns:
        List of ingress events with dates and signs
    """
    # Your implementation here
```

### 2. Optimization

```python
# Example task: Optimize transit calculations for long date ranges
# Original (inefficient) approach:
for i in range(days):
    current_date = start_date + timedelta(days=i)
    # Calculate planets for each day
    
# Optimized approach:
# 1. Sample at larger intervals (e.g., weekly)
# 2. Use binary search to find exact transit dates
# 3. Implement caching for repeated calculations
```

### 3. Testing

```python
# Example task: Write test cases for aspect calculations
async def test_aspect_calculation():
    # Given: Two planets at specific longitudes
    planet_positions = {
        "sun": 0.0,     # 0° Aries
        "moon": 90.0,   # 0° Cancer (90° from Sun)
    }
    
    # When: Calculating aspects
    aspects = await aspect_service.calculate_aspects(
        planet_positions=planet_positions,
        options={"aspects": ["square"], "orbs": {"square": 6.0}}
    )
    
    # Then: Should find a square aspect
    assert len(aspects) == 1
    assert aspects[0]["type"] == "square"
    assert aspects[0]["planet1"] == "sun"
    assert aspects[0]["planet2"] == "moon"
```

### 4. Documentation

```python
# Example task: Improve API documentation with examples
@router.post("/aspects", response_model=AspectResponse)
async def calculate_aspects(request: AspectRequest):
    """
    Calculate aspects between planetary positions.
    
    This endpoint detects astrological aspects (angular relationships) between planets
    based on their zodiacal longitudes.
    
    ### Parameters:
    - **planet_positions**: Dictionary mapping planet names to longitudes (0-359.99)
    - **options**: Configuration for aspect types and orbs
    
    ### Returns:
    A list of detected aspects with details about type, orb, and influence
    
    ### Example Request:
    ```json
    {
      "planet_positions": {
        "sun": 0.0,
        "moon": 90.0,
        "venus": 60.0
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
    """
```

## Common Astrological Calculations

For reference, here are some common calculations that AI assistants should understand:

### Zodiac Signs

```
Sign index = floor(longitude / 30)
Degree within sign = longitude % 30
```

### Aspects

```
Angular difference = abs(longitude1 - longitude2)
If angular difference > 180:
    angular difference = 360 - angular difference

# Check aspect:
is_aspect = abs(angular difference - aspect_angle) <= orb
```

### House Determination

```
# For Placidus and similar house systems, use Swiss Ephemeris
houses, ascmc = swe.houses(jd, lat, lng, hsys)

# Determine house for a planet:
for i in range(12):
    house_num = i + 1
    next_house = (i + 1) % 12 + 1
    
    if house_cusps[house_num] <= planet_longitude < house_cusps[next_house]:
        return house_num
```

## Collaborating with Human Developers

When collaborating with human developers:

1. Generate complete, runnable code
2. Explain complex astrological concepts when implementing them
3. Highlight potential edge cases or limitations
4. Provide performance considerations for computationally intensive calculations
5. Suggest alternative implementations where appropriate

## Requesting Human Input

When you need more information, be specific about what you need:

```
# I need more information about:
1. What house system should be used as default? (Placidus, Koch, etc.)
2. Should aspects between specific planets have different orbs?
3. What date range should be used for transit forecasts?
```

## Testing Your Code

You can verify your calculations against these reference values:

```
# Sun position on January 1, 2025, 12:00 UTC
Expected: ~280.5° (Capricorn)

# Moon position on January 1, 2025, 12:00 UTC
Expected: ~138° (Leo)

# Ascendant for January 1, 2025, 12:00 UTC, New York (40.7128° N, 74.0060° W)
Expected: ~7° (Aries)
```

By following this guide, AI assistants can effectively contribute to the MyDivinations Astrology Engine project while maintaining consistency with the project's standards and requirements.
