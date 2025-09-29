from .base_repository import BaseRepository
from .classroom_repository import ClassroomRepository
from .inscription_repository import InscriptionRepository
from .payment_repository import PaymentRepository

class CicleRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("cicle", conn)
        self.classroom_repo = ClassroomRepository(conn)
        self.inscription_repo = InscriptionRepository(conn)
        self.payment_repo = PaymentRepository(conn)

    def create_table(self):
        """
            Create the table 'cicle' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the cycle.
                cicle (CHAR(2)): Cycle identifier.
                date_start (DATE): Start date of the cycle.
                date_end (DATE): End date of the cycle.
                manager (VARCHAR(100)): Manager of the inscription.
            
            Returns:
                None
        """
        columns = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cicle CHAR(2),
            date_start DATE,
            date_end DATE,
            manager VARCHAR(100)
        """
        return super().create_table(columns)
    
    def delete_cicle_cascade(self, cicle_id: int) -> bool:
        """
        Eliminar ciclo y todas sus dependencias en cascada.
        
        Args:
            cicle_id (int): ID del ciclo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            # 1. Obtener todas las aulas del ciclo
            aulas = self.classroom_repo.get_all_rows()
            aulas_ciclo = [aula for aula in aulas if aula.get("id_cicle") == cicle_id]
            
            # 2. Para cada aula, eliminar sus inscripciones y pagos
            for aula in aulas_ciclo:
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
            
            # 3. Eliminar todas las aulas del ciclo
            self.classroom_repo.delete_row({"id_cicle": cicle_id})
            
            # 4. Finalmente, eliminar el ciclo
            result = self.delete_row({"id": cicle_id})
            
            return result > 0
            
        except Exception as e:
            print(f"Error al eliminar ciclo en cascada: {e}")
            return False
