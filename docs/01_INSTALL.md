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

## Backend

```bash
cd /home/cert/do-portal/backend
```

Create config file and save as `backend/config.cfg`
cp backend/config.cfg.example backend/config.cfg

```bash
export DO_LOCAL_CONFIG=/home/cert/do-portal/backend/config.cfg
python3 -m venv ~/do-portal
source ./bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
mkdir logs
```

## Database

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

## Frontend

```bash
cd /home/cert/do-portal/frontend
```

Create configuration files
cp frontend/config/envs/devel.json.example frontend/config/envs/devel.json
cp frontend/config/envs/production.json.example frontend/config/envs/production.json

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
   127.0.0.1       epplication-app
   127.0.0.1       portal-frontend
   127.0.0.1       portal-backend
```

This is necessary for the reverse proxy running inside the docker network
to send requests to the correct container.

## Login
http://portal-frontend:8081
email/password for the login can be found in `backend/install/master_user.yaml`

## Run ui-tests
```bash
cd epplication
bash test.sh
```

## Test Data and Fixtures

The docker image both installs necessary fixtures (like membership roles) and some structured testdata

The data files are found in the ./install directory:

roles.yaml
    contains additional roles which will be appended to default roles defined in the code (see MembershipRole.__insert_defaults in model.py)


master_user.yaml
    contains an organization and user (the minimum necessary to use the do_portal)

    added in the docker_entrypoint file via python3 manage.py insertmasteruser;


testdata.yaml
    contains several hierarchically structured organizations and users for testing

    added in the docker_entrypoint file via python3 demodata.py addyaml

Data Structure
the files are in the yaml format

'''
org:
  - abbreviation: master
    full_name: "MasterOrg"
    display_name: "Master Org"
user:
  - name: master
    org: master
    role: OrgAdmin
    comment: "Master User"
    email: "master@master.master"
    password: "Bla12345%"
'''

the reference to the organization in the user section is via the abbreviation




