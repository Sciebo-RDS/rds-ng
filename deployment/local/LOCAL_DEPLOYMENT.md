# Local development deployment

This is a guide on how to run a local deployment of RDS NG/bridgit integrated into a Nextcloud instance.

For this to work, you need to also clone the [rds-ng-nextcloud](https://github.com/Sciebo-RDS/rds-ng-nextcloud) repository next to this one, so that both repositories are located in the same base directory:

```
<common base directory>
  |- rds-ng
  |- rds-ng-nextcloud
```

## Prerequisites

Unfortunately, running a local instance of RDS NG+Nextcloud Integration is no easy feat, mainly due to browser security restrictions. There are a few steps that must be taken on the local system before being able to run the provided setup:

1. Add local domains
   Edit `/etc/hosts` and add the following two entries:
    ```
    127.0.0.1 nextcloud.dev.local
    127.0.0.1 bridgit.nextcloud.dev.local
    ```
2. Install **mkcert** and execute the following:
    ```
    mkcert -install

   mkcert \
    -cert-file local.crt \
    -key-file local.key \
    nextcloud.dev.local bridgit.nextcloud.dev.local
   ```
3. Copy the generated two files into `deployment/local/certs`.

These steps will allow you to use the two local domains to work over *https*, which is necessary for RDS NG to work properly.

Next, a few setup steps for Nextcloud need to be done:

1. Start the local deployment by simply running `make` in the main project directory; ignore any warnings or errors.
2. Once the Nextcloud container has started, go to `https://nextcloud.dev.local` and follow the on-screen instructions (use `admin/admin` to log in).
3. Enter the running Nextcloud container:
    ```
   docker exec -it nextcloud bash
   ```
4. Run the following commands in the container:
    1. Change ownership of `custom_apps`:
       ```
       chown -R www-data:www-data custom_apps
       ```
    2. Create an OAuth2 Client for RDS NG:
       ```
       ./occ oauth2:add-client "rds-ng" "https://nextcloud.dev.local/apps/rdsng"
       ```
       This will print out, among others, the client ID and secret. Open `env/00-oauth2.env` and copy the value of `clientId` to the environment variable `RDS_NG_OAUTH2_CLIENT_ID`, and the value of `clientSecret` to `RDS_NG_OAUTH2_CLIENT_SECRET`. Here is an example of how the final `00-oauth2.env` should look like (the shown values are, of course, only examples):
       ```
       RDS_NG_OAUTH2_CLIENT_ID=XxkqgCYAdMvBSrMukziVfwEhLKLPBrl5KmQLHblUgQQyCEbBSJqJF9uS1O1cC2Kl
       RDS_NG_OAUTH2_CLIENT_SECRET=7bXPn8hc4CLvszkap241QZfkXLwTtPWm1ZPpoFwyairJ3aG8gojrnf978yWj5QFA
       ```
5. Restart the deployment (this is necessary for the changes to take effect). You can do this by hitting `d` in the terminal of the running deployment (this will detach from all its processes, thus terminating the entire deployment) and rerun `make`.

All these steps only need to be done once. **Note**: The Nextcloud setup needs to be redone if you delete the `nextcloud` Docker volume.

## Configuration

1. After logging in to Nextcloud as `admin`, go to the _Apps_ settings section. Under _Disabled apps_, locate _bridgit_ and enable it.
2. Open the _Administration settings_ and go to the _bridgit_ section. Enter the following settings:
3.
    - **Frontend:**
        - **Frontend URL**: `https://bridgit.nextcloud.dev.local`
        - **Instance ID**: `default`
    - **Backend:**
        - **Domo URL:**: `https://bridgit.nextcloud.dev.local:5500`
        - **API key**: `V1ZXHYc4IOWtPCh5`

It's advisable to make sure that the settings have been saved by reloading the page.

## Running a local deployment

The provided `makefile` in the project root directory can be used to build local container images and boot up a local deployment; simply run `make` without any target. This will also start a Nextcloud instance, which runs on `https://nextcloud.dev.local`. The default administrator login is `admin/admin`.

To stop the entire deployment, simply press `d` to detach in the console; this will automatically stop all containers.
