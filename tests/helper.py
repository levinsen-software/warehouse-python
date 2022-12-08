import os
import random
import string
import uuid
import warehouse as wh

def random_string(length: int) -> str:
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])

def get_wh_client():
    host = os.environ['WAREHOUSE_HOST']
    apikey = os.environ['WAREHOUSE_APIKEY']

    auth = wh.ApikeyAuth(apikey)
    return wh.Client(host, auth)

class TemporaryProject():
    organization = "test"

    def __init__(self, client):
        self.client = client
        self.org = client.organization(TemporaryProject.organization)

    def __enter__(self):
        project_name = str(uuid.uuid4())
        self.project = self.org.create_project(project_name)

        return self.project

    def __exit__(self, type, val, tb):
        for bundle in self.project.find_bundles(''):
            bundle.trash()
            bundle.delete()
        
        self.project.delete()
