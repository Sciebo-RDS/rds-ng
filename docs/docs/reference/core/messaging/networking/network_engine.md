---
sidebar_label: network_engine
title: core.messaging.networking.network_engine
---

## NetworkEngine Objects

```python
class NetworkEngine()
```

Main network management class.

Messages go out to other components through this class, and new messages come in from the outside world here as well.
The network engine takes care of listening to incoming messages, routing them properly, and sending new messages to other components.

#### \_\_init\_\_

```python
def __init__(comp_data: BackendComponentData, message_bus: MessageBusProtocol)
```

**Arguments**:

- `comp_data` - The global component data.
- `message_bus` - The global message bus.

#### run

```python
def run() -> None
```

Listens to incoming messages in order to properly route them.

#### process

```python
def process() -> None
```

Called to perform periodic tasks.

#### send\_message

```python
def send_message(msg: Message, msg_meta: MessageMetaInformation) -> None
```

Sends a message across the network.

To do so, the message is first checked for validity (whether it actually *may* be sent). If it is valid, it is routed through the
client and/or server (the logic of this can be found in ``NetworkRouter``).

**Arguments**:

- `msg` - The message to be sent.
- `msg_meta` - The message meta information.

#### install\_filter

```python
def install_filter(fltr: NetworkFilter) -> None
```

Installs a new network message filter.

**Arguments**:

- `fltr` - The filter to add.

#### has\_server

```python
@property
def has_server() -> bool
```

Whether the network runs a server.

#### server

```python
@property
def server() -> Server | None
```

The server instance.

#### has\_client

```python
@property
def has_client() -> bool
```

Whether the network runs a client.

#### client

```python
@property
def client() -> Client | None
```

The client instance.

