#!/bin/sh

{

set -e

cd /home/cert/do-portal
python3 -m venv ~/do-portal

source ./bin/activate
pip install -r requirements.txt

if [ ! -d logs ]; then
  echo 'create logs dir'
  mkdir logs
fi

if [ ! -f config.cfg ]; then
  echo 'create docker config'
  cp config.cfg.docker config.cfg
else
  if ! cmp --silent config.cfg config.cfg.docker
  then
    echo 'Warning: config.cfg differs from config.cfg.docker!'
  fi
fi


echo $DO_LOCAL_CONFIG

until PGPASSWORD=do_portal psql -h portal-db -U do_portal -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - check schema"

# select_fody_table should be either 'f' or 't'
select_fody_table=`PGPASSWORD=do_portal psql -U do_portal -h portal-db -d do_portal -t -c "SELECT EXISTS (SELECT 1 from information_schema.tables WHERE table_schema = 'fody' AND table_name = 'organisation_automatic');"`

# DB init
if [ $select_fody_table = 'f' ]; then
  echo '###############'
  echo '### init DB ###'
  echo '###############'
  source bin/activate
  echo '### dropdb'
  PGPASSWORD=do_portal dropdb -U do_portal -h portal-db do_portal;
  echo '### createdb'
  PGPASSWORD=do_portal createdb -U do_portal -h portal-db -O do_portal do_portal;
  mv misc/migrations misc/tmp-migrations # TODO remove hack
  echo '### init'
  python3 manage.py db init;
  echo '### migrate'
  python3 manage.py db migrate;
  echo '### upgrade'
  python3 manage.py db upgrade;
  echo '### initializedb'
  python3 manage.py initializedb;
  echo '### insertmasteruser'
  python3 manage.py insertmasteruser;
  echo '### addyaml'
  python3 demodata.py addyaml
  rm -rf misc/migrations # TODO remove hack
  mv misc/tmp-migrations misc/migrations # TODO remove hack

  echo '### init RIPE/FODY'
  ### create RIPE/FODY dump
  # 1) create dump on remote server
  #    `pg_dump --no-owner --schema-only --no-privileges contactdb > /tmp/contactdb_schema_only.pgdump`
  # 2) move to install/contactdb_schema_only.pgdump
  # 3) change schema
  #    `sed -i 's/public\./fody./g' install/contactdb_schema_only.pgdump`
  PGPASSWORD=do_portal psql -U do_portal -h portal-db -c "CREATE SCHEMA fody";
  PGPASSWORD=do_portal psql -U do_portal -h portal-db -d do_portal --echo-errors --file=install/contactdb_schema_only.pgdump
fi

export FLASK_DEBUG=1
source ./bin/activate 
while :
do
python -u manage.py run -h 0.0.0.0 -p 8081
sleep 1
done

} >&2 # redirect stout to stderr
