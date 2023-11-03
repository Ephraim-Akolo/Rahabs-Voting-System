#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
echo "from django.contrib.auth import get_user_model; import os; User = get_user_model(); True if User.objects.filter(email=f'{os.getenv("DJANGO_SUPERUSER_USERNAME")}') else User.objects.create_superuser(f'{os.getenv("DJANGO_SUPERUSER_USERNAME")}', f'{os.getenv("DJANGO_SUPERUSER_EMAIL")}', f'{os.getenv("DJANGO_SUPERUSER_PASSWORD")}')" | python manage.py shell