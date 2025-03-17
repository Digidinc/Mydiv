# Archetypal Integration Guidelines

## Overview

This document outlines how the Path of Symbols mini-game integrates with and adapts to a user's unique archetypal profile. It provides technical and design specifications for ensuring that each user's journey through the Path of Symbols is personalized to their archetypal pattern, creating a more meaningful and transformative experience.

## Archetypal Profile Foundation

### Profile Data Structure

The archetypal profile is derived from the user's astrological data and consists of:

1. **Elemental Balance**
   - Numerical values (0-100) for Fire, Earth, Air, and Water affinities
   - Dominant element (highest value) and secondary element
   - Element lacking (lowest value)

2. **Primary Archetypes**
   - Three dominant archetypal patterns from Carol Pearson's 12 archetype system
   - Percentage strength for each (0-100)
   - Development stage for each (dormant, awakening, active, integrated)

3. **Planetary Influences**
   - Positions of key planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn)
   - Strength and prominence of each planetary energy
   - Key aspect patterns (Grand Cross, Grand Trine, T-Square, etc.)

4. **Consciousness Level**
   - Estimated level on Hawkins scale (0-1000)
   - Primary consciousness domain (Force vs. Power)
   - Primary growth opportunity

### Data Retrieval

The Path of Symbols accesses the user's archetypal profile through:

1. **Profile API**
   - Request archetypal profile data at journey start
   - Lightweight JSON format for efficient retrieval
   - Caching mechanism for offline functionality

2. **Update Mechanism**
   - Subscribe to profile updates if user modifies birth data
   - Graceful handling of profile changes between sessions
   - Persistence of journey progress despite profile updates

## Adaptation Mechanisms

The Path of Symbols adapts to the user's archetypal profile in five key ways:

### 1. Entry Point Customization

Each user begins their journey with a visualization and context tailored to their dominant archetypal energy:

#### Implementation Specifications

- **Entry Point Selection**
  - System identifies dominant archetype from profile
  - Maps to one of six primary entry visualizations
  - Selects appropriate initial symbol set and color palette
  - Determines starting fractal parameters

- **Technical Approach**
  - Entry point determination function runs at journey initialization
  - Parameters passed to both visualization and narrative systems
  - Entry state stored for journey continuity

#### Archetypal Mapping

| Dominant Archetype | Entry Visualization | Initial Symbols | Starting Tone |
|-------------------|---------------------|----------------|---------------|
| Creator/Artist | Creative emergence | Wands/Fire, Star, Spiral | Inspirational |
| Explorer/Seeker | Path with horizon | Wands/Fire, Fool, Arrow | Adventurous |
| Sage/Teacher | Connected patterns | Swords/Air, Hermit, Web | Contemplative |
| Hero/Warrior | Challenge landscape | Swords/Air, Chariot, Mountain | Determined |
| Caregiver/Nurturer | Growth garden | Cups/Water, Empress, Tree | Nurturing |
| Ruler/Leader | Structured edifice | Pentacles/Earth, Emperor, Cube | Ordered |

### 2. Path Guidance System

The system provides subtle guidance toward choices that promote growth based on the user's archetypal profile:

#### Implementation Specifications

- **Growth Path Identification**
  - Algorithm identifies archetypes needing development
  - Maps underdeveloped archetypes to journey paths
  - Creates weighted guidance values for each possible choice
  - Updates after each decision based on path taken

- **Technical Approach**
  - Guidance calculator runs at each decision point
  - Translates guidance values to visual/audio cues
  - Implements subtlety scaling based on user settings
  - Records guidance alignment for journey analysis

#### Guidance Manifestation

The system provides subtle, non-controlling guidance through:

1. **Visual Cues**
   - Element-specific symbols appear near growth-promoting choices:
     - **Fire** dominant: Subtle flame or light elements
     - **Earth** dominant: Crystal or root elements
     - **Air** dominant: Feather or wind patterns
     - **Water** dominant: Droplet or flow elements
   - Increased luminosity or saturation in growth-aligned direction
   - Symbolic elements from needed archetypes appear briefly
   - Fractal pattern shows subtle directional flow

2. **Audio Cues**
   - Harmonic resolution when focus moves toward growth choice
   - Subtle tonal shift when hovering over growth-promoting option
   - Archetypal sound signatures activate when aligned with growth
   - Binaural elements enhance focus toward beneficial choices

3. **Interaction Feedback**
   - Slightly increased responsiveness for growth-aligned choices
   - Subtle haptic confirmation when exploring growth directions
   - Smoother animation transitions toward beneficial paths
   - Micro-delays when moving toward less beneficial options

### 3. Symbol Resonance System

Symbols throughout the journey resonate differently based on the user's archetypal energies:

#### Implementation Specifications

- **Symbol Resonance Calculation**
  - Each symbol assigned archetypal affinity values
  - System compares user's profile to symbol affinities
  - Calculates resonance score (0-100) for each active symbol
  - Updates dynamically as journey progresses

- **Technical Approach**
  - Symbol manager maintains active symbol collection
  - Applies resonance effects based on calculated values
  - Implements weighted blending for visual effects
  - Records high-resonance symbols for journey summary

#### Resonance Effects

Symbol resonance manifests through:

1. **Visual Prominence**
   - High-resonance symbols appear slightly larger
   - Increased clarity and definition in rendering
   - Subtle animation effects activate
   - Aura or glow effect proportional to resonance

2. **Meaningful Placement**
   - High-resonance symbols positioned in focal areas
   - Appear more frequently in transitional moments
   - Create compositional emphasis through placement
   - Form connecting patterns with other resonant symbols

3. **Interaction Response**
   - More detailed information available on interaction
   - Extended animation sequences when activated
   - Memory effect (symbols reappear in later contexts)
   - Influence on surrounding symbolic elements