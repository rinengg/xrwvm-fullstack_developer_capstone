#!/bin/bash
set -e

cd /home/project/xrwvm-fullstack_developer_capstone

# Pull latest changes
git pull

# Build React frontend (outputs to server/frontend/build/)
cd server/frontend
npm install
npm run build

# Collect Django static files
cd ..
python3 manage.py collectstatic --noinput

# Restart Django
pkill -f "manage.py runserver" 2>/dev/null || true
sleep 1
nohup python3 manage.py runserver 0.0.0.0:8000 > /tmp/django.log 2>&1 &
echo "Django restarted. PID: $!"
echo "Done. React app is built and Django is running."
