FROM nginx:alpine

RUN apk add --no-cache openssl

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/ssl/localcerts /etc/nginx/logs

COPY linkapp.key /etc/ssl/localcerts/linkapp.key
COPY linkapp.pem /etc/ssl/localcerts/linkapp.pem
COPY conf /etc/nginx