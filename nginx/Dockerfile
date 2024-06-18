FROM nginx:latest
RUN mkdir /home/ba_framework
RUN mkdir /home/ba_framework/static
RUN mkdir /home/ba_framework/certs
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY /certs /home/ba_framework/certs
WORKDIR /home/ba_framework
