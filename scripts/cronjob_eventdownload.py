#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 12:06:13 2019

@author: sebastian
"""
import json
import requests
import psycopg2
import psycopg2.extras
import zipfile

QUERY = '''
SELECT
    to_char("time.source",
            'YYYY-MM-DD"T"HH24:MI:SSOF') as "time.source",
    id,
    "feed.code" as feed,
    "source.ip",
    "source.port",
    "source.url",
    "source.asn",
    "source.geolocation.cc",
    "source.geolocation.city",
    "source.fqdn",
    "source.local_hostname",
    "source.local_ip",
    "classification.identifier",
    "classification.taxonomy",
    "classification.type",
    "comment",
    "destination.ip",
    "destination.port",
    "destination.fqdn",
    "destination.url",
    "event_description.text",
    "event_description.url",
    "extra",
    "feed.documentation",
    "malware.name",
    "protocol.application",
    "protocol.transport"
FROM events
WHERE
    "time.source" >= current_date - interval '7 days' AND
    "time.source" <= current_date AND
    (
        {where}
    )
'''

headers = {'Accept': 'application/json',
           'API-Authorization': '<API KEY>'}

organizations = requests.get('https://<URL>/api/1.0/organizations', headers=headers)
organizations.raise_for_status()

con = psycopg2.connect(database='eventdb',
                       user='statsro',
                       password='<PASSWORD>',
                       host='localhost',
                       )
con.autocommit = True  # prevents deadlocks
cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print(len(organizations.json()['organizations']))
for org_item in organizations.json()['organizations']:
    org_details = requests.get('https://<URL>/api/1.0/organizations/%s'
                               '' % org_item['id'], headers=headers)
    org_details.raise_for_status()
    asns = []
    cidrs = []
    where = []
    for ripe_handle in org_details.json()['ripe_handles']:
        handles = requests.get('https://<URL>/api/1.0/ripe/settings/%s/%s'
                               '' % (org_item['id'], ripe_handle), headers=headers)
        handles.raise_for_status()
        asns.extend([a['asn'] for a in handles.json()['asns']])
        cidrs.extend([a['cidr'] for a in handles.json()['cidrs']])
    if not asns and not cidrs:
        continue
    if asns:
        where.append('"source.asn" IN (%s)' % ', '.join(asns))
    if cidrs:
        where.append(' OR '.join(('"source.ip" << %r' % cidr for cidr in cidrs)))
    cur.execute(QUERY.format(where=' OR '.join(where)))
    print(org_item['id'], len(asns), len(cidrs), cur.rowcount)
    with zipfile.ZipFile('/home/certjobs/eventdownload/%s.json.zip'
                         '' % org_item['id'] , mode='w',
                         compression=zipfile.ZIP_DEFLATED) as handle:
        handle.writestr('events.json', json.dumps([row for row in cur],
                                                  sort_keys=True, indent=4,
                                                  separators=(',', ': ')))

