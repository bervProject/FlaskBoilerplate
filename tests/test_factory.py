from web import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello/')
    assert b'Hello, World!' in response.data

def test_hello_with_name(client):
    response = client.get('/hello/berv')
    assert b'Hello berv' in response.data
