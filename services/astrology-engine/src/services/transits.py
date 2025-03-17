"""
Transits Service

This module provides a service for calculating transit aspects to a natal chart.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from loguru import logger

from models.transits import TransitOptions
from services.ephemeris import ephemeris_service
from services.aspects import AspectService
from services.birth_chart import BirthChartService

# Create aspect service for calculations
aspect_service = AspectService()
birth_chart_service = BirthChartService()

class TransitService:
    """Service for transit calculations."""
    
    def __init__(self):
        """Initialize the transits service."""
        self.aspect_service = aspect_service
    
    async def calculate_transits(
        self,
        natal_positions: Dict[str, float],
        transit_time: Dict[str, Any],
        options: TransitOptions
    ) -> List[Dict[str, Any]]:
        """
        Calculate transit aspects to a natal chart.
        
        Args:
            natal_positions: Dictionary of natal planet names and their longitudes
            transit_time: Time point for transit calculation
            options: Transit calculation options
            
        Returns:
            List of transit aspects
        """
        try:
            # Get transit date and time
            transit_date = transit_time["date"]
            transit_time_str = transit_time["time"]
            
            # Calculate transit positions
            transit_positions = await ephemeris_service.calculate_planet_positions(
                date=transit_date,
                time=transit_time_str,
                planets=options.planets
            )
            
            # Extract longitudes
            transit_longitudes = {p: pos["longitude"] for p, pos in transit_positions.items()}
            
            # Format for aspect calculation
            merged_positions = {}
            
            # Add natal positions with prefix "natal_"
            for planet, longitude in natal_positions.items():
                merged_positions[f"natal_{planet}"] = longitude
            
            # Add transit positions with prefix "transit_"
            for planet, longitude in transit_longitudes.items():
                merged_positions[f"transit_{planet}"] = longitude
            
            # Create aspect options from transit options
            aspect_options = {
                "aspects": options.aspects,
                "orbs": options.orbs
            }
            
            # Calculate aspects between all planets
            all_aspects = await self.aspect_service.calculate_aspects(
                planet_positions=merged_positions,
                options=aspect_options
            )
            
            # Filter to only include aspects between natal and transit planets
            transit_aspects = []
            for aspect in all_aspects:
                # Check if aspect is between natal and transit planets
                is_transit_aspect = (
                    (aspect["planet1"].startswith("natal_") and aspect["planet2"].startswith("transit_")) or
                    (aspect["planet1"].startswith("transit_") and aspect["planet2"].startswith("natal_"))
                )
                
                if is_transit_aspect:
                    # Format the aspect for transit response
                    formatted_aspect = {}
                    
                    # Determine which is the transit planet and which is the natal planet
                    if aspect["planet1"].startswith("transit_"):
                        formatted_aspect["transit_planet"] = aspect["planet1"].replace("transit_", "")
                        formatted_aspect["natal_planet"] = aspect["planet2"].replace("natal_", "")
                    else:
                        formatted_aspect["transit_planet"] = aspect["planet2"].replace("transit_", "")
                        formatted_aspect["natal_planet"] = aspect["planet1"].replace("natal_", "")
                    
                    # Add other aspect details
                    formatted_aspect["aspect"] = aspect["type"]
                    formatted_aspect["orb"] = aspect["orb"]
                    formatted_aspect["applying"] = aspect["applying"]
                    formatted_aspect["influence"] = aspect["influence"]
                    
                    # Add transit planet's sign and retrograde status
                    transit_planet = formatted_aspect["transit_planet"]
                    if transit_planet in transit_positions:
                        formatted_aspect["transit_sign"] = transit_positions[transit_planet]["sign"]
                        formatted_aspect["retrograde"] = transit_positions[transit_planet].get("retrograde", False)
                    
                    # Calculate exact date
                    exact_date = await self._calculate_exact_date(
                        transit_planet=formatted_aspect["transit_planet"],
                        natal_planet=formatted_aspect["natal_planet"],
                        natal_longitude=natal_positions[formatted_aspect["natal_planet"]],
                        transit_longitude=transit_longitudes[formatted_aspect["transit_planet"]],
                        aspect_type=formatted_aspect["aspect"],
                        transit_date=transit_date,
                        applying=formatted_aspect["applying"]
                    )
                    
                    if exact_date:
                        formatted_aspect["exact_date"] = exact_date
                    
                    transit_aspects.append(formatted_aspect)
            
            logger.info(f"Calculated {len(transit_aspects)} transit aspects for {transit_date}")
            return transit_aspects
            
        except Exception as e:
            logger.error(f"Error calculating transits: {str(e)}")
            raise
    
    async def calculate_transit_period(
        self,
        natal_positions: Dict[str, float],
        start_date: str,
        end_date: str,
        planets: Optional[List[str]] = None,
        aspects: Optional[List[str]] = None,
        orbs: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate transits over a period of time.
        
        Args:
            natal_positions: Dictionary of natal planet names and their longitudes
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            planets: Transit planets to include
            aspects: Aspect types to include
            orbs: Maximum orb for each aspect type
            
        Returns:
            Timeline of transit events sorted by date
        """
        try:
            # Set defaults if not provided
            if not planets:
                planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
            
            if not aspects:
                aspects = ["conjunction", "opposition", "trine", "square", "sextile"]
            
            if not orbs:
                orbs = {
                    "conjunction": 1.0,
                    "opposition": 1.0,
                    "trine": 0.8,
                    "square": 0.8,
                    "sextile": 0.6
                }
            
            # Parse dates
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Calculate number of days
            days = (end_dt - start_dt).days + 1
            
            # Initialize timeline
            transit_timeline = []
            
            # Check each day (or use a more efficient approach for longer periods)
            for i in range(0, days, 1):  # Sample every day
                current_dt = start_dt + timedelta(days=i)
                current_date = current_dt.strftime("%Y-%m-%d")
                
                # Set up transit options
                options = TransitOptions(
                    aspects=aspects,
                    orbs=orbs,
                    planets=planets
                )
                
                # Calculate transits for this day
                transits = await self.calculate_transits(
                    natal_positions=natal_positions,
                    transit_time={"date": current_date, "time": "12:00:00"},
                    options=options
                )
                
                # Filter for exact or near-exact transits
                for transit in transits:
                    if transit.get("exact_date") == current_date or transit["orb"] < 0.1:
                        # Format for timeline
                        event = {
                            "date": current_date,
                            "transit_planet": transit["transit_planet"],
                            "natal_planet": transit["natal_planet"],
                            "aspect": transit["aspect"],
                            "applying": transit["applying"],
                            "planet_retrograde": transit.get("retrograde", False)
                        }
                        
                        # Add to timeline if not already present
                        if not any(
                            t["date"] == event["date"] and 
                            t["transit_planet"] == event["transit_planet"] and
                            t["natal_planet"] == event["natal_planet"] and
                            t["aspect"] == event["aspect"]
                            for t in transit_timeline
                        ):
                            transit_timeline.append(event)
            
            # Sort timeline by date
            transit_timeline.sort(key=lambda x: x["date"])
            
            logger.info(f"Calculated transit timeline with {len(transit_timeline)} events from {start_date} to {end_date}")
            return transit_timeline
            
        except Exception as e:
            logger.error(f"Error calculating transit period: {str(e)}")
            raise
    
    async def generate_five_year_forecast(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        start_date: Optional[str] = None,
        transit_planets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a 5-year forecast of significant transits.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM:SS format (optional)
            birth_latitude: Birth latitude (optional)
            birth_longitude: Birth longitude (optional)
            start_date: Start date in YYYY-MM-DD format (defaults to current date)
            transit_planets: List of transit planets to include
            
        Returns:
            Dictionary with forecast data
        """
        try:
            # Set default values
            if not start_date:
                start_date = datetime.now().strftime("%Y-%m-%d")
            
            if not transit_planets:
                transit_planets = ["jupiter", "saturn", "uranus", "neptune", "pluto"]
            
            # Calculate end date (5 years from start)
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = start_dt + timedelta(days=365 * 5)
            end_date = end_dt.strftime("%Y-%m-%d")
            
            # First, calculate the natal chart
            birth_data = {
                "date": birth_date,
                "time": birth_time or "12:00:00"
            }
            
            if birth_latitude and birth_longitude:
                birth_data["location"] = {
                    "latitude": birth_latitude,
                    "longitude": birth_longitude
                }
            
            # Calculate natal chart using the birth chart service
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
                if planet in ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "ascendant", "mc"]
            }
            
            # Define significant aspects for the forecast
            significant_aspects = ["conjunction", "opposition", "square"]
            
            # Calculate transits
            transits = await self.calculate_transit_period(
                natal_positions=natal_positions,
                start_date=start_date,
                end_date=end_date,
                planets=transit_planets,
                aspects=significant_aspects
            )
            
            # Identify major life events (significant transits to Sun, Moon, Ascendant)
            life_events = []
            for transit in transits:
                is_major = (
                    transit["natal_planet"] in ["sun", "moon", "ascendant"] and
                    transit["transit_planet"] in ["jupiter", "saturn", "uranus", "neptune", "pluto"] and
                    transit["aspect"] in ["conjunction", "opposition", "square"]
                )
                
                if is_major:
                    # Add description
                    description = self._get_transit_description(
                        transit["transit_planet"],
                        transit["natal_planet"],
                        transit["aspect"]
                    )
                    
                    life_event = transit.copy()
                    life_event["description"] = description
                    life_event["significance"] = "major" if transit["aspect"] in ["conjunction", "opposition"] else "significant"
                    
                    life_events.append(life_event)
            
            logger.info(f"Generated 5-year forecast with {len(transits)} transits and {len(life_events)} major life events")
            return {
                "start_date": start_date,
                "end_date": end_date,
                "transits": transits,
                "life_events": life_events
            }
            
        except Exception as e:
            logger.error(f"Error generating 5-year forecast: {str(e)}")
            raise
    
    async def calculate_current_transits(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        orb: Optional[float] = 1.0
    ) -> List[Dict[str, Any]]:
        """
        Get current planetary transits to a natal chart.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM:SS format (optional)
            birth_latitude: Birth latitude (optional)
            birth_longitude: Birth longitude (optional)
            orb: Maximum orb in degrees
            
        Returns:
            List of active transits
        """
        try:
            # Get current date
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M:%S")
            
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
            
            # Define aspect types with custom orbs based on input orb
            aspects = ["conjunction", "opposition", "trine", "square", "sextile"]
            custom_orbs = {
                "conjunction": orb,
                "opposition": orb,
                "trine": orb,
                "square": orb,
                "sextile": orb
            }
            
            # Set up transit options
            options = TransitOptions(
                aspects=aspects,
                orbs=custom_orbs,
                planets=["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
            )
            
            # Calculate current transits
            transits = await self.calculate_transits(
                natal_positions=natal_positions,
                transit_time={"date": current_date, "time": current_time},
                options=options
            )
            
            # Add descriptions to transits
            for transit in transits:
                description = self._get_transit_description(
                    transit["transit_planet"],
                    transit["natal_planet"],
                    transit["aspect"]
                )
                transit["description"] = description
            
            logger.info(f"Calculated {len(transits)} current transits for birth date {birth_date}")
            return transits
            
        except Exception as e:
            logger.error(f"Error calculating current transits: {str(e)}")
            raise
    
    async def _calculate_exact_date(
        self,
        transit_planet: str,
        natal_planet: str,
        natal_longitude: float,
        transit_longitude: float,
        aspect_type: str,
        transit_date: str,
        applying: bool
    ) -> Optional[str]:
        """
        Calculate the date when a transit aspect becomes exact.
        
        This is a simplified approach that estimates the exact date based on
        planet speeds and current positions.
        
        Args:
            transit_planet: Transiting planet
            natal_planet: Natal planet
            natal_longitude: Longitude of natal planet
            transit_longitude: Longitude of transit planet
            aspect_type: Aspect type
            transit_date: Current transit date
            applying: Whether the aspect is applying
            
        Returns:
            Date string when the aspect becomes exact, or None if unknown
        """
        try:
            # Get aspect angle
            aspect_angle = self.aspect_service.aspect_angles.get(aspect_type, 0)
            
            # Calculate the target longitude for exact aspect
            target_longitude = (natal_longitude + aspect_angle) % 360
            
            # Get planet speeds
            planet_speeds = self.aspect_service.default_speeds
            speed = planet_speeds.get(transit_planet, 1.0)  # Degrees per day
            
            # If planet is retrograde, adjust speed
            if not applying:
                speed = -speed
            
            # Calculate angular distance
            angular_distance = (target_longitude - transit_longitude) % 360
            if angular_distance > 180:
                angular_distance = 360 - angular_distance
            
            # Calculate days until exact
            days_until_exact = angular_distance / abs(speed) if speed != 0 else 0
            
            # Round to nearest day
            days_until_exact = round(days_until_exact)
            
            # Calculate exact date
            current_dt = datetime.strptime(transit_date, "%Y-%m-%d")
            exact_dt = current_dt + timedelta(days=days_until_exact)
            
            # Format date
            exact_date = exact_dt.strftime("%Y-%m-%d")
            
            return exact_date
            
        except Exception as e:
            logger.error(f"Error calculating exact date: {str(e)}")
            return None
    
    def _get_transit_description(
        self,
        transit_planet: str,
        natal_planet: str,
        aspect_type: str
    ) -> str:
        """
        Generate a description for a transit aspect.
        
        This is a simplified approach that returns generic descriptions.
        A more comprehensive system would consider many more factors.
        
        Args:
            transit_planet: Transiting planet
            natal_planet: Natal planet
            aspect_type: Aspect type
            
        Returns:
            Description string
        """
        # This is a very simplified approach - real descriptions would be more nuanced
        descriptions = {
            # Jupiter transits
            ("jupiter", "sun", "conjunction"): "A period of growth, optimism, and expanded opportunities. Good for success and recognition.",
            ("jupiter", "moon", "conjunction"): "Emotional well-being, increased happiness, and domestic improvements.",
            ("jupiter", "ascendant", "conjunction"): "Personal growth, new opportunities, and increased confidence.",
            ("jupiter", "sun", "opposition"): "Potential for overdoing things or being overconfident. Need for balance.",
            ("jupiter", "moon", "opposition"): "Emotional excess or overindulgence. Challenge to find internal balance.",
            
            # Saturn transits
            ("saturn", "sun", "conjunction"): "A period of responsibility, limitations, and hard work. Important for character building.",
            ("saturn", "moon", "conjunction"): "Emotional restrictions and tests of emotional maturity.",
            ("saturn", "ascendant", "conjunction"): "Testing of identity and how you present yourself to the world.",
            ("saturn", "sun", "opposition"): "Challenges from authority figures or obstacles to personal goals.",
            ("saturn", "moon", "opposition"): "Emotional heaviness and potential family challenges.",
            
            # Uranus transits
            ("uranus", "sun", "conjunction"): "Sudden changes, unexpected events, and a desire for greater independence.",
            ("uranus", "moon", "conjunction"): "Emotional unpredictability and domestic changes.",
            ("uranus", "ascendant", "conjunction"): "Dramatic shifts in self-image and how others see you.",
            ("uranus", "sun", "opposition"): "Disruptions from outside forces, unexpected challenges to identity.",
            ("uranus", "moon", "opposition"): "Emotional upheaval and changes in home or family life.",
            
            # Neptune transits
            ("neptune", "sun", "conjunction"): "Increased sensitivity, spirituality, and potential confusion about direction.",
            ("neptune", "moon", "conjunction"): "Heightened emotional sensitivity and potential for emotional confusion.",
            ("neptune", "ascendant", "conjunction"): "Blurring of self-image and increased sensitivity to environments.",
            ("neptune", "sun", "opposition"): "Challenges with clarity and potential for deception from others.",
            ("neptune", "moon", "opposition"): "Emotional confusion and sensitivity to atmospheric conditions.",
            
            # Pluto transits
            ("pluto", "sun", "conjunction"): "Profound personal transformation and empowerment through challenges.",
            ("pluto", "moon", "conjunction"): "Deep emotional transformation and facing of emotional patterns.",
            ("pluto", "ascendant", "conjunction"): "Powerful identity transformation and rebirth.",
            ("pluto", "sun", "opposition"): "Power struggles with others and confrontation with deep psychological material.",
            ("pluto", "moon", "opposition"): "Intense emotional experiences and potential family dynamics transformation."
        }
        
        # Try to get specific description
        key = (transit_planet, natal_planet, aspect_type)
        description = descriptions.get(key)
        
        # If no specific description, provide a generic one
        if not description:
            if aspect_type == "conjunction":
                description = f"Transit {transit_planet.capitalize()} conjunct natal {natal_planet.capitalize()}: A significant period of merging and intensifying {natal_planet} qualities."
            elif aspect_type == "opposition":
                description = f"Transit {transit_planet.capitalize()} opposite natal {natal_planet.capitalize()}: A time of balance and integration between opposing forces."
            elif aspect_type == "trine":
                description = f"Transit {transit_planet.capitalize()} trine natal {natal_planet.capitalize()}: A period of ease and flow related to {natal_planet} qualities."
            elif aspect_type == "square":
                description = f"Transit {transit_planet.capitalize()} square natal {natal_planet.capitalize()}: A time of tension and productive challenges related to {natal_planet} qualities."
            elif aspect_type == "sextile":
                description = f"Transit {transit_planet.capitalize()} sextile natal {natal_planet.capitalize()}: An opportunity for growth and development of {natal_planet} qualities."
        
        return description

# Create a singleton instance
transit_service = TransitService()
