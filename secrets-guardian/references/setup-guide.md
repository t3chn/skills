# Secrets Protection Setup Guide

Step-by-step guide to configure multi-layered secret protection.

## Prerequisites

```bash
# Install pre-commit
pip install pre-commit

# Optional: Install gitleaks for manual scanning
# macOS
brew install gitleaks

# Linux
# Download from https://github.com/gitleaks/gitleaks/releases
```

## Step 1: Configure Pre-commit

### New Project

```bash
# Copy pre-commit config
cp /path/to/assets/pre-commit-config.yaml .pre-commit-config.yaml

# Or create minimal config:
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
EOF
```

### Existing Project with Pre-commit

Add to existing `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

## Step 2: Create Secrets Baseline

```bash
# Create empty baseline
echo '{"version": "1.5.0", "results": {}}' > .secrets.baseline

# Or scan existing codebase and create baseline
detect-secrets scan > .secrets.baseline
```

## Step 3: Update .gitignore

Append secret patterns:

```bash
cat >> .gitignore << 'EOF'

# Secrets - NEVER commit!
.env
.env.*
!.env.example
*.env
secrets.yaml
*.secret
*.key
*.pem
*_API_KEY*
credentials.json
EOF
```

## Step 4: Install Hooks

```bash
# Install pre-commit hook
pre-commit install

# Install pre-push hook (recommended)
pre-commit install --hook-type pre-push

# Verify installation
ls -la .git/hooks/pre-commit .git/hooks/pre-push
```

## Step 5: Test Setup

```bash
# Run all hooks on all files
pre-commit run --all-files

# Test with a fake secret
echo "API_KEY=sk-1234567890abcdef" > test-secret.txt
git add test-secret.txt
git commit -m "test"  # Should fail!
rm test-secret.txt
```

## Step 6: CI/CD Integration (Optional)

Copy workflow to GitHub Actions:

```bash
mkdir -p .github/workflows
cp /path/to/assets/security-workflow.yaml .github/workflows/security.yaml
```

## Troubleshooting

### Hook fails on false positive

Update baseline to exclude:

```bash
detect-secrets scan --baseline .secrets.baseline
git add .secrets.baseline
git commit -m "Update secrets baseline"
```

### Gitleaks too slow

Add `.gitleaksignore` for known safe patterns:

```
# .gitleaksignore
tests/fixtures/
*.test.js
```

### Pre-commit not running

Reinstall hooks:

```bash
pre-commit uninstall
pre-commit install
pre-commit install --hook-type pre-push
```

## Verification Checklist

- [ ] `.pre-commit-config.yaml` exists with gitleaks + detect-secrets
- [ ] `.secrets.baseline` exists
- [ ] `.gitignore` has secret patterns
- [ ] `pre-commit run --all-files` passes
- [ ] `.git/hooks/pre-commit` exists
- [ ] `.git/hooks/pre-push` exists (optional)
- [ ] CI workflow configured (optional)
