# Use the official Python 3.10 image from the Docker Hub
FROM python:3.10

# Set environment variables to ensure the Python output is sent straight to the terminal (standard output)
ENV PYTHONUNBUFFERED 1
# Prevent Python from writing .pyc files to disk (no bytecode files)
ENV PYTHONDONTWRITEBYTECODE 1
# Set an environment variable for the application home directory
ENV APP_HOME=/home/ba_framework

# Set the working directory inside the container to the application home directory
WORKDIR $APP_HOME

# Update the package lists for APT (the package manager for Debian-based distributions)
RUN apt-get update

# Copy the requirements.txt file from the local machine to the working directory in the container
COPY /requirements.txt ./requirements.txt
# Copy the entrypoint.sh script from the local machine to the working directory in the container
COPY /entrypoint.sh ./entrypoint.sh

# Upgrade pip to the latest version
RUN pip install --upgrade pip
# Install the Python dependencies listed in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory named "static" in the working directory
RUN mkdir ./static
# Create a directory named "certs" in the working directory
RUN mkdir ./certs

# Set an environment variable for the Django settings module
ENV DJANGO_SETTINGS_MODULE=ba_framework.settings

# Make the entrypoint.sh script executable
RUN chmod +x ./entrypoint.sh
# Set the entrypoint for the container to the entrypoint.sh script
ENTRYPOINT ["sh", "entrypoint.sh"]
