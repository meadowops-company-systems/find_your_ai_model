# Find Your AI Model - Design System & UI/UX Guide

## 1. Design Principles

SIMPLICITY
└─ One clear task: input → recommendation
└─ No unnecessary buttons or features
└─ Clean, uncluttered interface
CLARITY
└─ Clear instructions
└─ Obvious next steps
└─ Transparent reasoning
SPEED
└─ Fast feedback
└─ Show progress while loading
└─ Minimal clicks to result
TRUST
└─ Clear recommendations
└─ Show alternatives
└─ Display reasoning
ACCESSIBILITY
└─ WCAG 2.1 AA compliant
└─ Works without mouse
└─ Readable fonts
└─ Proper contrast


---

## 2. Color Palette

### Primary Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Blue | #0066FF | Buttons, links, accents |
| Black | #1A1A1A | Text, dark backgrounds |
| Gray | #666666 | Secondary text |

### Secondary Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Success Green | #22C55E | Checkmarks, positive |
| Warning Orange | #F59E0B | Warnings, alerts |
| Error Red | #EF4444 | Errors, negative |
| Light Gray | #F5F5F5 | Backgrounds |
| Border Gray | #E5E5E5 | Dividers |

---

## 3. Typography

### Font Family
Primary: Inter
├─ Modern and clean
├─ Excellent readability
├─ Google Fonts: https://fonts.google.com/specimen/Inter
└─ Fallback: -apple-system, BlinkMacSystemFont, sans-serif
Monospace: Fira Code
├─ For code snippets
├─ Google Fonts: https://fonts.google.com/specimen/Fira+Code
└─ Fallback: monospace

### Font Sizes

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 32px | 700 | 1.2 |
| H2 | 24px | 700 | 1.3 |
| H3 | 20px | 600 | 1.3 |
| Body Large | 16px | 400 | 1.5 |
| Body Small | 14px | 400 | 1.5 |
| Caption | 12px | 400 | 1.4 |

---

## 4. Components

### Button Component
States:
├─ Default (enabled)
├─ Hover (darker)
├─ Active (pressed)
├─ Disabled (grayed)
└─ Loading (spinner)
Variants:
├─ Primary (filled blue)
├─ Secondary (white border)
└─ Danger (red)
Sizes:
├─ Small: 32px height
├─ Medium: 40px height
├─ Large: 48px height

### Input Component
Features:
├─ Placeholder text
├─ Error state (red border)
├─ Valid state (green check)
├─ Focus state (blue border)
├─ Disabled state
└─ Character counter
Validation:
├─ Real-time feedback
├─ Error messages
└─ Success indicator

### Recommendation Card
Structure:
├─ Tool name + logo
├─ Match score (0-100)
├─ Visual stars (0-5)
├─ Key features
├─ Pricing
└─ Call-to-action
Colors:
├─ Score 90-100: Green
├─ Score 70-89: Blue
├─ Score 50-69: Orange
└─ Score <50: Red

---

## 5. Layout & Responsive Design

### Desktop (1024px+)
Layout:
├─ Max width: 1200px
├─ Padding: 40px sides
├─ Two-column (70% + 30%)
└─ Spacing: 32px between sections

### Tablet (640px - 1023px)
Layout:
├─ Max width: 100%
├─ Padding: 20px sides
├─ Single column (stack)
└─ Spacing: 24px between sections

### Mobile (< 640px)
Layout:
├─ Max width: 100%
├─ Padding: 12px sides
├─ Single column
├─ Full-width buttons
└─ Spacing: 16px between sections
Touch Targets:
├─ Minimum: 44x44px
├─ Buttons: 44px height
├─ Links: 44px min height

---

## 6. Key Pages

### Homepage / Input Page
Layout:
┌─────────────────────────────┐
│  Header (Logo + Nav)        │
├─────────────────────────────┤
│  Hero Section               │
│  Title: "Find Your AI Model"│
│  Subtitle: "Get the perfect |
│  tool in 30 seconds"        │
├─────────────────────────────┤
│  Input Form                 │
│  - Category dropdown        │
│  - Description textarea     │
│  - Character counter       │
│  - Submit button           │
│                            │
│  (Optional example tasks)  │
├─────────────────────────────┤
│  Footer                     │
└─────────────────────────────┘

### Results Page
Layout:
┌─────────────────────────────┐
│  Header                     │
├─────────────────────────────┤
│                            │
│  PRIMARY RECOMMENDATION    │
│  ┌──────────────────────┐  │
│  │ Tool Name      92/100│  │
│  │ ⭐⭐⭐⭐⭐          │  │
│  │ Why Best:           │  │
│  │ • Reason 1          │  │
│  │ • Reason 2          │  │
│  │ • Reason 3          │  │
│  │ Pricing: $20/month  │  │
│  │                     │  │
│  │ [Learn More]        │  │
│  └──────────────────────┘  │
│                            │
│  ALTERNATIVES              │
│  [Tool 2] [Tool 3]        │
│                            │
│  FREE OPTIONS              │
│  • Tool X (free)          │
│  • Tool Y (free)          │
│                            │
│  COST: $70/month          │
│                            │
│  [Book $100 Audit]        │
│                            │
├─────────────────────────────┤
│  Footer                     │
└─────────────────────────────┘

---

## 7. Interaction Patterns

### Loading State
Show:
├─ Skeleton loaders
├─ "Analyzing your task..."
├─ Progress animation
└─ Estimated time: 15-30 seconds

### Error State
Show:
├─ Clear error message
├─ What went wrong
├─ How to fix it
└─ Retry button

### Success State
Show:
├─ Primary recommendation
├─ Visual highlight
├─ Smooth scroll
└─ Ready for next action

---

## 8. Accessibility (WCAG 2.1 AA)

### Color Contrast
Requirements:
├─ Text vs background: 4.5:1 minimum
├─ Large text (18+): 3:1 minimum
├─ No information by color alone
└─ All tested against color blindness

### Fonts
Requirements:
├─ Minimum size: 12px
├─ Line height: 1.5 minimum
├─ Letter spacing: 0.02em minimum
└─ Readable sans-serif fonts

### Buttons & Forms
Requirements:
├─ Minimum size: 44x44px
├─ Focus state: 2px outline
├─ Keyboard accessible
├─ Proper label tags
└─ Error linked to inputs

### Screen Readers
Requirements:
├─ Semantic HTML
├─ Proper heading hierarchy
├─ ARIA labels where needed
├─ Alt text for images
└─ Meaningful link text

---

## 9. Animation & Transitions
Duration: 200-300ms
Easing: ease-in-out
Avoid: Excessive animations
Respect: prefers-reduced-motion
Examples:
├─ Button hover: 200ms
├─ Card entrance: 300ms
├─ Loading spinner: 1s (loop)
└─ Fade in: 200ms

---

## 10. Dark Mode (Future)
When implemented:
Background:
├─ Primary: #1A1A1A
├─ Secondary: #2D2D2D
└─ Tertiary: #3D3D3D
Text:
├─ Primary: #FFFFFF
├─ Secondary: #CCCCCC
└─ Tertiary: #999999
Accents:
├─ Primary: #00B4FF
└─ Status colors: Adjusted

---

**Document Version:** 1.0  
**Status:** Final  
**Last Updated:** May 31, 2026