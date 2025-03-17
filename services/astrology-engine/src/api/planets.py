"""
Planets API Router

This module defines the API endpoints for planetary positions.
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from loguru import logger
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# Import services
from services.ephemeris import EphemerisService

# Create router
router = APIRouter()

# Service instance
ephemeris_service = EphemerisService()

@router.get("/", response_model=Dict[str, Any])
async def get_planetary_positions(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    time: Optional[str] = Query(None, description="Time in HH:MM:SS format (defaults to 12:00:00)"),
    latitude: Optional[float] = Query(None, description="Observer's latitude (optional)"),
    longitude: Optional[float] = Query(None, description="Observer's longitude (optional)"),
    planets: Optional[str] = Query(None, description="Comma-separated list of planets (defaults to all)")
):
    """
    Get positions of planets at a given date and time.
    
    This endpoint calculates the positions of celestial bodies at the specified
    date and time, optionally from the perspective of a specific location.
    
    Returns the positions with zodiac sign, degrees, and other astronomical data.
    """
    try:
        logger.info(f"Getting planetary positions for date: {date}, time: {time}")
        
        # Parse planets list if provided
        planet_list = None
        if planets:
            planet_list = [p.strip() for p in planets.split(",")]
        
        # Set default time if not provided
        if not time:
            time = "12:00:00"
        
        # Calculate positions
        positions = await ephemeris_service.calculate_planet_positions(
            date=date,
            time=time,
            latitude=latitude,
            longitude=longitude,
            planets=planet_list
        )
        
        logger.info(f"Planetary positions calculation completed")
        return {
            "date": date,
            "time": time,
            "planets": positions
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for planetary positions: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating planetary positions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating planetary positions", "code": "CALCULATION_ERROR"}
        )

@router.get("/position-at-date", response_model=Dict[str, Any])
async def get_planet_position_at_date(
    planet: str = Query(..., description="Planet name (sun, moon, mercury, etc.)"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format (defaults to start_date)"),
    interval_days: Optional[int] = Query(1, description="Interval between calculations in days")
):
    """
    Get positions of a specific planet over a date range.
    
    This endpoint calculates the position of a celestial body at regular intervals
    over a specified date range. Useful for tracking planetary movements over time.
    
    Returns a list of positions with dates.
    """
    try:
        logger.info(f"Getting {planet} positions from {start_date} to {end_date or start_date}")
        
        # Validate dates
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = start
            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        
        if start > end:
            raise ValueError("Start date must be before or equal to end date")
        
        # Calculate positions
        positions = await ephemeris_service.calculate_planet_position_range(
            planet=planet,
            start_date=start_date,
            end_date=end_date or start_date,
            interval_days=interval_days
        )
        
        logger.info(f"Planet position range calculation completed")
        return {
            "planet": planet,
            "start_date": start_date,
            "end_date": end_date or start_date,
            "interval_days": interval_days,
            "positions": positions
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for planet position range: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating planet position range: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating planet positions", "code": "CALCULATION_ERROR"}
        )

@router.get("/ingress", response_model=Dict[str, Any])
async def get_planet_ingress(
    planet: str = Query(..., description="Planet name (sun, moon, mercury, etc.)"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format (defaults to 1 year from start)"),
    signs: Optional[str] = Query(None, description="Comma-separated list of signs to check ingress into (defaults to all)")
):
    """
    Get the dates when a planet enters new zodiac signs.
    
    This endpoint calculates when a planet moves from one zodiac sign to another
    within a specified date range.
    
    Returns a list of ingress events with dates and signs.
    """
    try:
        logger.info(f"Getting {planet} ingress dates from {start_date} to {end_date or 'one year from start'}")
        
        # Parse signs list if provided
        sign_list = None
        if signs:
            sign_list = [s.strip() for s in signs.split(",")]
        
        # Calculate ingress dates
        ingress_dates = await ephemeris_service.calculate_planet_ingress(
            planet=planet,
            start_date=start_date,
            end_date=end_date,
            signs=sign_list
        )
        
        logger.info(f"Planet ingress calculation completed")
        return {
            "planet": planet,
            "start_date": start_date,
            "end_date": end_date,
            "ingress_events": ingress_dates
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for planet ingress: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating planet ingress: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating planet ingress", "code": "CALCULATION_ERROR"}
        )
