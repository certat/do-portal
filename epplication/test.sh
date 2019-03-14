#!/bin/bash

echo 'copy ui-tests.sql to container'
docker cp ui-tests.sql epplication_app:/home/epplication/EPPlication/
docker exec -it epplication_app bash -c 'chown epplication:epplication ui-tests.sql'

echo 'delete existing tests'
docker exec -u epplication -it epplication_app bash -c 'carton exec script/database.pl -cmd delete-tests'

echo 'restore existing tests'
docker exec -u epplication -it epplication_app bash -c 'carton exec script/database.pl -cmd restore-tests --file ui-tests.sql'

echo 'copy test script to container'
docker cp test.pl epplication_app:/home/epplication/EPPlication/
docker exec -it epplication_app bash -c 'chown epplication:epplication test.pl'
docker exec -it epplication_app bash -c 'chmod u+x test.pl'

echo 'run test script'
docker exec -u epplication -it epplication_app bash -c 'carton exec ./test.pl'
