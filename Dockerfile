# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set the non-interactive frontend to avoid user prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce && \
    rm -rf /var/lib/apt/lists/*

# Get Docker version and set as environment variable
RUN docker --version | awk '{print $3}' | sed 's/,//' > /docker_version.txt

# Default command to keep the container running
CMD ["tail", "-f", "/dev/null"]
