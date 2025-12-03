# Backend Development

Определи язык проекта и запусти соответствующий скилл.

## Автоопределение

Проверь файлы в корне проекта:

```bash
ls pyproject.toml setup.py requirements.txt package.json tsconfig.json go.mod Cargo.toml 2>/dev/null
```

| Файл | Язык | Скилл |
|------|------|-------|
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python | `vi-skills:backend-python` |
| `package.json`, `tsconfig.json` | Node.js/TS | `vi-skills:backend-nodejs` |
| `go.mod` | Go | (TODO: backend-go) |
| `Cargo.toml` | Rust | (TODO: backend-rust) |

## Действие

1. **Всегда** загружай `vi-skills:backend-core` для общих паттернов
2. **Затем** загружай языковой скилл:
   - Python → `vi-skills:backend-python`
   - Node.js/TypeScript → `vi-skills:backend-nodejs`
3. Если язык не поддерживается → сообщи что скилл ещё не создан
4. Если несколько языков → спроси какой использовать
