# Use an official Python runtime as a parent image
FROM python:3.12.3-slim-bullseye

# Set environment variables to avoid writing .pyc files and to ensure output is logged
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies needed for Poetry installation
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Disable Poetry's virtual environment creation
RUN poetry config virtualenvs.create false

# Verify Poetry installation
RUN poetry --version

# Copy the poetry configuration file and pyproject.toml
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-dev

# Copy the rest of the application code to the container
COPY . /app/

# Set the Django settings module environment variable
ENV DJANGO_SETTINGS_MODULE=cookai.prod

# Expose port 8000 for the Django application
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
