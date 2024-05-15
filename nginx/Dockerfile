FROM nginx:latest
RUN mkdir /home/hitl_ba_framework
RUN mkdir /home/hitl_ba_framework/static
RUN mkdir /home/hitl_ba_framework/certs
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY /certs /home/hitl_ba_framework/certs
WORKDIR /home/hitl_ba_framework
