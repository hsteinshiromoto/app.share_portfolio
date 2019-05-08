#!/bin/sh

user_name=hsteinshiromoto
repo_name=$(git rev-parse --show-toplevel)
repo_name=$(basename ${repo_name})
registry=registry.gitlab.com
tag=latest

RED='\033[1;31m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
NC='\033[0m'

# Host folders
h_folder_code=$(pwd)

# Docker folders
d_folder_code=/home/${repo_name}


if [ -z "$1" ]
then
	docker_image=${registry}/${user_name}/${repo_name}:${tag}

else
	docker_image=$1

fi

container_id=$(docker ps -qf "ancestor=${docker_image}")

if [ -z "$container_id" ]
then
	echo "Creating container from image ${docker_image}"
	docker run -d -P -v ${h_folder_code}:${d_folder_code} -t ${docker_image}
	container_id=$(docker ps -qf "ancestor=${docker_image}")

else
	echo "Container already running"

fi
	
port1=$(docker ps -f "ancestor=${docker_image}" | grep -o "0.0.0.0:[0-9]*->[0-9]*" | cut -d ":" -f 2 | head -n 1)
port2=$(docker ps -f "ancestor=${docker_image}" | grep -o "0.0.0.0:[0-9]*->[0-9]*" | cut -d ":" -f 2 | sed -n 2p)
token=$(docker logs ${container_id} | tac | grep -o "token=[a-z0-9]*" | sed -n 1p | cut -d "=" -f 2)

echo "Container ID: ${RED}${container_id}${NC}"
echo "Port mappings: ${BLUE}${port1}, ${port2}${NC}"
echo "Jupyter token: ${GREEN}${token}${NC}"
