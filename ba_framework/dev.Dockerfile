FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV APP_HOME=/home/ba_framework

WORKDIR $APP_HOME

RUN apt-get update

COPY /requirements.txt ./requirements.txt
COPY /entrypoint.sh ./entrypoint.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./static
RUN mkdir ./certs

ENV DJANGO_SETTINGS_MODULE=ba_framework.settings

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "dev_entrypoint.sh"]
