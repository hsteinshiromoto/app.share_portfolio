SHELL:=/bin/bash
.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

# ---
# Export environ variables defined in .env file:
# ---

include .env
export $(shell sed 's/=.*//' .env)

# Check if variable is set in .env
ifndef REGISTRY_USER
$(error REGISTRY_USER is not set)
endif

# ---
# Arguments
# ---

# Files to be copied in build phase of the container
ifndef FILES
FILES="requirements.txt"
endif

ifndef DOCKER_TAG
DOCKER_TAG=latest
endif

ifndef DOCKER_REGISTRY
DOCKER_REGISTRY=registry.gitlab.com/${REGISTRY_USER}
endif

# ---
# Global Variables
# ---

PROJECT_PATH := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = $(shell basename ${PROJECT_PATH})
DOCKER_IMAGE = ${DOCKER_REGISTRY}/${PROJECT_NAME}

BUILD_DATE = $(shell date +%Y%m%d-%H:%M:%S)

# ---
# Commands
# ---

test:
	@echo "${FILES}"

## Build Container
build:
	$(eval DOCKER_IMAGE_TAG=${DOCKER_IMAGE}:${DOCKER_TAG})

	@echo "Building docker image ${DOCKER_IMAGE_TAG}"
	docker build --build-arg BUILD_DATE=${BUILD_DATE} \
		   		 --build-arg PROJECT_NAME=${PROJECT_NAME} \
		   		 -t ${DOCKER_IMAGE_TAG} .

## Build Jupyter Container
build_jupyter: build
	$(eval DOCKER_PARENT_IMAGE=${DOCKER_IMAGE}:${DOCKER_TAG})
	$(eval DOCKER_TAG=jupyter)
	$(eval DOCKER_IMAGE_TAG=${DOCKER_IMAGE}:${DOCKER_TAG})

	@echo "Building docker image ${DOCKER_IMAGE_TAG}"
	docker build --build-arg DOCKER_PARENT_IMAGE=${DOCKER_PARENT_IMAGE} \
				 --build-arg BUILD_DATE=${BUILD_DATE} \
		   		 --build-arg PROJECT_NAME=${PROJECT_NAME} \
		   		 -f jupyter/Dockerfile \
		   		 -t ${DOCKER_IMAGE_TAG} .

###
buildapp:
	docker build  \
	  	   --build-arg BASE_IMAGE=3.7-slim-stretch \
	  	   --build-arg FILES=. \
		   --build-arg REPO_NAME=${repo_name} \
		   -f app.Dockerfile \
		   -t ${registry}/${user_name}/${repo_name}_app:${tag} app/

## Compose containers
buildcompose:
	@echo "Composing containers"
	docker-compose build --build-arg BUILD_DATE=$(build_date) \
		   --build-arg REPO_NAME=$(repo_name) \
		   --build-arg DOCKER_IMAGE=$(docker_image) \
		   --build-arg REGISTRY=$(registry) \
		   --build-arg FILES=. app

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