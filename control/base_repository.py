from .bd.db_connection import Connection
class BaseRepository:
    def __init__(self, table: str, conn=None):
        self.conn = conn
        self.cursor = conn.cursor() if conn else None
        self.table = table

    def create_table(self, columns: str):
        """
            Create table in the database if not exists.

            Args:
                columns (str): Columns definition in SQL format.
            Returns:
                None
        """
        try:
            if self.conn:
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table} ({columns})")
                self.conn.commit()
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table} ({columns})")
                    conn.commit()
            print(f"Table {self.table} created")
        except Exception as e:
            print(f"Error to create table {self.table}: {e}")

    def insert_rows(self, data: list[dict]):
        """
            Insert multiple rows into the table.

            Args:
                data (list[dict]): List of dictionaries with column-value pairs.
            Returns:
                None
        """
        try:
            columns = ", ".join(data[0].keys())
            placeholders = ", ".join(["?" for _ in data[0]])
            values_data = [tuple(d.values()) for d in data]
            if self.conn:
                self.cursor.executemany(f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", values_data)
                self.conn.commit()
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.executemany(f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", values_data)
                    conn.commit()
            print(f"Insert values into {self.table} success")
        except Exception as e:
            print(f"Error insert values {self.table}: {e}")

    def insert_row(self, data: dict):
        """
            Insert a single row into the table.

            Args:
                data (dict): Dictionary with column-value pairs.
            Returns:
                None
        """
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data.keys()])
            values = tuple(data.values())
            if self.conn:
                self.cursor.execute(f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", values)
                self.conn.commit()
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", values)
                    conn.commit()
            print(f"Insert row into {self.table} success")
        except Exception as e:
            print(f"Error to insert into table {self.table}: {e}")

    def update_row(self, new_data: dict, conditions: dict):
        """
            Update rows by conditions.

            Args:
                new_data (dict): Dictionary with column-value pairs to update.
                conditions (dict): Dictionary with column-value pairs for WHERE clause.
            Returns:
                int: Number of rows affected.
        """
        try:
            set_clause = ", ".join([f"{col} = ?" for col in new_data.keys()])
            where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
            values = tuple(new_data.values()) + tuple(conditions.values())
            
            if self.conn:
                self.cursor.execute(f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}", values)
                self.conn.commit()
                return self.cursor.rowcount
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}", values)
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            print(f"Error to update {self.table}: {e}")
            return 0

    def delete_row(self, conditions: dict):
        """
            Delete rows by conditions.

            Args:
                conditions (dict): Dictionary with column-value pairs for WHERE clause.
            Returns:
                int: Number of rows affected.
        """
        try:
            where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
            values = tuple(conditions.values())
            
            if self.conn:
                self.cursor.execute(f"DELETE FROM {self.table} WHERE {where_clause}", values)
                self.conn.commit()
                return self.cursor.rowcount
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM {self.table} WHERE {where_clause}", values)
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            print(f"Error to delete row {self.table}: {e}")
            return 0

    def get_row_value(self, values):
        """
            Get a row by id or other criteria.

            Args:
                values (dict): Dictionary with column-value pairs.
            Returns:
                dict or None: Row data if found, else None.
        """
        try:
            if not values:
                return None
                
            where_clause = " AND ".join([f"{key} = ?" for key in values.keys()])
            params = tuple(values.values())
            
            if self.conn and self.cursor:
                self.cursor.execute(f"SELECT * FROM {self.table} WHERE {where_clause}", params)
                row = self.cursor.fetchone()
                columns = [description[0] for description in self.cursor.description]
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {self.table} WHERE {where_clause}", params)
                    row = cursor.fetchone()
                    columns = [description[0] for description in cursor.description]
            
            if row:
                # Convertir a diccionario
                if not columns:
                    # Si no hay cursor.description, usar nombres genéricos
                    columns = [f"col_{i}" for i in range(len(row))]
                return dict(zip(columns, row)) if columns else None
            return None
        except Exception as e:
            print(f"Error to get row {self.table}: {e}")
            return None
    def delete_all_rows(self):
        """
            Delete all rows from the table.

            Returns:
                None
        """
        try:
            if self.conn:
                self.cursor.execute(f"DELETE FROM {self.table}")
                self.conn.commit()
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM {self.table}")
                    conn.commit()
            print(f"All rows deleted from {self.table}")
        except Exception as e:
            print(f"Error to delete all rows {self.table}: {e}")

    def get_row(self, id: int):
        """
            Get a row by id.

            Args:
                id (int): Row identifier.
            Returns:
                tuple or None: Row data if found, else None.
        """
        try:
            if self.conn:
                self.cursor.execute(f"SELECT * FROM {self.table} WHERE id = ?", (id,))
                return self.cursor.fetchone()
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {self.table} WHERE id = ?", (id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error to get row {self.table}: {e}")
            return None

    def get_all_rows(self, searchs: dict = None):
        """
            Get all rows with optional search filters (case-insensitive LIKE).

            Args:
                searchs (dict, optional): Dictionary with column-value filters.
            Returns:
                list[dict] or None: Matching rows as dictionaries, else None.
        """
        try:
            if searchs:
                where = " OR ".join([f"{col} LIKE ? COLLATE NOCASE" for col in searchs.keys()])
                values = [f"%{val}%" for val in searchs.values()]
                sql = f"SELECT * FROM {self.table} WHERE {where}"
            else:
                sql = f"SELECT * FROM {self.table}"
                values = []

            if self.conn and self.cursor:
                self.cursor.execute(sql, values)
                rows = self.cursor.fetchall()
                columns = [description[0] for description in self.cursor.description]
            else:
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(sql, values)
                    rows = cursor.fetchall()
                    columns = [description[0] for description in cursor.description]
            
            if rows:
                # Convertir a lista de diccionarios
                if not columns:
                    # Si no hay cursor.description, usar nombres genéricos
                    columns = [f"col_{i}" for i in range(len(rows[0]))]
                return [dict(zip(columns, row)) for row in rows] if columns else []
            return []
        except Exception as e:
            print(f"Error to get all {self.table}: {e}")
            return []
