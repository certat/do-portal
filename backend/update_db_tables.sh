#!/bin/bash
# experimental script
# repairs db when alembic makes problems after git pull with changes in database structure

cd /home/cert/do-portal
source bin/activate

PGPASSWORD=do_portal psql -h portal-db -U do_portal -c '\q'
RETVAL=$?
if [ $RETVAL -ne 0 ]
then
  echo "postgresql is not available"
  exit 0
fi


select_fody_table=`PGPASSWORD=do_portal psql -U do_portal -h portal-db -d do_portal -t -c "SELECT EXISTS (SELECT 1 from information_schema.tables WHERE table_schema = 'fody' AND table_name = 'organisation_automatic');"`

# DB init
if [ $select_fody_table = 't' ]; then
  if [ ! -e misc/old-migrations-versions ]; then
    mkdir misc/old-migrations-versions
  elif [ ! -d misc/old-migrations-versions ]; then
    echo "misc/old-migrations-versions exists, but is not a directory"
    exit 0
  fi
 
  if test "$(ls -A misc/migrations/versions/)"; then
    mv -f misc/migrations/versions/* misc/old-migrations-versions/
  fi
  set -e

  PGPASSWORD=do_portal psql -U do_portal -h portal-db -d do_portal -c "delete from alembic_version;"

  python3 manage.py db migrate
  python3 manage.py db upgrade
fi

