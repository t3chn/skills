# Modern CSS

New features to use. All have good browser support (2024+).

## Container Queries

Style based on container size, not viewport.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 300px 1fr;
  }
}
```

## :has() Selector

Parent selector - style parent based on children.

```css
/* Card with image gets different padding */
.card:has(img) {
  padding: 0;
}

/* Form group with invalid input */
.form-group:has(:invalid) {
  border-color: red;
}

/* Nav with dropdown open */
nav:has(.dropdown:focus-within) {
  background: var(--color-surface);
}

/* Section followed by another section */
section:has(+ section) {
  margin-bottom: 0;
}
```

## Subgrid

Inherit grid from parent.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* spans 3 rows of parent */
}
```

## Logical Properties

Direction-agnostic spacing (LTR/RTL support).

```css
/* Old way */
.box {
  margin-left: 1rem;
  margin-right: 2rem;
  padding-top: 1rem;
  padding-bottom: 1rem;
}

/* New way */
.box {
  margin-inline-start: 1rem;
  margin-inline-end: 2rem;
  padding-block: 1rem;
}

/* Shorthand */
.box {
  margin-inline: 1rem 2rem;  /* start end */
  padding-block: 1rem;       /* top bottom same */
}
```

## color-mix()

Mix colors in CSS.

```css
:root {
  --primary: #3b82f6;
}

.hover-state {
  /* 20% black mixed with primary */
  background: color-mix(in srgb, var(--primary), black 20%);
}

.light-variant {
  /* 50% white mixed with primary */
  background: color-mix(in srgb, var(--primary), white 50%);
}

.transparent-variant {
  /* Primary at 50% opacity */
  background: color-mix(in srgb, var(--primary) 50%, transparent);
}
```

## oklch() Colors

Perceptually uniform color space.

```css
:root {
  /* oklch(lightness chroma hue) */
  --primary: oklch(60% 0.15 250);      /* blue */
  --primary-light: oklch(80% 0.1 250); /* same hue, lighter */
  --primary-dark: oklch(40% 0.15 250); /* same hue, darker */

  /* Easy color variations by changing lightness */
  --surface-1: oklch(98% 0.01 250);
  --surface-2: oklch(95% 0.01 250);
  --surface-3: oklch(90% 0.01 250);
}
```

## Scroll Snap

```css
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  gap: 1rem;
}

.carousel-item {
  scroll-snap-align: start;
  flex: 0 0 300px;
}
```

## View Transitions

Page transitions without JavaScript.

```css
/* Enable for the document */
@view-transition {
  navigation: auto;
}

/* Custom transition for specific element */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: 0.5s;
}
```

## text-wrap: balance

Balanced text wrapping for headings.

```css
h1, h2, h3 {
  text-wrap: balance;
}

/* For body text, use pretty */
p {
  text-wrap: pretty;
}
```

## Anchor Positioning

Position elements relative to other elements (no JS).

```css
.anchor {
  anchor-name: --my-anchor;
}

.tooltip {
  position: absolute;
  position-anchor: --my-anchor;
  top: anchor(bottom);
  left: anchor(center);
  translate: -50% 8px;
}
```

## @layer

Control cascade order.

```css
@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; padding: 0; box-sizing: border-box; }
}

@layer base {
  body { font-family: var(--font-body); }
}

@layer components {
  .btn { /* component styles */ }
}

@layer utilities {
  .mt-4 { margin-top: 1rem; }
}
```

## @scope

Scoped styles without shadow DOM.

```css
@scope (.card) to (.card-content) {
  /* Styles apply inside .card but not inside .card-content */
  p { margin-bottom: 1rem; }
  img { border-radius: var(--radius); }
}
```

## Nesting

Native CSS nesting.

```css
.card {
  background: var(--color-surface);
  padding: 1rem;

  & .title {
    font-size: 1.25rem;
    font-weight: 600;
  }

  &:hover {
    background: var(--color-bg);
  }

  @media (min-width: 768px) {
    padding: 2rem;
  }
}
```

## Browser Support Note

All features above work in Chrome, Edge, Safari, Firefox (2024 versions).

For older browser support, check: https://caniuse.com
