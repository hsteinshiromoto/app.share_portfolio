#!/bin/sh

user_name=hsteinshiromoto
repo_name=$(git rev-parse --show-toplevel)
repo_name=$(basename ${repo_name})
registry=registry.gitlab.com
tag=latest

if [ -z "$1" ]
then
	docker_image=${registry}/${user_name}/${repo_name}:${tag}

else
	docker_image=$1

fi

container_id=$(docker ps -qf "ancestor=${docker_image}")


docker exec -u root -i ${container_id} sh -c "cron"
docker exec -i ${container_id} sh -c "cat schedule | crontab -"