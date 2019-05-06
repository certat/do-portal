# Constituency Portal

This is a web-based application for managing contact information with network information, self-administration and statistics integration.
It is used by CERT.at/GovCERT.at/Austrian Energy CERT to maintain contact information for customers and network owners

## Features

- organization hierarchy
- Contacts always have a specified role, e.g. Administrator, Abuse contact etc.
- automatic import and update of RIPE data
- Contacts can get login access and administrate their own organization
- RIPE-handles can be assigned to organizations, linking Autonomous Systems (AS) and Network blocks (CIDRs) to organizations and (abuse) contacts
- Grafana integration to show statistics on the data from a EventDB for the organization's linked network objects
- Data per contact: PGP key, S/MIME certificate etc.

## Screenshots

TODO

## Related software / tools

### IntelMQ

Can retrieve the abuse contact information from the portal

https://github.com/certtools/intelmq/

### EventDB

A database feeded by IntelMQ is the data source for the event download and for the statistics

### Grafana

Grafana is integrated to provide statistics for the organizations' events

https://grafana.com/

# Installation

apt-get install -y \
   vim less tree ack \
   build-essential git \
   libssl-dev libxml2 libxml2-dev \
   ssdeep exiftool libfuzzy-dev \
   libffi-dev p7zip-full libncurses-dev \
   libxslt-dev lib32z1-dev libpq-dev \
   python3-venv python3-dev python3-pip \
   postgresql-client-9.6 nginx

useradd --create-home --home-dir /home/cert --user-group --shell /bin/bash cert

su - cert

git clone https://github.com/certat/do-portal.git

// backend and frontend config needs to be in sync.
// see frontend/nginx.conf, backend/config.cfg.docker and frontend/config/envs/docker.json

## backend

cd /home/cert/do-portal/backend

// create config file and save as backend/config.cfg

export DO_LOCAL_CONFIG=/home/cert/do-portal/backend/config.cfg

python3 -m venv ~/do-portal

source ./bin/activate

pip install -U pip setuptools

pip install -r requirements.txt

mkdir logs

## database

createdb do_portal;
mv misc/migrations misc/tmp-migrations
python manage.py db init;
python manage.py db migrate;
python manage.py db upgrade;
python manage.py initializedb;
python manage.py insertmasteruser;
python demodata.py addyaml
rm -rf misc/migrations
mv misc/tmp-migrations misc/migrations

psql -U do_portal -c "CREATE SCHEMA fody";
psql -U do_portal -d do_portal --echo-errors --file=install/contactdb_schema_only.pgdump

python manage.py run -h 0.0.0.0 -p 8081

## frontend

cd /home/cert/do-portal/frontend

// create config file and save as config/envs/production.json

npm install

PATH=$(npm bin):$PATH bower install

PATH=$(npm bin):$PATH grunt

//as root

// create nginx config and save as /etc/nginx/sites-available/portal-frontend

ln -s /etc/nginx/sites-available/portal-frontend /etc/nginx/sites-enabled/portal-frontend

/etc/init.d/nginx restart

# Docker

## requirements
 1) install docker
 2) install docker-compose

## installation
git clone https://github.com/certat/do-portal.git

## run portal
docker-compose up

## edit /etc/hosts file

add the following lines

   127.0.0.1       epplication_app
   127.0.0.1       portal-frontend
   127.0.0.1       portal-backend

this is necessary so that the reverse proxy running inside the docker network
sends your request to the correct container.

## run ui-tests
cd epplication
bash test.sh
