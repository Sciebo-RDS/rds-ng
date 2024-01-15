# Web component Dockerfile (release mode)
# --

# First stage: Build the web application via node and provide it as an internal image
FROM    rds-ng/node-base:latest as build-stage

# Argument definitions; note that COMPONENT_NAME MUST always be specified externally!
ARG     COMPONENT_NAME

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

# Build the container
WORKDIR /app/${COMPONENT_NAME}

ENV     COMPONENT_NAME=${COMPONENT_NAME}

ENV     RDS_GENERAL_DEBUG=0

RUN     npm run build


# Second stage: Create an Nginx web server and add the built application to it
FROM    nginx:latest

# Argument definitions; note that COMPONENT_NAME MUST always be specified externally!
ARG     COMPONENT_NAME

# Copy the web application from the build-stage image
WORKDIR /app
COPY    --from=build-stage /app/${COMPONENT_NAME}/dist /app

# Copy the main Nginx config
COPY    /deployment/containers/web-component/nginx.conf /etc/nginx/nginx.conf
