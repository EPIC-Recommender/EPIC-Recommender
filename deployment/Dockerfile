# Use the official Debian base image
FROM debian:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install PostgreSQL and dependencies
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install git
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Expose PostgreSQL and Django ports
EXPOSE 5432
EXPOSE 8000

# Start PostgreSQL service
RUN service postgresql start && su - postgres -c 'psql -c "CREATE DATABASE EpicDB;"' \

# Clone repository and install Python dependencies
RUN git clone https://github.com/EPIC-Recommender/EPIC-Recommender.git
WORKDIR /EPIC-Recommender
RUN git checkout docker
COPY requirements.txt requirements.txt
COPY DBconnection-deployment.py DBconnection.py

#prepare database

RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt
#RUN . venv/bin/activate && python3 manage.py migrate
#DBcreation
# Optionally, you can add a command to run your application or shell
# CMD ["python", "app.py"]
CMD service postgresql start
