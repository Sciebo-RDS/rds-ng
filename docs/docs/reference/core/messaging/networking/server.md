---
sidebar_label: server
title: core.messaging.networking.server
---

## Server Objects

```python
class Server(socketio.Server)
```

The server connection, based on ``socketio.Server``.

## SendTarget Objects

```python
class SendTarget(IntEnum)
```

Enum telling whether an outgoing message is only sent to a single (direct) target or spread across all connected clients.

## \_ComponentEntry Objects

```python
@dataclasses.dataclass()
class _ComponentEntry()
```

#### has\_timed\_out

```python
def has_timed_out() -> bool
```

Whether the connected component has timed out.

#### \_\_init\_\_

```python
def __init__(comp_id: UnitID, config: Configuration,
             message_builder: MessageBuilder)
```

**Arguments**:

- `comp_id` - The component identifier.
- `config` - The global configuration.
- `message_builder` - A message builder to use.

#### set\_message\_handler

```python
def set_message_handler(msg_handler: ServerMessageHandler) -> None
```

Sets a handler that gets called when a message arrives.

**Arguments**:

- `msg_handler` - The message handler to be called.

#### run

```python
def run() -> None
```

So far, does exactly nothing.

#### process

```python
def process() -> None
```

Periodically purges timed out clients.

#### send\_message

```python
def send_message(
        msg: Message,
        *,
        skip_components: typing.List[UnitID] | None = None) -> SendTarget
```

Sends a message to one or more clients.

For this, the message will be encoded as *JSON* first.

**Arguments**:

- `msg` - The message to send.
- `skip_components` - A list of components (clients) to be excluded from the targets.

