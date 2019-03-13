# Docker

## requirements
 1) install docker
 2) install docker-compose

## installation
git clone https://github.com/certat/do-portal.git
rootdir=`pwd`

### run do-portal
cd $rootdir/backend
docker-compose up

## run cp-portal
cd $rootdir/frontend
docker-compose up

## run ui-tests
cd $rootdir/epplication
docker-compose up
docker cp ui-tests.sql epplication_app:/home/epplication/EPPlication/
docker exec -it epplication_app bash -c 'carton exec script/database.pl -cmd delete-tests'
docker exec -it epplication_app bash -c 'carton exec script/database.pl -cmd restore-tests --file ui-tests.sql'
firefox localhost:8080
  - login admin/admin123
  - select config 'do-config' in navigation menu
  - select and run 'test portal' test
  - if you want to watch the selenium browser -> `xtightvncviewer localhost::5900` (password: `secret`)
