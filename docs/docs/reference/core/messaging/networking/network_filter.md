---
sidebar_label: network_filter
title: core.messaging.networking.network_filter
---

## NetworkFilter Objects

```python
class NetworkFilter()
```

Filters incoming and outgoing network messages.

## ConnectionType Objects

```python
class ConnectionType(IntEnum)
```

The affected connection type (client or server).

#### filter\_incoming\_message

```python
def filter_incoming_message(connection: ConnectionType, msg: Message,
                            msg_meta: MessageMetaInformation) -> bool
```

Filters incoming messages.

**Arguments**:

- `connection` - The connection the message came through.
- `msg` - The incoming message.
- `msg_meta` - The message meta information.
  

**Returns**:

  Whether the message should be filtered out.

#### filter\_outgoing\_message

```python
def filter_outgoing_message(connection: ConnectionType, msg: Message,
                            msg_meta: MessageMetaInformation) -> bool
```

Filters outgoing messages.

**Arguments**:

- `connection` - The connection the message is sent through.
- `msg` - The outgoing message.
- `msg_meta` - The message meta information.
  

**Returns**:

  Whether the message should be filtered out.

