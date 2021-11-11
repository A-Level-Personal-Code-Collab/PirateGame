#!/bin/bash
# A dedicated script to run before deploying a version of the pirate game.

#Replace all socketio addresses
grep -RiIl 'http://localhost:8001/' | xargs sed -i 's/"http://localhost:8001/"/"http://play.pirategame.live/websockets/"/g'

#Replace all website
grep -RiIl 'http://localhost:8000/' | xargs sed -i 's/"http://localhost:8000/"/"http://play.pirategame.live/"/g'

#Replace all database password data
grep -RiIl 'local-only' | xargs sed -i 's/local-only/$(cat /secrets/database)/g'

#Build dockers
docker-compose -f docker-compose.prod.yml up -d --build

#Copy static content
mkdir /var/www
cp -r app/static/ /var/www/

#Copy nginx configuration
cp nginx.conf /etc/nginx/vhosts.d/pirategame.conf
systemctl restart nginx