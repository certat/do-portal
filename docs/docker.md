# Docker

## requirements
 1) install docker
 2) install docker-compose

## installation
mkdir cert
cd cert
certdir=`pwd`

### run do-portal
cd $certdir
git clone https://github.com/certat/do-portal.git
cd do-portal
docker-compose up

## run cp-portal
cd $certdir
git clone https://github.com/certat/customer-portal.git
cd customer-portal
docker-compose up

## run ui-tests
cd $certdir/do-portal/epplication
docker-compose up
docker cp ui-tests.sql epplication_app:/home/epplication/EPPlication/
docker exec -it epplication_app bash -c 'carton exec script/database.pl -cmd delete-tests'
docker exec -it epplication_app bash -c 'carton exec script/database.pl -cmd restore-tests --file ui-tests.sql'
firefox localhost:8080
  - login admin/admin123
  - select config 'do-config' in navigation menu
  - select and run 'test portal' test
  - if you want to watch the selenium browser -> `xtightvncviewer localhost::5900` (password: `secret`)
