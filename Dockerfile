
FROM python:3.9
ENV DockerHOME=/home/app/pbp_project

RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $DockerHOME
RUN pip install -r requirements.txt
WORKDIR $DockerHOME/pbp_project
