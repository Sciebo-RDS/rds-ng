---
sidebar_label: event_dispatcher
title: core.messaging.dispatchers.event_dispatcher
---

## EventDispatcher Objects

```python
class EventDispatcher(MessageDispatcher[Event])
```

Message dispatcher specific to ``Event``.

#### dispatch

```python
def dispatch(msg: Event, msg_meta: EventMetaInformation,
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

