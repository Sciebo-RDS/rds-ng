---
sidebar_label: event
title: core.messaging.event
---

## Event Objects

```python
@dataclass(frozen=True, kw_only=True)
class Event(Message)
```

An event message.

Events are simple notifications that do not require a reply nor will *execute* anything.

#### EventType

pylint: disable=invalid-name

