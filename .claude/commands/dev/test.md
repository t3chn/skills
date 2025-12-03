# Testing

Определи язык проекта и запусти соответствующий скилл тестирования.

## Автоопределение

Проверь файлы в корне проекта:

```bash
ls pyproject.toml setup.py requirements.txt package.json go.mod Cargo.toml 2>/dev/null
```

| Файл | Язык | Скилл |
|------|------|-------|
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python | `vi-skills:python-testing` |
| `package.json` | TypeScript/JS | (TODO: typescript-testing) |
| `go.mod` | Go | (TODO: go-testing) |
| `Cargo.toml` | Rust | (TODO: rust-testing) |

## Действие

1. Если **Python** → запусти `vi-skills:python-testing`
2. Если язык не поддерживается → сообщи что скилл ещё не создан
3. Если несколько языков → спроси какой тестировать
