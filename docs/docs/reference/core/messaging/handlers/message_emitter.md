---
sidebar_label: message_emitter
title: core.messaging.handlers.message_emitter
---

## MessageEmitter Objects

```python
class MessageEmitter()
```

A helper class to easily create and emit messages.

This class stores a reference to the global message bus and offers methods to easily create new messages and send them through the bus.

#### \_\_init\_\_

```python
def __init__(origin_id: UnitID, message_bus: MessageBusProtocol)
```

**Arguments**:

- `origin_id` - The component identifier of the origin of newly created messages.
- `message_bus` - The global message bus to use.

#### emit\_command

```python
def emit_command(cmd_type: type[CommandType],
                 target: Channel,
                 done_callback: CommandDoneCallback | None = None,
                 fail_callback: CommandFailCallback | None = None,
                 async_callbacks: bool = False,
                 timeout: float = 0.0,
                 chain: Message | None = None,
                 **kwargs) -> MessageType
```

Emits a new command.

**Arguments**:

- `cmd_type` - The command type (i.e., a subclass of ``Command``).
- `target` - The destination of the message.
- `done_callback` - Callback when a reply for the command was received.
- `fail_callback` - Callback when no reply for the command was received.
- `async_callbacks` - Whether to execute the callbacks asynchronously in their own thread.
- `timeout` - The timeout (in seconds) until a command is deemed *not answered*. Pass ``0`` to disable timeouts.
- ``0 - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
- ``1 - Additional parameters.
  

**Returns**:

  The newly created command.
  

**Raises**:

- ``2 - ``cmd_type`` is not a subclass of ``Command``.

#### emit\_reply

```python
def emit_reply(reply_type: type[CommandReplyType],
               command: CommandType,
               *,
               success: bool = True,
               message: str = "",
               **kwargs) -> MessageType
```

Emits a new command reply.

Most parameters, like the proper target, are extracted from the originating command.

**Arguments**:

- `reply_type` - The reply type (i.e., a subclass of ``CommandReply``).
- `command` - The ``Command`` this reply is based on.
- `success` - Whether the command *succeeded* or not (how this is interpreted depends on the command).
- `message` - Additional message to include in the reply.
- `**kwargs` - Additional parameters.
  

**Returns**:

  The newly created command reply.
  

**Raises**:

- `RuntimeError` - ``reply_type`` is not a subclass of ``CommandReply``.

#### emit\_event

```python
def emit_event(event_type: type[EventType],
               target: Channel,
               chain: Message | None = None,
               **kwargs) -> MessageType
```

Emits a new event.

**Arguments**:

- `event_type` - The event type (i.e., a subclass of ``Event``).
- `target` - The destination of the message.
- `chain` - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
- `**kwargs` - Additional parameters.
  

**Returns**:

  The newly created event.
  

**Raises**:

- `RuntimeError` - ``event_type`` is not a subclass of ``Event``.

#### get\_message\_count

```python
def get_message_count(msg_type: MessageType) -> int
```

Gets how many messages of specific message types have beeen emitted.

The message emitter keeps track of how many messages of the three major types ``Command``, ``CommandReply`` and
``Event`` have been emitted.

**Arguments**:

- `msg_type` - The message type to get the count of. Must be either ``Command``, ``CommandReply`` or ``Event``.
  

**Returns**:

  The number of messages already emitted of the specified type.

