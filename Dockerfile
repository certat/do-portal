FROM debian:stretch-slim

RUN    apt-get update \
    && apt-get install -y \
       vim less tree ack \
       build-essential git \
       libssl-dev libxml2 libxml2-dev \
       ssdeep exiftool libfuzzy-dev \
       libffi-dev p7zip-full libncurses-dev \
       libxslt-dev lib32z1-dev libpq-dev \
       python3-venv python3-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --home-dir /home/cert \
            --user-group --shell /bin/bash cert

COPY --chown=cert:cert requirements.txt /home/cert/do-portal/requirements.txt
WORKDIR /home/cert
USER cert

ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL C.UTF-8
ENV DO_LOCAL_CONFIG /home/cert/do-portal/config.cfg

WORKDIR /home/cert/do-portal
RUN python3 -m venv ~/do-portal

RUN /bin/bash -c "source ./bin/activate && pip install -U pip setuptools && pip install -r requirements.txt"

COPY --chown=cert:cert . /home/cert/do-portal
RUN mkdir logs
RUN cp config.cfg.docker config.cfg

EXPOSE 5001

CMD /bin/bash -c "source ./bin/activate && python manage.py run -h 0.0.0.0 -p 5001"
