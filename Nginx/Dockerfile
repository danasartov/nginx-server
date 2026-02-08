FROM ubuntu:latest

# Install nginx
RUN apt-get update -y && apt-get install nginx -y

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/www/html
COPY index.html /var/www/html/index.html

EXPOSE 8080 8081

CMD ["nginx", "-g", "daemon off;"]