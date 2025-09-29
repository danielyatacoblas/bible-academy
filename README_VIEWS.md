# Bible Academy - Sistema de Vistas

## 📋 Descripción

Sistema completo de vistas para Bible Academy desarrollado con Flet, basado en las imágenes de diseño proporcionadas. Incluye login, dashboard principal y páginas de gestión para cada sección.

## 🏗️ Estructura del Proyecto

```
view/
├── main.py                 # Aplicación principal con navegación
├── login_view.py          # Vista de login (basada en imagen 1)
├── dashboard_view.py      # Dashboard principal (basado en imagen 2)
└── pages/
    ├── base_page.py       # Página base con funcionalidades comunes
    ├── students_page.py   # Gestión de estudiantes
    ├── teachers_page.py   # Gestión de docentes
    ├── courses_page.py    # Gestión de cursos
    └── academy_page.py    # Gestión de academia
```

## 🚀 Cómo Ejecutar

### 1. Ejecutar la aplicación:

```bash
cd bible-academy
python app.py
```

### 2. Credenciales de prueba:

- **Usuario:** admin
- **Contraseña:** admin

## 🎨 Características del Diseño

### Login (Vista 1)

- **Fondo azul oscuro** como en la imagen
- **Tarjeta blanca centrada** con bordes redondeados
- **Logo circular** con iconos de globo y cáliz
- **Campos de entrada** para usuario y contraseña
- **Botón de login** con estilo azul
- **Enlace "Olvidé mi contraseña"**

### Dashboard (Vista 2)

- **Sidebar izquierdo** con navegación
- **Logo y nombre de usuario** en el header
- **Menú de navegación** con iconos
- **Contenido principal** con tarjetas y gráficos
- **Tarjetas de resumen** con estadísticas
- **Sección de gráficos** (placeholders para desarrollo futuro)

## 📱 Funcionalidades Implementadas

### ✅ Login

- Validación de credenciales
- Mensajes de error/éxito
- Navegación automática al dashboard

### ✅ Dashboard Principal

- Navegación funcional entre secciones
- Tarjetas de estadísticas
- Gráficos placeholder
- Botón de logout

### ✅ Páginas de Gestión

#### Estudiantes

- Tabla con datos de ejemplo
- Botones de agregar, editar, eliminar
- Campos: ID, Nombre, Apellido, Teléfono

#### Docentes

- Tabla con datos de ejemplo
- Botones de agregar, editar, eliminar
- Campos: ID, Nombre, Apellido, Especialidad

#### Cursos

- Vista de tarjetas (grid)
- Información de nivel y estudiantes
- Botones de gestión

#### Academia

- Información general de la academia
- Estadísticas en tarjetas
- Botones de configuración

## 🔧 Arquitectura Técnica

### Patrón de Navegación

```python
# Navegación principal
BibleAcademyApp -> LoginView -> DashboardView -> Pages
```

### Componentes Base

- **BasePage**: Página base con header y funcionalidades comunes
- **LoginView**: Vista de autenticación
- **DashboardView**: Dashboard principal con sidebar

### Estructura de Páginas

```python
class PageName(BasePage):
    def _build_content(self):
        # Implementar contenido específico
        pass
```

## 🎯 Próximas Mejoras

### Integración con Base de Datos

- Conectar con repositorios existentes
- CRUD real para todas las entidades
- Validaciones de datos

### Funcionalidades Avanzadas

- Gráficos reales con datos
- Búsqueda y filtros
- Exportación de datos
- Reportes PDF

### Mejoras de UI/UX

- Integrar logo `iacym.jpg`
- Animaciones más suaves
- Temas personalizables
- Responsive design

## 📝 Comentarios del Código

El código sigue el estilo de comentarios formal del proyecto:

```python
def method_name(self, parameter: type) -> return_type:
    """
    Descripción breve del método

    Args:
        parameter: Descripción del parámetro

    Returns:
        Descripción del valor de retorno
    """
    # Implementación del método
```

## 🐛 Solución de Problemas

### Error de Importación

```python
# Si hay problemas con importaciones relativas
from login_view import LoginView
from dashboard_view import DashboardView
```

### Error de Navegación

- Verificar que las páginas estén correctamente importadas
- Revisar los IDs de navegación en `_show_page_content()`

### Error de Estilos

- Verificar que los colores estén definidos correctamente
- Revisar la configuración del tema en `main()`

## 📚 Documentación de Flet

Para más información sobre Flet:

- [Documentación oficial](https://flet.dev/docs/)
- [Ejemplos de código](https://flet.dev/docs/controls/)
- [Guías de diseño](https://flet.dev/docs/guides/python/)

## 🤝 Contribución

Para agregar nuevas páginas:

1. Crear archivo en `pages/`
2. Heredar de `BasePage`
3. Implementar `_build_content()`
4. Agregar navegación en `dashboard_view.py`

## 📞 Soporte

Para reportar problemas o solicitar funcionalidades, contacta al equipo de desarrollo.
