# Component service Dockerfile (development mode)
# --
FROM    rds-ng/py-base:develop

# Argument definitions; note that COMPONENT_NAME MUST always be specified externally!
ARG     COMPONENT_NAME
ARG     COMPONENT_FILE="main"
ARG     COMPONENT_APP="app"
ARG     COMPONENT_PORT=6969
ARG     COMPONENT_THREADS=9

# Copy testing data
WORKDIR /data

COPY    /deployment/data/ .

# Copy the source code
WORKDIR /component

COPY    /src/common ./common
COPY    /src/${COMPONENT_NAME} ./${COMPONENT_NAME}

ENV     PYTHONPATH="/component"

# Run the container
WORKDIR /component/${COMPONENT_NAME}

ENV     COMPONENT_NAME=${COMPONENT_NAME}
ENV     COMPONENT_FILE=${COMPONENT_FILE}
ENV     COMPONENT_APP=${COMPONENT_APP}
ENV     COMPONENT_PORT=${COMPONENT_PORT}
ENV     COMPONENT_THREADS=${COMPONENT_THREADS}

ENV     PYTHONDONTWRITEBYTECODE=1
ENV     RDS_GENERAL_DEBUG=1
ENV     FLASK_DEBUG=1
ENV     FLASK_ENV=development

EXPOSE  ${COMPONENT_PORT}
CMD     gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" --workers 1 --threads $COMPONENT_THREADS -b ":$COMPONENT_PORT" --reload "$COMPONENT_FILE:$COMPONENT_APP"
