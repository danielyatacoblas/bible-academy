# Documentación de Eliminación en Cascada

## Relaciones de Eliminación en Cascada Implementadas

### 1. **CICLO** (CicleRepository)

```
CICLO → AULAS → INSCRIPCIONES → PAGOS
```

- **Elimina**: Ciclo + Aulas del ciclo + Inscripciones de cada aula + Pagos de cada inscripción
- **Método**: `delete_cicle_cascade(cicle_id)`

### 2. **AULA** (ClassroomRepository)

```
AULA → INSCRIPCIONES → PAGOS
```

- **Elimina**: Aula + Inscripciones del aula + Pagos de cada inscripción
- **Método**: `delete_classroom_cascade(classroom_id)`

### 3. **DOCENTE** (TeacherRepository)

```
DOCENTE → AULAS → INSCRIPCIONES → PAGOS
```

- **Elimina**: Docente + Aulas del docente + Inscripciones de cada aula + Pagos de cada inscripción
- **Método**: `delete_teacher_cascade(teacher_id)`

### 4. **CURSO** (CourseRepository)

```
CURSO → AULAS → INSCRIPCIONES → PAGOS
```

- **Elimina**: Curso + Aulas del curso + Inscripciones de cada aula + Pagos de cada inscripción
- **Método**: `delete_course_cascade(course_id)`

### 5. **INSCRIPCIÓN** (InscriptionRepository)

```
INSCRIPCIÓN → PAGOS
```

- **Elimina**: Inscripción + Pagos de la inscripción
- **Método**: `delete_inscription_cascade(inscription_id)`

### 6. **ESTUDIANTE** (StudentRepository)

```
ESTUDIANTE → (Preparado para futuras relaciones)
```

- **Elimina**: Estudiante (extensible para futuras relaciones)
- **Método**: `delete_student_cascade(student_id)`

## Flujo de Eliminación Completo

### Ejemplo: Eliminar un Ciclo

1. **Ciclo** → Se elimina
2. **Aulas del ciclo** → Se eliminan automáticamente
3. **Inscripciones de cada aula** → Se eliminan automáticamente
4. **Pagos de cada inscripción** → Se eliminan automáticamente

### Ejemplo: Eliminar un Docente

1. **Docente** → Se elimina
2. **Aulas del docente** → Se eliminan automáticamente
3. **Inscripciones de cada aula** → Se eliminan automáticamente
4. **Pagos de cada inscripción** → Se eliminan automáticamente

### Ejemplo: Eliminar un Curso

1. **Curso** → Se elimina
2. **Aulas del curso** → Se eliminan automáticamente
3. **Inscripciones de cada aula** → Se eliminan automáticamente
4. **Pagos de cada inscripción** → Se eliminan automáticamente

## Características de Seguridad

- ✅ **Transacciones**: Cada método maneja errores y rollback
- ✅ **Validación**: Verifica que las eliminaciones sean exitosas
- ✅ **Logging**: Registra errores para debugging
- ✅ **Retorno**: Devuelve `True/False` para indicar éxito/fallo
- ✅ **Integridad**: Mantiene la integridad referencial de la base de datos

## Uso en la Aplicación

Ahora cuando elimines cualquier entidad desde la interfaz, automáticamente se eliminarán todas sus dependencias, garantizando la integridad de los datos y evitando registros huérfanos.

