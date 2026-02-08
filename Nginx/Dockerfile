FROM ubuntu:latest

# Install nginx + openssl for self signed cert
RUN apt-get update -y && apt-get install nginx openssl -y

# Copy the nginx configuration from the nginx folder
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/www/html
COPY index.html /var/www/html/index.html

# Generate self signed cert for HTTPS
RUN mkdir -p /etc/nginx/certs \
  && openssl req -x509 -nodes -days 365 \
     -newkey rsa:2048 \
     -keyout /etc/nginx/certs/selfsigned.key \
     -out /etc/nginx/certs/selfsigned.crt \
     -subj "/C=US/ST=NA/L=NA/O=Dev/OU=Dev/CN=localhost" \
  # Removes the openssl after generating the cert for reducing image size
  && apt-get purge -y openssl \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*


EXPOSE 8080 8081 

CMD ["nginx", "-g", "daemon off;"]