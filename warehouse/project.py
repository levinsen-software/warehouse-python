"""Project module"""
import uuid

from warehouse.bundle import WHBundle
from warehouse.errors import WarehouseClientException


class WHProject():
    """Class representing a warehouse project"""

    def __init__(self, wh, project_id):
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

    def find_bundles(self, query, sorting=None, limit=0):
        """Performs a search for bundles within this project"""
        items = [self.query_param()]
        if isinstance(query, str):
            items.append(self.wh.naturalQuery(query))
        elif isinstance(query, dict):
            for key, value in query.items():
                items.append(self.wh.str_matches_query(key, value))
        else:
            raise ValueError('only str and dict are supported as query types')

        query_obj = self.wh.and_query(items)
        return self.wh.internal_find_bundles(query_obj, sorting, limit)

    def find_bundle(self, query, sorting=None):
        """Performs a search for a single bundle within this project"""
        try:
            return self.find_bundles(query, sorting, 1)[0]
        except IndexError:
            return None

    def find_files(self, query, sorting=None, limit=0):
        """Performs a search for files within this project"""
        items = [self.query_param()]
        if isinstance(query, str):
            items.append(self.wh.naturalQuery(query))
        elif isinstance(query, dict):
            for key, value in query.items():
                items.append(self.wh.strMatchesQuery(key, value))
        else:
            raise ValueError('only str and dict are supported as query types')

        query_obj = self.wh.andQuery(items)
        return self.wh.internal_find_files(query_obj, sorting, limit)

    def find_file(self, query, sorting=None):
        """Performs a search for a single file within this project"""
        try:
            return self.find_files(query, sorting, 1)[0]
        except IndexError:
            return None

    def create_bundle(self, params):
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

    # Deprecated camelCase methods
    # Will be removed in future release
    queryParam = query_param
    findBundles = find_bundles
    findBundle = find_bundle
    findFiles = find_files
    findFile = find_file
    createBundle = create_bundle
