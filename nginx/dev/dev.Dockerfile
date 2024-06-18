FROM nginx:latest
RUN mkdir /home/ba_framework
RUN mkdir /home/ba_framework/static
RUN mkdir /home/ba_framework/certs
COPY dev.nginx.conf /etc/nginx/conf.d/default.conf
WORKDIR /home/ba_framework
