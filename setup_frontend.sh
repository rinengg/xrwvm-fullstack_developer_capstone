#!/bin/bash
set -e

cd /home/project/xrwvm-fullstack_developer_capstone

# Pull latest changes
git pull

# Build React frontend (outputs to server/frontend/build/)
cd server/frontend
npm install
npm run build

# Run Django migrations and collect static files
cd ..
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# Create root superuser if it doesn't exist
python3 manage.py shell -c "
from django.contrib.auth import get_user_model
U = get_user_model()
if not U.objects.filter(username='root').exists():
    U.objects.create_superuser('root', 'root@bestcars.com', 'root123')
    print('root superuser created')
else:
    print('root superuser already exists')
"

# Restart Django
pkill -f "manage.py runserver" 2>/dev/null || true
sleep 1
nohup python3 manage.py runserver 0.0.0.0:8000 > /tmp/django.log 2>&1 &
echo "Django restarted. PID: $!"
echo "Done. React app is built and Django is running."
