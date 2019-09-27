#!/bin/bash

# ---
# Functions
# ---

# Documentation
display_help() {
    echo "Usage: [variable=value] $0" >&2
    echo
    echo "   -d, --deploy               deploy container"
    echo "   -h, --help                 display help"
    echo "   -j, --jupyter_notebook     launch container with jupyter notebook"
    echo
    # echo some stuff here for the -a or --add-options
    exit 1
}

# Start jupyter server
jupyter() {
    echo "Starting Jupyter Notebook"
    DOCKER_TAG=jupyter
}

# Get container id
get_container_id() {
    echo
    echo "Getting container id for image ${DOCKER_IMAGE_TAG} ..."

    CONTAINER_ID=$(docker ps | grep "${DOCKER_IMAGE_TAG}" | awk '{ print $1}')

    if [[ -z "${CONTAINER_ID}" ]]; then
        echo "No container id found"

    else
        echo "Container id: ${bold}${CONTAINER_ID}${normal}"

    fi
}

# Get container id
deploy_container() {
    echo
    echo "Deploying container ..."
}

# Available options
while :
do
    case "$1" in
      -h | --help)
          display_help  # Call your function
          exit 0
          ;;

      -j | --jupyter_notebook)
          jupyter  # Call your function
          break
          ;;

      -d | --deploy)
          deploy_container  # Call your function
          break
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
# Variables
# ---

# Get Variables From make_variables.sh
IFS='|| ' read -r -a array <<< $(./make_variables.sh)

DOCKER_IMAGE=${array[0]}
PROJECT_NAME=${array[1]}
DOCKER_TAG="${DOCKER_TAG:-latest}"
DOCKER_IMAGE_TAG=${DOCKER_IMAGE}:${DOCKER_TAG}

RED="\033[1;31m"
BLUE='\033[1;34m'
GREEN='\033[1;32m'
NC='\033[0m'
bold=$(tput bold)
normal=$(tput sgr0)

# ---
# Commands
# ---

get_container_id

if [[ -z "${CONTAINER_ID}" ]]; then
	echo "Creating Container from image ${DOCKER_IMAGE_TAG} ..."

	docker run --env-file .env -e DOCKER_USER=$USER -e uid=$UID -d -P -v $(pwd):/home/${PROJECT_NAME} -t ${DOCKER_IMAGE_TAG} >/dev/null >&1

	echo "Done"

elif [ $1 = "deploy" ]
then 
	echo "Found container: ${container_id}"
	docker kill ${container_id}

	echo "Creating container from image ${docker_image}"
	docker run -d -p 80:5000 -t ${docker_image}
	container_id=$(docker ps -qf "ancestor=${docker_image}")

else
	echo "Container already running"

fi

get_container_id

if [[ "${DOCKER_TAG}" == "jupyter" ]]; then
    JUPYTER_PORT=$(docker ps -f "ancestor=${DOCKER_IMAGE_TAG}" | grep -o "0.0.0.0:[0-9]*->8888" | cut -d ":" -f 2 | head -n 1)

    echo -e "Port mapping: ${BLUE}${JUPYTER_PORT}${NC}"

    echo "Getting Jupyter token ..."
    sleep 5
    JUPYTER_TOKEN=$(docker exec -u $(id -u) -i ${CONTAINER_ID} sh -c "jupyter notebook list" | tac | grep -o "token=[a-z0-9]*" | sed -n 1p | cut -d "=" -f 2)
    echo -e "Jupyter token: ${GREEN}${JUPYTER_TOKEN}${NC}"

    JUPYTER_ADDRESS=$(docker ps -f "ancestor=${DOCKER_IMAGE}" | grep -o "0.0.0.0:[0-9]*")
    echo -e "Jupyter Address: ${BLUE}http://${JUPYTER_ADDRESS}/?token=${JUPYTER_TOKEN}${NC}"
fi

port2=$(docker ps -f "ancestor=${docker_image}" | grep -o "0.0.0.0:[0-9]*->[0-9]*" | cut -d ":" -f 2 | sed -n 2p)




