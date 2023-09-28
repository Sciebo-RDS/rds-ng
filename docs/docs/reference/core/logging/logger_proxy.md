---
sidebar_label: logger_proxy
title: core.logging.logger_proxy
---

## LoggerProxy Objects

```python
class LoggerProxy()
```

A proxy to automatically pass extra parameters to a logger.

This class allows us to store additional, fixed parameters passed to an existing logger, avoiding the need to use
a new logger instance. It offers the same public interface as an actual ``Logger`` and can thus be used like a
*real* logger.

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

**Arguments**:

- `logger` - The logger to use.

#### add\_param

```python
def add_param(name: str, value: typing.Any) -> None
```

Adds a new paramter that is always automatically passed to the logger.

**Arguments**:

- `name` - The name of the parameter.
- `value` - Its value.

#### remove\_param

```python
def remove_param(name: str) -> None
```

Removes a parameter that has been added previously.

**Arguments**:

- `name` - The name of the parameter.

#### clear\_params

```python
def clear_params() -> None
```

Removes all stored parameters.

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

