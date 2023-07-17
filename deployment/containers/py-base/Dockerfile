# Base image for all Python-based components
# --
FROM    python:3.11

# Update the image first
RUN     apt-get update \
&&      apt-get -y upgrade

# Install basic Python libraries
WORKDIR /base

COPY    /deployment/containers/py-base/requirements.txt .
RUN     pip install -r ./requirements.txt

# Add project configuration
WORKDIR /config
COPY    /config .
