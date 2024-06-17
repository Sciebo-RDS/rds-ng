# Base image for all Node-based components
# --
FROM    node:20

# Update the image first
RUN     apt-get update \
&&      apt-get -y upgrade

# Add project configuration
WORKDIR /config
COPY    /config .
