# Component service Dockerfile
# --
FROM    rds-ng/py-base:latest

# Argument definitions; note that COMPONENT_NAME MUST always be specified externally!
ARG     COMPONENT_NAME
ARG     COMPONENT_FILE="component.py"
ARG     COMPONENT_APP="app"
ARG     COMPONENT_PORT=6969
ARG     COMPONENT_THREADS=9

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

ENV     RDS_DEBUG=0
ENV     FLASK_DEBUG=0
ENV     FLASK_ENV=production

EXPOSE  ${COMPONENT_PORT}
CMD     uwsgi --http=":$COMPONENT_PORT" --workers=1 --gevent=$COMPONENT_THREADS --http-websockets --master --disable-logging --log-4xx --log-5xx --wsgi-file="$COMPONENT_FILE" --callable="$COMPONENT_APP"
