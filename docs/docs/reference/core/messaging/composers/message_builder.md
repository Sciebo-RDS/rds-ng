---
sidebar_label: message_builder
title: core.messaging.composers.message_builder
---

## MessageBuilder Objects

```python
class MessageBuilder()
```

A helper class to easily build and emit new messages.

This class stores a reference to the global message bus and offers methods to easily create new messages and send them through the bus.

#### \_\_init\_\_

```python
def __init__(origin_id: UnitID, message_bus: MessageBusProtocol)
```

**Arguments**:

- `origin_id` - The component identifier of the origin of newly created messages.
- `message_bus` - The global message bus to use.

#### build\_command

```python
def build_command(cmd_type: type[CommandType],
                  chain: Message | None = None,
                  **kwargs) -> CommandComposer
```

Builds a new command.

**Arguments**:

- `cmd_type` - The command type (i.e., a subclass of ``Command``).
- `chain` - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
- `**kwargs` - Additional message parameters.
  

**Returns**:

  A message composer to further build and finally emit the message.
  

**Raises**:

- `RuntimeError` - ``cmd_type`` is not a subclass of ``Command``.

#### build\_command\_reply

```python
def build_command_reply(reply_type: type[CommandReplyType],
                        command: CommandType,
                        success: bool = True,
                        message: str = "",
                        **kwargs) -> CommandReplyComposer
```

Builds a new command reply.

**Arguments**:

- `reply_type` - The command reply type (i.e., a subclass of ``CommandReply``).
- `command` - The ``Command`` this reply is based on.
- `success` - Whether the command *succeeded* or not (how this is interpreted depends on the command).
- `message` - Additional message to include in the reply.
- `**kwargs` - Additional message parameters.
  

**Returns**:

  A message composer to further build and finally emit the message.
  

**Raises**:

- `RuntimeError` - ``reply_type`` is not a subclass of ``CommandReply``.

#### build\_event

```python
def build_event(event_type: type[Event],
                chain: Message | None = None,
                **kwargs) -> EventComposer
```

Builds a new event.

**Arguments**:

- `event_type` - The event type (i.e., a subclass of ``Event``).
- `chain` - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
- `**kwargs` - Additional message parameters.
  

**Returns**:

  A message composer to further build and finally emit the message.
  

**Raises**:

- `RuntimeError` - ``event_type`` is not a subclass of ``Event``.

#### get\_message\_count

```python
def get_message_count(msg_type: MessageType) -> int
```

Gets how many messages of specific message types have been created.

The message builder keeps track of how many messages of the three major types ``Command``, ``CommandReply`` and
``Event`` have been created.

**Arguments**:

- `msg_type` - The message type to get the count of. Must be either ``Command``, ``CommandReply`` or ``Event``.
  

**Returns**:

  The number of messages already built of the specified type.

