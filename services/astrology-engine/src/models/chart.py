"""
Chart Models

This module defines Pydantic models for astrological charts and related data.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import UUID

from .birth_data import BirthData

class PlanetPosition(BaseModel):
    """Model for a celestial body's position in a chart."""
    
    sign: str = Field(..., description="Zodiac sign (Aries, Taurus, etc.)")
    degree: float = Field(..., description="Degree within the sign (0-29.99)")
    longitude: float = Field(..., description="Absolute longitude (0-359.99)")
    latitude: Optional[float] = Field(None, description="Celestial latitude")
    declination: Optional[float] = Field(None, description="Declination")
    speed: Optional[float] = Field(None, description="Daily motion in degrees")
    house: Optional[int] = Field(None, description="House position (1-12)")
    retrograde: Optional[bool] = Field(None, description="Whether the planet is retrograde")
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "sign": "Gemini",
                "degree": 24.83,
                "longitude": 84.83,
                "latitude": 1.2,
                "declination": 20.5,
                "speed": 0.9824,
                "house": 10,
                "retrograde": False
            }
        }

class Aspect(BaseModel):
    """Model for an aspect between two celestial bodies."""
    
    planet1: str = Field(..., description="First celestial body")
    planet2: str = Field(..., description="Second celestial body")
    type: str = Field(..., description="Aspect type (conjunction, opposition, etc.)")
    orb: float = Field(..., description="Orb in degrees")
    applying: bool = Field(..., description="Whether the aspect is applying or separating")
    influence: float = Field(..., description="Strength of influence (0-1)")
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "planet1": "sun",
                "planet2": "moon",
                "type": "trine",
                "orb": 2.3,
                "applying": False,
                "influence": 0.85
            }
        }

class HouseCusp(BaseModel):
    """Model for a house cusp in a chart."""
    
    sign: str = Field(..., description="Zodiac sign")
    degree: float = Field(..., description="Degree within the sign (0-29.99)")
    longitude: float = Field(..., description="Absolute longitude (0-359.99)")
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "sign": "Leo",
                "degree": 15.27,
                "longitude": 135.27
            }
        }

class ElementBalance(BaseModel):
    """Model for element balance in a chart."""
    
    fire: float = Field(..., description="Fire element percentage (0-100)")
    earth: float = Field(..., description="Earth element percentage (0-100)")
    air: float = Field(..., description="Air element percentage (0-100)")
    water: float = Field(..., description="Water element percentage (0-100)")
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "fire": 35,
                "earth": 15,
                "air": 20,
                "water": 30
            }
        }

class ModalityBalance(BaseModel):
    """Model for modality balance in a chart."""
    
    cardinal: float = Field(..., description="Cardinal modality percentage (0-100)")
    fixed: float = Field(..., description="Fixed modality percentage (0-100)")
    mutable: float = Field(..., description="Mutable modality percentage (0-100)")
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "cardinal": 40,
                "fixed": 30,
                "mutable": 30
            }
        }

class ChartSummary(BaseModel):
    """Model for a summary of a chart's key features."""
    
    sun_sign: str = Field(..., description="Sun sign")
    moon_sign: str = Field(..., description="Moon sign")
    ascendant: str = Field(..., description="Ascendant sign")
    dominant_element: str = Field(..., description="Dominant element")
    dominant_modality: str = Field(..., description="Dominant modality")
    dominant_planet: Optional[str] = Field(None, description="Dominant planet")
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "sun_sign": "Gemini",
                "moon_sign": "Libra",
                "ascendant": "Leo",
                "dominant_element": "Fire",
                "dominant_modality": "Cardinal",
                "dominant_planet": "Sun"
            }
        }

class ChartResponse(BaseModel):
    """Model for a complete birth chart response."""
    
    chart_id: Optional[str] = Field(None, description="Unique identifier for the chart")
    created_at: Optional[datetime] = Field(None, description="Time when chart was created")
    birth_data: BirthData = Field(..., description="Birth data used for calculation")
    summary: ChartSummary = Field(..., description="Summary of chart features")
    planets: Dict[str, PlanetPosition] = Field(..., description="Planetary positions")
    houses: Dict[int, HouseCusp] = Field(..., description="House cusps")
    aspects: Optional[List[Aspect]] = Field(None, description="Aspects between planets")
    element_balance: Optional[ElementBalance] = Field(None, description="Element balance percentages")
    modality_balance: Optional[ModalityBalance] = Field(None, description="Modality balance percentages")
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "chart_id": "chart-456",
                "created_at": "2025-03-15T15:23:45Z",
                "birth_data": {
                    "date": "1990-06-15",
                    "time": "14:25:00",
                    "location": {
                        "latitude": 34.0522,
                        "longitude": -118.2437,
                        "altitude": 71,
                        "location_name": "Los Angeles, CA"
                    },
                    "time_zone": "America/Los_Angeles"
                },
                "summary": {
                    "sun_sign": "Gemini",
                    "moon_sign": "Libra",
                    "ascendant": "Leo",
                    "dominant_element": "Fire",
                    "dominant_modality": "Cardinal",
                    "dominant_planet": "Sun"
                },
                "planets": {
                    "sun": {
                        "sign": "Gemini",
                        "degree": 24.83,
                        "longitude": 84.83,
                        "house": 10,
                        "retrograde": False
                    },
                    "moon": {
                        "sign": "Libra",
                        "degree": 22.53,
                        "longitude": 202.53,
                        "house": 2,
                        "retrograde": False
                    }
                },
                "houses": {
                    "1": {
                        "sign": "Leo",
                        "degree": 15.27,
                        "longitude": 135.27
                    },
                    "2": {
                        "sign": "Virgo",
                        "degree": 10.45,
                        "longitude": 160.45
                    }
                },
                "aspects": [
                    {
                        "planet1": "sun",
                        "planet2": "moon",
                        "type": "trine",
                        "orb": 2.3,
                        "applying": False,
                        "influence": 0.85
                    }
                ],
                "element_balance": {
                    "fire": 35,
                    "earth": 15,
                    "air": 20,
                    "water": 30
                },
                "modality_balance": {
                    "cardinal": 40,
                    "fixed": 30,
                    "mutable": 30
                }
            }
        }
