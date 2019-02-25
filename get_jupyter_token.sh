#!/bin/bash

repo_name=$(git rev-parse --show-toplevel)
repo_name=$(basename ${repo_name})
docker_image=hsteinshiromoto/${repo_name}:latest

container_id=$(docker ps -lq -f "ancestor=${docker_image}" -f status=running)

if [[ -z "${container_id}" ]]; then
    echo "No container for ${image_name} is currently running."
else
    token=$(docker logs ${container_id} 2>&1 | tac | grep "^ \+http:\/\/.*\?token" | head -n1 | sed -e 's/.*\?token=\(\w\+\)/\1/')
fi

echo ${token}
