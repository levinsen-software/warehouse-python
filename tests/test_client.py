import pytest
import warehouse as wh
import helper

client = helper.get_wh_client()

def test_connect():
    client.ping()

def test_connect_fail():
    with pytest.raises(Exception):
        wh.Client('https://0.0.0.0', None).ping()

def test_auth():
    client.check_token()

def test_projects():
    client.projects()

def test_populate():
    with helper.TemporaryProject(client) as p:
        for i in range(10):
            props = {
                'version': f'1.0.{i}',
            }

            for i in range(10):
                property_name = helper.random_string(10)
                property_value = helper.random_string(10)

                props[property_name] = property_value

            bundle = p.create_bundle(props)
            bundle.upload_file(b'test', 'testfile')

def test_find_bundles():
    with helper.TemporaryProject(client) as p:
        for _ in range(4):
            p.create_bundle({})

        assert len(client.find_bundles('')) >= 4

def test_find_bundle():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        assert type(client.find_bundle('')) is wh.WHBundle

def test_find_files():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        for _ in range(4):
            bundle.upload_file(b'test', 'testfile')
        
        assert len(client.find_files('')) >= 4

def test_find_file():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        bundle.upload_file(b'test', 'testfile')
        assert type(client.find_file('')) is wh.WHFile

