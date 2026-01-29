# Gas Town (gastown) — reading map

## Docs (в репозитории `gastown`)

- Быстрый обзор/установка/команды: `README.md`
- Концепты (роли, convoy, lifecycles): `docs/overview.md`, `docs/glossary.md`
- Тех. устройство (директории, config, prime, sparse-checkout): `docs/reference.md`
- Полная установка: `docs/INSTALLING.md`
- Дизайн-заметки: `docs/design/`

## Code entry points (в репозитории `gastown`)

- CLI entrypoint: `cmd/gt/main.go`
- Cobra root + регистрация команд: `internal/cmd/root.go`
- Команда `gt prime` и её варианты: `internal/cmd/prime*.go`
- Install + wrappers флаг: `internal/cmd/install.go`
- Врапперы для Codex/OpenCode: `internal/wrappers/` (шаблоны в `internal/wrappers/scripts/`)
- Шаблоны контекста/агентов: `templates/`

## Полезные `rg`-паттерны (в репозитории `gastown`)

- Найти реализацию подкоманды:
  - `rg -n 'Use: \"sling\"' internal/cmd -S`
  - `rg -n 'Use: \"prime\"' internal/cmd -S`
- Быстро найти место регистрации:
  - `rg -n 'AddCommand\\(' internal/cmd/root.go -S`
- Найти конфиг-ключ/лейбл:
  - `rg -n 'polecat_branch_template' -S`
  - `rg -n 'role_agents' -S`

## Runtime/Codex hints

- Для Codex удобнее запускать `gt-codex` (враппер) вместо `codex`, чтобы автоматически делать `gt prime`.
- Если после старта сессии “нет роли/контекста” — начать с `gt prime`, дальше смотреть `docs/reference.md` (секция про `CLAUDE.md` и injection).
