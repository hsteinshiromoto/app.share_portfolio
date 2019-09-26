#!/bin/bash

# ---
# Documentation
# ---

display_help() {
    echo "Usage: [variable=value] $0" >&2
    echo
    echo "   -h, --help                 display help"
    echo "   -j, --jupyter_notebook     launch container with jupyter notebook"
    echo
    # echo some stuff here for the -a or --add-options
    exit 1
}

jupyter() {
    echo "Starting Jupyter Notebook"
    DOCKER_TAG=jupyter
}

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
# Get Variables From make_variables.sh
# ---
IFS='|| ' read -r -a array <<< $(./make_variables.sh)

DOCKER_IMAGE=${array[0]}
PROJECT_NAME=${array[1]}
DOCKER_TAG="${DOCKER_TAG:-latest}"
DOCKER_IMAGE_TAG=${DOCKER_IMAGE}:${DOCKER_TAG}

CONTAINER_ID=$(docker ps | grep "${DOCKER_IMAGE_TAG}" | awk '{ print $1}')

RED="\033[1;31m"
BLUE='\033[1;34m'
GREEN='\033[1;32m'
NC='\033[0m'


if [[ -z "${CONTAINER_ID}" ]]; then
	echo "Creating Container from Image ${DOCKER_IMAGE_TAG}"
	docker run -d -P -v $(pwd):/home/${PROJECT_NAME} -t ${DOCKER_IMAGE_TAG}
	CONTAINER_ID=$(docker ps | grep "${DOCKER_IMAGE_TAG}" | awk '{ print $1}')

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

# Need to change permissions on folder $user/.local/share/jupyter for user app.share_portfolio
# before starting Jupyter server
docker exec -u root -i ${container_id} sh -c "chown -R ${repo_name}:${repo_name} /home/${repo_name}/.local/share/jupyter"
echo "Starting Jupyter server ..."
docker exec -d -i ${container_id} sh -c "jupyter notebook --no-browser --ip=0.0.0.0 --port=8888"
echo "Done"
	
port1=$(docker ps -f "ancestor=${docker_image}" | grep -o "0.0.0.0:[0-9]*->[0-9]*" | cut -d ":" -f 2 | head -n 1)
port2=$(docker ps -f "ancestor=${docker_image}" | grep -o "0.0.0.0:[0-9]*->[0-9]*" | cut -d ":" -f 2 | sed -n 2p)
token=$(docker exec -i ${container_id} sh -c "jupyter notebook list" | tac | grep -o "token=[a-z0-9]*" | sed -n 1p | cut -d "=" -f 2)

echo "Container ID: ${RED}${container_id}${NC}"
echo "Port mappings: ${BLUE}${port1}, ${port2}${NC}"
echo "Jupyter token: ${GREEN}${token}${NC}"
