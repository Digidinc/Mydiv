"""
Progressions Service

This module provides a service for calculating progressed charts.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from loguru import logger

from models.progressions import ProgressionOptions
from models.birth_data import BirthData
from services.ephemeris import ephemeris_service
from services.transits import transit_service
from services.birth_chart import BirthChartService

# Create birth chart service for calculations
birth_chart_service = BirthChartService()

class ProgressionService:
    """Service for progression calculations."""
    
    def __init__(self):
        """Initialize the progressions service."""
        # Different progression methods
        self.progression_methods = {
            "secondary": self._calculate_secondary_progressions,
            "tertiary": self._calculate_tertiary_progressions,
            "solar_arc": self._calculate_solar_arc_progressions,
            "minor": self._calculate_minor_progressions
        }
    
    async def calculate_progressions(
        self,
        birth_data: BirthData,
        progression_date: str,
        options: ProgressionOptions
    ) -> Dict[str, Any]:
        """
        Calculate a progressed chart.
        
        Args:
            birth_data: Birth data including date, time, and location
            progression_date: Date for progression calculation
            options: Progression options
            
        Returns:
            Progressed chart data
        """
        try:
            # Determine progression method
            progression_method = options.progression_type.lower()
            
            # Get method function
            method_func = self.progression_methods.get(progression_method)
            if not method_func:
                raise ValueError(f"Unsupported progression method: {progression_method}")
            
            # Calculate progressed chart using selected method
            progressed_chart = await method_func(
                birth_data=birth_data,
                progression_date=progression_date,
                planets=options.planets,
                include_houses=options.include_houses
            )
            
            logger.info(f"Calculated {progression_method} progressions for {progression_date}")
            return progressed_chart
            
        except Exception as e:
            logger.error(f"Error calculating progressions: {str(e)}")
            raise
    
    async def calculate_secondary_progressions(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        progression_date: str = None,
        planets: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate secondary progressions for a given birth chart.
        
        Secondary progressions use the "day for a year" principle.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM:SS format (optional)
            birth_latitude: Birth latitude (optional)
            birth_longitude: Birth longitude (optional)
            progression_date: Progression date (defaults to current date)
            planets: List of planets to include (defaults to all)
            
        Returns:
            Dictionary of progressed planet positions
        """
        try:
            # Set default values
            if not progression_date:
                progression_date = datetime.now().strftime("%Y-%m-%d")
            
            if not planets:
                planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]
            
            if not birth_time:
                birth_time = "12:00:00"
            
            # Parse dates
            birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
            progression_dt = datetime.strptime(progression_date, "%Y-%m-%d")
            
            # Calculate years between birth and progression date
            # This is simplified - a more accurate calculation would account for leap years
            years = (progression_dt - birth_dt).days / 365.25
            
            # Calculate progressed date (birth date + years in days)
            days = int(years)
            day_fraction = years - days
            hours = int(day_fraction * 24)
            minutes = int((day_fraction * 24 - hours) * 60)
            seconds = int(((day_fraction * 24 - hours) * 60 - minutes) * 60)
            
            progressed_dt = birth_dt + timedelta(days=days)
            progressed_dt = progressed_dt.replace(
                hour=birth_dt.hour + hours,
                minute=birth_dt.minute + minutes,
                second=birth_dt.second + seconds
            )
            
            # Format progressed date and time
            progressed_date = progressed_dt.strftime("%Y-%m-%d")
            progressed_time = progressed_dt.strftime("%H:%M:%S")
            
            # Calculate positions for progressed date
            progressed_positions = await ephemeris_service.calculate_planet_positions(
                date=progressed_date,
                time=progressed_time,
                latitude=birth_latitude,
                longitude=birth_longitude,
                planets=planets
            )
            
            logger.info(f"Calculated secondary progressions for {progression_date} using progressed date {progressed_date}")
            return progressed_positions
            
        except Exception as e:
            logger.error(f"Error calculating secondary progressions: {str(e)}")
            raise
    
    async def calculate_progression_timeline(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        start_date: str = None,
        end_date: str = None,
        interval_months: int = 6,
        planet: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate a timeline of progressions for a period of time.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM:SS format (optional)
            birth_latitude: Birth latitude (optional)
            birth_longitude: Birth longitude (optional)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            interval_months: Interval in months between calculations
            planet: Specific planet to track (defaults to all major planets)
            
        Returns:
            Timeline of progressed positions
        """
        try:
            # Set default values
            if not start_date:
                start_date = datetime.now().strftime("%Y-%m-%d")
            
            if not end_date:
                # Default to 5 years from start date
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = start_dt + timedelta(days=365 * 5)
                end_date = end_dt.strftime("%Y-%m-%d")
            
            # Determine which planets to track
            planets_to_track = [planet] if planet else ["sun", "moon", "mercury", "venus", "mars"]
            
            # Parse dates
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Calculate number of intervals
            months = (end_dt.year - start_dt.year) * 12 + end_dt.month - start_dt.month
            intervals = months // interval_months + 1
            
            # Initialize timeline
            timeline = []
            
            # Calculate progressions for each interval
            for i in range(intervals):
                # Calculate date for this interval
                current_dt = start_dt
                if i > 0:
                    # Add months to date
                    new_month = start_dt.month + (i * interval_months)
                    new_year = start_dt.year + (new_month - 1) // 12
                    new_month = ((new_month - 1) % 12) + 1
                    
                    # Create new date (handling month length differences)
                    current_dt = datetime(new_year, new_month, min(start_dt.day, 28))
                
                current_date = current_dt.strftime("%Y-%m-%d")
                
                # Calculate progressions for this date
                progressed_positions = await self.calculate_secondary_progressions(
                    birth_date=birth_date,
                    birth_time=birth_time,
                    birth_latitude=birth_latitude,
                    birth_longitude=birth_longitude,
                    progression_date=current_date,
                    planets=planets_to_track
                )
                
                # Track sign changes
                if i > 0 and planet:
                    prev_positions = timeline[-1]["positions"]
                    current_sign = progressed_positions[planet]["sign"]
                    prev_sign = prev_positions[planet]["sign"]
                    
                    if current_sign != prev_sign:
                        # This is a sign change (ingress)
                        progressed_positions[planet]["ingress"] = True
                
                # Add to timeline
                timeline_entry = {
                    "date": current_date,
                    "positions": {}
                }
                
                # Format positions
                for p in planets_to_track:
                    if p in progressed_positions:
                        timeline_entry["positions"][p] = {
                            "sign": progressed_positions[p]["sign"],
                            "degree": progressed_positions[p]["degree"],
                            "retrograde": progressed_positions[p].get("retrograde", False),
                            "ingress": progressed_positions[p].get("ingress", False)
                        }
                
                timeline.append(timeline_entry)
            
            logger.info(f"Calculated progression timeline with {len(timeline)} entries from {start_date} to {end_date}")
            return timeline
            
        except Exception as e:
            logger.error(f"Error calculating progression timeline: {str(e)}")
            raise
    
    async def calculate_progressed_chart_with_transits(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        calculation_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate a progressed chart with current transits.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM:SS format (optional)
            birth_latitude: Birth latitude (optional)
            birth_longitude: Birth longitude (optional)
            calculation_date: Date for calculation (defaults to current date)
            
        Returns:
            Dictionary with progressed chart and transit aspects
        """
        try:
            # Set default values
            if not calculation_date:
                calculation_date = datetime.now().strftime("%Y-%m-%d")
            
            # Calculate natal chart
            natal_chart = await birth_chart_service.calculate_chart_summary(
                date=birth_date,
                time=birth_time,
                latitude=birth_latitude,
                longitude=birth_longitude
            )
            
            # Extract natal positions
            natal_positions = {
                planet: data["longitude"] 
                for planet, data in natal_chart["planets"].items()
            }
            
            # Calculate progressed positions
            progressed_positions = await self.calculate_secondary_progressions(
                birth_date=birth_date,
                birth_time=birth_time,
                birth_latitude=birth_latitude,
                birth_longitude=birth_longitude,
                progression_date=calculation_date
            )
            
            # Extract progressed longitudes
            progressed_longitudes = {
                planet: data["longitude"] 
                for planet, data in progressed_positions.items()
            }
            
            # Calculate transits to natal chart
            transits_to_natal = await transit_service.calculate_transits(
                natal_positions=natal_positions,
                transit_time={"date": calculation_date, "time": "12:00:00"},
                options={
                    "aspects": ["conjunction", "opposition", "trine", "square", "sextile"],
                    "orbs": {
                        "conjunction": 1.0,
                        "opposition": 1.0,
                        "trine": 0.8,
                        "square": 0.8,
                        "sextile": 0.6
                    },
                    "planets": ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
                }
            )
            
            # Calculate transits to progressed chart
            transits_to_progressed = await transit_service.calculate_transits(
                natal_positions=progressed_longitudes,
                transit_time={"date": calculation_date, "time": "12:00:00"},
                options={
                    "aspects": ["conjunction", "opposition", "trine", "square", "sextile"],
                    "orbs": {
                        "conjunction": 1.0,
                        "opposition": 1.0,
                        "trine": 0.8,
                        "square": 0.8,
                        "sextile": 0.6
                    },
                    "planets": ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
                }
            )
            
            logger.info(f"Calculated progressed chart with transits for {calculation_date}")
            return {
                "calculation_date": calculation_date,
                "progressed_positions": progressed_positions,
                "transits_to_natal": transits_to_natal,
                "transits_to_progressed": transits_to_progressed
            }
            
        except Exception as e:
            logger.error(f"Error calculating progressed chart with transits: {str(e)}")
            raise
    
    async def _calculate_secondary_progressions(
        self,
        birth_data: BirthData,
        progression_date: str,
        planets: List[str],
        include_houses: bool
    ) -> Dict[str, Any]:
        """
        Calculate secondary progressions.
        
        Secondary progressions use the "day for a year" principle.
        
        Args:
            birth_data: Birth data
            progression_date: Progression date
            planets: List of planets to include
            include_houses: Whether to include house positions
            
        Returns:
            Dictionary with progressed chart data
        """
        # Extract birth data
        birth_date = birth_data.date
        birth_time = birth_data.time
        
        # Extract location if available
        birth_latitude = None
        birth_longitude = None
        if birth_data.location:
            birth_latitude = birth_data.location.latitude
            birth_longitude = birth_data.location.longitude
        
        # Calculate secondary progressions
        progressed_positions = await self.calculate_secondary_progressions(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
            progression_date=progression_date,
            planets=planets
        )
        
        # Create result structure
        result = {
            "positions": progressed_positions
        }
        
        # Calculate houses if requested and location available
        if include_houses and birth_latitude and birth_longitude:
            # Parse dates
            birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
            progression_dt = datetime.strptime(progression_date, "%Y-%m-%d")
            
            # For secondary progressions, houses are often calculated using the birth location
            # but with the local sidereal time for the progressed date
            # This is a simplification - actual house calculation would be more complex
            
            # Calculate progressed date
            years = (progression_dt - birth_dt).days / 365.25
            progressed_dt = birth_dt + timedelta(days=int(years))
            progressed_date = progressed_dt.strftime("%Y-%m-%d")
            
            # Calculate houses (using current time)
            house_data = await ephemeris_service._calculate_houses(
                jd=ephemeris_service._date_to_jd(progression_dt),
                lat=birth_latitude,
                lng=birth_longitude
            )
            
            # Add houses to result
            result["houses"] = house_data["cusps"]
        
        return result
    
    async def _calculate_tertiary_progressions(
        self,
        birth_data: BirthData,
        progression_date: str,
        planets: List[str],
        include_houses: bool
    ) -> Dict[str, Any]:
        """
        Calculate tertiary progressions.
        
        Tertiary progressions use the "day for a lunar month" principle.
        
        Args:
            birth_data: Birth data
            progression_date: Progression date
            planets: List of planets to include
            include_houses: Whether to include house positions
            
        Returns:
            Dictionary with progressed chart data
        """
        # Extract birth data
        birth_date = birth_data.date
        birth_time = birth_data.time
        
        # Extract location if available
        birth_latitude = None
        birth_longitude = None
        if birth_data.location:
            birth_latitude = birth_data.location.latitude
            birth_longitude = birth_data.location.longitude
        
        # Parse dates
        birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
        progression_dt = datetime.strptime(progression_date, "%Y-%m-%d")
        
        # Calculate lunar months between birth and progression date
        # A lunar month is approximately 27.32 days (sidereal month)
        lunar_month_days = 27.32
        days_diff = (progression_dt - birth_dt).days
        lunar_months = days_diff / lunar_month_days
        
        # Calculate progressed date (birth date + lunar months in days)
        progressed_dt = birth_dt + timedelta(days=lunar_months)
        
        # Format progressed date and time
        progressed_date = progressed_dt.strftime("%Y-%m-%d")
        progressed_time = progressed_dt.strftime("%H:%M:%S")
        
        # Calculate positions for progressed date
        progressed_positions = await ephemeris_service.calculate_planet_positions(
            date=progressed_date,
            time=progressed_time,
            latitude=birth_latitude,
            longitude=birth_longitude,
            planets=planets
        )
        
        # Create result structure
        result = {
            "positions": progressed_positions
        }
        
        # Calculate houses if requested and location available
        if include_houses and birth_latitude and birth_longitude:
            # For tertiary progressions, houses are calculated similarly to secondary
            # but using the tertiary progressed date
            
            # Calculate houses (using current time)
            house_data = await ephemeris_service._calculate_houses(
                jd=ephemeris_service._date_to_jd(progressed_dt),
                lat=birth_latitude,
                lng=birth_longitude
            )
            
            # Add houses to result
            result["houses"] = house_data["cusps"]
        
        return result
    
    async def _calculate_solar_arc_progressions(
        self,
        birth_data: BirthData,
        progression_date: str,
        planets: List[str],
        include_houses: bool
    ) -> Dict[str, Any]:
        """
        Calculate solar arc progressions.
        
        Solar arc progressions move all planets by the same arc that the progressed Sun has moved.
        
        Args:
            birth_data: Birth data
            progression_date: Progression date
            planets: List of planets to include
            include_houses: Whether to include house positions
            
        Returns:
            Dictionary with progressed chart data
        """
        # Extract birth data
        birth_date = birth_data.date
        birth_time = birth_data.time
        
        # Extract location if available
        birth_latitude = None
        birth_longitude = None
        if birth_data.location:
            birth_latitude = birth_data.location.latitude
            birth_longitude = birth_data.location.longitude
        
        # Calculate natal positions
        natal_positions = await ephemeris_service.calculate_planet_positions(
            date=birth_date,
            time=birth_time,
            latitude=birth_latitude,
            longitude=birth_longitude,
            planets=planets + ["sun"]  # Ensure Sun is included
        )
        
        # Calculate secondary progressed Sun position
        secondary_progressed = await self.calculate_secondary_progressions(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
            progression_date=progression_date,
            planets=["sun"]
        )
        
        # Calculate solar arc (difference between progressed and natal Sun)
        natal_sun_longitude = natal_positions["sun"]["longitude"]
        progressed_sun_longitude = secondary_progressed["sun"]["longitude"]
        
        solar_arc = progressed_sun_longitude - natal_sun_longitude
        if solar_arc < 0:
            solar_arc += 360  # Ensure positive arc
        
        # Apply solar arc to all natal positions
        progressed_positions = {}
        for planet in planets:
            if planet in natal_positions:
                # Get natal position
                natal_position = natal_positions[planet]
                
                # Calculate progressed longitude
                progressed_longitude = (natal_position["longitude"] + solar_arc) % 360
                
                # Determine sign and degree
                sign_idx = int(progressed_longitude / 30)
                degree = progressed_longitude % 30
                
                # Create progressed position
                progressed_positions[planet] = {
                    "longitude": progressed_longitude,
                    "sign": ephemeris_service.signs[sign_idx],
                    "degree": degree,
                    "retrograde": natal_position.get("retrograde", False)  # Maintain natal retrograde status
                }
        
        # Create result structure
        result = {
            "positions": progressed_positions
        }
        
        # Calculate houses if requested and location available
        if include_houses and birth_latitude and birth_longitude:
            # For solar arc, houses are typically calculated using the solar arc applied to house cusps
            
            # Get natal houses
            natal_house_data = await ephemeris_service._calculate_houses(
                jd=ephemeris_service._date_to_jd(datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")),
                lat=birth_latitude,
                lng=birth_longitude
            )
            
            # Apply solar arc to house cusps
            progressed_houses = {}
            for house_num, house_data in natal_house_data["cusps"].items():
                # Calculate progressed longitude
                progressed_longitude = (house_data["longitude"] + solar_arc) % 360
                
                # Determine sign and degree
                sign_idx = int(progressed_longitude / 30)
                degree = progressed_longitude % 30
                
                # Create progressed house position
                progressed_houses[house_num] = {
                    "longitude": progressed_longitude,
                    "sign": ephemeris_service.signs[sign_idx],
                    "degree": degree
                }
            
            # Add houses to result
            result["houses"] = progressed_houses
        
        return result
    
    async def _calculate_minor_progressions(
        self,
        birth_data: BirthData,
        progression_date: str,
        planets: List[str],
        include_houses: bool
    ) -> Dict[str, Any]:
        """
        Calculate minor progressions.
        
        Minor progressions use the "month for a year" principle.
        
        Args:
            birth_data: Birth data
            progression_date: Progression date
            planets: List of planets to include
            include_houses: Whether to include house positions
            
        Returns:
            Dictionary with progressed chart data
        """
        # Extract birth data
        birth_date = birth_data.date
        birth_time = birth_data.time
        
        # Extract location if available
        birth_latitude = None
        birth_longitude = None
        if birth_data.location:
            birth_latitude = birth_data.location.latitude
            birth_longitude = birth_data.location.longitude
        
        # Parse dates
        birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
        progression_dt = datetime.strptime(progression_date, "%Y-%m-%d")
        
        # Calculate years between birth and progression date
        years = (progression_dt - birth_dt).days / 365.25
        
        # For minor progressions, 1 month = 1 year
        # So, add (years × 30.44) days to birth date (approximation)
        month_days = 30.44  # Average days in a month
        days_to_add = years * month_days
        
        # Calculate progressed date
        progressed_dt = birth_dt + timedelta(days=days_to_add)
        
        # Format progressed date and time
        progressed_date = progressed_dt.strftime("%Y-%m-%d")
        progressed_time = progressed_dt.strftime("%H:%M:%S")
        
        # Calculate positions for progressed date
        progressed_positions = await ephemeris_service.calculate_planet_positions(
            date=progressed_date,
            time=progressed_time,
            latitude=birth_latitude,
            longitude=birth_longitude,
            planets=planets
        )
        
        # Create result structure
        result = {
            "positions": progressed_positions
        }
        
        # Calculate houses if requested and location available
        if include_houses and birth_latitude and birth_longitude:
            # Calculate houses for the progressed date
            house_data = await ephemeris_service._calculate_houses(
                jd=ephemeris_service._date_to_jd(progressed_dt),
                lat=birth_latitude,
                lng=birth_longitude
            )
            
            # Add houses to result
            result["houses"] = house_data["cusps"]
        
        return result

# Create a singleton instance
progression_service = ProgressionService()
