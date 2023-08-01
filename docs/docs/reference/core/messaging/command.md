---
sidebar_label: command
title: core.messaging.command
---

## Command Objects

```python
@dataclass(frozen=True, kw_only=True)
class Command(Message)
```

A command message.

Commands are instructions that need to be *executed* by the receiving component.

**Notes**:

  Commands need to *always* be replied by emitting a corresponding ``CommandReply``.
  This reply is then automatically sent back to the original sender.
  

**Attributes**:

- `unique` - A unique identifier for each issued command.

#### CommandType

pylint: disable=invalid-name

