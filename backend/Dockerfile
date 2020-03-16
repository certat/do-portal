FROM debian:stretch
#FROM debian:stretch-slim

# create man dirs manually because otherwise psql won't install on debian-slim
#RUN for i in {1..8}; do mkdir -p "/usr/share/man/man$i"; done

RUN    apt-get update \
    && apt-get install -y \
       vim less tree ack \
       build-essential git \
       libssl-dev libxml2 libxml2-dev \
       ssdeep exiftool libfuzzy-dev \
       libffi-dev p7zip-full libncurses-dev \
       libxslt-dev lib32z1-dev libpq-dev \
       python3-venv python3-dev python3-pip python3-setuptools \
       postgresql-client-9.6 \
       procps \
    && rm -rf /var/lib/apt/lists/*

ARG CONTAINER_UID=1000
RUN useradd --create-home --home-dir /home/cert \
            --uid $CONTAINER_UID --user-group --shell /bin/bash cert

USER cert
WORKDIR /home/cert/do-portal

ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL C.UTF-8
ENV DO_LOCAL_CONFIG /home/cert/do-portal/config.cfg

EXPOSE 8081

CMD ["bash", "./docker_entrypoint.sh"]
