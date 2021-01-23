"""
Warehouse Client

This module contains the main client for warehouse communication.
"""

import requests
from warehouse.bundle import WHBundle
from warehouse.file import WHFile
from warehouse.project import WHProject
from warehouse.sorting import Sorting
from warehouse.errors import WarehouseClientException


class UserCredentialsAuth():
    """Authenticate using username/password"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, req):
        return requests.auth.HTTPBasicAuth(self.username, self.password)(req)


class TokenAuth():
    """Authenticate using a web token"""

    def __init__(self, token):
        self.token = token

    def __call__(self, req):
        req.headers['Authorization'] = 'token %s' % self.token
        return req


class ApikeyAuth():
    """Authenticate using an API key"""

    def __init__(self, apikey):
        self.apikey = apikey

    def __call__(self, req):
        req.headers['Authorization'] = 'apikey %s' % self.apikey
        return req


class Client():
    """Main client object for warehouse"""

    def __init__(self, url, auth, verify=True):
        self.url = url
        self.auth = auth
        self.session = requests.Session()

        self.session.auth = auth
        self.session.verify = verify

    def ping(self):
        """Tests the connection to warehouse"""
        with self.session.get('%s/ping' % self.url, auth=self.auth) as req:
            req.raise_for_status()

    def check_token(self):
        """Tests the provided authentication method"""
        try:
            with self.session.post('%s/checkToken' % self.url, auth=self.auth) as req:
                req.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise WarehouseClientException('Permission denied') from e

            raise WarehouseClientException(
                'Unknown server response: %d' % e.response.status_code) from e

        except requests.RequestException as e:
            raise WarehouseClientException('Connection error') from e

    @staticmethod
    def and_query(items):
        """Returns a warehouse and query"""
        return {'and': items}

    @staticmethod
    def equals_query(key, value):
        """Returns a warehouse equals query"""
        return {'equals': {'key': key, 'value': value}}

    @staticmethod
    def str_matches_query(key, value):
        """Returns a warehouse string matching query"""
        return {'str_pattern_matches': {'key': key, 'value': value}}

    @staticmethod
    def natural_query(query):
        """Returns a natural query"""
        return {'natural_query': query}

    def bundle(self, bundle_id):
        """Returns a WHBundle object with the provided ID"""
        return WHBundle(self, bundle_id)

    def file(self, file_id):
        """Returns a WHFile object with the provided ID"""
        return WHFile(self, file_id)

    def project(self, project_id):
        """Returns a WHProject object with the provided ID"""
        return WHProject(self, project_id)

    def projects(self):
        """Returns a list of all accessible warehouse projects"""
        with self.session.get('%s/organizations' % self.url) as req:
            json_res = req.json()
            _projects = []
            for organization in json_res['organizations']:
                for project in organization['projects']:
                    _projects.append(self.project(
                        '%s/%s' % (organization['organization_name'], project['project_name'])))

            return _projects

    def internal_find_bundles(self, query, sorting=None, limit=0):
        """Internal bundle lookup method"""
        if not sorting:
            sorting = Sorting(None, None, None)

        keys = ['bundle.id']

        if sorting.key:
            keys.append(sorting.key)

        query_obj = {
            'table': 'bundles',
            'keys': keys,
            'sorting': sorting.as_dict(),
            'query': query
        }

        if limit > 0:
            query_obj['limit'] = limit

        bundles = []
        with self.session.post('%s/search/keys' % self.url, json=query_obj) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error searching: %s' % req.text)
            json_res = req.json()

            for bundle in json_res['results']:
                bundles.append(self.bundle(bundle[0]))

        return bundles

    def find_bundles(self, query, sorting=None, limit=0):
        """Perform a search for bundles with the given parameters"""
        if isinstance(query, str):
            query_obj = self.natural_query(query)
        elif isinstance(query, dict):
            items = []
            for key, value in query.items():
                items.append(self.str_matches_query(key, value))

            query_obj = self.and_query(items)
        else:
            raise ValueError('only str and dict are supported as query types')

        return self.internal_find_bundles(query_obj, sorting, limit)

    def find_bundle(self, query, sorting=None):
        """Perform a search for a single bundle"""
        try:
            return self.find_bundles(query, sorting, 1)[0]
        except IndexError:
            return None

    def internal_find_files(self, query, sorting=None, limit=0):
        """Internal file lookup method"""
        if not sorting:
            sorting = Sorting(None, None, None)

        keys = ['file.id']

        if sorting.key:
            keys.append(sorting.key)

        query_obj = {
            'table': 'files',
            'keys': keys,
            'sorting': sorting.as_dict(),
            'query': query
        }

        if limit > 0:
            query_obj['limit'] = limit

        files = []
        with self.session.post('%s/search/keys' % self.url, json=query_obj) as req:
            json_res = req.json()

            for f in json_res['results']:
                files.append(self.file(f[0]))

        return files

    def find_files(self, query, sorting=None, limit=0):
        """Perform a search for files with the given parameters"""
        if isinstance(query, str):
            query_obj = self.natural_query(query)
        elif isinstance(query, dict):
            items = []
            for key, value in query.items():
                items.append(self.str_matches_query(key, value))

            query_obj = self.and_query(items)
        else:
            raise ValueError('only str and dict are supported as query types')

        return self.internal_find_files(query_obj, sorting, limit)

    def find_file(self, query, sorting=None):
        """Perform a search for a single file"""
        try:
            return self.find_files(query, sorting, 1)[0]
        except IndexError:
            return None

    # Deprecated camelCase methods
    # Will be removed in future release
    checkToken = check_token
    andQuery = and_query
    equalsQuery = equals_query
    strMatchesQuery = str_matches_query
    naturalQuery = natural_query
    findBundles = find_bundles
    findBundle = find_bundle
    findFiles = find_files
    findFile = find_file
