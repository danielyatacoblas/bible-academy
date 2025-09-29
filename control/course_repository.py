from .base_repository import BaseRepository
from .classroom_repository import ClassroomRepository
from .inscription_repository import InscriptionRepository
from .payment_repository import PaymentRepository

class CourseRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("course", conn)
        self.classroom_repo = ClassroomRepository(conn)
        self.inscription_repo = InscriptionRepository(conn)
        self.payment_repo = PaymentRepository(conn)

    def create_table(self):
        """
            Create the table 'course' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the course.
                name (VARCHAR(100)): Name of the course.
                level (INTEGER): Level of the course.
            
            Returns:
                None
        """
        columns = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            level INTEGER
        """
        return super().create_table(columns)
    
    def delete_course_cascade(self, course_id: int) -> bool:
        """
        Eliminar curso y todas sus dependencias en cascada.
        
        Args:
            course_id (int): ID del curso a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            # 1. Obtener aulas del curso
            aulas = self.classroom_repo.get_all_rows()
            aulas_curso = [aula for aula in aulas if aula.get("id_course") == course_id]
            
            # 2. Para cada aula, eliminar inscripciones y pagos
            for aula in aulas_curso:
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
            
            # 3. Eliminar todas las aulas del curso
            self.classroom_repo.delete_row({"id_course": course_id})
            
            # 4. Eliminar el curso
            result = self.delete_row({"id": course_id})
            
            return result > 0
            
        except Exception as e:
            print(f"Error al eliminar curso en cascada: {e}")
            return False