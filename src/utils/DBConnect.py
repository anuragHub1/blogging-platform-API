import os
from dotenv import load_dotenv
from src.utils.MySQLWrapper import DBConnection

env_file = ".env"
load_dotenv(dotenv_path=env_file)


def connect() -> DBConnection:
    try:
        db = DBConnection(
            host=os.getenv("DB_HOST", "localhost"),
            username=os.getenv("DB_USERNAME", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", ""),
        )
        db.connect()
        return db
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")


def get_db():
    db = connect()
    try:
        yield db
    finally:
        if db:
            db.close_connection()
