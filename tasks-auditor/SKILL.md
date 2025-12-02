---
name: tasks-auditor
description: |
  End-of-day audit of beads tasks across multiple projects.
  Triggers: "аудит задач", "проверь задачи", "audit tasks", "ревизия задач", "end of day review"
---

# Tasks Auditor

Аудит задач beads во всех проектах. Проверяет здоровье БД, дубли, stale задачи, orphaned dependencies.

## Когда использовать

- В конце рабочего дня
- При переключении между проектами
- Когда нужно понять общую картину по задачам

## Проекты для аудита

По умолчанию проверяются:
- `/Users/vi/projects/forgequant/context8-mcp`
- `/Users/vi/itools/checko-mcp`

## Процедура аудита

Для каждого проекта выполни команды **последовательно**:

### 1. Статистика (главное)
```bash
cd /path/to/project && bd count --by-status
```

### 2. Открытые задачи
```bash
bd list --status open
```

### 3. Задачи в работе
```bash
bd list --status in_progress
```

### 4. Stale задачи (>7 дней)
```bash
bd stale --days 7
```

### 5. Дубликаты
```bash
bd duplicates --dry-run
```

### 6. Orphaned dependencies
```bash
bd repair-deps
```

### 7. Health check
```bash
bd doctor
```

## Формат отчёта

После выполнения команд, сформируй отчёт:

```markdown
# Аудит задач [дата]

## Сводка
- Проверено проектов: N
- Критических проблем: N
- Предупреждений: N

## Проекты

### [project-name]
**Статус:** ✅ Healthy | ⚠️ Issues | ❌ Critical

| Open | In Progress | Blocked | Closed |
|------|-------------|---------|--------|
| N    | N           | N       | N      |

**Open tasks:** (если есть)
- task-id: Title

---

## Предупреждения

### Stale задачи
- [project] task-id: Title (N дней)

### Дубликаты
- [project] task-a = task-b

### Orphaned deps
- [project] task-id → deleted-task

## Рекомендации
- [ ] Конкретное действие
```

## Классификация проблем

**Critical (❌):**
- Database corruption
- Validation failures

**Warning (⚠️):**
- Stale tasks (>7 дней без обновлений)
- Duplicates
- Orphaned dependencies
- Tasks in_progress без активности

**Healthy (✅):**
- Нет проблем
