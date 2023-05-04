# Component service Dockerfile
# --

# Argument definitions; note that COMPONENT_NAME MUST always be specified externally!
ARG     COMPONENT_NAME=""
ARG     COMPONENT_APP="component:app"
ARG     COMPONENT_PORT=6969
ARG     COMPONENT_WORKERS=4

# Python-based component
FROM    rds-ng/py-base:latest

# Copy the source code
WORKDIR /component

COPY    /src/common ./common
COPY    /src/${COMPONENT_NAME} ./${COMPONENT_NAME}

# Run the component on port 6969
WORKDIR /component/${COMPONENT_NAME}

ENV     COMPONENT_NAME $COMPONENT_NAME
ENV     COMPONENT_APP $COMPONENT_APP
ENV     COMPONENT_PORT $COMPONENT_PORT
ENV     COMPONENT_WORKERS $COMPONENT_WORKERS
EXPOSE  6969

ENTRYPOINT     gunicorn --bind="0.0.0.0:$COMPONENT_PORT" --workers=$COMPONENT_WORKERS --reload "$COMPONENT_APP"
