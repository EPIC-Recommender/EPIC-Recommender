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
    gunicorn \
    nginx \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose PostgreSQL and Django ports
EXPOSE 5432
EXPOSE 80

USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "ALTER USER postgres PASSWORD 'root';" && \
    createdb EpicDB


# Switch back to root user to perform further operations
USER root

# Start PostgreSQL service
# (Note: Starting services via systemd isn't straightforward in Docker; it's better handled externally)
RUN service postgresql start && su - postgres -c 'psql -c "CREATE DATABASE EpicDB;"'


COPY . EPIC-Recommender/
WORKDIR /EPIC-Recommender
COPY DBconnection-deployment.py DBconnection.py

RUN service postgresql start && \
    su - postgres -c "psql -d EpicDB -f /EPIC-Recommender/DBcreation.sql" && \
    su - postgres -c "psql -d EpicDB -f /EPIC-Recommender/DBfunctions.sql"

# Prepare virtual environment and install Python dependencies
RUN python3 -m venv venv
RUN . venv/bin/activate && pip3 install -r requirements.txt
RUN . venv/bin/activate && pip3 install gunicorn

#fill the database with the movies and other data
RUN service postgresql start && \
    . venv/bin/activate && python3 jsonToDB.py

RUN service postgresql start && . venv/bin/activate && python3 manage.py migrate

COPY nginx.conf /etc/nginx/nginx.conf
RUN chmod +x start.sh

CMD ["./start.sh"]
