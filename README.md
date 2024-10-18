# Sciebo RDS - Next Generation

This is the repository of the next-gen version of **Sciebo** **R**esearch **D**ata **S**ervices, codenamed **_RDS-NG_**.

## Directories

Here's a list of the main directories found within this repository:

| Directory     | Contents                                                                                                                                                                                                                                                          |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/deployment` | All deployment related files, like Helm templates, Dockerfiles, etc.                                                                                                                                                                                              |
| `/src`        | The source code for all components of RDS-NG.                                                                                                                                                                                                                     |
| `/config`     | Project configuration files; note that these files are _not_ runtime configuration files for the various components themselves.                                                                                                                                   |
| `/scripts`    | Various helper scripts, used especially for development purposes. These are not part of the main software stack, and are usually used to perform meta-tasks like type checking, etc. Note that the scripts must be called from within the main project directory. |
| `/docs`       | The entire developers' documentation as a Docusaurus project.                                                                                                                                                                                                     |
| `/.trunk`     | Unsorted files kept for development purposes; will be removed at some point.                                                                                                                                                                                      |
| `/.bin`       | Some helper scripts that are mostly internal but could be useful for others, too.                                                                                                                                                                                 |

## Local deployment

For easy local deployment, we have provided a `docker-compose.yaml` found in `/deployment/containers` that can be used to build and run all components on your local computer. To make this process even easier, an accompanying `makefile` is provided supporting the following commands:

| Directive         | Description                                             |
|-------------------|---------------------------------------------------------|
| `build` (default) | Builds all containers                                   |
| `build-no-cache`  | Builds all containers, ignoring previously cached steps |
| `run`             | Builds and starts all containers interactively          |
| `logs`            | Shows all container logs                                |

All commands (except for `logs`) are also available as a development-specific version: Simply put a `dev-` in front of the command, i.e. `dev-build`.

## Coding style

We use [black](https://github.com/psf/black) (for Python) and [Prettier](https://github.com/prettier/prettier) (for TypeScript) as code formatters. Please use those to format your code before you push, chances are there's an extension for your IDE.
