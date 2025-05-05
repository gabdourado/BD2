from MySQLdb import connect
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        charset="utf8mb4",
        autocommit=False
    )