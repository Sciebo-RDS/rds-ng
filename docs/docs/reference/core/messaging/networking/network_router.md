---
sidebar_label: network_router
title: core.messaging.networking.network_router
---

## NetworkRouter Objects

```python
class NetworkRouter()
```

Network routing rules and logic.

When a message enters the network engine in order to be sent to remote targets, it is first checked for its
validity. Afterwards, the router decides through which channels (local, client, server) it needs to be sent.

## Direction Objects

```python
class Direction(IntEnum)
```

Enum telling the direction (INcoming or OUTgoing) of a message.

## RoutingError Objects

```python
class RoutingError(RuntimeError)
```

Represents errors during routing validation.

#### \_\_init\_\_

```python
def __init__(comp_id: UnitID, *, has_client: bool, has_server: bool)
```

**Arguments**:

- `comp_id` - The component id (required to decide whether we match a given direct target).
- `has_client` - Whether the network has a client instance.
- `has_server` - Whether the network has a server instance.

#### verify\_message

```python
def verify_message(direction: Direction, msg: Message) -> None
```

Verifies whether a message may enter the network engine.

**Arguments**:

- `direction` - The direction (*IN* or *OUT*) of the message.
- `msg` - The message that wants to enter the network engine.
  

**Raises**:

- `RoutingError` - In case the message is not valid to enter the network engine.

#### check\_local\_routing

```python
def check_local_routing(direction: Direction, msg: Message,
                        msg_meta: MessageMetaInformation) -> bool
```

Checks if the message should be routed locally (dispatched via the message bus).

**Arguments**:

- `direction` - The direction (*IN* or *OUT*) of the message.
- `msg` - The actual message.
- `msg_meta` - The message meta information.
  

**Returns**:

  Whether local routing should happen.

#### check\_client\_routing

```python
def check_client_routing(direction: Direction, msg: Message,
                         msg_meta: MessageMetaInformation) -> bool
```

Checks if the message should be routed through the client.

**Arguments**:

- `direction` - The direction (*IN* or *OUT*) of the message.
- `msg` - The actual message.
- `msg_meta` - The message meta information.
  

**Returns**:

  Whether client routing should happen.

#### check\_server\_routing

```python
def check_server_routing(direction: Direction, msg: Message,
                         msg_meta: MessageMetaInformation) -> bool
```

Checks if the message should be routed through the server.

**Arguments**:

- `direction` - The direction (*IN* or *OUT*) of the message.
- `msg` - The actual message.
- `msg_meta` - The message meta information.
  

**Returns**:

  Whether server routing should happen.

