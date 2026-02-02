# Tasks API (quick reference)

Use this when you need automation without the interactive `coder` CLI.

## Auth

All examples below require a **Coder session token**:

- Get it via CLI: `coder login token`
- Use it as an HTTP header: `Coder-Session-Token: <token>`

Assume:

```bash
export CODER_URL="https://coder.example.com"
export CODER_SESSION_TOKEN="..." # from `coder login token`
```

## List tasks

```bash
curl -sS "$CODER_URL/api/v2/tasks?q=owner:me" \
  -H "Accept: application/json" \
  -H "Coder-Session-Token: $CODER_SESSION_TOKEN"
```

## Get task (by id or name)

```bash
curl -sS "$CODER_URL/api/v2/tasks/me/<task>" \
  -H "Accept: application/json" \
  -H "Coder-Session-Token: $CODER_SESSION_TOKEN"
```

## Get logs

```bash
curl -sS "$CODER_URL/api/v2/tasks/me/<task>/logs" \
  -H "Accept: application/json" \
  -H "Coder-Session-Token: $CODER_SESSION_TOKEN"
```

## Send input

```bash
curl -sS -X POST "$CODER_URL/api/v2/tasks/me/<task>/send" \
  -H "Content-Type: application/json" \
  -H "Coder-Session-Token: $CODER_SESSION_TOKEN" \
  -d '{"input":"Please also add unit tests."}'
```

## Delete task

```bash
curl -sS -X DELETE "$CODER_URL/api/v2/tasks/me/<task>" \
  -H "Coder-Session-Token: $CODER_SESSION_TOKEN"
```

## Create task (note)

Task creation requires a `template_version_id` (and optionally a `template_version_preset_id`), so for most workflows the simplest automation is:

```bash
coder task create --quiet --template <task-template> --preset "<preset>" "<prompt>"
```
