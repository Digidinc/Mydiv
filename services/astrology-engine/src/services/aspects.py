"""
Aspects Service

This module provides a service for calculating aspects between planets.
"""
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from loguru import logger

from models.aspects import AspectOptions, AspectConfigRequest
from services.ephemeris import ephemeris_service

class AspectService:
    """Service for aspect calculations."""
    
    def __init__(self):
        """Initialize the aspects service."""
        # Aspect types with their angles in degrees
        self.aspect_angles = {
            "conjunction": 0,
            "opposition": 180,
            "trine": 120,
            "square": 90,
            "sextile": 60,
            "quincunx": 150,
            "semi_sextile": 30,
            "semi_square": 45,
            "sesquiquadrate": 135,
            "quintile": 72
        }
        
        # Default orbs based on aspect
        self.default_orbs = {
            "conjunction": 8.0,
            "opposition": 8.0,
            "trine": 6.0,
            "square": 6.0,
            "sextile": 4.0,
            "quincunx": 3.0,
            "semi_sextile": 2.0,
            "semi_square": 2.0,
            "sesquiquadrate": 2.0,
            "quintile": 2.0
        }
        
        # Default planet speeds (degrees per day) for applying/separating logic
        # This is simplified - actual speeds vary
        self.default_speeds = {
            "sun": 1.0,
            "moon": 13.0,
            "mercury": 1.0,
            "venus": 1.0,
            "mars": 0.5,
            "jupiter": 0.08,
            "saturn": 0.03,
            "uranus": 0.01,
            "neptune": 0.006,
            "pluto": 0.004,
            "chiron": 0.05,
            "north_node": 0.05,
            "true_node": 0.05,
            "south_node": 0.05,
            "lilith": 0.1,
            "true_lilith": 0.1
        }
    
    async def calculate_aspects(
        self,
        planet_positions: Dict[str, float],
        options: AspectOptions
    ) -> List[Dict[str, Any]]:
        """
        Calculate aspects between planets based on their longitudes.
        
        Args:
            planet_positions: Dictionary of planet names and their longitudes
            options: Aspect calculation options
            
        Returns:
            List of calculated aspects
        """
        aspects = []
        planet_list = list(planet_positions.keys())
        
        # Get the aspects to calculate
        aspect_types = options.aspects
        orbs = options.orbs
        
        # For each pair of planets
        for i in range(len(planet_list)):
            for j in range(i+1, len(planet_list)):
                planet1 = planet_list[i]
                planet2 = planet_list[j]
                
                # Get longitudes
                longitude1 = planet_positions[planet1]
                longitude2 = planet_positions[planet2]
                
                # Calculate angle difference
                angle_diff = abs(longitude1 - longitude2)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # Check each aspect type
                for aspect_type in aspect_types:
                    # Skip if not a valid aspect type
                    if aspect_type not in self.aspect_angles:
                        continue
                    
                    # Get the ideal angle for this aspect
                    ideal_angle = self.aspect_angles[aspect_type]
                    
                    # Get the orb for this aspect
                    allowed_orb = orbs.get(aspect_type, self.default_orbs.get(aspect_type, 5.0))
                    
                    # Check if within orb
                    orb = abs(angle_diff - ideal_angle)
                    if orb <= allowed_orb:
                        # Calculate applying/separating
                        # This is simplified; real calculation needs planet speeds and directions
                        applying = self._is_applying(planet1, planet2, longitude1, longitude2, ideal_angle)
                        
                        # Calculate influence based on orb
                        influence = 1.0 - (orb / allowed_orb)
                        
                        # Add to results
                        aspects.append({
                            "planet1": planet1,
                            "planet2": planet2,
                            "type": aspect_type,
                            "orb": round(orb, 2),
                            "applying": applying,
                            "influence": round(influence, 2)
                        })
        
        logger.info(f"Calculated {len(aspects)} aspects between {len(planet_list)} planets")
        return aspects
    
    async def calculate_planetary_aspects(
        self,
        config: AspectConfigRequest,
        date1: Optional[str] = None,
        time1: Optional[str] = None,
        date2: Optional[str] = None,
        time2: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate aspects between planets at two different dates/times.
        
        Args:
            config: Aspect configuration
            date1: First date in YYYY-MM-DD format (optional if already in config)
            time1: First time in HH:MM:SS format (optional)
            date2: Second date in YYYY-MM-DD format (optional, defaults to current)
            time2: Second time in HH:MM:SS format (optional)
            
        Returns:
            List of calculated aspects
        """
        try:
            # Set default times if not provided
            if not time1:
                time1 = "12:00:00"
            if not time2:
                time2 = "12:00:00"
            
            # Set default second date to current date if not provided
            if not date2:
                date2 = datetime.now().strftime("%Y-%m-%d")
            
            # Get first set of planet positions
            positions1 = await ephemeris_service.calculate_planet_positions(
                date=date1,
                time=time1,
                planets=config.planets1
            )
            
            # Get the planets for second calculation
            planets2 = config.planets2 if config.planets2 else config.planets1
            
            # Get second set of planet positions
            positions2 = await ephemeris_service.calculate_planet_positions(
                date=date2,
                time=time2,
                planets=planets2
            )
            
            # Extract longitudes
            longitudes1 = {p: pos["longitude"] for p, pos in positions1.items()}
            longitudes2 = {p: pos["longitude"] for p, pos in positions2.items()}
            
            # Prepare merged positions for aspect calculation
            merged_positions = {}
            
            # Add planets from first chart with prefix "1_"
            for planet, longitude in longitudes1.items():
                merged_positions[f"1_{planet}"] = longitude
            
            # Add planets from second chart with prefix "2_"
            for planet, longitude in longitudes2.items():
                merged_positions[f"2_{planet}"] = longitude
            
            # Create modified options from the config
            options = AspectOptions(
                aspects=config.aspects,
                orbs=config.orbs
            )
            
            # Calculate aspects between all planets
            all_aspects = await self.calculate_aspects(
                planet_positions=merged_positions,
                options=options
            )
            
            # Filter to only include aspects between charts (not within the same chart)
            cross_chart_aspects = []
            for aspect in all_aspects:
                # Check if planets are from different charts
                is_cross_chart = (
                    (aspect["planet1"].startswith("1_") and aspect["planet2"].startswith("2_")) or
                    (aspect["planet1"].startswith("2_") and aspect["planet2"].startswith("1_"))
                )
                
                if is_cross_chart:
                    # Remove the prefixes for clarity
                    aspect["planet1"] = aspect["planet1"][2:]
                    aspect["planet2"] = aspect["planet2"][2:]
                    
                    # Add chart information
                    if aspect["planet1"] in config.planets1:
                        aspect["chart1_planet"] = aspect["planet1"]
                        aspect["chart2_planet"] = aspect["planet2"]
                    else:
                        aspect["chart1_planet"] = aspect["planet2"]
                        aspect["chart2_planet"] = aspect["planet1"]
                    
                    cross_chart_aspects.append(aspect)
            
            logger.info(f"Calculated {len(cross_chart_aspects)} cross-chart aspects")
            return cross_chart_aspects
            
        except Exception as e:
            logger.error(f"Error calculating planetary aspects: {str(e)}")
            raise
    
    async def calculate_aspect_timeline(
        self,
        planet1: str,
        planet2: str,
        aspect_type: str,
        start_date: str,
        end_date: str,
        orb: float = 1.0
    ) -> List[Dict[str, Any]]:
        """
        Calculate when a specific aspect between two planets becomes exact.
        
        Args:
            planet1: First planet
            planet2: Second planet
            aspect_type: Aspect type
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            orb: Orb in degrees
            
        Returns:
            List of dates when the aspect is exact
        """
        try:
            # Validate inputs
            if aspect_type not in self.aspect_angles:
                raise ValueError(f"Invalid aspect type: {aspect_type}")
            
            # Get the ideal angle for this aspect
            ideal_angle = self.aspect_angles[aspect_type]
            
            # Parse dates
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Calculate number of days
            days = (end_dt - start_dt).days + 1
            
            # Track aspect timeline
            timeline = []
            prev_diff = None
            
            # Check each day
            for i in range(days):
                current_dt = start_dt + timedelta(days=i)
                current_date = current_dt.strftime("%Y-%m-%d")
                
                # Calculate planet positions
                positions = await ephemeris_service.calculate_planet_positions(
                    date=current_date,
                    planets=[planet1, planet2]
                )
                
                # Extract longitudes
                longitude1 = positions[planet1]["longitude"]
                longitude2 = positions[planet2]["longitude"]
                
                # Calculate angle difference
                angle_diff = (longitude1 - longitude2) % 360
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # Calculate how far from exact
                diff_from_exact = abs(angle_diff - ideal_angle)
                
                # If we're within orb of exact
                if diff_from_exact <= orb:
                    # Check if we changed direction (indicates exact aspect)
                    # This is a basic approach that works for daily intervals
                    if prev_diff is not None and (
                        (prev_diff < diff_from_exact and diff_from_exact < orb) or
                        (prev_diff > diff_from_exact and diff_from_exact < 0.5)  # Very close to exact
                    ):
                        # This day has an exact aspect
                        timeline.append({
                            "date": current_date,
                            "planet1": planet1,
                            "planet2": planet2,
                            "aspect": aspect_type,
                            "is_exact": True,
                            "orb": round(diff_from_exact, 2),
                            "planet1_sign": positions[planet1]["sign"],
                            "planet2_sign": positions[planet2]["sign"],
                            "planet1_retrograde": positions[planet1].get("retrograde", False),
                            "planet2_retrograde": positions[planet2].get("retrograde", False)
                        })
                
                # Save the difference for next iteration
                prev_diff = diff_from_exact
            
            logger.info(f"Found {len(timeline)} exact {aspect_type} aspects between {planet1} and {planet2}")
            return timeline
            
        except Exception as e:
            logger.error(f"Error calculating aspect timeline: {str(e)}")
            raise
    
    def _is_applying(
        self,
        planet1: str,
        planet2: str,
        longitude1: float,
        longitude2: float,
        ideal_angle: float
    ) -> bool:
        """
        Determine if an aspect is applying or separating.
        
        This is a simplified calculation based on default planet speeds.
        For accurate results, actual planet speeds at the time should be used.
        
        Args:
            planet1: First planet
            planet2: Second planet
            longitude1: Longitude of first planet
            longitude2: Longitude of second planet
            ideal_angle: Ideal angle for the aspect
            
        Returns:
            True if applying, False if separating
        """
        # This is a simplified approach
        # For accurate calculation, we need the actual speeds and directions
        
        # Extract planet names without prefixes if present
        if '_' in planet1:
            planet1 = planet1.split('_', 1)[1]
        if '_' in planet2:
            planet2 = planet2.split('_', 1)[1]
        
        # Get default speeds
        speed1 = self.default_speeds.get(planet1, 1.0)
        speed2 = self.default_speeds.get(planet2, 1.0)
        
        # Calculate current angular difference
        diff = (longitude1 - longitude2) % 360
        if diff > 180:
            diff = 360 - diff
        
        # Calculate relative speed
        relative_speed = speed1 - speed2
        
        # If the faster planet is behind, it's applying
        if diff < ideal_angle:
            return relative_speed > 0
        else:
            return relative_speed < 0

# Create a singleton instance
aspect_service = AspectService()
