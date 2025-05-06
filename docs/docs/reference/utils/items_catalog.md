---
sidebar_label: items_catalog
title: utils.items_catalog
---

#### ItemType

pylint: disable=invalid-name

## ItemsCatalog Objects

```python
class ItemsCatalog(typing.Generic[ItemType])
```

Generic catalog to keep track of &quot;registered&quot; items (where the definition of &quot;item&quot; is completely context dependant).

This is a globally accessible list of these items, associated with their respective names.

#### define

```python
@staticmethod
def define()
```

A decorator to define a new item catalog.

**Notes**:

  This decorator must always be used for new item catalogs; otherwise, data corruption might occur.

#### register\_item

```python
@classmethod
def register_item(cls, name: str, item: ItemType) -> None
```

Registers a new item.

**Arguments**:

- `name` - The item name.
- `item` - The item.

#### find\_item

```python
@classmethod
def find_item(cls, name: str) -> ItemType | None
```

Finds the item associated with the given ``name``.

**Arguments**:

- `name` - The item name.
  

**Returns**:

  The associated item, if any.

#### items

```python
@classmethod
def items(cls) -> typing.Tuple[str, ItemType]
```

Generator to iterate over all registered items.

**Returns**:

  Tuple consisting of the item name and the item itself.

