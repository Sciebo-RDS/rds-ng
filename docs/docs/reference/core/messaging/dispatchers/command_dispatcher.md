---
sidebar_label: command_dispatcher
title: core.messaging.dispatchers.command_dispatcher
---

## CommandDispatcher Objects

```python
class CommandDispatcher(MessageDispatcher[Command])
```

Message dispatcher specific to ``Command``.

#### process

```python
def process() -> None
```

Takes care of checking whether issued commands have already timed out.

#### pre\_dispatch

```python
def pre_dispatch(msg: Command, msg_meta: CommandMetaInformation) -> None
```

Adds command meta information to a global list so that command replies can be handled properly.

**Arguments**:

- `msg` - The command that is about to be dispatched.
- `msg_meta` - The command meta information.

#### dispatch

```python
def dispatch(msg: Command, msg_meta: CommandMetaInformation,
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

#### invoke\_reply\_callback

```python
@staticmethod
def invoke_reply_callback(
        unique: Trace,
        *,
        reply: CommandReply | None = None,
        fail_type: CommandReply.FailType = CommandReply.FailType.NONE,
        fail_msg: str = "") -> None
```

Invokes command reply handlers.

When emitting a command, it is possible to specify reply callbacks that are invoked beside message handlers. This method will call the correct
callback and take care of intercepting exceptions.

**Arguments**:

- `unique` - The unique trace of the command.
- `reply` - The received command reply (if any).
- `fail_type` - The type of the command failure (in case of a timeout or exception).
- `fail_msg` - The failure message.

