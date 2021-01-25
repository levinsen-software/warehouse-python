"""Bundle module"""
from warehouse.file import WHFile
from warehouse.errors import WarehouseClientException


class WHBundle():
    """Class representing a single warehouse bundle"""

    def __init__(self, wh, bundle_id):
        self.wh = wh
        self.id = bundle_id

    def __str__(self):
        return 'WHBundle(id=%s)' % self.id

    def get_properties(self):
        """Returns a dictionary with properties for the bundle"""
        with self.wh.session.get('%s/bundles/%s' % (self.wh.url, self.id)) as req:
            return req.json()

    def files(self):
        """Returns a list of the files contained in the bundle"""
        with self.wh.session.get('%s/bundles/%s' % (self.wh.url, self.id)) as req:
            json_res = req.json()
            files = []
            for f in json_res['files']:
                files.append(self.wh.file(f['file_id']))

            return files

    def find_files(self, query, sorting=None, limit=0):
        """Performs a search for files in the bundle"""
        query_obj = [self.wh.equals_query('bundle.id', self.id)]

        if isinstance(query, str):
            query_obj.append(self.wh.natural_query(query))
        elif isinstance(query, dict):
            for key, value in query.items():
                query_obj.append(self.wh.str_matches_query(key, value))
        else:
            raise ValueError('only str and dict are supported as query types')

        return self.wh.internal_find_files(self.wh.andQuery(query_obj), sorting, limit)

    def find_file(self, query, sorting=None):
        """Performs a search for a single file"""
        try:
            return self.find_files(query, sorting, 1)[0]
        except IndexError:
            return None

    def update_properties(self, props):
        """Sets the provided properties for the bundle

        props: dict"""
        req = []
        for key, value in props.items():
            if value is None:
                req.append({'delete': {'key': key}})
            else:
                req.append({'assign': {'key': key, 'value': value}})

        with self.wh.session.patch('%s/bundles/%s' % (self.wh.url, self.id), json=req) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error updating properties: %s' % req.text)

            return req.json()

    def trash(self):
        """Trashes the bundle"""
        with self.wh.session.post('%s/bundles/%s/trash' % (self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error trashing bundle: %s' % req.text)

    def restore(self):
        """Restores the bundle from trash"""
        with self.wh.session.post('%s/bundles/%s/restore' % (self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error restoring bundle: %s' % req.text)

    def upload_file(self, f, name=None):
        """Uploads the passed file object to the bundle"""
        headers = {}
        if name:
            headers['x-file-property'] = 'filename=%s' % name

        url = '%s/bundles/%s/files' % (self.wh.url, self.id)
        with self.wh.session.post(url, data=f, headers=headers) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error uploading file: %s' % req.text)

            json_res = req.json()
            file_id = json_res.get('file_id')
            if not file_id:
                raise WarehouseClientException(
                    'could not upload file: no id received')

            return WHFile(self.wh, file_id)

    # Deprecated camelCase methods
    # Will be removed in future release
    getProperties = get_properties
    findFiles = find_files
    findFile = find_file
    updateProperties = update_properties
    uploadFile = upload_file
