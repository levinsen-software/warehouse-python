import requests
from warehouse.file import WHFile
from warehouse.errors import WarehouseClientException

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
                q.append(self.wh.strMatchesQuery(k, v))        
        else:
            raise ValueError('only str and dict are supported as query types')

        return self.wh._findFiles(self.wh.andQuery(q), sorting, limit)
    
    def findFile(self, query, sorting=None):
        try:
            return self.findFiles(query, sorting, 1)[0]
        except IndexError:
            return None
    
    def updateProperties(self, props):
        req = []
        for key, value in props.items():
            if value is None:
                req.append({'delete': {'key': key}})
            else:
                req.append({'assign': {'key': key, 'value': value}})

        with requests.patch('%s/bundles/%s' % (self.wh.url, self.id), auth=self.wh.auth, json=req) as r:
            if r.status_code < 200 or r.status_code >= 300:
                raise WarehouseClientException('error updating properties: %s' % r.text)

            return r.json()
    
    def trash(self):
        with requests.post('%s/bundles/%s/trash' % (self.wh.url, self.id), auth=self.wh.auth) as r:
            if r.status_code < 200 or r.status_code >= 300:
                raise WarehouseClientException('error trashing bundle: %s' % r.text)

    def restore(self):
        with requests.post('%s/bundles/%s/restore' % (self.wh.url, self.id), auth=self.wh.auth) as r:
            if r.status_code < 200 or r.status_code >= 300:
                raise WarehouseClientException('error restoring bundle: %s' % r.text)
    
    def uploadFile(self, f, name=None):
        headers = {}
        if name:
            headers['x-file-property'] = 'filename=%s' % name
        with requests.post('%s/bundles/%s/files' % (self.wh.url, self.id), auth=self.wh.auth, data=f, headers=headers) as r:
            if r.status_code < 200 or r.status_code >= 300:
                raise WarehouseClientException('error uploading file: %s' % r.text)
            
            o = r.json()
            id = o.get('file_id')
            if not id:
                raise WarehouseClientException('could not upload file: no id received')

            return WHFile(self.wh, id)