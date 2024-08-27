import os
from typing import Any, List, Dict
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from dbutils.pooled_db import PooledDB

load_dotenv()

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.pool = PooledDB(
                creator=pymysql,
                maxconnections=6,
                mincached=2,
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db=os.getenv('DB_NAME'),
                charset=os.getenv('DB_CHARSET', 'utf8mb4'),
                cursorclass=DictCursor
            )
        return cls._instance

    def execute_query(self, sql: str, params: tuple = None) -> List[Dict[str, Any]]:
        with self.pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()

    def execute_single_query(self, sql: str, params: tuple = None) -> Dict[str, Any] | None:
        with self.pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()

db = DatabaseManager()