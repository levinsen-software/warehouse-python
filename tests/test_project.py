import warehouse as wh
import helper

client = helper.get_wh_client()

def test_project_info():
    with helper.TemporaryProject(client) as p:
        p.get_info()

def test_find_bundles():
    with helper.TemporaryProject(client) as p:
        for _ in range(4):
            p.create_bundle({})

        assert len(p.find_bundles('')) is 4

def test_find_bundle():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        assert type(p.find_bundle('')) is wh.WHBundle

def test_find_files():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        for _ in range(4):
            bundle.upload_file(b'test', 'testfile')
        
        assert len(p.find_files('')) is 4

def test_find_file():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        bundle.upload_file(b'test', 'testfile')
        assert type(p.find_file('')) is wh.WHFile