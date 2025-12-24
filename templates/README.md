# Project Templates

Reusable templates for production-ready projects.

## GitHub Actions CI

```bash
# Copy to your project
mkdir -p .github/workflows
cp templates/github-actions/ci.yml .github/workflows/ci.yml
```

### Features

- **Pre-commit checks** - linting, formatting
- **Type checking** - mypy (Python), tsc (TypeScript)
- **Security scanning** - Semgrep, Gitleaks, Bandit
- **Tests with coverage** - pytest, vitest, go test
- **Language auto-detection** - only runs relevant jobs

### Customization

1. Enable language-specific jobs by uncommenting them
2. Add language jobs to the `ci-success.needs` array
3. Configure coverage thresholds in your tooling config
4. Add deployment steps for your infrastructure

### Language Support

| Language | Lint | Types | Security | Tests |
|----------|------|-------|----------|-------|
| Python | Ruff | mypy | Bandit | pytest |
| TypeScript | Biome | tsc | Semgrep | vitest/bun |
| Go | golangci-lint | built-in | Semgrep | go test |
| Rust | clippy | built-in | Semgrep | cargo test |

## Related Skills

- `pre-commit` config in repo root
- Convention skills for language-specific patterns
- `secrets-guardian` skill for secrets detection
