import warehouse as wh
import helper
import tempfile

client = helper.get_wh_client()

def test_file_properties():
    with helper.TemporaryProject(client) as p:
        props = {
            'integer': 123,
            'string': "qwerty",
            'json': {'key': 'value'},
            'bool': True,
            'float': 1.234
        }

        bundle = p.create_bundle(props)
        file = bundle.upload_file(b'data', 'testfile')
        file.update_properties(props)


        read_props = file.get_properties()
        for key, val in props.items():
            assert read_props.get(key) == val
        
        file.update_properties({'integer': 321, 'json': None, 'new': 'testvalue'})

        expected_props = {
            'integer': 321,
            'string': "qwerty",
            'bool': True,
            'float': 1.234,
            'new': 'testvalue'
        }

        read_props = file.get_properties()
        for key, val in expected_props.items():
            assert read_props.get(key) == val
        
        assert read_props.get('json') is None

def test_file_download():
    with helper.TemporaryProject(client) as p:
        bundle = p.create_bundle({})
        file = bundle.upload_file(b'data', 'testfile')

        with tempfile.NamedTemporaryFile() as f:
            file.download(f.name)

            assert open(f.name, 'rb').read() == b'data'
