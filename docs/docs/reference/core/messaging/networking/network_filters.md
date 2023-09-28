---
sidebar_label: network_filters
title: core.messaging.networking.network_filters
---

## NetworkFilters Objects

```python
class NetworkFilters()
```

A list of network filters.

#### install

```python
def install(fltr: NetworkFilter) -> None
```

Adds a new filter.

**Arguments**:

- `fltr` - The filter to add.

#### filter\_incoming\_message

```python
def filter_incoming_message(connection: NetworkFilter.ConnectionType,
                            msg: Message,
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
def filter_outgoing_message(connection: NetworkFilter.ConnectionType,
                            msg: Message,
                            msg_meta: MessageMetaInformation) -> bool
```

Filters outgoing messages.

**Arguments**:

- `connection` - The connection the message is sent through.
- `msg` - The outgoing message.
- `msg_meta` - The message meta information.
  

**Returns**:

  Whether the message should pass.

