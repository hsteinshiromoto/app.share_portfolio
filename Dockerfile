ARG DOCKER_PARENT_IMAGE="python:3.7-slim-stretch"
FROM $DOCKER_PARENT_IMAGE

# --- 
# Build arguments
# ---
ARG BUILD_DATE
ARG DOCKER_IMAGE
ARG FILES=""
ARG PROJECT_NAME

# Silence debconf
ARG DEBIAN_FRONTEND=noninteractive

# ---
# Enviroment variables
# ---
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

ENV PROJECT_ROOT /home/$PROJECT_NAME
ENV PYTHONPATH $PROJECT_ROOT

ENV TZ=Australia/Sydney

# Set container time zone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

LABEL org.label-schema.build-date=$BUILD_DATE \
      maintainer="Dr Humberto STEIN SHIROMOTO <h.stein.shiromoto@gmail.com>"

# ---
# Copy Necessary Files
# ---
COPY debian-requirements.txt /usr/local/debian-requirements.txt
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY run_python.sh /usr/local/bin/run_python.sh
COPY test_environment.py /usr/local/bin/test_environment.py
COPY setup.py /usr/local/bin/setup.py
COPY requirements.txt /usr/local/requirements.txt
COPY $FILES $PROJECT_ROOT/

RUN chmod +x /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/run_python.sh && \
	chmod +x /usr/local/bin/test_environment.py && \
	chmod +x /usr/local/bin/setup.py

# ---
# Set up the necessary Debian packages
# ---
RUN apt-get update && \
	DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" /usr/local/debian-requirements.txt) && \
    apt-get install -y $DEBIAN_PACKAGES && \
    apt-get clean

# ---
# Set up the necessary Python packages
# ---
RUN bash /usr/local/bin/run_python.sh -t && \
	bash /usr/local/bin/run_python.sh -r

# Create the "home" folder 
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]