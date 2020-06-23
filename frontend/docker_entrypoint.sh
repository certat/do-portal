#!/bin/sh

{

set -e

cd /home/cert/customer-portal

npm install

npx bower install

if [ ! -f config/envs/devel.json ]; then
  echo 'create docker devel config'
  cp config/envs/docker.json config/envs/devel.json
else
  if ! cmp --silent config/envs/devel.json config/envs/docker.json
  then
    echo 'Warning: config/envs/devel.json differs from config/envs/docker.json!'
  fi
fi

if [ ! -f config/envs/production.json ]; then
  echo 'create docker production config'
  cp config/envs/docker.json config/envs/production.json
else
  if ! cmp --silent config/envs/production.json config/envs/docker.json
  then
    echo 'Warning: config/envs/production.json differs from config/envs/docker.json!'
  fi
fi

if [ ! -f secret.json ]; then
    echo 'create secret.json.'
    cp secret.json.example secret.json
fi

npx grunt serve

} >&2 # redirect stout to stderr
