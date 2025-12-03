# Настроить защиту от утечки секретов

Запусти скилл `vi-skills:secrets-guardian` через Skill tool и выполни **Setup Protection**:

1. Проверь существующую защиту:
```bash
ls -la .pre-commit-config.yaml .secrets.baseline .gitignore 2>/dev/null
```

2. Если .pre-commit-config.yaml отсутствует — скопируй из assets скилла

3. Проверь .gitignore на паттерны секретов, добавь если нет

4. Создай .secrets.baseline

5. Установи hooks:
```bash
pre-commit install
pre-commit install --hook-type pre-push
```

6. Спроси про GitHub Actions workflow для CI
