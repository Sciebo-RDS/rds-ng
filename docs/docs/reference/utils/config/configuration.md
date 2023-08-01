---
sidebar_label: configuration
title: utils.config.configuration
---

## Configuration Objects

```python
class Configuration()
```

Encapsulates configuration settings and their fallback default values.

Settings can be loaded from a configuration file (in *TOML* format) or provided as environment variables (see below).

All settings are accessed by an identifier of type ``SettingID``, which represents settings in a path-like format;
``General.Debug``, for example, refers to a setting called ``Debug`` in the ``General` section.

A corresponding configuration file would look like this::

[General]
Debug = True

A setting identifier is translated to its corresponding environment variable name by replacing all dots (.) with underscores (_),
prepending a prefix (defaults to *&#x27;RDS&#x27;*), as well as making everything uppercase::

General.Debug -&gt; RDS_GENERAL_DEBUG

**Notes**:

  When accessing a setting value, a default value must *always* be present. This means that before a setting can be accessed,
  a default value must be added using ``add_defaults``.

#### \_\_init\_\_

```python
def __init__(env_prefix: str = "RDS")
```

**Arguments**:

- `env_prefix` - The prefix to use when generating the environment variable name of a setting.

#### load

```python
def load(filename: str) -> None
```

Loads settings from a *TOML* file.

**Arguments**:

- `filename` - The file to load.
  

**Raises**:

- `FileNotFoundError` - If the specified file doesn&#x27;t exist or couldn&#x27;t be opened.

#### add\_defaults

```python
def add_defaults(defaults: typing.Dict[SettingID, typing.Any]) -> None
```

Adds default values for settings, merging the new defaults into the existing ones.

**Arguments**:

- `defaults` - A dictionary containing the new default values.
  

**Notes**:

  It is always necessary to add a default value for a setting before accessing it.

#### value

```python
def value(key: SettingID) -> typing.Any
```

Gets the value of a setting.

The value is first looked up in the environment variables. If not found, the loaded settings are searched.
If that also fails, the defaults are used.

**Arguments**:

- `key` - The identifier of the setting.
  

**Returns**:

  The value of the setting.
  

**Raises**:

- `KeyError` - The setting identifier was not found in the defaults.

#### settings\_file

```python
@property
def settings_file() -> str
```

The name of the currently loaded settings file.

