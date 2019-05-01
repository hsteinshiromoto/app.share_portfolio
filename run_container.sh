#!/bin/sh

repo_name=$(git rev-parse --show-toplevel)
repo_name=$(basename ${repo_name})
docker_image=hsteinshiromoto/${repo_name}:latest

# Host folders
h_folder_code=$(pwd)

# Docker folders
d_folder_code=/home/${repo_name}

container_id=$(docker ps -qf "ancestor=${docker_image}")

if [ ! -z "$1" ];
then
	docker_image=$1
	echo "Running container from image: ${docker_image}"
	docker run -v ${h_folder_code}:${d_folder_code} -t -d ${docker_image}
	container_id=$(docker ps -qf "ancestor=${docker_image}")
	echo "Running container: ${container_id}"

elif [ -z "$container_id" ]
then
	echo "Running container from image: ${docker_image}"
	docker run -v ${h_folder_code}:${d_folder_code} -t -d ${docker_image}
	container_id=$(docker ps -qf "ancestor=${docker_image}")
	echo "Running container: ${container_id}"

else
	echo "Container already running: ${container_id}"
	docker exec -it ${container_id} /bin/bash

fi