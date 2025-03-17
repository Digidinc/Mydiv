# Magician Service Implementation Guide - Part 2

This document continues the implementation guide for the Magician service, covering the integration components, vector embedding, and LLM integration.

## 5. Implement Integration with Astrology Engine

In `src/integrations/astrology_engine.py`:

```python
import httpx
from typing import Dict, Any, Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

from src.config import settings

class AstrologyEngineClient:
    """Client for interacting with the Astrology Engine API."""
    
    def __init__(self):
        self.base_url = str(settings.ASTROLOGY_ENGINE_BASE_URL)
        self.api_key = settings.ASTROLOGY_ENGINE_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def get_birth_chart(
        self,
        birth_data: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get a birth chart from the Astrology Engine.
        
        Args:
            birth_data: Birth date, time, and location
            options: Options for the birth chart calculation
            
        Returns:
            Birth chart data
        """
        # Default options
        if options is None:
            options = {
                "house_system": "placidus",
                "with_aspects": True,
                "with_dignities": True,
                "with_dominant_elements": True,
            }
        
        # Prepare request data
        data = {
            "birth_data": birth_data,
            "options": options,
        }
        
        # Make request
        url = f"{self.base_url}/birth_chart"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=data,
                    headers=self.headers,
                    timeout=30.0,
                )
                
                # Check response
                response.raise_for_status()
                
                # Return birth chart data
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Astrology Engine: {e.response.status_code} - {e.response.text}")
            raise ValueError(f"Error from Astrology Engine: {e.response.reason_phrase}")
        except httpx.RequestError as e:
            logger.error(f"Request error to Astrology Engine: {str(e)}")
            raise ValueError(f"Error connecting to Astrology Engine: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def get_current_transits(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        orb: float = 1.5,
    ) -> Dict[str, Any]:
        """
        Get current transits for a birth chart.
        
        Args:
            birth_date: Birth date (YYYY-MM-DD)
            birth_time: Birth time (HH:MM:SS)
            birth_latitude: Birth latitude
            birth_longitude: Birth longitude
            orb: Orb for aspects
            
        Returns:
            Current transits data
        """
        # Prepare query parameters
        params = {
            "birth_date": birth_date,
            "orb": orb,
        }
        
        # Add optional parameters
        if birth_time:
            params["birth_time"] = birth_time
        if birth_latitude is not None:
            params["birth_latitude"] = birth_latitude
        if birth_longitude is not None:
            params["birth_longitude"] = birth_longitude
        
        # Make request
        url = f"{self.base_url}/transits/current-transits"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=30.0,
                )
                
                # Check response
                response.raise_for_status()
                
                # Return transits data
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Astrology Engine: {e.response.status_code} - {e.response.text}")
            raise ValueError(f"Error from Astrology Engine: {e.response.reason_phrase}")
        except httpx.RequestError as e:
            logger.error(f"Request error to Astrology Engine: {str(e)}")
            raise ValueError(f"Error connecting to Astrology Engine: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def get_transit_forecast(
        self,
        birth_date: str,
        birth_time: Optional[str] = None,
        birth_latitude: Optional[float] = None,
        birth_longitude: Optional[float] = None,
        start_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a five-year transit forecast.
        
        Args:
            birth_date: Birth date (YYYY-MM-DD)
            birth_time: Birth time (HH:MM:SS)
            birth_latitude: Birth latitude
            birth_longitude: Birth longitude
            start_date: Start date for forecast (YYYY-MM-DD)
            
        Returns:
            Forecast data
        """
        # Prepare query parameters
        params = {
            "birth_date": birth_date,
        }
        
        # Add optional parameters
        if birth_time:
            params["birth_time"] = birth_time
        if birth_latitude is not None:
            params["birth_latitude"] = birth_latitude
        if birth_longitude is not None:
            params["birth_longitude"] = birth_longitude
        if start_date:
            params["start_date"] = start_date
        
        # Make request
        url = f"{self.base_url}/transits/five-year-forecast"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=30.0,
                )
                
                # Check response
                response.raise_for_status()
                
                # Return forecast data
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Astrology Engine: {e.response.status_code} - {e.response.text}")
            raise ValueError(f"Error from Astrology Engine: {e.response.reason_phrase}")
        except httpx.RequestError as e:
            logger.error(f"Request error to Astrology Engine: {str(e)}")
            raise ValueError(f"Error connecting to Astrology Engine: {str(e)}")
```

## 6. Implement Vector Embedding

In `src/core/embedding.py`:

```python
from typing import Dict, Any, List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from loguru import logger

from src.config import settings

# Initialize embedding model
try:
    model = SentenceTransformer('all-mpnet-base-v2')
except Exception as e:
    logger.error(f"Error initializing sentence transformer: {str(e)}")
    model = None

async def generate_profile_embedding(
    birth_chart: Dict[str, Any],
    archetype_map: Optional[Dict[str, Any]] = None,
    profile_data: Optional[Dict[str, Any]] = None,
) -> List[float]:
    """
    Generate a vector embedding for a user profile.
    
    Args:
        birth_chart: Birth chart data
        archetype_map: Archetype mapping data
        profile_data: Profile preference data
        
    Returns:
        Vector embedding
    """
    # Create text representation of profile
    text_components = []
    
    # Add birth chart data
    if birth_chart:
        # Add sun sign
        if "planets" in birth_chart and "sun" in birth_chart["planets"]:
            sun = birth_chart["planets"]["sun"]
            text_components.append(f"Sun in {sun['sign']} at {sun['degree']:.1f} degrees")
        
        # Add moon sign
        if "planets" in birth_chart and "moon" in birth_chart["planets"]:
            moon = birth_chart["planets"]["moon"]
            text_components.append(f"Moon in {moon['sign']} at {moon['degree']:.1f} degrees")
        
        # Add ascendant
        if "houses" in birth_chart and 1 in birth_chart["houses"]:
            ascendant = birth_chart["houses"][1]
            text_components.append(f"Ascendant in {ascendant['sign']} at {ascendant['degree']:.1f} degrees")
        
        # Add other planets
        if "planets" in birth_chart:
            for planet, data in birth_chart["planets"].items():
                if planet not in ["sun", "moon"]:
                    text_components.append(f"{planet.capitalize()} in {data['sign']} at {data['degree']:.1f} degrees")
    
    # Add archetype map data
    if archetype_map:
        # Add dominant archetypes
        if "dominant_archetypes" in archetype_map:
            for archetype in archetype_map["dominant_archetypes"]:
                text_components.append(f"Strong {archetype['name']} archetype with strength {archetype['strength']:.1f}")
        
        # Add elements
        if "elements" in archetype_map:
            elements = archetype_map["elements"]
            for element, value in elements.items():
                text_components.append(f"{element.capitalize()} element: {value:.1f}%")
        
        # Add modalities
        if "modalities" in archetype_map:
            modalities = archetype_map["modalities"]
            for modality, value in modalities.items():
                text_components.append(f"{modality.capitalize()} modality: {value:.1f}%")
    
    # Add profile data
    if profile_data:
        # Add preferred symbols
        if "preferred_symbols" in profile_data:
            symbols = profile_data["preferred_symbols"]
            if symbols:
                text_components.append(f"Preferred symbols: {', '.join(symbols)}")
        
        # Add growth areas
        if "growth_areas" in profile_data:
            growth_areas = profile_data["growth_areas"]
            if growth_areas:
                text_components.append(f"Growth areas: {', '.join(growth_areas)}")
        
        # Add consciousness level
        if "consciousness_level" in profile_data:
            text_components.append(f"Consciousness level: {profile_data['consciousness_level']}")
    
    # Join text components
    text = " ".join(text_components)
    
    # Generate embedding
    if model is None:
        # Return random embedding for development
        logger.warning("Using random embedding because model is not available")
        return list(np.random.rand(settings.EMBEDDING_DIMENSION))
    
    # Generate embedding
    embedding = model.encode(text)
    
    # Convert to list and return
    return embedding.tolist()

async def generate_message_embedding(message: str) -> List[float]:
    """
    Generate a vector embedding for a message.
    
    Args:
        message: Message text
        
    Returns:
        Vector embedding
    """
    # Generate embedding
    if model is None:
        # Return random embedding for development
        logger.warning("Using random embedding because model is not available")
        return list(np.random.rand(settings.EMBEDDING_DIMENSION))
    
    # Generate embedding
    embedding = model.encode(message)
    
    # Convert to list and return
    return embedding.tolist()

async def generate_insight_embedding(
    insight_type: str,
    title: str,
    content: str,
) -> List[float]:
    """
    Generate a vector embedding for an insight.
    
    Args:
        insight_type: Type of insight
        title: Insight title
        content: Insight content
        
    Returns:
        Vector embedding
    """
    # Create text representation
    text = f"{insight_type}: {title}. {content}"
    
    # Generate embedding
    if model is None:
        # Return random embedding for development
        logger.warning("Using random embedding because model is not available")
        return list(np.random.rand(settings.EMBEDDING_DIMENSION))
    
    # Generate embedding
    embedding = model.encode(text)
    
    # Convert to list and return
    return embedding.tolist()
```

## 7. Implement LLM Integration

In `src/integrations/llm.py`:

```python
from typing import Dict, Any, List, Optional
import json
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings

class LLMService:
    """Service for interacting with language models."""
    
    def __init__(self):
        """Initialize the LLM service."""
        self.provider = settings.LLM_PROVIDER
        
        if self.provider == "openai":
            import openai
            self.client = openai.Client(api_key=settings.OPENAI_API_KEY)
        elif self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a completion using the configured LLM provider.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            if self.provider == "openai":
                return await self._generate_openai_completion(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            elif self.provider == "anthropic":
                return await self._generate_anthropic_completion(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise ValueError(f"Error generating completion: {str(e)}")
    
    async def _generate_openai_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a completion using OpenAI.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        # Create messages
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Generate completion
        response = await self.client.chat.completions.create(
            model="gpt-4",  # Or other model as needed
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # Return generated text
        return response.choices[0].message.content
    
    async def _generate_anthropic_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a completion using Anthropic.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        # Create system prompt
        system = system_prompt if system_prompt else ""
        
        # Generate completion
        response = await self.client.completions.create(
            model="claude-2",  # Or other model as needed
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # Return generated text
        return response.completion
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def generate_structured_output(
        self,
        prompt: str,
        output_schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate structured output using the configured LLM provider.
        
        Args:
            prompt: User prompt
            output_schema: JSON schema for output
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            
        Returns:
            Structured output as dictionary
        """
        # Create combined prompt
        combined_prompt = (
            f"{prompt}\n\n"
            f"Respond with a JSON object that follows this schema:\n"
            f"{json.dumps(output_schema, indent=2)}"
        )
        
        # Generate completion
        response = await self.generate_completion(
            prompt=combined_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
        )
        
        # Parse JSON response
        try:
            # Extract JSON from response (handle potential text before/after JSON)
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in response")
            
            json_str = response[json_start:json_end]
            result = json.loads(json_str)
            
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            logger.error(f"Response text: {response}")
            raise ValueError(f"Error parsing structured output: {str(e)}")
```