# Local deployment

The following guide will briefly show you how to run a local setup of RDS-NG within a Nextcloud instance.

RDS-NG can be run either in `develop` or in `release` mode. We recommend to use the stable `release` setup; if you want to get all the latest changes immediately, use the `develop` setup instead.

Note that both setups are almost identical.

## Prerequisites

In order to run a local deployment of RDS-NG, you'll need Docker as well as its _compose_ plugin installed.

## Step 0: Create directories

On your machine, create a base directory where you'll put all RDS-NG components into:

```bash
mkdir rds-ng
```

Next, create the following directory inside the base one:

```bash
mkdir -p rds-ng/nextcloud/custom_apps
```

## Step 1: Clone the RDS-NG repository

Clone the RDS-NG repository:

```bash
git clone https://github.com/Sciebo-RDS/rds-ng.git
````

Checkout the `release` branch (only if you want to run the `release` setup; the default branch currently is set to `develop` automatically):

```bash
cd rds-ng
git pull
git checkout release
````

## Step 2: Clone the Nextcloud integration app

Clone the Nextcloud integration app into the `custom_apps` folder of your Nextcloud instance using the following `git` command:

```bash
git clone https://github.com/Sciebo-RDS/rds-ng-nextcloud.git
```

## Step 3: Deploy Nextcloud

The following bash script can be used to run a local Nextcloud instance ready to be used with RDS-NG.

**Note:** Replace `{BASE_PATH}` with the appropriate base path (see step 0) of your RDS-NG setup and `{YOURIP}` with the nextwork IP address of your local machine.

```bash
docker stop nextcloud
docker rm -f nextcloud
docker run -d -p 8080:80 \
  --name nextcloud \
  -e NEXTCLOUD_ADMIN_USER=admin \
  -e NEXTCLOUD_ADMIN_PASSWORD=admin \
  -v nextcloud:/var/www/html \
  -v {BASE_PATH}/nextcloud/custom_apps:/var/www/html/custom_apps \
  -v {BASE_PATH}/rds-ng-nextcloud:/var/www/html/custom_apps/rdsng \
  nextcloud:29
 
docker exec -w /var/www/html/custom_apps/rdsng nextcloud make build
docker exec -u 33 nextcloud /var/www/html/occ config:system:set trusted_domains 10 --value={YOURIP}
docker exec -u 33 nextcloud /var/www/html/occ config:system:set overwritehost --value={YOURIP}:8080
```

It's easiest to save above script to a file and execute it to launch the Nextcloud container.

### Step 3.1: Fix Nextcloud apps folder permissions

Login to the Nextcloud container:

```bash
docker exec -it nextcloud bash
```

Now, fix the apps folder permissions by executing the following command inside the Nextcloud container:

```bash
chown -R www-data:www-data custom_apps
```

### Step 3.2: Restart the container

After fixing the permissions, you'll need to start the container anew by executing above script again.

## Step 4: Configure Nextcloud

1. Browse to `localhost:8080` and login with `admin/admin`
2. In the Nextcloud main menu, go to `Apps -> Disabled Apps`, enable `BridgIT` (the display name of RDS-NG)
3. Go to `Administration Settings -> Security`, add a new OAUTH2 client
    * Name: RDS-NG
    * Redirect URL: `http://localhost:8080/apps/rdsng/main`
4. Go to `Administration Settings -> BridgIT`, set the BridgIT URL to `http://localhost:8000`

## Step 5: Configure RDS-NG

First, copy the `.env` example files in the RDS-NG repository directory from `deployment/env/examples` to `deployment/env`. Also create a folder called `.data` inside the repository directory (SQLite will store its data there):

```bash
cp deployment/env/examples/* deployment/env
mkdir .data
```

For the `release` setup, edit the `server.env` file and set `RDS_AUTHORIZATION_OAUTH2_SECRETS_HOST` to the OAUTH2 secret created in step 4, and set `RDS_AUTHORIZATION_OAUTH2_CLIENT_ID` in  `frontend.env` to the corresponding client ID. If you want to use the `develop` setup, the `.env` files are prefixed with `dev.` (e.g., `dev.server.env`).

Client IDs and secrets for the various connectors are set in the same way; you'll need to register accounts at `test.osf.io` and `sandbox.zenodo.org` first in order to use them.

To start the RDS-NG containers in `release` mode, enter `deployment/containers` and execute:

```bash
make run
```

To start them in `develop` mode, execute:

```bash
make dev-run
```

## Step 6: Open the RDS-NG app

Browse to `localhost:8080` to get to your Nextcloud instance; from there, simply launch the RDS-NG app by clicking its `BridgIT` icon in the top bar.

> **IMPORTANT!**
> You *have* to use `localhost:8080`, your local IP won't work! Nextcloud tends to redirect you to your network IP; if that happens, you'll have to replace the IP with `localhost:8080`.
