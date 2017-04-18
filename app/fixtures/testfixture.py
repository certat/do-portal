import os
import sys
import json
from collections import namedtuple
import requests
import datetime
import yaml

from app import create_app
from flask import current_app
from flask.cli import FlaskGroup
from flask_gnupg import fetch_gpg_key
from app import db
from app.models import User, Organization, IpRange, Fqdn, Asn, Email
from app.models import OrganizationGroup, Vulnerability, Tag
from app.models import ContactEmail, emails_organizations, tags_vulnerabilities
from app.models import Role, ReportType, OrganizationMembership, MembershipRole

class testdata:

   def addyaml():
      """Add sample data from yaml file""" 
      with open("install/testdata.yaml", 'r') as stream:
           data_loaded = yaml.load(stream)
   
      for org in data_loaded['org']:
         if 'full_name' not in org:
            org['full_name'] = org['abbreviation']
         if 'display_name' not in org:
            org['display_name'] = org['abbreviation']
         o = Organization(
            abbreviation=org['abbreviation'],
            full_name=org['full_name'],
            display_name=org['display_name'],
         )
         if ('parent_org' in org):
            po = Organization.query.filter_by(abbreviation=org['parent_org']).first() 
            o.parent_org = po
         db.session.add(o)
         db.session.commit()    
   
      for user in data_loaded['user']:
         u = User.query.filter_by(name = user['name']).first()
         if (not u):
            u = User(
               name = user['name']
            )
            u.api_key = '61938c95b8dd503e2b8126ee51b5a2644d121694170af29cac6304ee9f376e71'
            u.password = 'bla'
            db.session.add(u)
         
         role = MembershipRole.query.filter_by(name=user['role']).first()
         org = Organization.query.filter_by(abbreviation=user['org']).first()
         if 'email' not in user:
             user['email'] = 'na@email.at'
         if 'street' not in user:
             user['street'] = 'no street'
         if 'zip' not in user:
             user['zip'] = '1234'
         if 'city' not in user:
             user['city'] = 'n/a'
         if 'country' not in user:
             user['country'] = 'no country for old men'
         if 'comment' not in user:
             user['comment'] = 'no comment'
         if 'phone' not in user:
             user['phone'] = '12345678'
         
         oxu = OrganizationMembership(
            email =  user['email'],
            street = user['street'],
            city = user['city'],
            zip  = user['zip'],
            country = user['country'],
            comment = user['comment'],
            phone =user['phone'],
            organization = org, 
            user = u,
            membership_role = role,
         )
         db.session.commit()    
   
   def print():
      """output sample data"""
      u = User.query.filter_by(name="certmaster").first()
      echo(u.name + str(u.id))
      for uo in u.user_memberships:
          print(uo.email)
          print(uo)
          print(uo.organization.full_name)
          for co in uo.organization.child_organizations:
             print(co.full_name)
   
      print('**** organization_memberships ******')
      for oxu in u.get_organization_memberships():
      
          print('%s %s %s' % 
              (oxu.email, oxu.membership_role.name,  oxu.organization.full_name))
   
      #print(u.org_ids)
   
      print('**** organization_memberships ******')
      oms = User.query.filter_by(name = 'Verbund Admin').first().get_organization_memberships()  
      if (oms):
        for oxu in oms: 
          print('%s %s %s' % 
             (oxu.email, oxu.membership_role.name,  oxu.organization.full_name))
   
      print('**** organizations ******')
      orgs = u.get_organizations()
      i = 0
      for org in orgs:
          print('%d %s %s' % 
              (i, org.full_name, org.abbreviation))
          i += 1
   
      print('**** permission checks ******')
      evn_user = User.query.filter_by(name = 'EVN User').first()
      evnmaster = User.query.filter_by(name = 'evnmaster').first()
      print("evnmaster for EVN %s \nEVN for evnmaster %s" %
           (evnmaster.may_handle_user(evn_user), evn_user.may_handle_user(evnmaster)))
      print("cert for EVN %s \nEVN for cert %s" %
           (u.may_handle_user(evn_user), evn_user.may_handle_user(u)))
      print("cert for evnmaster %s \nevnmaster for cert %s" %
           (u.may_handle_user(evnmaster), evnmaster.may_handle_user(u)))
   
   
      print('**** user.get_userss ******')
      users = u.get_users()
      for user in users:
         print("%s" % (user.name))
      
      print('**** user.get_users(evnmaster) ******')
      users = evnmaster.get_users()
      for user in users:
         print("%s" % (user.name))
     
   
   if __name__ == '__main__':
       cli()
