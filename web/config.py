import os


class Config:
    PONY = {
        'provider': 'postgres',
        'user': os.environ.get('PG_USER', 'postgres'),
        'password': os.environ.get('PG_PASSWORD', 'devpassword'),
        'host': os.environ.get('PG_HOST', 'localhost'),
        'database': os.environ.get('PG_DB_NAME', 'bookdb')
    }
