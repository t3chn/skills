# Secret Scanning Tools Reference

## Gitleaks

Fast, lightweight secret scanner.

**Installation:**
```bash
# macOS
brew install gitleaks

# Linux (download binary)
wget https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_8.21.2_linux_x64.tar.gz
```

**Commands:**
```bash
# Scan current directory (no git history)
gitleaks detect --no-git -v

# Scan git history
gitleaks detect -v

# Scan specific path
gitleaks detect --source /path/to/code -v

# Generate report
gitleaks detect -f json -r report.json
```

**Configuration:** `.gitleaks.toml`
```toml
[allowlist]
paths = [
    '''tests/fixtures/''',
    '''\.secrets\.baseline''',
]
```

---

## detect-secrets

Yelp's secret scanner with baseline support.

**Installation:**
```bash
pip install detect-secrets
```

**Commands:**
```bash
# Scan all files
detect-secrets scan

# Scan with baseline (only new secrets)
detect-secrets scan --baseline .secrets.baseline

# Update baseline (mark false positives)
detect-secrets scan --baseline .secrets.baseline

# Audit baseline interactively
detect-secrets audit .secrets.baseline
```

**Baseline format:** `.secrets.baseline`
```json
{
  "version": "1.5.0",
  "plugins_used": [...],
  "results": {
    "file.py": [
      {
        "type": "Secret Keyword",
        "line_number": 10,
        "is_secret": false
      }
    ]
  }
}
```

---

## TruffleHog

Deep secret scanner with verification.

**Installation:**
```bash
# macOS
brew install trufflehog

# Docker
docker pull trufflesecurity/trufflehog
```

**Commands:**
```bash
# Scan directory
trufflehog filesystem /path/to/code

# Scan git repo
trufflehog git file:///path/to/repo

# Only verified secrets (API calls to check validity)
trufflehog filesystem /path --only-verified

# Scan GitHub org
trufflehog github --org=myorg
```

---

## Bandit (Python)

Python security linter.

**Installation:**
```bash
pip install bandit
```

**Commands:**
```bash
# Scan directory
bandit -r src/

# With config
bandit -c pyproject.toml -r src/

# Only high severity
bandit -r src/ -ll
```

**Configuration:** `pyproject.toml`
```toml
[tool.bandit]
exclude_dirs = ["tests", ".venv"]
skips = ["B101"]  # Skip assert warnings
```

---

## Semgrep

Multi-language SAST scanner.

**Installation:**
```bash
pip install semgrep
# or
brew install semgrep
```

**Commands:**
```bash
# Auto-detect rules
semgrep --config auto

# Security rules only
semgrep --config p/security-audit

# Secrets rules
semgrep --config p/secrets
```

---

## Pre-commit

Hook manager for all tools.

**Installation:**
```bash
pip install pre-commit
```

**Commands:**
```bash
# Install hooks
pre-commit install
pre-commit install --hook-type pre-push

# Run manually
pre-commit run --all-files

# Run specific hook
pre-commit run gitleaks --all-files

# Update hooks to latest versions
pre-commit autoupdate

# Uninstall
pre-commit uninstall
```

---

## Quick Comparison

| Tool | Speed | False Positives | Verification | Best For |
|------|-------|-----------------|--------------|----------|
| Gitleaks | Fast | Low | No | Pre-commit, CI |
| detect-secrets | Medium | Medium (baseline helps) | No | Baseline tracking |
| TruffleHog | Slow | Very Low | Yes | Deep scans, CI |
| Bandit | Fast | Medium | No | Python code |
| Semgrep | Medium | Low | No | Multi-language SAST |

**Recommended combination:**
- Pre-commit: gitleaks + detect-secrets
- CI: gitleaks + trufflehog (--only-verified)
