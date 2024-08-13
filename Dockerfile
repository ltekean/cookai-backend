# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye

# Set environment variables to avoid writing .pyc files and to ensure output is logged
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app/

ENV DJANGO_SETTINGS_MODULE=cookai.prod

# Expose port 8000 for the Django application
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
