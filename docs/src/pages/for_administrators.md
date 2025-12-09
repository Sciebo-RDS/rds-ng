---
title: For technical administrators
description: Why your institution should use bridgit
hide_table_of_contents: false
---

# *bridgit* for Technical Administrators
<div style={{textAlign: 'center', width: '35%', float: 'right' }}>
  <img class="bg-white"  src="/img/octopi/developer.png" />
</div>

*bridgit* is an open-access research data management app developed in an academic setting to support researchers. The app was successfully piloted at the University of Münster in the Sciebo Hochschulcloud NRW, where it was seamlessly integrated into an existing Nextcloud environment.

For administrators, *bridgit* offers a modular add-on that can be integrated into Nextcloud-based infrastructures or other university cloud services. It provides institutions with a secure, compliant, and researcher-friendly tool for research data management without disrupting existing workflows.

## Why Nextcloud?
*bridgit* has been designed with Nextcloud integration in mind, making it a natural fit for universities and institutions that already rely on Nextcloud for cloud storage and collaboration. By running as an add-on, *bridgit* benefits from Nextcloud’s secure, user-managed environment while adding domain-specific functionality tailored to research data.


## Getting Started as an Administrator
1.	**Clone the Repository**
 Pull the latest version of *bridgit* from GitHub:
`git clone https://github.com/Sciebo-RDS/rds-ng.git`

2.	**Install Dependencies**
 Navigate to the project directory and install all required dependencies:
```
cd bridgit
[PLACEHOLDER_FOR_DEPENDENCY_COMMANDS]
```

3.	**Deploy to Nextcloud**
 Copy *bridgit* into your Nextcloud apps directory:
`cp -r bridgit /var/www/nextcloud/apps/`

4.	**Enable the App**
 Log into your Nextcloud as an admin and activate *bridgit* via the Apps section.

5.	**Configuration**
- Configure repository connections (Zenodo, OSF, etc.)
- Set access rights for researchers and administrators
- Adjust metadata schema as required for your institution

## Extend and Contribute
*bridgit* is an open-source project and welcomes contributions. Developers can:

- Create plugins to support additional repositories
- Extend metadata annotation features
- Integrate with institutional authentication systems


Fork, contribute, and submit pull requests here:

- **[GitHub Repository](https://github.com/Sciebo-RDS/rds-ng)**
- **[Deployment Documentation](https://github.com/Sciebo-RDS/rds-ng/blob/release/DEPLOYMENT.md)**

## Summary
*bridgit* provides a ready-to-integrate, open-access solution for research data management in academic cloud infrastructures. By leveraging Nextcloud as its foundation, it ensures security, scalability, and usability for researchers while remaining flexible for administrators.

