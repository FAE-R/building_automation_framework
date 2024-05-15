FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV APP_HOME=/home/mqtt_client

RUN apt-get update

WORKDIR $APP_HOME

COPY /mqtt_client.py ./mqtt_client.py
COPY /settings.py ./settings.py

COPY /requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=settings
