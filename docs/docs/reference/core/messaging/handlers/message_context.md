---
sidebar_label: message_context
title: core.messaging.handlers.message_context
---

## MessageContext Objects

```python
class MessageContext()
```

An execution context for messages dispatched by the message bus.

When a message handler gets executed (i.e., called by the message bus dispatchers), an instance of ``MessageContext`` (or a subclass)
is passed to the handler. This context can be seen as a *unit of work* that exists during the execution of the handler. Its main task is to
hold data that is specific to this single execution.

A message context is used as a context manager. In its ``__exit__`` method, any exceptions will be catched, printed and passed on. This
makes tracing of errors that occur during message handling easier.

It is also possible to have message handlers receive custom subtypes of this class. See ``Component`` and its ``create_service`` method for
details.

#### \_\_init\_\_

```python
def __init__(msg_meta: MessageMetaInformation, msg_builder: MessageBuilder, *,
             logger: LoggerProtocol, config: Configuration)
```

**Arguments**:

- `msg_builder` - A ``MessageBuilder`` to be assigned to this context.
- `msg_meta` - The meta information of the message.
- `logger` - A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
- `config` - The global component configuration.

#### is\_entrypoint\_local

```python
@property
def is_entrypoint_local() -> bool
```

Whether the message entered locally.

#### is\_entrypoint\_server

```python
@property
def is_entrypoint_server() -> bool
```

Whether the message entered through the server.

#### is\_entrypoint\_client

```python
@property
def is_entrypoint_client() -> bool
```

Whether the message entered through the client.

#### message\_builder

```python
@property
def message_builder() -> MessageBuilder
```

The message builder to be used within this context.

#### logger

```python
@property
def logger() -> LoggerProtocol
```

The logger to be used within this context.

#### config

```python
@property
def config() -> Configuration
```

The global component configuration.

