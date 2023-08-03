# Web service Dockerfile (development mode)
# --
FROM    rds-ng/node-base:develop

# Argument definitions; note that WEB_NAME MUST always be specified externally!
ARG     WEB_NAME
ARG     WEB_COMMAND="dev"
ARG     WEB_PORT=6969

# Copy the source code
WORKDIR /app

COPY    /src/common/web ./web-common
COPY    /src/web/${WEB_NAME} ./web-${WEB_NAME}

# Install the local 'web-common' package
RUN     cd web-${WEB_NAME} \
&&      npm install "../web-common"

# Update some module paths
COPY    /deployment/scripts/update-module-paths.sh .
RUN     ./update-module-paths.sh ./web-${WEB_NAME} \
&&      rm -f ./update-module-paths.sh

# Create the workspace package.json file and install Node dependencies
RUN     echo "{ \"private\": true, \"workspaces\": [\"web-${WEB_NAME}\", \"web-common\"] }" > package.json \
&&      npm install

# Run the container
WORKDIR /app/web-${WEB_NAME}

ENV     WEB_NAME=${WEB_NAME}
ENV     WEB_COMMAND=${WEB_COMMAND}
ENV     WEB_PORT=${WEB_PORT}

EXPOSE  ${WEB_PORT}
CMD     npm run $WEB_COMMAND -- --host="0.0.0.0" --port=$WEB_PORT
