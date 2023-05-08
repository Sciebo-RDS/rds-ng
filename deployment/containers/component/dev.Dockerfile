# Component service Dockerfile (development mode)
# --
FROM    rds-ng/py-base:develop

# Argument definitions; note that COMPONENT_NAME MUST always be specified externally!
ARG     COMPONENT_NAME
ARG     COMPONENT_APP="component:app"
ARG     COMPONENT_PORT=6969

# Copy the source code
WORKDIR /component

COPY    /src/common ./common
ADD     /src/${COMPONENT_NAME} ./${COMPONENT_NAME}

# Run the container
WORKDIR /component/${COMPONENT_NAME}

ENV     COMPONENT_NAME=${COMPONENT_NAME}
ENV     COMPONENT_APP=${COMPONENT_APP}
ENV     COMPONENT_PORT=${COMPONENT_PORT}
ENV     COMPONENT_WORKERS=${COMPONENT_WORKERS}

ENV     FLASK_ENV=development
ENV     FLASK_DEBUG=1

EXPOSE  ${COMPONENT_PORT}
CMD     gunicorn --bind="0.0.0.0:$COMPONENT_PORT" --workers=1 --reload --log-level="debug" "$COMPONENT_APP"
