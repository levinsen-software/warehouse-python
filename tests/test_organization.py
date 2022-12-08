import warehouse as wh
import helper

client = helper.get_wh_client()

def test_organization_info():
    org = client.organization('test')
    org.get_info()