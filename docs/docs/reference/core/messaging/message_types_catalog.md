---
sidebar_label: message_types_catalog
title: core.messaging.message_types_catalog
---

## MessageTypesCatalog Objects

```python
class MessageTypesCatalog()
```

Global catalog of all registered message types.

This is a globally accessible list of all message types, associated with their respective message names.
It&#x27;s mainly used to create proper message objects from incoming network messages.

#### register\_type

```python
@staticmethod
def register_type(name: MessageName, msg_type: type[MessageType]) -> None
```

Registers a new message type.

**Arguments**:

- `name` - The message name.
- `msg_type` - The message type.

#### find\_type

```python
@staticmethod
def find_type(name: MessageName) -> type[MessageType] | None
```

Finds the message type associated with the given ``name``.

**Arguments**:

- `name` - The message name.
  

**Returns**:

  The associated message type, if any.

