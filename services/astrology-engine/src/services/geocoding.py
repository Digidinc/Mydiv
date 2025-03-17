"""
Geocoding Service

This module provides geocoding functionality to convert location names to coordinates.
"""
import aiohttp
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from typing import Tuple, Optional, Dict, Any
from loguru import logger
from config import settings

class GeocodingService:
    """Service for geocoding location names to coordinates."""
    
    def __init__(self):
        """Initialize the geocoding service."""
        self.nominatim = Nominatim(
            user_agent="mydivinations-astrology-engine",
            timeout=5
        )
        self._cache = {}  # Simple in-memory cache
    
    async def geocode(self, location_name: str) -> Tuple[float, float, Optional[str]]:
        """
        Convert a location name to latitude and longitude coordinates.
        
        Args:
            location_name: The name of the location to geocode
            
        Returns:
            Tuple containing (latitude, longitude, timezone_name)
            
        Raises:
            ValueError: If the location cannot be geocoded
        """
        # Check cache first
        if location_name in self._cache:
            logger.info(f"Geocoding cache hit for: {location_name}")
            return self._cache[location_name]
        
        try:
            logger.info(f"Geocoding location: {location_name}")
            # Use geopy's Nominatim for geocoding
            location = self.nominatim.geocode(location_name)
            
            if not location:
                logger.warning(f"Unable to geocode location: {location_name}")
                raise ValueError(f"Unable to geocode location: {location_name}")
            
            latitude = location.latitude
            longitude = location.longitude
            
            # Get timezone information
            timezone_name = await self._get_timezone(latitude, longitude)
            
            # Cache the result
            result = (latitude, longitude, timezone_name)
            self._cache[location_name] = result
            
            logger.info(f"Geocoded {location_name} to lat: {latitude}, lng: {longitude}, timezone: {timezone_name}")
            return result
            
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            logger.error(f"Geocoding service error: {str(e)}")
            raise ValueError(f"Geocoding service temporarily unavailable. Please try again later.")
        
        except Exception as e:
            logger.error(f"Error geocoding location {location_name}: {str(e)}")
            raise ValueError(f"Error geocoding location: {str(e)}")
    
    async def _get_timezone(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Get the timezone name for given coordinates.
        
        Args:
            latitude: The latitude
            longitude: The longitude
            
        Returns:
            The timezone name or None if it cannot be determined
        """
        try:
            # Use timezone API to get timezone info
            async with aiohttp.ClientSession() as session:
                url = f"http://api.timezonedb.com/v2.1/get-time-zone"
                params = {
                    "key": settings.TIMEZONE_DB_API_KEY or "GAXQDGVFB55J",  # Fallback to demo key
                    "format": "json",
                    "by": "position",
                    "lat": latitude,
                    "lng": longitude
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "OK":
                            return data.get("zoneName")
            
            # Fallback if API call fails
            return None
            
        except Exception as e:
            logger.error(f"Error getting timezone for coordinates ({latitude}, {longitude}): {str(e)}")
            return None

# Create a singleton instance
geocoding_service = GeocodingService()
