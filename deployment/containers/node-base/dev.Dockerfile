# Base image for all Node-based components (development mode)
# --
FROM    node:18

# Update the image first (and install some helpful tools)
RUN     apt-get update \
&&      apt-get -y upgrade \
&&      apt-get -y install nano vim

# Some useful macros
RUN     echo 'alias ll="ls -la"' >> ~/.bashrc \
&&      echo 'alias build="npm run build"' >> ~/.bashrc

# Add project configuration
WORKDIR /config
COPY    /config .
