---
sidebar_label: message_bus
title: core.messaging.message_bus
---

## MessageBus Objects

```python
class MessageBus()
```

Bus for dispatching messages.

The message bus is probably the most central aspect of the system as a whole. It not only invokes local message handlers (which are basically
callback functions), it also sends messages across the network to other components if necessary. The message bus on the remote side will then
decide what to do with the incoming message: Dispatch it locally there, send it to yet another component, or just ignore it.

Message handlers are always registered through a ``MessageService``. When a message gets dispatched locally by the bus, it will call any handlers
associated with the message (via its name). If a message needs to be sent to another component, the bus will invoke the ``NetworkEngine`` to do
so.

To be error tolerant, any exceptions that arise during message handling will be logged but won&#x27;t result in program termination.

**Notes**:

  The message bus is thread-safe.

#### \_\_init\_\_

```python
def __init__(comp_data: BackendComponentData)
```

**Arguments**:

- `comp_data` - The global component data.

#### add\_service

```python
def add_service(svc: MessageService) -> bool
```

Adds a new message service to the bus.

**Arguments**:

- `svc` - The message service to add.
  

**Returns**:

  Whether the message service was added.

#### remove\_service

```python
def remove_service(svc: MessageService) -> bool
```

Removes a message service from the bus.

**Arguments**:

- `svc` - The message service to remove.
  

**Returns**:

  Whether the message service was removed.

#### run

```python
def run() -> None
```

Initiates periodic tasks performed by the bus.

#### dispatch

```python
def dispatch(msg: Message, msg_meta: MessageMetaInformationType) -> None
```

Dispatches a message.

To do so, the message is first checked for validity (whether it actually *may* be dispatched). If it is valid,
the ``MessageRouter`` will determine if it needs to be dispatched to another component or locally (or both).

**Arguments**:

- `msg` - The message to be dispatched.
- `msg_meta` - The message meta information.

#### network

```python
@property
def network() -> NetworkEngine
```

The network engine instance.

