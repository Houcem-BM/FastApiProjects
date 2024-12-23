# Use a lightweight web server base image
FROM nginx:alpine

# Copy website files to the default NGINX HTML directory
COPY RUSTAPI.html /usr/share/nginx/html/index.html
COPY RUSTAPI.css /usr/share/nginx/html/
COPY RUSTAPI.js /usr/share/nginx/html/

# Expose port 80 for serving the website
EXPOSE 80
