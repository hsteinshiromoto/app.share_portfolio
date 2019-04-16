#!/usr/bin/env bash
# !/bin/bash

repo_name=$(git rev-parse --show-toplevel)
repo_name=$(basename ${repo_name})
docker_image=hsteinshiromoto/${repo_name}:latest

# Host folders

h_folder_code=${PWD}

# Docker folders

d_folder_code=/home/${repo_name}


container_id=$(docker ps -qf "ancestor=${docker_image}")

if [[ $1 = 'clean' ]];
then

    docker container prune

elif [[ $1 = "bokeh" ]]
then

    bokeh_port=$(docker ps -f "ancestor=${docker_image}" | grep -o "0.0.0.0:[0-9]*->5000*" | cut -d ":" -f 2 | cut -d "-" -f 1 |head -n 1)
    docker exec -i ${container_id} \
           bash -c "bokeh serve app/app.py --port 5000 --address '0.0.0.0' --allow-websocket-origin=0.0.0.0:${bokeh_port}"

else
    if [[ -z "$container_id" ]];
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

    # port=$(docker inspect ${container_id} | grep '"HostPort":' | sed -e 's/ *"HostPort": "\(\w\+\)"/\1/')
    port1=$(docker ps -f "ancestor=${docker_image}" | grep -o "0.0.0.0:[0-9]*->[0-9]*" | cut -d ":" -f 2 | head -n 1)
    port2=$(docker ps -f "ancestor=${docker_image}" | grep -o "0.0.0.0:[0-9]*->[0-9]*" | cut -d ":" -f 2 | sed -n 2p)
    token=$(./get_jupyter_token.sh)

    echo -e "\tContainer ID: ${container_id}"
    echo -e "\tPort mappings:\t${port1}, ${port2}"
    echo -e "\tJupyter token: ${token}\n"
fi