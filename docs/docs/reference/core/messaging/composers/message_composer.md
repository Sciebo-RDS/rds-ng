---
sidebar_label: message_composer
title: core.messaging.composers.message_composer
---

## MessageComposer Objects

```python
class MessageComposer(abc.ABC)
```

A class to collect all information necessary to create and emit a message.

#### \_\_init\_\_

```python
def __init__(origin_id: UnitID,
             message_bus: MessageBusProtocol,
             msg_type: type[MessageType],
             chain: Message | None = None,
             **kwargs)
```

**Arguments**:

- `origin_id` - The component identifier of the origin of newly created messages.
- `message_bus` - The global message bus to use.
- `msg_type` - The message type.
- `chain` - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
- `**kwargs` - Additional message parameters.

#### before

```python
def before(callback: BeforeDispatchCallback) -> typing.Self
```

Adds a callback that will be called immediately before the message is dispatched.

**Arguments**:

- `callback` - The callback to add.
  

**Returns**:

  This composer instance to allow call chaining.

#### emit

```python
def emit(target: Channel) -> None
```

Sends the built message through the message bus.

**Arguments**:

- `target` - The target of the message.

