---
sidebar_label: meta_information
title: component.meta_information
---

## MetaInformation Objects

```python
class MetaInformation()
```

Accesses meta information about the entire project and its various component stored in a *JSON* file.

The JSON file needs to be structured like this::

    {
        &quot;global&quot;: {
            &quot;title&quot;: &quot;RDS-NG&quot;,
            &quot;version&quot;: &quot;0.0.1&quot;
        },

        &quot;components&quot;: {
            &quot;gate&quot;: {
                &quot;name&quot;: &quot;Gate service&quot;,
                &quot;directory&quot;: &quot;gate&quot;,
                &quot;tech&quot;: &quot;py&quot;
            },
            ...
        }
    }

#### \_\_init\_\_

```python
def __init__(info_file: str = "/config/meta-information.json")
```

**Arguments**:

- `info_file` - The JSON file to load the meta information from.
  

**Raises**:

- `ValueError` - If the information file couldn&#x27;t be loaded.

#### title

```python
@property
def title() -> str
```

The project title.

#### version

```python
@property
def version() -> Version
```

The project version (see https://semver.org).

#### get\_components

```python
def get_components() -> typing.List[str]
```

A list of all component names.

**Returns**:

  The names of all components.

#### get\_component

```python
def get_component(comp: str) -> typing.Dict[str, typing.Any]
```

Retrieves the meta information stored for a specific component.

This meta information includes the ``name`` of the component, as well as its ``directory`` within the code structure (rooted at ``/src``).

**Arguments**:

- `comp` - The name of the component.
  

**Returns**:

  A dictionary containing the meta information.

