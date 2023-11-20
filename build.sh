#!/usr/bin/env bash
# exit on error
set -o errexit

apt update -y && apt install libgl1 -y
pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
echo "from django.contrib.auth import get_user_model; import os; password = os.getenv('DJANGO_SUPERUSER_PASSWORD'); user_name = os.getenv('DJANGO_SUPERUSER_USERNAME'); email = os.getenv('DJANGO_SUPERUSER_EMAIL'); User = get_user_model(); True if User.objects.filter(email=email) else User.objects.create_superuser(user_name, email, password)" | python manage.py shell