"""
Transit Models

This module defines the data models for transit calculations.
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any

class TimePoint(BaseModel):
    """Model for a specific point in time."""
    
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    time: str = Field("12:00:00", description="Time in HH:MM:SS format")
    time_zone: Optional[str] = Field("UTC", description="Time zone name or offset")
    
    @validator("date")
    def validate_date(cls, v):
        """Validate date format."""
        # Basic format validation, more complex validation in service layer
        date_parts = v.split("-")
        if len(date_parts) != 3:
            raise ValueError("Date must be in YYYY-MM-DD format")
        
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

class TransitOptions(BaseModel):
    """Options for transit calculations."""
    
    aspects: List[str] = Field(
        default=["conjunction", "opposition", "trine", "square", "sextile"],
        description="Types of aspects to consider for transits"
    )
    
    orbs: Dict[str, float] = Field(
        default={
            "conjunction": 1.5,
            "opposition": 1.5,
            "trine": 1.0,
            "square": 1.0,
            "sextile": 0.8
        },
        description="Maximum orb (in degrees) for each aspect type"
    )
    
    planets: List[str] = Field(
        default=["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"],
        description="Planets to include in transit calculations"
    )

class TransitRequest(BaseModel):
    """Request model for transit calculation."""
    
    natal_positions: Dict[str, float] = Field(
        ...,
        description="Dictionary of natal planet names and their longitudes in degrees"
    )
    
    transit_time: TimePoint = Field(
        ...,
        description="Time point for transit calculation"
    )
    
    options: TransitOptions = Field(
        default=TransitOptions(),
        description="Options for transit calculation"
    )

class Transit(BaseModel):
    """Model for a transit aspect."""
    
    transit_planet: str = Field(..., description="Transiting planet")
    natal_planet: str = Field(..., description="Natal planet being aspected")
    aspect: str = Field(..., description="Aspect type (conjunction, opposition, etc.)")
    orb: float = Field(..., description="Orb in degrees")
    applying: bool = Field(..., description="Whether the transit is applying or separating")
    exact_date: Optional[str] = Field(None, description="Date when the transit is exact")
    influence: float = Field(..., description="Strength of influence (0-1)")

class TransitResponse(BaseModel):
    """Response model for transit calculation."""
    
    transit_date: str = Field(..., description="Date for which transits were calculated")
    transits: List[Transit] = Field(..., description="List of calculated transits")

class TransitPeriodRequest(BaseModel):
    """Request model for calculating transits over a period."""
    
    natal_positions: Dict[str, float] = Field(
        ...,
        description="Dictionary of natal planet names and their longitudes in degrees"
    )
    
    start_date: str = Field(
        ...,
        description="Start date for transit calculation in YYYY-MM-DD format"
    )
    
    end_date: str = Field(
        ...,
        description="End date for transit calculation in YYYY-MM-DD format"
    )
    
    planets: List[str] = Field(
        default=["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"],
        description="Transit planets to include in calculations"
    )
    
    aspects: List[str] = Field(
        default=["conjunction", "opposition", "trine", "square", "sextile"],
        description="Aspect types to include in calculations"
    )
    
    orbs: Dict[str, float] = Field(
        default={
            "conjunction": 1.0,
            "opposition": 1.0,
            "trine": 0.8,
            "square": 0.8,
            "sextile": 0.6
        },
        description="Maximum orb (in degrees) for each aspect type"
    )

class TransitEvent(BaseModel):
    """Model for a transit event in a timeline."""
    
    date: str = Field(..., description="Date of the transit event")
    transit_planet: str = Field(..., description="Transiting planet")
    natal_planet: str = Field(..., description="Natal planet being aspected")
    aspect: str = Field(..., description="Aspect type")
    applying: bool = Field(..., description="Whether the transit is applying or separating when exact")
    planet_retrograde: bool = Field(False, description="Whether the transit planet is retrograde")
    description: Optional[str] = Field(None, description="Description of the transit's significance")

class TransitPeriodResponse(BaseModel):
    """Response model for transit period calculation."""
    
    start_date: str = Field(..., description="Start date of the calculation period")
    end_date: str = Field(..., description="End date of the calculation period")
    transit_timeline: List[TransitEvent] = Field(..., description="Timeline of transit events")
