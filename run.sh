# !/bin/bash

repo_name=$(git rev-parse --show-toplevel)
repo_name=$(basename ${repo_name})
docker_image=hsteinshiromoto/${repo_name}:latest

# Host folders

h_folder_code=${PWD}

# Docker folders

d_folder_code=/home/${repo_name}


container_id=$(docker ps -qf "ancestor=${docker_image}")

if [ -z "$container_id" ] 
then

	docker tag ${docker_image} ${repo_name}
	echo "Creating container... "
	docker run -d -P -v ${h_folder_code}:${d_folder_code} ${docker_image} 

	sleep 2
    echo "DONE."

	container_id=$(docker ps -qf "ancestor=${docker_image}")

else

	container_id=$(docker ps -qf "ancestor=${docker_image}")
	echo "Container already exists"

fi

port=$(docker inspect ${container_id} | grep '"HostPort":' | sed -e 's/ *"HostPort": "\(\w\+\)"/\1/')
token=$(./get_jupyter_token.sh)

echo -e "\tContainer ID: ${container_id}"
echo -e "\tListening port: ${port}"
echo -e "\tJupyter token: ${token}\n"