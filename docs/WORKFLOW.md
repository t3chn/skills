# Git Workflow для AI-разработки

Trunk-based development с git worktrees для параллельной работы AI-агентов.

## Стратегия ветвления

```
main (always deployable)
├── feature/auth-system     (max 1-2 days)
├── fix/parser-bug          (max 1 day)
└── refactor/api-cleanup    (max 2 days)
```

**Правила:**
- Все изменения через feature branches
- Ветка живёт максимум 1-2 дня
- Merge через PR с code review
- main всегда deployable

## Параллельная работа (Worktrees)

Git worktrees позволяют работать над несколькими ветками одновременно в разных директориях:

```
~/projects/skills/              # main worktree
~/projects/skills/.trees/
├── feature-auth/              # Agent 1
├── fix-parser/                # Agent 2
└── docs-update/               # Agent 3
```

### Создание worktree

```bash
# Через helper script
./scripts/setup-worktree.sh feature/my-feature

# Или напрямую
git worktree add .trees/feature-my-feature -b feature/my-feature main
```

### Работа в worktree

```bash
cd .trees/feature-my-feature

# ... edit, commit ...

git push -u origin feature/my-feature
# Создать PR в GitHub
```

### Удаление после merge

```bash
git worktree remove .trees/feature-my-feature
git branch -d feature/my-feature
```

### Список worktrees

```bash
git worktree list
```

## Conventional Commits

Формат: `type(scope): message`

| Тип | Описание |
|-----|----------|
| `feat:` | Новая функциональность |
| `fix:` | Исправление бага |
| `docs:` | Документация |
| `test:` | Тесты |
| `refactor:` | Рефакторинг без изменения поведения |
| `style:` | Форматирование, стиль кода |
| `chore:` | Прочее (CI, deps, configs) |
| `ci:` | CI/CD изменения |

**Примеры:**
```bash
git commit -m "feat(auth): add JWT token refresh"
git commit -m "fix(parser): handle empty input"
git commit -m "docs: update workflow documentation"
git commit -m "test(api): add integration tests"
```

## Pre-Push Validation

При каждом push автоматически запускаются:

| Проверка | Языки | Инструмент |
|----------|-------|------------|
| Linting | Python | ruff |
| Linting | TypeScript | biome |
| Linting | Go | golangci-lint |
| Linting | Rust | clippy |
| Formatting | All | язык-специфичные |
| Secrets | All | gitleaks |
| Tests | All | pytest, go test, etc |

### Локальная проверка

```bash
# Все проверки
pre-commit run --all-files

# Конкретный hook
pre-commit run ruff-check --all-files

# Только изменённые файлы
pre-commit run
```

### Установка hooks

```bash
pip install pre-commit
pre-commit install --install-hooks -t pre-commit -t pre-push -t commit-msg
```

## CI/CD (GitHub Actions)

### На каждый PR:
- **Lint** — pre-commit для всех файлов
- **Test Python** — pytest в каждом Python проекте
- **Test Go** — go test в каждом Go проекте
- **Test Node** — npm/pnpm test в каждом Node проекте
- **Test Rust** — cargo test в каждом Rust проекте
- **Security** — gitleaks + dependency audit

### Branch protection (рекомендуется):
- Require PR reviews
- Require status checks to pass
- Require up-to-date branches

## Пример workflow

```bash
# 1. Создать worktree для новой задачи
./scripts/setup-worktree.sh feature/user-auth

# 2. Перейти в worktree
cd .trees/feature-user-auth

# 3. Разработка с TDD
# ... write tests first, then implementation ...

# 4. Commit с conventional message
git add .
git commit -m "feat(auth): implement JWT authentication"

# 5. Push (pre-push hooks запустят тесты)
git push -u origin feature/user-auth

# 6. Создать PR в GitHub

# 7. После merge — cleanup
cd ../..
git worktree remove .trees/feature-user-auth
git branch -d feature/user-auth
git pull
```

## Интеграция с TDD Enforcer

tdd-enforcer плагин проверяет при завершении сессии:
- Был ли изменён код
- Были ли запущены тесты

Если код изменён без тестов — warning (или block в strict mode).

Конфигурация: `.claude/tdd-enforcer.local.md`

## Troubleshooting

### Hook failed

```bash
# Пропустить hooks (только для debugging!)
git commit --no-verify -m "message"
git push --no-verify

# Обновить hooks
pre-commit autoupdate
pre-commit install --install-hooks
```

### Worktree conflicts

```bash
# Список worktrees
git worktree list

# Удалить "мёртвый" worktree
git worktree prune

# Force remove
git worktree remove --force .trees/broken-worktree
```
