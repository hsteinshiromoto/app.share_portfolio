FROM hsteinshiromoto/docker.datascience:latest

ARG BUILD_DATE

LABEL org.label-schema.build-date=$BUILD_DATE \
      maintainer="Dr Humberto STEIN SHIROMOTO <h.stein.shiromoto@gmail.com>"

COPY requirements.txt /home

RUN pip install -r requirements.txt

WORKDIR /home