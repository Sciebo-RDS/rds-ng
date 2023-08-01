---
sidebar_label: message_meta_information_list
title: core.messaging.meta.message_meta_information_list
---

## MessageMetaInformationList Objects

```python
class MessageMetaInformationList()
```

List to store message meta information objects.

**Notes**:

  The list is thread-safe.

## \_Entry Objects

```python
@dataclasses.dataclass(frozen=True)
class _Entry()
```

#### has\_timed\_out

```python
def has_timed_out() -> bool
```

Whether the message has timed out.

#### add

```python
def add(unique: Trace, meta: MessageMetaInformation, timeout: float) -> None
```

Adds a new entry to the list.

**Arguments**:

- `unique` - The unique trace identifying the message.
- `meta` - The message meta information.
- `timeout` - A timeout (in seconds) after which a message is deemed timed out.

#### remove

```python
def remove(unique: Trace) -> None
```

Removes an entry from the list.

**Arguments**:

- `unique` - The unique trace identifying the message.

#### find

```python
def find(unique: Trace) -> MessageMetaInformation | None
```

Finds an entry associated with the given ``unique``.

**Arguments**:

- `unique` - The unique trace identifying the message.
  

**Returns**:

  The found meta information, if any.

#### find\_timed\_out\_entries

```python
def find_timed_out_entries() -> typing.List[Trace]
```

Finds all entries that have timed out already.

**Returns**:

  A list of all timed out entries.

