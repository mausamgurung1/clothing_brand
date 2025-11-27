#!/bin/bash

# Exit on error
set -e

echo "Starting entrypoint script..."

# Wait for database to be ready (if using external DB)
echo "Checking database connection..."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if not exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin@gmail.com').exists():
    User.objects.create_superuser('admin@gmail.com', 'admin@gmail.com', 'admin!@#')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Entrypoint script completed successfully!"

# Execute the main command
exec "$@"
