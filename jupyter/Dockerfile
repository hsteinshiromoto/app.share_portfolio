ARG DOCKER_PARENT_IMAGE
FROM $DOCKER_PARENT_IMAGE

# ---
# Enviroment variables
# ---
ENV TINI_VERSION v0.6.0

# ---
# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
# ---

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
RUN ["/usr/bin/tini", "--"]

RUN pip install jupyter jupyter_contrib_nbextensions

RUN jupyter contrib nbextension install --system && \
	jupyter nbextensions_configurator enable --system

EXPOSE 8888
CMD jupyter notebook --ip="0.0.0.0" --port=8888 --no-browser