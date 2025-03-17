# Magician Service Architecture

This document outlines the architecture and design decisions for the Magician service, which provides an AI-powered personalized guidance system within the MyDivinations platform.

## System Overview

The Magician service is designed as a microservice with these key responsibilities:

1. Creating and maintaining user psycho-spiritual profiles
2. Generating personalized mystical insights based on astrological data
3. Providing natural language interaction through a conversational interface
4. Tracking user consciousness evolution over time
5. Integrating with other MyDivinations services

![System Architecture Diagram](https://via.placeholder.com/800x500?text=Magician+Architecture+Diagram)

## Architecture Components

### 1. Core Service Layer

The core service layer implements the business logic and is organized into these primary modules:

#### Profile Service
- Creates and maintains user psycho-spiritual profiles
- Manages vector embeddings for semantic representation
- Tracks changes in archetypal patterns over time

#### Insight Service
- Generates personalized interpretations of astrological data
- Creates tailored guidance based on user profile and current transits
- Manages the insight generation pipeline

#### Conversation Service
- Handles natural language interaction with users
- Maintains context across conversation sessions
- Routes specialized queries to appropriate handlers

#### Archetype Service
- Manages the core archetypal framework
- Maps astrological patterns to archetypal expressions
- Tracks dominant archetypal patterns in user profiles

### 2. Data Layer

The data layer handles persistence and retrieval of user data:

#### PostgreSQL Database (with pgvector extension)
- Stores user profiles and metadata
- Maintains conversation history
- Tracks interaction patterns
- Stores vector embeddings for semantic search

#### Redis Cache
- Caches frequently accessed profile data
- Caches recent astrological calculations
- Stores session information
- Implements rate limiting

#### Vector Embeddings
- Represents user profiles as high-dimensional vectors
- Enables semantic similarity search
- Facilitates personalization through pattern matching

### 3. Integration Layer

The integration layer connects with other services:

#### Astrology Engine Client
- Fetches birth chart data
- Retrieves transit information
- Accesses progression calculations

#### LLM Integration
- Connects to language model providers
- Handles prompt engineering and context management
- Processes and refines model outputs

#### Authentication Client
- Verifies user authentication
- Manages authorization for protected endpoints
- Validates JWT tokens

### 4. API Layer

The API layer exposes the service functionality:

#### RESTful API
- Public-facing endpoints for client applications
- Documented with OpenAPI/Swagger
- Implements standard API patterns

#### WebSocket API (optional)
- Real-time communication for chat interfaces
- Streaming responses for long-running operations
- Interactive conversation functionality

## Data Flow

### Profile Creation Flow

1. Client submits user profile creation request with birth data
2. API layer validates request and forwards to Profile Service
3. Profile Service requests birth chart from Astrology Engine
4. Birth chart data is analyzed to extract archetypal patterns
5. Initial vector embedding is generated from birth chart data
6. Profile data and embedding are stored in PostgreSQL
7. Response with profile ID and summary is returned to client

```
┌────────┐      ┌────────────┐      ┌─────────────────┐      ┌──────────────────┐
│ Client │──1──>│ API Layer  │──2──>│ Profile Service │──3──>│ Astrology Engine │
└────────┘      └────────────┘      └─────────────────┘      └──────────────────┘
                                             │
                                             │ 4. Analyze chart
                                             ▼
                                    ┌─────────────────┐
                                    │ Archetype Service │
                                    └─────────────────┘
                                             │
                                             │ 5. Generate embedding
                                             ▼
                                    ┌─────────────────┐      ┌──────────────────┐
                                    │ Profile Service │──6──>│ PostgreSQL/pgvector │
                                    └─────────────────┘      └──────────────────┘
                                             │
                                             │ 7. Return response
                                             ▼
┌────────┐      ┌────────────┐      ┌─────────────────┐
│ Client │<─────│ API Layer  │<─────│ Profile Service │
└────────┘      └────────────┘      └─────────────────┘
```

### Insight Generation Flow

1. Client requests personalized insight for a specific user profile
2. API layer validates request and forwards to Insight Service
3. Insight Service retrieves user profile from Profile Service
4. Current astrological data is fetched from Astrology Engine
5. User profile and astrological data are combined for personalization
6. LLM generates personalized content based on combined data
7. Insight is stored and returned to client

```
┌────────┐      ┌────────────┐      ┌─────────────────┐
│ Client │──1──>│ API Layer  │──2──>│ Insight Service │
└────────┘      └────────────┘      └─────────────────┘
                                             │
                      ┌────────────────┬─────┴─────┬────────────────┐
                      │                │           │                │
                      ▼                ▼           ▼                ▼
            ┌─────────────────┐ ┌──────────────┐ ┌───────────┐ ┌─────────────┐
            │ Profile Service │ │Astrology Engine│ │ LLM Service│ │ Redis Cache │
            └─────────────────┘ └──────────────┘ └───────────┘ └─────────────┘
                      │                │           │
                      └────────────────┴─────┬─────┘
                                             │
                                             │ 6. Generate personalized content
                                             ▼
                                    ┌─────────────────┐
                                    │ Insight Service │
                                    └─────────────────┘
                                             │
                                             │ 7. Store and return insight
                                             ▼
┌────────┐      ┌────────────┐      ┌─────────────────┐      ┌──────────────────┐
│ Client │<─────│ API Layer  │<─────│ Insight Service │─────>│ PostgreSQL/pgvector │
└────────┘      └────────────┘      └─────────────────┘      └──────────────────┘
```

### Conversation Flow

1. Client sends message in a conversation
2. API layer validates request and forwards to Conversation Service
3. Conversation Service retrieves conversation history and user profile
4. Context is built from profile, history, and current astrological data
5. LLM generates response based on context and user message
6. Response is processed and enhanced with personalized insights
7. Message pair is stored and response returned to client

```
┌────────┐      ┌────────────┐      ┌──────────────────┐
│ Client │──1──>│ API Layer  │──2──>│Conversation Service│
└────────┘      └────────────┘      └──────────────────┘
                                             │
                      ┌────────────────┬─────┴─────┬────────────────┐
                      │                │           │                │
                      ▼                ▼           ▼                ▼
         ┌────────────────────┐ ┌──────────────┐ ┌───────────┐ ┌─────────────────┐
         │ PostgreSQL/pgvector │ │Astrology Engine│ │ LLM Service│ │ Profile Service │
         └────────────────────┘ └──────────────┘ └───────────┘ └─────────────────┘
                      │                │           │                │
                      └────────────────┴─────┬─────┴────────────────┘
                                             │
                                             │ 6. Process response
                                             ▼
                                    ┌──────────────────┐      ┌────────────────────┐
                                    │Conversation Service│──7──>│ PostgreSQL/pgvector │
                                    └──────────────────┘      └────────────────────┘
                                             │
                                             │ 7. Return response
                                             ▼
┌────────┐      ┌────────────┐      ┌──────────────────┐
│ Client │<─────│ API Layer  │<─────│Conversation Service│
└────────┘      └────────────┘      └──────────────────┘
```

## Database Schema

### User Profiles Table

```sql
CREATE TABLE user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    birth_data JSONB NOT NULL,
    profile_data JSONB NOT NULL DEFAULT '{}',
    profile_embedding VECTOR(1536),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE(user_id)
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_updated_at ON user_profiles(updated_at);
```

### Conversations Table

```sql
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES user_profiles(profile_id),
    title VARCHAR(255),
    context JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_conversations_profile_id ON conversations(profile_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);
```

### Messages Table

```sql
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(conversation_id),
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    embedding VECTOR(1536),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

### Insights Table

```sql
CREATE TABLE insights (
    insight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES user_profiles(profile_id),
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    data JSONB NOT NULL DEFAULT '{}',
    embedding VECTOR(1536),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_insights_profile_id ON insights(profile_id);
CREATE INDEX idx_insights_type ON insights(type);
CREATE INDEX idx_insights_created_at ON insights(created_at);
```

### Archetypal Maps Table

```sql
CREATE TABLE archetypal_maps (
    map_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES user_profiles(profile_id),
    dominant_archetypes JSONB NOT NULL,
    elements JSONB NOT NULL,
    modalities JSONB NOT NULL,
    polarities JSONB NOT NULL,
    visualization_data JSONB NOT NULL,
    source_data JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_archetypal_maps_profile_id ON archetypal_maps(profile_id);
CREATE INDEX idx_archetypal_maps_created_at ON archetypal_maps(created_at);
```

### User Preferences Table

```sql
CREATE TABLE user_preferences (
    preference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES user_profiles(profile_id),
    preference_key VARCHAR(100) NOT NULL,
    preference_value JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE(profile_id, preference_key)
);

CREATE INDEX idx_user_preferences_profile_id ON user_preferences(profile_id);
```

### Vector Indexes

```sql
-- Create vector indexes for similarity search
CREATE INDEX idx_profiles_embedding ON user_profiles USING ivfflat (profile_embedding vector_cosine_ops);
CREATE INDEX idx_messages_embedding ON messages USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_insights_embedding ON insights USING ivfflat (embedding vector_cosine_ops);
```

## Technology Stack

### Backend Framework
- **FastAPI**: High-performance API framework with automatic OpenAPI documentation
- **Uvicorn/Gunicorn**: ASGI server for hosting the FastAPI application
- **Pydantic**: Data validation and settings management

### Database
- **PostgreSQL 15+**: Core relational database
- **pgvector extension**: Vector storage and similarity search
- **SQLAlchemy**: ORM for database interactions
- **Alembic**: Database migration management

### Caching and Messaging
- **Redis**: Caching, session management, and rate limiting
- **Redis Streams** (optional): Event streaming for service communication

### AI and ML
- **OpenAI API** or **Anthropic Claude API**: LLM integration for natural language generation
- **sentence-transformers**: Vector embedding generation
- **scikit-learn**: Basic ML operations for profile analysis

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Local development environment
- **GitHub Actions**: CI/CD pipelines
- **Kubernetes** (production): Container orchestration
- **Prometheus/Grafana**: Monitoring and alerting

### Security
- **FastAPI built-in security**: JWT validation
- **Pydantic validators**: Request validation
- **Rate limiting middleware**: Protection against abuse
- **HTTPS**: Secure communication
- **Environment-based secrets**: Secure configuration

## Deployment Architecture

The Magician service will be deployed as containers in a Kubernetes cluster:

### Development Environment
- Docker Compose for local development
- Integration testing against mocked dependencies
- Separate development database

### Staging Environment
- Kubernetes deployment with dev/test databases
- Integration with other MyDivinations services in staging
- Automated testing and validation

### Production Environment
- Kubernetes deployment with high availability
- Auto-scaling based on load
- Multiple replicas across availability zones
- Database replication and backups

## Scaling Considerations

### Horizontal Scaling
- Stateless API layer can scale horizontally
- Background processing for compute-intensive operations
- Database connection pooling for efficient resource usage

### Database Scaling
- Read replicas for high-read scenarios
- Connection pooling
- Optimized vector indexes for fast similarity search

### Caching Strategy
- Profile data caching with TTL
- Astrological calculation caching
- Response caching for frequently accessed data

## Integration with Astrology Engine

The Magician service integrates with the Astrology Engine service for all astrological calculations:

### Integration Pattern
- HTTP REST API calls
- Circuit breaker pattern for resilience
- Response caching to reduce load
- Retry logic for transient failures

### Required Endpoints
- Birth chart calculations
- Transit calculations
- Progression calculations
- Aspect analysis

## LLM Integration

The Magician service leverages large language models for natural language generation:

### Provider Integration
- OpenAI API or Anthropic Claude API
- Fallback mechanisms between providers
- Error handling and retry logic

### Prompt Engineering
- Carefully crafted prompt templates for different use cases
- Dynamic context building from user profile and astrological data
- Response validation and filtering
- Safety mechanisms to ensure appropriate content

### Token Management
- Token usage tracking
- Efficient context management
- Response length optimization

## Error Handling Strategy

The service implements comprehensive error handling:

### Common Error Types
- Input validation errors
- Integration errors (Astrology Engine, LLM providers)
- Database errors
- Authentication/authorization errors

### Error Handling Patterns
- Circuit breakers for external dependencies
- Graceful degradation for non-critical features
- Detailed error logging with context
- User-friendly error messages

## Monitoring and Observability

The service implements comprehensive monitoring:

### Key Metrics
- Request latency
- Error rates
- Database query performance
- External API response times
- Vector search performance
- LLM token usage

### Logging Strategy
- Structured JSON logs
- Correlation IDs for request tracing
- Log levels (DEBUG, INFO, WARNING, ERROR)
- PII filtering in logs

### Health Checks
- Database connectivity
- External API availability
- System resource utilization
- Background process health

## Security Considerations

### Data Protection
- Encryption at rest for sensitive data
- HTTPS for all API endpoints
- Secure handling of birth data
- Authorization checks for all endpoints

### Input Validation
- Strict schema validation with Pydantic
- Input sanitization
- Proper handling of Unicode and special characters

### Rate Limiting
- Per-user rate limits
- Graduated response for abuse
- API key validation

## Development Workflow

### Local Development
1. Clone repository
2. Start local environment with Docker Compose
3. Run migrations to set up database
4. Start FastAPI development server
5. Use Swagger UI for API testing

### Testing Strategy
- Unit tests for core functionality
- Integration tests for service interactions
- End-to-end tests for key user flows
- Performance testing for vector operations

### CI/CD Pipeline
- Automated testing on pull requests
- Static code analysis
- Vulnerability scanning
- Automated deployment to staging and production

## Appendix

### Vector Embedding Strategy

The service uses vector embeddings to represent:

1. **User Profiles**: Capturing the user's psycho-spiritual makeup
2. **Conversations**: Representing the semantic content of messages
3. **Insights**: Encoding the content of generated insights

The default embedding dimension is 1536, compatible with OpenAI's text-embedding-ada-002 model.

### Archetype Framework

The service uses a 12-archetype framework based on Jungian psychology, with these core archetypes:

1. The Seeker
2. The Creator
3. The Guardian
4. The Nurturer
5. The Transformer
6. The Sage
7. The Ruler
8. The Lover
9. The Magician
10. The Innocent
11. The Rebel
12. The Shadow

Each archetype has astrological correspondences and psychological expressions.

---

*Last Updated: March 17, 2025*