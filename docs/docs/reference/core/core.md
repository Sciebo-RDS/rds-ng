---
sidebar_label: core
title: core.core
---

## Core Objects

```python
class Core()
```

The main *underlying basis* of any component.

The ``Core`` brings together all portions and aspects that build the underlying foundation of every component,
including the ``MessageBus``.

The core can be regarded as a facade to the *inner structure* of a component. It only offers a small number of public
methods and is accessed from the outside very rarely.

An instance of this class is always created when creating a ``Component``; it should never be instantiated otherwise.

#### \_\_init\_\_

```python
def __init__(module_name: str, comp_data: BackendComponentData)
```

**Arguments**:

- `module_name` - The module name used for *Flask* initialization.
- `comp_data` - The component data used to access common component information.

#### register\_service

```python
def register_service(svc: MessageService) -> None
```

Registers a message service.

Services are always created and registered using ``create_service`` (in ``Component``),
so you should rarely (if ever) need to call this method directly.

**Arguments**:

- `svc` - The message service to register.

#### unregister\_service

```python
def unregister_service(svc: MessageService) -> None
```

Removes a message service.

**Arguments**:

- `svc` - The message service to remove.

#### run

```python
def run() -> None
```

Starts periodic background tasks.

#### message\_bus

```python
@property
def message_bus() -> MessageBus
```

The global ``MessageBus`` instance.

#### flask

```python
@property
def flask() -> flask.Flask
```

The global ``Flask`` instance.

#### is\_debug\_mode

```python
@property
def is_debug_mode() -> bool
```

Whether we&#x27;re running in Debug mode.

