FROM ubuntu:noble-20250529

RUN apt update \
 && apt install -y \
    software-properties-common \
 && add-apt-repository ppa:deadsnakes/ppa \
 && apt update \
 && apt install -y \
    build-essential \
    python3.13 \
    python3.13-venv \
    python3-pip \
    nginx \
    supervisor \
 && rm -rf /var/lib/apt/lists/*

# Copy the application code to /app
COPY . /app
WORKDIR /app
# Install Python dependencies
RUN python3.13 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python3.13 -m pip install --no-cache-dir -r requirements.txt

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY gradio.conf /etc/nginx/sites-available/default
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Configure Supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Create a directory for logs
RUN mkdir -p /var/log/supervisor

# Expose the port that Nginx will listen on
EXPOSE 80

# Use supervisord to start all services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
