"""
Configuration settings for the Astrology Engine Service.

This module loads configuration from environment variables and provides
a consistent interface for accessing configuration values throughout the application.
"""
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    APP_NAME: str = "astrology-engine"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Redis settings for caching
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    
    # Swiss Ephemeris settings
    EPHEMERIS_PATH: str = "/app/ephe"
    
    # API Gateway settings
    API_KEY_HEADER: str = "X-API-Key"
    API_KEY: str = ""
    
    # Cache settings
    ENABLE_CACHE: bool = True
    
    # Geocoding settings
    GEOCODING_USER_AGENT: str = "mydivinations-astrology-engine"
    GEOCODING_CACHE_TTL: int = 86400  # 24 hours
    
    # TimeZoneDB API settings
    TIMEZONE_DB_API_KEY: str = ""  # Register at https://timezonedb.com for a free API key
    
    # Transit forecast settings
    DEFAULT_FORECAST_YEARS: int = 5
    DEFAULT_FORECAST_PLANETS: List[str] = ["jupiter", "saturn", "uranus", "neptune", "pluto"]
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Create settings instance
settings = Settings()

# Configure logging
logger.remove()  # Remove default handler
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# Add console logger with appropriate log level
logger.add(
    sink=lambda msg: print(msg, end=""),
    format=log_format,
    level=settings.LOG_LEVEL,
    serialize=False,
)

# Check for required environment variables
if settings.DEBUG:
    logger.warning("Running in DEBUG mode. Do not use in production!")

# Log application configuration (excluding sensitive values)
if settings.DEBUG:
    logger.debug("Application configuration:")
    for key, value in settings.model_dump().items():
        if key not in ["API_KEY", "TIMEZONE_DB_API_KEY"]:
            logger.debug(f"  {key}: {value}")

# Validate Swiss Ephemeris path
if not os.path.exists(settings.EPHEMERIS_PATH):
    logger.warning(f"Swiss Ephemeris path does not exist: {settings.EPHEMERIS_PATH}")
    logger.warning("Some calculations may fail or be inaccurate.")

# Warn about missing TimeZoneDB API key
if not settings.TIMEZONE_DB_API_KEY:
    logger.warning("TimeZoneDB API key not set. Using fallback time zone determination.")
