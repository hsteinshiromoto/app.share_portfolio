FROM hsteinshiromoto/docker.datascience:latest

# Get build arguments

ARG BUILD_DATE
ARG REPO_NAME
ARG DOCKER_IMAGE
ARG CI_REGISTRY

# Set enviroment variables
ENV HOME /home/$REPO_NAME
ENV PYTHONPATH $HOME
ENV DOCKER_IMAGE DOCKER_IMAGE
ENV CI_REGISTRY CI_REGISTRY

# Create the "home" folder 
RUN mkdir $HOME

# Copy necessary files
COPY requirements.txt $HOME

#Install requirements from text file
RUN pip install -r $HOME/requirements.txt

# Expose Ports
EXPOSE 5000

LABEL org.label-schema.build-date=$BUILD_DATE \
      maintainer="Dr Humberto STEIN SHIROMOTO <h.stein.shiromoto@gmail.com>"

WORKDIR $HOME