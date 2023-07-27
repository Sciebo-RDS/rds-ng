---
sidebar_label: client
title: core.messaging.networking.client
---

## Client Objects

```python
class Client(socketio.Client)
```

The client connection, based on ``socketio.Client``.

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

Automatically connects to a server if one was configured.

#### send\_message

```python
def send_message(msg: Message) -> None
```

Sends a message to the server (if connected).

For this, the message will be encoded as *JSON* first.

**Arguments**:

- `msg` - The message to send.

