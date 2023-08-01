---
sidebar_label: component
title: component.component
---

## Component Objects

```python
class Component()
```

Base class for all project components.

Components are always based on this class. It mainly maintains an instance of the ``Core``, but also stores general information
about the component itself and the entire project.

When writing a component, always create a new subclass that extends ``Component``. Pass all the necessary information to its
constructor (see ``Args``) and, after doing further setup steps, call its ``run`` method.

#### \_\_init\_\_

```python
def __init__(comp_id: UnitID,
             role: ComponentRole,
             *,
             module_name: str,
             config_file: str = "./config.toml")
```

**Arguments**:

- `comp_id` - The identifier of this component.
- `role` - The role of this component.
- `module_name` - The component module name; simply pass ``__name__`` here.
- `config_file` - The configuration file to load.

#### app

```python
def app() -> typing.Any
```

Creates a WSGI application object that can be used to be run by a gateway service.

**Returns**:

  The WSGI application object.

#### run

```python
def run() -> None
```

Starts the component&#x27;s execution cycles.

**Notes**:

  It is mandatory to call this method after creating and setting up a component.

#### create\_service

```python
def create_service(
        name: str,
        *,
        context_type: type[ServiceContextType] = ServiceContext) -> Service
```

Creates and registers a new service.

**Arguments**:

- `name` - The name of the service.
- `context_type` - Can be used to override the default ``ServiceContext`` type. All message handlers
  associated with the new service will then receive instances of this type for their service context.
  

**Returns**:

  The newly created service.

#### config

```python
@property
def config() -> Configuration
```

The configuration used by the component.

#### data

```python
@property
def data() -> ComponentData
```

A data helper object that stores useful component data and information.
