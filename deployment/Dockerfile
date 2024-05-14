# Use the official Debian base image
FROM debian:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    postgresql-client \
    git \
    python3 \
    python3-pip \
    python3-venv \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose PostgreSQL and Django ports
EXPOSE 5432
EXPOSE 8000

# Start PostgreSQL service
# (Note: Starting services via systemd isn't straightforward in Docker; it's better handled externally)
RUN service postgresql start && su - postgres -c 'psql -c "CREATE DATABASE EpicDB;"'

# Clone repository and install Python dependencies
RUN git clone https://github.com/EPIC-Recommender/EPIC-Recommender.git
WORKDIR /EPIC-Recommender
RUN git checkout docker
COPY requirements.txt requirements.txt
COPY DBconnection-deployment.py DBconnection.py

# Prepare virtual environment and install Python dependencies
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

# Optionally, you can create database, users, and tables here
# Example:
#RUN . venv/bin/activate && python3 manage.py migrate

# Optionally, you can add commands to initialize the database, create users, etc.

# Optionally, you can add a command to run your application
# CMD ["python", "app.py"]

