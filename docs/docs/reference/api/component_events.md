---
sidebar_label: component_events
title: api.component_events
---

## ComponentInformation Objects

```python
@dataclasses.dataclass(frozen=True, kw_only=True)
class ComponentInformation()
```

Component information as an object.

## ComponentInformationEvent Objects

```python
@Message.define("event/component/information")
class ComponentInformationEvent(Event)
```

Contains information about a connected component; this is automatically sent whenever a connection is established (bilaterally).

**Attributes**:

- `comp_id` - The component ID.
- `comp_name` - The component name.
- `comp_version` - The component version.
- `api_protocol` - The API protocol version.

#### component\_information

```python
def component_information() -> ComponentInformation
```

The component information bundled as an object.

**Returns**:

  The component information stored in a ``ComponentInformation`` object.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          *,
          comp_id: UnitID,
          comp_name: str,
          comp_version: str,
          chain: Message | None = None) -> EventComposer
```

Helper function to easily build this message.

