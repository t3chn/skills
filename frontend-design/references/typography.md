# Typography

Curated font pairings. All Google Fonts.

## Font Pairings

### Display + Body Combinations

| Display | Body | Vibe | Import |
|---------|------|------|--------|
| **Fraunces** | Source Serif 4 | Editorial, sophisticated | `family=Fraunces:wght@400;700&family=Source+Serif+4` |
| **Playfair Display** | Lato | Classic, elegant | `family=Playfair+Display:wght@400;700&family=Lato` |
| **Space Grotesk** | Inter | Modern, technical | `family=Space+Grotesk:wght@400;700&family=Inter` |
| **Outfit** | Outfit | Clean, versatile | `family=Outfit:wght@400;600;800` |
| **DM Serif Display** | DM Sans | Warm, approachable | `family=DM+Serif+Display&family=DM+Sans` |
| **Syne** | Work Sans | Bold, contemporary | `family=Syne:wght@400;700&family=Work+Sans` |
| **Instrument Serif** | Instrument Sans | Refined, modern | `family=Instrument+Serif&family=Instrument+Sans` |

### Monospace Combinations

| Display | Body | Vibe | Import |
|---------|------|------|--------|
| **JetBrains Mono** | JetBrains Mono | Dev, technical | `family=JetBrains+Mono:wght@400;700` |
| **Space Grotesk** | IBM Plex Mono | Tech, professional | `family=Space+Grotesk:wght@400;700&family=IBM+Plex+Mono` |
| **VT323** | IBM Plex Mono | Retro, playful | `family=VT323&family=IBM+Plex+Mono` |
| **Fira Code** | Fira Sans | Balanced, readable | `family=Fira+Code&family=Fira+Sans` |

### Statement Fonts (use sparingly)

| Font | Best For | Import |
|------|----------|--------|
| **Bebas Neue** | Headlines only | `family=Bebas+Neue` |
| **Dela Gothic One** | Bold Japanese-inspired | `family=Dela+Gothic+One` |
| **Righteous** | Retro headers | `family=Righteous` |
| **Archivo Black** | Impact headers | `family=Archivo+Black` |
| **Major Mono Display** | Decorative mono | `family=Major+Mono+Display` |

## Import Pattern

```html
<!-- Single font -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">

<!-- Pairing -->
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;700&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">
```

## CSS Setup

```css
:root {
  --font-display: 'Fraunces', serif;
  --font-body: 'Source Serif 4', serif;
  --font-mono: 'JetBrains Mono', monospace;
}

body {
  font-family: var(--font-body);
  font-size: 1rem;
  line-height: 1.6;
}

h1, h2, h3 {
  font-family: var(--font-display);
  line-height: 1.2;
  font-weight: 700;
}

code, pre {
  font-family: var(--font-mono);
}
```

## Typography Scale

```css
:root {
  /* Fluid type scale */
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.25rem, 1rem + 1vw, 1.5rem);
  --text-xl: clamp(1.5rem, 1rem + 2vw, 2.5rem);
  --text-2xl: clamp(2rem, 1rem + 4vw, 4rem);
  --text-hero: clamp(3rem, 1rem + 8vw, 8rem);
}
```

## Anti-Patterns

**Never use as primary:**
- Inter (overused)
- Roboto (Google default)
- Open Sans (dated)
- Arial/Helvetica (system fallback only)
- Poppins (AI cliché)

**Use with caution:**
- Space Grotesk (becoming overused)
- Montserrat (dated)

## Tips

1. **Limit to 2 fonts** - Display + Body is enough
2. **Load only needed weights** - 400 and 700 usually sufficient
3. **Use `display=swap`** - Prevents invisible text
4. **Preconnect** - Speeds up font loading
5. **System fallbacks** - Always include: `serif`, `sans-serif`, or `monospace`
