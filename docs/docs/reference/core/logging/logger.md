---
sidebar_label: logger
title: core.logging.logger
---

## Logger Objects

```python
class Logger(logging.Logger)
```

A customized logger offering advanced formatting and parameters listing.

This logger and its corresponding ``Formatter`` display the log level, scope, as well as a parameters listing
in a color-rich format for easy readability.

#### \_\_init\_\_

```python
def __init__(name: str, level: int = logging.INFO)
```

**Arguments**:

- `name` - The name of the logger.
- `level` - The maximum level for log entries to be displayed.

#### setLevel

```python
def setLevel(level: int) -> None
```

Sets the logging level of this logger.

**Arguments**:

- `level` - The maximum level for entries to be logged.

#### debug

```python
def debug(msg: str, *, scope: str | None = None, **kwargs) -> None
```

Logs a debugging message.

**Arguments**:

- `msg` - The text to log.
- `scope` - The scope of the entry.
- `**kwargs` - Any additional parameters.

#### info

```python
def info(msg: str, *, scope: str | None = None, **kwargs) -> None
```

Logs an information message.

**Arguments**:

- `msg` - The text to log.
- `scope` - The scope of the entry.
- `**kwargs` - Any additional parameters.

#### warning

```python
def warning(msg: str, *, scope: str | None = None, **kwargs) -> None
```

Logs a warning message.

**Arguments**:

- `msg` - The text to log.
- `scope` - The scope of the entry.
- `**kwargs` - Any additional parameters.

#### error

```python
def error(msg: str, *, scope: str | None = None, **kwargs) -> None
```

Logs an error message.

**Arguments**:

- `msg` - The text to log.
- `scope` - The scope of the entry.
- `**kwargs` - Any additional parameters.

