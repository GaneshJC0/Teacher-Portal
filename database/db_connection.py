import sqlite3
import os
from contextlib import contextmanager
from config import Config

class DatabaseConnection:
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Ensure the database directory and file exist"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    def execute_update(self, query, params=None):
        """Execute an update/insert/delete query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
    
    def execute_insert(self, query, params=None):
        """Execute an insert query and return the last row id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid

# Global database instance
db = DatabaseConnection()