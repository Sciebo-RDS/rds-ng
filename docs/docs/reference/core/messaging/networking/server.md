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

Flag telling whether an outgoing message is only sent to a single (direct) target or spread across all connected clients.

#### \_\_init\_\_

```python
def __init__(comp_id: UnitID, config: Configuration)
```

**Arguments**:

- `comp_id` - The component identifier.
- `config` - The global configuration.

#### run

```python
def run() -> None
```

So far, does exactly nothing.

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

