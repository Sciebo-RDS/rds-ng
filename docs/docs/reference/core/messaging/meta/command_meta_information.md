---
sidebar_label: command_meta_information
title: core.messaging.meta.command_meta_information
---

## CommandMetaInformation Objects

```python
@dataclasses.dataclass(frozen=True, kw_only=True)
class CommandMetaInformation(MessageMetaInformation)
```

Message meta information specific to ``Command``.

**Attributes**:

- `requires_reply` - Commands always require a reply.
- `done_callbacks` - Called when a reply was received for this command.
- `fail_callbacks` - Called when no reply was received for this command or an exception occurred.
- `async_callbacks` - Whether the callbacks should be invoked asynchronously in their own thread.
- `timeout` - The timeout (in seconds) before a command is deemed not replied.

