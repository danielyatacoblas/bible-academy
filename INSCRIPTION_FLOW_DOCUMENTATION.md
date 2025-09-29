# Documentación del Flujo de Inscripción y Pago

## Resumen

Este documento explica el flujo completo de inscripción y pago implementado en el sistema de la Academia Bíblica. El flujo garantiza que primero se realice la inscripción y luego el registro de pago, ya que el pago debe tener el ID de la inscripción.

## Estructura del Flujo

### 1. Modelos Actualizados

#### Inscription Model (`model/inscription.py`)

```python
class Inscription(BaseEntity):
    def __init__(self, id_student:int, id_classroom:int, year:int, cycle:str,
                 date_taken:str, type_material:str, status:bool=True,
                 date_inscription:str=None, status_material:bool=True, id:int=None):
```

**Atributos:**

- `id_student`: ID del estudiante (requerido)
- `id_classroom`: ID del aula (requerido)
- `year`: Año de inscripción (requerido)
- `cycle`: Ciclo de inscripción (requerido)
- `date_taken`: Fecha de toma de inscripción (requerido)
- `type_material`: Tipo de material (requerido)
- `status`: Estado de la inscripción (default: True)
- `date_inscription`: Fecha de inscripción (default: None)
- `status_material`: Estado del material (default: True)

#### Payment Model (`model/payment.py`)

```python
class Payment(BaseEntity):
    def __init__(self, method_payment: str, amount:int, created_datetime:str,
                 id_inscription:int, id:int=None):
```

**Atributos:**

- `method_payment`: Método de pago (requerido)
- `amount`: Monto del pago (requerido)
- `created_datetime`: Fecha y hora de creación (requerido)
- `id_inscription`: ID de la inscripción (requerido - FK)

### 2. Repositorios Actualizados

#### InscriptionRepository (`control/inscription_repository.py`)

**Nuevos métodos:**

1. **`create_inscription_with_payment(inscription_data, payment_data)`**

   - Crea inscripción y pago en una transacción
   - Garantiza que el pago tenga el ID de la inscripción
   - Maneja rollback si falla el pago

2. **`get_last_inserted_id()`**

   - Obtiene el ID del último registro insertado
   - Necesario para vincular pago con inscripción

3. **`get_inscription_with_payments(inscription_id)`**
   - Obtiene inscripción con todos sus pagos
   - Útil para consultas completas

#### PaymentRepository (`control/payment_repository.py`)

**Nuevo método:**

1. **`get_last_inserted_id()`**
   - Obtiene el ID del último pago insertado
   - Para confirmar creación exitosa

### 3. Gestor de Flujo (`control/utils/inscription_flow.py`)

#### InscriptionFlowManager

**Métodos principales:**

1. **`create_complete_inscription(student_id, classroom_id, year, cycle, type_material, payment_method, amount)`**

   - Flujo completo de inscripción con pago
   - Valida existencia de estudiante y aula
   - Crea inscripción y pago automáticamente

2. **`get_student_inscriptions(student_id)`**

   - Obtiene todas las inscripciones de un estudiante
   - Incluye todos los pagos asociados

3. **`add_payment_to_inscription(inscription_id, payment_method, amount)`**

   - Agrega pago adicional a inscripción existente
   - Útil para pagos parciales o adicionales

4. **`get_inscription_summary(inscription_id)`**
   - Resumen completo de inscripción
   - Incluye datos del estudiante, aula y todos los pagos
   - Calcula total pagado

## Flujo de Trabajo

### 1. Inscripción Completa (Recomendado)

```python
from control.utils.inscription_flow import InscriptionFlowManager

# Crear gestor
flow_manager = InscriptionFlowManager()

# Crear inscripción con pago
result = flow_manager.create_complete_inscription(
    student_id=1,
    classroom_id=1,
    year=2024,
    cycle="Primer Ciclo",
    type_material="Libro de Texto",
    payment_method="Efectivo",
    amount=150
)

if result["success"]:
    print(f"Inscripción ID: {result['inscription_id']}")
    print(f"Pago ID: {result['payment_id']}")
```

### 2. Inscripción por Pasos (Avanzado)

```python
from control.inscription_repository import InscriptionRepository
from control.payment_repository import PaymentRepository

# 1. Crear inscripción
inscription_repo = InscriptionRepository()
inscription_data = {
    "id_student": 1,
    "id_classroom": 1,
    "year": 2024,
    "cycle": "Primer Ciclo",
    "date_taken": "2024-01-15",
    "type_material": "Libro de Texto",
    "status": True,
    "date_inscription": "2024-01-15",
    "status_material": True
}
inscription_repo.insert_row(inscription_data)

# 2. Obtener ID de inscripción
inscription_id = inscription_repo.get_last_inserted_id()

# 3. Crear pago
payment_repo = PaymentRepository()
payment_data = {
    "method_payment": "Efectivo",
    "amount": 150,
    "id_inscription": inscription_id,
    "created_datetime": "2024-01-15 10:30:00"
}
payment_repo.insert_row(payment_data)
```

## Validaciones y Seguridad

### 1. Validaciones Automáticas

- ✅ Existencia del estudiante
- ✅ Existencia del aula
- ✅ Integridad referencial (FK)
- ✅ Rollback automático en caso de error

### 2. Transacciones

- ✅ Inscripción y pago en una sola transacción
- ✅ Rollback si falla cualquier paso
- ✅ Consistencia de datos garantizada

### 3. Manejo de Errores

- ✅ Mensajes de error descriptivos
- ✅ Logging de errores
- ✅ Recuperación automática

## Casos de Uso

### 1. Inscripción Nueva

```python
# Estudiante se inscribe por primera vez
result = flow_manager.create_complete_inscription(...)
```

### 2. Pago Adicional

```python
# Agregar pago adicional a inscripción existente
result = flow_manager.add_payment_to_inscription(
    inscription_id=1,
    payment_method="Transferencia",
    amount=50
)
```

### 3. Consulta de Historial

```python
# Ver todas las inscripciones de un estudiante
result = flow_manager.get_student_inscriptions(student_id=1)
```

### 4. Resumen Completo

```python
# Obtener resumen detallado de una inscripción
result = flow_manager.get_inscription_summary(inscription_id=1)
```

## Ventajas del Nuevo Flujo

1. **Orden Correcto**: Inscripción → Pago (no al revés)
2. **Integridad**: FK garantizada automáticamente
3. **Transaccional**: Todo o nada
4. **Validaciones**: Automáticas y completas
5. **Flexibilidad**: Permite pagos adicionales
6. **Consultas**: Fáciles y completas
7. **Mantenimiento**: Código organizado y reutilizable

## Archivos Modificados/Creados

### Modificados:

- `model/inscription.py` - Modelo actualizado
- `control/inscription_repository.py` - Nuevos métodos
- `control/payment_repository.py` - Método get_last_inserted_id

### Creados:

- `control/utils/inscription_flow.py` - Gestor de flujo
- `control/utils/inscription_example.py` - Ejemplos de uso
- `INSCRIPTION_FLOW_DOCUMENTATION.md` - Esta documentación

## Próximos Pasos

1. **Testing**: Crear tests unitarios para el flujo
2. **UI Integration**: Integrar con la interfaz de usuario
3. **Reports**: Generar reportes de inscripciones y pagos
4. **Notifications**: Notificaciones automáticas
5. **Backup**: Estrategia de respaldo de datos

