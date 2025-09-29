from .base_repository import BaseRepository
from .payment_repository import PaymentRepository

class InscriptionRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("inscription", conn)
        self.payment_repo = PaymentRepository(conn)

    def create_table(self):
        """
            Create the table 'inscription' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the inscription.
                status (BOOLEAN): Status of the inscription.
                date_inscription (DATE): Date of the inscription.
                type_material (VARCHAR(50)): Type of material.
                status_material (BOOLEAN): Status of the material.
                id_classroom (INTEGER): Foreign key to classroom table.
            
            Returns:
                None
        """
        columns = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_student INTEGER,
            id_classroom INTEGER,
            year INTEGER,
            cycle VARCHAR(10),
            date_taken DATE,
            type_material VARCHAR(50),
            status BOOLEAN DEFAULT 1,
            date_inscription DATE DEFAULT CURRENT_DATE,
            status_material BOOLEAN DEFAULT 1,
            FOREIGN KEY (id_student) REFERENCES student(id),
            FOREIGN KEY (id_classroom) REFERENCES classroom(id)
        """
        return super().create_table(columns)
    
    def create_inscription_with_payment(self, inscription_data: dict, payment_data: dict) -> dict:
        """
        Crear inscripción y su pago correspondiente en una transacción.
        
        Args:
            inscription_data (dict): Datos de la inscripción
            payment_data (dict): Datos del pago
            
        Returns:
            dict: Resultado con success, inscription_id y payment_id
        """
        try:
            # 1. Crear la inscripción primero
            self.insert_row(inscription_data)
            
            # 2. Obtener el ID de la inscripción recién creada
            inscription_id = self.get_last_inserted_id()
            if not inscription_id:
                return {"success": False, "error": "No se pudo obtener ID de inscripción"}
            
            # 3. Agregar el ID de inscripción al pago
            payment_data["id_inscription"] = inscription_id
            
            # 4. Crear el pago
            self.payment_repo.insert_row(payment_data)
            
            payment_id = self.payment_repo.get_last_inserted_id()
            
            return {
                "success": True, 
                "inscription_id": inscription_id,
                "payment_id": payment_id,
                "message": "Inscripción y pago creados exitosamente"
            }
            
        except Exception as e:
            print(f"Error al crear inscripción con pago: {e}")
            return {"success": False, "error": f"Error en transacción: {str(e)}"}
    
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
    
    def get_inscription_with_payments(self, inscription_id: int) -> dict:
        """
        Obtener inscripción con todos sus pagos.
        
        Args:
            inscription_id (int): ID de la inscripción
            
        Returns:
            dict: Inscripción con sus pagos
        """
        try:
            # Obtener la inscripción
            inscription = self.get_row_value({"id": inscription_id})
            if not inscription:
                return None
            
            # Obtener los pagos de la inscripción
            payments = self.payment_repo.get_all_rows({"id_inscription": inscription_id})
            
            return {
                "inscription": inscription,
                "payments": payments
            }
            
        except Exception as e:
            print(f"Error al obtener inscripción con pagos: {e}")
            return None

    def delete_inscription_cascade(self, inscription_id: int) -> bool:
        """
        Eliminar inscripción y todas sus dependencias en cascada.
        
        Args:
            inscription_id (int): ID de la inscripción a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            # 1. Eliminar todos los pagos de la inscripción
            self.payment_repo.delete_row({"id_inscription": inscription_id})
            
            # 2. Eliminar la inscripción
            result = self.delete_row({"id": inscription_id})
            
            return result > 0
            
        except Exception as e:
            print(f"Error al eliminar inscripción en cascada: {e}")
            return False