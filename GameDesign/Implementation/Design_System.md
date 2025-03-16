# MyDivinations Design System

This document outlines the design system for the MyDivinations web application, providing a comprehensive guide for visual elements, components, and interaction patterns.

## Color Palette

### Primary Colors
- **Deep Indigo** `#3730A3` - Represents consciousness and insight
  - Light: `#4F46E5`
  - Dark: `#312E81`

- **Teal** `#0D9488` - Represents growth and transformation
  - Light: `#14B8A6`
  - Dark: `#0F766E`

- **Dark Orange** `#C2410C` - For important elements and calls to action (darker than original)
  - Light: `#EA580C`
  - Dark: `#9A3412`

### Neutrals
- White: `#FFFFFF`
- Nearly White: `#F8FAFC`
- Light Gray: `#E2E8F0`
- Medium Gray: `#94A3B8`
- Dark Gray: `#475569`
- Charcoal: `#1E293B`
- Nearly Black: `#0F172A`

### Semantic Colors
- Success: `#16A34A`
- Warning: `#EAB308`
- Error: `#DC2626`
- Info: `#0EA5E9`

### Gradients
- **Cosmic Gradient**: `linear-gradient(135deg, #0F172A 0%, #3730A3 100%)`
- **Fractal Gradient**: `linear-gradient(135deg, #0F766E 0%, #3730A3 100%)`
- **Transformation Gradient**: `linear-gradient(135deg, #C2410C 0%, #3730A3 100%)`

## Typography

### Font Families
- **Headings**: Raleway (clean, modern sans-serif with subtle character)
- **Body**: Inter (highly readable on all devices)
- **Accent/Quotes**: Playfair Display (for mystical/archetypal quotations)

### Font Sizes
- **Heading 1**: 2.5rem (40px) / Line height: 1.2
- **Heading 2**: 2rem (32px) / Line height: 1.2
- **Heading 3**: 1.5rem (24px) / Line height: 1.3
- **Heading 4**: 1.25rem (20px) / Line height: 1.4
- **Heading 5**: 1.125rem (18px) / Line height: 1.4
- **Body Large**: 1.125rem (18px) / Line height: 1.5
- **Body**: 1rem (16px) / Line height: 1.5
- **Body Small**: 0.875rem (14px) / Line height: 1.5
- **Caption**: 0.75rem (12px) / Line height: 1.5

### Font Weights
- **Regular**: 400
- **Medium**: 500
- **Semi-Bold**: 600
- **Bold**: 700

## Spacing System

We use a 4-point spacing system (4px = 0.25rem):
- **4xs**: 0.25rem (4px)
- **3xs**: 0.5rem (8px)
- **2xs**: 0.75rem (12px)
- **xs**: 1rem (16px)
- **sm**: 1.5rem (24px)
- **md**: 2rem (32px)
- **lg**: 3rem (48px)
- **xl**: 4rem (64px)
- **2xl**: 6rem (96px)
- **3xl**: 8rem (128px)

## Borders & Shadows

### Border Radii
- **None**: 0
- **Small**: 0.25rem (4px)
- **Medium**: 0.5rem (8px)
- **Large**: 1rem (16px)
- **Circular**: 9999px

### Shadows
- **Subtle**: `0 1px 2px rgba(15, 23, 42, 0.1)`
- **Medium**: `0 4px 6px -1px rgba(15, 23, 42, 0.1), 0 2px 4px -2px rgba(15, 23, 42, 0.1)`
- **Large**: `0 10px 15px -3px rgba(15, 23, 42, 0.1), 0 4px 6px -4px rgba(15, 23, 42, 0.1)`
- **Elevated**: `0 20px 25px -5px rgba(15, 23, 42, 0.1), 0 8px 10px -6px rgba(15, 23, 42, 0.1)`

## Component Design Patterns

### Buttons

#### Primary Button
- Background: Deep Indigo (`#3730A3`)
- Text: White
- Border Radius: Medium
- Padding: 0.5rem 1rem (8px 16px)
- Font: Body
- Font Weight: Semi-Bold

#### Secondary Button
- Background: White
- Text: Deep Indigo (`#3730A3`)
- Border: 1px solid Deep Indigo
- Border Radius: Medium
- Padding: 0.5rem 1rem (8px 16px)
- Font: Body
- Font Weight: Semi-Bold

#### Tertiary/Text Button
- Background: Transparent
- Text: Deep Indigo (`#3730A3`)
- Border Radius: Medium
- Padding: 0.5rem 1rem (8px 16px)
- Font: Body
- Font Weight: Medium

#### Call to Action Button
- Background: Dark Orange (`#C2410C`)
- Text: White
- Border Radius: Medium
- Padding: 0.5rem 1.5rem (8px 24px)
- Font: Body
- Font Weight: Bold

### Cards

#### Basic Card
- Background: White
- Border: 1px solid Light Gray (`#E2E8F0`)
- Border Radius: Medium
- Padding: 1.5rem (24px)
- Shadow: Medium

#### Feature Card
- Background: White
- Border: None
- Border Radius: Large
- Padding: 2rem (32px)
- Shadow: Large

#### Symbolic Card
- Background: Nearly White (`#F8FAFC`)
- Border: 1px solid Light Gray (`#E2E8F0`)
- Border Radius: Medium
- Padding: 1.5rem (24px)
- Shadow: Subtle
- Accent: Left border 4px Deep Indigo or Teal

### Form Elements

#### Text Input
- Background: White
- Border: 1px solid Medium Gray (`#94A3B8`)
- Border Radius: Medium
- Padding: 0.5rem 0.75rem (8px 12px)
- Font: Body
- Focus: 2px border Deep Indigo

#### Select
- Background: White
- Border: 1px solid Medium Gray (`#94A3B8`)
- Border Radius: Medium
- Padding: 0.5rem 0.75rem (8px 12px)
- Font: Body
- Focus: 2px border Deep Indigo

#### Checkbox/Radio
- Border: 1px solid Medium Gray (`#94A3B8`)
- Border Radius: Small (checkbox), Circular (radio)
- Selected: Deep Indigo background

## Iconography

We will use a combination of custom icons and the [Lucide](https://lucide.dev/) icon library.

### Icon Sizes
- **Small**: 1rem (16px)
- **Medium**: 1.5rem (24px)
- **Large**: 2rem (32px)

### Icon Style Guidelines
- Consistent line weight (1.5px)
- Rounded corners
- Simple, minimal design
- Uniform padding within bounding box

## Fractal Visualization Styling

The fractal visualizations will incorporate:
- Smooth gradient transitions
- Variable opacity layers
- Sacred geometry influences
- Organic flowing animations
- Responsive scaling based on device size

## Responsive Breakpoints

- **Mobile**: 0-639px
- **Tablet**: 640px-1023px
- **Desktop**: 1024px+

## Accessibility Guidelines

- Minimum contrast ratio of 4.5:1 for normal text
- Minimum contrast ratio of 3:1 for large text
- Focus indicators on all interactive elements
- Alternative text for all visual elements
- Semantic HTML structure
- Keyboard navigable interface

## Animation & Transitions

### Timing
- **Fast**: 150ms
- **Medium**: 300ms
- **Slow**: 500ms

### Easing
- **Default**: cubic-bezier(0.4, 0, 0.2, 1)
- **Ease-in**: cubic-bezier(0.4, 0, 1, 1)
- **Ease-out**: cubic-bezier(0, 0, 0.2, 1)
- **Ease-in-out**: cubic-bezier(0.4, 0, 0.2, 1)

## Usage Guidelines

- Use the primary color (Deep Indigo) for main actions and primary UI elements
- Use the secondary color (Teal) for supporting elements and secondary actions
- Use the accent color (Dark Orange) sparingly for important calls to action
- Maintain ample white space for a calm, focused user experience
- Use sacred geometry and fractal elements to reinforce the archetypal theme
- Ensure all interactive elements have proper hover and active states

---

*Last Updated: March 16, 2025 | 21:20 PST*  
*MyDiv FD*