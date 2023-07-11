# Use the official Python base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y --fix-missing

# Copy the Django project code to the container
COPY . /app/

# Expose the port your Django app runs on
EXPOSE 8000

# Define the command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
