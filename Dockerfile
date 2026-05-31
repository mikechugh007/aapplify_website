# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /irobotdocker

# Install dependencies

# Copy project files to the container
COPY . /irobotdocker/

COPY requirements.txt /irobotdocker/
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install django-browser-reload && pip install sorl-thumbnail
RUN python manage.py makemigrations authentication && python manage.py migrate

# Expose the port Django runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
