---
sidebar_label: network_setting_ids
title: settings.network_setting_ids
---

## NetworkServerSettingIDs Objects

```python
class NetworkServerSettingIDs()
```

Identifiers for server-specific networking settings.

**Attributes**:

- `ALLOWED_ORIGINS` - A comma-separated list of allowed origins; use the asterisk (*) to allow all (value type: ``string``).
- `IDLE_TIMEOUT` - The time (in seconds) until idle clients will be disconnected automatically; set to 0 to disable.

## NetworkClientSettingIDs Objects

```python
class NetworkClientSettingIDs()
```

Identifiers for client-specific networking settings.

**Attributes**:

- `SERVER_ADDRESS` - The address of the server the client should automatically connect to (value type: ``string``).
- `CONNECTION_TIMEOUT` - The maximum time (in seconds) for connection attempts (value type: ``float``).

