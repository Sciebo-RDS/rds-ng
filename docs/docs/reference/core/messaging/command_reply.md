---
sidebar_label: command_reply
title: core.messaging.command_reply
---

## CommandReply Objects

```python
@dataclass(frozen=True, kw_only=True)
class CommandReply(Message)
```

A command reply message.

Every command needs to receive a reply in the form of a ``CommandReply`` message. The reply contains
information about its ``success``, as well as a text message which is usually used to describe reasons for
failures.

**Attributes**:

- `success` - Whether the command succeeded.
- `message` - Arbitrary text, usually used to describe reasons for failures.
- `unique` - The unique identifier of its corresponding command.

## FailType Objects

```python
class FailType(IntEnum)
```

Used when a command failed.

#### CommandReplyType

pylint: disable=invalid-name

