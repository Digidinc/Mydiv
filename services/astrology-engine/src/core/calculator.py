"""
Astrology Calculator

This module provides the core calculation service for astrological data,
building on the Ephemeris Provider to perform specific astrological calculations.
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import math
from loguru import logger

from .ephemeris import EphemerisProvider

# Constants for calculations
MAJOR_ASPECTS = {
    "conjunction": {"angle": 0, "orb": 8, "influence": 1.0},
    "opposition": {"angle": 180, "orb": 8, "influence": 0.9},
    "trine": {"angle": 120, "orb": 6, "influence": 0.8},
    "square": {"angle": 90, "orb": 6, "influence": 0.7},
    "sextile": {"angle": 60, "orb": 4, "influence": 0.6}
}

MINOR_ASPECTS = {
    "semi_square": {"angle": 45, "orb": 2, "influence": 0.3},
    "sesquiquadrate": {"angle": 135, "orb": 2, "influence": 0.3},
    "semi_sextile": {"angle": 30, "orb": 2, "influence": 0.2},
    "quincunx": {"angle": 150, "orb": 3, "influence": 0.4},
    "quintile": {"angle": 72, "orb": 2, "influence": 0.2},
    "bi_quintile": {"angle": 144, "orb": 2, "influence": 0.2}
}

# Planet and zodiac sign properties
PLANET_PROPERTIES = {
    "sun": {"element": "fire", "modality": None, "weight": 10},
    "moon": {"element": "water", "modality": None, "weight": 10},
    "mercury": {"element": "air", "modality": None, "weight": 8},
    "venus": {"element": "earth", "modality": None, "weight": 7},
    "mars": {"element": "fire", "modality": None, "weight": 7},
    "jupiter": {"element": "fire", "modality": None, "weight": 6},
    "saturn": {"element": "earth", "modality": None, "weight": 6},
    "uranus": {"element": "air", "modality": None, "weight": 4},
    "neptune": {"element": "water", "modality": None, "weight": 4},
    "pluto": {"element": "water", "modality": None, "weight": 4},
    "north_node": {"element": None, "modality": None, "weight": 2},
    "south_node": {"element": None, "modality": None, "weight": 2},
    "chiron": {"element": None, "modality": None, "weight": 3}
}

SIGN_PROPERTIES = {
    "aries": {"element": "fire", "modality": "cardinal", "polarity": "masculine"},
    "taurus": {"element": "earth", "modality": "fixed", "polarity": "feminine"},
    "gemini": {"element": "air", "modality": "mutable", "polarity": "masculine"},
    "cancer": {"element": "water", "modality": "cardinal", "polarity": "feminine"},
    "leo": {"element": "fire", "modality": "fixed", "polarity": "masculine"},
    "virgo": {"element": "earth", "modality": "mutable", "polarity": "feminine"},
    "libra": {"element": "air", "modality": "cardinal", "polarity": "masculine"},
    "scorpio": {"element": "water", "modality": "fixed", "polarity": "feminine"},
    "sagittarius": {"element": "fire", "modality": "mutable", "polarity": "masculine"},
    "capricorn": {"element": "earth", "modality": "cardinal", "polarity": "feminine"},
    "aquarius": {"element": "air", "modality": "fixed", "polarity": "masculine"},
    "pisces": {"element": "water", "modality": "mutable", "polarity": "feminine"}
}

class AstrologyCalculator:
    """
    Core calculation service for astrological data.
    This class builds on the EphemerisProvider to perform specific astrological calculations.
    """
    
    def __init__(self, ephemeris_provider: EphemerisProvider):
        """
        Initialize the calculator with an ephemeris provider.
        
        Args:
            ephemeris_provider: Provider for ephemeris calculations
        """
        self.ephemeris = ephemeris_provider
    
    def get_julian_day(self, date: str, time: str, timezone: str) -> float:
        """
        Convert a date and time to Julian day.
        
        Args:
            date: Date in YYYY-MM-DD format
            time: Time in HH:MM:SS format
            timezone: Time zone identifier
            
        Returns:
            Julian day number
        """
        # Parse date
        year, month, day = map(int, date.split('-'))
        
        # Parse time
        hour, minute, second = map(int, time.split(':'))
        
        # Convert to decimal hours
        decimal_hour = hour + minute/60.0 + second/3600.0
        
        # TODO: Handle timezone conversion properly
        # For now, assuming time is already in UT/GMT
        
        # Calculate Julian day
        return self.ephemeris.get_julian_day(year, month, day, decimal_hour)
    
    def calculate_planet_position(self, planet: str, julian_day: float) -> Dict[str, Any]:
        """
        Calculate the position of a planet at a given Julian day.
        
        Args:
            planet: Planet name (sun, moon, etc.)
            julian_day: Julian day number
            
        Returns:
            Dictionary with planet position information
        """
        return self.ephemeris.calculate_planet_position(planet, julian_day)
    
    def calculate_all_planets(self, julian_day: float) -> Dict[str, Dict[str, Any]]:
        """
        Calculate positions for all major planets.
        
        Args:
            julian_day: Julian day number
            
        Returns:
            Dictionary with position information for all planets
        """
        planets = {}
        for planet in PLANET_PROPERTIES.keys():
            planets[planet] = self.calculate_planet_position(planet, julian_day)
        
        return planets
    
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
        return self.ephemeris.calculate_houses(julian_day, latitude, longitude, house_system)
    
    def calculate_aspects(
        self,
        planet_positions: Dict[str, Dict[str, Any]],
        aspects_to_calculate: Optional[List[str]] = None,
        custom_orbs: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate aspects between planets.
        
        Args:
            planet_positions: Dictionary with planet positions
            aspects_to_calculate: List of aspect types to calculate (default: major aspects)
            custom_orbs: Dictionary with custom orbs for aspects
            
        Returns:
            List of aspects between planets
        """
        if aspects_to_calculate is None:
            # Default to major aspects
            aspects_to_calculate = list(MAJOR_ASPECTS.keys())
        
        # Combine major and minor aspects based on what's requested
        aspect_data = {}
        for aspect in aspects_to_calculate:
            if aspect in MAJOR_ASPECTS:
                aspect_data[aspect] = MAJOR_ASPECTS[aspect]
            elif aspect in MINOR_ASPECTS:
                aspect_data[aspect] = MINOR_ASPECTS[aspect]
        
        # Apply custom orbs if provided
        if custom_orbs:
            for aspect, orb in custom_orbs.items():
                if aspect in aspect_data:
                    aspect_data[aspect]["orb"] = orb
        
        # Calculate aspects between all planets
        aspects = []
        calculated_pairs = set()
        
        for planet1 in planet_positions:
            for planet2 in planet_positions:
                # Skip same planet and already calculated pairs
                if planet1 == planet2 or (planet1, planet2) in calculated_pairs or (planet2, planet1) in calculated_pairs:
                    continue
                
                # Add to calculated pairs
                calculated_pairs.add((planet1, planet2))
                
                # Get planet longitudes
                longitude1 = planet_positions[planet1]["longitude"]
                longitude2 = planet_positions[planet2]["longitude"]
                
                # Calculate angle between planets
                angle = abs(longitude1 - longitude2)
                if angle > 180:
                    angle = 360 - angle
                
                # Check for aspects
                for aspect_type, aspect_info in aspect_data.items():
                    aspect_angle = aspect_info["angle"]
                    max_orb = aspect_info["orb"]
                    base_influence = aspect_info["influence"]
                    
                    # Calculate orb
                    orb = abs(angle - aspect_angle)
                    
                    # Check if within orb
                    if orb <= max_orb:
                        # Calculate influence based on orb
                        influence = base_influence * (1 - orb / max_orb)
                        
                        # Determine if applying or separating
                        # This is a simplification - true calculation requires knowing planet speeds
                        speed1 = planet_positions[planet1].get("speed", 0)
                        speed2 = planet_positions[planet2].get("speed", 0)
                        applying = self._is_aspect_applying(longitude1, longitude2, speed1, speed2, aspect_angle)
                        
                        # Add aspect to results
                        aspects.append({
                            "planet1": planet1,
                            "planet2": planet2,
                            "type": aspect_type,
                            "angle": aspect_angle,
                            "orb": orb,
                            "applying": applying,
                            "influence": influence
                        })
        
        # Sort aspects by influence
        aspects.sort(key=lambda x: x["influence"], reverse=True)
        
        return aspects
    
    def calculate_element_balance(self, planet_positions: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate the balance of elements in a chart.
        
        Args:
            planet_positions: Dictionary with planet positions
            
        Returns:
            Dictionary with element percentages
        """
        # Initialize element scores
        element_scores = {
            "fire": 0.0,
            "earth": 0.0,
            "air": 0.0,
            "water": 0.0
        }
        
        # Initialize total weight
        total_weight = 0.0
        
        # Calculate weighted scores
        for planet, position in planet_positions.items():
            # Skip if planet doesn't have properties defined
            if planet not in PLANET_PROPERTIES:
                continue
            
            # Get planet weight
            weight = PLANET_PROPERTIES[planet]["weight"]
            total_weight += weight
            
            # Get sign of planet
            sign = position["sign"]
            
            # Get element of sign
            element = SIGN_PROPERTIES[sign]["element"]
            
            # Add weighted score to element
            element_scores[element] += weight
        
        # Convert to percentages
        if total_weight > 0:
            for element in element_scores:
                element_scores[element] = (element_scores[element] / total_weight) * 100
        
        return element_scores
    
    def calculate_modality_balance(self, planet_positions: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate the balance of modalities in a chart.
        
        Args:
            planet_positions: Dictionary with planet positions
            
        Returns:
            Dictionary with modality percentages
        """
        # Initialize modality scores
        modality_scores = {
            "cardinal": 0.0,
            "fixed": 0.0,
            "mutable": 0.0
        }
        
        # Initialize total weight
        total_weight = 0.0
        
        # Calculate weighted scores
        for planet, position in planet_positions.items():
            # Skip if planet doesn't have properties defined
            if planet not in PLANET_PROPERTIES:
                continue
            
            # Get planet weight
            weight = PLANET_PROPERTIES[planet]["weight"]
            total_weight += weight
            
            # Get sign of planet
            sign = position["sign"]
            
            # Get modality of sign
            modality = SIGN_PROPERTIES[sign]["modality"]
            
            # Add weighted score to modality
            modality_scores[modality] += weight
        
        # Convert to percentages
        if total_weight > 0:
            for modality in modality_scores:
                modality_scores[modality] = (modality_scores[modality] / total_weight) * 100
        
        return modality_scores
    
    def get_sign_name(self, longitude: float) -> str:
        """
        Get zodiac sign name for a given longitude.
        
        Args:
            longitude: Longitude in degrees (0-360)
            
        Returns:
            Sign name
        """
        return self.ephemeris.get_sign_name(longitude)
    
    def get_sign_properties(self, sign_name: str) -> Dict[str, Any]:
        """
        Get properties of a zodiac sign.
        
        Args:
            sign_name: Sign name
            
        Returns:
            Dictionary with sign properties
        """
        return SIGN_PROPERTIES.get(sign_name.lower(), {})
    
    def _is_aspect_applying(
        self,
        longitude1: float,
        longitude2: float,
        speed1: float,
        speed2: float,
        aspect_angle: float
    ) -> bool:
        """
        Determine if an aspect is applying or separating.
        
        Args:
            longitude1: Longitude of first planet
            longitude2: Longitude of second planet
            speed1: Speed of first planet
            speed2: Speed of second planet
            aspect_angle: Angle of the aspect
            
        Returns:
            True if applying, False if separating
        """
        # This is a simplification - true calculation is more complex
        # For a conjunction (0°), planets are approaching if the faster planet is behind the slower
        # For an opposition (180°), planets are approaching if they're moving toward opposition
        
        relative_speed = speed1 - speed2
        
        # If relative speed is 0, the aspect is neither applying nor separating
        if abs(relative_speed) < 0.001:
            return False
        
        # Calculate current angular separation
        separation = (longitude1 - longitude2) % 360
        if separation > 180:
            separation = 360 - separation
        
        # For a conjunction (0°)
        if aspect_angle == 0:
            # If planets are moving toward each other
            return (relative_speed < 0 and separation < 180) or (relative_speed > 0 and separation > 180)
        
        # For an opposition (180°)
        if aspect_angle == 180:
            # If planets are moving toward opposition
            return (relative_speed < 0 and separation > 180) or (relative_speed > 0 and separation < 180)
        
        # For other aspects, this is a complex calculation that depends on the specific aspect
        # This is a very simplified approach
        return separation < aspect_angle
