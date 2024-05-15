FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV APP_HOME=/home/dwd

RUN apt-get update

WORKDIR $APP_HOME

COPY /core.py ./core.py
COPY /settings.py ./settings.py

COPY /requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=settings
