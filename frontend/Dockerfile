FROM debian:stretch-slim

RUN    apt-get update \
    && apt-get install -y --no-install-recommends \
       git curl vim tree ack \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*

ARG CONTAINER_UID=1000
RUN useradd --create-home --home-dir /home/cert \
            --uid $CONTAINER_UID --user-group --shell /bin/bash cert

USER cert
WORKDIR /home/cert/customer-portal

EXPOSE 8081
CMD ["bash", "./docker_entrypoint.sh"]
