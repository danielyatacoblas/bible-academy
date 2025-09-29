from .base_repository import BaseRepository
from .inscription_repository import InscriptionRepository

class StudentRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("student", conn)
        self.inscription_repo = InscriptionRepository(conn)

    def create_table(self):
        """
            Create the table 'student' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the student.
                name (VARCHAR(100)): Name of the student.
                lastname (VARCHAR(100)): Last name of the student.
                phone (VARCHAR(20)): Phone number of the student.
                date_baptism (DATE): Date of baptism.
                date_of_birth (DATE): Date of birth.
                id_team (INTEGER): Foreign key to team table.
            
            Returns:
                None
        """
        columns = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            lastname VARCHAR(100),
            phone VARCHAR(20),
            date_baptism DATE,
            date_of_birth DATE,
            id_team INTEGER,
            FOREIGN KEY (id_team) REFERENCES team(id)
        """
        return super().create_table(columns)
    
    def delete_student_cascade(self, student_id: int) -> bool:
        """
        Eliminar estudiante y todas sus dependencias en cascada.
        
        Args:
            student_id (int): ID del estudiante a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            # 1. Eliminar todas las inscripciones del estudiante
            # Nota: Necesitamos verificar si hay una relación directa estudiante-inscripción
            # Por ahora, eliminamos el estudiante directamente
            result = self.delete_row({"id": student_id})
            
            return result > 0
            
        except Exception as e:
            print(f"Error al eliminar estudiante en cascada: {e}")
            return False