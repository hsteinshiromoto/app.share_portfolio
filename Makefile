# ---
# Define Variables
# ---

# Define container image
user_name=hsteinshiromoto
repo_path=$(shell git rev-parse --show-toplevel)
repo_name=$(shell basename $(repo_path))
tag = latest

registry=registry.gitlab.com

docker_image=${registry}/${user_name}/${repo_name}:${tag}

build_date=$(shell date +%Y%m%d-%H:%M:%S)

# Set up env to be used in the container build phase
#include .env
#export $(shell sed 's/=.*//' .env)

# ---
# Commands
# ---

###
buildapp:
	docker build  \
	  	   --build-arg BASE_IMAGE=3.7-slim-stretch \
	  	   --build-arg FILES=. \
		   --build-arg REPO_NAME=${repo_name} \
		   -f app/app.Dockerfile \
		   -t ${registry}/${user_name}/${repo_name}_app:${tag} .

## Build container locally
buildlocal:
	@echo "Building docker image $(docker_image)"
	docker build --build-arg BUILD_DATE=$(build_date) \
		   --build-arg REPO_NAME=$(repo_name) \
		   --build-arg DOCKER_IMAGE=$(docker_image) \
		   --build-arg REGISTRY=$(registry) \
		   --build-arg FILES="requirements.txt" \
		   -t $(docker_image) .

## Build container
build:
	@echo "Building docker image $(docker_image)"
	docker build --build-arg BUILD_DATE=$(build_date) \
		   --build-arg REPO_NAME=$(repo_name) \
		   --build-arg DOCKER_IMAGE=$(docker_image) \
		   --build-arg REGISTRY=$(registry) \
		   --build-arg FILES=. \
		   -t $(docker_image) .

## Compose containers
buildcompose:
	@echo "Composing containers"
	docker-compose build --build-arg BUILD_DATE=$(build_date) \
		   --build-arg REPO_NAME=$(repo_name) \
		   --build-arg DOCKER_IMAGE=$(docker_image) \
		   --build-arg REGISTRY=$(registry) \
		   --build-arg FILES=. app

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

# ---
# Self Documenting Commands
# ---

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')


.PHONY: build_gitlab, buildlocal