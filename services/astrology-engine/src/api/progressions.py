"""
Progressions API Router

This module defines the API endpoints for progression calculations.
"""
from fastapi import APIRouter, HTTPException, Body, Query
from loguru import logger
from typing import Dict, Any, List, Optional

# Import models
from models.progressions import ProgressionRequest, ProgressionResponse

# Import services
from services.progressions import ProgressionService

# Create router
router = APIRouter()

# Service instance
progression_service = ProgressionService()

@router.post("/", response_model=ProgressionResponse)
async def calculate_progressions(request: ProgressionRequest):
    """
    Calculate progressed chart positions.
    
    This endpoint calculates the positions of planets in a progressed chart
    for a specific progression date, using the birth chart as the base.
    
    Supports various progression methods, with secondary progressions as the default.
    
    Returns the planetary positions and house cusps in the progressed chart.
    """
    try:
        logger.info(f"Calculating progressions for date: {request.progression_date}")
        
        # Call service to calculate progressions
        progressed_chart = await progression_service.calculate_progressions(
            birth_data=request.birth_data,
            progression_date=request.progression_date,
            options=request.options
        )
        
        logger.info(f"Progressions calculation completed")
        return {
            "progression_date": request.progression_date,
            "progressed_positions": progressed_chart["positions"],
            "progressed_houses": progressed_chart.get("houses")
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for progressions calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating progressions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating progressions", "code": "CALCULATION_ERROR"}
        )

@router.get("/secondary", response_model=Dict[str, Any])
async def calculate_secondary_progressions(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: Optional[str] = Query(None, description="Birth time in HH:MM:SS format"),
    birth_latitude: Optional[float] = Query(None, description="Birth location latitude"),
    birth_longitude: Optional[float] = Query(None, description="Birth location longitude"),
    progression_date: str = Query(..., description="Progression date in YYYY-MM-DD format"),
    planets: Optional[str] = Query(None, description="Comma-separated list of planets to include (defaults to all)")
):
    """
    Calculate secondary progressions for a given birth chart.
    
    This simplified endpoint calculates secondary progressions (where each day after
    birth corresponds to one year of life) for a specified progression date.
    
    Returns the positions of planets in the progressed chart.
    """
    try:
        logger.info(f"Calculating secondary progressions for birth date: {birth_date}, progression date: {progression_date}")
        
        # Parse planets list if provided
        planet_list = None
        if planets:
            planet_list = [p.strip() for p in planets.split(",")]
        
        # Call service to calculate secondary progressions
        progressed_positions = await progression_service.calculate_secondary_progressions(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
            progression_date=progression_date,
            planets=planet_list
        )
        
        logger.info(f"Secondary progressions calculation completed")
        return {
            "birth_date": birth_date,
            "progression_date": progression_date,
            "progressed_positions": progressed_positions
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for secondary progressions calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating secondary progressions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating secondary progressions", "code": "CALCULATION_ERROR"}
        )

@router.get("/progression-timeline", response_model=Dict[str, Any])
async def calculate_progression_timeline(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: Optional[str] = Query(None, description="Birth time in HH:MM:SS format"),
    birth_latitude: Optional[float] = Query(None, description="Birth location latitude"),
    birth_longitude: Optional[float] = Query(None, description="Birth location longitude"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    interval_months: int = Query(6, description="Interval in months between calculations"),
    planet: Optional[str] = Query(None, description="Specific planet to track (defaults to all)")
):
    """
    Calculate a timeline of progressions for a period of time.
    
    This endpoint calculates how progressed planets move over a specified period,
    tracking their positions at regular intervals. This is useful for forecasting
    long-term patterns.
    
    Returns a timeline of progressed positions.
    """
    try:
        logger.info(f"Calculating progression timeline from {start_date} to {end_date}")
        
        # Call service to calculate progression timeline
        timeline = await progression_service.calculate_progression_timeline(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
            start_date=start_date,
            end_date=end_date,
            interval_months=interval_months,
            planet=planet
        )
        
        logger.info(f"Progression timeline calculation completed")
        return {
            "birth_date": birth_date,
            "start_date": start_date,
            "end_date": end_date,
            "interval_months": interval_months,
            "progression_timeline": timeline
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for progression timeline calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating progression timeline: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating progression timeline", "code": "CALCULATION_ERROR"}
        )

@router.get("/progressed-chart-with-transits", response_model=Dict[str, Any])
async def calculate_progressed_chart_with_transits(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: Optional[str] = Query(None, description="Birth time in HH:MM:SS format"),
    birth_latitude: Optional[float] = Query(None, description="Birth location latitude"),
    birth_longitude: Optional[float] = Query(None, description="Birth location longitude"),
    calculation_date: Optional[str] = Query(None, description="Calculation date in YYYY-MM-DD format (defaults to current date)")
):
    """
    Calculate a progressed chart with current transits.
    
    This comprehensive endpoint calculates a progressed chart for the current date
    (or specified date) and also includes current transit aspects to both the natal
    and progressed chart.
    
    Returns a complete progressed chart with transit aspects.
    """
    try:
        logger.info(f"Calculating progressed chart with transits for birth date: {birth_date}")
        
        # Call service to calculate progressed chart with transits
        result = await progression_service.calculate_progressed_chart_with_transits(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
            calculation_date=calculation_date
        )
        
        logger.info(f"Progressed chart with transits calculation completed")
        return {
            "birth_date": birth_date,
            "calculation_date": result["calculation_date"],
            "progressed_positions": result["progressed_positions"],
            "transits_to_natal": result["transits_to_natal"],
            "transits_to_progressed": result["transits_to_progressed"]
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for progressed chart with transits calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating progressed chart with transits: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating progressed chart with transits", "code": "CALCULATION_ERROR"}
        )
