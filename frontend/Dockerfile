FROM node:8-stretch

RUN    apt-get update \
    && apt-get install -y --no-install-recommends \
       nginx \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --home-dir /home/cert \
            --user-group --shell /bin/bash cert

WORKDIR /home/cert/customer-portal
RUN chown cert:cert /home/cert/customer-portal
USER cert

COPY --chown=cert:cert ./package.json /home/cert/customer-portal/package.json
RUN npm install

COPY --chown=cert:cert ./bower.json /home/cert/customer-portal/bower.json
RUN PATH=$(npm bin):$PATH bower install

EXPOSE 8081

COPY --chown=cert:cert . /home/cert/customer-portal
RUN cp config/envs/docker.json config/envs/devel.json

RUN PATH=$(npm bin):$PATH grunt

USER root
RUN    cp /home/cert/customer-portal/nginx.conf /etc/nginx/sites-available/portal-frontend \
    && ln -s /etc/nginx/sites-available/portal-frontend /etc/nginx/sites-enabled/portal-frontend \
    && rm /etc/nginx/sites-enabled/default

CMD /etc/init.d/nginx restart && tail -f /var/log/nginx/access.log
