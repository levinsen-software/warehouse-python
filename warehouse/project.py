"""Project module"""
from __future__ import annotations

from warehouse.file import WHFile
from warehouse.bundle import WHBundle
from warehouse.errors import WarehouseClientException
from warehouse.sorting import Sorting

import uuid
from typing import Optional, Dict, Any, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    from warehouse.client import Client

class WHProject():
    """Class representing a warehouse project"""

    def __init__(self, wh: Client, project_id: str):
        self.wh = wh
        self.id = project_id

    def __str__(self):
        return 'WHProject(id=%s)' % self.id

    def query_param(self):
        """Returns a query object identifying this project"""
        try:
            uuid.UUID(self.id)
            return self.wh.equalsQuery('project.id', self.id)
        except ValueError:
            return self.wh.equalsQuery('project.name', self.id)

    def get_info(self):
        """Returns a dictionary with project info"""
        with self.wh.session.get('%s/projects/%s' % (
            self.wh.url, self.id.replace('/', '%2F'))) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error getting project info: %s' % req.text)

            return req.json()

    def find_bundles(self, query: Union[str, Dict[str, Any]], sorting: Optional[Sorting]=None, limit: int=0) -> List[WHBundle]:
        """Performs a search for bundles within this project"""
        # pyright: reportUnnecessaryIsInstance=false
        items = [self.query_param()]
        if isinstance(query, str):
            items.append(Client.naturalQuery(query))
        elif isinstance(query, dict):
            for key, value in query.items():
                items.append(Client.str_matches_query(key, value))
        else:
            raise ValueError('only str and dict are supported as query types')

        query_obj = Client.and_query(items)
        return self.wh.internal_find_bundles(query_obj, sorting, limit)

    def find_bundle(self, query: Union[str, Dict[str, Any]], sorting: Optional[Sorting]=None) -> Optional[WHBundle]:
        """Performs a search for a single bundle within this project"""
        try:
            return self.find_bundles(query, sorting, 1)[0]
        except IndexError:
            return None

    def find_files(self, query: Union[str, Dict[str, Any]], sorting: Optional[Sorting]=None, limit: int=0) -> List[WHFile]:
        """Performs a search for files within this project"""
        items = [self.query_param()]
        if isinstance(query, str):
            items.append(Client.naturalQuery(query))
        elif isinstance(query, dict):
            for key, value in query.items():
                items.append(Client.strMatchesQuery(key, value))
        else:
            raise ValueError('only str and dict are supported as query types')

        query_obj = Client.andQuery(items)
        return self.wh.internal_find_files(query_obj, sorting, limit)

    def find_file(self, query: Union[str, Dict[str, Any]], sorting: Optional[Sorting]=None) -> Optional[WHFile]:
        """Performs a search for a single file within this project"""
        try:
            return self.find_files(query, sorting, 1)[0]
        except IndexError:
            return None

    def create_bundle(self, params: Dict[str, Any]) -> WHBundle:
        """Creates a bundle within this project, and returns the WHBundle object"""
        url = '%s/projects/%s/bundles' % (self.wh.url,
                                          self.id.replace('/', '%2F'))
        with self.wh.session.post(url, json=params) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException('returned error: %s' % req.text)

            json_res = req.json()

            bundle_id = json_res.get('bundle_id')
            if not bundle_id:
                raise WarehouseClientException('could not create bundle')

            return WHBundle(self.wh, bundle_id)
    
    def delete(self):
        """Deletes the project"""
        with self.wh.session.delete('%s/projects/%s' % (self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error deleting project: %s' % req.text)

    # Deprecated camelCase methods
    # Will be removed in future release
    queryParam = query_param
    findBundles = find_bundles
    findBundle = find_bundle
    findFiles = find_files
    findFile = find_file
    createBundle = create_bundle
