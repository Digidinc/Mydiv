"""
Birth Chart API Router

This module defines the API endpoints for birth chart calculations.
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from loguru import logger
from typing import Optional, Dict, Any

# Import models
from models.birth_data import BirthDataRequest
from models.chart import ChartResponse

# Import services
from services.birth_chart import BirthChartService

# Create router
router = APIRouter()

# Service instance
birth_chart_service = BirthChartService()

@router.post("/", response_model=ChartResponse)
async def calculate_birth_chart(request: BirthDataRequest):
    """
    Calculate a complete natal chart from birth information.
    
    This endpoint calculates a full astrological natal chart based on the provided
    birth data, including planetary positions, house cusps, aspects, and dominant
    patterns.
    
    Returns a complete chart object with all astrological elements.
    """
    try:
        logger.info(f"Calculating birth chart for date: {request.birth_data.date}, time: {request.birth_data.time}, location: {request.birth_data.location.location_name}")
        
        # Call service to calculate chart
        chart = await birth_chart_service.calculate_chart(
            birth_data=request.birth_data,
            options=request.options
        )
        
        logger.info(f"Birth chart calculation completed successfully")
        return chart
    
    except ValueError as e:
        logger.error(f"Invalid data for birth chart calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_BIRTH_DATA"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating birth chart: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating birth chart", "code": "CALCULATION_ERROR"}
        )

@router.get("/{chart_id}", response_model=ChartResponse)
async def get_stored_chart(chart_id: str):
    """
    Retrieve a previously calculated birth chart by ID.
    
    This endpoint retrieves a birth chart that was previously calculated and stored.
    The chart is identified by its unique chart ID.
    
    Returns the complete chart object.
    """
    try:
        logger.info(f"Retrieving stored birth chart with ID: {chart_id}")
        
        # Call service to retrieve chart
        chart = await birth_chart_service.get_chart_by_id(chart_id)
        
        if not chart:
            logger.warning(f"Chart with ID {chart_id} not found")
            raise HTTPException(
                status_code=404,
                detail={"message": "Chart not found", "code": "CHART_NOT_FOUND"}
            )
        
        logger.info(f"Successfully retrieved chart with ID: {chart_id}")
        return chart
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Error retrieving chart with ID {chart_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error retrieving birth chart", "code": "RETRIEVAL_ERROR"}
        )

@router.get("/", response_model=Dict[str, Any])
async def get_chart_summary(
    date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    time: Optional[str] = Query(None, description="Birth time in HH:MM:SS format"),
    latitude: Optional[float] = Query(None, description="Birth location latitude"),
    longitude: Optional[float] = Query(None, description="Birth location longitude"),
):
    """
    Get a summary of a birth chart without storing it.
    
    This endpoint calculates a simplified version of a birth chart and returns
    only the summary information, such as sun sign, moon sign, and ascendant.
    
    This is useful for quick lookups without the overhead of a full chart calculation.
    """
    try:
        logger.info(f"Calculating chart summary for date: {date}, time: {time}")
        
        # Call service to get chart summary
        summary = await birth_chart_service.get_chart_summary(
            date=date,
            time=time,
            latitude=latitude,
            longitude=longitude
        )
        
        logger.info(f"Chart summary calculation completed successfully")
        return summary
    
    except ValueError as e:
        logger.error(f"Invalid data for chart summary calculation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e), "code": "INVALID_BIRTH_DATA"}
        )
    
    except Exception as e:
        logger.error(f"Error calculating chart summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error calculating chart summary", "code": "CALCULATION_ERROR"}
        )
