"""
Ephemeris Service

This module provides a service for interacting with the Swiss Ephemeris library.
It handles planet positions, sign determinations, and other ephemeris calculations.
"""
import swisseph as swe
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from loguru import logger

from config import settings

class EphemerisService:
    """Service for Swiss Ephemeris calculations."""
    
    def __init__(self):
        """
        Initialize the Swiss Ephemeris wrapper.
        
        Sets up the ephemeris path and initializes the planet mappings.
        """
        # Set ephemeris path
        swe.set_ephe_path(settings.EPHEMERIS_PATH)
        logger.info(f"Initialized Swiss Ephemeris with path: {settings.EPHEMERIS_PATH}")
        
        # Planet mappings
        self.planets = {
            "sun": swe.SUN,
            "moon": swe.MOON,
            "mercury": swe.MERCURY,
            "venus": swe.VENUS,
            "mars": swe.MARS,
            "jupiter": swe.JUPITER,
            "saturn": swe.SATURN,
            "uranus": swe.URANUS,
            "neptune": swe.NEPTUNE,
            "pluto": swe.PLUTO,
            "chiron": swe.CHIRON,
            "north_node": swe.MEAN_NODE,
            "true_node": swe.TRUE_NODE,
            "south_node": -1,  # Calculated from north node
            "vertex": -2,      # Calculated separately
            "lilith": swe.MEAN_APOG,
            "true_lilith": swe.OSCU_APOG,
            "pars_fortuna": -3  # Calculated separately
        }
        
        # House system mappings
        self.house_systems = {
            "placidus": b'P',
            "koch": b'K',
            "campanus": b'C',
            "equal": b'E',
            "whole_sign": b'W',
            "regiomontanus": b'R',
            "porphyry": b'O',
            "topocentric": b'T',
            "alcabitius": b'B',
            "morinus": b'M'
        }
        
        # Zodiac signs
        self.signs = [
            "Aries", "Taurus", "Gemini", "Cancer", 
            "Leo", "Virgo", "Libra", "Scorpio", 
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # Elements by sign
        self.elements = {
            "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
            "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
            "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
            "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
        }
        
        # Modalities by sign
        self.modalities = {
            "Aries": "Cardinal", "Cancer": "Cardinal", "Libra": "Cardinal", "Capricorn": "Cardinal",
            "Taurus": "Fixed", "Leo": "Fixed", "Scorpio": "Fixed", "Aquarius": "Fixed",
            "Gemini": "Mutable", "Virgo": "Mutable", "Sagittarius": "Mutable", "Pisces": "Mutable"
        }
    
    async def calculate_planet_positions(
        self, 
        date: str, 
        time: str = "12:00:00", 
        latitude: Optional[float] = None, 
        longitude: Optional[float] = None, 
        planets: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate positions of planets at a given date and time.
        
        Args:
            date: Date in YYYY-MM-DD format
            time: Time in HH:MM:SS format (defaults to 12:00:00)
            latitude: Observer's latitude (optional)
            longitude: Observer's longitude (optional)
            planets: List of planets to calculate (defaults to all)
            
        Returns:
            Dictionary of planet positions with sign, degree, and other data
        """
        try:
            # Parse date and time
            dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
            
            # Convert to Julian Day
            jd = self._date_to_jd(dt)
            
            # Determine which planets to calculate
            planet_list = planets or list(self.planets.keys())
            
            # Filter out special planets that require separate calculations
            standard_planets = [p for p in planet_list if self.planets.get(p, -999) >= 0]
            special_planets = [p for p in planet_list if self.planets.get(p, -999) < 0]
            
            # Calculate positions
            positions = {}
            
            # Process standard planets
            for planet_name in standard_planets:
                planet_id = self.planets.get(planet_name)
                if planet_id is not None:
                    positions[planet_name] = self._calculate_planet_position(jd, planet_id)
            
            # Process special planets
            if "south_node" in special_planets and "north_node" in positions:
                positions["south_node"] = self._calculate_south_node(positions["north_node"])
            
            if "pars_fortuna" in special_planets:
                if all(p in positions for p in ["sun", "moon", "ascendant"]):
                    positions["pars_fortuna"] = self._calculate_pars_fortuna(
                        positions["sun"],
                        positions["moon"],
                        positions["ascendant"]
                    )
            
            # Calculate houses if coordinates are provided
            if latitude is not None and longitude is not None:
                house_data = self._calculate_houses(jd, latitude, longitude)
                
                # Add house-specific points to positions
                positions["ascendant"] = house_data["ascendant"]
                positions["mc"] = house_data["mc"]
                
                if "vertex" in special_planets:
                    positions["vertex"] = house_data["vertex"]
                
                # Add house numbers to planets
                for planet_name, planet_data in positions.items():
                    if "longitude" in planet_data:
                        planet_data["house"] = self._get_house_number(
                            planet_data["longitude"],
                            house_data["cusps"]
                        )
            
            logger.info(f"Calculated positions for {len(positions)} planets at {date} {time}")
            return positions
            
        except Exception as e:
            logger.error(f"Error calculating planet positions: {str(e)}")
            raise
    
    async def calculate_planet_position_range(
        self,
        planet: str,
        start_date: str,
        end_date: str,
        interval_days: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Calculate positions of a planet over a date range.
        
        Args:
            planet: Planet name
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            interval_days: Interval between calculations in days
            
        Returns:
            List of planet positions over the date range
        """
        try:
            # Validate planet
            if planet not in self.planets:
                raise ValueError(f"Invalid planet: {planet}")
            
            # Parse dates
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Calculate number of days and positions
            days = (end_dt - start_dt).days + 1
            num_positions = days // interval_days + (1 if days % interval_days else 0)
            
            positions = []
            for i in range(num_positions):
                current_dt = start_dt + timedelta(days=i * interval_days)
                current_date = current_dt.strftime("%Y-%m-%d")
                
                # Calculate position
                position_data = await self.calculate_planet_positions(
                    date=current_date,
                    planets=[planet]
                )
                
                # Add date and extract the planet's position
                position_entry = position_data[planet].copy()
                position_entry["date"] = current_date
                positions.append(position_entry)
            
            logger.info(f"Calculated {len(positions)} positions for {planet} from {start_date} to {end_date}")
            return positions
            
        except Exception as e:
            logger.error(f"Error calculating planet position range: {str(e)}")
            raise
    
    async def calculate_planet_ingress(
        self,
        planet: str,
        start_date: str,
        end_date: Optional[str] = None,
        signs: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate when a planet enters new zodiac signs.
        
        Args:
            planet: Planet name
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format (defaults to 1 year from start)
            signs: List of specific signs to check (defaults to all)
            
        Returns:
            List of ingress events with dates and signs
        """
        try:
            # Validate planet
            if planet not in self.planets:
                raise ValueError(f"Invalid planet: {planet}")
            
            # Parse start date
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            
            # Set default end date to 1 year from start if not provided
            if not end_date:
                end_dt = start_dt + timedelta(days=365)
            else:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Validate date range
            if start_dt > end_dt:
                raise ValueError("Start date must be before end date")
            
            # Filter signs if provided
            sign_list = signs or self.signs
            for sign in sign_list:
                if sign not in self.signs:
                    raise ValueError(f"Invalid sign: {sign}")
            
            # Get planet positions at daily intervals
            positions = await self.calculate_planet_position_range(
                planet=planet,
                start_date=start_date,
                end_date=end_dt.strftime("%Y-%m-%d"),
                interval_days=1
            )
            
            # Find sign changes
            ingress_events = []
            prev_sign = None
            
            for pos in positions:
                current_sign = pos["sign"]
                
                # Check if sign changed
                if prev_sign is not None and current_sign != prev_sign:
                    # Check if the new sign is in our target list
                    if current_sign in sign_list:
                        ingress_events.append({
                            "date": pos["date"],
                            "planet": planet,
                            "sign": current_sign,
                            "degree": pos["degree"],
                            "retrograde": pos.get("retrograde", False)
                        })
                
                prev_sign = current_sign
            
            logger.info(f"Found {len(ingress_events)} ingress events for {planet} from {start_date} to {end_dt.strftime('%Y-%m-%d')}")
            return ingress_events
            
        except Exception as e:
            logger.error(f"Error calculating planet ingress: {str(e)}")
            raise
    
    def _date_to_jd(self, dt: datetime) -> float:
        """
        Convert a Python datetime to Julian Day.
        
        Args:
            dt: Python datetime object
            
        Returns:
            Julian Day as float
        """
        year, month, day = dt.year, dt.month, dt.day
        hour = dt.hour + dt.minute/60.0 + dt.second/3600.0
        
        # Convert to Julian Day
        jd = swe.julday(year, month, day, hour)
        return jd
    
    def _calculate_planet_position(self, jd: float, planet_id: int) -> Dict[str, Any]:
        """
        Calculate position data for a celestial body.
        
        Args:
            jd: Julian Day
            planet_id: Swiss Ephemeris planet ID
            
        Returns:
            Dictionary with position data
        """
        # Calculate position
        xx, ret = swe.calc_ut(jd, planet_id)
        
        # Get basic data
        longitude = xx[0]
        latitude = xx[1]
        distance = xx[2]
        speed = xx[3]  # Daily motion in longitude
        
        # Determine sign and degree
        sign_idx = int(longitude / 30)
        degree = longitude % 30
        sign = self.signs[sign_idx]
        
        # Determine if retrograde
        retrograde = speed < 0
        
        return {
            "longitude": longitude,
            "latitude": latitude,
            "distance": distance,
            "speed": speed,
            "sign": sign,
            "degree": degree,
            "retrograde": retrograde
        }
    
    def _calculate_houses(self, jd: float, lat: float, lng: float, system: str = "placidus") -> Dict[str, Any]:
        """
        Calculate house cusps for a given time and location.
        
        Args:
            jd: Julian Day
            lat: Latitude
            lng: Longitude
            system: House system name
            
        Returns:
            Dictionary with house data
        """
        # Get house system code
        hsys = self.house_systems.get(system.lower(), b'P')  # Default to Placidus
        
        # Calculate houses
        cusps, ascmc = swe.houses(jd, lat, lng, hsys)
        
        # Process house cusps
        house_cusps = {}
        for i in range(12):
            house_num = i + 1
            longitude = cusps[i]
            sign_idx = int(longitude / 30)
            degree = longitude % 30
            
            house_cusps[house_num] = {
                "longitude": longitude,
                "sign": self.signs[sign_idx],
                "degree": degree
            }
        
        # Process special points
        ascendant = {
            "longitude": ascmc[0],
            "sign": self.signs[int(ascmc[0] / 30)],
            "degree": ascmc[0] % 30
        }
        
        mc = {
            "longitude": ascmc[1],
            "sign": self.signs[int(ascmc[1] / 30)],
            "degree": ascmc[1] % 30
        }
        
        # Calculate vertex
        # This is a simplification; for true vertex, more complex calculations are needed
        vertex = {
            "longitude": ascmc[4] if len(ascmc) > 4 else 0,
            "sign": self.signs[int((ascmc[4] if len(ascmc) > 4 else 0) / 30)],
            "degree": (ascmc[4] if len(ascmc) > 4 else 0) % 30
        }
        
        return {
            "cusps": house_cusps,
            "ascendant": ascendant,
            "mc": mc,
            "vertex": vertex
        }
    
    def _calculate_south_node(self, north_node: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate South Node position from North Node.
        
        Args:
            north_node: North Node position data
            
        Returns:
            South Node position data
        """
        # South Node is opposite to North Node
        longitude = (north_node["longitude"] + 180) % 360
        sign_idx = int(longitude / 30)
        degree = longitude % 30
        
        return {
            "longitude": longitude,
            "sign": self.signs[sign_idx],
            "degree": degree,
            "retrograde": north_node.get("retrograde", False),
            "house": north_node.get("house")
        }
    
    def _calculate_pars_fortuna(
        self, 
        sun: Dict[str, Any], 
        moon: Dict[str, Any], 
        ascendant: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate Part of Fortune.
        
        Formula: Ascendant + Moon - Sun
        
        Args:
            sun: Sun position data
            moon: Moon position data
            ascendant: Ascendant position data
            
        Returns:
            Part of Fortune position data
        """
        # Calculate longitude
        longitude = (ascendant["longitude"] + moon["longitude"] - sun["longitude"]) % 360
        sign_idx = int(longitude / 30)
        degree = longitude % 30
        
        return {
            "longitude": longitude,
            "sign": self.signs[sign_idx],
            "degree": degree
        }
    
    def _get_house_number(self, longitude: float, house_cusps: Dict[int, Dict[str, Any]]) -> int:
        """
        Determine the house number for a given longitude.
        
        Args:
            longitude: Celestial longitude in degrees
            house_cusps: Dictionary of house cusps
            
        Returns:
            House number (1-12)
        """
        # Extract house cusp longitudes
        cusp_longitudes = [house_cusps[i+1]["longitude"] for i in range(12)]
        
        # Find the house
        for i in range(12):
            next_i = (i + 1) % 12
            
            # Check if the longitude is between this cusp and the next
            if cusp_longitudes[i] <= cusp_longitudes[next_i]:
                # Regular case
                if cusp_longitudes[i] <= longitude < cusp_longitudes[next_i]:
                    return i + 1
            else:
                # Cusps cross 0°
                if longitude >= cusp_longitudes[i] or longitude < cusp_longitudes[next_i]:
                    return i + 1
        
        # Default to 1st house if house can't be determined
        return 1
    
    def _get_dominant_elements(self, positions: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate the dominant elements based on planet positions.
        
        Args:
            positions: Dictionary of planet positions
            
        Returns:
            Dictionary with element counts
        """
        elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
        
        for planet, data in positions.items():
            if "sign" in data:
                element = self.elements.get(data["sign"])
                if element:
                    elements[element] += 1
        
        return elements
    
    def _get_dominant_modalities(self, positions: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate the dominant modalities based on planet positions.
        
        Args:
            positions: Dictionary of planet positions
            
        Returns:
            Dictionary with modality counts
        """
        modalities = {"Cardinal": 0, "Fixed": 0, "Mutable": 0}
        
        for planet, data in positions.items():
            if "sign" in data:
                modality = self.modalities.get(data["sign"])
                if modality:
                    modalities[modality] += 1
        
        return modalities

# Create a singleton instance
ephemeris_service = EphemerisService()
