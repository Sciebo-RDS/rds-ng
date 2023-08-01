---
sidebar_label: service_context
title: service.service_context
---

## ServiceContext Objects

```python
class ServiceContext(MessageContext)
```

An execution context for messages dispatched by the message bus to a service.

This class is an extension to the more general ``MessageContext`` specifically used by ``Service`` and its message handlers.

#### \_\_init\_\_

```python
def __init__(msg_emitter: MessageEmitter, config: Configuration,
             logger: LoggerProtocol)
```

**Arguments**:

- `msg_emitter` - A ``MessageEmitter`` to be assigned to this context.
- `config` - The global component configuration.
- `logger` - A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.

#### config

```python
@property
def config() -> Configuration
```

The global component configuration.

#### ServiceContextType

pylint: disable=invalid-name

