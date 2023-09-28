---
sidebar_label: message_types_catalog
title: core.messaging.message_types_catalog
---

## MessageTypesCatalog Objects

```python
@ItemsCatalog.define()
class MessageTypesCatalog(ItemsCatalog[type[MessageType]])
```

Global catalog of all registered message types.

This is a globally accessible list of all message types, associated with their respective message names.
It&#x27;s mainly used to create proper message objects from incoming network messages.

