"""
Birth Data Models

This module defines Pydantic models for birth data used in astrological calculations.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
import re

class GeoLocation(BaseModel):
    """Geographic location model for birth location."""
    
    latitude: float = Field(..., description="Latitude in decimal degrees", ge=-90, le=90)
    longitude: float = Field(..., description="Longitude in decimal degrees", ge=-180, le=180)
    altitude: Optional[float] = Field(0, description="Altitude in meters")
    location_name: Optional[str] = Field(None, description="Human-readable location name")
    
    @validator('latitude')
    def validate_latitude(cls, v):
        """Validate latitude is within valid range."""
        if v < -90 or v > 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        """Validate longitude is within valid range."""
        if v < -180 or v > 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return v
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "latitude": 34.0522,
                "longitude": -118.2437,
                "altitude": 71,
                "location_name": "Los Angeles, CA"
            }
        }

class BirthData(BaseModel):
    """Birth data model for astrological calculations."""
    
    date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    time: str = Field(..., description="Birth time in HH:MM:SS format (24-hour)")
    location: GeoLocation = Field(..., description="Birth location")
    time_zone: str = Field(..., description="Time zone identifier (e.g., 'America/Los_Angeles')")
    
    @validator('date')
    def validate_date(cls, v):
        """Validate date format is YYYY-MM-DD."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        
        # Check year is within valid range for ephemeris calculations (1800-2399)
        year = int(v.split("-")[0])
        if year < 1800 or year > 2399:
            raise ValueError("Year must be between 1800 and 2399 for accurate calculations")
        
        return v
    
    @validator('time')
    def validate_time(cls, v):
        """Validate time format is HH:MM:SS."""
        time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$')
        if not time_pattern.match(v):
            raise ValueError("Time must be in HH:MM:SS format (24-hour)")
        return v
    
    @validator('time_zone')
    def validate_time_zone(cls, v):
        """Validate time zone is in valid format."""
        # Basic format validation, complete validation would require a timezone database
        if '/' not in v and v not in ['UTC', 'GMT']:
            raise ValueError("Time zone must be a valid IANA time zone identifier (e.g., 'America/Los_Angeles')")
        return v
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "date": "1990-06-15",
                "time": "14:25:00",
                "location": {
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                    "altitude": 71,
                    "location_name": "Los Angeles, CA"
                },
                "time_zone": "America/Los_Angeles"
            }
        }

class ChartOptions(BaseModel):
    """Options for chart calculation."""
    
    house_system: str = Field("placidus", description="House system to use for calculations")
    with_aspects: bool = Field(True, description="Whether to calculate aspects between planets")
    with_dignities: bool = Field(False, description="Whether to calculate essential dignities")
    with_dominant_elements: bool = Field(True, description="Whether to calculate dominant elements")
    with_dominant_modalities: bool = Field(True, description="Whether to calculate dominant modalities")
    
    @validator('house_system')
    def validate_house_system(cls, v):
        """Validate house system is supported."""
        valid_systems = ["placidus", "koch", "campanus", "regiomontanus", "equal", "whole_sign", "porphyry"]
        if v.lower() not in valid_systems:
            raise ValueError(f"House system must be one of: {', '.join(valid_systems)}")
        return v.lower()
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
                "house_system": "placidus",
                "with_aspects": True,
                "with_dignities": False,
                "with_dominant_elements": True,
                "with_dominant_modalities": True
            }
        }

class BirthDataRequest(BaseModel):
    """Request model for birth chart calculation."""
    
    birth_data: BirthData = Field(..., description="Birth data for chart calculation")
    options: ChartOptions = Field(default_factory=ChartOptions, description="Options for chart calculation")
    
    class Config:
        """Configuration for the model."""
        json_schema_extra = {
            "example": {
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
                "options": {
                    "house_system": "placidus",
                    "with_aspects": True,
                    "with_dignities": False,
                    "with_dominant_elements": True,
                    "with_dominant_modalities": True
                }
            }
        }
