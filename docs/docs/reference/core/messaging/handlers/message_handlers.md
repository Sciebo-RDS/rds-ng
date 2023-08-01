---
sidebar_label: message_handlers
title: core.messaging.handlers.message_handlers
---

## MessageHandlers Objects

```python
class MessageHandlers()
```

Holds mappings for message handlers.

#### add\_handler

```python
def add_handler(fltr: str,
                handler: MessageHandler,
                message_type: type[MessageType] = Message,
                is_async: bool = False) -> None
```

Adds a new message handler mapping.

**Arguments**:

- `fltr` - The message name filter.
- `handler` - The message handler.
- `message_type` - The message type the handler expects.
- `is_async` - Whether the handler should be invoked asynchronously in its own thread.

#### find\_handlers

```python
def find_handlers(msg_name: MessageName) -> MessageHandlerMappings
```

Finds all handlers that fit the given ``msg_name``.

The message name filter can be a complete message name, or a wildcard pattern using asterisks (*).

**Arguments**:

- `msg_name` - The message name (pattern).
  

**Returns**:

  A list of all found message handlers.

