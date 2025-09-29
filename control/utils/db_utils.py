"""
Database utility functions for better connection management
"""
from contextlib import contextmanager
from .bd.db_connection import Connection


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Ensures proper connection handling and cleanup.
    
    Usage:
        with get_db_connection() as conn:
            # Use connection here
            pass
    """
    conn = None
    try:
        conn = Connection.connect()
        if not conn:
            raise Exception("No se pudo establecer conexión con la base de datos")
        yield conn
    except Exception as e:
        print(f"Error en conexión de base de datos: {e}")
        raise
    finally:
        if conn:
            conn.close()


def safe_execute_query(conn, query, params=None, fetch_one=False, fetch_all=False):
    """
    Safely execute a database query with proper error handling.
    
    Args:
        conn: Database connection
        query (str): SQL query to execute
        params (tuple, optional): Query parameters
        fetch_one (bool): Whether to fetch one result
        fetch_all (bool): Whether to fetch all results
        
    Returns:
        Query result or None if error
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            return cursor.rowcount
    except Exception as e:
        print(f"Error ejecutando consulta: {e}")
        return None


def get_columns_from_cursor(cursor):
    """
    Get column names from cursor description.
    
    Args:
        cursor: Database cursor
        
    Returns:
        list: Column names
    """
    try:
        return [description[0] for description in cursor.description] if cursor.description else []
    except Exception:
        return []


def rows_to_dicts(rows, columns):
    """
    Convert database rows to list of dictionaries.
    
    Args:
        rows: Database rows
        columns: Column names
        
    Returns:
        list: List of dictionaries
    """
    if not rows or not columns:
        return []
    
    try:
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error convirtiendo filas a diccionarios: {e}")
        return []

