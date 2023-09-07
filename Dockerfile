FROM python:3.9

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE user_auth.settings

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project files into the container at /app
COPY . /app/