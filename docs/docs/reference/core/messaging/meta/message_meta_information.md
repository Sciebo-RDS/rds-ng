---
sidebar_label: message_meta_information
title: core.messaging.meta.message_meta_information
---

## MessageMetaInformation Objects

```python
@dataclasses.dataclass(frozen=True, kw_only=True)
class MessageMetaInformation()
```

Stores additional information necessary for message dispatching.

When a message is emitted, additional information is required to be able to properly handle it.
This includes its entrypoint into the system, as well as whether the message type requires a reply.

**Attributes**:

- `entrypoint` - From where the message entered the system (locally or remotely).
- `requires_reply` - Whether a reply is expected.

## Entrypoint Objects

```python
class Entrypoint(IntEnum)
```

Defines from where a message has entered the system.

#### MessageMetaInformationType

pylint: disable=invalid-name

