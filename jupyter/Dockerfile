ARG DOCKER_PARENT_IMAGE
FROM $DOCKER_PARENT_IMAGE

#---
# Run Commands
#---

RUN pip install jupyter jupyter_contrib_nbextensions

RUN jupyter contrib nbextension install --system && \
	jupyter nbextensions_configurator enable --system

EXPOSE 8888
CMD jupyter notebook --ip="0.0.0.0" --port=8888 --no-browser