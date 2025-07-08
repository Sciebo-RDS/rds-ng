# RDS-NG configuration

Below is an overview of all available settings of each RDS-NG component. These settings can either be set in `config.toml` files (located in `src/<component>/.config`) or via environment variables.

## Environment variables

Environment variables are always prefixed with `RDS_` and written in capital letters; all dots need to replaced by underscores. A setting like `authorization.refresh_attempts_limit`, for example, translates to `RDS_AUTHORIZATION_REFRESH_ATTEMPTS_LIMIT`.

To pass environment variables into the containers, `.env` files can be used; these are placed inside the `deployment/env` directory; examples are provided in the `examples` subdirectory.

> **IMPORTANT!**
> Environment variables can only be used in the frontend when running in `develop` mode! If you want to run in `release` mode, frontend settings _must_ be set in its `config.toml`file (located in `src/frontend/static/config`).

## Settings

Most settings have reasonable defaults and usually don't need to be changed. Mandatory settngs are always listed for each component and must be set in order to be able to run RDS-NG.

> **IMPORTANT!**
> Always set all mandatory settings in your configuration! Otherwise, the setup will not run.

### Backend settings

The backend consists of the server and the various connectors; they all share a set of certain settings but also have their own ones as well.

#### Mandatory settings

- All components
    - `network.api_key`
- Server
    - `network.server.allowed_origins`
- Connectors
    - `connector.target` (1)
    - `network.client.server_address`
    - `authorization.strategy`
    - `authorization.oauth2.server.host` (2)
    - `authorization.oauth2.server.authorization_endpoint` (2)
    - `authorization.oauth2.server.token_endpoint` (2)
    - `authorization.oauth2.client.id` (2)
    - `authorization.oauth2.client.redirect_url` (2)

_(1)_ By default, connectors target the test instances of the corresponding service.
_(2)_ If the service uses OAUTH2 authorization.

> **IMPORTANT!**
> By default, data will only be stored in memory and will thus be lost whenever the server is restarted! It is thus highly advised to configure a database for the server in order to persist data.

#### All components | Network

| Setting                                        | Description                                                                                        | Type    | Default value |
|------------------------------------------------|----------------------------------------------------------------------------------------------------|---------|---------------|
| <code>network.api_key</code>                   | An arbitrary API key to access protected resources; this must be the same value on all components. | String  |               |
| <code>network.verify_sll</code>                | If enabled, SSL certificates will be verified.                                                     | Boolean | true          |
| <code>network.transmission_chunnk_size</code>  | The size (in bytes) for network transmissions.                                                     | Number  | 1048576       |
| <code>network.regular_command_timeout</code>   | The maximum time (in seconds) for a command-reply to arrive.                                       | Number  | 10.0          |
| <code>network.external_requests_timeout</code> | The maximum time (in seconds) for requests to external services; set to 0 to disable.              | Number  | 15.0          |

#### Server | Network

| Setting                                     | Description                                                                                       | Type   | Default value |
|---------------------------------------------|---------------------------------------------------------------------------------------------------|--------|---------------|
| <code>network.server.allowed_origins</code> | A comma-separated list of allowed origins; use the asterisk (*) to allow all.                     | String |               |
| <code>network.server.idle_timeout</code>    | The time (in seconds) until idle clients will be disconnected automatically; set to 0 to disable. | Number | 3600          |

#### Server | Authorization

Authorization is in most cases performed using OAUTH2. The server takes care of managing and refreshing authorization tokens of external services. Connectors also use OAUTH2 to authorizate against their respective external service.

| Setting                                           | Description                                                                         | Type   | Default value |
|---------------------------------------------------|-------------------------------------------------------------------------------------|--------|---------------|
| <code>authorization.refresh_attempts_delay</code> | The delay between token refresh attempts in seconds.                                | Number | 30.0          |
| <code>authorization.refresh_attempts_limit</code> | The maximum number of refresh attempts before removing a token; 0 disables removal. | Number | 3             |

#### Server | Storage

The server needs to store its data; this can either be in-memory (super volatile) or in a database. For production systems, a database should always be used; RDS-NG currently supports *SQLite*, *PostgreSQL*, *MySQL* and *MariaDB*. Note that all databases except SQLite require additional software not provided by us.

| Setting                                           | Description                                                                                           | Type   | Default value |
|---------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------|---------------|
| <code>storage.driver</code>                       | The driver to use for the storage; possible values are *memory* or *database*.                        | String | memory        |
| <code>storage.database.engine</code>              | The database backend to use; can be *sqlite*, *postgresql*, *mysql* or *mariadb*.                     | String | sqlite        |
| <code>storage.database.sqlite.file</code>         | The (absolute) filename where SQLite stores its data; if not set, an in-memory database will be used. | String |               |
| <code>storage.database.postgresql.host</code>     | The host of the database system.                                                                      | String |               |
| <code>storage.database.postgresql.port</code>     | The port of the database system; if omitted, the default port will be used.                           | Number |               |
| <code>storage.database.postgresql.database</code> | The name of the database to use.                                                                      | String | rds_ng        |
| <code>storage.database.postgresql.user</code>     | The database username.                                                                                | String |               |
| <code>storage.database.postgresql.password</code> | The password for the database user.                                                                   | String |               |
| <code>storage.database.mysql.host</code>          | The host of the database system.                                                                      | String |               |
| <code>storage.database.mysql.port</code>          | The port of the database system; if omitted, the default port will be used.                           | Number |               |
| <code>storage.database.mysql.database</code>      | The name of the database to use.                                                                      | String | rds_ng        |
| <code>storage.database.mysql.user</code>          | The database username.                                                                                | String |               |
| <code>storage.database.mysql.password</code>      | The password for the database user.                                                                   | String |               |
| <code>storage.database.mariadb.host</code>        | The host of the database system.                                                                      | String |               |
| <code>storage.database.mariadb.port</code>        | The port of the database system; if omitted, the default port will be used.                           | Number |               |
| <code>storage.database.mariadb.database</code>    | The name of the database to use.                                                                      | String | rds_ng        |
| <code>storage.database.mariadb.user</code>        | The database username.                                                                                | String |               |
| <code>storage.database.mariadb.password</code>    | The password for the database user.                                                                   | String |               |

#### Connectors | General

| Setting                       | Description                                                   | Type   | Default value                       |
|-------------------------------|---------------------------------------------------------------|--------|-------------------------------------|
| <code>connector.target</code> | The URL of the connector target (i.e., its external service). | String | _(the service's test instance URL)_ |

#### Connectors | Network

| Setting                                        | Description                                                           | Type   | Default value |
|------------------------------------------------|-----------------------------------------------------------------------|--------|---------------|
| <code>network.client.server_address</code>     | The address of the server the client should automatically connect to. | String |               |
| <code>network.client.connection_timeout</code> | The maximum time (in seconds) for connection attempts.                | Number | 10.0          |

#### Connectors | Authorization

| Setting                                                         | Description                                                                                                                                                                | Type   | Default value |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------|
| <code>authorization.strategy</code>                             | The authorization strategy (type) the external service uses; currently, only **oauth2** is supported.                                                                      | String |               |
| <code>authorization.oauth2.server.host</code>                   | The OAUTH2 host server, as provided by the external service.                                                                                                               | String |               |
| <code>authorization.oauth2.server.authorization_endpoint</code> | The (relative) authorization endpoint; this is usually documented by the external service provider.                                                                        | String |               |
| <code>authorization.oauth2.server.token_endpoint</code>         | The (relative) token endpoint; this is usually documented by the external service provider.                                                                                | String |               |
| <code>authorization.oauth2.server.scope</code>                  | The (optional) access scope.                                                                                                                                               | String |               |
| <code>authorization.oauth2.client.id</code>                     | The OAUTH2 client ID of the connector.                                                                                                                                     | String |               |
| <code>authorization.oauth2.client.secret</code>                 | The OAUTH2 client secret of the connector.                                                                                                                                 | String |               |
| <code>authorization.oauth2.client.redirect_url</code>           | The URL OAUTH2 will redirect to; this needs to be set to the full URL of the host integration (e.g., `http://localhost:8080/apps/rdsng/main` for a local Nextcloud setup). | String |               |
| <code>transmission.max_attempts</code>                          | The maximum number of transmission operation (up-/downloads) attempts.                                                                                                     | Number | 3             |
| <code>transmission.attempts_delay</code>                        | The delay (in seconds) between transmission operation (up-/downloads) attempts.                                                                                            | Number | 3.0           |

### Frontend settings

#### Mandatory settings

- <code>network.client.server_address</code>
- <code>integration.host.api_url</code>
- <code>authorization.oauth2.client.id</code> (1)
- <code>authorization.oauth2.client.redirect_url</code> (1)

_(1)_ If the host uses OAUTH2 authorization.

#### General

| Setting                                    | Description                                                         | Type    | Default value |
|--------------------------------------------|---------------------------------------------------------------------|---------|---------------|
| <code>general.verbose_notifications</code> | Whether to display more verbose notifications (good for debugging). | Boolean | false         |
| <code>general.notification_timeout</code>  | The timeout for overlay notifications in seconds.                   | Number  | 3.0           |
| <code>general.notification_timeout</code>  | The timeout for overlay notifications in seconds.                   | Number  | 3.0           |

#### Theming

| Setting                                | Description                           | Type   | Default value |
|----------------------------------------|---------------------------------------|--------|---------------|
| <code>theme.primary_color</code>       | The primary theme color.              | String | #29833B       |
| <code>theme.light.surface_color</code> | The surface color when in light mode. | String | Slate         |
| <code>theme.dark.surface_color</code>  | The surface color when in dark mode.  | String | White         |

#### Networking

| Setting                                        | Description                                                           | Type   | Default value |
|------------------------------------------------|-----------------------------------------------------------------------|--------|---------------|
| <code>network.regular_command_timeout</code>   | The maximum time (in seconds) for a command-reply to arrive.          | Number | 10.0          |
| <code>network.client.server_address</code>     | The address of the server the client should automatically connect to. | String |               |
| <code>network.client.connection_timeout</code> | The maximum time (in seconds) for connection attempts.                | Number | 10.0          |

#### Integration

| Setting                               | Description                                                                                                                                                                                | Type   | Default value |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------|
| <code>integration.host.api_url</code> | The full URL where the host integration exposes its API; this needs to be in the form of `<APP_URL>/api/v1` (e.g., `http://localhost:8080/apps/rdsng/api/v1` for a local Nextcloud setup). | String |               |

#### Authorization

In order to be properly integrated into its host system, the frontend will authorize against it using OAUTH2. This means that you usually will need to generate a new OAUTH2 client ID and secret for the frontend in your host system.

| Setting                                               | Description                                                                                                                                                                | Type   | Default value |
|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------|
| <code>authorization.oauth2.client.id</code>           | The OAUTH2 client ID of the frontend.                                                                                                                                      | String |               |
| <code>authorization.oauth2.client.redirect_url</code> | The URL OAUTH2 will redirect to; this needs to be set to the full URL of the host integration (e.g., `http://localhost:8080/apps/rdsng/main` for a local Nextcloud setup). | String |               |
