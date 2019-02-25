default: build

docker_user=hsteinshiromoto
repo_path=$(shell git rev-parse --show-toplevel)
repo_name=$(shell basename $(repo_path))
tag = latest

docker_image = $(docker_user)/$(repo_name):$(tag)

build_date=$(shell date +%Y%m%d-%H:%M:%S)

build:
	@echo "Building Container $(docker_image)"
	docker build --build-arg BUILD_DATE=$(build_date) -t $(docker_image)  . 

.PHONY: build