import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_backend.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Admin user created (username: admin, password: admin123)')
else:
    print('✓ Admin user already exists')
