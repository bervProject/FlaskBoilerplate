import os
import tempfile
import pytest
from web import create_app


@pytest.fixture
def app():

    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'PONY': {
            'provider': 'postgres',
            'user': os.environ.get('PG_USER', 'postgres'),
            'password': os.environ.get('PG_PASSWORD', 'devpassword'),
            'host': os.environ.get('PG_HOST', 'localhost'),
            'database': os.environ.get('PG_DB_NAME', 'bookdb')
        }
    })

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
