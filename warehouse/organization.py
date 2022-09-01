"""Organization module"""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from warehouse.project import WHProject
from warehouse.errors import WarehouseClientException

if TYPE_CHECKING:
    from warehouse.client import Client


class WHOrganization():
    """Class representing a warehouse organization"""

    def __init__(self, wh: Client, organization_id: str):
        self.wh = wh
        self.id = organization_id

    def __str__(self):
        return 'WHOrganization(id=%s)' % self.id

    def query_param(self):
        """Returns a query object identifying this project"""
        try:
            uuid.UUID(self.id)
            return self.wh.equalsQuery('organization.id', self.id)
        except ValueError:
            return self.wh.equalsQuery('organization.name', self.id)

    def get_info(self):
        """Returns a dictionary with project info"""
        with self.wh.session.get('%s/organizations/%s' % (
            self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error getting project info: %s' % req.text)

            return req.json()
    
    def delete(self):
        """Deletes the organization"""
        with self.wh.session.delete('%s/organizations/%s' % (self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error deleting organization: %s' % req.text)

    
    def create_project(self, name: str):
        with self.wh.session.post('%s/organizations/%s/projects' % (self.wh.url, self.id), json={"name": name}) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException('returned error: %s' % req.text)
            
            json_res = req.json()

            return WHProject(self.wh, json_res['project_id'])