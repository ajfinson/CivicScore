"""Postgres connection pool"""
import psycopg2
from psycopg2 import pool
from app.config import settings


class DatabasePool:
    """PostgreSQL connection pool manager"""
    
    def __init__(self):
        self.connection_pool = None
    
    def initialize(self):
        """Initialize connection pool"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,  # min and max connections
                settings.database_url
            )
            print("Database connection pool created")
        except Exception as e:
            print(f"Error creating connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        return self.connection_pool.getconn()
    
    def return_connection(self, connection):
        """Return a connection to the pool"""
        self.connection_pool.putconn(connection)
    
    def close_all(self):
        """Close all connections"""
        if self.connection_pool:
            self.connection_pool.closeall()


# Global pool instance
db_pool = DatabasePool()
