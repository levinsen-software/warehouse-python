import requests
from . bundle import WHBundle
from . file import WHFile
from . sorting import Sorting

class UserCredentialsAuth():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, r):
        return requests.auth.HTTPBasicAuth(self.username, self.password)(r)

class TokenAuth():
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'token %s' % self.token
        return r

class ApikeyAuth():
    def __init__(self, apikey):
        self.apikey = apikey

    def __call__(self, r):
        r.headers['Authorization'] = 'apikey %s' % self.apikey
        return r


class Client():
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth

    def ping(self):
        with requests.get('%s/ping' % self.url, auth=self.auth) as r:
            r.raise_for_status()
    
    def checkToken(self):
        with requests.post('%s/checkToken' % self.url, auth=self.auth) as r:
            r.raise_for_status()
    
    def andQuery(self, items):
        return {'and': items}

    def equalsQuery(self, key, value):
        return {'equals': {'key': key, 'value': value}}

    def strMatchesQuery(self, key, value):
        return {'str_pattern_matches': {'key': key, 'value': value}}
    
    def naturalQuery(self, query):
        return {'natural_query': query}
    
    def bundle(self, id):
        return WHBundle(self, id)
    
    def file(self, id):
        return WHFile(self, id)
    
    # def projects(self):
    #     with requests.get('%s/organizations' % self.url, auth=self.auth) as r:
    #         j = r.json()
    #         projects = []
    #         for o in j['organizations']:
    #             for p in o['projects']:
    #                 projects.append('%s/%s' % (o['organization_name'], p['project_name']))
        
    #         return projects
    
    def _findBundles(self, query, sorting=None, limit=0):
        if not sorting:
            sorting = Sorting(None, None, None)
        
        keys = ['bundle.id']

        if sorting.key:
            keys.append(sorting.key)

        q = {
            'table': 'bundles',
            'keys': keys,
            'sorting': sorting.as_dict(),
            'query': query
        }

        if limit > 0:
            q['limit'] = limit

        bundles = []
        with requests.post('%s/search/keys' % self.url, auth=self.auth, json=q) as r:
            j = r.json()

            for b in j['results']:
                bundles.append(self.bundle(b[0]))

        return bundles
    
    def findBundles(self, query, sorting=None, limit=0):
        if type(query) is str:
            q = self.naturalQuery(query)
        elif type(query) is dict:
            items = []
            for k, v in query.items():
                items.append(self.strMatchesQuery(k, v))
            
            q = self.andQuery(items)
        else:
            raise ValueError('only str and dict are supported as query types')

        return self._findBundles(q, sorting, limit)
    
    def findBundle(self, query, sorting):
        return self.findBundles(query, sorting, 1)

    def _findFiles(self, query, sorting=None, limit=0):
        if not sorting:
            sorting = Sorting(None, None, None)
        
        keys = ['file.id']

        if sorting.key:
            keys.append(sorting.key)

        q = {
            'table': 'files',
            'keys': keys,
            'sorting': sorting.as_dict(),
            'query': query
        }
        
        if limit > 0:
            q['limit'] = limit

        files = []
        with requests.post('%s/search/keys' % self.url, auth=self.auth, json=q) as r:
            j = r.json()

            for f in j['results']:
                files.append(self.file(f[0]))

        return files
    
    def findFiles(self, query, sorting=None, limit=0):
        if type(query) is str:
            q = self.naturalQuery(query)
        elif type(query) is dict:
            items = []
            for k, v in query.items():
                items.append(self.strMatchesQuery(k, v))
            
            q = self.andQuery(items)
        else:
            raise ValueError('only str and dict are supported as query types')

        return self._findFiles(q, sorting, limit)

    def findFile(self, query, sorting):
        return self.findFiles(query, sorting, 1)