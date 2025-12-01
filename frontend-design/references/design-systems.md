# Ready Design Systems

Pick one, copy the CSS, build.

## 1. Brutalist Mono

Raw, technical, no-nonsense.

```css
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;700&display=swap');

:root {
  --font-display: 'Space Grotesk', sans-serif;
  --font-body: 'JetBrains Mono', monospace;

  --color-bg: #0a0a0a;
  --color-surface: #141414;
  --color-text: #fafafa;
  --color-text-muted: #737373;
  --color-accent: #22c55e;
  --color-border: #262626;

  --radius: 0;
}
```

**Use for:** Dev tools, terminals, documentation, tech products

---

## 2. Editorial Serif

Magazine-quality, sophisticated, content-focused.

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@400;700&family=Source+Serif+4:wght@400;600&display=swap');

:root {
  --font-display: 'Fraunces', serif;
  --font-body: 'Source Serif 4', serif;

  --color-bg: #faf8f5;
  --color-surface: #ffffff;
  --color-text: #1a1a1a;
  --color-text-muted: #666666;
  --color-accent: #b91c1c;
  --color-border: #e5e5e5;

  --radius: 2px;
}
```

**Use for:** Blogs, publications, portfolios, luxury brands

---

## 3. Neon Dark

Bold, vibrant, energetic.

```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

:root {
  --font-display: 'Outfit', sans-serif;
  --font-body: 'Outfit', sans-serif;

  --color-bg: #09090b;
  --color-surface: #18181b;
  --color-text: #fafafa;
  --color-text-muted: #71717a;
  --color-accent: #f472b6;
  --color-accent-2: #38bdf8;
  --color-border: #27272a;

  --radius: 8px;
  --glow: 0 0 20px rgba(244, 114, 182, 0.3);
}
```

**Use for:** Gaming, creative tools, entertainment, startups

---

## 4. Natural Warm

Organic, approachable, human.

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Lora:wght@400;600&display=swap');

:root {
  --font-display: 'Lora', serif;
  --font-body: 'DM Sans', sans-serif;

  --color-bg: #fefdfb;
  --color-surface: #f5f0e8;
  --color-text: #292524;
  --color-text-muted: #78716c;
  --color-accent: #b45309;
  --color-border: #e7e5e4;

  --radius: 12px;
}
```

**Use for:** Food, wellness, sustainable brands, personal sites

---

## 5. Corporate Clean

Professional, trustworthy, scalable.

```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
  --font-display: 'Plus Jakarta Sans', sans-serif;
  --font-body: 'Plus Jakarta Sans', sans-serif;

  --color-bg: #ffffff;
  --color-surface: #f8fafc;
  --color-text: #0f172a;
  --color-text-muted: #64748b;
  --color-accent: #0ea5e9;
  --color-border: #e2e8f0;

  --radius: 6px;
}
```

**Use for:** SaaS, enterprise, fintech, B2B products

---

## 6. Retro Computing

Nostalgic, distinctive, memorable.

```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=VT323&display=swap');

:root {
  --font-display: 'VT323', monospace;
  --font-body: 'IBM Plex Mono', monospace;

  --color-bg: #1e1e2e;
  --color-surface: #313244;
  --color-text: #a6e3a1;
  --color-text-muted: #6c7086;
  --color-accent: #f9e2af;
  --color-border: #45475a;

  --radius: 0;
  --scanline: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.15),
    rgba(0, 0, 0, 0.15) 1px,
    transparent 1px,
    transparent 2px
  );
}
```

**Use for:** Games, creative portfolios, dev tools, experimental projects

---

## Usage Pattern

```html
<style>
  /* Paste design system variables above */

  body {
    font-family: var(--font-body);
    background: var(--color-bg);
    color: var(--color-text);
  }

  h1, h2, h3 {
    font-family: var(--font-display);
  }

  .card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius);
  }

  .accent {
    color: var(--color-accent);
  }

  .muted {
    color: var(--color-text-muted);
  }
</style>
```

## Tailwind Integration

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        surface: 'var(--color-surface)',
        accent: 'var(--color-accent)',
        border: 'var(--color-border)',
      },
      fontFamily: {
        display: ['var(--font-display)'],
        body: ['var(--font-body)'],
      },
      borderRadius: {
        DEFAULT: 'var(--radius)',
      }
    }
  }
}
```
