FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=password123
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_FIRST_NAME=Admin
ENV DJANGO_SUPERUSER_LAST_NAME=User

# Set a working directory for the app
WORKDIR /app

# Copy the requirements file into the container and install the dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Copy modified backends.py file to image
COPY ./backward_dependencies/backends.py /usr/local/lib/python3.6/site-packages/rest_framework_simplejwt/backends.py


# Run any Django migrations required
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py createsuperuser --noinput

# First Normal User
RUN echo "from django.contrib.auth.models import User; User.objects.create_user('testuser1', 'testuser1@example.com', 'password')" | python manage.py shell


# First Normal User
RUN echo "from django.contrib.auth.models import User; User.objects.create_user('testuser2', 'testuser2@example.com', 'password')" | python manage.py shell

# Expose the port that the app should run on (this should match the port specified in the Django settings)
EXPOSE 8000

# Start the Django development server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]