# Base image for all Python-based components (development mode)
# --
FROM    python:3.11

# Update the image first (and install some helpful tools)
RUN     apt-get update \
&&      apt-get -y upgrade \
&&      apt-get -y install nano

# Install basic Python libraries
WORKDIR /base

COPY    /deployment/containers/py-base/requirements.txt .
RUN     pip install -r ./requirements.txt

COPY    /deployment/containers/py-base/dev.requirements.txt .
RUN     pip install -r ./dev.requirements.txt

# Add project configuration
WORKDIR /config
COPY    /config .
