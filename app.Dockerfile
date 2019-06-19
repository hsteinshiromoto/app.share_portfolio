
ARG FILES
ARG REPO_NAME
ARG BASE_IMAGE

FROM python:$BASE_IMAGE

ENV PROJECT_ROOT /home/$REPO_NAME

COPY $FILES $PROJECT_ROOT
RUN pip install --upgrade pip && pip install pandas flask bokeh

EXPOSE 5000

CMD python3 ${PROJECT_ROOT}/app/app.py

WORKDIR $PROJECT_ROOT