"""
Astrology API Service

This module provides a service for interacting with the Astrology Engine API.
It handles making requests to the API and caching responses for efficiency.
"""
import os
import json
import hashlib
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union

from loguru import logger
from fastapi import HTTPException, status

# Import database connection
from db.postgres import db_pool

# Import Redis connection for caching
from cache.redis import redis_client

# Configuration
ASTROLOGY_API_BASE_URL = os.getenv("ASTROLOGY_API_BASE_URL", "https://api.mydivinations.com/astrology-engine")
ASTROLOGY_API_KEY = os.getenv("ASTROLOGY_API_KEY")
API_TIMEOUT = 30.0  # seconds


class AstrologyApiService:
    """Service for interacting with the Astrology Engine API."""
    
    def __init__(self):
        """Initialize the service."""
        self.base_url = ASTROLOGY_API_BASE_URL
        self.api_key = ASTROLOGY_API_KEY
        
        if not self.api_key:
            logger.warning("ASTROLOGY_API_KEY environment variable not set. API requests will fail.")
        
        # Headers for API requests
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
    
    async def get_birth_chart(self, birth_data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get a complete birth chart from the Astrology Engine API.
        
        Args:
            birth_data: Dictionary containing birth information (date, time, location)
            options: Optional configuration for the birth chart calculation
            
        Returns:
            Complete birth chart data
        """
        # Default options if not provided
        if options is None:
            options = {
                "house_system": "placidus",
                "with_aspects": True,
                "with_dignities": True,
                "with_dominant_elements": True
            }
        
        # Create request data
        data = {
            "birth_data": birth_data,
            "options": options
        }
        
        # Calculate cache key
        cache_key = self._calculate_cache_key("birth_chart", data)
        
        # Check cache first
        cached_result = await self._get_from_cache(cache_key)
        if cached_result:
            logger.debug(f"Cache hit for birth chart: {cache_key}")
            return cached_result
        
        # Make API request
        try:
            async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
                response = await client.post(
                    f"{self.base_url}/birth_chart",
                    json=data,
                    headers=self.headers
                )
                
                # Check for successful response
                response.raise_for_status()
                
                # Parse response
                birth_chart = response.json()
                
                # Cache the result (birth charts don't change)
                await self._store_in_cache(cache_key, birth_chart, expire=None)
                
                return birth_chart
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while fetching birth chart: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 400:
                # Bad request, probably invalid input
                error_detail = e.response.json().get("detail", str(e))
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid birth data: {error_detail}"
                )
            else:
                # Other API errors
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Error from Astrology API: {str(e)}"
                )
                
        except httpx.RequestError as e:
            logger.error(f"Request error while fetching birth chart: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to Astrology API: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error while fetching birth chart: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing birth chart request: {str(e)}"
            )
    
    async def get_current_transits(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        orb: float = 1.5
    ) -> Dict[str, Any]:
        """
        Get current planetary transits to a birth chart.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM:SS format (optional)
            birth_latitude: Birth location latitude (optional)
            birth_longitude: Birth location longitude (optional)
            orb: Maximum orb in degrees (default: 1.5)
            
        Returns:
            Current active transits
        """
        # Create query parameters
        params = {
            "birth_date": birth_date,
            "orb": orb
        }
        
        # Add optional parameters if provided
        if birth_time:
            params["birth_time"] = birth_time
        if birth_latitude is not None:
            params["birth_latitude"] = birth_latitude
        if birth_longitude is not None:
            params["birth_longitude"] = birth_longitude
        
        # Create cache key
        today = datetime.now().strftime("%Y-%m-%d")
        cache_key = self._calculate_cache_key(f"current_transits_{today}", params)
        
        # Check cache first (transits change daily)
        cached_result = await self._get_from_cache(cache_key)
        if cached_result:
            logger.debug(f"Cache hit for current transits: {cache_key}")
            return cached_result
        
        # Make API request
        try:
            async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
                response = await client.get(
                    f"{self.base_url}/transits/current-transits",
                    params=params,
                    headers=self.headers
                )
                
                # Check for successful response
                response.raise_for_status()
                
                # Parse response
                transits = response.json()
                
                # Cache for 24 hours (transits change daily)
                await self._store_in_cache(cache_key, transits, expire=86400)
                
                return transits
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while fetching current transits: {e.response.status_code} - {e.response.text}")
            error_detail = e.response.json().get("detail", str(e))
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Astrology API: {error_detail}"
            )
                
        except httpx.RequestError as e:
            logger.error(f"Request error while fetching current transits: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to Astrology API: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error while fetching current transits: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing transits request: {str(e)}"
            )
    
    async def get_five_year_forecast(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        start_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a 5-year forecast of significant transits.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM:SS format (optional)
            birth_latitude: Birth location latitude (optional)
            birth_longitude: Birth location longitude (optional)
            start_date: Start date for the forecast (defaults to current date)
            
        Returns:
            Five-year forecast with significant transits and major life events
        """
        # Create query parameters
        params = {
            "birth_date": birth_date
        }
        
        # Add optional parameters if provided
        if birth_time:
            params["birth_time"] = birth_time
        if birth_latitude is not None:
            params["birth_latitude"] = birth_latitude
        if birth_longitude is not None:
            params["birth_longitude"] = birth_longitude
        if start_date:
            params["start_date"] = start_date
        
        # Create cache key
        today = datetime.now().strftime("%Y-%m-%d")
        cache_key = self._calculate_cache_key(f"five_year_forecast_{today}", params)
        
        # Check cache first
        cached_result = await self._get_from_cache(cache_key)
        if cached_result:
            logger.debug(f"Cache hit for five-year forecast: {cache_key}")
            return cached_result
        
        # Make API request
        try:
            async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
                response = await client.get(
                    f"{self.base_url}/transits/five-year-forecast",
                    params=params,
                    headers=self.headers
                )
                
                # Check for successful response
                response.raise_for_status()
                
                # Parse response
                forecast = response.json()
                
                # Cache for 7 days (forecast doesn't change much day to day)
                await self._store_in_cache(cache_key, forecast, expire=604800)
                
                return forecast
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while fetching five-year forecast: {e.response.status_code} - {e.response.text}")
            error_detail = e.response.json().get("detail", str(e))
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Astrology API: {error_detail}"
            )
                
        except httpx.RequestError as e:
            logger.error(f"Request error while fetching five-year forecast: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to Astrology API: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error while fetching five-year forecast: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing forecast request: {str(e)}"
            )
    
    async def calculate_transit_period(
        self,
        natal_positions: Dict[str, float],
        start_date: str,
        end_date: str,
        planets: Optional[List[str]] = None,
        aspects: Optional[List[str]] = None,
        orbs: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculate transits over a specific period of time.
        
        Args:
            natal_positions: Dictionary of natal planet names and their longitudes
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            planets: Transit planets to include (defaults to outer planets)
            aspects: Aspect types to include (defaults to major aspects)
            orbs: Maximum orb for each aspect type
            
        Returns:
            Timeline of transit events sorted by date
        """
        # Default values
        if planets is None:
            planets = ["jupiter", "saturn", "uranus", "neptune", "pluto"]
        
        if aspects is None:
            aspects = ["conjunction", "opposition", "trine", "square"]
        
        if orbs is None:
            orbs = {
                "conjunction": 1.0,
                "opposition": 1.0,
                "square": 0.8,
                "trine": 0.8,
                "sextile": 0.6
            }
        
        # Create request data
        data = {
            "natal_positions": natal_positions,
            "start_date": start_date,
            "end_date": end_date,
            "planets": planets,
            "aspects": aspects,
            "orbs": orbs
        }
        
        # Calculate cache key
        cache_key = self._calculate_cache_key("transit_period", data)
        
        # Check cache first
        cached_result = await self._get_from_cache(cache_key)
        if cached_result:
            logger.debug(f"Cache hit for transit period: {cache_key}")
            return cached_result
        
        # Make API request
        try:
            async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
                response = await client.post(
                    f"{self.base_url}/transits/period",
                    json=data,
                    headers=self.headers
                )
                
                # Check for successful response
                response.raise_for_status()
                
                # Parse response
                transit_period = response.json()
                
                # Cache for 7 days
                await self._store_in_cache(cache_key, transit_period, expire=604800)
                
                return transit_period
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while calculating transit period: {e.response.status_code} - {e.response.text}")
            error_detail = e.response.json().get("detail", str(e))
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Astrology API: {error_detail}"
            )
                
        except httpx.RequestError as e:
            logger.error(f"Request error while calculating transit period: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to Astrology API: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error while calculating transit period: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing transit period request: {str(e)}"
            )
    
    async def calculate_secondary_progressions(
        self,
        birth_date: str,
        progression_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        planets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Calculate secondary progressions for a given date.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            progression_date: Date for progression calculation in YYYY-MM-DD format
            birth_time: Birth time in HH:MM:SS format (optional)
            birth_latitude: Birth latitude (optional)
            birth_longitude: Birth longitude (optional)
            planets: List of planets to include (defaults to all)
            
        Returns:
            Dictionary of progressed planet positions
        """
        # Create query parameters
        params = {
            "birth_date": birth_date,
            "progression_date": progression_date
        }
        
        # Add optional parameters if provided
        if birth_time:
            params["birth_time"] = birth_time
        if birth_latitude is not None:
            params["birth_latitude"] = birth_latitude
        if birth_longitude is not None:
            params["birth_longitude"] = birth_longitude
        if planets:
            params["planets"] = ",".join(planets)
        
        # Calculate cache key
        cache_key = self._calculate_cache_key("secondary_progressions", params)
        
        # Check cache first
        cached_result = await self._get_from_cache(cache_key)
        if cached_result:
            logger.debug(f"Cache hit for secondary progressions: {cache_key}")
            return cached_result
        
        # Make API request
        try:
            async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
                response = await client.get(
                    f"{self.base_url}/progressions/secondary",
                    params=params,
                    headers=self.headers
                )
                
                # Check for successful response
                response.raise_for_status()
                
                # Parse response
                progressions = response.json()
                
                # Cache for 30 days (progressions change very slowly)
                await self._store_in_cache(cache_key, progressions, expire=2592000)
                
                return progressions
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while calculating progressions: {e.response.status_code} - {e.response.text}")
            error_detail = e.response.json().get("detail", str(e))
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Astrology API: {error_detail}"
            )
                
        except httpx.RequestError as e:
            logger.error(f"Request error while calculating progressions: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to Astrology API: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error while calculating progressions: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing progressions request: {str(e)}"
            )
    
    async def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Get a cached API response.
        
        Args:
            cache_key: The cache key
            
        Returns:
            Cached data if available, None otherwise
        """
        try:
            # Try to get from Redis cache
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            
            # Try to get from database cache
            async with db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT response_data
                    FROM astrology_cache
                    WHERE query_hash = $1 AND expires_at > NOW()
                    """,
                    cache_key
                )
                
                if row:
                    return row["response_data"]
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving from cache: {str(e)}")
            # If cache access fails, just return None (will fetch fresh data)
            return None
    
    async def _store_in_cache(self, cache_key: str, data: Dict[str, Any], expire: Optional[int] = None) -> None:
        """
        Store data in cache.
        
        Args:
            cache_key: The cache key
            data: The data to cache
            expire: Expiration time in seconds (None for no expiration)
        """
        try:
            # Store in Redis cache (for quick access)
            json_data = json.dumps(data)
            if expire:
                await redis_client.set(cache_key, json_data, ex=expire)
            else:
                await redis_client.set(cache_key, json_data)
            
            # Store in database cache (for persistence)
            # Calculate expiration date
            expires_at = None
            if expire:
                expires_at = datetime.now() + timedelta(seconds=expire)
            
            async with db_pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO astrology_cache 
                    (query_hash, query_type, query_params, response_data, expires_at)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (query_hash) 
                    DO UPDATE SET
                        response_data = $4,
                        expires_at = $5,
                        created_at = NOW()
                    """,
                    cache_key,
                    self._get_query_type(cache_key),
                    {},  # We don't need to store params since we have the hash
                    data,
                    expires_at
                )
                
        except Exception as e:
            logger.error(f"Error storing in cache: {str(e)}")
            # If cache storage fails, just continue (non-critical)
    
    def _calculate_cache_key(self, prefix: str, data: Dict[str, Any]) -> str:
        """
        Calculate a cache key for a request.
        
        Args:
            prefix: Key prefix
            data: Request data to hash
            
        Returns:
            Cache key
        """
        # Normalize data by sorting keys
        sorted_data = json.dumps(data, sort_keys=True)
        
        # Calculate hash
        hash_obj = hashlib.sha256(sorted_data.encode())
        hash_digest = hash_obj.hexdigest()
        
        # Create key with prefix
        return f"{prefix}:{hash_digest}"
    
    def _get_query_type(self, cache_key: str) -> str:
        """
        Extract query type from cache key.
        
        Args:
            cache_key: The cache key
            
        Returns:
            Query type
        """
        return cache_key.split(":")[0]

# Create singleton instance
astrology_api_service = AstrologyApiService()
