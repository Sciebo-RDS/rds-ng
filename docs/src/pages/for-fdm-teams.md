---
title: For RDM Service Teams
description: bridgit for FDM Teams
hide_table_of_contents: false
---

## For RDM Service Teams

<div style={{textAlign: 'center', width: '25%', float: 'right', margin: '2%'}}>

<span style={{ margin: '2%' }}>
<img class="bg-white"  src="/img/octopi/developer.png" />
</span>

</div>

_bridgit_ is built for the people who make research data management work: the coordinators, admins, and developers who connect systems, set standards, and keep everything running smoothly.
For developers, _bridgit_ offers a modular add-on that can be integrated into Nextcloud-based infrastructures or other university cloud services. It provides institutions with a secure, compliant, and researcher-friendly tool for research data management without disrupting existing workflows.

## For Research Data Management Departments

RDM departments set up _bridgit_ to translate data policies and FAIR principles into the actual configuration researchers see every day.

What you can do with _bridgit_:

- Define institutional metadata schemas and required fields for your specific datasets
- Set default templates for Data Management Plans (DMPs) that align with funder requirements
- Establish workflows for dataset review, approval, and publication
- Monitor FAIRness and data-sharing activity via dashboard reports
- Provide centralized documentation and help texts within the _bridgit_ interface

Get in touch with us now to help you setting up the app in your ecosystem!

## For Admins and Implementators

Admins ensure that _bridgit_ runs securely inside the institutional environment and that users can access it with their existing credentials.

How to get started:

- Deploy _bridgit_ as an app within the institutional Sciebo or Nextcloud instance
- Integrate _bridgit_ with identity management systems (Shibboleth, LDAP, SSO)
- Connect external storage or repository endpoints (e.g. Zenodo, OSF, institutional archives)
- Enable or disable modules (annotation, DMPs, publication) depending on user groups
- Manage access roles (researcher, reviewer, institutional admin)
- Configure automatic metadata synchronization between _bridgit_ and institutional databases

Install the _bridgit_ app within your Sciebo or Nextcloud environment and connect it to your identity system. Our deployment guide will walk you through it.

## For Developers & Deployers

_bridgit_’s modular and API-driven architecture allows you to build new connectors, automate processes, and adapt the app to your infrastructure. One best practice example for you to get inspired: _bridgit_ was successfully piloted at the University of Münster in the Sciebo Hochschulcloud NRW, where it was seamlessly integrated into an existing Nextcloud environment.

How to get started:

1. **Clone the Repository**
   Pull the latest version of _bridgit_ from GitHub:
   `git clone https://github.com/Sciebo-RDS/rds-ng.git`

2. **Install Dependencies**
   Navigate to the project directory and install all required dependencies:

```
cd bridgit
```

3. **Deploy to Nextcloud**
   Copy _bridgit_ into your Nextcloud apps directory:
   `cp -r bridgit /var/www/nextcloud/apps/`

4. **Enable the App**
   Log into your Nextcloud as an admin and activate _bridgit_ via the Apps section.

5. **Configuration**

- Configure repository connections (Zenodo, OSF, etc.)
- Set access rights for researchers and administrators
- Adjust metadata schema as required for your institution

### Extend and Contribute

_bridgit_ is an open-source project and welcomes contributions. Developers can:

- Create plugins to support additional repositories
- Extend metadata annotation features
- Integrate with institutional authentication systems

Fork, contribute, and submit pull requests here:

- **[GitHub Repository](https://github.com/Sciebo-RDS/rds-ng)**
- **[Deployment Documentation](https://github.com/Sciebo-RDS/rds-ng/blob/release/DEPLOYMENT.md)**

## Get in Touch

The underlying philosophy is simple: just as research data should be shared openly to maximize its benefit for science, the app itself is shared openly so that any institution can adopt it and simplify research data sharing for its community.

If you have any further questions on how to install *bridgit* in your institution’s environment, please don’t hesitate to contact:

University of Münster – sciebo.rds@uni-muenster.de

Or visit our [Contact Page](contact) for further details.
