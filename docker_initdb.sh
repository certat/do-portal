#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER dope_test PASSWORD 'dope_test';
    CREATE DATABASE dope_test;
    GRANT ALL PRIVILEGES ON DATABASE dope_test TO dope_test;
EOSQL
