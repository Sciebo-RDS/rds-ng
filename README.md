# Sciebo RDS - Next Generation

This is the repository of the next-gen version of **Sciebo** **R**esearch **D**ata **S**ervices, codenamed **_RDS-NG_**, also known as `bridgit`.

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

## Feedback

We're always eager to hear from you! Feel free to email us about any issues you encounter or features that you'd like to see: [sciebo.rds@uni-muenster.de](mailto:sciebo.rds@uni-muenster.de)!
