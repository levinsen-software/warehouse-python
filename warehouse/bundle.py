import requests

class WHBundle():
    def __init__(self, wh, id):
        self.wh = wh
        self.id = id
    
    def __str__(self):
        return 'WHBundle(id=%s)' % self.id

    def getProperties(self):
        with requests.get('%s/bundles/%s' % (self.wh.url, self.id), auth=self.wh.auth) as r:
            return r.json()

    def files(self):
        with requests.get('%s/bundles/%s' % (self.wh.url, self.id), auth=self.wh.auth) as r:
            j = r.json()
            files = []
            for f in j['files']:
                files.append(self.wh.file(f['file_id']))
            
            return files

    def findFiles(self, query, sorting=None, limit=0):
        q = [self.wh.equalsQuery('bundle.id', self.id)]

        if type(query) is str:
            q.append(self.wh.naturalQuery(query))
        elif type(query) is dict:
            for k, v in query.items():
                q.append(self.strMatchesQuery(k, v))        
        else:
            raise ValueError('only str and dict are supported as query types')
        print(self.wh.andQuery(q))
        return self.wh._findFiles(self.wh.andQuery(q), sorting, limit)
    
    def findFile(self, query, sorting):
        return findFiles(query, sorting, 1)