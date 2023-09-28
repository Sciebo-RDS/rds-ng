---
sidebar_label: command_reply_composer
title: core.messaging.composers.command_reply_composer
---

## CommandReplyComposer Objects

```python
class CommandReplyComposer(MessageComposer)
```

Composer for ``CommandReply`` messages.

#### \_\_init\_\_

```python
def __init__(origin_id: UnitID, message_bus: MessageBusProtocol,
             msg_type: type[MessageType], command: CommandType, **kwargs)
```

**Arguments**:

- `origin_id` - The component identifier of the origin of newly created messages.
- `message_bus` - The global message bus to use.
- `msg_type` - The message type.
- `command` - The ``Command`` this reply is based on.
- `**kwargs` - Additional message parameters.

#### emit

```python
def emit() -> None
```

Sends the built message through the message bus.

