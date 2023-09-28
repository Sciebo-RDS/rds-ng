---
sidebar_label: service
title: services.service
---

## Service Objects

```python
@typing.final
class Service(MessageService)
```

Base service class providing easy message handler mapping.

A service can be seen as the bridge between the inner workings of a component (represented by a ``Core``) and the
outside component domain.

Services register the various message handlers that are called when a certain message is received by the message bus and
dispatched locally. They also create instances of ``ServiceContext`` (or a subclass) that represent a single *unit of work*
when executing a message handler.

Message handlers are defined using the ``message_handler`` decorator, as can be seen in this example (``svc`` being a ``Service`` instance)::

    @svc.message_handler(&quot;msg/event&quot;, Event)
    def h(msg: Event, ctx: ServiceContext) -&gt; None:
        ctx.logger.info(f&quot;EVENT HANDLER CALLED&quot;)

#### \_\_init\_\_

```python
def __init__(comp_id: UnitID,
             name: str,
             *,
             message_bus: MessageBusProtocol,
             context_type: type[ServiceContextType] = ServiceContext)
```

**Arguments**:

- `comp_id` - The global component identifier.
- `name` - The service name.
- `message_bus` - The global message bus.
- `context_type` - The type to use when creating a service context.

#### message\_handler

```python
def message_handler(
    message_type: type[MessageType] = Message,
    *,
    name_filter: str = "",
    is_async: bool = False
) -> typing.Callable[[MessageHandler], MessageHandler]
```

A decorator to declare a message handler.

To define a new message handler, use the following pattern::

@svc.message_handler(&quot;msg/event&quot;, Event)
def h(msg: Event, ctx: ServiceContext) -&gt; None:
ctx.logger.info(f&quot;EVENT HANDLER CALLED&quot;)

**Arguments**:

- `message_type` - The type of the message.
- `name_filter` - A more generic message name filter to match against; wildcards (*) are supported as well.
- `is_async` - Whether to execute the handler asynchronously in its own thread.

#### name

```python
@property
def name() -> str
```

The name of this service.

#### message\_builder

```python
@property
def message_builder() -> MessageBuilder
```

The service&#x27;s message builder.

