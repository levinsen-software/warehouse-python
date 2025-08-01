"""File module"""
from __future__ import annotations

import os
import shutil

from warehouse.errors import WarehouseClientException

from typing import Dict, Any, List, Optional

class WHFile():
    """Class representing a single warehouse file"""

    def __init__(self, wh: 'Client', file_id: str):
        self.wh = wh
        self.id = file_id

    def __str__(self):
        return 'WHFile(id=%s)' % self.id

    def get_properties(self) -> Dict[str, Any]:
        """Returns the properties associated with this file"""
        with self.wh.session.get('%s/files/%s' % (self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error getting properties: %s' % req.text)
            return req.json()

    def update_properties(self, props: Dict[str, Any]):
        """Update the file properties with the provided values"""
        request_json: List[Dict[str, Any]] = []
        for key, value in props.items():
            if value is None:
                request_json.append({'delete': {'key': key}})
            else:
                request_json.append({'assign': {'key': key, 'value': value}})

        with self.wh.session.patch('%s/files/%s' % (self.wh.url, self.id), json=request_json) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error updating properties: %s' % req.text)

            return req.json()

    def trash(self):
        """Trash this file"""
        with self.wh.session.post('%s/files/%s/trash' % (self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error trashing file: %s' % req.text)

    def restore(self):
        """Restore this file from trash"""
        with self.wh.session.post('%s/files/%s/restore' % (self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error restoring file: %s' % req.text)
    
    def delete(self):
        """Permanently delete this file"""
        with self.wh.session.delete('%s/files/%s' % (self.wh.url, self.id)) as req:
            if req.status_code < 200 or req.status_code >= 300:
                raise WarehouseClientException(
                    'error deleting file: %s' % req.text)


    def download(self, path: Optional[str]=None, create_dirs: bool=False):
        """Download this file"""
        url = '%s/files/%s/download' % (self.wh.url, self.id)
        with self.wh.session.get(url, stream=True) as req:
            req.raise_for_status()

            filename = "download"

            try:
                filename = req.headers['x-content-filename']
            except KeyError:
                pass
    
            if path is not None:
                basename = os.path.basename(path)
                if not basename:
                    filename = os.path.join(os.path.dirname(path), filename)
                else:
                    filename = path

                if create_dirs:
                    os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename + '.part', 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            shutil.move(filename + '.part', filename)
            return filename

    # Deprecated camelCase methods
    # Will be removed in future release
    getProperties = get_properties
    updateProperties = update_properties
