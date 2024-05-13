# Use the official Debian base image
FROM debian:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install PostgreSQL and dependencies
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN apt-get update && apt-get install -y \
    pipenv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#Install git
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies using apt-get
RUN apt-get update && apt-get install -y \
    python3-django \
    python3-psycopg2 \
    python3-django-bootstrap5 \
    python3-pytest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose PostgreSQL and Djangoj
# port
EXPOSE 5432
EXPOSE 8000

# Start PostgreSQL service
CMD ["service", "postgresql", "start"]

# Set up pipenv environment (replace with your own setup commands)
RUN git clone https://github.com/EPIC-Recommender/EPIC-Recommender.git
WORKDIR /EPIC-Recommender
#TODO: dont forget remove the bellow line for production
RUN git checkout docker
#COPY Pipfile Pipfile.lock

# Optionally, you can add a command to run your application or shell
# CMD ["python", "app.py"]

