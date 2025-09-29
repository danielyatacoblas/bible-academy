from .base_repository import BaseRepository
from .inscription_repository import InscriptionRepository
from .payment_repository import PaymentRepository

class ClassroomRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("classroom", conn)
        self.inscription_repo = InscriptionRepository(conn)
        self.payment_repo = PaymentRepository(conn)

    def create_table(self):
        """
            Create the table 'classroom' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the classroom.
                name (VARCHAR(100)): Name of the classroom.
                start_date (DATE): Start date of the classroom.
                end_date (DATE): End date of the classroom.
                id_teacher (INTEGER): Foreign key to teacher table.
                id_course (INTEGER): Foreign key to course table.
                id_cicle (INTEGER): Foreign key to cicle table.
            
            Returns:
                None
        """
        columns = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            start_date DATE,
            end_date DATE,
            id_teacher INTEGER,
            id_course INTEGER,
            id_cicle INTEGER,
            FOREIGN KEY (id_teacher) REFERENCES teacher(id),
            FOREIGN KEY (id_course) REFERENCES course(id),
            FOREIGN KEY (id_cicle) REFERENCES cicle(id)
        """
        return super().create_table(columns)
    
    def delete_classroom_cascade(self, classroom_id: int) -> bool:
        """
        Eliminar aula y todas sus dependencias en cascada.
        
        Args:
            classroom_id (int): ID del aula a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            # 1. Obtener inscripciones del aula
            inscripciones = self.inscription_repo.get_all_rows()
            inscripciones_aula = [insc for insc in inscripciones if insc.get("id_classroom") == classroom_id]
            
            # 2. Eliminar pagos de cada inscripción
            for inscripcion in inscripciones_aula:
                inscripcion_id = inscripcion.get("id")
                if inscripcion_id:
                    self.payment_repo.delete_row({"id_inscription": inscripcion_id})
            
            # 3. Eliminar todas las inscripciones del aula
            self.inscription_repo.delete_row({"id_classroom": classroom_id})
            
            # 4. Eliminar el aula
            result = self.delete_row({"id": classroom_id})
            
            return result > 0
            
        except Exception as e:
            print(f"Error al eliminar aula en cascada: {e}")
            return False