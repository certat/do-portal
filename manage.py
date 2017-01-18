#!venv/bin/python
import os
import sys
import json
from collections import namedtuple
from getpass import getpass
import requests
import datetime

from app import create_app
from flask_migrate import MigrateCommand
from flask_script import Manager, prompt_bool
from flask_gnupg import fetch_gpg_key
from app import db, models, mail
from app.models import User, Organization, IpRange, Fqdn, Asn, Email
from app.models import OrganizationGroup, AHBot, Vulnerability, Tag
from app.models import ContactEmail, emails_organizations, tags_vulnerabilities
from app.models import Role, Permission
from app.api.decorators import async

app = create_app(os.getenv('DO_CONFIG') or 'default')
manager = Manager(app)

CollabCustomer = namedtuple('CollabCustomer', ['name', 'config'])


class CollabError(Exception):
    pass


#: on every schema change migrate by running:
#: $ ./manage.py db migrate
#: $ ./manage.py db upgrade
manager.add_command('db', MigrateCommand)


@app.context_processor
def inject_permissions():
    return dict(Permission=Permission)


@async
def send_async_mail(msg):
    with app.app_context():
        mail.send(msg)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models, Permission=Permission)


@manager.command
def create_groups():
    """Create initial organization groups:Constituents, Partners and
    National CERTs

    """
    groups_count = OrganizationGroup.query.count()
    if groups_count > 0:
        sys.exit("Groups table is not empty.")
    constituents = OrganizationGroup(name='Constituents', color='#0033cc')
    db.session.add(constituents)
    nat_certs = OrganizationGroup(name='National CERTs', color='#AF2018')
    db.session.add(nat_certs)
    partners = OrganizationGroup(name='Partners', color='#00FF00')
    db.session.add(partners)
    db.session.commit()
    print('Groups added')


@manager.command
def insert_roles():
    """Insert default user roles"""
    if prompt_bool("Insert default roles? (roles table will be truncated)"):
        Role.query.delete()
        Role._Role__insert_default_roles()
        print("Done")


@manager.option('-c', '-url', dest='collab_url',
                default='https://abusehelper.cert.europa.eu/collab/customers/'
                        'FrontPage?action=getMetaJSON&args='
                        'CategoryAbuseContact,%27%20%27%20||Full%20name||'
                        'IP%20range||FQDN||ASN||Abuse%20email%27%20%27||'
                        'Mail%20template||Mail%20times||ID||'
                        '%27%20%27Point%20of%20Contact||')
@manager.option('-u', '-user', dest='username', required=True)
def import_from_collab(collab_url, username):
    """Import customers from AbuseHelper collab wiki.

    .. note:: Will not verify certificates

    :param collab_url: URL of collab
    :param username: Collab username
    """
    group_count = OrganizationGroup.query.count()
    if group_count < 1:
        sys.exit("No groups defined. "
                 "Run create_groups to create default groups.")
    if prompt_bool("This command will drop all exiting organizations"
                   " and all their details (IPs, Emails, ASNs, etc.). "
                   "Are you sure you want to continue?"):
        password = getpass(prompt='Enter collab password:')
        if not password:
            sys.exit("No anonymous access allowed")
        ah_resp = requests.get(collab_url, auth=(username, password),
                               verify=False)
        if ah_resp.status_code != 200:
            app.log.error(ah_resp.reason)
            sys.exit(1)

        print("Deleting old data...")
        db.session.execute(emails_organizations.delete())
        db.session.execute(tags_vulnerabilities.delete())

        ContactEmail.query.delete()
        IpRange.query.delete()
        Fqdn.query.delete()
        Asn.query.delete()
        Email.query.delete()
        Vulnerability.query.delete()
        Organization.query.filter(Organization.group_id == 1).delete()
        print("Old data deleted!")

        data = json.loads(ah_resp.text)
        for name, config in data.items():
            org = Organization.from_collab(CollabCustomer(name, config))
            print("Adding {}...".format(org.abbreviation))
            db.session.add(org)
        db.session.commit()
        print('Done')


@manager.option('-c', '-url', dest='collab_url',
                default='https://abusehelper.cert.europa.eu/collab/'
                        'national_certs/FrontPage?action=getMetaJSON&args'
                        '=CategoryNationalCert,%20||Rule||Description||'
                        'Abuse%20email||Mail%20template||Mail%20times||'
                        'Disabled||')
@manager.option('-u', '-user', dest='username', required=True)
def import_national_certs(collab_url, username):
    """Import national CERTs information from AbuseHelper collab wiki.

    .. note:: Does not verify certificates

    :param collab_url: URL of collab
    :param username: Collab username
    """
    if prompt_bool("This command should be run only once, on install"):
        password = getpass(prompt='Enter collab password:')
        if not password:
            sys.exit("No anonymous access allowed")
        ah_resp = requests.get(collab_url, auth=(username, password),
                               verify=False)
        if ah_resp.status_code != 200:
            app.log.error(ah_resp.reason)
            sys.exit(1)
        data = json.loads(ah_resp.text)
        for country, details in data.items():
            org = Organization(
                abbreviation=country,
                group_id=2,
                full_name='National CERT of ' + country
            )

            try:
                org.mail_times = details['Mail times'][0]
            except IndexError:
                app.log.debug('Using default mail times...')
            try:
                org.mail_template = details['Mail template'][0]
            except IndexError:
                app.log.debug('Using default template...')
            org.abuse_emails = details['Abuse email']
            print("Adding {}...".format(country))
            db.session.add(org)
        db.session.commit()
        print('Done')


@manager.command
def delorg(org_id):
    o = Organization.get(org_id)
    o.fqdns = o.ip_ranges = o.asns = o.abuse_emails = o.contact_emails = []
    Organization.query.filter_by(id=org_id).delete()
    db.session.commit()


@manager.option('-f', '--file', dest='hof_dump', required=True)
def import_hof(hof_dump):
    """Import Hall of Fame records from initial PoC"""
    dos = {}
    staff = User.query.filter_by(role_id=1).all()
    for do in staff:
        name = ''.join([n[0] for n in do.name.split()])
        if name == 'VRR':
            dos['VR'] = do.id
        dos[name] = do.id

    constituents = {}
    orgs = Organization.query.filter_by(group_id=1).all()
    for org in orgs:
        constituents[org.abbreviation] = org.id

    with open(hof_dump) as f:
        hof = json.loads(f.read())
        for entry in hof:
            if entry['published'] == 'yes':
                published = True
            else:
                published = False
            if entry['scanable'] == 'yes':
                scanable = True
            else:
                scanable = False
            user_id = dos.get(entry['DO'], 1)
            org_id = constituents.get(entry['constituent'], 146)
            list_types = []
            vtype = entry['type']
            if Tag.query.filter_by(name=vtype).first():
                list_types.append(Tag.query.filter_by(name=vtype).first())
            else:
                list_types.append(Tag(name=vtype))

            vuln = Vulnerability(
                user_id=user_id, check_string=entry['check_string'],
                updated=datetime.datetime.now(),
                reporter_name=entry['reporter'],
                url=entry['url'],
                request_data=json.dumps(entry['data']),
                request_method=entry['method'],
                request_response_code=entry['test_status'],
                tested=entry['last_test'], reported=entry['report_date'],
                patched=entry['patched_date'], published=published,
                scanable=scanable, incident_id=entry['Incident'],
                organization_id=org_id, labels_=list_types
            )
            db.session.add(vuln)
        db.session.commit()
    print('Done')


@manager.option('-f', '--file', dest='botsdump', required=True)
def import_bots(botsdump):
    """
    # >>> import startup
    # >>> configs = list(startup.configs())
    # >>> data = {}
    # >>> for c in configs:
    # >>>     data[c.name] = c.params
    # >>> with open('bots.json') as f:
    # >>>     f.write(json.dumps(data))
    :param botsdump:
    :return:
    """
    with open(botsdump) as f:
        bots = json.loads(f.read())
        for name, params in bots.items():
            if '.sanitizer' in name:
                continue
            b = AHBot(name=name, params=json.dumps(params))
            if 'url' in params:
                b.url = params['url']
            db.session.add(b)
    db.session.commit()


@manager.option('-e', '--emails', dest='emails')
def download_keys(emails):
    if not emails:
        sys.exit("Error: Please provide emails")
    for e in emails:
        fetch_gpg_key(e, app.config['GPG_KEYSERVERS'][0])


@manager.command
def add_user(name, email, admin=False):
    """Create new local account

    :param name: Account name
    :param email: E-mail
    :param admin: Mark account as admin, default is False.
    """
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(name=name, email=email, password=password, is_admin=admin)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(email))


if __name__ == '__main__':
    manager.run()
