# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install sudo
RUN apt-get update && apt-get install -y sudo

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Ansible via pip
RUN pip install --no-cache-dir ansible
# Install Docker client
RUN apt-get update && apt-get install -y docker.io

# Copy the Ansible related files into the container at /usr/src/app
COPY . .
# Give rights to execute
RUN chmod +x ./run_playbooks.sh

# Run Ansible playbooks using CMD instruction
CMD ["bash","run_playbooks.sh"]
