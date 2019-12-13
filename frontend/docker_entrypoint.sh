#!/bin/sh

{

set -e

cd /home/cert/customer-portal

npm install

PATH=$(npm bin):$PATH bower install

cp config/envs/docker.json config/envs/devel.json
cp config/envs/docker.json config/envs/production.json

PATH=$(npm bin):$PATH grunt serve

} >&2 # redirect stout to stderr
