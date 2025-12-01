# Animations

CSS-first patterns. Copy and use.

## Entrance Animations

### Fade In Up
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}
```

### Fade In Scale
```css
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.fade-in-scale {
  animation: fadeInScale 0.4s ease-out forwards;
}
```

### Slide In Left
```css
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.slide-in-left {
  animation: slideInLeft 0.5s ease-out forwards;
}
```

## Stagger Pattern

```css
/* Apply to parent container's children */
.stagger-children > * {
  opacity: 0;
  animation: fadeInUp 0.5s ease-out forwards;
}

.stagger-children > *:nth-child(1) { animation-delay: 0.1s; }
.stagger-children > *:nth-child(2) { animation-delay: 0.2s; }
.stagger-children > *:nth-child(3) { animation-delay: 0.3s; }
.stagger-children > *:nth-child(4) { animation-delay: 0.4s; }
.stagger-children > *:nth-child(5) { animation-delay: 0.5s; }
.stagger-children > *:nth-child(6) { animation-delay: 0.6s; }
```

## Hover Effects

### Lift
```css
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}
```

### Scale
```css
.hover-scale {
  transition: transform 0.2s ease;
}

.hover-scale:hover {
  transform: scale(1.02);
}
```

### Glow
```css
.hover-glow {
  transition: box-shadow 0.3s ease;
}

.hover-glow:hover {
  box-shadow: 0 0 30px var(--color-accent, rgba(59, 130, 246, 0.5));
}
```

### Underline Reveal
```css
.hover-underline {
  position: relative;
}

.hover-underline::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.hover-underline:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}
```

## Button Effects

### Press
```css
.btn-press {
  transition: transform 0.1s ease;
}

.btn-press:active {
  transform: scale(0.97);
}
```

### Shine
```css
.btn-shine {
  position: relative;
  overflow: hidden;
}

.btn-shine::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s ease;
}

.btn-shine:hover::after {
  left: 100%;
}
```

## Loading States

### Pulse
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}
```

### Skeleton
```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface) 25%,
    var(--color-border) 50%,
    var(--color-surface) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius, 4px);
}
```

### Spinner
```css
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

## Scroll Animations (CSS-only)

```css
/* Requires: elements start with opacity: 0 */
@keyframes scrollFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-reveal {
  opacity: 0;
  transform: translateY(30px);
  animation: scrollFadeIn 0.6s ease forwards;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}
```

## Easing Reference

```css
:root {
  /* Smooth */
  --ease-out: cubic-bezier(0.33, 1, 0.68, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);

  /* Bouncy */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Snappy */
  --ease-snap: cubic-bezier(0.2, 0, 0, 1);

  /* Spring-like */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

## Tips

1. **Keep it subtle** - 0.2-0.4s for UI, 0.5-0.8s for reveals
2. **Use ease-out** for entrances, ease-in for exits
3. **One orchestrated moment** beats scattered micro-interactions
4. **Reduce motion** - Always respect `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
