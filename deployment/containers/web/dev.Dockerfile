# Web service Dockerfile (development mode)
# --
FROM    rds-ng/node-base:develop

# Argument definitions; note that WEB_NAME MUST always be specified externally!
ARG     WEB_NAME
ARG     WEB_COMMAND="dev"
ARG     WEB_PORT=6969

# Copy the source code
WORKDIR /app

COPY    /src/common ./src/common
COPY    /src/web/${WEB_NAME} .

# Install Node dependencies
RUN     npm install

# Run the container
ENV     WEB_NAME=${WEB_NAME}
ENV     WEB_COMMAND=${WEB_COMMAND}
ENV     WEB_PORT=${WEB_PORT}

EXPOSE  ${WEB_PORT}
CMD     npm run $WEB_COMMAND -- --host="0.0.0.0" --port=$WEB_PORT
