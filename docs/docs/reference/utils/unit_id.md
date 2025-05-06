---
sidebar_label: unit_id
title: utils.unit_id
---

## UnitID Objects

```python
@dataclass_json

@dataclass(frozen=True)
class UnitID()
```

A general unit identifier.

A *unit* basically is something that has a unique identifier consisting of three parts: The general ``type`` (e.g., *&#x27;infra&#x27;* for components
belonging to the overall infrastructure), the ``unit`` name itself (e.g., *&#x27;gate&#x27;* or *&#x27;server&#x27;*), and an ``instance`` specifier (used to
distinguish multiple instances of the same unit).

**Attributes**:

- `type` - The unit type.
- `unit` - The unit name.
- `instance` - The instance specifier.

#### equals

```python
def equals(other: typing.Self) -> bool
```

Compares this identifier to another one.

**Arguments**:

- `other` - The unit identifier to compare this one to.
  

**Notes**:

  The ``instance`` specifiers are only compared if both are not ``None``.
  

**Returns**:

  Whether both identifiers are equal.

#### from\_string

```python
@staticmethod
def from_string(id_str: str) -> 'UnitID'
```

Creates a new ``UnitID`` from a string.

The string must be of the form ``&lt;type&gt;/&lt;unit&gt;/&lt;instance&gt;`` or ``&lt;type&gt;/&lt;unit&gt;``.

**Arguments**:

- `id_str` - The unit identifier string.
  

**Returns**:

  The newly created ``UnitID``.
  

**Raises**:

- `ValueError` - If the passed string is invalid.

