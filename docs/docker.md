# Docker

## git repositories

```
wget https://github.com/certat/do-portal/archive/release.zip
unzip release.zip
rm release.zip
cd do-portal-release
docker-compose build
docker-compose up

wget https://github.com/certat/customer-portal/archive/release.zip
unzip release.zip
rm release.zip
cd customer-portal-release
docker-compose build
docker-compose up
```

## init database
```
# on postgres container cert_db
docker exec -i -t cert_db bash -c " \
     dropdb -U do_portal do_portal \
  && createdb -U do_portal -O do_portal do_portal"

# create fody schema
docker exec -e PGPASSWORD=do_portal -e PGHOST=cert_db -e PGUSER=do_portal -i -t do-portal bash -c " \
     psql -c 'CREATE SCHEMA fody;' \
  && psql -f install/contactdb.pgdump \
  && psql -c 'grant select on all tables in schema fody to do_portal;' \
  && psql -c 'grant select on all sequences in schema fody to do_portal;' \
  && psql -c 'grant usage on schema fody to do_portal;' \
  "

docker exec -i -t do-portal bash -c " \
     source bin/activate \
  && echo misc/migrations clusterfuck \
  && mv misc/migrations misc/tmp-migrations \
  && python3 manage.py db init \
  && python3 manage.py db migrate \
  && python3 manage.py db upgrade \
  && python3 manage.py addsampledata \
  && python3 demodata.py addyaml \
  && rm -rf misc/migrations \
  && mv misc/tmp-migrations misc/migrations"

docker restart do-portal
```

## open in browser
http://127.0.0.1:5002
