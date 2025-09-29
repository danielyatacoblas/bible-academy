"""
Utilidades para el flujo de inscripción y pago.
Maneja el proceso completo de inscripción de estudiantes con sus pagos correspondientes.
"""

from datetime import datetime
from ..inscription_repository import InscriptionRepository
from ..payment_repository import PaymentRepository
from ..student_repository import StudentRepository
from ..classroom_repository import ClassroomRepository


class InscriptionFlowManager:
    """
    Gestor del flujo completo de inscripción y pago.
    """
    
    def __init__(self, conn=None):
        self.inscription_repo = InscriptionRepository(conn)
        self.payment_repo = PaymentRepository(conn)
        self.student_repo = StudentRepository(conn)
        self.classroom_repo = ClassroomRepository(conn)
    
    def create_complete_inscription(self, student_id: int, classroom_id: int, 
                                  year: int, cycle: str, type_material: str,
                                  payment_method: str, amount: int) -> dict:
        """
        Crear inscripción completa con pago.
        
        Args:
            student_id (int): ID del estudiante
            classroom_id (int): ID del aula
            year (int): Año de inscripción
            cycle (str): Ciclo de inscripción
            type_material (str): Tipo de material
            payment_method (str): Método de pago
            amount (int): Monto del pago
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # 1. Validar que el estudiante existe
            student = self.student_repo.get_row_value({"id": student_id})
            if not student:
                return {"success": False, "error": "Estudiante no encontrado"}
            
            # 2. Validar que el aula existe
            classroom = self.classroom_repo.get_row_value({"id": classroom_id})
            if not classroom:
                return {"success": False, "error": "Aula no encontrada"}
            
            # 3. Preparar datos de inscripción
            current_date = datetime.now().strftime("%Y-%m-%d")
            inscription_data = {
                "id_student": student_id,
                "id_classroom": classroom_id,
                "year": year,
                "cycle": cycle,
                "date_taken": current_date,
                "type_material": type_material,
                "status": True,
                "date_inscription": current_date,
                "status_material": True
            }
            
            # 4. Preparar datos de pago
            payment_data = {
                "method_payment": payment_method,
                "amount": amount,
                "created_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 5. Crear inscripción con pago
            result = self.inscription_repo.create_inscription_with_payment(
                inscription_data, payment_data
            )
            
            if result["success"]:
                result["student_name"] = f"{student['name']} {student['lastname']}"
                result["classroom_name"] = classroom.get('name', 'Aula sin nombre')
            
            return result
            
        except Exception as e:
            return {"success": False, "error": f"Error en el flujo de inscripción: {str(e)}"}
    
    def get_student_inscriptions(self, student_id: int) -> dict:
        """
        Obtener todas las inscripciones de un estudiante con sus pagos.
        
        Args:
            student_id (int): ID del estudiante
            
        Returns:
            dict: Inscripciones del estudiante
        """
        try:
            # Obtener inscripciones del estudiante
            inscriptions = self.inscription_repo.get_all_rows({"id_student": student_id})
            
            result = []
            for inscription in inscriptions:
                # Obtener pagos de cada inscripción
                payments = self.payment_repo.get_all_rows({"id_inscription": inscription["id"]})
                inscription["payments"] = payments
                result.append(inscription)
            
            return {"success": True, "inscriptions": result}
            
        except Exception as e:
            return {"success": False, "error": f"Error al obtener inscripciones: {str(e)}"}
    
    def add_payment_to_inscription(self, inscription_id: int, 
                                 payment_method: str, amount: int) -> dict:
        """
        Agregar un pago adicional a una inscripción existente.
        
        Args:
            inscription_id (int): ID de la inscripción
            payment_method (str): Método de pago
            amount (int): Monto del pago
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # Validar que la inscripción existe
            inscription = self.inscription_repo.get_row_value({"id": inscription_id})
            if not inscription:
                return {"success": False, "error": "Inscripción no encontrada"}
            
            # Preparar datos del pago
            payment_data = {
                "method_payment": payment_method,
                "amount": amount,
                "id_inscription": inscription_id,
                "created_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Crear el pago
            self.payment_repo.insert_row(payment_data)
            payment_id = self.payment_repo.get_last_inserted_id()
            
            if payment_id:
                return {
                    "success": True,
                    "payment_id": payment_id,
                    "message": "Pago agregado exitosamente"
                }
            else:
                return {"success": False, "error": "Error al crear pago"}
                
        except Exception as e:
            return {"success": False, "error": f"Error al agregar pago: {str(e)}"}
    
    def get_inscription_summary(self, inscription_id: int) -> dict:
        """
        Obtener resumen completo de una inscripción con todos sus pagos.
        
        Args:
            inscription_id (int): ID de la inscripción
            
        Returns:
            dict: Resumen de la inscripción
        """
        try:
            # Obtener inscripción con pagos
            inscription_data = self.inscription_repo.get_inscription_with_payments(inscription_id)
            if not inscription_data:
                return {"success": False, "error": "Inscripción no encontrada"}
            
            inscription = inscription_data["inscription"]
            payments = inscription_data["payments"]
            
            # Calcular total pagado
            total_paid = sum(payment["amount"] for payment in payments)
            
            # Obtener información del estudiante
            student = self.student_repo.get_row_value({"id": inscription["id_student"]})
            
            # Obtener información del aula
            classroom = self.classroom_repo.get_row_value({"id": inscription["id_classroom"]})
            
            return {
                "success": True,
                "inscription": inscription,
                "student": student,
                "classroom": classroom,
                "payments": payments,
                "total_paid": total_paid,
                "payment_count": len(payments)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error al obtener resumen: {str(e)}"}
