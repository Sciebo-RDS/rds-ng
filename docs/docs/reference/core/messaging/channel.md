---
sidebar_label: channel
title: core.messaging.channel
---

## Channel Objects

```python
@dataclass_json

@dataclass(frozen=True)
class Channel()
```

The target of a message.

Message targets are represented by so-called *channels*. These can be *local* for messages that will only
be dispatched locally and not across the network or *direct* for specific (remote) targets.

**Attributes**:

- `type` - The channel type.
- `target` - The actual target in case of a direct channel.

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

#### local

```python
@staticmethod
def local() -> "Channel"
```

Creates a new local channel.

#### direct

```python
@staticmethod
def direct(target: str | UnitID) -> "Channel"
```

Creates a new direct channel.

