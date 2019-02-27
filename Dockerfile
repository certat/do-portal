FROM node:8-stretch

RUN useradd --create-home --home-dir /home/cert \
            --user-group --shell /bin/bash cert

WORKDIR /home/cert/customer-portal
RUN chown cert:cert /home/cert/customer-portal
USER cert
COPY --chown=cert:cert ./package.json /home/cert/customer-portal/package.json
RUN npm install
RUN npm install grunt-cli
RUN npm install bower

COPY --chown=cert:cert ./bower.json /home/cert/customer-portal/bower.json
RUN PATH=$(npm bin):$PATH bower install

EXPOSE 5002
EXPOSE 35729

COPY --chown=cert:cert . /home/cert/customer-portal
RUN cp config/envs/docker.json config/envs/devel.json

CMD PATH=$(npm bin):$PATH grunt serve
