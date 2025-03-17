# Magician Service Implementation Guide

This guide provides step-by-step instructions for implementing the Magician service as described in the architecture and API documentation.

## Prerequisites

Before starting implementation, ensure you have:

1. Python 3.9+
2. Docker and Docker Compose
3. PostgreSQL 15+ with pgvector extension
4. Redis 7+
5. Access to OpenAI API or Anthropic Claude API
6. Access to Astrology Engine API

## Development Environment Setup

### 1. Project Structure

Create the following directory structure:

```
services/magician/
├── src/
│   ├── api/                # API endpoints
│   │   ├── __init__.py
│   │   ├── profiles.py     # Profile endpoints
│   │   ├── insights.py     # Insight endpoints
│   │   ├── conversations.py # Conversation endpoints
│   │   ├── archetypes.py   # Archetype endpoints
│   │   └── health.py       # Health check endpoint
│   ├── core/               # Core business logic
│   │   ├── __init__.py
│   │   ├── profile.py      # Profile management
│   │   ├── insight.py      # Insight generation
│   │   ├── conversation.py # Conversation handling
│   │   ├── archetype.py    # Archetype mapping
│   │   └── embedding.py    # Vector embedding utilities
│   ├── db/                 # Database modules
│   │   ├── __init__.py
│   │   ├── engine.py       # Database connection
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── repositories/   # Repository pattern implementations
│   │   └── migrations/     # Alembic migrations
│   ├── integrations/       # External service integrations
│   │   ├── __init__.py
│   │   ├── astrology_engine.py  # Astrology Engine client
│   │   ├── llm.py          # Language model integration
│   │   └── auth.py         # Authentication integration
│   ├── utils/              # Utility functions
│   │   ├── __init__.py
│   │   ├── logging.py      # Logging configuration
│   │   ├── security.py     # Security utilities
│   │   └── validators.py   # Custom validators
│   ├── config.py           # Configuration management
│   └── main.py             # Application entry point
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
├── scripts/                # Utility scripts
├── Dockerfile              # Container definition
├── docker-compose.yml      # Local development setup
├── requirements.txt        # Python dependencies
├── requirements-dev.txt    # Development dependencies
├── alembic.ini             # Alembic configuration
├── .env.example            # Example environment variables
└── README.md               # Service-specific instructions
```

### 2. Environment Configuration

Create a `.env.example` file with the following variables:

```
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/magician
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis
REDIS_URL=redis://localhost:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=INFO

# Authentication
AUTH_SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Astrology Engine
ASTROLOGY_ENGINE_BASE_URL=https://api.mydivinations.com/astrology-engine
ASTROLOGY_ENGINE_API_KEY=your-astrology-engine-api-key

# LLM Provider (choose one)
LLM_PROVIDER=openai  # or anthropic
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

Copy this to a `.env` file and update with your actual values.

### 3. Docker Setup

Create a Dockerfile:

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create a docker-compose.yml:

```yaml
version: '3.8'

services:
  magician-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: magician
    volumes:
      - postgres_data:/var/lib/postgresql/data
    command: postgres -c shared_preload_libraries=pg_stat_statements

  pgvector-setup:
    image: postgres:15
    depends_on:
      - db
    command: >
      bash -c "
        sleep 5 &&
        PGPASSWORD=postgres psql -h db -U postgres -d magician -c 'CREATE EXTENSION IF NOT EXISTS vector;' &&
        PGPASSWORD=postgres psql -h db -U postgres -d magician -c 'CREATE EXTENSION IF NOT EXISTS pg_stat_statements;'
      "

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 4. Python Dependencies

Create a requirements.txt file:

```
fastapi==0.109.1
uvicorn[standard]==0.27.0
gunicorn==21.2.0
pydantic==2.5.2
sqlalchemy==2.0.23
alembic==1.13.0
psycopg2-binary==2.9.9
asyncpg==0.28.0
pgvector==0.2.4
redis==5.0.1
httpx==0.25.2
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
loguru==0.7.2
sentence-transformers==2.2.2
openai==1.3.7
anthropic==0.5.0
tenacity==8.2.3
```

And a requirements-dev.txt for development dependencies:

```
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
isort==5.12.0
mypy==1.7.1
flake8==6.1.0
httpx==0.25.2
```

## Implementation Steps

### 1. Database Models

#### Create SQLAlchemy Models

In `src/db/models.py`:

```python
from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, unique=True)
    birth_data = Column(JSONB, nullable=False)
    profile_data = Column(JSONB, nullable=False, default={})
    profile_embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="profile")
    insights = relationship("Insight", back_populates="profile")
    archetypal_maps = relationship("ArchetypalMap", back_populates="profile")
    preferences = relationship("UserPreference", back_populates="profile")

class Conversation(Base):
    __tablename__ = "conversations"
    
    conversation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.profile_id"), nullable=False)
    title = Column(String(255), nullable=True)
    context = Column(JSONB, nullable=False, default={})
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.conversation_id"), nullable=False)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(JSONB, nullable=False, default={})
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

class Insight(Base):
    __tablename__ = "insights"
    
    insight_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.profile_id"), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    data = Column(JSONB, nullable=False, default={})
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="insights")

class ArchetypalMap(Base):
    __tablename__ = "archetypal_maps"
    
    map_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.profile_id"), nullable=False)
    dominant_archetypes = Column(JSONB, nullable=False)
    elements = Column(JSONB, nullable=False)
    modalities = Column(JSONB, nullable=False)
    polarities = Column(JSONB, nullable=False)
    visualization_data = Column(JSONB, nullable=False)
    source_data = Column(JSONB, nullable=False, default={})
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="archetypal_maps")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    preference_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.profile_id"), nullable=False)
    preference_key = Column(String(100), nullable=False)
    preference_value = Column(JSONB, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="preferences")
    
    __table_args__ = (
        sqlalchemy.UniqueConstraint('profile_id', 'preference_key', name='uq_user_preference_profile_key'),
    )
```

#### Create Database Connection

In `src/db/engine.py`:

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)

# Create session factory
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
```

#### Set Up Alembic for Migrations

Initialize Alembic:

```bash
alembic init src/db/migrations
```

Update `alembic.ini`:

```ini
# alembic.ini

[alembic]
script_location = src/db/migrations
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = driver://user:pass@localhost/dbname
```

Create a migration script:

```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply the migration:

```bash
alembic upgrade head
```

### 2. Configuration Management

In `src/config.py`:

```python
from pydantic import BaseSettings, PostgresDsn, RedisDsn, validator, HttpUrl
from typing import Optional, Dict, Any, List


class Settings(BaseSettings):
    """Application settings."""
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: RedisDsn
    
    # Authentication
    AUTH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Astrology Engine
    ASTROLOGY_ENGINE_BASE_URL: HttpUrl
    ASTROLOGY_ENGINE_API_KEY: str
    
    # LLM Provider
    LLM_PROVIDER: str = "openai"  # or "anthropic"
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Embedding model
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_DIMENSION: int = 1536
    
    @validator("LLM_PROVIDER")
    def validate_llm_provider(cls, v, values):
        if v not in ["openai", "anthropic"]:
            raise ValueError("LLM_PROVIDER must be 'openai' or 'anthropic'")
        
        if v == "openai" and not values.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")
        
        if v == "anthropic" and not values.get("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER is 'anthropic'")
        
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()
```

### 3. Create API Endpoints

#### Set Up Main Application

In `src/main.py`:

```python
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from loguru import logger

from src.api import profiles, insights, conversations, archetypes, health
from src.config import settings
from src.utils.logging import setup_logging

# Set up logging
setup_logging()

# Create FastAPI application
app = FastAPI(
    title="Magician Service API",
    description="API for the MyDivinations Magician Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Process request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response
        logger.info(f"Response: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        # Log error
        process_time = time.time() - start_time
        logger.error(f"Error: {request.method} {request.url.path} - {str(e)} - Time: {process_time:.4f}s")
        
        # Return error response
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "Internal server error",
                }
            },
        )

# Include API routers
app.include_router(profiles.router, prefix="/api/v1", tags=["Profiles"])
app.include_router(insights.router, prefix="/api/v1", tags=["Insights"])
app.include_router(conversations.router, prefix="/api/v1", tags=["Conversations"])
app.include_router(archetypes.router, prefix="/api/v1", tags=["Archetypes"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting Magician Service API in {settings.ENVIRONMENT} environment")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Magician Service API")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "Magician",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
    }

# Run application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
```

#### Implement Profile Endpoints

In `src/api/profiles.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any

from src.db.engine import get_db
from src.core.profile import ProfileService
from src.integrations.auth import get_current_user
from src.models.profiles import (
    ProfileCreateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
)

router = APIRouter(prefix="/profiles")

# Get profile service
async def get_profile_service(db: AsyncSession = Depends(get_db)):
    return ProfileService(db)

@router.post("/", response_model=Dict[str, Any])
async def create_profile(
    request: ProfileCreateRequest,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Create a new user psycho-spiritual profile."""
    try:
        profile = await profile_service.create_profile(
            user_id=current_user["user_id"],
            birth_data=request.birth_data,
            initial_preferences=request.initial_preferences,
        )
        
        return {
            "success": True,
            "data": profile,
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "PROFILE_ERROR",
                "message": str(e),
            }
        }

@router.get("/{profile_id}", response_model=Dict[str, Any])
async def get_profile(
    profile_id: str,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Retrieve a user's psycho-spiritual profile."""
    try:
        profile = await profile_service.get_profile(profile_id)
        
        # Ensure user can only access their own profiles
        if profile.user_id != current_user["user_id"]:
            return {
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "You do not have permission to access this profile",
                }
            }
        
        return {
            "success": True,
            "data": profile,
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "PROFILE_ERROR",
                "message": str(e),
            }
        }

@router.patch("/{profile_id}", response_model=Dict[str, Any])
async def update_profile(
    profile_id: str,
    request: ProfileUpdateRequest,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Update a user's psycho-spiritual profile."""
    try:
        # Ensure user can only update their own profiles
        profile = await profile_service.get_profile(profile_id)
        if profile.user_id != current_user["user_id"]:
            return {
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "You do not have permission to update this profile",
                }
            }
        
        updated_profile = await profile_service.update_profile(
            profile_id=profile_id,
            update_data=request.dict(exclude_unset=True),
        )
        
        return {
            "success": True,
            "data": {
                "profile_id": str(updated_profile.profile_id),
                "updated_at": updated_profile.updated_at,
            },
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "PROFILE_ERROR",
                "message": str(e),
            }
        }
```

Implementation of the other API modules (`insights.py`, `conversations.py`, `archetypes.py`, `health.py`) would follow a similar pattern.

### 4. Implement Core Business Logic

#### Profile Management

In `src/core/profile.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from src.db.models import UserProfile, ArchetypalMap
from src.core.embedding import generate_profile_embedding
from src.integrations.astrology_engine import AstrologyEngineClient
from src.core.archetype import ArchetypeService

class ProfileService:
    """Service for managing user psycho-spiritual profiles."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.astrology_client = AstrologyEngineClient()
        self.archetype_service = ArchetypeService(db)
    
    async def create_profile(
        self,
        user_id: str,
        birth_data: Dict[str, Any],
        initial_preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new user profile.
        
        Args:
            user_id: User ID
            birth_data: Birth date, time, and location
            initial_preferences: Initial user preferences
            
        Returns:
            Created profile with initial archetype map
        """
        # Check if profile already exists for this user
        query = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await self.db.execute(query)
        existing_profile = result.scalars().first()
        
        if existing_profile:
            raise ValueError(f"Profile already exists for user {user_id}")
        
        # Get birth chart from Astrology Engine
        birth_chart = await self.astrology_client.get_birth_chart(birth_data)
        
        # Generate initial profile data
        profile_data = {
            "dominant_archetypes": [],
            "preferred_symbols": [],
            "growth_areas": [],
            "consciousness_level": "exploring",
        }
        
        # Add initial preferences if provided
        if initial_preferences:
            profile_data.update(initial_preferences)
        
        # Create profile
        profile = UserProfile(
            user_id=user_id,
            birth_data=birth_data,
            profile_data=profile_data,
        )
        
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        
        # Generate archetype map from birth chart
        archetype_map = await self.archetype_service.generate_archetypal_map(
            profile_id=str(profile.profile_id),
            chart_data=birth_chart,
        )
        
        # Generate profile embedding
        embedding = await generate_profile_embedding(
            birth_chart=birth_chart,
            archetype_map=archetype_map,
            profile_data=profile_data,
        )
        
        # Update profile with embedding
        profile.profile_embedding = embedding
        await self.db.commit()
        await self.db.refresh(profile)
        
        # Format response
        response = {
            "profile_id": str(profile.profile_id),
            "created_at": profile.created_at.isoformat(),
            "archetype_map": archetype_map,
        }
        
        return response
    
    async def get_profile(self, profile_id: str) -> UserProfile:
        """
        Get a user profile by ID.
        
        Args:
            profile_id: Profile ID
            
        Returns:
            User profile
        """
        query = select(UserProfile).where(UserProfile.profile_id == uuid.UUID(profile_id))
        result = await self.db.execute(query)
        profile = result.scalars().first()
        
        if not profile:
            raise ValueError(f"Profile not found: {profile_id}")
        
        return profile
    
    async def update_profile(
        self,
        profile_id: str,
        update_data: Dict[str, Any],
    ) -> UserProfile:
        """
        Update a user profile.
        
        Args:
            profile_id: Profile ID
            update_data: Data to update
            
        Returns:
            Updated user profile
        """
        # Get current profile
        profile = await self.get_profile(profile_id)
        
        # Update profile data
        profile_data = dict(profile.profile_data)
        profile_data.update(update_data)
        
        # Execute update
        query = (
            update(UserProfile)
            .where(UserProfile.profile_id == uuid.UUID(profile_id))
            .values(
                profile_data=profile_data,
                updated_at=datetime.utcnow(),
            )
            .returning(UserProfile)
        )
        
        result = await self.db.execute(query)
        updated_profile = result.scalars().first()
        await self.db.commit()
        
        # Generate new embedding if needed (could be moved to background task)
        # This is simplified - in production, you might want to do this asynchronously
        if update_data:
            # Get latest archetype map
            archetype_query = (
                select(ArchetypalMap)
                .where(ArchetypalMap.profile_id == uuid.UUID(profile_id))
                .order_by(ArchetypalMap.created_at.desc())
            )
            archetype_result = await self.db.execute(archetype_query)
            archetype_map = archetype_result.scalars().first()
            
            # Get birth chart
            birth_chart = await self.astrology_client.get_birth_chart(updated_profile.birth_data)
            
            # Generate new embedding
            embedding = await generate_profile_embedding(
                birth_chart=birth_chart,
                archetype_map=archetype_map.dominant_archetypes if archetype_map else None,
                profile_data=updated_profile.profile_data,
            )
            
            # Update embedding
            embedding_query = (
                update(UserProfile)
                .where(UserProfile.profile_id == uuid.UUID(profile_id))
                .values(profile_embedding=embedding)
            )
            await self.db.execute(embedding_query)
            await self.db.commit()
        
        return updated_profile
```