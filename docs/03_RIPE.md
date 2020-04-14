RIPE integration
================

We use the RIPE integration developed for fody to load the RIPE data.

Installation
------------

First we install the certbund-contact tool. The code shows how to install it in a virtualenv:

```bash
apt install curl
mkdir fody_importer
cd fody_importer
git clone https://github.com/Intevation/intelmq-certbund-contact.git
python3 -m virtualenv -p python3 intelmq_venv
~cp-server/fody_importer/intelmq_venv/bin/pip install ~cp-server/fody_importer/intelmq-certbund-contact/
~cp-server/fody_importer/intelmq_venv/bin/pip install psycopg2
```

Database
--------

Next, we need to setup the database structure:

```bash
sudo -u postgres psql do_portal < backend/install/contactdb_schema_only.pgdump
```

And then we can set the permissions and create a new user called fody. This user only has access to the needed tables.
A separate schema "fody" is used for the imported data. This allows clear separation of data, software and privileges.
By setting the default search path for the user, the import afterwards automatically use this schema.
```bash
sudo -u postgres psql do_portal
CREATE USER fody WITH PASSWORD '$PASSWORD';
ALTER USER fody SET search_path TO 'fody';
CREATE SCHEMA fody;
GRANT USAGE ON SCHEMA fody to fody;
GRANT ALL ON ALL TABLES IN SCHEMA fody TO fody;
GRANT ALL ON ALL SEQUENCES IN SCHEMA fody TO fody;
GRANT SELECT on fody.organisation_automatic to do_portal;
GRANT SELECT on fody.organisation_to_network_automatic to do_portal;
GRANT SELECT on fody.network_automatic to do_portal;
GRANT SELECT on fody.organisation_to_asn_automatic to do_portal;
GRANT SELECT on fody.contact_automatic to do_portal;
```

Cronjob
-------

To load and periodically update the RIPE data, a script like this can be used:

```bash
set -e

sudo -iu cp-server
cd ~/fody_importer
~cp-server/fody_importer/intelmq-certbund-contact/bin/ripe_download
pushd $(date -I)
~cp-server/fody_importer/intelmq_venv/bin/python ~cp-server/fody_importer/intelmq-certbund-contact/intelmq_certbund_contact/ripe/ripe_diff.py --restrict-to-country AT --conninfo "user=fody dbname=do_portal password=$PASSWORD host=localhost"
popd
rm $(date -I)
```

Data structure
--------------

The following tables are relevant:

```
do_portal=> \dt+ fody.*_automatic
 fody   | contact_automatic                 | table |
 fody   | network_automatic                 | table |
[...]
 fody   | organisation_automatic            | table |
 fody   | organisation_to_asn_automatic     | table |
[...]
 fody   | organisation_to_network_automatic | table |
```
