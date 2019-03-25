# Docker

## requirements
 1) install docker
 2) install docker-compose

## installation
git clone https://github.com/certat/do-portal.git

## run portal
docker-compose up

## edit /etc/hosts file

add the following lines

   127.0.0.1       epplication_app
   127.0.0.1       portal-frontend
   127.0.0.1       portal-backend

this is necessary so that the reverse proxy running inside the docker network
sends your request to the correct container.

## run ui-tests
cd epplication
bash test.sh
