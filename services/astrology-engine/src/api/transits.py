"""
Transits API Router

This module defines the API endpoints for transit calculations.
"""
from fastapi import APIRouter, HTTPException, Body, Query
from loguru import logger
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import models
from models.transits import TransitRequest, TransitResponse, TransitPeriodRequest, TransitPeriodResponse

# Import services
from services.transits import TransitService

# Create router
router = APIRouter()

# Service instance
transit_service = TransitService()

@router.post("/", response_model=TransitResponse)
async def calculate_transits(request: TransitRequest):
    """
    Calculate current transits to natal chart.
    
    This endpoint calculates how current planetary positions (or any specified date)
    form aspects to a natal chart's planetary positions.
    
    Returns a list of transit aspects with details about strength, applying/separating,
    and exact dates.
    """
    try:
        logger.info(f"Calculating transits for date: {request.transit_time.date}")
        
        # Call service to calculate transits
        transits = await transit_service.calculate_transits(
            natal_positions=request.natal_positions,
            transit_time=request.transit_time,
            options=request.options
        )
        
        logger.info(f"Transit calculation completed, found {len(transits)} transits")
        return {
            "transit_date": request.transit_time.date,
            "transits": transits
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for transit calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating transits: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating transits", "code": "CALCULATION_ERROR"}
        )

@router.post("/period", response_model=TransitPeriodResponse)
async def calculate_transit_period(request: TransitPeriodRequest):
    """
    Calculate transits over a period of time.
    
    This endpoint calculates significant transit aspects over a specified period,
    identifying when they become exact. This is useful for forecasting and
    predictive astrology.
    
    Returns a timeline of transit events sorted by date.
    """
    try:
        logger.info(f"Calculating transit period from {request.start_date} to {request.end_date}")
        
        # Call service to calculate transit period
        transit_timeline = await transit_service.calculate_transit_period(
            natal_positions=request.natal_positions,
            start_date=request.start_date,
            end_date=request.end_date,
            planets=request.planets,
            aspects=request.aspects,
            orbs=request.orbs
        )
        
        logger.info(f"Transit period calculation completed, found {len(transit_timeline)} events")
        return {
            "start_date": request.start_date,
            "end_date": request.end_date,
            "transit_timeline": transit_timeline
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for transit period calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating transit period: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating transit period", "code": "CALCULATION_ERROR"}
        )

@router.get("/five-year-forecast", response_model=Dict[str, Any])
async def generate_five_year_forecast(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: Optional[str] = Query(None, description="Birth time in HH:MM:SS format"),
    birth_latitude: Optional[float] = Query(None, description="Birth location latitude"),
    birth_longitude: Optional[float] = Query(None, description="Birth location longitude"),
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format (defaults to current date)"),
    transit_planets: Optional[str] = Query(None, description="Comma-separated list of transit planets to include")
):
    """
    Generate a 5-year forecast of significant transits.
    
    This endpoint generates a comprehensive 5-year forecast of significant transits
    to a natal chart. This includes outer planet transits to personal planets and
    key life events.
    
    Returns a timeline of significant transit events over the next 5 years.
    """
    try:
        logger.info(f"Generating 5-year forecast for birth date: {birth_date}")
        
        # Set default start date to current date if not provided
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        # Parse transit planets if provided
        transit_planet_list = None
        if transit_planets:
            transit_planet_list = [p.strip() for p in transit_planets.split(",")]
        
        # Call service to generate forecast
        forecast = await transit_service.generate_five_year_forecast(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
            start_date=start_date,
            transit_planets=transit_planet_list
        )
        
        logger.info(f"5-year forecast generation completed, found {len(forecast)} events")
        return {
            "birth_date": birth_date,
            "start_date": start_date,
            "end_date": forecast["end_date"],  # This will be 5 years from start date
            "significant_transits": forecast["transits"],
            "major_life_events": forecast["life_events"]
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for 5-year forecast: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error generating 5-year forecast: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error generating 5-year forecast", "code": "CALCULATION_ERROR"}
        )

@router.get("/current-transits", response_model=Dict[str, Any])
async def get_current_transits(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: Optional[str] = Query(None, description="Birth time in HH:MM:SS format"),
    birth_latitude: Optional[float] = Query(None, description="Birth location latitude"),
    birth_longitude: Optional[float] = Query(None, description="Birth location longitude"),
    orb: Optional[float] = Query(1.0, description="Orb in degrees")
):
    """
    Get current planetary transits to a natal chart.
    
    This endpoint calculates the current transits to a natal chart, including
    whether each transit is applying or separating.
    
    Returns a list of active transits with details.
    """
    try:
        logger.info(f"Calculating current transits for birth date: {birth_date}")
        
        # Call service to calculate current transits
        transits = await transit_service.calculate_current_transits(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
            orb=orb
        )
        
        logger.info(f"Current transits calculation completed, found {len(transits)} active transits")
        return {
            "birth_date": birth_date,
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "active_transits": transits
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for current transits: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating current transits: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating current transits", "code": "CALCULATION_ERROR"}
        )
