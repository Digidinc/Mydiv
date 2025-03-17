"""
Aspects API Router

This module defines the API endpoints for aspect calculations.
"""
from fastapi import APIRouter, HTTPException, Body
from loguru import logger
from typing import Dict, Any, List, Optional

# Import models
from models.aspects import AspectRequest, AspectConfigRequest, AspectResponse

# Import services
from services.aspects import AspectService

# Create router
router = APIRouter()

# Service instance
aspect_service = AspectService()

@router.post("/", response_model=AspectResponse)
async def calculate_aspects(request: AspectRequest):
    """
    Calculate aspects between planetary positions.
    
    This endpoint calculates the aspects between celestial bodies based on
    their longitudes, using the specified aspect types and orbs.
    
    Returns a list of aspects with details about the aspect type, orb, and influence.
    """
    try:
        logger.info(f"Calculating aspects between {len(request.planet_positions)} planets")
        
        # Call service to calculate aspects
        aspects = await aspect_service.calculate_aspects(
            planet_positions=request.planet_positions,
            options=request.options
        )
        
        logger.info(f"Aspect calculation completed, found {len(aspects)} aspects")
        return {
            "aspects": aspects
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for aspect calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating aspects: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating aspects", "code": "CALCULATION_ERROR"}
        )

@router.post("/planetary-aspects", response_model=Dict[str, Any])
async def calculate_aspects_between_planets(
    aspects_config: AspectConfigRequest = Body(...),
    date1: Optional[str] = Body(None, description="First date in YYYY-MM-DD format"),
    time1: Optional[str] = Body(None, description="First time in HH:MM:SS format"),
    date2: Optional[str] = Body(None, description="Second date in YYYY-MM-DD format (defaults to current date)"),
    time2: Optional[str] = Body(None, description="Second time in HH:MM:SS format (defaults to current time)")
):
    """
    Calculate aspects between planets at two different dates/times.
    
    This endpoint calculates the aspects between planets at two different points in time.
    This can be used for synastry (comparing two birth charts) or transit calculations.
    
    If date1/time1 are not provided, they're taken from the aspects_config.
    If date2/time2 are not provided, current date and time are used.
    
    Returns a list of aspects between the planets at the specified times.
    """
    try:
        logger.info(f"Calculating aspects between planets at two different times")
        
        # Call service to calculate aspects
        aspects = await aspect_service.calculate_planetary_aspects(
            config=aspects_config,
            date1=date1,
            time1=time1,
            date2=date2,
            time2=time2
        )
        
        logger.info(f"Planetary aspects calculation completed, found {len(aspects)} aspects")
        return {
            "date1": date1 or "from config",
            "time1": time1 or "from config",
            "date2": date2 or "current date",
            "time2": time2 or "current time",
            "aspects": aspects
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for planetary aspects calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating planetary aspects: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating planetary aspects", "code": "CALCULATION_ERROR"}
        )

@router.post("/aspect-timeline", response_model=Dict[str, Any])
async def calculate_aspect_timeline(
    planet1: str = Body(..., description="First planet"),
    planet2: str = Body(..., description="Second planet"),
    aspect_type: str = Body(..., description="Aspect type (conjunction, opposition, trine, etc.)"),
    start_date: str = Body(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Body(..., description="End date in YYYY-MM-DD format"),
    orb: float = Body(1.0, description="Orb in degrees")
):
    """
    Calculate a timeline of when an aspect between two planets becomes exact.
    
    This endpoint calculates when a specific aspect between two planets becomes exact
    within a date range. This is useful for finding key astrological events.
    
    Returns a list of dates when the aspect is exact, along with additional details.
    """
    try:
        logger.info(f"Calculating {aspect_type} timeline between {planet1} and {planet2} from {start_date} to {end_date}")
        
        # Call service to calculate aspect timeline
        timeline = await aspect_service.calculate_aspect_timeline(
            planet1=planet1,
            planet2=planet2,
            aspect_type=aspect_type,
            start_date=start_date,
            end_date=end_date,
            orb=orb
        )
        
        logger.info(f"Aspect timeline calculation completed, found {len(timeline)} exact aspects")
        return {
            "planet1": planet1,
            "planet2": planet2,
            "aspect_type": aspect_type,
            "start_date": start_date,
            "end_date": end_date,
            "orb": orb,
            "timeline": timeline
        }
    
    except ValueError as e:
        logger.error(f"Invalid data for aspect timeline calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_PARAMETER"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating aspect timeline: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating aspect timeline", "code": "CALCULATION_ERROR"}
        )
