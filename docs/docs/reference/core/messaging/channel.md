---
sidebar_label: channel
title: core.messaging.channel
---

## Channel Objects

```python
@dataclass(frozen=True)
class Channel()
```

The target of a message.

Message targets are represented by so-called *channels*. These can be *local* for messages that will only
be dispatched locally and not across the network, *direct* for specific (remote) targets, as well as general
*rooms* consisting of arbitrary participants (this is still WIP and may even be removed later).

**Attributes**:

- `type` - The channel type.
- `target` - The actual target (either a direct one or a room).

## Type Objects

```python
class Type(StrEnum)
```

The different channel types.

#### target\_id

```python
@property
def target_id() -> UnitID | None
```

Generates a ``UnitID`` from the target of this channel.

**Returns**:

  The component ID of the target, if any.

#### is\_local

```python
@property
def is_local() -> bool
```

Whether this is a local channel.

#### is\_direct

```python
@property
def is_direct() -> bool
```

Whether this is a direct channel.

#### is\_room

```python
@property
def is_room() -> bool
```

Whether this is a room channel.

#### local

```python
@staticmethod
def local() -> 'Channel'
```

Creates a new local channel.

#### direct

```python
@staticmethod
def direct(target: str) -> 'Channel'
```

Creates a new direct channel.

#### room

```python
@staticmethod
def room(target: str) -> 'Channel'
```

Creates a new room channel.

