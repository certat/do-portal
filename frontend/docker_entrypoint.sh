#!/bin/sh

{

set -e

cd /home/cert/customer-portal

npm install

npx bower install

echo 'create config/envs/devel.json.'
cp config/envs/docker.json config/envs/devel.json

echo 'create config/envs/production.json.'
cp config/envs/docker.json config/envs/production.json

if [ ! -f secret.json ]; then
    echo 'create secret.json.'
    cp secret.json.example secret.json
fi

npx grunt serve

} >&2 # redirect stout to stderr
