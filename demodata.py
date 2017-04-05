#!venv/bin/python
import os
import sys
import json
from collections import namedtuple
import requests
import datetime
import click
import yaml

from app import create_app
from flask import current_app
from flask.cli import FlaskGroup
from flask_gnupg import fetch_gpg_key
from app import db
from app.models import User, Organization, IpRange, Fqdn, Asn, Email
from app.models import OrganizationGroup, Vulnerability, Tag
from app.models import ContactEmail, emails_organizations, tags_vulnerabilities
from app.models import Role, ReportType, OrganizationUser, OrganizationUserRole


def create_cli_app(info):
    return create_app(os.getenv('DO_CONFIG') or 'default')


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group(cls=FlaskGroup, create_app=create_cli_app)
def cli():
    """DO portal management script"""


@cli.command()
def addyaml():
   """Add sample data from yaml file""" 
   with open("install/testdata.yaml", 'r') as stream:
        data_loaded = yaml.load(stream)

   click.echo(yaml.dump(data_loaded, default_flow_style=False))

   for org in data_loaded['org']:
      click.echo(org['name'])
      o = Organization(
         abbreviation=org['name'],
         full_name=org['name'],
      )
      if ('parent_org' in org):
         po = Organization.query.filter_by(full_name=org['parent_org']).first() 
         o.parent_org = po
      db.session.add(o)
      db.session.commit()    

   for user in data_loaded['user']:
      click.echo(user['name'])
      u = User(
         name = user['name']
      )
      u.password = 'bla'
      db.session.add(u)
      
      role = OrganizationUserRole.query.filter_by(name=user['role']).first()
      org = Organization.query.filter_by(full_name=user['org']).first()
      oxu = OrganizationUser(
         email =  user['name'] + '@' + org.full_name,
         organization = org, 
         user = u,
         org_user_role = role,
      )
      db.session.commit()    

@cli.command()
def add():
    """Add sample data"""

    cert = Organization(
        abbreviation="CERT",
        full_name="CERT Master User",
    )
    db.session.add(cert)

    cert_user = User(
        name = "cert master user",
    )
    cert_user.password = 'bla'
    db.session.add(cert_user)
    
    cert_user4cert = OrganizationUser(
        email = 'certifant@cert.at',
        zip = '1234',
        organization = cert,        
        user = cert_user
    )
       
    db.session.commit()    
    
    click.echo('Done Org id: ' + str(cert.id)) 
    click.echo('Done User id: ' + str(cert_user.id)) 
    click.echo('adding sub org') 

    evn = Organization(
        abbreviation="EVN",
        full_name="EVN Dach",
        parent_org = cert
    )
    # db.session.add(evn)

    evn_user = User(
        name = "evn master user"
    )
    evn_user.password = 'bla'
    
    OrganizationUser(
        email = 'master@evn.at',
        zip = '5678',
        organization = evn,        
        user = evn_user
    )

    evn_strom = Organization(
        abbreviation="EVN Strom",
        full_name="EVN Strom",
        parent_org = evn
    )
    db.session.add(evn_strom)

    evn_strom_user = User(
        name = "evn strom user",
    )
    evn_strom_user.password = 'bla'
    db.session.add(evn_strom_user)
    
    evnstrom_orguser = OrganizationUser(
        email = 'strom@evn.at',
        zip = '5678',
        organization = evn_strom,        
        user = evn_strom_user
    )
    db.session.commit()    
    

@cli.command()
def delete():
    """delete sample data"""
    OrganizationUser.query.delete()
    Organization.query.delete()
    User.query.delete()
    db.session.commit()

@cli.command()
def print():
   """output sample data"""
   u = User.query.filter_by(name="certmaster").first()
   click.echo(u.name)
   for uo in u.user_organizations:
       click.echo(uo.email)
       click.echo(uo.organization.full_name)
       for co in uo.organization.child_organizations:
          click.echo(co.full_name)

   for user in u.get_user_organizations():
       click.echo('%s %s' % (user.name, user.role))
      


if __name__ == '__main__':
    cli()
