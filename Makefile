default: build

docker_user=hsteinshiromoto
repo_path=$(shell git rev-parse --show-toplevel)
repo_name=$(shell basename $(repo_path))
tag = latest

docker_image = $(docker_user)/$(repo_name):$(tag)

build_date=$(shell date +%Y%m%d-%H:%M:%S)

build:
	@echo "Building docker image $(docker_image) for repository $(repo_name)"
	docker build --build-arg BUILD_DATE=$(build_date) --build-arg REPO_NAME=$(repo_name) -t $(docker_image)  . 

build_gitlab:
	@echo "Building docker image $(git_lab_registry)/$(docker_user)/$(repo_name):$(tag)"
	docker build --build-arg BUILD_DATE=$(build_date) --build-arg REPO_NAME=$(repo_name) -t $(git_lab_registry)/$(docker_user)/$(repo_name):$(tag) . 

.PHONY: build