#!/bin/sh

{

set -e

cd /home/cert/customer-portal

npm install

PATH=$(npm bin):$PATH bower install

echo 'create config/envs/devel.json.'
cp config/envs/docker.json config/envs/devel.json

echo 'create config/envs/production.json.'
cp config/envs/docker.json config/envs/production.json

if [ ! -f secret.json ]; then
    echo 'create secret.json.'
    cp secret.json.example secret.json
fi

PATH=$(npm bin):$PATH grunt serve

} >&2 # redirect stout to stderr
