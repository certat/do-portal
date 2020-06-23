============
Installation
============

Rough, incomplete installation instructions.

Requirements
============

OS
--

.. code-block:: bash

    sudo apt-get install ssdeep exiftool libfuzzy-dev libffi-dev p7zip-full libncurses-dev python3-dev mysql-server python3-virtualenv git

.. note::

    In Debian sid most of forensics tools can be installed by installing the
    forensics-all metapackage.

virtualenv
----------

As a lot of libraries will be installed and/or updated and we don't want to mix
up with the system's libraries. We thus use a virtualenv:

.. code-block:: bash

    python3-virtualenv
    virtualenv ~/do-portal/ -p python3
    source ~/do-portal/bin/activate

Now, `which python3` and `which pip3` should show the executables inside the
virtualenv.

Python libraries
----------------

First upgrade your pip and setuptools. Current versions of these are required
by the libraries we will install.

.. code-block:: bash

    sudo pip install -U pip setuptools
    sudo pip install -r requirements.txt


RabbitMQ
--------

.. code-block:: bash

    sudo apt-get install rabbitmq-server
    sudo rabbitmqctl add_user doportal doportal
    sudo rabbitmqctl add_vhost do.cert.europa.eu
    sudo rabbitmqctl set_user_tags doportal do
    sudo rabbitmqctl set_permissions -p do.cert.europa.eu doportal ".*" ".*" ".*"


Celery
------

.. code-block:: bash

    venv/bin/pip install celery

Start the celery worker
+++++++++++++++++++++++

.. code-block:: bash

    export DO_LOCAL_CONFIG=/srv/doportal/config.cfg
    sudo -E -u www-data -s /bin/bash -c "venv/bin/celery worker -A celery_worker.celery -l debug"


Mailman
-------

`<https://mailman.readthedocs.org/en/latest/src/mailman/docs/WebUIin5.html>`_
`<https://pythonhosted.org/mailman/README.html>`_
Django 1.9 is not fully supported by postorious_standalone.
Use Django==1.8.5

.. code-block:: bash

    apt-get install postfix
    # config
    mkdir /srv/mailman && cd /srv/mailman
    git clone https://gitlab.com/mailman/mailman.git
    ../py3/bin/python setup.py develop
    py3/bin/mailman -C /srv/mailman/mailman.cfg start
    git clone https://gitlab.com/mailman/mailmanclient.git
    ../py3/bin/python setup.py develop
    git clone https://gitlab.com/mailman/postorius.git
    ../py3/bin/python setup.py develop
    git clone https://gitlab.com/mailman/postorius_standalone.git

GPG setup
---------

Required for searching keys:

.. code-block:: bash

    apt-get install gnupg-curl

Get CA certificate:

.. code-block:: bash

    wget -O /usr/share/ca-certificates/sks-keyservers.netCA.crt https://sks-keyservers.net/sks-keyservers.netCA.pem
    dpkg-reconfigure ca-certificates

OpenSSL
-------

When connecting to SSL enabled APIs that use the CERT-EU wildcard
certificate you need to install the CA on the client side.
In python you have to provide the full chain
in the correct order. E.i. concatenate the certificates in one bundle.

.. code-block:: bash

    cat DigiCert\ SHA2\ Secure\ Server\ CA.cer DigiCert\ Global\ Root\ CA.cer >> digi_chain.crt

Test it:

.. code-block:: python

    import requests
    chain='/full/path/to/digi_chain.crt'
    url = "https://*.cert.europa.eu/.../auth/login"
    user = 'username'
    passwd = 'passwd'
    r = requests.post(url, auth=(user, passwd), verify=chain)


Alternatively, setting the REQUESTS_CA_BUNDLE or CURL_CA_BUNDLE
environment varible will have the save effect.


Avira
-----

.. code-block:: bash

    unzip
    mv savapi-sdk-linux_glibc24_x86_64 /opt/savapi/
    cd /opt/savapi/src && make
    cd /opt/savapi/bin
    ./savapi --tcp=127.0.0.1:9999
    ./clientlib_basic_example /srv/doportal/app/static/data/samples/stux.zip 10776
    # 10776 is the product ID


F-Secure
--------

.. code-block:: bash

    ./fsls-<major>.<minor>.<build>-rtm --command-line-only

    /opt/f-secure/fsav/fsav-config
    /opt/f-secure/fsav/sbin/fschooser


Disable real-time virus protection and integrity check
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: bash

    /opt/f-secure/fsma/bin/chtest s 45.1.40.10 0
    /opt/f-secure/fsma/bin/chtest s 45.1.70.10 0

Comodo
------

Install http://ftp.de.debian.org/debian/pool/main/o/openssl/libssl0.9.8_0.9.8o-4squeeze14_i386.deb

Tests
-----

Make sure you have a working configuration first.

.. code-block:: bash

    py.test --flake8 --cov=app --cov-report=html --cov-report=term -r we tests


Setup
=====

Create a config.cfg like this one: https://github.com/certeu/do-portal-vagrant/tree/8dc4cab8ad4ddb8792d040b295189bca1765fffc/files/configs/doportal
and adapt paths, mysql configs etc

Set some environment variables (and make them permanent):

.. code-block:: bash

    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
    export DO_LOCAL_CONFIG=/path/to/config.cfg

Create the logs directory:

.. code-block:: bash

    mkdir logs

Create the database and run the integrated webserver:

.. code-block:: bash

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py addsampledata
    python manage.py run -h 0.0.0.0 -p 8000

You can now access the interface at `http://doportal` with user
`testadmin@domain.tld` and password `changeme`. You need to acces the portal
with only the hostname `doportal` and port 80, others do not work!

Now you can setup a webserver to serve the application.

Bootstrap Database - Default Data
=================================

.. code-block:: bash

     python demodata.py addyaml

this uses "install/testdata.yaml" to prime the database

the same structure may be used to insert your initial masteruser

in app/fixtures/testfixture.py all the methods to prime the database are implemented

