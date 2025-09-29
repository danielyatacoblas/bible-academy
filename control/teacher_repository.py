from .base_repository import BaseRepository
from .classroom_repository import ClassroomRepository
from .inscription_repository import InscriptionRepository
from .payment_repository import PaymentRepository

class TeacherRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("teacher", conn)
        self.classroom_repo = ClassroomRepository(conn)
        self.inscription_repo = InscriptionRepository(conn)
        self.payment_repo = PaymentRepository(conn)

    def create_table(self):
        """
            Create the table 'teacher' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the teacher.
                name (VARCHAR(100)): Name of the teacher.
                lastname (VARCHAR(100)): Last name of the teacher.
                phone (VARCHAR(20)): Phone number of the teacher.
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
    
    def delete_teacher_cascade(self, teacher_id: int) -> bool:
        """
        Eliminar docente y todas sus dependencias en cascada.
        
        Args:
            teacher_id (int): ID del docente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            # 1. Obtener aulas del docente
            aulas = self.classroom_repo.get_all_rows()
            aulas_docente = [aula for aula in aulas if aula.get("id_teacher") == teacher_id]
            
            # 2. Para cada aula, eliminar inscripciones y pagos
            for aula in aulas_docente:
                aula_id = aula.get("id")
                if aula_id:
                    # Obtener inscripciones de la aula
                    inscripciones = self.inscription_repo.get_all_rows()
                    inscripciones_aula = [insc for insc in inscripciones if insc.get("id_classroom") == aula_id]
                    
                    # Eliminar pagos de cada inscripción
                    for inscripcion in inscripciones_aula:
                        inscripcion_id = inscripcion.get("id")
                        if inscripcion_id:
                            self.payment_repo.delete_row({"id_inscription": inscripcion_id})
                    
                    # Eliminar inscripciones de la aula
                    self.inscription_repo.delete_row({"id_classroom": aula_id})
            
            # 3. Eliminar todas las aulas del docente
            self.classroom_repo.delete_row({"id_teacher": teacher_id})
            
            # 4. Eliminar el docente
            result = self.delete_row({"id": teacher_id})
            
            return result > 0
            
        except Exception as e:
            print(f"Error al eliminar docente en cascada: {e}")
            return False