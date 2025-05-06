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
def __init__(comp_id: UnitID, config: Configuration,
             message_builder: MessageBuilder)
```

**Arguments**:

- `comp_id` - The component identifier.
- `config` - The global configuration.
- `message_builder` - A message builder instance.

#### set\_message\_handler

```python
def set_message_handler(msg_handler: ClientMessageHandler) -> None
```

Sets a handler that gets called when a message arrives.

**Arguments**:

- `msg_handler` - The message handler to be called.

#### run

```python
def run() -> None
```

Automatically connects to a server if one was configured.

#### process

```python
def process() -> None
```

Periodically performs certain tasks.

#### connect\_to\_server

```python
def connect_to_server() -> None
```

Establishes the connection to the server.

#### send\_message

```python
def send_message(msg: Message) -> None
```

Sends a message to the server (if connected).

For this, the message will be encoded as *JSON* first.

**Arguments**:

- `msg` - The message to send.

