---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces. Use when building web components, pages, or applications. Provides ready design systems, font pairings, color palettes, and animation patterns to avoid generic AI aesthetics.
---

# Frontend Design

Build distinctive frontends without reinventing design each time.

## References

| Topic | Reference |
|-------|-----------|
| **Ready Design Systems** | `references/design-systems.md` - Pick one and go |
| **Typography** | `references/typography.md` - Font pairings |
| **Animations** | `references/animations.md` - CSS patterns |
| **Modern CSS** | `references/modern-css.md` - New features |

## Quick Start

1. **Pick a design system** from `references/design-systems.md`
2. **Copy the CSS variables** into your project
3. **Use the font pairing** from that system
4. **Add animations** from `references/animations.md`

## Stack Decision

```
PROJECT TYPE?
│
├─ Marketing/Landing → HTML + Tailwind + vanilla JS
├─ Dashboard/App → React/Vue + Tailwind + shadcn/ui
├─ Simple interactive → HTML + CSS + Alpine.js
└─ Complex SPA → Next.js/Nuxt + Tailwind
```

## Anti-Slop Checklist

Before delivering, verify:

- [ ] NOT using: Inter, Roboto, Arial, system-ui as primary font
- [ ] NOT using: purple/blue gradient on white (the AI cliché)
- [ ] NOT using: rounded-xl on everything
- [ ] NOT using: generic card grid layout
- [ ] HAS: one distinctive visual element (unusual font, bold color, asymmetry)
- [ ] HAS: intentional whitespace (not everything cramped)
- [ ] HAS: hover/focus states that feel crafted
- [ ] HAS: consistent spacing system (4px/8px base)

## Design Principles

**Pick ONE direction and commit:**

| Direction | Characteristics |
|-----------|-----------------|
| **Brutalist** | Raw, monospace, harsh contrast, no decoration |
| **Editorial** | Large serif headlines, generous whitespace, magazine feel |
| **Playful** | Rounded shapes, bright colors, bouncy animations |
| **Luxury** | Thin sans-serif, muted colors, lots of space |
| **Technical** | Monospace accents, data-dense, dark mode |
| **Organic** | Soft gradients, natural colors, flowing shapes |

## Quick Patterns

### Hero Section (not generic)
```css
/* Asymmetric hero with overlapping elements */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 90vh;
  overflow: hidden;
}
.hero-content {
  padding: clamp(2rem, 8vw, 8rem);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.hero-visual {
  position: relative;
  margin-left: -10%;  /* overlap */
}
```

### Typography Scale
```css
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.25rem, 1rem + 1vw, 1.5rem);
  --text-xl: clamp(1.5rem, 1rem + 2vw, 2.5rem);
  --text-2xl: clamp(2rem, 1rem + 4vw, 4rem);
  --text-hero: clamp(3rem, 1rem + 8vw, 8rem);
}
```

### Spacing System
```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
  --space-24: 6rem;    /* 96px */
}
```

## Tailwind Recommendations

```js
// tailwind.config.js - distinctive setup
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        display: ['var(--font-display)'],
        body: ['var(--font-body)'],
      },
      // Use design system colors from references/design-systems.md
    }
  }
}
```

**Avoid these Tailwind patterns:**
- `rounded-xl` everywhere (use `rounded-none` or `rounded-sm` for variation)
- `shadow-lg` on every card
- `bg-gradient-to-r from-purple-500 to-pink-500`
- Generic `max-w-7xl mx-auto px-4`

**Prefer:**
- Asymmetric padding (`pl-8 pr-16`)
- Mix of rounded and sharp corners
- Custom shadows with color (`shadow-[0_4px_20px_rgba(0,0,0,0.1)]`)
- Full-bleed sections with contained content
