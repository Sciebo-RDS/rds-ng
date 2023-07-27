---
sidebar_label: formatter
title: core.logging.formatter
---

## Formatter Objects

```python
class Formatter(logging.Formatter)
```

Customized log formatter.

This formatter mainly colorizes log records for better readability.

#### format

```python
def format(record: logging.LogRecord) -> str
```

Colorizes the various portions of a log record.

**Returns**:

  The formatted text.

