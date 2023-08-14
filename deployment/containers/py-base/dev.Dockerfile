# Base image for all Python-based components (development mode)
# --
FROM    python:3.11

# Update the image first (and install some helpful tools)
RUN     apt-get update \
&&      apt-get -y upgrade \
&&      apt-get -y install nano vim

# Some useful macros
RUN     echo 'alias ll="ls -la"' >> ~/.bashrc

# Install basic Python libraries
WORKDIR /base

COPY    /deployment/containers/py-base/requirements.txt .
RUN     pip install -r ./requirements.txt

# Add project configuration
WORKDIR /config
COPY    /config .

# Make print() to always flush immediately
ENV     PYTHONUNBUFFERED=1
