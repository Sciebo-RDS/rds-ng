---
sidebar_label: storage
title: data.storage.storage
---

#### EntityType

pylint: disable=invalid-name

#### EntityKeyType

pylint: disable=invalid-name

## Storage Objects

```python
class Storage(typing.Generic[EntityType, EntityKeyType], abc.ABC)
```

Defines a general storage interface for basic CRUD operations.

#### add

```python
@abc.abstractmethod
def add(entity: EntityType) -> None
```

Adds a new entity or updates an existing one.

**Raises**:

- `StorageException` - If the entity couldn&#x27;t be added.

#### remove

```python
@abc.abstractmethod
def remove(entity: EntityType) -> None
```

Removes an entity.

**Raises**:

- `StorageException` - If the entity couldn&#x27;t be removed.

#### get

```python
@abc.abstractmethod
def get(key: EntityKeyType) -> EntityType | None
```

Retrieves the entity identified by the given key.

**Returns**:

  The found entity, or ``None`` if no entity with the given key exists.
  

**Raises**:

- `StorageException` - If the entity couldn&#x27;t be fetched (not due to a missing key).

#### list

```python
@abc.abstractmethod
def list() -> typing.List[EntityType]
```

Retrieves all stored entities.

**Returns**:

  A list of all entitites.
  

**Raises**:

- `StorageException` - If the entities couldn&#x27;t be listed.

