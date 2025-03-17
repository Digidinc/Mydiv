"""
Aspect Models

This module defines the data models for aspect calculations.
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any

class AspectOptions(BaseModel):
    """Options for aspect calculations."""
    
    aspects: List[str] = Field(
        default=["conjunction", "opposition", "trine", "square", "sextile"],
        description="Types of aspects to calculate"
    )
    
    orbs: Dict[str, float] = Field(
        default={
            "conjunction": 8.0,
            "opposition": 8.0,
            "trine": 6.0,
            "square": 6.0,
            "sextile": 4.0
        },
        description="Maximum orb (in degrees) for each aspect type"
    )
    
    @validator("aspects")
    def validate_aspects(cls, v):
        """Validate aspect types."""
        valid_aspects = [
            "conjunction", "opposition", "trine", "square", "sextile",
            "quincunx", "semi_sextile", "semi_square", "sesquiquadrate", "quintile"
        ]
        
        for aspect in v:
            if aspect not in valid_aspects:
                raise ValueError(f"Invalid aspect type: {aspect}")
        
        return v

class AspectRequest(BaseModel):
    """Request model for aspect calculation."""
    
    planet_positions: Dict[str, float] = Field(
        ...,
        description="Dictionary of planet names and their longitudes in degrees"
    )
    
    options: AspectOptions = Field(
        default=AspectOptions(),
        description="Options for aspect calculation"
    )
    
    @validator("planet_positions")
    def validate_planet_positions(cls, v):
        """Validate planet positions."""
        if not v:
            raise ValueError("At least one planet position must be provided")
        
        for planet, longitude in v.items():
            if not isinstance(longitude, (int, float)):
                raise ValueError(f"Longitude for {planet} must be a number")
            
            if longitude < 0 or longitude >= 360:
                raise ValueError(f"Longitude for {planet} must be between 0 and 359.99 degrees")
        
        return v

class Aspect(BaseModel):
    """Model for an astrological aspect."""
    
    planet1: str = Field(..., description="First celestial body")
    planet2: str = Field(..., description="Second celestial body")
    type: str = Field(..., description="Aspect type (conjunction, opposition, etc.)")
    orb: float = Field(..., description="Orb in degrees")
    applying: bool = Field(..., description="Whether the aspect is applying or separating")
    influence: float = Field(..., description="Strength of influence (0-1)")
    exact_date: Optional[str] = Field(None, description="Date when the aspect is exact (if applicable)")

class AspectResponse(BaseModel):
    """Response model for aspect calculation."""
    
    aspects: List[Aspect] = Field(..., description="List of calculated aspects")

class AspectConfigRequest(BaseModel):
    """Configuration for aspect calculations between planets."""
    
    planets1: List[str] = Field(..., description="First set of planets")
    planets2: Optional[List[str]] = Field(None, description="Second set of planets (if different from first)")
    aspects: List[str] = Field(
        default=["conjunction", "opposition", "trine", "square", "sextile"],
        description="Types of aspects to calculate"
    )
    orbs: Dict[str, float] = Field(
        default={
            "conjunction": 5.0,
            "opposition": 5.0,
            "trine": 4.0,
            "square": 4.0,
            "sextile": 3.0
        },
        description="Maximum orb (in degrees) for each aspect type"
    )
