# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /usr/src/app/
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY jsonapi/ /usr/src/app/