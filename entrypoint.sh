#!/bin/bash
set -e

# If "-e uid={custom/local user id}" flag is not set for "docker run" command, use 9999 as default
CURRENT_UID=${uid:-9999}
DOCKER_USER=${DOCKER_USER:-docker_user}

if [[ -z "$DOCKER_PASSWORD" ]]; then
    echo "ERROR: DOCKER_PASSWORD is undefined"
    exit 1

else
    # Create user called "docker" with selected UID
    useradd --shell /bin/bash -p $(openssl passwd -1 $DOCKER_PASSWORD) -u $CURRENT_UID -o -c "" -m $DOCKER_USER

fi


if [[ "$1" == "ssh" ]]; then
    apt-get install openssh-server
    service ssh start

fi

# Execute process
exec gosu $DOCKER_USER "$@"