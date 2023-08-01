---
sidebar_label: message_handler
title: core.messaging.handlers.message_handler
---

## MessageHandlerMapping Objects

```python
@dataclass(frozen=True)
class MessageHandlerMapping()
```

Mapping from a message name filter to a message handler.

**Attributes**:

- `filter` - The message name filter.
- `handler` - The message handler.
- `message_type` - The message type the handler expects.
- `is_async` - Whether the handler should be invoked asynchronously in its own thread.

