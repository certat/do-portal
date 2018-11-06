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
                  'cidrs')

    def __init__(self, ripe_org_hdl):
        self._cidrs = None

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
            return None

        raise AttributeError('no such handle')

    @property
    def cidrs(self):
        if self._cidrs:
            return self._cidrs
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

        self._cidrs = [row[0] for row in results]
        return self._cidrs;

