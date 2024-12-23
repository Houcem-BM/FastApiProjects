# Use a base image with Python installed
FROM python:3.9-slim

# Install system dependencies and libraries required for pycaret and other packages
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    libatlas-base-dev \
    libssl-dev \
    supervisor \
    apache2 \
    libapache2-mod-wsgi-py3 && \
    apt-get clean

# Copy the web files to the Apache root directory
COPY AI+api.html /var/www/html/AI+api.html
COPY AI+api.css /var/www/html/AI+api.css
COPY AI+api.js /var/www/html/AI+api.js

# Copy the FastAPI app and dependencies
WORKDIR /app
COPY AI+api.py /app/AI+api.py
COPY bestModel.pkl /app/bestModel.pkl
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Configure Apache to reverse proxy requests to FastAPI
RUN echo '<VirtualHost *:80>\n\
    DocumentRoot /var/www/html\n\
    ProxyPass /api http://127.0.0.1:8000/\n\
    ProxyPassReverse /api http://127.0.0.1:8000/\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Enable necessary Apache modules
RUN a2enmod proxy proxy_http

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create the necessary log directory for Uvicorn
RUN mkdir -p /var/log/uvicorn

# Expose the port for Apache
EXPOSE 80

# Start the supervisor to manage both Apache and FastAPI
CMD ["/usr/bin/supervisord"]
