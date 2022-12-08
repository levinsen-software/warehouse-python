import warehouse as wh
import helper

client = helper.get_wh_client()

def test_bundle_properties():
    with helper.TemporaryProject(client) as p:
        props = {
            'integer': 123,
            'string': "qwerty",
            'json': {'key': 'value'},
            'bool': True,
            'float': 1.234
        }

        bundle = p.create_bundle(props)

        read_props = bundle.get_properties()
        for key, val in props.items():
            assert read_props.get(key) == val
        
        
        bundle.update_properties({'integer': 321, 'json': None, 'new': 'testvalue'})

        expected_props = {
            'integer': 321,
            'string': "qwerty",
            'bool': True,
            'float': 1.234,
            'new': 'testvalue'
        }

        read_props = bundle.get_properties()
        for key, val in expected_props.items():
            assert read_props.get(key) == val
        
        assert read_props.get('json') is None

    
def test_files():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})

        for _ in range(5):
            bundle.upload_file(b'data', 'filename')
        
        files = bundle.files()
        
        assert len(files) == 5

def test_find_files():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        for _ in range(4):
            bundle.upload_file(b'test', 'testfile')
        
        assert len(bundle.find_files('')) is 4

def test_find_file():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        bundle.upload_file(b'test', 'testfile')
        assert type(bundle.find_file('')) is wh.WHFile