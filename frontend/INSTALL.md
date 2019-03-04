# Installation / Upgrade procedure

## Install dependencies

Needs proxy:

npm install
npm install grunt-cli
npm install bower
./node_modules/.bin/bower install

## Configuration

copy secret.json from other installation if not exists
Maybe names did change, check Gruntfile.js and secret.json for compatibility (ununderstandable errors with popup anyway at the grunt call)

## Build
./node_modules/.bin/grunt

Static files will be in `dist/` then.
