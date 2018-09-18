FROM node:8-stretch

RUN useradd --create-home --home-dir /home/cert \
            --user-group --shell /bin/bash cert

COPY --chown=cert:cert . /home/cert/customer-portal
WORKDIR /home/cert/customer-portal
USER cert
RUN npm install
RUN npm install grunt-cli
RUN npm install bower

RUN PATH=$(npm bin):$PATH bower install

RUN PATH=$(npm bin):$PATH grunt

EXPOSE 5002
EXPOSE 35729

CMD PATH=$(npm bin):$PATH grunt serve
