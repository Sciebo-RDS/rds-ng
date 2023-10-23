# Web component Dockerfile (development mode)
# --
FROM    rds-ng/node-base:develop

# Argument definitions; note that COMPONENT_NAME MUST always be specified externally!
ARG     COMPONENT_NAME
ARG     COMPONENT_COMMAND="dev"
ARG     COMPONENT_PORT=6969

# Copy/create all necessary package.json files so we can install dependencies early (before copying the actual sources)
WORKDIR /app

COPY    /src/common/package.json ./common/
COPY    /src/${COMPONENT_NAME}/package.json ./${COMPONENT_NAME}/

# Create the workspace package.json file and install all Node dependencies
RUN     echo "{ \"private\": true, \"workspaces\": [\"common\", \"${COMPONENT_NAME}\"] }" > package.json \
&&      npm install \
&&      cd ${COMPONENT_NAME} \
&&      npm install "../common"

# Finally, copy the entire source code
COPY    /src/common ./common
COPY    /src/${COMPONENT_NAME} ./${COMPONENT_NAME}

# Run the container
WORKDIR /app/${COMPONENT_NAME}

ENV     COMPONENT_NAME=${COMPONENT_NAME}
ENV     COMPONENT_COMMAND=${COMPONENT_COMMAND}
ENV     COMPONENT_PORT=${COMPONENT_PORT}

ENV     RDS_GENERAL_DEBUG=1

EXPOSE  ${COMPONENT_PORT}
CMD     npm run $COMPONENT_COMMAND -- --host="0.0.0.0" --port=$COMPONENT_PORT
