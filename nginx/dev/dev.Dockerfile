FROM nginx:latest
RUN mkdir /home/hitl_ba_framework
RUN mkdir /home/hitl_ba_framework/static
RUN mkdir /home/hitl_ba_framework/certs
COPY dev.nginx.conf /etc/nginx/conf.d/default.conf
WORKDIR /home/hitl_ba_framework
