import os
import time
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_connection(retries=5, delay=3):
    db_config = {
        'host': os.getenv('DB_HOST', 'db'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'cursorclass': pymysql.cursors.DictCursor,
        'autocommit': True
    }
    for attempt in range(retries):
        try:
            conn = pymysql.connect(**db_config)
            return conn
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e
