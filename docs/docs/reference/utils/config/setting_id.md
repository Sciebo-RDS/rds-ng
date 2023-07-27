---
sidebar_label: setting_id
title: utils.config.setting_id
---

## SettingID Objects

```python
@dataclasses.dataclass(frozen=True)
class SettingID()
```

A setting identifier.

Settings are specified by a category they belong to, as well as their actual name.

Categories support sub-categories by separating them using dots (.);
when represented as a string, all component tokens are separated by dots.

**Attributes**:

- `category` - The category name. Sub-categories can be separated by dots (.).
- `name` - The name of the setting.

#### split

```python
def split() -> typing.List[str]
```

Splits the entire identifier into single string tokens.

**Returns**:

  The tokens list.

#### env\_name

```python
def env_name(prefix: str) -> str
```

Generates an environment variable name for this identifier.

A setting identifier is translated to its corresponding environment variable name by replacing all dots (.) with underscores (_),
prepending a ``prefix``, as well as making everything uppercase.

**Arguments**:

- `prefix` - The prefix to prepend.
  

**Returns**:

  The corresponding environment variable name.

