---
sidebar_label: random
title: utils.random
---

#### generate\_random\_string

```python
def generate_random_string(length: int,
                           *,
                           include_punctuation: bool = False) -> str
```

Generates a random string consisting of ``length`` characters.

By default, all ASCII-letters (upper- and lower-case) as well as all digits are used. If ``include_punctuation`` is set to ``True``,
punctuation characters are used as well.

**Arguments**:

- `length` - The length of the generated strings.
- `include_punctuation` - Whether to include punctuation characters.
  

**Returns**:

  The generated string.
  

**Raises**:

- `ValueError` - If the specified length is less than 1.

