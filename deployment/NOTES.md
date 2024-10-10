# Deployment notes

## Environment files

Variables are passed to the containers via environment files found under `/deployment/env/`. We do not supply any defaults here, but examples can be found under `/deployment/env/examples`. Copy these to `/deployment/env` and adjust them to match your own deployment environment.

### Prefixes

By default, the `Release` deployment uses no prefixes for these files, while the `Debug` one uses a `dev.` prefix.

To change the prefix to use, create a `.env` file in `/deployment/containers/` and set the following environment variable:

```
RDS_NG_BUILD_ENVIRONMENT_PREFIX=example.
```

This will then use environment files prefixed with `example.` for building the containers (e.g., `example.server.env`).

Using your own prefix allows you to quickly switch between different configurations.
