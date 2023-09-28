---
sidebar_label: message_service
title: core.messaging.handlers.message_service
---

## MessageService Objects

```python
class MessageService()
```

Base class for all message services.

A *message service* wraps message handlers and proper message context creation (i.e., using a flexible context type). It
is used by the message bus as an encapsulated layer for message dispatching.

#### \_\_init\_\_

```python
def __init__(comp_id: UnitID,
             *,
             message_bus: MessageBusProtocol,
             context_type: type[MessageContextType] = MessageContext)
```

**Arguments**:

- `comp_id` - The global component identifier.
- `message_bus` - The global message bus.
- `context_type` - The type to use when creating a message context.

#### create\_context

```python
def create_context(msg_meta: MessageMetaInformation, *, logger: LoggerProtocol,
                   config: Configuration) -> MessageContext
```

Creates a new service context.

**Arguments**:

- `msg_meta` - The meta information of the message.
- `logger` - The logger to be used within the new context.
- `config` - The global component configuration.
  

**Returns**:

  The newly created message context.

#### create\_message\_builder

```python
def create_message_builder() -> MessageBuilder
```

Creates a new message builder.

**Returns**:

  The newly created message builder.

#### message\_handlers

```python
@property
def message_handlers() -> MessageHandlers
```

The message handlers maintained by this message service.

