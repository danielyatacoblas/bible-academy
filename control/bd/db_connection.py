import sqlite3
import os

class Connection:

    DB_NAME = os.path.join(os.path.dirname(__file__), "academy.db")

    @staticmethod
    def connect():
        """
            Open to connection to academy db
        """
        try:
            return sqlite3.connect(Connection.DB_NAME)
        except Exception as e:
            print(f"Error to connect db: {e}")
            return None
    
    @staticmethod
    def cursor():
        """
            Return tuple to connection to db and close db
        """
        try:
            conn = Connection.connect()
            if conn :
                return conn, conn.cursor()
            return None, None
        except Exception as e:
            print(f"Error to cursor: {e}")
            return None, None
