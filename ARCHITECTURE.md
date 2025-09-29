# Bible Academy - Arquitectura SOLID

## 📋 Descripción

Sistema de gestión académica bíblica desarrollado con Flet, implementando principios SOLID y arquitectura limpia.

## 🏗️ Arquitectura del Proyecto

```
bible-academy/
├── app.py                          # Punto de entrada (solo importa desde view)
├── view/                           # Capa de presentación
│   ├── main.py                     # Aplicación principal y configuración
│   ├── login_view.py              # Vista de login
│   ├── dashboard_view.py          # Dashboard con NavigationRail
│   ├── pages/                     # Páginas específicas
│   │   ├── base_page.py           # Página base (abstracción)
│   │   ├── students_page.py       # Gestión de estudiantes
│   │   ├── teachers_page.py       # Gestión de docentes
│   │   ├── courses_page.py        # Gestión de cursos
│   │   ├── academy_page.py        # Gestión de academia
│   │   └── page_factory.py        # Factory para crear páginas
│   ├── components/                 # Componentes reutilizables
│   └── images/                     # Recursos (logo, etc.)
├── model/                          # Capa de modelo (entidades)
├── control/                        # Capa de control (lógica de negocio)
└── tests/                          # Pruebas unitarias
```

## 🎯 Principios SOLID Implementados

### 1. **Single Responsibility Principle (SRP)**

- **`StudentsPage`**: Solo maneja la gestión de estudiantes
- **`TeachersPage`**: Solo maneja la gestión de docentes
- **`CoursesPage`**: Solo maneja la gestión de cursos
- **`AcademyPage`**: Solo maneja la gestión de academia
- **`PageFactory`**: Solo crea páginas

### 2. **Open/Closed Principle (OCP)**

- **`BasePage`**: Abierto para extensión, cerrado para modificación
- **`PageFactory`**: Fácil agregar nuevos tipos de página sin modificar código existente

### 3. **Liskov Substitution Principle (LSP)**

- Todas las páginas pueden ser sustituidas por `BasePage`
- `PageFactory` puede crear cualquier tipo de página

### 4. **Interface Segregation Principle (ISP)**

- **`BasePage`**: Interfaz específica para páginas
- **`PageFactory`**: Interfaz específica para creación de páginas

### 5. **Dependency Inversion Principle (DIP)**

- **`DashboardView`**: Depende de abstracciones (`PageFactory`)
- **`PageFactory`**: Depende de abstracciones (`BasePage`)

## 🔧 Componentes Principales

### **BasePage (Abstracción)**

```python
class BasePage(ft.Control):
    def __init__(self, title: str, on_back: Optional[Callable] = None)
    def _build_content(self)  # Método abstracto
    def show_message(self, message: str, message_type: str = "info")
```

### **PageFactory (Factory Pattern)**

```python
class PageFactory:
    @classmethod
    def create_page(cls, page_type: str, on_back: Optional[Callable] = None) -> BasePage
    @classmethod
    def get_available_pages(cls) -> Dict[str, str]
    @classmethod
    def register_page(cls, page_type: str, page_class: type)
```

### **Páginas Específicas**

- **`StudentsPage`**: Tabla con datos de estudiantes, búsqueda, CRUD
- **`TeachersPage`**: Grid con tarjetas de docentes, filtros
- **`CoursesPage`**: Grid con cursos, filtros por nivel, colores por nivel
- **`AcademyPage`**: Información general, estadísticas, gestión

## 🚀 Flujo de la Aplicación

```
app.py → view/main.py → BibleAcademyApp → LoginView → DashboardView → Pages
```

### **1. Inicio**

```python
# app.py
from view.main import main
ft.app(target=main)
```

### **2. Configuración**

```python
# view/main.py
def main(page: ft.Page):
    # Configuración de ventana y tema
    app = BibleAcademyApp()
    page.add(app)
```

### **3. Navegación**

```python
# BibleAcademyApp
LoginView → DashboardView → PageFactory.create_page() → SpecificPage
```

## 🎨 Características de Diseño

### **Login**

- Logo real `iacym.jpg`
- Diseño basado en imagen proporcionada
- Validación de credenciales
- Navegación automática al dashboard

### **Dashboard**

- **NavigationRail** moderno y responsive
- Logo integrado en el header
- Navegación funcional entre páginas
- Tarjetas de estadísticas
- Gráficos placeholder

### **Páginas**

- **Búsqueda**: SearchBar en todas las páginas
- **Filtros**: Dropdowns para filtrar datos
- **CRUD**: Botones de agregar, editar, eliminar
- **Responsive**: GridView y Column adaptativos

## 📱 Funcionalidades por Página

### **Estudiantes**

- Tabla con: ID, Nombre, Apellido, Teléfono, Equipo
- Búsqueda por nombre, apellido, teléfono
- Botones CRUD funcionales

### **Docentes**

- Grid de tarjetas con: Nombre, Especialidad, Experiencia
- Búsqueda por nombre, apellido, especialidad
- Botones CRUD funcionales

### **Cursos**

- Grid de tarjetas con: Nombre, Nivel, Estudiantes, Duración
- Filtros por nivel (Básico, Intermedio, Avanzado)
- Colores por nivel
- Búsqueda por nombre

### **Academia**

- Información general de la academia
- Estadísticas en tarjetas
- Botones de gestión y configuración

## 🔄 Extensibilidad

### **Agregar Nueva Página**

1. Crear clase en `view/pages/`
2. Heredar de `BasePage`
3. Implementar `_build_content()`
4. Registrar en `PageFactory`

```python
# Ejemplo: Nueva página de reportes
class ReportsPage(BasePage):
    def _build_content(self):
        # Implementar contenido
        pass

# Registrar en factory
PageFactory.register_page("reports", ReportsPage)
```

### **Agregar Nueva Funcionalidad**

1. Extender `BasePage` si es común
2. Implementar en páginas específicas si es particular
3. Usar `PageFactory` para crear instancias

## 🧪 Testing

### **Estructura de Pruebas**

```
tests/
├── test_students_page.py
├── test_teachers_page.py
├── test_courses_page.py
├── test_academy_page.py
└── test_page_factory.py
```

### **Pruebas Unitarias**

- Cada página tiene sus propias pruebas
- Factory tiene pruebas de creación
- BasePage tiene pruebas de funcionalidades comunes

## 📚 Documentación

### **Comentarios**

- Formales y descriptivos
- Documentación de métodos públicos
- Ejemplos de uso cuando es necesario

### **Type Hints**

- Tipos explícitos en todos los métodos
- Optional para parámetros opcionales
- Callable para callbacks

## 🚀 Ejecución

```bash
cd bible-academy
python app.py
```

## 🎯 Beneficios de la Arquitectura

### **Mantenibilidad**

- Código organizado y modular
- Fácil localizar funcionalidades
- Cambios aislados por componente

### **Escalabilidad**

- Fácil agregar nuevas páginas
- Factory pattern para extensión
- Separación clara de responsabilidades

### **Testabilidad**

- Componentes independientes
- Fácil crear mocks y stubs
- Pruebas unitarias aisladas

### **Reutilización**

- `BasePage` reutilizable
- `PageFactory` genérico
- Componentes modulares

## 🔧 Próximas Mejoras

### **Integración con Base de Datos**

- Conectar páginas con repositorios
- CRUD real con validaciones
- Persistencia de datos

### **Funcionalidades Avanzadas**

- Gráficos reales con datos
- Exportación de reportes
- Notificaciones push
- Autenticación real

### **Mejoras de UI/UX**

- Temas personalizables
- Animaciones más suaves
- Responsive design mejorado
- Accesibilidad

