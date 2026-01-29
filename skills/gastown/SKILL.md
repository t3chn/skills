---
name: gastown
description: "Work with Gas Town (gastown) and the `gt` CLI: install/setup a town (`gt install`), manage rigs/crew/polecats, run mayor/deacon/witness/refinery, use convoys + beads (`bd`) + mail, recover context via `gt prime`, and troubleshoot common failures (doctor, sparse-checkout, routing). Also use when contributing to `github.com/steveyegge/gastown` (Go + Cobra subcommands in `internal/cmd`, templates in `templates/`, wrappers like `gt-codex`). Triggers: gastown/Gas Town/gt/convoy/sling/mayor/deacon/witness/prime/beads/bd (и русские: мэр/полкэт/прайм)."
---

# Gastown (Gas Town / `gt`)

## Overview

Системно решать задачи по Gas Town: от установки и ежедневной работы в Town/Rig до внесения изменений в исходники CLI.

## Быстрый выбор сценария

- **Использование `gt` (операции)**: пользователь настраивает/использует Gas Town как инструмент (workspace `~/gt`, роли, convoys, sling, mail, prime).
- **Разработка `gastown` (код)**: пользователь меняет репозиторий `github.com/steveyegge/gastown` (команды CLI, шаблоны, тесты, релизные штуки).

## Операции: установка и ежедневная работа (`gt`)

1) Проверить окружение
   - Нужны: Go (смотри `go.mod` в репо), Git, `bd` (beads).
   - Опционально: tmux, Claude Code, Codex CLI, OpenCode CLI.

2) Поставить `gt` и `bd`
   - `brew install gastown` или `go install github.com/steveyegge/gastown/cmd/gt@latest`
   - `go install github.com/steveyegge/beads/cmd/bd@latest`

3) Создать Town и первый Rig
   - `gt install ~/gt --git` (или без `--git`, если git-инициализация не нужна)
   - `cd ~/gt`
   - `gt rig add <rig-name> <git-url>`
   - `gt crew add <you> --rig <rig-name>` и перейти в `~/gt/<rig>/crew/<you>/rig/`

4) Запустить координацию и работу
   - Mayor: `gt mayor attach`
   - Трекинг: `gt convoy create ...`, `gt convoy list`, `gt convoy show`
   - Раздача задач: `gt sling <bead-id> <rig-name>`

5) Восстановление/инъекция контекста
   - Основная команда: `gt prime` (особенно после “новой сессии”, очистки контекста и т.п.).
   - Если роль автономная и нужна почта: `gt mail check --inject` (когда это уместно для конкретного рантайма/роли).

## Codex CLI: как не потерять контекст

- Предпочитать `gt-codex` вместо `codex`, чтобы перед стартом автоматически выполнялся `gt prime`.
  - Установить врапперы: `gt install --wrappers` (или совместить с `gt install ... --wrappers`).
- Если врапперов нет: запускать `gt prime` вручную после старта сессии Codex.
- Если Codex не подхватывает роль-инструкции по файлам проекта: настроить `project_doc_fallback_filenames = ["CLAUDE.md"]` в `~/.codex/config.toml` (как рекомендует README проекта).

## Диагностика и типовые поломки

- Запускать `gt doctor` (и `gt doctor --fix`, если это безопасно и ожидаемо).
- При проблемах с маршрутизацией beads: включать `BD_DEBUG_ROUTING=1` для команды `bd ...`.
- При “странном” контексте/инструкциях: проверять, что работа идёт внутри Town/Rig-дерева и что применён `gt prime`.
- При проблемах со sparse-checkout/изоляцией репо: `gt doctor --fix`.

## Разработка: вклад в репозиторий `gastown`

1) Сборка и тесты
   - `make build` (включает `go generate ./...`)
   - `make test` или `go test ./...`

2) Карта кода (с чего начинать)
   - Точка входа CLI: `cmd/gt/main.go`
   - Cobra-команды: `internal/cmd/*.go` (обычно “файл = команда/подкоманда”)
   - Prime/инъекция контекста: `internal/cmd/prime*.go`
   - Врапперы для рантаймов: `internal/wrappers/` (например, `gt-codex`)
   - Шаблоны контекста/агентов: `templates/`
   - Документация: `README.md`, `docs/overview.md`, `docs/reference.md`, `docs/INSTALLING.md`

3) Изменение/добавление CLI-команд
   - Держать UX стабильным: не ломать флаги/форматы вывода без миграции.
   - Добавлять/править тесты рядом в `internal/cmd/*_test.go` (по аналогии с существующими).
   - Обновлять docs/README, если команда пользовательская.

## References (load as needed)

- Reading map + grep-подсказки: `references/reading-map.md`
