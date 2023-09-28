---
sidebar_label: message_router
title: core.messaging.message_router
---

## MessageRouter Objects

```python
class MessageRouter()
```

Message routing rules and logic.

When a message enters the message bus, it is first checked for its validity.
Afterwards, the router decides through which channels (local, remote) it needs to be sent.

## RoutingError Objects

```python
class RoutingError(RuntimeError)
```

Represents errors during routing validation.

#### \_\_init\_\_

```python
def __init__(comp_id: UnitID)
```

**Arguments**:

- `comp_id` - The component id (required to decide whether we match a given direct target).

#### verify\_message

```python
def verify_message(msg: Message, msg_meta: MessageMetaInformation) -> None
```

Verifies whether a message may enter the message bus.

**Arguments**:

- `msg` - The message that wants to enter the network engine.
- `msg_meta` - The message meta information.
  

**Raises**:

- `RoutingError` - In case the message is not valid to enter the message bus.

#### check\_local\_routing

```python
def check_local_routing(msg: Message,
                        msg_meta: MessageMetaInformation) -> bool
```

Checks if the message should be routed locally.

**Arguments**:

- `msg` - The message.
- `msg_meta` - The message meta information.
  

**Returns**:

  Whether local routing should happen.

#### check\_remote\_routing

```python
def check_remote_routing(msg: Message,
                         msg_meta: MessageMetaInformation) -> bool
```

Checks if the message should be routed remotely.

**Arguments**:

- `msg` - The message.
- `msg_meta` - The message meta information.
  

**Returns**:

  Whether remote routing should happen.

