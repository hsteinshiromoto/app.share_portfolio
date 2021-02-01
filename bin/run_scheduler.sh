#!/bin/sh

user_name=hsteinshiromoto
# repo_name=$(git rev-parse --show-toplevel)
# repo_name=$(basename ${repo_name})
repo_name=app.share_portfolio
registry=registry.gitlab.com
tag=latest
docker_image=${registry}/${user_name}/${repo_name}:${tag}
container_id=$(docker ps -qf "ancestor=${docker_image}")

echo "Activating cron ..."
docker exec -u root -i ${container_id} sh -c "cron"
echo "Done"

echo "Adding tasks to crontab ..."
docker exec -u root -i ${container_id} sh -c "chmod +x /home/app.share_portfolio/src/main.py"
docker exec -i ${container_id} sh -c "cat schedule | crontab -"
echo "Done"