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

#### dispatch

```python
def dispatch(msg: CommandReply, msg_meta: CommandReplyMetaInformation,
             handler: MessageHandlerMapping, ctx: MessageContextType) -> None
```

Dispatches a message to locally registered message handlers.

Handlers can be either called synchronously or asynchronously, depending on how the handler was registered.

**Notes**:

  Exceptions arising within a message handler will not interrupt the running program; instead, such errors will only be logged.
  

**Arguments**:

- `msg` - The message to be dispatched.
- `msg_meta` - The message meta information.
- `handler` - The handler to be invoked.
- `ctx` - The message context.
  

**Raises**:

- `RuntimeError` - If the handler requires a different message type.

