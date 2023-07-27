---
sidebar_label: component_role
title: component.roles.component_role
---

## ComponentRole Objects

```python
class ComponentRole(abc.ABC)
```

The role definition of a component.

A component role defines certain aspects of a component. This usually corresponds to having specific features
enabled or overriding types that are used within the core.

## RuntimeAspects Objects

```python
@dataclasses.dataclass(frozen=True, kw_only=True)
class RuntimeAspects()
```

Runtime aspects of a role.

**Attributes**:

- `runtime_app_type` - The runtime (WSGI) application type to instantiate.

## NetworkingAspects Objects

```python
@dataclasses.dataclass(frozen=True, kw_only=True)
class NetworkingAspects()
```

Networking aspects of a role.

**Attributes**:

- `has_server` - Whether this role runs a server in the networking engine.
- `has_client` - Whether this role runs a client in the networking engine.

#### \_\_init\_\_

```python
def __init__(role_name: str, *, runtime_aspects: RuntimeAspects,
             networking_aspects: NetworkingAspects)
```

**Arguments**:

- `role_name` - The name of the role.
- `networking_aspects` - The networking aspects to use.

#### name

```python
@property
def name() -> str
```

The name of the role.

#### runtime\_aspects

```python
@property
def runtime_aspects() -> RuntimeAspects
```

The runtime aspects of this role.

#### networking\_aspects

```python
@property
def networking_aspects() -> NetworkingAspects
```

The networking aspects of the role.

