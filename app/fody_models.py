import os
import datetime
from app import db, login_manager, config
from sqlalchemy import desc, event, text
import time
from pprint import pprint

_config = config.get(os.getenv('DO_CONFIG') or 'default')

class FodyOrganization():
    __public__ = ('ripe_org_hdl',
                  'name',
                  'organisation_automatic_id',
                  'cidrs',
                  'asns',
                  'abusecs')

    cidrs   = None
    asns    = None
    abusecs = None

    def __init__(self, ripe_org_hdl):
        results = db.engine.execute(
            text("""
            select ripe_org_hdl,
                   name,
                   organisation_automatic_id
              from fody.organisation_automatic
             where ripe_org_hdl = :b_ripe_org_hdl
            """
            ), {'b_ripe_org_hdl': ripe_org_hdl})

        for row in results:
            self.ripe_org_hdl = row[0]
            self.name = row[1]
            self.organisation_automatic_id = row[2]
            c = self._cidrs
            a = self._asns
            ac = self._abusecs
            return None

        raise AttributeError('no such handle')

    @property
    def _cidrs(self):
        if self.cidrs:
            return self.cidrs
        results = db.engine.execute(
            text("""
            select address
                   from fody.organisation_automatic oa
                   join fody.organisation_to_network_automatic o2na
                     on oa.organisation_automatic_id =
                        o2na.organisation_automatic_id
                   join fody.network_automatic na
                     on o2na.network_automatic_id = na.network_automatic_id
                      where ripe_org_hdl = :b_ripe_org_hdl
            """
            ), {'b_ripe_org_hdl': self.ripe_org_hdl})

        self.cidrs = [row[0] for row in results]
        return self.cidrs;

    @property
    def _asns(self):
        if self.asns:
            return self.asns
        results = db.engine.execute(
            text("""
            select asn
                   from fody.organisation_automatic oa
                   join fody.organisation_to_asn_automatic o2aa
                     on oa.organisation_automatic_id =
                        o2aa.organisation_automatic_id
                      where ripe_org_hdl = :b_ripe_org_hdl
            """
            ), {'b_ripe_org_hdl': self.ripe_org_hdl})

        self.asns = [str(row[0]) for row in results]
        return self.asns;

    @property
    def _abusecs(self):
        if self.abusecs:
            return self.abusecs
        results = db.engine.execute(
            text("""
            select email
                   from fody.organisation_automatic oa
                   join fody.contact_automatic ca
                     on oa.organisation_automatic_id =
                        ca.organisation_automatic_id
                      where ripe_org_hdl = :b_ripe_org_hdl
            """
            ), {'b_ripe_org_hdl': self.ripe_org_hdl})

        self.abusecs = [str(row[0]) for row in results]

