# Web service Dockerfile (development mode)
# --
FROM    rds-ng/node-base:develop

# Argument definitions; note that WEB_NAME MUST always be specified externally!
ARG     WEB_NAME
ARG     WEB_COMMAND="dev"
ARG     WEB_PORT=6969

# Copy/create all necessary package.json files so we can install dependencies early (before copying the actual sources)
WORKDIR /app

COPY    /src/common/web/package.json ./web-common/
COPY    /src/web/${WEB_NAME}/package.json ./web-${WEB_NAME}/

# Create the workspace package.json file and install all Node dependencies
RUN     echo "{ \"private\": true, \"workspaces\": [\"web-${WEB_NAME}\", \"web-common\"] }" > package.json \
&&      npm install \
&&      cd web-${WEB_NAME} \
&&      npm install "../web-common"

# Finally, copy the entire source code
COPY    /src/common/web ./web-common
COPY    /src/web/${WEB_NAME} ./web-${WEB_NAME}

# Run the container
WORKDIR /app/web-${WEB_NAME}

ENV     WEB_NAME=${WEB_NAME}
ENV     WEB_COMMAND=${WEB_COMMAND}
ENV     WEB_PORT=${WEB_PORT}

EXPOSE  ${WEB_PORT}
CMD     npm run $WEB_COMMAND -- --host="0.0.0.0" --port=$WEB_PORT
