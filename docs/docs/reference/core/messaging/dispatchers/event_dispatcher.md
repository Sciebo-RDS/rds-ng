---
sidebar_label: event_dispatcher
title: core.messaging.dispatchers.event_dispatcher
---

## EventDispatcher Objects

```python
class EventDispatcher(MessageDispatcher[Event])
```

Message dispatcher specific to ``Event``.

#### pre\_dispatch

```python
def pre_dispatch(msg: Event, msg_meta: EventMetaInformation) -> None
```

Adds command meta information to a global list so that command replies can be handled properly.

**Arguments**:

- `msg` - The command that is about to be dispatched.
- `msg_meta` - The command meta information.

