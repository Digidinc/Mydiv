# MyDivinations Magician Database Schema

This document outlines the PostgreSQL database schema for the Magician service, including pgvector extension usage for embedding storage and similarity search.

## Overview

The Magician service uses PostgreSQL with the pgvector extension to store and retrieve:

1. User profiles with vector embeddings
2. Conversation history
3. Astrological data caching
4. Symbolic and archetypal associations
5. Personalized content preferences

## Setting Up PostgreSQL with pgvector

Before implementing the schema, ensure your PostgreSQL instance has the pgvector extension installed:

```sql
-- Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

## Schema Definition

### User Profiles Table

Stores core user information and profile embeddings.

```sql
CREATE TABLE user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL UNIQUE,
    birth_data JSONB NOT NULL,
    profile_embedding vector(1536) NOT NULL,  -- Embedding dimension may vary based on model
    profile_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for vector similarity search
CREATE INDEX user_profiles_embedding_idx ON user_profiles USING ivfflat (profile_embedding vector_cosine_ops);
```

### Archetypal Profiles

Stores the user's archetypal balance and affinities.

```sql
CREATE TABLE archetypal_profiles (
    archetypal_profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES user_profiles(profile_id) ON DELETE CASCADE,
    dominant_archetypes JSONB NOT NULL DEFAULT '{}', -- Contains archetype scores
    archetypal_history JSONB NOT NULL DEFAULT '[]',  -- Timeline of archetypal shifts
    last_analysis_date TIMESTAMP WITH TIME ZONE,
    archetypal_embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

### User Interactions

Stores all interactions with the Magician.

```sql
CREATE TABLE user_interactions (
    interaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    session_id UUID,
    interaction_text TEXT NOT NULL,
    embedding vector(1536),
    interaction_type VARCHAR(50) NOT NULL,  -- "question", "reflection", "insight", etc.
    response_text TEXT,
    response_embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for full-text search
CREATE INDEX user_interactions_text_idx ON user_interactions USING gin(to_tsvector('english', interaction_text));

-- Index for vector similarity search
CREATE INDEX user_interactions_embedding_idx ON user_interactions USING ivfflat (embedding vector_cosine_ops);
```

### Symbol Affinities

Tracks which symbols and archetypes resonate most with the user.

```sql
CREATE TABLE symbol_affinities (
    affinity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES user_profiles(profile_id) ON DELETE CASCADE,
    symbol_name VARCHAR(100) NOT NULL,
    affinity_score FLOAT NOT NULL DEFAULT 0.0,  -- 0 to 1
    interaction_count INTEGER NOT NULL DEFAULT 0,
    last_interaction TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(profile_id, symbol_name)
);
```

### Astrological Insights

Stores personalized interpretations of astrological events.

```sql
CREATE TABLE astrological_insights (
    insight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES user_profiles(profile_id) ON DELETE CASCADE,
    insight_type VARCHAR(50) NOT NULL,  -- "transit", "natal", "progression", etc.
    astrological_data JSONB NOT NULL,   -- The referenced astrological event
    insight_text TEXT NOT NULL,
    embedding vector(1536),
    rating INTEGER,                     -- User feedback rating (1-5)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for retrieving recent insights
CREATE INDEX astrological_insights_profile_date_idx ON astrological_insights(profile_id, created_at);
```

### Consciousness Journey

Tracks the user's growth and development over time.

```sql
CREATE TABLE consciousness_journey (
    journey_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES user_profiles(profile_id) ON DELETE CASCADE,
    stage_name VARCHAR(100) NOT NULL,
    stage_description TEXT,
    entry_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    exit_date TIMESTAMP WITH TIME ZONE,
    insights JSONB DEFAULT '[]',
    growth_metrics JSONB DEFAULT '{}'
);
```

### Astrological Cache

Caches results from the Astrology Engine API to reduce duplicate calls.

```sql
CREATE TABLE astrology_cache (
    cache_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_hash VARCHAR(64) NOT NULL UNIQUE,  -- Hash of the query parameters
    query_type VARCHAR(50) NOT NULL,         -- "birth_chart", "transit", etc.
    query_params JSONB NOT NULL,
    response_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Index for quick lookup by query hash
CREATE INDEX astrology_cache_hash_idx ON astrology_cache(query_hash);

-- Index for cleaning expired cache entries
CREATE INDEX astrology_cache_expiry_idx ON astrology_cache(expires_at);
```

## Advanced Query Examples

### Finding Similar User Profiles

```sql
-- Find users with similar archetypal profiles
SELECT 
    p.user_id,
    p.profile_embedding <=> :target_embedding AS distance
FROM 
    user_profiles p
ORDER BY 
    distance
LIMIT 10;
```

### Retrieving Relevant Past Interactions

```sql
-- Find similar past conversations to provide context
SELECT 
    interaction_text,
    response_text,
    created_at,
    embedding <=> :query_embedding AS similarity
FROM 
    user_interactions
WHERE 
    user_id = :user_id
ORDER BY 
    similarity
LIMIT 5;
```

### Tracking Archetypal Evolution

```sql
-- Generate a timeline of archetypal shifts
SELECT 
    entry_date,
    stage_name,
    growth_metrics
FROM 
    consciousness_journey
WHERE 
    profile_id = :profile_id
ORDER BY 
    entry_date;
```

### Finding Resonant Symbols

```sql
-- Identify symbols that strongly resonate with the user
SELECT 
    symbol_name,
    affinity_score
FROM 
    symbol_affinities
WHERE 
    profile_id = :profile_id AND
    affinity_score >= 0.7
ORDER BY 
    affinity_score DESC;
```

## Data Management Functions

### Updating Profile Embeddings

```sql
-- Function to update a user's profile embedding
CREATE OR REPLACE FUNCTION update_profile_embedding(
    p_profile_id UUID,
    p_new_embedding vector(1536)
) RETURNS VOID AS $$
BEGIN
    UPDATE user_profiles
    SET 
        profile_embedding = p_new_embedding,
        updated_at = NOW()
    WHERE 
        profile_id = p_profile_id;
END;
$$ LANGUAGE plpgsql;
```

### Archiving Old Interactions

```sql
-- Function to archive interactions older than a certain date
CREATE OR REPLACE FUNCTION archive_old_interactions(
    p_user_id VARCHAR,
    p_older_than TIMESTAMP WITH TIME ZONE
) RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    -- Move interactions to archive table (implementation varies)
    -- ...
    
    -- Delete from main table
    DELETE FROM user_interactions
    WHERE 
        user_id = p_user_id AND
        created_at < p_older_than;
    
    GET DIAGNOSTICS v_count = ROW_COUNT;
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;
```

## Integration with Astrology Engine

The database structure allows for efficient storage and retrieval of astrological data from the Astrology Engine API:

1. User birth data is stored in the `user_profiles` table's `birth_data` field
2. API responses are cached in the `astrology_cache` table
3. Personalized interpretations are stored in `astrological_insights`

This approach ensures:
- Reduced API calls through effective caching
- Persistent storage of personalized interpretations
- Ability to track which astrological factors most influence a user

## Performance Considerations

For optimal performance with pgvector:

1. Choose appropriate vector dimensions based on your LLM model
2. Use `ivfflat` indexes for larger tables (>10,000 rows)
3. Consider using HNSW indexes for even better performance with larger datasets
4. Regularly maintain indexes with `VACUUM ANALYZE`
5. Monitor query performance and adjust index parameters as needed

## Backup and Maintenance

Regular database maintenance should include:

1. Daily backups of all tables
2. Weekly cleanup of expired cache entries
3. Monthly archiving of old interaction data
4. Quarterly reindexing of vector indexes
5. Regular monitoring of database size and performance

---

*This schema provides the foundation for the Magician service's personalized user profiling and interaction capabilities.*