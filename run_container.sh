#!/bin/sh

user_name=hsteinshiromoto
# repo_name=$(git rev-parse --show-toplevel)
# repo_name=$(basename ${repo_name})
repo_name=app.share_portfolio
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

docker_image=${registry}/${user_name}/${repo_name}:${tag}

container_id=$(docker ps -qf "ancestor=${docker_image}")

if [ -z "$container_id" ] && [ $1 = "local" ]; then
	echo "Creating container from image ${docker_image}"
	docker run -d -P -v ${h_folder_code}:${d_folder_code} -t ${docker_image}
	container_id=$(docker ps -qf "ancestor=${docker_image}")

elif [ $1 = "deploy" ]
then 
	echo "Found container: ${container_id}"
	docker kill ${container_id}

	echo "Creating container from image ${docker_image}"
	docker run -d -p 80:5000 -v ${h_folder_code}:${d_folder_code} -t ${docker_image}
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
