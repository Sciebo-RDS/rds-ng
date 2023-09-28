---
sidebar_label: backend_component_data
title: component.backend_component_data
---

## BackendComponentData Objects

```python
@dataclasses.dataclass(frozen=True, kw_only=True)
class BackendComponentData()
```

Holds general data and information about the component.

Objects of this class are passed to certain parts of the core for easy access to frequently
used component information and data, like its configuration or role.

**Attributes**:

- `comp_id` - The component identifier.
- `role` - The component role.
- `config` - The configuration.
- `title` - The component title.
- `name` - The component name.
- `version` - The component version.

