---
sidebar_label: logging
title: core.logging
---

#### set\_level

```python
def set_level(level: int) -> None
```

Sets the global logging level.

**Arguments**:

- `level` - The logging level.

#### debug

```python
def debug(msg: str, *, scope: str | None = None, **kwargs)
```

Logs a debugging message.

**Arguments**:

- `msg` - The text to log.
- `scope` - The scope of the entry.
- `**kwargs` - Any additional parameters.

#### info

```python
def info(msg: str, *, scope: str | None = None, **kwargs)
```

Logs an information message.

**Arguments**:

- `msg` - The text to log.
- `scope` - The scope of the entry.
- `**kwargs` - Any additional parameters.

#### warning

```python
def warning(msg: str, *, scope: str | None = None, **kwargs)
```

Logs a warning message.

**Arguments**:

- `msg` - The text to log.
- `scope` - The scope of the entry.
- `**kwargs` - Any additional parameters.

#### error

```python
def error(msg: str, *, scope: str | None = None, **kwargs)
```

Logs an error message.

**Arguments**:

- `msg` - The text to log.
- `scope` - The scope of the entry.
- `**kwargs` - Any additional parameters.

#### default\_logger

```python
def default_logger() -> Logger
```

Retrieves the default (global) logger.

