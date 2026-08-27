# Kubernetes deployment

Charts for a Helm/k8s deployment can be found in `deployment/charts`. Please refer to the included `values.yaml` files for further details.

**Note:** The charts are still under development, so not everything might work as expected yet.

## Live changes

Debugging a running k8s deployment can be difficult, since live changes usually don't work. However, both the backend and frontend containers can nevertheless be edited on-the-fly:

- The frontend container will hot-reload all changes.
- The backend containers will not be able to directly handle changes, but it is possible to restart the internal Python process without killing the entire pod:
    1. Modify the files you want to change; this probably will lead to all sorts of Python errors, which can be ignored.
    1. Take a look at all running processes by executing `ps aux`; the output will look something like this:
        ```
        USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
        root           1  0.0  0.0   2680  1124 ?        Ss   Sep03   0:00 /bin/sh -c gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" --workers 1 --threads $COMPONENT_THREADS --timeout 900 -b ":$COMPONENT_PORT" "$COMPONENT_FILE:$COMPONEN
        root           7  0.0  0.0  40988 31320 ?        S    Sep03   0:06 /usr/local/bin/python3.12 /usr/local/bin/gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker --workers 1 --threads 9 --timeout 900 -b :6969 main:app
        root           8  0.1  0.0 154872 65200 ?        S    Sep03   2:00 /usr/local/bin/python3.12 /usr/local/bin/gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker --workers 1 --threads 9 --timeout 900 -b :6969 main:app
        root          13  0.0  0.0   4764  4108 pts/0    Ss   08:42   0:00 bash
        root          19  0.0  0.0   6792  3876 pts/0    R+   08:42   0:00 ps aux
        ```

       Take note of the Python process with the higher VSZ and RSS; this is the process you want to restart (in most cases, this will be PID **8**).
    1. Kill the process you just identified by issueing `kill -1 8`; this will send a hangup/termination signal to the process and let it gracefully reload.
    1. The Python process should be immediately restarted while the pod keeps running; all changes will now take effect.

# Local deployment

The directory `deployment/local` contains files to run a local deployment alongside a Nextcloud. The makefile located in the project root directory can be used to build and run this deployment. Before using this, though, read the instructions in [LOCAL_DEPLOYMENT.md](deployment/local/LOCAL_DEPLOYMENT.md) carefully, as it will not work out-of-the-box!
