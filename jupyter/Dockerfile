ARG DOCKER_PARENT_IMAGE="python:3.7-slim-stretch"
FROM $DOCKER_PARENT_IMAGE

ENV TINI_VERSION v0.6.0

# ---
# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
# ---

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
RUN ["/usr/bin/tini", "--"]

RUN pip install --upgrade pip && pip install jupyter jupyter jupyter_contrib_nbextensions

RUN jupyter contrib nbextension install --system && \
	jupyter nbextensions_configurator enable --system

CMD jupyter -m notebook