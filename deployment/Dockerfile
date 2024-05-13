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

# Expose PostgreSQL port
EXPOSE 5432

# Start PostgreSQL service
CMD ["service", "postgresql", "start"]

# Set up pipenv environment (replace with your own setup commands)
RUN git clone https://github.com/EPIC-Recommender/EPIC-Recommender.git
WORKDIR /EPIC-Recommender
RUN git checkout docker
#COPY Pipfile Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile

# Optionally, you can add a command to run your application or shell
# CMD ["python", "app.py"]

