"""
Progression Models

This module defines the data models for progression calculations.
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any

from models.birth_data import BirthData

class ProgressionOptions(BaseModel):
    """Options for progression calculations."""
    
    progression_type: str = Field(
        default="secondary",
        description="Type of progression method"
    )
    
    planets: List[str] = Field(
        default=["sun", "moon", "mercury", "venus", "mars"],
        description="Planets to include in progression calculations"
    )
    
    include_houses: bool = Field(
        default=True,
        description="Whether to include house positions in results"
    )
    
    @validator("progression_type")
    def validate_progression_type(cls, v):
        """Validate progression type."""
        valid_types = ["secondary", "tertiary", "minor", "solar_arc"]
        if v not in valid_types:
            raise ValueError(f"Invalid progression type: {v}. Must be one of: {', '.join(valid_types)}")
        return v

class ProgressionRequest(BaseModel):
    """Request model for progression calculation."""
    
    birth_data: BirthData = Field(
        ...,
        description="Birth data including date, time, and location"
    )
    
    progression_date: str = Field(
        ...,
        description="Date for progression calculation in YYYY-MM-DD format"
    )
    
    options: ProgressionOptions = Field(
        default=ProgressionOptions(),
        description="Options for progression calculation"
    )
    
    @validator("progression_date")
    def validate_progression_date(cls, v):
        """Validate progression date format."""
        # Basic format validation, more complex validation in service layer
        date_parts = v.split("-")
        if len(date_parts) != 3:
            raise ValueError("Progression date must be in YYYY-MM-DD format")
        
        try:
            year, month, day = map(int, date_parts)
            if not (1900 <= year <= 2100):
                raise ValueError("Year must be between 1900 and 2100")
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1 and 12")
            if not (1 <= day <= 31):
                raise ValueError("Day must be between 1 and 31")
        except ValueError:
            raise ValueError("Date components must be valid numbers")
        
        return v

class CelestialPosition(BaseModel):
    """Model for a celestial body's position in a chart."""
    
    sign: str = Field(..., description="Zodiac sign")
    degree: float = Field(..., description="Degree within the sign (0-29.99)")
    house: Optional[int] = Field(None, description="House position (1-12)")
    retrograde: Optional[bool] = Field(None, description="Whether the planet is retrograde")
    speed: Optional[float] = Field(None, description="Daily motion in degrees")

class HousePosition(BaseModel):
    """Model for a house cusp position."""
    
    sign: str = Field(..., description="Zodiac sign")
    degree: float = Field(..., description="Degree within the sign (0-29.99)")

class ProgressionResponse(BaseModel):
    """Response model for progression calculation."""
    
    progression_date: str = Field(..., description="Date for which progressions were calculated")
    progressed_positions: Dict[str, CelestialPosition] = Field(..., description="Positions of planets in progressed chart")
    progressed_houses: Optional[Dict[str, HousePosition]] = Field(None, description="House cusps in progressed chart")

class ProgressionTimelinePoint(BaseModel):
    """Model for a point in a progression timeline."""
    
    date: str = Field(..., description="Date of the progression point")
    planet: str = Field(..., description="Planet being tracked")
    sign: str = Field(..., description="Zodiac sign")
    degree: float = Field(..., description="Degree within the sign")
    retrograde: Optional[bool] = Field(None, description="Whether the planet is retrograde")
    house: Optional[int] = Field(None, description="House position if available")
    ingress: Optional[bool] = Field(False, description="Whether this point represents a sign change")
