# Debugging / Logs

Use this when prek behaves unexpectedly or hook installs fail.

## Verbose output

Increase verbosity:

```bash
uvx prek run -vvv
```

## Trace log file

By default, prek writes a trace log to:

- `~/.cache/prek/prek.log`

Override with:

```bash
uvx prek run --log-file /tmp/prek.log
```

When reporting issues, include the log file.
