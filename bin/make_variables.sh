#!/bin/bash

# ---
# Documentation
# ---

display_help() {
    echo "Usage: [variable=value] $0 ./script.sh" >&2
    echo
    echo "   -h, --help                 display help"
    echo
    # echo some stuff here for the -a or --add-options
    exit 1
}

while :
do
    case "$1" in
      -h | --help)
          display_help  # Call your function
          exit 0
          ;;

      --) # End of all options
          shift
          break
          ;;
      -*)
          echo "Error: Unknown option: $1" >&2
          ## or call function display_help
          exit 1
          ;;
      *)  # No more options
          break
          ;;
    esac
done

# ---
# Export environ variables defined in .env file:
# ---

set -a # automatically export all variables
source .env
set +a

# Check if variable is defined in .env file
if [[ -z ${REGISTRY_USER} ]]; then
	echo "Error! Variable REGISTRY_USER is not defined" 1>&2
	exit 1

fi

# ---
# Global Variables
# ---

PROJECT_DIR=$(pwd)
PROJECT_NAME=$(basename ${PROJECT_DIR})

REGISTRY=registry.gitlab.com/${REGISTRY_USER}
DOCKER_IMAGE=${REGISTRY}/${PROJECT_NAME}

RED='\033[1;31m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
NC='\033[0m'

echo "${DOCKER_IMAGE}||${PROJECT_NAME}"