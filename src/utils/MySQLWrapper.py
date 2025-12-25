import mysql.connector
from mysql.connector import Error
from typing import Any, Optional, List
from mysql.connector.cursor import MySQLCursor


class DBConnection:
    def __init__(self, host: str, username: str, password: str, database: str):
        self.config = {
            "host": host,
            "username": username,
            "password": password,
            "database": database,
        }
        self.connection: Optional[mysql.connector.MySQLConnection] = None
        self.cursor: Optional[MySQLCursor] = None

    def connect(self):
        if self.connection and self.connection.is_connected():
            return
        self.connection = mysql.connector.MySQLConnection(**self.config)
        self.cursor = self.connection.cursor(dictionary=True)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(
        self, query: str, params: Optional[tuple] = None, commit: bool = False
    ) -> List[dict]:

        self.connect()
        assert self.connection is not None
        assert self.cursor is not None

        try:
            self.cursor.execute(query, params or ())
            if commit:
                self.connection.commit()

            if self.cursor.with_rows:
                return self.cursor.fetchall()  # type: ignore

            return []

        except Error as e:
            self.connection.rollback()
            raise e
