#!/bin/bash
set -e

# If "-e uid={custom/local user id}" flag is not set for "docker run" command, use 9999 as default
CURRENT_UID=${uid:-9999}
DOCKER_USER=${DOCKER_USER:-docker_user}

# Create user called "docker" with selected UID
useradd --shell /bin/bash -u $CURRENT_UID -o -c "" -m $DOCKER_USER

# Execute process
exec gosu $DOCKER_USER "$@"