# RDS-NG - Changelog

## v1.4.0 - 2026-01-12

### New

- Connectors can be excluded on a per-tenant basis

### Improvements

- Extended tenant (host+frontend) support
- Reworked Helm charts
- API protocol versions are now compared, leading to notifications in case of mismatches

### Fixes

- Occasional UI freezes on load

## v1.3.0 - 2025-12-09

### New

- **datasafe** connector
- **Dataverse** connector
- Authorization strategy `bearer`

### Improvements

- Made connection and transfer attempts use exponential delays to make them more error tolerant
- Append the instance ID to user IDs to avoid clashes between instances

### Fixes

- Optional metadata profiles were always checked for required fields, even if not selected
- Update Python WebDAV library due to issues with file downloads

## v1.2.0 - 2025-10-17

### New

- Support for multiple hosts
- Basic authentication (username/password) support for connectors
- More debugging capabilities

### Improvements

- Unaccessible resource paths are handled less pungent
- Meta and connector information can be set via environment variables
- Configurable support email address

### Fixes

- Project state renewals could lead to deadlocks
- Minor fixes here and there

## v1.1.1 - 2025-08-25

### Improvements

- Connectors log the announcements they send

### Fixes

- User settings could go out-of-sync if the server was unable to apply the new settings

## v1.1.0 - 2025-08-22

### New

- Multiple, user-selectable metadata profiles are now supported where applicable
- Authorization is done through a new endpoint in the integration app to better support multiple frontends on a single backend

### Improvements

- When adding a new connection, the authorization process will start automatically
- Retry authorization requests a few times before failing
- The usual bit of small UI improvements

## v1.0.4 - 2025-07-25

### Improvements

- Show a hint if no connections have been added in the projects list

### Fixes

- The wrong root directory is used for data annotation

## v1.0.3 - 2025-07-22

### Improvements

- Load file trees dynamically to avoid performance issues

### Fixes

- Authorization site doesn't display correctly on smaller resolutions
- Minor UI fixes

## v1.0.2 - 2025-07-14

### Improvements

- More helpful error pages
- Other small UI improvements

### Fixes

- Auto-reload doesn't work in Firefox

## v1.0.1 - 2025-07-10

### Fixes

- Minor UI fixes

## v1.0.0 - 2025-07-03

First public beta release, now under the product name **bridgit**.

## v0.7.0 - 2024-10-07

First minimal viable product release

## v0.0.0 - 2023-05-04

Project kickoff
