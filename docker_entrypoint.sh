#!/bin/sh

{

set -e

echo $DO_LOCAL_CONFIG

until PGPASSWORD=do_portal psql -h db -U do_portal -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - check schema"

# DB init
if PGPASSWORD=do_portal psql -U do_portal -h cert_db -d do_portal -lqt | cut -d \| -f 1 | grep -qw do_portal; then
  echo '###############'
  echo '### init DB ###'
  echo '###############'
  source bin/activate
  echo '### dropdb'
  PGPASSWORD=do_portal dropdb -U do_portal -h cert_db do_portal;
  echo '### createdb'
  PGPASSWORD=do_portal createdb -U do_portal -h cert_db -O do_portal do_portal;
  mv misc/migrations misc/tmp-migrations
  echo '### init'
  python3 manage.py db init;
  echo '### migrate'
  python3 manage.py db migrate;
  echo '### upgrade'
  python3 manage.py db upgrade;
  echo '### addsampledata'
  python3 manage.py addsampledata;
  echo '### addyaml'
  python3 demodata.py addyaml
  rm -rf misc/migrations
  mv misc/tmp-migrations misc/migrations
fi

# FODY
set +e
fody_schema_exists=`PGPASSWORD=do_portal psql -h db -U do_portal -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'fody';" do_portal 2>&1`
echo $fody_schema_exists;
set -e

if [[ $fody_schema_exists != *"fody (1 row)"* ]]; then
  echo 'init RIPE/FODY'
  PGPASSWORD=do_portal psql -h db -U do_portal -c "CREATE SCHEMA fody";
  PGPASSWORD=do_portal psql -U do_portal -h cert_db -d do_portal --echo-errors --file=create_fody_schema.sql
fi

source ./bin/activate && python manage.py run -h 0.0.0.0 -p 5001

} >&2 # redirect stout to stderr
