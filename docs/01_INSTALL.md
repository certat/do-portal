# Installation

```
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
```

Backend and frontend configuration needs to be in sync.
See `frontend/nginx.conf`, `backend/config.cfg.docker` and `frontend/config/envs/docker.json`.

## Backend

```bash
cd /home/cert/do-portal/backend
```

Create config file and save as `backend/config.cfg`

```bash
export DO_LOCAL_CONFIG=/home/cert/do-portal/backend/config.cfg
python3 -m venv ~/do-portal
source ./bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
mkdir logs
```

## Database

### Install
```bash
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

```

### Upgrade
python manage.py db migrate;
python manage.py db upgrade;

if an error occurs the table "alembic_version" in the database has to upgraded to the correct version

## Frontend

```bash
cd /home/cert/do-portal/frontend
cp secret.json.example secret.json
```

Create configuration file and save it as `config/envs/production.json`
```bash
npm install
PATH=$(npm bin):$PATH bower install
PATH=$(npm bin):$PATH grunt
```
Create the nginx configuration and save it as `/etc/nginx/sites-available/portal-frontend`.

```bash
ln -s /etc/nginx/sites-available/portal-frontend /etc/nginx/sites-enabled/portal-frontend
systemctl restart nginx
```

# Docker

An installation based on docker is also possible

## Requirements
 1) install docker
 2) install docker-compose

## Installation
```bash
git clone https://github.com/certat/do-portal.git
```
## run portal
```bash
docker-compose up
```
## edit /etc/hosts file

add the following lines

```
   127.0.0.1       epplication_app
   127.0.0.1       portal-frontend
   127.0.0.1       portal-backend
```

This is necessary that the reverse proxy running inside the docker network
sends your request to the correct container.

## Run ui-tests
```bash
cd epplication
bash test.sh
```
