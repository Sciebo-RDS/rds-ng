---
sidebar_label: network_events
title: api.network_events
---

## ClientConnectedEvent Objects

```python
@Message.define("event/network/client-connected")
class ClientConnectedEvent(Event)
```

Emitted whenever the ``Client`` established a connection to the server.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          *,
          chain: Message | None = None) -> EventComposer
```

Helper function to easily build this message.

## ClientDisconnectedEvent Objects

```python
@Message.define("event/network/client-disconnected")
class ClientDisconnectedEvent(Event)
```

Emitted whenever the ``Client`` cuts its connection from the server.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          *,
          chain: Message | None = None) -> EventComposer
```

Helper function to easily build this message.

## ClientConnectionErrorEvent Objects

```python
@Message.define("event/network/client-connection-error")
class ClientConnectionErrorEvent(Event)
```

Emitted whenever the ``Client`` is unable to establish a connection.

**Attributes**:

- `reason` - The connection error reason.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          *,
          reason: str,
          chain: Message | None = None) -> EventComposer
```

Helper function to easily build this message.

## ServerConnectedEvent Objects

```python
@Message.define("event/network/server-connected")
class ServerConnectedEvent(Event)
```

Emitted whenever the ``Server`` established a connection to a client.

**Attributes**:

- `client_id` - The internal client ID.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          *,
          comp_id: UnitID,
          client_id: str,
          chain: Message | None = None) -> EventComposer
```

Helper function to easily build this message.

## ServerDisconnectedEvent Objects

```python
@Message.define("event/network/server-disconnected")
class ServerDisconnectedEvent(Event)
```

Emitted whenever the ``Server`` cuts a connection from a client.

**Attributes**:

- `client_id` - The internal client ID.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          *,
          comp_id: UnitID,
          client_id: str,
          chain: Message | None = None) -> EventComposer
```

Helper function to easily build this message.

