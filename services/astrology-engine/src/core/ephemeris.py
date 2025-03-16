"""
Ephemeris Provider Interface

This module provides an abstraction over the Swiss Ephemeris library
for astronomical and astrological calculations.
"""
from typing import Dict, List, Any, Optional
import os
from loguru import logger

# Import Swiss Ephemeris (conditionally, with fallback for development)
try:
    import swisseph as swe
    SWISS_EPH_AVAILABLE = True
except ImportError:
    logger.warning("Swiss Ephemeris library not available. Using fallback mode for development.")
    SWISS_EPH_AVAILABLE = False

# Constants for calculations
PLANETS = {
    "sun": swe.SUN if SWISS_EPH_AVAILABLE else 0,
    "moon": swe.MOON if SWISS_EPH_AVAILABLE else 1,
    "mercury": swe.MERCURY if SWISS_EPH_AVAILABLE else 2,
    "venus": swe.VENUS if SWISS_EPH_AVAILABLE else 3,
    "mars": swe.MARS if SWISS_EPH_AVAILABLE else 4,
    "jupiter": swe.JUPITER if SWISS_EPH_AVAILABLE else 5,
    "saturn": swe.SATURN if SWISS_EPH_AVAILABLE else 6,
    "uranus": swe.URANUS if SWISS_EPH_AVAILABLE else 7,
    "neptune": swe.NEPTUNE if SWISS_EPH_AVAILABLE else 8,
    "pluto": swe.PLUTO if SWISS_EPH_AVAILABLE else 9,
    "north_node": swe.MEAN_NODE if SWISS_EPH_AVAILABLE else 10,
    "south_node": swe.MEAN_NODE if SWISS_EPH_AVAILABLE else 11,  # Calculated from North Node
    "chiron": swe.CHIRON if SWISS_EPH_AVAILABLE else 15
}

HOUSE_SYSTEMS = {
    "placidus": b'P',
    "koch": b'K',
    "porphyrius": b'O',
    "regiomontanus": b'R',
    "campanus": b'C',
    "equal": b'E',
    "whole_sign": b'W',
    "meridian": b'X',
    "morinus": b'M',
    "polich_page": b'T',
    "alcabitius": b'B',
    "krusinski": b'U',
    "equal_mc": b'L'
}

# Signs and their properties
SIGNS = {
    "aries": {"element": "fire", "modality": "cardinal", "start_degree": 0},
    "taurus": {"element": "earth", "modality": "fixed", "start_degree": 30},
    "gemini": {"element": "air", "modality": "mutable", "start_degree": 60},
    "cancer": {"element": "water", "modality": "cardinal", "start_degree": 90},
    "leo": {"element": "fire", "modality": "fixed", "start_degree": 120},
    "virgo": {"element": "earth", "modality": "mutable", "start_degree": 150},
    "libra": {"element": "air", "modality": "cardinal", "start_degree": 180},
    "scorpio": {"element": "water", "modality": "fixed", "start_degree": 210},
    "sagittarius": {"element": "fire", "modality": "mutable", "start_degree": 240},
    "capricorn": {"element": "earth", "modality": "cardinal", "start_degree": 270},
    "aquarius": {"element": "air", "modality": "fixed", "start_degree": 300},
    "pisces": {"element": "water", "modality": "mutable", "start_degree": 330}
}

# Mapping of degrees to signs
SIGN_FOR_DEGREE = [
    "aries", "aries", "taurus", "taurus", "gemini", "gemini",
    "cancer", "cancer", "leo", "leo", "virgo", "virgo",
    "libra", "libra", "scorpio", "scorpio", "sagittarius", "sagittarius",
    "capricorn", "capricorn", "aquarius", "aquarius", "pisces", "pisces"
]


class EphemerisProvider:
    """
    Provider for ephemeris calculations using Swiss Ephemeris.
    This class abstracts the details of the Swiss Ephemeris library.
    """
    
    def __init__(self, ephemeris_path: str):
        """
        Initialize the ephemeris provider.
        
        Args:
            ephemeris_path: Path to ephemeris data files
        """
        self.ephemeris_path = ephemeris_path
        
        # Initialize Swiss Ephemeris if available
        if SWISS_EPH_AVAILABLE:
            # Check if path exists
            if os.path.exists(ephemeris_path):
                swe.set_ephe_path(ephemeris_path)
                logger.info(f"Swiss Ephemeris initialized with path: {ephemeris_path}")
            else:
                logger.warning(f"Ephemeris path not found: {ephemeris_path}")
                logger.warning("Using built-in ephemeris data (less accurate)")
        else:
            logger.warning("Running in development mode without Swiss Ephemeris")
    
    def calculate_planet_position(self, planet: str, julian_day: float) -> Dict[str, Any]:
        """
        Calculate the position of a planet at a given Julian day.
        
        Args:
            planet: Planet name (sun, moon, etc.)
            julian_day: Julian day number
            
        Returns:
            Dictionary with planet position information
        """
        if not SWISS_EPH_AVAILABLE:
            # Fallback for development
            return self._mock_planet_position(planet, julian_day)
        
        # Get planet ID from constants
        planet_id = PLANETS.get(planet.lower())
        if planet_id is None:
            raise ValueError(f"Unknown planet: {planet}")
        
        # Handle special case for South Node
        if planet.lower() == "south_node":
            # South Node is opposite to North Node
            result = swe.calc_ut(julian_day, PLANETS["north_node"])
            # Add 180 degrees and normalize to 0-360
            longitude = (result[0] + 180) % 360
        else:
            # Calculate planet position
            result = swe.calc_ut(julian_day, planet_id)
            longitude = result[0]
        
        # Extract data from Swiss Ephemeris result
        latitude = result[1]
        distance = result[2]
        speed_longitude = result[3]
        speed_latitude = result[4]
        
        # Determine sign and degree within sign
        sign_num = int(longitude / 30)
        sign_degree = longitude % 30
        sign_name = list(SIGNS.keys())[sign_num]
        
        # Determine if retrograde
        is_retrograde = speed_longitude < 0
        
        # Return formatted result
        return {
            "longitude": longitude,
            "latitude": latitude,
            "distance": distance,
            "speed": speed_longitude,
            "speed_latitude": speed_latitude,
            "sign": sign_name,
            "degree": sign_degree,
            "retrograde": is_retrograde
        }
    
    def calculate_houses(
        self, 
        julian_day: float, 
        latitude: float, 
        longitude: float, 
        house_system: str = "placidus"
    ) -> Dict[int, Dict[str, Any]]:
        """
        Calculate house cusps for a given time and location.
        
        Args:
            julian_day: Julian day number
            latitude: Geographic latitude in degrees
            longitude: Geographic longitude in degrees
            house_system: House system to use (placidus, koch, etc.)
            
        Returns:
            Dictionary with house positions
        """
        if not SWISS_EPH_AVAILABLE:
            # Fallback for development
            return self._mock_houses(julian_day, latitude, longitude, house_system)
        
        # Get house system code
        house_system_code = HOUSE_SYSTEMS.get(house_system.lower())
        if house_system_code is None:
            raise ValueError(f"Unknown house system: {house_system}")
        
        # Calculate houses
        houses, ascendant, mc, armc, vertex, equatorial_ascendant = swe.houses(
            julian_day, latitude, longitude, house_system_code
        )
        
        # Format results
        result = {}
        for i in range(12):
            house_num = i + 1
            house_longitude = houses[i]
            
            # Determine sign and degree
            sign_num = int(house_longitude / 30)
            sign_degree = house_longitude % 30
            sign_name = list(SIGNS.keys())[sign_num]
            
            result[house_num] = {
                "longitude": house_longitude,
                "sign": sign_name,
                "degree": sign_degree
            }
        
        # Add special points
        result["ascendant"] = ascendant
        result["mc"] = mc
        result["armc"] = armc
        result["vertex"] = vertex
        result["equatorial_ascendant"] = equatorial_ascendant
        
        return result
    
    def get_julian_day(self, year: int, month: int, day: int, hour: float = 0.0) -> float:
        """
        Calculate Julian day number for a given date and time.
        
        Args:
            year: Year
            month: Month (1-12)
            day: Day (1-31)
            hour: Hour as decimal (0-24)
            
        Returns:
            Julian day number
        """
        if not SWISS_EPH_AVAILABLE:
            # Simplified calculation for development
            # This is a rough approximation and not accurate for all dates
            a = (14 - month) // 12
            y = year + 4800 - a
            m = month + 12 * a - 3
            jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
            return jdn + hour / 24.0
        
        # Use Swiss Ephemeris for accurate calculation
        return swe.julday(year, month, day, hour)
    
    def get_sign_name(self, longitude: float) -> str:
        """
        Get zodiac sign name for a given longitude.
        
        Args:
            longitude: Longitude in degrees (0-360)
            
        Returns:
            Sign name
        """
        sign_num = int(longitude / 30) % 12
        return list(SIGNS.keys())[sign_num]
    
    def get_sign_info(self, sign_name: str) -> Dict[str, Any]:
        """
        Get information about a zodiac sign.
        
        Args:
            sign_name: Sign name (aries, taurus, etc.)
            
        Returns:
            Dictionary with sign information
        """
        sign_data = SIGNS.get(sign_name.lower())
        if sign_data is None:
            raise ValueError(f"Unknown sign: {sign_name}")
        
        return sign_data
    
    # Mock methods for development when Swiss Ephemeris is not available
    
    def _mock_planet_position(self, planet: str, julian_day: float) -> Dict[str, Any]:
        """Mock planet position for development."""
        # This just returns predetermined values for demonstration
        mock_data = {
            "sun": {"longitude": 84.83, "latitude": 0.0, "sign": "gemini", "degree": 24.83, "retrograde": False},
            "moon": {"longitude": 202.53, "latitude": -3.1, "sign": "libra", "degree": 22.53, "retrograde": False},
            "mercury": {"longitude": 70.23, "latitude": 1.2, "sign": "gemini", "degree": 10.23, "retrograde": False},
            "venus": {"longitude": 45.78, "latitude": 0.8, "sign": "taurus", "degree": 15.78, "retrograde": False},
            "mars": {"longitude": 135.45, "latitude": 0.3, "sign": "leo", "degree": 15.45, "retrograde": False},
            "jupiter": {"longitude": 280.12, "latitude": -0.5, "sign": "capricorn", "degree": 10.12, "retrograde": True},
            "saturn": {"longitude": 310.67, "latitude": -0.2, "sign": "aquarius", "degree": 10.67, "retrograde": False},
            "uranus": {"longitude": 192.34, "latitude": 0.0, "sign": "libra", "degree": 12.34, "retrograde": False},
            "neptune": {"longitude": 355.78, "latitude": 0.0, "sign": "pisces", "degree": 25.78, "retrograde": False},
            "pluto": {"longitude": 286.23, "latitude": 0.0, "sign": "capricorn", "degree": 16.23, "retrograde": False}
        }
        
        planet_data = mock_data.get(planet.lower(), {
            "longitude": 0.0,
            "latitude": 0.0,
            "sign": "aries",
            "degree": 0.0,
            "retrograde": False
        })
        
        # Add additional fields for consistency with real calculation
        planet_data["distance"] = 1.0
        planet_data["speed"] = -0.5 if planet_data["retrograde"] else 0.5
        planet_data["speed_latitude"] = 0.0
        
        return planet_data
    
    def _mock_houses(
        self,
        julian_day: float,
        latitude: float,
        longitude: float,
        house_system: str
    ) -> Dict[int, Dict[str, Any]]:
        """Mock house calculation for development."""
        # This just returns predetermined values for demonstration
        houses = {
            1: {"longitude": 135.27, "sign": "leo", "degree": 15.27},
            2: {"longitude": 160.45, "sign": "virgo", "degree": 10.45},
            3: {"longitude": 185.23, "sign": "libra", "degree": 5.23},
            4: {"longitude": 213.56, "sign": "scorpio", "degree": 3.56},
            5: {"longitude": 245.78, "sign": "sagittarius", "degree": 5.78},
            6: {"longitude": 282.67, "sign": "capricorn", "degree": 12.67},
            7: {"longitude": 315.27, "sign": "aquarius", "degree": 15.27},
            8: {"longitude": 340.45, "sign": "pisces", "degree": 10.45},
            9: {"longitude": 5.23, "sign": "aries", "degree": 5.23},
            10: {"longitude": 33.56, "sign": "taurus", "degree": 3.56},
            11: {"longitude": 65.78, "sign": "gemini", "degree": 5.78},
            12: {"longitude": 102.67, "sign": "cancer", "degree": 12.67},
            "ascendant": 135.27,
            "mc": 33.56,
            "armc": 33.56,
            "vertex": 213.56,
            "equatorial_ascendant": 135.27
        }
        
        return houses
