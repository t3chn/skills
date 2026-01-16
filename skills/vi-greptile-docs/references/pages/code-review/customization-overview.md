# Customization Overview

URL: https://www.greptile.com/docs/code-review/customization-overview

Greptile offers two methods to customize review behavior: the **Dashboard UI** and ** greptile.json**.

## Configuration Methods

* Dashboard UI
* greptile.json

```
Organization-wide defaults at [app.greptile.com](https://app.greptile.com/).
```

* Changes apply immediately
* No code commits required
* Affects all repositories

Repository-specific overrides in your repo root.

* Version controlled
* Reviewed in PRs
* Supports advanced features like pattern repositories

**Configuration hierarchy:** `greptile.json` (if present) overrides dashboard settings for that repository.

## In This Section
