import os
from pathlib import Path

import dotenv

dotenv.load_dotenv(Path('.env'))


DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


REDIS_HOST = 'localhost'
REDIS_PORT = 6379


DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


DATE_FORMAT = "%d.%m.%Y"
