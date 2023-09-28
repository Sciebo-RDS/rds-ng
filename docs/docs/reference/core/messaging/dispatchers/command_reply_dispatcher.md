---
sidebar_label: command_reply_dispatcher
title: core.messaging.dispatchers.command_reply_dispatcher
---

## CommandReplyDispatcher Objects

```python
class CommandReplyDispatcher(MessageDispatcher[CommandReply])
```

Message dispatcher specific to ``CommandReply``.

#### pre\_dispatch

```python
def pre_dispatch(msg: CommandReply,
                 msg_meta: CommandReplyMetaInformation) -> None
```

Invokes reply callbacks associated with the replied command.

**Arguments**:

- `msg` - The command reply that is about to be dispatched.
- `msg_meta` - The command reply meta information.

