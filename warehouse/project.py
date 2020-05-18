import requests
import uuid

from warehouse.bundle import WHBundle
from warehouse.errors import WarehouseClientException

class WHProject():
    def __init__(self, wh, id):
        self.wh = wh
        self.id = id

    def __str__(self):
        return 'WHProject(id=%s)' % self.id

    def queryParam(self):
        try:
            uuid.UUID(self.id)
            return self.wh.equalsQuery('project.id', self.id)
        except ValueError:
            return self.wh.equalsQuery('project.name', self.id)
    
    def findBundles(self, query, sorting=None, limit=0):
        items = [self.queryParam()]
        if type(query) is str:
            items.append(self.wh.naturalQuery(query))
        elif type(query) is dict:
            for k, v in query.items():
                items.append(self.wh.strMatchesQuery(k, v))
        else:
            raise ValueError('only str and dict are supported as query types')
        
        q = self.wh.andQuery(items)
        return self.wh._findBundles(q, sorting, limit)
    
    def findBundle(self, query, sorting):
        try:
            return self.findBundles(query, sorting, 1)[0]
        except IndexError:
            return None

    def findFiles(self, query, sorting=None, limit=0):
        items = [self.queryParam()]
        if type(query) is str:
            items.append(self.wh.naturalQuery(query))
        elif type(query) is dict:
            for k, v in query.items():
                items.append(self.wh.strMatchesQuery(k, v))
        else:
            raise ValueError('only str and dict are supported as query types')
        

        q = self.wh.andQuery(items)
        return self.wh._findFiles(q, sorting, limit)

    def findFile(self, query, sorting=None):
        try:
            return self.findFiles(query, sorting, 1)[0]
        except IndexError:
            return None
    
    def createBundle(self, params):
        with requests.post('%s/projects/%s/bundles' % (self.wh.url, self.id.replace('/', '%2F')), auth=self.wh.auth, json=params) as r:
            if r.status_code < 200 or r.status_code >= 300:
                raise WarehouseClientException('returned error: %s' % r.text)

            j = r.json()

            id = j.get('bundle_id')
            if not id:
                raise WarehouseClientException('could not create bundle')
            
            return WHBundle(self.wh, id)