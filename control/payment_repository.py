from .base_repository import BaseRepository

class PaymentRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("payment", conn)

    def create_table(self):
        """
            Create the table 'payment' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the payment.
                method_payment (VARCHAR(50)): Method of payment.
                amount (INTEGER): Amount of payment.
                created_datetime (DATETIME): Creation date and time of the payment.
                id_inscription (INTEGER): Foreign key to inscription table.
            
            Returns:
                None
        """
        columns = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_payment VARCHAR(50),
            amount INTEGER,
            created_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
            id_inscription INTEGER,
            FOREIGN KEY (id_inscription) REFERENCES inscription(id)
        """
        return super().create_table(columns)
    
    def get_last_inserted_id(self) -> int:
        """
        Obtener el ID del último registro insertado.
        
        Returns:
            int: ID del último registro insertado
        """
        try:
            if self.conn and self.cursor:
                # Obtener el último ID insertado en la tabla
                self.cursor.execute(f"SELECT MAX(id) FROM {self.table}")
                result = self.cursor.fetchone()
                return result[0] if result and result[0] else None
            else:
                from .bd.db_connection import Connection
                with Connection.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT MAX(id) FROM {self.table}")
                    result = cursor.fetchone()
                    return result[0] if result and result[0] else None
        except Exception as e:
            print(f"Error al obtener último ID insertado: {e}")
            return None