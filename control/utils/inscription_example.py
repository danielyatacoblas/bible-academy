"""
Ejemplo de uso del flujo de inscripción y pago.
Demuestra cómo usar las utilidades para crear inscripciones completas.
"""

from inscription_flow import InscriptionFlowManager
from ..bd.db_connection import Connection


def example_complete_inscription():
    """
    Ejemplo de cómo crear una inscripción completa con pago.
    """
    try:
        # Crear el gestor de flujo
        flow_manager = InscriptionFlowManager()
        
        # Datos de ejemplo para la inscripción
        student_id = 1  # ID del estudiante (debe existir en la BD)
        classroom_id = 1  # ID del aula (debe existir en la BD)
        year = 2024
        cycle = "Primer Ciclo"
        type_material = "Libro de Texto"
        payment_method = "Efectivo"
        amount = 150
        
        # Crear inscripción completa
        result = flow_manager.create_complete_inscription(
            student_id=student_id,
            classroom_id=classroom_id,
            year=year,
            cycle=cycle,
            type_material=type_material,
            payment_method=payment_method,
            amount=amount
        )
        
        if result["success"]:
            print("✅ Inscripción creada exitosamente!")
            print(f"   - ID de Inscripción: {result['inscription_id']}")
            print(f"   - ID de Pago: {result['payment_id']}")
            print(f"   - Estudiante: {result['student_name']}")
            print(f"   - Aula: {result['classroom_name']}")
        else:
            print(f"❌ Error: {result['error']}")
            
        return result
        
    except Exception as e:
        print(f"Error en el ejemplo: {e}")
        return None


def example_get_student_inscriptions():
    """
    Ejemplo de cómo obtener todas las inscripciones de un estudiante.
    """
    try:
        flow_manager = InscriptionFlowManager()
        student_id = 1
        
        result = flow_manager.get_student_inscriptions(student_id)
        
        if result["success"]:
            print(f"✅ Inscripciones del estudiante {student_id}:")
            for inscription in result["inscriptions"]:
                print(f"   - Inscripción ID: {inscription['id']}")
                print(f"   - Año: {inscription['year']}")
                print(f"   - Ciclo: {inscription['cycle']}")
                print(f"   - Pagos: {len(inscription['payments'])}")
        else:
            print(f"❌ Error: {result['error']}")
            
        return result
        
    except Exception as e:
        print(f"Error en el ejemplo: {e}")
        return None


def example_add_additional_payment():
    """
    Ejemplo de cómo agregar un pago adicional a una inscripción existente.
    """
    try:
        flow_manager = InscriptionFlowManager()
        inscription_id = 1  # ID de inscripción existente
        payment_method = "Transferencia"
        amount = 50
        
        result = flow_manager.add_payment_to_inscription(
            inscription_id, payment_method, amount
        )
        
        if result["success"]:
            print("✅ Pago adicional agregado!")
            print(f"   - ID de Pago: {result['payment_id']}")
        else:
            print(f"❌ Error: {result['error']}")
            
        return result
        
    except Exception as e:
        print(f"Error en el ejemplo: {e}")
        return None


def example_get_inscription_summary():
    """
    Ejemplo de cómo obtener un resumen completo de una inscripción.
    """
    try:
        flow_manager = InscriptionFlowManager()
        inscription_id = 1
        
        result = flow_manager.get_inscription_summary(inscription_id)
        
        if result["success"]:
            inscription = result["inscription"]
            student = result["student"]
            classroom = result["classroom"]
            payments = result["payments"]
            
            print("✅ Resumen de Inscripción:")
            print(f"   - Estudiante: {student['name']} {student['lastname']}")
            print(f"   - Aula: {classroom.get('name', 'Sin nombre')}")
            print(f"   - Año: {inscription['year']}")
            print(f"   - Ciclo: {inscription['cycle']}")
            print(f"   - Total Pagado: ${result['total_paid']}")
            print(f"   - Número de Pagos: {result['payment_count']}")
            
            for i, payment in enumerate(payments, 1):
                print(f"     Pago {i}: ${payment['amount']} ({payment['method_payment']})")
        else:
            print(f"❌ Error: {result['error']}")
            
        return result
        
    except Exception as e:
        print(f"Error en el ejemplo: {e}")
        return None


if __name__ == "__main__":
    print("=== Ejemplos de Flujo de Inscripción y Pago ===\n")
    
    # Ejecutar ejemplos
    print("1. Crear inscripción completa:")
    example_complete_inscription()
    
    print("\n2. Obtener inscripciones de estudiante:")
    example_get_student_inscriptions()
    
    print("\n3. Agregar pago adicional:")
    example_add_additional_payment()
    
    print("\n4. Obtener resumen de inscripción:")
    example_get_inscription_summary()

