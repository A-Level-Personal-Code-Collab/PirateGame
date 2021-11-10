#!/bin/bash
# A dedicated script to run before deploying a version of the pirate game.

#Replace all socketio addresses
find app/ -type f -exec sed -i 's/"http://localhost:8001/"/"http://play.pirategame.live/websockets/"/g' {} \;

#Replace all website
find app/ -type f -exec sed -i 's/"http://localhost:8000/"/"http://play.pirategame.live/"/g' {} \;

#Replace all database password data
find app/ -type f -exec sed -i 's/local-only/$(cat /secrets/database)/g' {} \;

#Build dockers
docker stop $(docker container ls -aq)
docker contianer prune -f
docker-compose up -d -f docker-compose.prod.yml --build

#Copy static content
mkdir /var/www
cp -r app/static/ /var/www/

#Copy nginx configuration
cp nginx.conf /etc/nginx/vhosts.d/pirategame.conf
systemctl restart nginx