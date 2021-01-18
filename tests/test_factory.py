from web import create_app


def test_config():
    assert not create_app({
        PONY={
            'provider': 'postgres',
            'user': os.environ.get('PG_USER', 'postgres'),
            'password': os.environ.get('PG_PASSWORD', 'devpassword'),
            'host': os.environ.get('PG_HOST', 'localhost'),
            'database': os.environ.get('PG_DB_NAME', 'bookdb')
        }
    }).testing
    assert create_app({'TESTING': True,
                       PONY={
                           'provider': 'postgres',
                           'user': os.environ.get('PG_USER', 'postgres'),
                           'password': os.environ.get('PG_PASSWORD', 'devpassword'),
                           'host': os.environ.get('PG_HOST', 'localhost'),
                           'database': os.environ.get('PG_DB_NAME', 'bookdb')
                       }}).testing


def test_hello(client):
    response = client.get('/hello/')
    assert b'Hello, World!' in response.data

def test_hello_with_name(client):
    response = client.get('/hello/berv')
    assert b'Hello berv' in response.data
