FROM python:3.7-slim-stretch

# --- 
# Build arguments
# ---
ARG BUILD_DATE
ARG REPO_NAME
ARG DOCKER_IMAGE
ARG REGISTRY

# Silence debconf
ARG DEBIAN_FRONTEND=noninteractive

# ---
# Enviroment variables
# ---
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
ENV TINI_VERSION v0.6.0
ENV PROJECT_ROOT /home/$REPO_NAME
ENV PYTHONPATH $PROJECT_ROOT
ENV DOCKER_IMAGE $DOCKER_IMAGE
ENV REGISTRY $REGISTRY

ENV TZ=Australia/Sydney

# Set container time zone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

LABEL org.label-schema.build-date=$BUILD_DATE \
      maintainer="Dr Humberto STEIN SHIROMOTO <h.stein.shiromoto@gmail.com>"

# ---
# Set up the necessary Debian packages
# ---

# Install git
RUN apt update && apt install -y git procps

# Create the "home" folder 
RUN mkdir -p $PROJECT_ROOT

# ---
# Set up the necessary Python packages
# ---
COPY requirements.txt $PROJECT_ROOT
RUN pip install --upgrade pip && pip install -r $PROJECT_ROOT/requirements.txt

# ---
# Set up jupyter notebook extensions
# ---
RUN jupyter contrib nbextension install --system && \
	jupyter nbextensions_configurator enable --system

# ---
# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
# ---

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# ---
# Setup User
# ---

RUN useradd --create-home -s /bin/bash $REPO_NAME
USER $REPO_NAME

# ---
# Setup container ports and start Jupyter server
# ---
EXPOSE 8888
CMD ["jupyter", "notebook", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--port=8888"]


# Expose Ports
EXPOSE 5000
CMD python3 ${PROJECT_ROOT}/app/app.py

WORKDIR $PROJECT_ROOT