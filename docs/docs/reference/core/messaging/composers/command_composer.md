---
sidebar_label: command_composer
title: core.messaging.composers.command_composer
---

## CommandComposer Objects

```python
class CommandComposer(MessageComposer)
```

Composer for ``Command`` messages.

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

#### done

```python
def done(callback: CommandDoneCallback) -> typing.Self
```

Adds a *Done* callback.

**Arguments**:

- `callback` - The callback to add.
  

**Returns**:

  This composer instance to allow call chaining.

#### failed

```python
def failed(callback: CommandFailCallback) -> typing.Self
```

Adds a *Fail* callback.

**Arguments**:

- `callback` - The callback to add.
  

**Returns**:

  This composer instance to allow call chaining.

#### async\_callbacks

```python
def async_callbacks(async_cbs: bool) -> typing.Self
```

Sets whether to use asynchronous callbacks.

**Arguments**:

- `async_cbs` - Enable asynchronous callbacks.
  

**Returns**:

  This composer instance to allow call chaining.

#### timeout

```python
def timeout(timeout: float) -> typing.Self
```

Sets a reply timeout.

**Arguments**:

- `timeout` - The timeout (in seconds).
  

**Returns**:

  This composer instance to allow call chaining.

