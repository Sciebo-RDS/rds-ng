---
sidebar_label: message_dispatcher
title: core.messaging.dispatchers.message_dispatcher
---

## MessageDispatcher Objects

```python
class MessageDispatcher(abc.ABC, typing.Generic[MessageType])
```

Base message dispatcher responsible for sending messages to registered handlers.

Dispatching a message (locally) is done by passing the message to one or more registered message handlers within a ``Service``.
The message dispatcher also performs pre- and post-dispatching tasks and takes care of catching errors raised in a handler.

#### \_\_init\_\_

```python
def __init__(meta_information_type: type[MessageMetaInformationType])
```

**Arguments**:

- `meta_information_type` - The required type of the message meta information passed alongside the actual messages.

#### process

```python
def process() -> None
```

Called to perform periodic tasks.

#### pre\_dispatch

```python
def pre_dispatch(msg: MessageType,
                 msg_meta: MessageMetaInformationType) -> None
```

Called to perform tasks *before* sending a message.

This method is called before any service-registered message handler is invoked.

**Arguments**:

- `msg` - The message that is about to be dispatched.
- `msg_meta` - The message meta information.
  

**Raises**:

- `RuntimeError` - If the meta information type is invalid.

#### dispatch

```python
def dispatch(msg: MessageType, msg_meta: MessageMetaInformationType,
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

#### post\_dispatch

```python
def post_dispatch(msg: MessageType,
                  msg_meta: MessageMetaInformationType) -> None
```

Called to perform tasks *after* sending a message.

This method is called after any service-registered message handler have been invoked.

**Arguments**:

- `msg` - The message that has just been dispatched.
- `msg_meta` - The message meta information.

