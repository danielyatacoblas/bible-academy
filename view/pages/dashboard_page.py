import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from control.session.user_repository import UserRepository
from control.bd.db_connection import Connection
from control.cicle_repository import CicleRepository
from control.classroom_repository import ClassroomRepository
from control.course_repository import CourseRepository
from control.teacher_repository import TeacherRepository
from control.student_repository import StudentRepository
from control.team_repository import TeamRepository
from control.inscription_repository import InscriptionRepository
from control.payment_repository import PaymentRepository
from tkinter import ttk
from view.components.chart import ChartGenerator, create_matplotlib_widget

class DashboardPage:
    def __init__(self, parent, current_user=None):
        self.parent = parent
        self.current_user = current_user or {"user": "Usuario", "role": "Usuario"}
        self.current_section = "Dashboard"
        
        # Repositorios
        self.user_repo = UserRepository()
        self.cicle_repo = CicleRepository()
        self.classroom_repo = ClassroomRepository()
        self.course_repo = CourseRepository()
        self.teacher_repo = TeacherRepository()
        self.student_repo = StudentRepository()
        self.team_repo = TeamRepository()
        self.inscription_repo = InscriptionRepository()
        self.payment_repo = PaymentRepository()
        
        # Generador de gráficos
        self.chart_generator = ChartGenerator()
        
        # Variables para Academia
        self.academia_subsection = "ciclo"  # "ciclo", "aulas" o "matricula"
        self.current_cicle_page = 1
        self.current_classroom_page = 1
        self.cicles_per_page = 10
        self.classrooms_per_page = 10
        self.active_cicle = None  # Ciclo activo seleccionado
        self.selected_aula_for_matricula = None  # Aula seleccionada para matrícula
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz del dashboard"""
        # Configurar tema claro
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Frame principal del dashboard
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        # Crear sidebar izquierdo
        self.create_sidebar()
        
        # Crear área de contenido principal
        self.create_content_area()
        
        # Mostrar contenido inicial del dashboard
        self.show_dashboard_content()
        
    def create_sidebar(self):
        """Crear barra lateral izquierda"""
        # Frame del sidebar
        self.sidebar = ctk.CTkFrame(
            self.main_frame,
            width=250,
            fg_color="#1f538d",
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo y nombre de usuario
        self.create_user_section()
        
        # Menú de navegación
        self.create_navigation_menu()
        
        # Configuración en la parte inferior
        self.create_config_section()
        
    def create_user_section(self):
        """Crear sección de usuario en la parte superior del sidebar"""
        # Frame para el usuario
        self.user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.user_frame.pack(fill="x", padx=20, pady=20)
        
        # Logo/Icono usando la imagen iacym.jpg
        import os
        
        # Crear frame para el logo
        self.logo_frame = ctk.CTkFrame(
            self.user_frame,
            width=60,
            height=60,
            fg_color="white",
            corner_radius=8
        )
        self.logo_frame.pack(pady=(0, 10))
        self.logo_frame.pack_propagate(False)
        
        # Cargar la imagen del logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "view", "images", "iacym.jpg")
        
        try:
            from PIL import Image, ImageTk
            
            if os.path.exists(logo_path):
                # Cargar y redimensionar la imagen
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image)
                
                # Crear label con la imagen
                self.logo_label = ctk.CTkLabel(
                    self.logo_frame,
                    image=logo_photo,
                    text=""
                )
                self.logo_label.pack(expand=True)
                self.logo_label.image = logo_photo  # Mantener referencia
            else:
                # Si no existe la imagen, usar texto como fallback
                self.logo_text = ctk.CTkLabel(
                    self.logo_frame,
                    text="AB",
                    font=ctk.CTkFont(size=25, weight="bold"),
                    text_color="#1f538d"
                )
                self.logo_text.pack(expand=True)
        except ImportError:
            # Si no hay PIL, usar texto como fallback
            self.logo_text = ctk.CTkLabel(
                self.logo_frame,
                text="AB",
                font=ctk.CTkFont(size=25, weight="bold"),
                text_color="#1f538d"
            )
            self.logo_text.pack(expand=True)
        
        # Nombre de usuario
        self.user_name_label = ctk.CTkLabel(
            self.user_frame,
            text=self.current_user.get("user", "Usuario"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        self.user_name_label.pack()
        
        # Rol del usuario
        self.user_role_label = ctk.CTkLabel(
            self.user_frame,
            text=self.current_user.get("role", "Usuario"),
            font=ctk.CTkFont(size=12),
            text_color="#b3d9ff"
        )
        self.user_role_label.pack()
        
    def create_navigation_menu(self):
        """Crear menú de navegación"""
        # Frame para el menú
        self.menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.menu_frame.pack(fill="x", padx=20, pady=20)
        
        # Elementos del menú
        self.menu_items = [
            ("Dashboard", "dashboard"),
            ("Academia", "academia"),
            ("Red", "red"),
            ("Cursos", "cursos"),
            ("Estudiantes", "estudiantes"),
            ("Docentes", "docentes")
        ]
        
        self.menu_buttons = {}
        
        for text, section in self.menu_items:
            # Crear botón del menú
            btn = ctk.CTkButton(
                self.menu_frame,
                text=text,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
                command=lambda s=section: self.navigate_to_section(s),
                fg_color="transparent",
                hover_color="#0d47a1",
                text_color="white",
                anchor="w"
            )
            btn.pack(fill="x", pady=2)
            self.menu_buttons[section] = btn
            
    def create_config_section(self):
        """Crear sección de configuración en la parte inferior"""
        # Frame para configuración
        self.config_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.config_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        # Botón de configuración
        self.config_btn = ctk.CTkButton(
            self.config_frame,
            text="Configuración",
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            command=lambda: self.navigate_to_section("configuracion"),
            fg_color="transparent",
            hover_color="#0d47a1",
            text_color="white",
            anchor="w"
        )
        self.config_btn.pack(fill="x", pady=2)
        
        # Botón de logout
        self.logout_btn = ctk.CTkButton(
            self.config_frame,
            text="Cerrar Sesión",
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            command=self.logout,
            fg_color="#dc3545",
            hover_color="#c82333",
            text_color="white",
            anchor="w"
        )
        self.logout_btn.pack(fill="x", pady=2)
        
    def create_content_area(self):
        """Crear área de contenido principal"""
        # Frame del contenido
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.content_frame.pack(side="right", fill="both", expand=True)
        
    def navigate_to_section(self, section):
        """Navegar a una sección específica"""
        # Actualizar botones del menú
        for btn_section, btn in self.menu_buttons.items():
            if btn_section == section:
                btn.configure(fg_color="#0d47a1")
            else:
                btn.configure(fg_color="transparent")
        
        # Actualizar sección actual
        self.current_section = section
        
        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Mostrar contenido según la sección
        if section == "dashboard":
            self.show_dashboard_content()
        elif section == "academia":
            self.show_academia_content()
        elif section == "red":
            self.show_red_content()
        elif section == "cursos":
            self.show_cursos_content()
        elif section == "estudiantes":
            self.show_estudiantes_content()
        elif section == "docentes":
            self.show_docentes_content()
        elif section == "configuracion":
            self.show_configuracion_content()
            
    def show_dashboard_content(self):
        """Mostrar contenido del dashboard con indicadores y gráficos"""
        # Título
        title = ctk.CTkLabel(
            self.content_frame,
            text="Dashboard - Academia Bíblica",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(20, 10))
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Crear indicadores
        self.create_dashboard_indicators(main_frame)
        
        # Crear gráficos
        self.create_dashboard_charts(main_frame)
    
    def create_dashboard_indicators(self, parent):
        """Crear indicadores del dashboard"""
        # Título de indicadores
        indicators_title = ctk.CTkLabel(
            parent,
            text="Indicadores Principales",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f538d"
        )
        indicators_title.pack(pady=(10, 15), anchor="w")
        
        # Frame para los indicadores
        indicators_frame = ctk.CTkFrame(parent, fg_color="transparent")
        indicators_frame.pack(fill="x", pady=(0, 20))
        
        # Obtener estadísticas
        stats = self.get_dashboard_statistics()
        
        # Indicador 1: Total de Estudiantes
        self.create_indicator_card(
            indicators_frame,
            title="Total Estudiantes",
            value=str(stats["total_students"]),
            color="#28a745",
            row=0,
            column=0
        )
        
        # Indicador 2: Aulas Activas
        self.create_indicator_card(
            indicators_frame,
            title="Aulas Activas",
            value=str(stats["active_classrooms"]),
            color="#007bff",
            row=0,
            column=1
        )
        
        # Indicador 3: Matrículas del Mes
        self.create_indicator_card(
            indicators_frame,
            title="Matrículas del Mes",
            value=str(stats["monthly_inscriptions"]),
            color="#ffc107",
            row=0,
            column=2
        )
    
    def create_indicator_card(self, parent, title, value, color, row, column):
        """Crear una tarjeta de indicador"""
        # Frame de la tarjeta
        card = ctk.CTkFrame(
            parent,
            width=200,
            height=120,
            corner_radius=15,
            fg_color="white",
            border_width=2,
            border_color=color
        )
        card.grid(row=row, column=column, padx=10, pady=5, sticky="ew")
        card.grid_propagate(False)
        
        # Configurar peso de columna
        parent.grid_columnconfigure(column, weight=1)
        
        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(28, 5))
        
        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#666666"
        )
        title_label.pack(pady=(0, 15))
    
    def get_dashboard_statistics(self):
        """Obtener estadísticas para el dashboard"""
        try:
            # Total de estudiantes
            total_students = len(self.student_repo.get_all_rows())
            
            # Aulas activas (todas las aulas por ahora)
            active_classrooms = len(self.classroom_repo.get_all_rows())
            
            # Matrículas del mes (todas las inscripciones por ahora)
            monthly_inscriptions = len(self.inscription_repo.get_all_rows())
            
            return {
                "total_students": total_students,
                "active_classrooms": active_classrooms,
                "monthly_inscriptions": monthly_inscriptions
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {
                "total_students": 0,
                "active_classrooms": 0,
                "monthly_inscriptions": 0
            }
    
    def create_dashboard_charts(self, parent):
        """Crear gráficos del dashboard con matplotlib"""
        # Título de gráficos
        charts_title = ctk.CTkLabel(
            parent,
            text="Gráficos y Estadísticas Avanzadas",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f538d"
        )
        charts_title.pack(pady=(20, 15), anchor="w")
        
        # Frame principal para los gráficos
        charts_main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        charts_main_frame.pack(fill="both", expand=True)
        
        # Primera fila de gráficos (3 gráficos)
        first_row_frame = ctk.CTkFrame(charts_main_frame, fg_color="transparent")
        first_row_frame.pack(fill="x", pady=(0, 10))
        first_row_frame.grid_columnconfigure(0, weight=1)
        first_row_frame.grid_columnconfigure(1, weight=1)
        first_row_frame.grid_columnconfigure(2, weight=1)
        
        # Gráfico 1: Gráfico de Línea - Tendencia de Matrículas
        self.create_line_chart_widget(first_row_frame, 0, 0)
        
        # Gráfico 2: Gráfico de Pastel - Distribución de Estudiantes por Equipo
        self.create_pie_chart_widget(first_row_frame, 0, 1)
        
        # Gráfico 3: Gráfico de Barras - Pagos por Método
        self.create_bar_chart_widget(first_row_frame, 0, 2)
        
        # Segunda fila de gráficos (2 gráficos nuevos)
        second_row_frame = ctk.CTkFrame(charts_main_frame, fg_color="transparent")
        second_row_frame.pack(fill="x", pady=(10, 0))
        second_row_frame.grid_columnconfigure(0, weight=1)
        second_row_frame.grid_columnconfigure(1, weight=1)
        
        # Gráfico 4: Histograma - Distribución de Edades
        self.create_histogram_widget(second_row_frame, 0, 0)
        
        # Gráfico 5: Gráfico de Dispersión - Rendimiento por Curso
        self.create_scatter_plot_widget(second_row_frame, 0, 1)
    
    def create_line_chart_widget(self, parent, row=0, column=0):
        """Crear widget de gráfico de línea"""
        try:
            # Frame del gráfico
            chart_frame = ctk.CTkFrame(
                parent,
                width=350,
                height=280,
                corner_radius=15,
                fg_color="white"
            )
            chart_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            chart_frame.pack_propagate(False)
            
            # Obtener datos para el gráfico de línea
            data = self.chart_generator.get_matriculas_trend_data(self.inscription_repo)
            
            # Crear gráfico de línea
            fig = self.chart_generator.create_line_chart(
                data=data,
                title="Tendencia de Matrículas",
                xlabel="Mes",
                ylabel="Cantidad de Matrículas",
                width=5.5,
                height=4
            )
            
            # Crear widget de matplotlib
            canvas = create_matplotlib_widget(fig, chart_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error creando gráfico de línea: {e}")
            # Crear mensaje de error
            error_label = ctk.CTkLabel(
                chart_frame,
                text="Error al cargar gráfico de línea",
                font=ctk.CTkFont(size=12),
                text_color="#dc3545"
            )
            error_label.pack(expand=True)
    
    def create_pie_chart_widget(self, parent, row=0, column=0):
        """Crear widget de gráfico de pastel"""
        try:
            # Frame del gráfico
            chart_frame = ctk.CTkFrame(
                parent,
                width=350,
                height=280,
                corner_radius=15,
                fg_color="white"
            )
            chart_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            chart_frame.pack_propagate(False)
            
            # Obtener datos para el gráfico de pastel
            data, labels = self.chart_generator.get_equipos_distribution_data(
                self.team_repo, self.student_repo
            )
            
            # Crear gráfico de pastel
            fig = self.chart_generator.create_pie_chart(
                data=data,
                labels=labels,
                title="Estudiantes por Equipo",
                width=5.5,
                height=4.5
            )
            
            # Crear widget de matplotlib
            canvas = create_matplotlib_widget(fig, chart_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error creando gráfico de pastel: {e}")
            # Crear mensaje de error
            error_label = ctk.CTkLabel(
                chart_frame,
                text="Error al cargar gráfico de pastel",
                font=ctk.CTkFont(size=12),
                text_color="#dc3545"
            )
            error_label.pack(expand=True)
    
    def create_bar_chart_widget(self, parent, row=0, column=0):
        """Crear widget de gráfico de barras"""
        try:
            # Frame del gráfico
            chart_frame = ctk.CTkFrame(
                parent,
                width=350,
                height=280,
                corner_radius=15,
                fg_color="white"
            )
            chart_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            chart_frame.pack_propagate(False)
            
            # Obtener datos para el gráfico de barras
            data, labels = self.chart_generator.get_payment_methods_data(self.payment_repo)
            
            # Crear gráfico de barras
            fig = self.chart_generator.create_bar_chart(
                data=data,
                labels=labels,
                title="Pagos por Método",
                xlabel="Método de Pago",
                ylabel="Cantidad de Pagos",
                width=5.5,
                height=4
            )
            
            # Crear widget de matplotlib
            canvas = create_matplotlib_widget(fig, chart_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error creando gráfico de barras: {e}")
            # Crear mensaje de error
            error_label = ctk.CTkLabel(
                chart_frame,
                text="Error al cargar gráfico de barras",
                font=ctk.CTkFont(size=12),
                text_color="#dc3545"
            )
            error_label.pack(expand=True)
    
    def create_histogram_widget(self, parent, row=0, column=0):
        """Crear widget de histograma"""
        try:
            # Frame del gráfico
            chart_frame = ctk.CTkFrame(
                parent,
                width=350,
                height=280,
                corner_radius=15,
                fg_color="white"
            )
            chart_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            chart_frame.pack_propagate(False)
            
            # Obtener datos para el histograma
            ages = self.chart_generator.get_student_age_distribution_data(self.student_repo)
            
            # Crear histograma
            fig = self.chart_generator.create_histogram(
                data=ages,
                title="Distribución de Edades",
                xlabel="Edad",
                ylabel="Cantidad de Estudiantes",
                bins=8,
                width=5.5,
                height=4
            )
            
            # Crear widget de matplotlib
            canvas = create_matplotlib_widget(fig, chart_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error creando histograma: {e}")
            # Crear mensaje de error
            error_label = ctk.CTkLabel(
                chart_frame,
                text="Error al cargar histograma",
                font=ctk.CTkFont(size=12),
                text_color="#dc3545"
            )
            error_label.pack(expand=True)
    
    def create_scatter_plot_widget(self, parent, row=0, column=0):
        """Crear widget de gráfico de dispersión"""
        try:
            # Frame del gráfico
            chart_frame = ctk.CTkFrame(
                parent,
                width=350,
                height=280,
                corner_radius=15,
                fg_color="white"
            )
            chart_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            chart_frame.pack_propagate(False)
            
            # Obtener datos para el gráfico de dispersión
            x_data, y_data = self.chart_generator.get_course_performance_data(
                self.course_repo, self.student_repo, self.inscription_repo
            )
            
            # Crear gráfico de dispersión
            fig = self.chart_generator.create_scatter_plot(
                x_data=x_data,
                y_data=y_data,
                title="Rendimiento por Curso",
                xlabel="Estudiantes Inscritos",
                ylabel="Rendimiento (%)",
                width=5.5,
                height=4
            )
            
            # Crear widget de matplotlib
            canvas = create_matplotlib_widget(fig, chart_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error creando gráfico de dispersión: {e}")
            # Crear mensaje de error
            error_label = ctk.CTkLabel(
                chart_frame,
                text="Error al cargar gráfico de dispersión",
                font=ctk.CTkFont(size=12),
                text_color="#dc3545"
            )
            error_label.pack(expand=True)
    
    def get_chart_color(self, index):
        """Obtener color para gráficos basado en índice"""
        colors = ["#28a745", "#007bff", "#ffc107", "#dc3545", "#6f42c1", "#20c997"]
        return colors[index % len(colors)]
        
    def show_academia_content(self):
        """Mostrar contenido de Academia con navegación entre Ciclo y Aulas"""
        # Contenido según la subsección seleccionada
        if self.academia_subsection == "ciclo":
            self.show_ciclo_content()
        elif self.academia_subsection == "aulas":
            self.show_aulas_content()
        elif self.academia_subsection == "matricula":
            self.show_matricula_content()
    
    
    def create_academia_navigation(self):
        """Crear navegación entre subsecciones de Academia"""
        # Este método ya no es necesario, se eliminó para evitar espacio adicional
        pass
        
        
    
    def switch_academia_subsection(self, subsection):
        """Cambiar entre subsecciones de Academia con validación de flujo"""
        # Validar flujo correcto
        if subsection == "aulas" and not self.active_cicle:
            messagebox.showwarning(
                "Ciclo Requerido", 
                "Debe seleccionar un ciclo activo antes de acceder a las aulas.\n\nPor favor, primero cree o seleccione un ciclo."
            )
            return
        
        if subsection == "matricula" and not self.active_cicle:
            messagebox.showwarning(
                "Ciclo Requerido", 
                "Debe seleccionar un ciclo activo antes de crear matrículas.\n\nPor favor, primero cree o seleccione un ciclo."
            )
            return
        
        self.academia_subsection = subsection
        
        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            if widget.winfo_class() != "CTkLabel" or "ACADEMIA BIBLICA" not in widget.cget("text"):
                widget.destroy()
        
        # Mostrar contenido según la subsección
        if subsection == "ciclo":
            self.show_ciclo_content()
        elif subsection == "aulas":
            self.show_aulas_content()
        elif subsection == "matricula":
            self.show_matricula_content()
    
    def show_ciclo_content(self):
        """Mostrar contenido de gestión de Ciclos"""
        # Frame principal para Ciclo
        ciclo_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        ciclo_frame.pack(fill="both", expand=True, padx=20, pady=(0, 0))
        
        # Header con título y botones de acción
        header_frame = ctk.CTkFrame(ciclo_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame,
            text="CICLOS",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#1f538d"
        )
        title_label.pack(side="left", pady=(0, 5))
        
        # Frame para botones de acción
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right", pady=(0, 5))
        
        # Botón Finalizar Ciclo
        finalizar_btn = ctk.CTkButton(
            actions_frame,
            text="Finalizar Ciclo",
            width=160,
            height=42,
            command=self.finalizar_ciclo_activo,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        finalizar_btn.pack(side="right", padx=(8, 0))
        
        # Botón Exportar Excel
        export_btn = ctk.CTkButton(
            actions_frame,
            text="Exportar Excel",
            width=160,
            height=42,
            command=self.export_ciclos_excel,
            fg_color="#17a2b8",
            hover_color="#138496",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        export_btn.pack(side="right", padx=(8, 0))
        
        # Botón Agregar Ciclo
        add_ciclo_btn = ctk.CTkButton(
            actions_frame,
            text="Agregar Ciclo",
            width=160,
            height=42,
            command=self.show_add_ciclo_dialog,
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        add_ciclo_btn.pack(side="right", padx=(8, 0))
        
        # Filtros
        self.create_ciclo_filters(ciclo_frame)
        
        # Tabla de ciclos
        self.create_ciclo_table(ciclo_frame)
        
        # Paginación
        self.create_ciclo_pagination(ciclo_frame)
        
        # Cargar datos
        self.load_ciclos()
    
    def create_ciclo_filters(self, parent):
        """Crear filtros para la tabla de ciclos"""
        filters_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        filters_frame.pack(fill="x", pady=(0, 12))
        
        # Título de filtros
        filters_title = ctk.CTkLabel(
            filters_frame,
            text="FILTROS DE BÚSQUEDA",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        filters_title.pack(pady=(12, 8))
        
        # Frame para primera fila de filtros
        filters_row1 = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_row1.pack(fill="x", padx=20, pady=(0, 8))
        
        # Encargado
        encargado_frame = ctk.CTkFrame(filters_row1, fg_color="transparent")
        encargado_frame.pack(side="left", padx=(0, 25))
        
        encargado_label = ctk.CTkLabel(encargado_frame, text="Encargado:", font=ctk.CTkFont(size=13, weight="bold"))
        encargado_label.pack(anchor="w")
        
        self.ciclo_encargado_var = ctk.StringVar()
        self.ciclo_encargado_var.trace('w', self.filter_ciclos)
        encargado_entry = ctk.CTkEntry(
            encargado_frame,
            placeholder_text="Buscar por encargado...",
            textvariable=self.ciclo_encargado_var,
            width=200,
            height=32
        )
        encargado_entry.pack(pady=(6, 0))
        
        # Año
        año_frame = ctk.CTkFrame(filters_row1, fg_color="transparent")
        año_frame.pack(side="left", padx=(0, 25))
        
        año_label = ctk.CTkLabel(año_frame, text="Año:", font=ctk.CTkFont(size=13, weight="bold"))
        año_label.pack(anchor="w")
        
        self.ciclo_año_var = ctk.StringVar()
        self.ciclo_año_var.set("Todos")
        self.ciclo_año_var.trace('w', self.filter_ciclos)
        año_combo = ctk.CTkComboBox(
            año_frame,
            values=["Todos", "2023", "2024", "2025", "2026"],
            variable=self.ciclo_año_var,
            width=130,
            height=32
        )
        año_combo.pack(pady=(6, 0))
        
        # Ciclo
        ciclo_frame = ctk.CTkFrame(filters_row1, fg_color="transparent")
        ciclo_frame.pack(side="left", padx=(0, 25))
        
        ciclo_label = ctk.CTkLabel(ciclo_frame, text="Ciclo:", font=ctk.CTkFont(size=13, weight="bold"))
        ciclo_label.pack(anchor="w")
        
        self.ciclo_numero_var = ctk.StringVar()
        self.ciclo_numero_var.set("Todos")
        self.ciclo_numero_var.trace('w', self.filter_ciclos)
        ciclo_combo = ctk.CTkComboBox(
            ciclo_frame,
            values=["Todos", "I", "II", "III", "IV", "V"],
            variable=self.ciclo_numero_var,
            width=110,
            height=32
        )
        ciclo_combo.pack(pady=(6, 0))
        
        # Frame para segunda fila de filtros
        filters_row2 = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_row2.pack(fill="x", padx=20, pady=(0, 12))
        
        # Fecha Inicio
        fecha_inicio_frame = ctk.CTkFrame(filters_row2, fg_color="transparent")
        fecha_inicio_frame.pack(side="left", padx=(0, 25))
        
        fecha_inicio_label = ctk.CTkLabel(fecha_inicio_frame, text="Fecha Inicio:", font=ctk.CTkFont(size=13, weight="bold"))
        fecha_inicio_label.pack(anchor="w")
        
        self.ciclo_fecha_inicio_var = ctk.StringVar()
        self.ciclo_fecha_inicio_var.trace('w', self.filter_ciclos)
        fecha_inicio_entry = ctk.CTkEntry(
            fecha_inicio_frame,
            placeholder_text="DD-MM-AAAA",
            textvariable=self.ciclo_fecha_inicio_var,
            width=150,
            height=32
        )
        fecha_inicio_entry.pack(pady=(6, 0))
        
        # Fecha Cierre
        fecha_cierre_frame = ctk.CTkFrame(filters_row2, fg_color="transparent")
        fecha_cierre_frame.pack(side="left", padx=(0, 25))
        
        fecha_cierre_label = ctk.CTkLabel(fecha_cierre_frame, text="Fecha Cierre:", font=ctk.CTkFont(size=13, weight="bold"))
        fecha_cierre_label.pack(anchor="w")
        
        self.ciclo_fecha_cierre_var = ctk.StringVar()
        self.ciclo_fecha_cierre_var.trace('w', self.filter_ciclos)
        fecha_cierre_entry = ctk.CTkEntry(
            fecha_cierre_frame,
            placeholder_text="DD-MM-AAAA",
            textvariable=self.ciclo_fecha_cierre_var,
            width=150,
            height=32
        )
        fecha_cierre_entry.pack(pady=(6, 0))
        
        # Botón limpiar filtros
        clear_filters_btn = ctk.CTkButton(
            filters_row2,
            text="Limpiar Filtros",
            width=140,
            height=32,
            command=self.clear_ciclo_filters,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=12)
        )
        clear_filters_btn.pack(side="right", pady=(25, 0))
    
    def create_ciclo_table(self, parent):
        """Crear tabla de ciclos"""
        # Título de la tabla
        table_title = ctk.CTkLabel(
            parent,
            text="LISTADO DE CICLOS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f538d"
        )
        table_title.pack(pady=(0, 8), anchor="w")
        
        # Frame principal de la tabla
        table_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        table_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Configurar estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="white",
                       foreground="black",
                       rowheight=40,
                       fieldbackground="white",
                       font=("Arial", 11))
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       font=("Arial", 12, "bold"))
        style.map("Treeview.Heading",
                 background=[("active", "#0056b3")])
        
        # Configurar tags para filas
        style.configure("activo.Treeview", background="#e8f5e8")
        style.configure("inactivo.Treeview", background="#f8f9fa")
        
        columns = ("Estado", "Año", "Ciclo", "Fecha Inicio", "Fecha Fin", "Encargado", "Acciones")
        self.ciclo_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Configurar encabezados
        self.ciclo_tree.heading("Estado", text="ESTADO")
        self.ciclo_tree.heading("Año", text="AÑO")
        self.ciclo_tree.heading("Ciclo", text="CICLO")
        self.ciclo_tree.heading("Fecha Inicio", text="FECHA INICIO")
        self.ciclo_tree.heading("Fecha Fin", text="FECHA FIN")
        self.ciclo_tree.heading("Encargado", text="ENCARGADO")
        self.ciclo_tree.heading("Acciones", text="ACCIONES")
        
        # Configurar columnas
        self.ciclo_tree.column("Estado", width=100, anchor="center")
        self.ciclo_tree.column("Año", width=80, anchor="center")
        self.ciclo_tree.column("Ciclo", width=80, anchor="center")
        self.ciclo_tree.column("Fecha Inicio", width=140, anchor="center")
        self.ciclo_tree.column("Fecha Fin", width=140, anchor="center")
        self.ciclo_tree.column("Encargado", width=200, anchor="center")
        self.ciclo_tree.column("Acciones", width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.ciclo_tree.yview)
        self.ciclo_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack con padding
        self.ciclo_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Eventos
        self.ciclo_tree.bind("<Double-1>", self.on_ciclo_double_click)
        self.ciclo_tree.bind("<Button-3>", self.show_ciclo_context_menu)
        
        # Configurar selección
        self.ciclo_tree.bind("<<TreeviewSelect>>", self.on_ciclo_select)
    
    def create_ciclo_pagination(self, parent):
        """Crear controles de paginación para ciclos"""
        pagination_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        pagination_frame.pack(fill="x", pady=(0, 10))
        
        # Frame para información de paginación
        info_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        info_frame.pack(side="left", padx=20, pady=8)
        
        self.ciclo_pagination_label = ctk.CTkLabel(
            info_frame,
            text="1/1 Páginas",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#1f538d"
        )
        self.ciclo_pagination_label.pack()
        
        # Frame para botones de navegación
        nav_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        nav_frame.pack(side="right", padx=20, pady=8)
        
        prev_btn = ctk.CTkButton(
            nav_frame,
            text="Anterior",
            width=110,
            height=32,
            command=self.previous_ciclo_page,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        prev_btn.pack(side="left", padx=(0, 8))
        
        next_btn = ctk.CTkButton(
            nav_frame,
            text="Siguiente",
            width=110,
            height=32,
            command=self.next_ciclo_page,
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        next_btn.pack(side="left")
    
    def clear_ciclo_filters(self):
        """Limpiar todos los filtros de ciclos"""
        self.ciclo_encargado_var.set("")
        self.ciclo_año_var.set("Todos")
        self.ciclo_numero_var.set("Todos")
        self.ciclo_fecha_inicio_var.set("")
        self.ciclo_fecha_cierre_var.set("")
        self.filter_ciclos()
    
    def on_ciclo_select(self, event):
        """Manejar selección de ciclo en la tabla"""
        selection = self.ciclo_tree.selection()
        if selection:
            item = self.ciclo_tree.item(selection[0])
            values = item['values']
            # Aquí puedes agregar lógica adicional cuando se selecciona un ciclo
            pass
    
    def finalizar_ciclo_activo(self):
        """Finalizar el ciclo activo"""
        if not self.active_cicle:
            messagebox.showwarning("Advertencia", "No hay ningún ciclo activo para finalizar.")
            return
        
        # Confirmar finalización
        respuesta = messagebox.askyesno(
            "Finalizar Ciclo",
            f"¿Está seguro de que desea finalizar el ciclo {self.active_cicle.get('cicle')} ({self.active_cicle.get('date_start')[:4]})?\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                # Aquí iría la lógica para finalizar el ciclo
                # Por ejemplo, marcar como finalizado en la base de datos
                self.active_cicle = None
                messagebox.showinfo("Éxito", "Ciclo finalizado correctamente.")
                self.load_ciclos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al finalizar ciclo: {e}")
    
    def export_ciclos_excel(self):
        """Exportar ciclos a Excel"""
        try:
            from tkinter import filedialog
            import pandas as pd
            
            # Obtener datos de ciclos
            ciclos = self.cicle_repo.get_all_rows()
            if not ciclos:
                messagebox.showwarning("Advertencia", "No hay ciclos para exportar.")
                return
            
            # Crear DataFrame
            df_data = []
            for ciclo in ciclos:
                df_data.append({
                    'Estado': 'ACTIVO' if (self.active_cicle and self.active_cicle.get("id") == ciclo.get("id")) else 'Inactivo',
                    'Año': str(ciclo.get("date_start", ""))[:4] if ciclo.get("date_start") else "",
                    'Ciclo': ciclo.get("cicle", ""),
                    'Fecha Inicio': str(ciclo.get("date_start", "")),
                    'Fecha Fin': str(ciclo.get("date_end", "")),
                    'Encargado': ciclo.get("manager", "")
                })
            
            df = pd.DataFrame(df_data)
            
            # Seleccionar archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Guardar reporte de ciclos"
            )
            
            if filename:
                df.to_excel(filename, index=False, engine='openpyxl')
                messagebox.showinfo("Éxito", f"Reporte exportado correctamente a:\n{filename}")
                
        except ImportError:
            messagebox.showerror("Error", "Para exportar a Excel necesita instalar pandas y openpyxl:\npip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")
    
    def load_ciclos(self):
        """Cargar ciclos desde la base de datos"""
        try:
            # Obtener todos los ciclos
            ciclos = self.cicle_repo.get_all_rows()
            
            # Aplicar filtros
            ciclos_filtrados = self.apply_ciclo_filters(ciclos)
            
            # Actualizar tabla
            self.update_ciclo_table(ciclos_filtrados)
            
            # Actualizar paginación
            total_pages = (len(ciclos_filtrados) + self.cicles_per_page - 1) // self.cicles_per_page
            self.ciclo_pagination_label.configure(text=f"{self.current_cicle_page}/{max(1, total_pages)} Páginas")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ciclos: {e}")
    
    def apply_ciclo_filters(self, ciclos):
        """Aplicar filtros a la lista de ciclos"""
        filtered = ciclos.copy()
        
        # Filtrar por encargado
        encargado = self.ciclo_encargado_var.get().strip().lower()
        if encargado:
            filtered = [c for c in filtered if encargado in c.get("manager", "").lower()]
        
        # Filtrar por año
        año = self.ciclo_año_var.get()
        if año != "Todos":
            filtered = [c for c in filtered if str(c.get("date_start", "")).startswith(año)]
        
        # Filtrar por ciclo
        ciclo = self.ciclo_numero_var.get()
        if ciclo != "Todos":
            filtered = [c for c in filtered if c.get("cicle", "") == ciclo]
        
        # Filtrar por fecha inicio
        fecha_inicio = self.ciclo_fecha_inicio_var.get().strip()
        if fecha_inicio:
            filtered = [c for c in filtered if fecha_inicio in str(c.get("date_start", ""))]
        
        # Filtrar por fecha cierre
        fecha_cierre = self.ciclo_fecha_cierre_var.get().strip()
        if fecha_cierre:
            filtered = [c for c in filtered if fecha_cierre in str(c.get("date_end", ""))]
        
        return filtered
    
    def update_ciclo_table(self, ciclos):
        """Actualizar la tabla de ciclos"""
        # Limpiar tabla
        for item in self.ciclo_tree.get_children():
            self.ciclo_tree.delete(item)
        
        # Calcular rango de páginas
        start_idx = (self.current_cicle_page - 1) * self.cicles_per_page
        end_idx = start_idx + self.cicles_per_page
        
        # Agregar ciclos de la página actual
        for ciclo in ciclos[start_idx:end_idx]:
            año = str(ciclo.get("date_start", ""))[:4] if ciclo.get("date_start") else ""
            fecha_inicio = str(ciclo.get("date_start", "")) if ciclo.get("date_start") else ""
            fecha_fin = str(ciclo.get("date_end", "")) if ciclo.get("date_end") else ""
            
            # Determinar estado del ciclo
            if self.active_cicle and self.active_cicle.get("id") == ciclo.get("id"):
                estado = "ACTIVO"
                acciones = "Ver | Editar | Desactivar"
                tags = ("activo",)
            else:
                estado = "INACTIVO"
                acciones = "Ver | Editar | Activar"
                tags = ("inactivo",)
            
            item_id = self.ciclo_tree.insert("", "end", values=(
                estado,
                año,
                ciclo.get("cicle", ""),
                fecha_inicio,
                fecha_fin,
                ciclo.get("manager", ""),
                acciones
            ), tags=tags)
            
            # Configurar tags para colores alternados
            if len(self.ciclo_tree.get_children()) % 2 == 0:
                self.ciclo_tree.set(item_id, "#", len(self.ciclo_tree.get_children()))
    
    def filter_ciclos(self, *args):
        """Filtrar ciclos en tiempo real"""
        self.current_cicle_page = 1
        self.load_ciclos()
    
    def previous_ciclo_page(self):
        """Ir a la página anterior de ciclos"""
        if self.current_cicle_page > 1:
            self.current_cicle_page -= 1
            self.load_ciclos()
    
    def next_ciclo_page(self):
        """Ir a la página siguiente de ciclos"""
        try:
            ciclos = self.cicle_repo.get_all_rows()
            ciclos_filtrados = self.apply_ciclo_filters(ciclos)
            total_pages = (len(ciclos_filtrados) + self.cicles_per_page - 1) // self.cicles_per_page
            
            if self.current_cicle_page < total_pages:
                self.current_cicle_page += 1
                self.load_ciclos()
        except Exception as e:
            messagebox.showerror("Error", f"Error en paginación: {e}")
    
    def show_add_ciclo_dialog(self):
        """Mostrar diálogo para agregar nuevo ciclo"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Agregar Ciclo")
        dialog.geometry("500x550")
        dialog.resizable(False, False)
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (550 // 2)
        dialog.geometry(f"500x550+{x}+{y}")
        
        # Hacer modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Título
        title = ctk.CTkLabel(
            dialog,
            text="AGREGAR CICLO",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=20)
        
        # Frame para campos (sin expand)
        fields_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Ciclo
        ciclo_label = ctk.CTkLabel(fields_frame, text="Ciclo:", font=ctk.CTkFont(size=14))
        ciclo_label.pack(pady=(0, 5), anchor="w")
        
        ciclo_var = ctk.StringVar()
        ciclo_combo = ctk.CTkComboBox(
            fields_frame,
            values=["I", "II", "III", "IV", "V"],
            variable=ciclo_var,
            width=450,
            height=35
        )
        ciclo_combo.pack(pady=(0, 15))
        
        # Encargado
        encargado_label = ctk.CTkLabel(fields_frame, text="Encargado:", font=ctk.CTkFont(size=14))
        encargado_label.pack(pady=(0, 5), anchor="w")
        
        encargado_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese nombre del encargado",
            width=450,
            height=35
        )
        encargado_entry.pack(pady=(0, 15))
        
        # Fecha Inicio
        fecha_inicio_label = ctk.CTkLabel(fields_frame, text="Fecha Inicio:", font=ctk.CTkFont(size=14))
        fecha_inicio_label.pack(pady=(0, 5), anchor="w")
        
        fecha_inicio_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="YYYY-MM-DD",
            width=450,
            height=35
        )
        fecha_inicio_entry.pack(pady=(0, 15))
        
        # Fecha Fin
        fecha_fin_label = ctk.CTkLabel(fields_frame, text="Fecha Fin:", font=ctk.CTkFont(size=14))
        fecha_fin_label.pack(pady=(0, 5), anchor="w")
        
        fecha_fin_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="YYYY-MM-DD",
            width=450,
            height=35
        )
        fecha_fin_entry.pack(pady=(0, 15))
        
        # Frame para botones (separado y visible)
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 30), padx=20)
        
        def add_ciclo():
            ciclo = ciclo_var.get()
            encargado = encargado_entry.get().strip()
            fecha_inicio = fecha_inicio_entry.get().strip()
            fecha_fin = fecha_fin_entry.get().strip()
            
            # Validaciones
            if not ciclo or not encargado or not fecha_inicio or not fecha_fin:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return
            
            try:
                # Crear ciclo
                self.cicle_repo.insert_row({
                    "cicle": ciclo,
                    "manager": encargado,
                    "date_start": fecha_inicio,
                    "date_end": fecha_fin
                })
                
                messagebox.showinfo("Éxito", "Ciclo creado correctamente.")
                dialog.destroy()
                
                # Recargar ciclos
                self.load_ciclos()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear ciclo: {e}")
        
        def cancel():
            dialog.destroy()
        
        # Botones (más grandes y centrados)
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="AGREGAR CICLO",
            width=200,
            height=50,
            command=add_ciclo,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        add_btn.pack(side="left", padx=(0, 20))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="CANCELAR",
            width=200,
            height=50,
            command=cancel,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        cancel_btn.pack(side="left")
        
        # Enfocar en el primer campo
        ciclo_combo.focus()
    
    def activate_ciclo(self, ciclo_id):
        """Activar un ciclo específico"""
        try:
            # Obtener el ciclo por ID
            ciclos = self.cicle_repo.get_all_rows()
            ciclo = next((c for c in ciclos if c.get("id") == ciclo_id), None)
            
            if ciclo:
                self.active_cicle = ciclo
                messagebox.showinfo(
                    "Ciclo Activado", 
                    f"Ciclo {ciclo.get('cicle')} ({ciclo.get('date_start')[:4]}) activado correctamente.\n\nAhora puede acceder a las aulas y crear matrículas."
                )
                
                # Actualizar la tabla
                self.load_ciclos()
                
                # Actualizar el título si estamos en la vista de ciclo
                if self.academia_subsection == "ciclo":
                    self.update_ciclo_title()
            else:
                messagebox.showerror("Error", "No se pudo encontrar el ciclo seleccionado.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al activar ciclo: {e}")
    
    def update_ciclo_title(self):
        """Actualizar el título con el ciclo activo"""
        # El título ahora es fijo como "CICLOS"
        pass
    
    def show_ciclo_context_menu(self, event):
        """Mostrar menú contextual para ciclo"""
        try:
            # Obtener elemento seleccionado
            item = self.ciclo_tree.identify_row(event.y)
            if not item:
                return
            
            # Seleccionar el elemento
            self.ciclo_tree.selection_set(item)
            values = self.ciclo_tree.item(item, "values")
            
            # Obtener ID del ciclo (asumiendo que está en los datos)
            # Por simplicidad, usaremos el índice como ID temporal
            ciclo_index = self.ciclo_tree.index(item)
            
            # Crear menú contextual
            context_menu = tk.Menu(self.parent, tearoff=0)
            
            # Ver aulas
            context_menu.add_command(
                label="Ver Aulas",
                command=lambda: self.on_ciclo_double_click(event)
            )
            
            # Editar
            context_menu.add_command(
                label="Editar Ciclo",
                command=lambda: self.show_edit_ciclo_dialog(event)
            )
            
            # Eliminar
            context_menu.add_command(
                label="Eliminar Ciclo",
                command=lambda: self.delete_ciclo(ciclo_index + 1)  # ID temporal
            )
            
            # Separador
            context_menu.add_separator()
            
            # Activar/Desactivar
            if values[0] == "ACTIVO":
                context_menu.add_command(
                    label="Desactivar",
                    command=lambda: self.deactivate_ciclo()
                )
            else:
                context_menu.add_command(
                    label="Activar Ciclo",
                    command=lambda: self.activate_ciclo(ciclo_index + 1)  # ID temporal
                )
            
            # Mostrar menú
            context_menu.tk_popup(event.x_root, event.y_root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar menú: {e}")
    
    def deactivate_ciclo(self):
        """Desactivar el ciclo actual"""
        if self.active_cicle:
            self.active_cicle = None
            messagebox.showinfo("Ciclo Desactivado", "El ciclo ha sido desactivado.")
            self.load_ciclos()
            self.update_ciclo_title()
        else:
            messagebox.showinfo("Info", "No hay ningún ciclo activo.")
    
    def show_ciclo_details(self, ciclo_index):
        """Mostrar detalles del ciclo"""
        messagebox.showinfo("Detalles del Ciclo", "Funcionalidad de detalles en desarrollo")
    
    def delete_ciclo(self, ciclo_id):
        """Eliminar ciclo con confirmación"""
        try:
            # Obtener datos del ciclo
            ciclos = self.cicle_repo.get_all_rows()
            ciclo_data = None
            
            # Buscar el ciclo por índice (temporal)
            if ciclo_id <= len(ciclos):
                ciclo_data = ciclos[ciclo_id - 1]
            
            if not ciclo_data:
                messagebox.showerror("Error", "No se pudo encontrar el ciclo.")
                return
            
            # Mostrar confirmación
            ciclo_name = ciclo_data.get("cicle", "")
            manager = ciclo_data.get("manager", "")
            
            result = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar el ciclo {ciclo_name}?\n\n"
                f"Encargado: {manager}\n\n"
                f"ADVERTENCIA: Esta acción eliminará:\n"
                f"• Todas las aulas del ciclo\n"
                f"• Todas las inscripciones de esas aulas\n"
                f"• Todos los pagos relacionados\n\n"
                f"Esta acción NO se puede deshacer."
            )
            
            if result:
                # Usar eliminación en cascada
                success = self.cicle_repo.delete_cicle_cascade(ciclo_data.get("id"))
                
                if success:
                    messagebox.showinfo("Éxito", f"Ciclo {ciclo_name} eliminado correctamente")
                    
                    # Si era el ciclo activo, desactivarlo
                    if self.active_cicle and self.active_cicle.get("id") == ciclo_data.get("id"):
                        self.active_cicle = None
                        self.update_ciclo_title()
                    
                    # Recargar la tabla
                    self.load_ciclos()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el ciclo")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar ciclo: {e}")
    
    def on_ciclo_double_click(self, event):
        """Manejar doble clic en fila de ciclo para ver aulas"""
        try:
            # Obtener elemento seleccionado
            item = self.ciclo_tree.selection()[0] if self.ciclo_tree.selection() else None
            if not item:
                return
            
            # Obtener datos del ciclo
            values = self.ciclo_tree.item(item, "values")
            ciclo_name = values[2]  # Columna "Ciclo"
            año = values[1]  # Columna "Año"
            
            # Obtener el ciclo completo de la base de datos
            ciclos = self.cicle_repo.get_all_rows()
            ciclo_data = next((c for c in ciclos if c.get("cicle") == ciclo_name), None)
            
            if ciclo_data:
                # Mostrar vista de aulas del ciclo
                self.show_aulas_del_ciclo(ciclo_data)
            else:
                messagebox.showerror("Error", "No se pudo encontrar los datos del ciclo.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar aulas del ciclo: {e}")
    
    def show_aulas_del_ciclo(self, ciclo_data):
        """Mostrar aulas de un ciclo específico"""
        # Crear ventana modal para aulas del ciclo
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"Aulas - Ciclo {ciclo_data.get('cicle')} {ciclo_data.get('date_start')[:4]}")
        dialog.geometry("1000x700")
        dialog.resizable(True, True)
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (1000 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"1000x700+{x}+{y}")
        
        # Hacer modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Título
        title = ctk.CTkLabel(
            dialog,
            text=f"AULAS - CICLO {ciclo_data.get('cicle')} {ciclo_data.get('date_start')[:4]}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=20)
        
        # Información del ciclo
        info_frame = ctk.CTkFrame(dialog, fg_color="#e3f2fd", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        info_text = f"Período: {ciclo_data.get('date_start')} - {ciclo_data.get('date_end')} | Encargado: {ciclo_data.get('manager')}"
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color="#1565c0"
        )
        info_label.pack(pady=10)
        
        # Frame para botones de acción
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Botón Agregar Aula
        add_aula_btn = ctk.CTkButton(
            buttons_frame,
            text="Agregar Aula",
            width=150,
            height=40,
            command=lambda: self.show_add_aula_dialog(ciclo_data.get('id'), aulas_tree),
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        add_aula_btn.pack(side="right", padx=(10, 0))
        
        # Botón Matrícula
        matricula_btn = ctk.CTkButton(
            buttons_frame,
            text="Matrícula",
            width=150,
            height=40,
            command=lambda: self.show_matricula_from_aulas(ciclo_data),
            fg_color="#6f42c1",
            hover_color="#5a32a3",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        matricula_btn.pack(side="right")
        
        # Tabla de aulas
        table_frame = ctk.CTkFrame(dialog)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ("Curso", "Aula", "Docente", "Fecha Inicio", "Fecha Fin", "Acciones")
        aulas_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        aulas_tree.heading("Curso", text="Curso")
        aulas_tree.heading("Aula", text="Aula")
        aulas_tree.heading("Docente", text="Docente")
        aulas_tree.heading("Fecha Inicio", text="Fecha Inicio")
        aulas_tree.heading("Fecha Fin", text="Fecha Fin")
        aulas_tree.heading("Acciones", text="Acciones")
        
        aulas_tree.column("Curso", width=150, anchor="center")
        aulas_tree.column("Aula", width=150, anchor="center")
        aulas_tree.column("Docente", width=200, anchor="center")
        aulas_tree.column("Fecha Inicio", width=120, anchor="center")
        aulas_tree.column("Fecha Fin", width=120, anchor="center")
        aulas_tree.column("Acciones", width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=aulas_tree.yview)
        aulas_tree.configure(yscrollcommand=scrollbar.set)
        
        aulas_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cargar aulas del ciclo
        self.load_aulas_del_ciclo(aulas_tree, ciclo_data.get('id'))
        
        # Eventos de la tabla
        aulas_tree.bind("<Double-1>", lambda e: self.on_aula_double_click(e, aulas_tree, ciclo_data))
        aulas_tree.bind("<Button-3>", lambda e: self.show_aula_context_menu(e, aulas_tree, ciclo_data))
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            dialog,
            text="Cerrar",
            width=100,
            height=35,
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=12)
        )
        close_btn.pack(pady=(0, 20))
    
    def load_aulas_del_ciclo(self, tree, ciclo_id):
        """Cargar aulas de un ciclo específico"""
        try:
            # Obtener todas las aulas
            aulas = self.classroom_repo.get_all_rows()
            
            # Filtrar aulas del ciclo
            aulas_ciclo = [aula for aula in aulas if aula.get("id_cicle") == ciclo_id]
            
            # Obtener datos de cursos y docentes para mostrar nombres
            cursos = self.course_repo.get_all_rows()
            docentes = self.teacher_repo.get_all_rows()
            
            # Crear diccionarios para búsqueda rápida
            cursos_dict = {c.get("id"): c.get("name", "") for c in cursos}
            docentes_dict = {d.get("id"): f"{d.get('name', '')} {d.get('lastname', '')}" for d in docentes}
            
            # Limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            
            # Agregar aulas
            for aula in aulas_ciclo:
                # Obtener nombres
                curso_nombre = cursos_dict.get(aula.get("id_course"), "Curso no encontrado")
                docente_nombre = docentes_dict.get(aula.get("id_teacher"), "Docente no encontrado")
                
                tree.insert("", "end", values=(
                    curso_nombre,
                    aula.get("name", ""),
                    docente_nombre,
                    str(aula.get("start_date", "")),
                    str(aula.get("end_date", "")),
                    "Ver | Editar | Eliminar"
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar aulas: {e}")
    
    def on_aula_double_click(self, event, tree, ciclo_data):
        """Manejar doble clic en aula para ver matriculados"""
        try:
            # Obtener elemento seleccionado
            item = tree.selection()[0] if tree.selection() else None
            if not item:
                return
            
            # Obtener datos del aula
            values = tree.item(item, "values")
            aula_name = values[1]  # Columna "Aula"
            
            # Mostrar matriculados del aula
            self.show_matriculados_del_aula(aula_name, ciclo_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar matriculados: {e}")
    
    def show_matriculados_del_aula(self, aula_name, ciclo_data):
        """Mostrar matriculados de un aula específica"""
        # Crear ventana modal para matriculados
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"Matriculados - {aula_name}")
        dialog.geometry("1200x600")
        dialog.resizable(True, True)
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (1200 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"1200x600+{x}+{y}")
        
        # Hacer modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Título
        title = ctk.CTkLabel(
            dialog,
            text=f"MATRICULADOS - {aula_name}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=20)
        
        # Información del aula y ciclo
        info_frame = ctk.CTkFrame(dialog, fg_color="#e8f5e8", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        info_text = f"Aula: {aula_name} | Ciclo: {ciclo_data.get('cicle')} {ciclo_data.get('date_start')[:4]} | Encargado: {ciclo_data.get('manager')}"
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color="#2e7d32"
        )
        info_label.pack(pady=10)
        
        # Botón Agregar Matrícula
        add_matricula_btn = ctk.CTkButton(
            dialog,
            text="Agregar Matrícula",
            width=180,
            height=40,
            command=lambda: self.show_add_matricula_dialog(aula_name, ciclo_data),
            fg_color="#6f42c1",
            hover_color="#5a32a3",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        add_matricula_btn.pack(pady=(0, 20), padx=20, anchor="e")
        
        # Tabla de matriculados
        table_frame = ctk.CTkFrame(dialog)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ("Estudiante", "Curso", "Red", "Fecha Matrícula", "Tipo Material", "Estado", "Material", "Pagos", "Acciones")
        matriculados_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        matriculados_tree.heading("Estudiante", text="Estudiante")
        matriculados_tree.heading("Curso", text="Curso")
        matriculados_tree.heading("Red", text="Red")
        matriculados_tree.heading("Fecha Matrícula", text="Fecha Matrícula")
        matriculados_tree.heading("Tipo Material", text="Tipo Material")
        matriculados_tree.heading("Estado", text="Estado")
        matriculados_tree.heading("Material", text="Material")
        matriculados_tree.heading("Pagos", text="Pagos")
        matriculados_tree.heading("Acciones", text="Acciones")
        
        matriculados_tree.column("Estudiante", width=150, anchor="center")
        matriculados_tree.column("Curso", width=120, anchor="center")
        matriculados_tree.column("Red", width=100, anchor="center")
        matriculados_tree.column("Fecha Matrícula", width=120, anchor="center")
        matriculados_tree.column("Tipo Material", width=120, anchor="center")
        matriculados_tree.column("Estado", width=100, anchor="center")
        matriculados_tree.column("Material", width=100, anchor="center")
        matriculados_tree.column("Pagos", width=80, anchor="center")
        matriculados_tree.column("Acciones", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=matriculados_tree.yview)
        matriculados_tree.configure(yscrollcommand=scrollbar.set)
        
        matriculados_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Agregar eventos para editar y eliminar matrículas
        matriculados_tree.bind("<Double-1>", lambda e: self.show_edit_matricula_dialog(e, matriculados_tree, aula_name, ciclo_data))
        matriculados_tree.bind("<Button-3>", lambda e: self.show_matricula_context_menu(e, matriculados_tree, aula_name, ciclo_data))
        
        # Cargar matriculados del aula
        self.load_matriculados_del_aula(matriculados_tree, aula_name)
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            dialog,
            text="Cerrar",
            width=100,
            height=35,
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=12)
        )
        close_btn.pack(pady=(0, 20))
    
    def load_matriculados_del_aula(self, tree, aula_name):
        """Cargar matriculados de un aula específica desde la base de datos"""
        try:
            # Importar repositorios necesarios
            from control.inscription_repository import InscriptionRepository
            from control.student_repository import StudentRepository
            from control.classroom_repository import ClassroomRepository
            from control.payment_repository import PaymentRepository
            
            # Crear repositorios
            inscription_repo = InscriptionRepository()
            student_repo = StudentRepository()
            classroom_repo = ClassroomRepository()
            payment_repo = PaymentRepository()
            
            # Obtener ID del aula por nombre
            classroom = classroom_repo.get_row_value({"name": aula_name})
            if not classroom:
                messagebox.showerror("Error", f"No se encontró el aula: {aula_name}")
                return
            
            classroom_id = classroom["id"]
            
            # Obtener todas las inscripciones del aula
            inscriptions = inscription_repo.get_all_rows({"id_classroom": classroom_id})
            
            # Limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            
            if not inscriptions:
                # Mostrar mensaje si no hay inscripciones
                tree.insert("", "end", values=(
                    "No hay estudiantes inscritos",
                    "", "", "", "", "", "", "", ""
                ))
                return
            
            # Procesar cada inscripción
            for inscription in inscriptions:
                try:
                    # Obtener datos del estudiante
                    student = student_repo.get_row_value({"id": inscription["id_student"]})
                    if not student:
                        continue  # Saltar si no se encuentra el estudiante
                    
                    # Obtener datos del curso (usando el aula como curso)
                    course_name = classroom.get("name", "Sin nombre")
                    
                    # Obtener datos de la red (usando el equipo del estudiante)
                    from control.team_repository import TeamRepository
                    team_repo = TeamRepository()
                    team = team_repo.get_row_value({"id": student.get("id_team")})
                    team_name = team.get("name", "Sin equipo") if team else "Sin equipo"
                    
                    # Formatear fecha de inscripción
                    fecha_matricula = inscription.get("date_inscription", "")
                    if fecha_matricula:
                        try:
                            from datetime import datetime
                            fecha_obj = datetime.strptime(fecha_matricula, "%Y-%m-%d")
                            fecha_formateada = fecha_obj.strftime("%d-%m-%Y")
                        except:
                            fecha_formateada = fecha_matricula
                    else:
                        fecha_formateada = "Sin fecha"
                    
                    # Obtener tipo de material
                    tipo_material = inscription.get("type_material", "Sin especificar")
                    
                    # Estado de la inscripción
                    estado = "Activo" if inscription.get("status", False) else "Inactivo"
                    
                    # Estado del material
                    material_estado = "Entregado" if inscription.get("status_material", False) else "Pendiente"
                    
                    # Contar pagos de la inscripción
                    payments = payment_repo.get_all_rows({"id_inscription": inscription["id"]})
                    num_pagos = len(payments) if payments else 0
                    pagos_text = f"{num_pagos}" if num_pagos > 0 else "0"
                    
                    # Nombre completo del estudiante
                    nombre_completo = f"{student.get('name', '')} {student.get('lastname', '')}".strip()
                    
                    # Insertar en la tabla
                    tree.insert("", "end", values=(
                        nombre_completo,
                        course_name,
                        team_name,
                        fecha_formateada,
                        tipo_material,
                        estado,
                        material_estado,
                        pagos_text,
                        "Editar | Eliminar"
                    ))
                    
                except Exception as e:
                    print(f"Error procesando inscripción {inscription.get('id', 'N/A')}: {e}")
                    continue
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar matriculados: {e}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
    
    def show_matricula_context_menu(self, event, tree, aula_name, ciclo_data):
        """Mostrar menú contextual para matrícula"""
        try:
            # Obtener elemento seleccionado
            item = tree.identify_row(event.y)
            if not item:
                return
            
            # Seleccionar el elemento
            tree.selection_set(item)
            values = tree.item(item, "values")
            
            # Verificar que no sea la fila de "No hay estudiantes inscritos"
            if values[0] == "No hay estudiantes inscritos":
                return
            
            # Crear menú contextual
            context_menu = tk.Menu(self.parent, tearoff=0)
            
            # Editar matrícula
            context_menu.add_command(
                label="Editar Matrícula",
                command=lambda: self.show_edit_matricula_dialog(event, tree, aula_name, ciclo_data)
            )
            
            # Eliminar matrícula
            context_menu.add_command(
                label="Eliminar Matrícula",
                command=lambda: self.delete_matricula_from_context(values, tree, aula_name, ciclo_data)
            )
            
            # Ver pagos
            context_menu.add_command(
                label="Ver Pagos",
                command=lambda: self.show_pagos_matricula(values, tree, aula_name, ciclo_data)
            )
            
            # Mostrar menú
            context_menu.tk_popup(event.x_root, event.y_root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en menú contextual: {e}")
    
    def show_edit_matricula_dialog(self, event, tree, aula_name, ciclo_data):
        """Mostrar diálogo para editar matrícula"""
        try:
            # Obtener elemento seleccionado
            item = tree.selection()[0] if tree.selection() else None
            if not item:
                messagebox.showwarning("Advertencia", "Por favor seleccione una matrícula para editar")
                return
            
            # Obtener datos de la matrícula
            values = tree.item(item, "values")
            estudiante_name = values[0]  # Columna "Estudiante"
            
            # Obtener la matrícula completa de la base de datos
            from control.inscription_repository import InscriptionRepository
            from control.student_repository import StudentRepository
            from control.classroom_repository import ClassroomRepository
            
            inscription_repo = InscriptionRepository()
            student_repo = StudentRepository()
            classroom_repo = ClassroomRepository()
            
            # Buscar el estudiante por nombre
            students = student_repo.get_all_rows()
            student_data = None
            for student in students:
                full_name = f"{student.get('name', '')} {student.get('lastname', '')}".strip()
                if full_name == estudiante_name:
                    student_data = student
                    break
            
            if not student_data:
                messagebox.showerror("Error", "No se pudo encontrar los datos del estudiante.")
                return
            
            # Buscar la inscripción del estudiante en esta aula
            classroom = classroom_repo.get_row_value({"name": aula_name})
            if not classroom:
                messagebox.showerror("Error", "No se pudo encontrar el aula.")
                return
            
            inscriptions = inscription_repo.get_all_rows({
                "id_student": student_data["id"],
                "id_classroom": classroom["id"]
            })
            
            if not inscriptions:
                messagebox.showerror("Error", "No se encontró la matrícula.")
                return
            
            # Usar la primera inscripción encontrada
            inscription_data = inscriptions[0]
            
            # Crear diálogo de edición
            dialog = ctk.CTkToplevel(self.parent)
            dialog.title(f"Editar Matrícula - {estudiante_name}")
            dialog.geometry("600x700")
            dialog.resizable(False, False)
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
            y = (dialog.winfo_screenheight() // 2) - (700 // 2)
            dialog.geometry(f"600x700+{x}+{y}")
            
            # Hacer modal
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Título
            title = ctk.CTkLabel(
                dialog,
                text=f"EDITAR MATRÍCULA - {estudiante_name}",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#1f538d"
            )
            title.pack(pady=20)
            
            # Frame principal
            main_frame = ctk.CTkScrollableFrame(dialog, width=550, height=500)
            main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            # Variables para los campos
            year_var = ctk.StringVar(value=str(inscription_data.get('year', 2024)))
            cycle_var = ctk.StringVar(value=inscription_data.get('cycle', 'Primer Ciclo'))
            material_type = ctk.StringVar(value=inscription_data.get('type_material', 'Libro de Texto'))
            status_var = ctk.BooleanVar(value=bool(inscription_data.get('status', True)))
            material_status_var = ctk.BooleanVar(value=bool(inscription_data.get('status_material', True)))
            
            # Campo: Año
            ctk.CTkLabel(main_frame, text="Año:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            year_entry = ctk.CTkEntry(
                main_frame,
                textvariable=year_var,
                width=500,
                height=35
            )
            year_entry.pack(fill="x", pady=(0, 10))
            
            # Campo: Ciclo
            ctk.CTkLabel(main_frame, text="Ciclo:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            cycle_entry = ctk.CTkEntry(
                main_frame,
                textvariable=cycle_var,
                width=500,
                height=35
            )
            cycle_entry.pack(fill="x", pady=(0, 10))
            
            # Campo: Tipo de Material
            ctk.CTkLabel(main_frame, text="Tipo de Material:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            material_combo = ctk.CTkComboBox(
                main_frame,
                variable=material_type,
                values=["Libro de Texto", "Material Digital", "Físico", "Digital"],
                width=500,
                height=35
            )
            material_combo.pack(fill="x", pady=(0, 10))
            
            # Campo: Estado de la Matrícula
            status_checkbox = ctk.CTkCheckBox(
                main_frame,
                text="Matrícula Activa",
                variable=status_var,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            status_checkbox.pack(anchor="w", pady=(10, 5))
            
            # Campo: Estado del Material
            material_checkbox = ctk.CTkCheckBox(
                main_frame,
                text="Material Entregado",
                variable=material_status_var,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            material_checkbox.pack(anchor="w", pady=(10, 20))
            
            # Función para actualizar matrícula
            def update_matricula():
                try:
                    # Validar campos
                    if not year_var.get() or not cycle_var.get():
                        messagebox.showerror("Error", "Complete todos los campos obligatorios")
                        return
                    
                    # Preparar datos actualizados
                    updated_data = {
                        "year": int(year_var.get()),
                        "cycle": cycle_var.get(),
                        "type_material": material_type.get(),
                        "status": status_var.get(),
                        "status_material": material_status_var.get()
                    }
                    
                    # Actualizar en la base de datos
                    result = inscription_repo.update_row(updated_data, {"id": inscription_data["id"]})
                    
                    if result > 0:
                        messagebox.showinfo("Éxito", f"Matrícula de {estudiante_name} actualizada correctamente")
                        dialog.destroy()
                        # Recargar la tabla de matriculados
                        self.load_matriculados_del_aula(tree, aula_name)
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar la matrícula")
                        
                except ValueError as e:
                    messagebox.showerror("Error", f"Error en los datos ingresados: {e}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error inesperado: {e}")
            
            # Botones
            buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            update_btn = ctk.CTkButton(
                buttons_frame,
                text="ACTUALIZAR MATRÍCULA",
                width=200,
                height=50,
                command=update_matricula,
                fg_color="#28a745",
                hover_color="#218838",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            update_btn.pack(side="left", padx=(0, 20))
            
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="CANCELAR",
                width=200,
                height=50,
                command=dialog.destroy,
                fg_color="#dc3545",
                hover_color="#c82333",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            cancel_btn.pack(side="left")
            
            # Enfocar en el primer campo
            year_entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir diálogo de edición: {e}")
            import traceback
            traceback.print_exc()
    
    def delete_matricula_from_context(self, values, tree, aula_name, ciclo_data):
        """Eliminar matrícula desde el menú contextual"""
        try:
            estudiante_name = values[0]  # Columna "Estudiante"
            
            # Obtener datos de la matrícula
            from control.inscription_repository import InscriptionRepository
            from control.student_repository import StudentRepository
            from control.classroom_repository import ClassroomRepository
            
            inscription_repo = InscriptionRepository()
            student_repo = StudentRepository()
            classroom_repo = ClassroomRepository()
            
            # Buscar el estudiante por nombre
            students = student_repo.get_all_rows()
            student_data = None
            for student in students:
                full_name = f"{student.get('name', '')} {student.get('lastname', '')}".strip()
                if full_name == estudiante_name:
                    student_data = student
                    break
            
            if not student_data:
                messagebox.showerror("Error", "No se pudo encontrar los datos del estudiante.")
                return
            
            # Buscar la inscripción del estudiante en esta aula
            classroom = classroom_repo.get_row_value({"name": aula_name})
            if not classroom:
                messagebox.showerror("Error", "No se pudo encontrar el aula.")
                return
            
            inscriptions = inscription_repo.get_all_rows({
                "id_student": student_data["id"],
                "id_classroom": classroom["id"]
            })
            
            if not inscriptions:
                messagebox.showerror("Error", "No se encontró la matrícula.")
                return
            
            # Usar la primera inscripción encontrada
            inscription_data = inscriptions[0]
            
            # Mostrar confirmación
            result = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar la matrícula de '{estudiante_name}'?\n\n"
                f"ADVERTENCIA: Esta acción eliminará:\n"
                f"• La inscripción del estudiante\n"
                f"• Todos los pagos relacionados\n\n"
                f"Esta acción NO se puede deshacer."
            )
            
            if result:
                # Usar eliminación en cascada
                success = inscription_repo.delete_inscription_cascade(inscription_data["id"])
                
                if success:
                    messagebox.showinfo("Éxito", f"Matrícula de '{estudiante_name}' eliminada correctamente")
                    # Recargar matriculados
                    self.load_matriculados_del_aula(tree, aula_name)
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la matrícula")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar matrícula: {e}")
            import traceback
            traceback.print_exc()
    
    def show_pagos_matricula(self, values, tree, aula_name, ciclo_data):
        """Mostrar los pagos de una matrícula específica"""
        try:
            estudiante_name = values[0]  # Columna "Estudiante"
            
            # Obtener datos de la matrícula
            from control.inscription_repository import InscriptionRepository
            from control.student_repository import StudentRepository
            from control.classroom_repository import ClassroomRepository
            from control.payment_repository import PaymentRepository
            
            inscription_repo = InscriptionRepository()
            student_repo = StudentRepository()
            classroom_repo = ClassroomRepository()
            payment_repo = PaymentRepository()
            
            # Buscar el estudiante por nombre
            students = student_repo.get_all_rows()
            student_data = None
            for student in students:
                full_name = f"{student.get('name', '')} {student.get('lastname', '')}".strip()
                if full_name == estudiante_name:
                    student_data = student
                    break
            
            if not student_data:
                messagebox.showerror("Error", "No se pudo encontrar los datos del estudiante.")
                return
            
            # Buscar la inscripción del estudiante en esta aula
            classroom = classroom_repo.get_row_value({"name": aula_name})
            if not classroom:
                messagebox.showerror("Error", "No se pudo encontrar el aula.")
                return
            
            inscriptions = inscription_repo.get_all_rows({
                "id_student": student_data["id"],
                "id_classroom": classroom["id"]
            })
            
            if not inscriptions:
                messagebox.showerror("Error", "No se encontró la matrícula.")
                return
            
            # Usar la primera inscripción encontrada
            inscription_data = inscriptions[0]
            
            # Obtener pagos de la inscripción
            payments = payment_repo.get_all_rows({"id_inscription": inscription_data["id"]})
            
            # Crear ventana de pagos
            dialog = ctk.CTkToplevel(self.parent)
            dialog.title(f"Pagos - {estudiante_name}")
            dialog.geometry("800x600")
            dialog.resizable(True, True)
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
            y = (dialog.winfo_screenheight() // 2) - (600 // 2)
            dialog.geometry(f"800x600+{x}+{y}")
            
            # Hacer modal
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Título
            title = ctk.CTkLabel(
                dialog,
                text=f"PAGOS - {estudiante_name}",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#1f538d"
            )
            title.pack(pady=20)
            
            # Información de la matrícula
            info_frame = ctk.CTkFrame(dialog, fg_color="#e8f5e8", corner_radius=8)
            info_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            info_text = f"Aula: {aula_name} | Ciclo: {inscription_data.get('cycle', 'N/A')} {inscription_data.get('year', 'N/A')}"
            info_label = ctk.CTkLabel(
                info_frame,
                text=info_text,
                font=ctk.CTkFont(size=12),
                text_color="#2e7d32"
            )
            info_label.pack(pady=10)
            
            # Tabla de pagos
            table_frame = ctk.CTkFrame(dialog)
            table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            columns = ("ID", "Método", "Monto", "Fecha", "Acciones")
            payments_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
            
            payments_tree.heading("ID", text="ID")
            payments_tree.heading("Método", text="Método de Pago")
            payments_tree.heading("Monto", text="Monto")
            payments_tree.heading("Fecha", text="Fecha")
            payments_tree.heading("Acciones", text="Acciones")
            
            payments_tree.column("ID", width=80, anchor="center")
            payments_tree.column("Método", width=150, anchor="center")
            payments_tree.column("Monto", width=100, anchor="center")
            payments_tree.column("Fecha", width=150, anchor="center")
            payments_tree.column("Acciones", width=100, anchor="center")
            
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=payments_tree.yview)
            payments_tree.configure(yscrollcommand=scrollbar.set)
            
            payments_tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Cargar pagos
            total_paid = 0
            if payments:
                for payment in payments:
                    # Formatear fecha
                    fecha = payment.get("created_datetime", "")
                    if fecha:
                        try:
                            from datetime import datetime
                            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
                            fecha_formateada = fecha_obj.strftime("%d-%m-%Y %H:%M")
                        except:
                            fecha_formateada = fecha
                    else:
                        fecha_formateada = "Sin fecha"
                    
                    # Formatear monto
                    monto = payment.get("amount", 0)
                    total_paid += monto
                    
                    payments_tree.insert("", "end", values=(
                        payment.get("id", ""),
                        payment.get("method_payment", ""),
                        f"${monto}",
                        fecha_formateada,
                        "Editar | Eliminar"
                    ))
            else:
                payments_tree.insert("", "end", values=(
                    "No hay pagos registrados",
                    "", "", "", ""
                ))
            
            # Resumen de pagos
            summary_frame = ctk.CTkFrame(dialog, fg_color="#fff3cd", corner_radius=8)
            summary_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            summary_text = f"Total de Pagos: {len(payments) if payments else 0} | Total Pagado: ${total_paid}"
            summary_label = ctk.CTkLabel(
                summary_frame,
                text=summary_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#856404"
            )
            summary_label.pack(pady=10)
            
            # Botón cerrar
            close_btn = ctk.CTkButton(
                dialog,
                text="Cerrar",
                width=100,
                height=35,
                command=dialog.destroy,
                fg_color="#6c757d",
                hover_color="#5a6268",
                font=ctk.CTkFont(size=12)
            )
            close_btn.pack(pady=(0, 20))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar pagos: {e}")
            import traceback
            traceback.print_exc()
    
    def show_add_matricula_dialog(self, aula_name, ciclo_data):
        """Mostrar diálogo para agregar nueva matrícula"""
        try:
            # Crear diálogo
            dialog = ctk.CTkToplevel(self.parent)
            dialog.title(f"Agregar Matrícula - {aula_name}")
            dialog.geometry("600x700")
            dialog.resizable(False, False)
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
            y = (dialog.winfo_screenheight() // 2) - (700 // 2)
            dialog.geometry(f"600x700+{x}+{y}")
            
            # Hacer modal
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Título
            title = ctk.CTkLabel(
                dialog,
                text=f"NUEVA MATRÍCULA - {aula_name}",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#1f538d"
            )
            title.pack(pady=20)
            
            # Frame principal
            main_frame = ctk.CTkScrollableFrame(dialog, width=550, height=500)
            main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            # Importar repositorios
            from control.student_repository import StudentRepository
            from control.classroom_repository import ClassroomRepository
            from control.team_repository import TeamRepository
            from control.utils.inscription_flow import InscriptionFlowManager
            
            student_repo = StudentRepository()
            classroom_repo = ClassroomRepository()
            team_repo = TeamRepository()
            flow_manager = InscriptionFlowManager()
            
            # Obtener datos necesarios
            students = student_repo.get_all_rows()
            teams = team_repo.get_all_rows()
            classroom = classroom_repo.get_row_value({"name": aula_name})
            
            if not classroom:
                messagebox.showerror("Error", f"No se encontró el aula: {aula_name}")
                dialog.destroy()
                return
            
            # Variables para los campos
            selected_student = ctk.StringVar()
            selected_team = ctk.StringVar()
            year_var = ctk.StringVar(value=str(ciclo_data.get('date_start', '2024')[:4]))
            cycle_var = ctk.StringVar(value=ciclo_data.get('cicle', 'Primer Ciclo'))
            material_type = ctk.StringVar(value="Libro de Texto")
            payment_method = ctk.StringVar(value="Efectivo")
            amount_var = ctk.StringVar(value="150")
            
            # Contador de matrículas creadas
            matriculas_creadas = 0
            
            # Campo: Estudiante
            ctk.CTkLabel(main_frame, text="Estudiante:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            student_combo = ctk.CTkComboBox(
                main_frame,
                variable=selected_student,
                values=[f"{s['name']} {s['lastname']}" for s in students],
                width=500,
                height=35
            )
            student_combo.pack(fill="x", pady=(0, 10))
            
            # Campo: Red/Equipo
            ctk.CTkLabel(main_frame, text="Red/Equipo:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            team_combo = ctk.CTkComboBox(
                main_frame,
                variable=selected_team,
                values=[t['name'] for t in teams],
                width=500,
                height=35
            )
            team_combo.pack(fill="x", pady=(0, 10))
            
            # Campo: Año
            ctk.CTkLabel(main_frame, text="Año:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            year_entry = ctk.CTkEntry(
                main_frame,
                textvariable=year_var,
                width=500,
                height=35
            )
            year_entry.pack(fill="x", pady=(0, 10))
            
            # Campo: Ciclo
            ctk.CTkLabel(main_frame, text="Ciclo:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            cycle_entry = ctk.CTkEntry(
                main_frame,
                textvariable=cycle_var,
                width=500,
                height=35
            )
            cycle_entry.pack(fill="x", pady=(0, 10))
            
            # Campo: Tipo de Material
            ctk.CTkLabel(main_frame, text="Tipo de Material:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            material_combo = ctk.CTkComboBox(
                main_frame,
                variable=material_type,
                values=["Libro de Texto", "Material Digital", "Físico", "Digital"],
                width=500,
                height=35
            )
            material_combo.pack(fill="x", pady=(0, 10))
            
            # Campo: Método de Pago
            ctk.CTkLabel(main_frame, text="Método de Pago:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            payment_combo = ctk.CTkComboBox(
                main_frame,
                variable=payment_method,
                values=["Efectivo", "Transferencia", "Tarjeta", "Yape", "Plin"],
                width=500,
                height=35
            )
            payment_combo.pack(fill="x", pady=(0, 10))
            
            # Campo: Monto
            ctk.CTkLabel(main_frame, text="Monto:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
            amount_entry = ctk.CTkEntry(
                main_frame,
                textvariable=amount_var,
                width=500,
                height=35
            )
            amount_entry.pack(fill="x", pady=(0, 20))
            
            # Contador de matrículas
            counter_frame = ctk.CTkFrame(main_frame, fg_color="#e8f5e8", corner_radius=8)
            counter_frame.pack(fill="x", pady=(0, 10))
            
            counter_label = ctk.CTkLabel(
                counter_frame,
                text="Matrículas creadas en esta sesión: 0",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#2e7d32"
            )
            counter_label.pack(pady=10)
            
            # Función para crear matrícula
            def create_matricula():
                try:
                    # Validar campos
                    if not selected_student.get():
                        messagebox.showerror("Error", "Seleccione un estudiante")
                        return
                    
                    if not selected_team.get():
                        messagebox.showerror("Error", "Seleccione una red/equipo")
                        return
                    
                    # Obtener ID del estudiante seleccionado
                    student_name = selected_student.get()
                    student_data = next((s for s in students if f"{s['name']} {s['lastname']}" == student_name), None)
                    if not student_data:
                        messagebox.showerror("Error", "No se encontró el estudiante seleccionado")
                        return
                    
                    student_id = student_data["id"]
                    classroom_id = classroom["id"]
                    year = int(year_var.get())
                    cycle = cycle_var.get()
                    material = material_type.get()
                    payment_method_val = payment_method.get()
                    amount = int(amount_var.get())
                    
                    # Crear matrícula usando el flujo completo
                    result = flow_manager.create_complete_inscription(
                        student_id=student_id,
                        classroom_id=classroom_id,
                        year=year,
                        cycle=cycle,
                        type_material=material,
                        payment_method=payment_method_val,
                        amount=amount
                    )
                    
                    if result["success"]:
                        # Mostrar mensaje de éxito más detallado
                        success_message = f"""¡MATRÍCULA CREADA EXITOSAMENTE!

ID Inscripción: {result['inscription_id']}
ID Pago: {result['payment_id']}
Estudiante: {result.get('student_name', 'N/A')}
Aula: {result.get('classroom_name', 'N/A')}

La matrícula se ha registrado correctamente en la base de datos.
El pago se ha procesado exitosamente.
Puedes agregar más matrículas usando este formulario."""
                        
                        messagebox.showinfo("¡ÉXITO!", success_message)
                        
                        # Limpiar formulario para nueva matrícula
                        student_combo.set("")
                        team_combo.set("")
                        year_var.set(str(ciclo_data.get('date_start', '2024')[:4]))
                        cycle_var.set(ciclo_data.get('cicle', 'Primer Ciclo'))
                        material_type.set("Libro de Texto")
                        payment_method.set("Efectivo")
                        amount_var.set("150")
                        
                        # Enfocar en el primer campo para nueva matrícula
                        student_combo.focus()
                        
                        # Incrementar contador y actualizar display
                        matriculas_creadas += 1
                        counter_label.configure(text=f"Matrículas creadas en esta sesión: {matriculas_creadas}")
                        
                        # Cambiar temporalmente el color del botón para indicar éxito
                        create_btn.configure(fg_color="#155724", text="¡AGREGADA!")
                        dialog.after(2000, lambda: create_btn.configure(fg_color="#28a745", text="CREAR MATRÍCULA"))
                        
                    else:
                        messagebox.showerror("Error", f"Error al crear matrícula:\n{result['error']}")
                        
                except ValueError as e:
                    messagebox.showerror("Error", f"Error en los datos ingresados: {e}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error inesperado: {e}")
            
            # Botones
            buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            create_btn = ctk.CTkButton(
                buttons_frame,
                text="CREAR MATRÍCULA",
                width=180,
                height=50,
                command=create_matricula,
                fg_color="#28a745",
                hover_color="#218838",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            create_btn.pack(side="left", padx=(0, 15))
            
            clear_btn = ctk.CTkButton(
                buttons_frame,
                text="LIMPIAR",
                width=150,
                height=50,
                command=lambda: [
                    student_combo.set(""),
                    team_combo.set(""),
                    year_var.set(str(ciclo_data.get('date_start', '2024')[:4])),
                    cycle_var.set(ciclo_data.get('cicle', 'Primer Ciclo')),
                    material_type.set("Libro de Texto"),
                    payment_method.set("Efectivo"),
                    amount_var.set("150"),
                    student_combo.focus()
                ],
                fg_color="#ffc107",
                hover_color="#e0a800",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            clear_btn.pack(side="left", padx=(0, 15))
            
            close_btn = ctk.CTkButton(
                buttons_frame,
                text="CERRAR",
                width=150,
                height=50,
                command=dialog.destroy,
                fg_color="#dc3545",
                hover_color="#c82333",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            close_btn.pack(side="left")
            
            # Enfocar en el primer campo
            student_combo.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir diálogo de matrícula: {e}")
            import traceback
            traceback.print_exc()
    
    def show_add_aula_dialog(self, ciclo_id, tree=None):
        """Mostrar diálogo para agregar aula a un ciclo"""
        try:
            # Crear diálogo
            dialog = ctk.CTkToplevel(self.parent)
            dialog.title("Agregar Aula")
            dialog.geometry("600x700")
            dialog.resizable(False, False)
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
            y = (dialog.winfo_screenheight() // 2) - (700 // 2)
            dialog.geometry(f"600x700+{x}+{y}")
            
            # Hacer modal
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Título
            title = ctk.CTkLabel(
                dialog,
                text="AGREGAR AULA",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#1f538d"
            )
            title.pack(pady=20)
            
            # Frame para campos
            fields_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            fields_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            # Nombre del Aula
            name_label = ctk.CTkLabel(fields_frame, text="Nombre del Aula:", font=ctk.CTkFont(size=14))
            name_label.pack(pady=(0, 5), anchor="w")
            
            name_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="Ingrese nombre del aula",
                width=550,
                height=35
            )
            name_entry.pack(pady=(0, 15))
            
            # Fecha Inicio
            start_date_label = ctk.CTkLabel(fields_frame, text="Fecha Inicio:", font=ctk.CTkFont(size=14))
            start_date_label.pack(pady=(0, 5), anchor="w")
            
            start_date_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="YYYY-MM-DD",
                width=550,
                height=35
            )
            start_date_entry.pack(pady=(0, 15))
            
            # Fecha Fin
            end_date_label = ctk.CTkLabel(fields_frame, text="Fecha Fin:", font=ctk.CTkFont(size=14))
            end_date_label.pack(pady=(0, 5), anchor="w")
            
            end_date_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="YYYY-MM-DD",
                width=550,
                height=35
            )
            end_date_entry.pack(pady=(0, 15))
            
            # Docente
            teacher_label = ctk.CTkLabel(fields_frame, text="Docente:", font=ctk.CTkFont(size=14))
            teacher_label.pack(pady=(0, 5), anchor="w")
            
            # Obtener docentes disponibles
            teachers = self.teacher_repo.get_all_rows()
            teacher_names = [f"{t.get('name', '')} {t.get('lastname', '')}" for t in teachers]
            
            teacher_combo = ctk.CTkComboBox(
                fields_frame,
                values=teacher_names,
                width=550,
                height=35
            )
            teacher_combo.pack(pady=(0, 15))
            
            # Curso
            course_label = ctk.CTkLabel(fields_frame, text="Curso:", font=ctk.CTkFont(size=14))
            course_label.pack(pady=(0, 5), anchor="w")
            
            # Obtener cursos disponibles
            courses = self.course_repo.get_all_rows()
            course_names = [c.get('name', '') for c in courses]
            
            course_combo = ctk.CTkComboBox(
                fields_frame,
                values=course_names,
                width=550,
                height=35
            )
            course_combo.pack(pady=(0, 15))
            
            # Frame para botones
            buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(20, 30), padx=20)
            
            def add_aula():
                name = name_entry.get().strip()
                start_date = start_date_entry.get().strip()
                end_date = end_date_entry.get().strip()
                teacher_name = teacher_combo.get()
                course_name = course_combo.get()
                
                if not name or not start_date or not end_date or not teacher_name or not course_name:
                    messagebox.showerror("Error", "Por favor complete todos los campos")
                    return
                
                try:
                    # Buscar ID del docente
                    teacher_id = None
                    for teacher in teachers:
                        full_name = f"{teacher.get('name', '')} {teacher.get('lastname', '')}"
                        if full_name == teacher_name:
                            teacher_id = teacher.get('id')
                            break
                    
                    # Buscar ID del curso
                    course_id = None
                    for course in courses:
                        if course.get('name') == course_name:
                            course_id = course.get('id')
                            break
                    
                    if not teacher_id or not course_id:
                        messagebox.showerror("Error", "No se pudo encontrar el docente o curso seleccionado")
                        return
                    
                    # Crear aula
                    aula_data = {
                        "name": name,
                        "start_date": start_date,
                        "end_date": end_date,
                        "id_teacher": teacher_id,
                        "id_course": course_id,
                        "id_cicle": ciclo_id
                    }
                    
                    # Insertar aula
                    self.classroom_repo.insert_row(aula_data)
                    
                    # Si llegamos aquí, la inserción fue exitosa (no se lanzó excepción)
                    messagebox.showinfo("Éxito", "Aula agregada correctamente")
                    dialog.destroy()
                    
                    # Recargar aulas si se proporciona el tree
                    if tree:
                        self.load_aulas_del_ciclo(tree, ciclo_id)
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Error al agregar aula: {e}")
            
            def cancel():
                dialog.destroy()
            
            # Botones
            add_btn = ctk.CTkButton(
                buttons_frame,
                text="AGREGAR AULA",
                width=200,
                height=50,
                command=add_aula,
                fg_color="#28a745",
                hover_color="#218838",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            add_btn.pack(side="left", padx=(0, 20))
            
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="CANCELAR",
                width=200,
                height=50,
                command=cancel,
                fg_color="#dc3545",
                hover_color="#c82333",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            cancel_btn.pack(side="left")
            
            # Enfocar en el primer campo
            name_entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir diálogo de agregar aula: {e}")
    
    def show_matricula_from_aulas(self, ciclo_data):
        """Mostrar diálogo de matrícula desde la vista de aulas"""
        try:
            # Verificar si hay aulas en el ciclo
            aulas = self.classroom_repo.get_all_rows()
            aulas_ciclo = [aula for aula in aulas if aula.get("id_cicle") == ciclo_data.get('id')]
            
            if not aulas_ciclo:
                messagebox.showwarning(
                    "Advertencia", 
                    "No hay aulas creadas en este ciclo.\n\n"
                    "Primero debe crear al menos un aula para poder agregar matrículas."
                )
                return
            
            # Mostrar diálogo de selección de aula para matrícula
            self.show_select_aula_for_matricula_dialog(ciclo_data, aulas_ciclo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir matrícula: {e}")
    
    def show_select_aula_for_matricula_dialog(self, ciclo_data, aulas_ciclo):
        """Mostrar diálogo para seleccionar aula y agregar matrícula"""
        try:
            # Crear diálogo
            dialog = ctk.CTkToplevel(self.parent)
            dialog.title("Seleccionar Aula para Matrícula")
            dialog.geometry("500x400")
            dialog.resizable(False, False)
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
            y = (dialog.winfo_screenheight() // 2) - (400 // 2)
            dialog.geometry(f"500x400+{x}+{y}")
            
            # Hacer modal
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Título
            title = ctk.CTkLabel(
                dialog,
                text="AGREGAR MATRÍCULA",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#1f538d"
            )
            title.pack(pady=20)
            
            # Información del ciclo
            ciclo_info = ctk.CTkLabel(
                dialog,
                text=f"Ciclo: {ciclo_data.get('cicle', '')} - {ciclo_data.get('year', '')}",
                font=ctk.CTkFont(size=14),
                text_color="#1565c0"
            )
            ciclo_info.pack(pady=(0, 20))
            
            # Frame para selección
            selection_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            selection_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            # Label para seleccionar aula
            aula_label = ctk.CTkLabel(selection_frame, text="Seleccionar Aula:", font=ctk.CTkFont(size=14))
            aula_label.pack(pady=(0, 10), anchor="w")
            
            # Crear lista de aulas
            aulas_list = []
            for aula in aulas_ciclo:
                # Obtener nombre del curso
                cursos = self.course_repo.get_all_rows()
                curso_nombre = "Curso no encontrado"
                for curso in cursos:
                    if curso.get("id") == aula.get("id_course"):
                        curso_nombre = curso.get("name", "")
                        break
                
                aulas_list.append(f"{aula.get('name', '')} - {curso_nombre}")
            
            # ComboBox para seleccionar aula
            aula_combo = ctk.CTkComboBox(
                selection_frame,
                values=aulas_list,
                width=450,
                height=35
            )
            aula_combo.pack(pady=(0, 20))
            
            # Frame para botones
            buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(20, 30), padx=20)
            
            def agregar_matricula():
                aula_seleccionada = aula_combo.get()
                if not aula_seleccionada:
                    messagebox.showerror("Error", "Por favor seleccione un aula")
                    return
                
                # Obtener el aula seleccionada
                aula_nombre = aula_seleccionada.split(" - ")[0]
                aula_data = next((a for a in aulas_ciclo if a.get("name") == aula_nombre), None)
                
                if aula_data:
                    dialog.destroy()
                    # Mostrar diálogo de matrícula para el aula seleccionada
                    self.show_add_matricula_dialog(aula_nombre, ciclo_data)
                else:
                    messagebox.showerror("Error", "No se pudo encontrar el aula seleccionada")
            
            def cancelar():
                dialog.destroy()
            
            # Botones
            agregar_btn = ctk.CTkButton(
                buttons_frame,
                text="AGREGAR MATRÍCULA",
                width=200,
                height=50,
                command=agregar_matricula,
                fg_color="#6f42c1",
                hover_color="#5a32a3",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            agregar_btn.pack(side="left", padx=(0, 20))
            
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="CANCELAR",
                width=200,
                height=50,
                command=cancelar,
                fg_color="#dc3545",
                hover_color="#c82333",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            cancel_btn.pack(side="left")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir selección de aula: {e}")
    
    def show_aula_context_menu(self, event, tree, ciclo_data):
        """Mostrar menú contextual para aula"""
        try:
            # Obtener elemento seleccionado
            item = tree.identify_row(event.y)
            if not item:
                return
            
            # Seleccionar el elemento
            tree.selection_set(item)
            values = tree.item(item, "values")
            
            # Crear menú contextual
            context_menu = tk.Menu(self.parent, tearoff=0)
            
            # Editar aula
            context_menu.add_command(
                label="Editar Aula",
                command=lambda: self.show_edit_aula_dialog(event, tree, ciclo_data)
            )
            
            # Eliminar aula
            context_menu.add_command(
                label="Eliminar Aula",
                command=lambda: self.delete_aula_from_context(values, tree, ciclo_data)
            )
            
            # Mostrar menú
            context_menu.tk_popup(event.x_root, event.y_root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en menú contextual: {e}")
    
    def show_edit_aula_dialog(self, event, tree, ciclo_data):
        """Mostrar diálogo para editar aula"""
        try:
            # Obtener elemento seleccionado
            item = tree.selection()[0] if tree.selection() else None
            if not item:
                messagebox.showwarning("Advertencia", "Por favor seleccione un aula para editar")
                return
            
            # Obtener datos del aula
            values = tree.item(item, "values")
            aula_name = values[1]  # Columna "Aula"
            
            # Obtener el aula completo de la base de datos
            aulas = self.classroom_repo.get_all_rows()
            aula_data = next((a for a in aulas if a.get("name") == aula_name), None)
            
            if not aula_data:
                messagebox.showerror("Error", "No se pudo encontrar los datos del aula.")
                return
            
            # Crear diálogo de edición (similar al de agregar)
            dialog = ctk.CTkToplevel(self.parent)
            dialog.title("Editar Aula")
            dialog.geometry("600x700")
            dialog.resizable(False, False)
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
            y = (dialog.winfo_screenheight() // 2) - (700 // 2)
            dialog.geometry(f"600x700+{x}+{y}")
            
            # Hacer modal
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Título
            title = ctk.CTkLabel(
                dialog,
                text="EDITAR AULA",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#1f538d"
            )
            title.pack(pady=20)
            
            # Frame para campos
            fields_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            fields_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            # Nombre del Aula
            name_label = ctk.CTkLabel(fields_frame, text="Nombre del Aula:", font=ctk.CTkFont(size=14))
            name_label.pack(pady=(0, 5), anchor="w")
            
            name_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="Ingrese nombre del aula",
                width=550,
                height=35
            )
            name_entry.insert(0, aula_data.get("name", ""))
            name_entry.pack(pady=(0, 15))
            
            # Fecha Inicio
            start_date_label = ctk.CTkLabel(fields_frame, text="Fecha Inicio:", font=ctk.CTkFont(size=14))
            start_date_label.pack(pady=(0, 5), anchor="w")
            
            start_date_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="YYYY-MM-DD",
                width=550,
                height=35
            )
            start_date_entry.insert(0, str(aula_data.get("start_date", "")))
            start_date_entry.pack(pady=(0, 15))
            
            # Fecha Fin
            end_date_label = ctk.CTkLabel(fields_frame, text="Fecha Fin:", font=ctk.CTkFont(size=14))
            end_date_label.pack(pady=(0, 5), anchor="w")
            
            end_date_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="YYYY-MM-DD",
                width=550,
                height=35
            )
            end_date_entry.insert(0, str(aula_data.get("end_date", "")))
            end_date_entry.pack(pady=(0, 15))
            
            # Docente
            teacher_label = ctk.CTkLabel(fields_frame, text="Docente:", font=ctk.CTkFont(size=14))
            teacher_label.pack(pady=(0, 5), anchor="w")
            
            # Obtener docentes disponibles
            teachers = self.teacher_repo.get_all_rows()
            teacher_names = [f"{t.get('name', '')} {t.get('lastname', '')}" for t in teachers]
            
            teacher_combo = ctk.CTkComboBox(
                fields_frame,
                values=teacher_names,
                width=550,
                height=35
            )
            # Seleccionar el docente actual
            current_teacher = next((t for t in teachers if t.get('id') == aula_data.get('id_teacher')), None)
            if current_teacher:
                current_teacher_name = f"{current_teacher.get('name', '')} {current_teacher.get('lastname', '')}"
                teacher_combo.set(current_teacher_name)
            teacher_combo.pack(pady=(0, 15))
            
            # Curso
            course_label = ctk.CTkLabel(fields_frame, text="Curso:", font=ctk.CTkFont(size=14))
            course_label.pack(pady=(0, 5), anchor="w")
            
            # Obtener cursos disponibles
            courses = self.course_repo.get_all_rows()
            course_names = [c.get('name', '') for c in courses]
            
            course_combo = ctk.CTkComboBox(
                fields_frame,
                values=course_names,
                width=550,
                height=35
            )
            # Seleccionar el curso actual
            current_course = next((c for c in courses if c.get('id') == aula_data.get('id_course')), None)
            if current_course:
                course_combo.set(current_course.get('name', ''))
            course_combo.pack(pady=(0, 15))
            
            # Frame para botones
            buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(20, 30), padx=20)
            
            def update_aula():
                name = name_entry.get().strip()
                start_date = start_date_entry.get().strip()
                end_date = end_date_entry.get().strip()
                teacher_name = teacher_combo.get()
                course_name = course_combo.get()
                
                if not name or not start_date or not end_date or not teacher_name or not course_name:
                    messagebox.showerror("Error", "Por favor complete todos los campos")
                    return
                
                try:
                    # Buscar ID del docente
                    teacher_id = None
                    for teacher in teachers:
                        full_name = f"{teacher.get('name', '')} {teacher.get('lastname', '')}"
                        if full_name == teacher_name:
                            teacher_id = teacher.get('id')
                            break
                    
                    # Buscar ID del curso
                    course_id = None
                    for course in courses:
                        if course.get('name') == course_name:
                            course_id = course.get('id')
                            break
                    
                    if not teacher_id or not course_id:
                        messagebox.showerror("Error", "No se pudo encontrar el docente o curso seleccionado")
                        return
                    
                    # Actualizar aula
                    update_data = {
                        "name": name,
                        "start_date": start_date,
                        "end_date": end_date,
                        "id_teacher": teacher_id,
                        "id_course": course_id
                    }
                    
                    result = self.classroom_repo.update_row(update_data, {"id": aula_data.get("id")})
                    
                    if result > 0:
                        messagebox.showinfo("Éxito", "Aula actualizada correctamente")
                        dialog.destroy()
                        # Recargar aulas
                        self.load_aulas_del_ciclo(tree, ciclo_data.get('id'))
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el aula")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar aula: {e}")
            
            def cancel():
                dialog.destroy()
            
            # Botones
            update_btn = ctk.CTkButton(
                buttons_frame,
                text="ACTUALIZAR AULA",
                width=200,
                height=50,
                command=update_aula,
                fg_color="#28a745",
                hover_color="#218838",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            update_btn.pack(side="left", padx=(0, 20))
            
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="CANCELAR",
                width=200,
                height=50,
                command=cancel,
                fg_color="#dc3545",
                hover_color="#c82333",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            cancel_btn.pack(side="left")
            
            # Enfocar en el primer campo
            name_entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir diálogo de edición: {e}")
    
    def delete_aula_from_context(self, values, tree, ciclo_data):
        """Eliminar aula desde el menú contextual"""
        try:
            aula_name = values[1]  # Columna "Aula"
            
            # Obtener el aula completo de la base de datos
            aulas = self.classroom_repo.get_all_rows()
            aula_data = next((a for a in aulas if a.get("name") == aula_name), None)
            
            if not aula_data:
                messagebox.showerror("Error", "No se pudo encontrar los datos del aula.")
                return
            
            # Mostrar confirmación
            result = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar el aula '{aula_name}'?\n\n"
                f"ADVERTENCIA: Esta acción eliminará:\n"
                f"• Todas las inscripciones del aula\n"
                f"• Todos los pagos relacionados\n\n"
                f"Esta acción NO se puede deshacer."
            )
            
            if result:
                # Usar eliminación en cascada
                success = self.classroom_repo.delete_classroom_cascade(aula_data.get("id"))
                
                if success:
                    messagebox.showinfo("Éxito", f"Aula '{aula_name}' eliminada correctamente")
                    # Recargar aulas
                    self.load_aulas_del_ciclo(tree, ciclo_data.get('id'))
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el aula")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar aula: {e}")
    
    def show_edit_ciclo_dialog(self, event):
        """Mostrar diálogo para editar ciclo"""
        try:
            # Obtener elemento seleccionado
            item = self.ciclo_tree.selection()[0] if self.ciclo_tree.selection() else None
            if not item:
                messagebox.showwarning("Advertencia", "Por favor seleccione un ciclo para editar")
                return
            
            # Obtener datos del ciclo
            values = self.ciclo_tree.item(item, "values")
            ciclo_name = values[2]  # Columna "Ciclo"
            
            # Obtener el ciclo completo de la base de datos
            ciclos = self.cicle_repo.get_all_rows()
            ciclo_data = next((c for c in ciclos if c.get("cicle") == ciclo_name), None)
            
            if not ciclo_data:
                messagebox.showerror("Error", "No se pudo encontrar los datos del ciclo.")
                return
            
            # Crear diálogo de edición
            dialog = ctk.CTkToplevel(self.parent)
            dialog.title("Editar Ciclo")
            dialog.geometry("500x550")
            dialog.resizable(False, False)
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
            y = (dialog.winfo_screenheight() // 2) - (550 // 2)
            dialog.geometry(f"500x550+{x}+{y}")
            
            # Hacer modal
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Título
            title = ctk.CTkLabel(
                dialog,
                text="EDITAR CICLO",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#1f538d"
            )
            title.pack(pady=20)
            
            # Frame para campos
            fields_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            fields_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            # Ciclo
            ciclo_label = ctk.CTkLabel(fields_frame, text="Ciclo:", font=ctk.CTkFont(size=14))
            ciclo_label.pack(pady=(0, 5), anchor="w")
            
            ciclo_var = ctk.StringVar(value=ciclo_data.get("cicle", ""))
            ciclo_combo = ctk.CTkComboBox(
                fields_frame,
                values=["I", "II", "III", "IV", "V"],
                variable=ciclo_var,
                width=450,
                height=35
            )
            ciclo_combo.pack(pady=(0, 15))
            
            # Encargado
            encargado_label = ctk.CTkLabel(fields_frame, text="Encargado:", font=ctk.CTkFont(size=14))
            encargado_label.pack(pady=(0, 5), anchor="w")
            
            encargado_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="Ingrese nombre del encargado",
                width=450,
                height=35
            )
            encargado_entry.insert(0, ciclo_data.get("manager", ""))
            encargado_entry.pack(pady=(0, 15))
            
            # Fecha Inicio
            fecha_inicio_label = ctk.CTkLabel(fields_frame, text="Fecha Inicio:", font=ctk.CTkFont(size=14))
            fecha_inicio_label.pack(pady=(0, 5), anchor="w")
            
            fecha_inicio_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="YYYY-MM-DD",
                width=450,
                height=35
            )
            fecha_inicio_entry.insert(0, str(ciclo_data.get("date_start", "")))
            fecha_inicio_entry.pack(pady=(0, 15))
            
            # Fecha Fin
            fecha_fin_label = ctk.CTkLabel(fields_frame, text="Fecha Fin:", font=ctk.CTkFont(size=14))
            fecha_fin_label.pack(pady=(0, 5), anchor="w")
            
            fecha_fin_entry = ctk.CTkEntry(
                fields_frame,
                placeholder_text="YYYY-MM-DD",
                width=450,
                height=35
            )
            fecha_fin_entry.insert(0, str(ciclo_data.get("date_end", "")))
            fecha_fin_entry.pack(pady=(0, 15))
            
            # Frame para botones
            buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(20, 30), padx=20)
            
            def update_ciclo():
                ciclo = ciclo_var.get()
                encargado = encargado_entry.get().strip()
                fecha_inicio = fecha_inicio_entry.get().strip()
                fecha_fin = fecha_fin_entry.get().strip()
                
                if not ciclo or not encargado or not fecha_inicio or not fecha_fin:
                    messagebox.showerror("Error", "Por favor complete todos los campos")
                    return
                
                try:
                    # Actualizar ciclo
                    update_data = {
                        "cicle": ciclo,
                        "manager": encargado,
                        "date_start": fecha_inicio,
                        "date_end": fecha_fin
                    }
                    
                    result = self.cicle_repo.update_row(update_data, {"id": ciclo_data.get("id")})
                    
                    if result > 0:
                        messagebox.showinfo("Éxito", "Ciclo actualizado correctamente")
                        dialog.destroy()
                        self.load_ciclos()
                        self.update_ciclo_title()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el ciclo")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar ciclo: {e}")
            
            def cancel():
                dialog.destroy()
            
            # Botones
            update_btn = ctk.CTkButton(
                buttons_frame,
                text="ACTUALIZAR CICLO",
                width=200,
                height=50,
                command=update_ciclo,
                fg_color="#28a745",
                hover_color="#218838",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            update_btn.pack(side="left", padx=(0, 20))
            
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="CANCELAR",
                width=200,
                height=50,
                command=cancel,
                fg_color="#dc3545",
                hover_color="#c82333",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            cancel_btn.pack(side="left")
            
            # Enfocar en el primer campo
            ciclo_combo.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir diálogo de edición: {e}")
    
    
    def show_aulas_content(self):
        """Mostrar contenido de gestión de Aulas"""
        # Frame principal para Aulas
        aulas_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        aulas_frame.pack(fill="both", expand=True, padx=30)
        
        # Título con información del ciclo activo
        
        # Información del ciclo activo
        if self.active_cicle:
            info_frame = ctk.CTkFrame(aulas_frame, fg_color="#e3f2fd", corner_radius=8)
            info_frame.pack(fill="x", pady=(0, 15))
            
            info_text = f"Ciclo Activo: {self.active_cicle.get('cicle')} | Encargado: {self.active_cicle.get('manager')} | Período: {self.active_cicle.get('date_start')} - {self.active_cicle.get('date_end')}"
            info_label = ctk.CTkLabel(
                info_frame,
                text=info_text,
                font=ctk.CTkFont(size=12),
                text_color="#1565c0"
            )
            info_label.pack(pady=10)
        
        # Formulario de Aulas
        self.create_aulas_form(aulas_frame)
        
        # Tabla de Aulas
        self.create_aulas_table(aulas_frame)
        
        # Paginación
        self.create_aulas_pagination(aulas_frame)
        
        # Cargar datos
        self.load_aulas()
    
    def create_aulas_form(self, parent):
        """Crear formulario para agregar aulas"""
        form_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Primera fila
        row1_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1_frame.pack(fill="x", padx=20, pady=15)
        
        # Fecha Inicio
        fecha_inicio_label = ctk.CTkLabel(row1_frame, text="Fecha Inicio:", font=ctk.CTkFont(size=14))
        fecha_inicio_label.pack(side="left", padx=(0, 10))
        
        self.aula_fecha_inicio_var = ctk.StringVar()
        fecha_inicio_entry = ctk.CTkEntry(
            row1_frame,
            placeholder_text="YYYY-MM-DD",
            textvariable=self.aula_fecha_inicio_var,
            width=150
        )
        fecha_inicio_entry.pack(side="left", padx=(0, 20))
        
        # Fecha Fin
        fecha_fin_label = ctk.CTkLabel(row1_frame, text="Fecha Fin:", font=ctk.CTkFont(size=14))
        fecha_fin_label.pack(side="left", padx=(0, 10))
        
        self.aula_fecha_fin_var = ctk.StringVar()
        fecha_fin_entry = ctk.CTkEntry(
            row1_frame,
            placeholder_text="YYYY-MM-DD",
            textvariable=self.aula_fecha_fin_var,
            width=150
        )
        fecha_fin_entry.pack(side="left", padx=(0, 20))
        
        # Curso
        curso_label = ctk.CTkLabel(row1_frame, text="Curso:", font=ctk.CTkFont(size=14))
        curso_label.pack(side="left", padx=(0, 10))
        
        self.aula_curso_var = ctk.StringVar()
        curso_combo = ctk.CTkComboBox(
            row1_frame,
            values=["Doctrina 1", "Doctrina 2", "Historia", "Evangelios"],
            variable=self.aula_curso_var,
            width=150
        )
        curso_combo.pack(side="left")
        
        # Segunda fila
        row2_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Aula
        aula_label = ctk.CTkLabel(row2_frame, text="Aula:", font=ctk.CTkFont(size=14))
        aula_label.pack(side="left", padx=(0, 10))
        
        self.aula_nombre_var = ctk.StringVar()
        aula_entry = ctk.CTkEntry(
            row2_frame,
            placeholder_text="Ej: 2do Secundaria",
            textvariable=self.aula_nombre_var,
            width=150
        )
        aula_entry.pack(side="left", padx=(0, 20))
        
        # Docente
        docente_label = ctk.CTkLabel(row2_frame, text="Docente:", font=ctk.CTkFont(size=14))
        docente_label.pack(side="left", padx=(0, 10))
        
        self.aula_docente_var = ctk.StringVar()
        docente_combo = ctk.CTkComboBox(
            row2_frame,
            values=["Daniel Yataco", "María García", "Juan Pérez"],
            variable=self.aula_docente_var,
            width=200
        )
        docente_combo.pack(side="left", padx=(0, 20))
        
        # Botón Agregar Aula
        add_aula_btn = ctk.CTkButton(
            row2_frame,
            text="Agregar Aula",
            width=150,
            height=35,
            command=self.add_aula,
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        add_aula_btn.pack(side="left")
    
    def create_aulas_table(self, parent):
        """Crear tabla de aulas"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        columns = ("Curso", "Aula", "Docente", "Fecha Inicio", "Fecha Fin", "Acciones")
        self.aulas_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        
        self.aulas_tree.heading("Curso", text="Curso")
        self.aulas_tree.heading("Aula", text="Aula")
        self.aulas_tree.heading("Docente", text="Docente")
        self.aulas_tree.heading("Fecha Inicio", text="Fecha Inicio")
        self.aulas_tree.heading("Fecha Fin", text="Fecha Fin")
        self.aulas_tree.heading("Acciones", text="Acciones")
        
        self.aulas_tree.column("Curso", width=150, anchor="center")
        self.aulas_tree.column("Aula", width=150, anchor="center")
        self.aulas_tree.column("Docente", width=200, anchor="center")
        self.aulas_tree.column("Fecha Inicio", width=120, anchor="center")
        self.aulas_tree.column("Fecha Fin", width=120, anchor="center")
        self.aulas_tree.column("Acciones", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.aulas_tree.yview)
        self.aulas_tree.configure(yscrollcommand=scrollbar.set)
        
        self.aulas_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.aulas_tree.bind("<Double-1>", self.show_edit_aula_dialog)
        self.aulas_tree.bind("<Button-3>", self.show_aula_context_menu)
    
    def create_aulas_pagination(self, parent):
        """Crear controles de paginación para aulas"""
        pagination_frame = ctk.CTkFrame(parent, fg_color="transparent")
        pagination_frame.pack(fill="x", pady=(0, 15))
        
        self.aulas_pagination_label = ctk.CTkLabel(
            pagination_frame,
            text="1/10 Páginas",
            font=ctk.CTkFont(size=12)
        )
        self.aulas_pagination_label.pack(side="left")
        
        prev_btn = ctk.CTkButton(
            pagination_frame,
            text="Anterior",
            width=80,
            height=30,
            command=self.previous_aulas_page,
            font=ctk.CTkFont(size=12)
        )
        prev_btn.pack(side="right", padx=(5, 0))
        
        next_btn = ctk.CTkButton(
            pagination_frame,
            text="Siguiente",
            width=80,
            height=30,
            command=self.next_aulas_page,
            font=ctk.CTkFont(size=12)
        )
        next_btn.pack(side="right")
    
    def load_aulas(self):
        """Cargar aulas desde la base de datos del ciclo activo"""
        try:
            if not self.active_cicle:
                # Si no hay ciclo activo, mostrar mensaje
                self.update_aulas_table([])
                self.aulas_pagination_label.configure(text="0/0 Páginas")
                return
            
            # Obtener todas las aulas
            aulas = self.classroom_repo.get_all_rows()
            
            # Filtrar aulas del ciclo activo
            aulas_ciclo = [aula for aula in aulas if aula.get("id_cicle") == self.active_cicle.get("id")]
            
            # Actualizar tabla
            self.update_aulas_table(aulas_ciclo)
            
            # Actualizar paginación
            total_pages = (len(aulas_ciclo) + self.classrooms_per_page - 1) // self.classrooms_per_page
            self.aulas_pagination_label.configure(text=f"{self.current_classroom_page}/{max(1, total_pages)} Páginas")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar aulas: {e}")
    
    def update_aulas_table(self, aulas):
        """Actualizar la tabla de aulas"""
        # Limpiar tabla
        for item in self.aulas_tree.get_children():
            self.aulas_tree.delete(item)
        
        # Calcular rango de páginas
        start_idx = (self.current_classroom_page - 1) * self.classrooms_per_page
        end_idx = start_idx + self.classrooms_per_page
        
        # Agregar aulas de la página actual
        for aula in aulas[start_idx:end_idx]:
            self.aulas_tree.insert("", "end", values=(
                aula.get("course_name", ""),
                aula.get("name", ""),
                aula.get("teacher_name", ""),
                str(aula.get("start_date", "")),
                str(aula.get("end_date", "")),
                "Editar | Eliminar"
            ))
    
    def add_aula(self):
        """Agregar nueva aula al ciclo activo"""
        fecha_inicio = self.aula_fecha_inicio_var.get().strip()
        fecha_fin = self.aula_fecha_fin_var.get().strip()
        curso = self.aula_curso_var.get()
        aula = self.aula_nombre_var.get().strip()
        docente = self.aula_docente_var.get()
        
        # Validaciones
        if not fecha_inicio or not fecha_fin or not curso or not aula or not docente:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return
        
        # Validar que hay un ciclo activo
        if not self.active_cicle:
            messagebox.showerror("Error", "Debe tener un ciclo activo para crear aulas.")
            return
        
        try:
            # Crear aula asociada al ciclo activo
            self.classroom_repo.insert_row({
                "name": aula,
                "start_date": fecha_inicio,
                "end_date": fecha_fin,
                "id_teacher": 1,  # ID del docente (por ahora hardcodeado)
                "id_course": 1,   # ID del curso (por ahora hardcodeado)
                "id_cicle": self.active_cicle.get("id")  # ID del ciclo activo
            })
            
            messagebox.showinfo(
                "Éxito", 
                f"Aula '{aula}' creada correctamente para el ciclo {self.active_cicle.get('cicle')}."
            )
            
            # Limpiar formulario
            self.aula_fecha_inicio_var.set("")
            self.aula_fecha_fin_var.set("")
            self.aula_curso_var.set("")
            self.aula_nombre_var.set("")
            self.aula_docente_var.set("")
            
            # Recargar aulas
            self.load_aulas()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear aula: {e}")
    
    def previous_aulas_page(self):
        """Ir a la página anterior de aulas"""
        if self.current_classroom_page > 1:
            self.current_classroom_page -= 1
            self.load_aulas()
    
    def next_aulas_page(self):
        """Ir a la página siguiente de aulas"""
        try:
            aulas = self.classroom_repo.get_all_rows()
            total_pages = (len(aulas) + self.classrooms_per_page - 1) // self.classrooms_per_page
            
            if self.current_classroom_page < total_pages:
                self.current_classroom_page += 1
                self.load_aulas()
        except Exception as e:
            messagebox.showerror("Error", f"Error en paginación: {e}")
    
    
    
    def show_matricula_content(self):
        """Mostrar contenido del formulario de matrícula"""
        # Frame principal para Matrícula
        matricula_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        matricula_frame.pack(fill="both", expand=True, padx=30)
        
        # Título con información del ciclo activo
        if self.active_cicle:
            ciclo_info = f"{self.active_cicle.get('cicle')} - {self.active_cicle.get('date_start')[:4]}"
            title_text = f"MATRÍCULA - CICLO {ciclo_info}"
        else:
            title_text = "MATRÍCULA"
            
        title = ctk.CTkLabel(
            matricula_frame,
            text=title_text,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))
        
        # Información del ciclo activo
        if self.active_cicle:
            info_frame = ctk.CTkFrame(matricula_frame, fg_color="#e8f5e8", corner_radius=8)
            info_frame.pack(fill="x", pady=(0, 15))
            
            info_text = f"Ciclo Activo: {self.active_cicle.get('cicle')} | Encargado: {self.active_cicle.get('manager')} | Período: {self.active_cicle.get('date_start')} - {self.active_cicle.get('date_end')}"
            info_label = ctk.CTkLabel(
                info_frame,
                text=info_text,
                font=ctk.CTkFont(size=12),
                text_color="#2e7d32"
            )
            info_label.pack(pady=10)
        else:
            # Mensaje de advertencia si no hay ciclo activo
            warning_frame = ctk.CTkFrame(matricula_frame, fg_color="#fff3e0", corner_radius=8)
            warning_frame.pack(fill="x", pady=(0, 15))
            
            warning_label = ctk.CTkLabel(
                warning_frame,
                text="No hay un ciclo activo. Debe activar un ciclo antes de crear matrículas.",
                font=ctk.CTkFont(size=12),
                text_color="#f57c00"
            )
            warning_label.pack(pady=10)
        
        # Sección de Consulta
        self.create_matricula_consulta_section(matricula_frame)
        
        # Sección de Matrícula
        self.create_matricula_form_section(matricula_frame)
    
    def create_matricula_consulta_section(self, parent):
        """Crear sección de consulta de matrículas"""
        consulta_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        consulta_frame.pack(fill="x", pady=(0, 20))
        
        # Título de consulta
        consulta_title = ctk.CTkLabel(
            consulta_frame,
            text="Consulta",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        consulta_title.pack(pady=(15, 10))
        
        # Filtros
        filters_frame = ctk.CTkFrame(consulta_frame, fg_color="transparent")
        filters_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Buscar Estudiante
        estudiante_label = ctk.CTkLabel(filters_frame, text="Buscar Estudiante:", font=ctk.CTkFont(size=14))
        estudiante_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.matricula_estudiante_var = ctk.StringVar()
        estudiante_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="Buscar por nombre...",
            textvariable=self.matricula_estudiante_var,
            width=200
        )
        estudiante_entry.grid(row=0, column=1, padx=(0, 20), pady=10)
        
        # Buscar Curso
        curso_label = ctk.CTkLabel(filters_frame, text="Buscar Curso:", font=ctk.CTkFont(size=14))
        curso_label.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="w")
        
        self.matricula_curso_var = ctk.StringVar()
        curso_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="Buscar curso...",
            textvariable=self.matricula_curso_var,
            width=200
        )
        curso_entry.grid(row=0, column=3, padx=(0, 20), pady=10)
        
        # Año
        año_label = ctk.CTkLabel(filters_frame, text="Año:", font=ctk.CTkFont(size=14))
        año_label.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.matricula_año_var = ctk.StringVar()
        año_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="2025",
            textvariable=self.matricula_año_var,
            width=100
        )
        año_entry.grid(row=1, column=1, padx=(0, 20), pady=10)
        
        # Fecha Llevada
        fecha_label = ctk.CTkLabel(filters_frame, text="Fecha Llevada:", font=ctk.CTkFont(size=14))
        fecha_label.grid(row=1, column=2, padx=(0, 10), pady=10, sticky="w")
        
        self.matricula_fecha_var = ctk.StringVar()
        fecha_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="DD-MM-AAAA",
            textvariable=self.matricula_fecha_var,
            width=150
        )
        fecha_entry.grid(row=1, column=3, padx=(0, 20), pady=10)
        
        # Tabla de consulta
        table_frame = ctk.CTkFrame(consulta_frame)
        table_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        columns = ("Curso", "Año", "Ciclo", "Fecha Llevada", "Docente", "Acciones")
        self.consulta_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=4)
        
        self.consulta_tree.heading("Curso", text="Curso")
        self.consulta_tree.heading("Año", text="Año")
        self.consulta_tree.heading("Ciclo", text="Ciclo")
        self.consulta_tree.heading("Fecha Llevada", text="Fecha Llevada")
        self.consulta_tree.heading("Docente", text="Docente")
        self.consulta_tree.heading("Acciones", text="Acciones")
        
        self.consulta_tree.column("Curso", width=150, anchor="center")
        self.consulta_tree.column("Año", width=80, anchor="center")
        self.consulta_tree.column("Ciclo", width=80, anchor="center")
        self.consulta_tree.column("Fecha Llevada", width=120, anchor="center")
        self.consulta_tree.column("Docente", width=150, anchor="center")
        self.consulta_tree.column("Acciones", width=80, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.consulta_tree.yview)
        self.consulta_tree.configure(yscrollcommand=scrollbar.set)
        
        self.consulta_tree.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Paginación de consulta
        pagination_frame = ctk.CTkFrame(consulta_frame, fg_color="transparent")
        pagination_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.consulta_pagination_label = ctk.CTkLabel(
            pagination_frame,
            text="1/10 Páginas",
            font=ctk.CTkFont(size=12)
        )
        self.consulta_pagination_label.pack(side="left")
        
        prev_btn = ctk.CTkButton(
            pagination_frame,
            text="Anterior",
            width=80,
            height=30,
            command=self.previous_consulta_page,
            font=ctk.CTkFont(size=12)
        )
        prev_btn.pack(side="right", padx=(5, 0))
        
        next_btn = ctk.CTkButton(
            pagination_frame,
            text="Siguiente",
            width=80,
            height=30,
            command=self.next_consulta_page,
            font=ctk.CTkFont(size=12)
        )
        next_btn.pack(side="right")
    
    def create_matricula_form_section(self, parent):
        """Crear sección del formulario de matrícula"""
        form_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        form_frame.pack(fill="both", expand=True)
        
        # Título del formulario
        form_title = ctk.CTkLabel(
            form_frame,
            text="Matrícula",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        form_title.pack(pady=(15, 20))
        
        # Sección Estudiante
        self.create_estudiante_section(form_frame)
        
        # Sección Inscripción
        self.create_inscripcion_section(form_frame)
        
        # Sección Pago
        self.create_pago_section(form_frame)
        
        # Botón final
        self.create_matricula_final_button(form_frame)
    
    def create_estudiante_section(self, parent):
        """Crear sección de información del estudiante"""
        estudiante_frame = ctk.CTkFrame(parent, fg_color="#f8f9fa", corner_radius=8)
        estudiante_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Título de sección
        section_title = ctk.CTkLabel(
            estudiante_frame,
            text="Estudiante",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        section_title.pack(pady=(15, 10))
        
        # Primera fila - Estudiante y botones
        row1_frame = ctk.CTkFrame(estudiante_frame, fg_color="transparent")
        row1_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Estudiante
        estudiante_label = ctk.CTkLabel(row1_frame, text="Estudiante:", font=ctk.CTkFont(size=14))
        estudiante_label.pack(side="left", padx=(0, 10))
        
        self.matricula_estudiante_select_var = ctk.StringVar()
        estudiante_combo = ctk.CTkComboBox(
            row1_frame,
            values=["Seleccionar estudiante..."],
            variable=self.matricula_estudiante_select_var,
            width=250
        )
        estudiante_combo.pack(side="left", padx=(0, 20))
        
        # Botones de estudiante
        add_estudiante_btn = ctk.CTkButton(
            row1_frame,
            text="Agregar Estudiante",
            width=150,
            height=30,
            command=self.show_add_estudiante_dialog,
            fg_color="#17a2b8",
            hover_color="#138496",
            font=ctk.CTkFont(size=12)
        )
        add_estudiante_btn.pack(side="left", padx=(0, 10))
        
        update_estudiante_btn = ctk.CTkButton(
            row1_frame,
            text="Actualizar Estudiante",
            width=150,
            height=30,
            command=self.update_estudiante,
            fg_color="#ffc107",
            hover_color="#e0a800",
            font=ctk.CTkFont(size=12)
        )
        update_estudiante_btn.pack(side="left", padx=(0, 10))
        
        clear_form_btn = ctk.CTkButton(
            row1_frame,
            text="Vaciar Formulario",
            width=150,
            height=30,
            command=self.clear_matricula_form,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=12)
        )
        clear_form_btn.pack(side="left")
        
        # Segunda fila - Campos del estudiante
        row2_frame = ctk.CTkFrame(estudiante_frame, fg_color="transparent")
        row2_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Nombres
        nombres_label = ctk.CTkLabel(row2_frame, text="Nombres:", font=ctk.CTkFont(size=14))
        nombres_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_nombres_var = ctk.StringVar()
        nombres_entry = ctk.CTkEntry(
            row2_frame,
            placeholder_text="Ingrese nombres",
            textvariable=self.matricula_nombres_var,
            width=200
        )
        nombres_entry.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        # Apellidos
        apellidos_label = ctk.CTkLabel(row2_frame, text="Apellidos:", font=ctk.CTkFont(size=14))
        apellidos_label.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_apellidos_var = ctk.StringVar()
        apellidos_entry = ctk.CTkEntry(
            row2_frame,
            placeholder_text="Ingrese apellidos",
            textvariable=self.matricula_apellidos_var,
            width=200
        )
        apellidos_entry.grid(row=0, column=3, padx=(0, 20), pady=5)
        
        # Tercera fila - Más campos
        row3_frame = ctk.CTkFrame(estudiante_frame, fg_color="transparent")
        row3_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Fecha Bautismo
        bautismo_label = ctk.CTkLabel(row3_frame, text="Fecha Bautismo:", font=ctk.CTkFont(size=14))
        bautismo_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_bautismo_var = ctk.StringVar()
        bautismo_entry = ctk.CTkEntry(
            row3_frame,
            placeholder_text="DD-MM-AAAA",
            textvariable=self.matricula_bautismo_var,
            width=150
        )
        bautismo_entry.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        # Fecha Nacimiento
        nacimiento_label = ctk.CTkLabel(row3_frame, text="Fecha Nacimiento:", font=ctk.CTkFont(size=14))
        nacimiento_label.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_nacimiento_var = ctk.StringVar()
        nacimiento_entry = ctk.CTkEntry(
            row3_frame,
            placeholder_text="DD-MM-AAAA",
            textvariable=self.matricula_nacimiento_var,
            width=150
        )
        nacimiento_entry.grid(row=0, column=3, padx=(0, 20), pady=5)
        
        # Cuarta fila
        row4_frame = ctk.CTkFrame(estudiante_frame, fg_color="transparent")
        row4_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Teléfono
        telefono_label = ctk.CTkLabel(row4_frame, text="Teléfono:", font=ctk.CTkFont(size=14))
        telefono_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_telefono_var = ctk.StringVar()
        telefono_entry = ctk.CTkEntry(
            row4_frame,
            placeholder_text="Número de teléfono",
            textvariable=self.matricula_telefono_var,
            width=200
        )
        telefono_entry.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        # Red
        red_label = ctk.CTkLabel(row4_frame, text="Red:", font=ctk.CTkFont(size=14))
        red_label.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_red_var = ctk.StringVar()
        red_combo = ctk.CTkComboBox(
            row4_frame,
            values=["Rise Up", "Youth", "Adults", "Children"],
            variable=self.matricula_red_var,
            width=200
        )
        red_combo.grid(row=0, column=3, padx=(0, 20), pady=5)
    
    def create_inscripcion_section(self, parent):
        """Crear sección de inscripción"""
        inscripcion_frame = ctk.CTkFrame(parent, fg_color="#f8f9fa", corner_radius=8)
        inscripcion_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Título de sección
        section_title = ctk.CTkLabel(
            inscripcion_frame,
            text="Inscripción",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        section_title.pack(pady=(15, 10))
        
        # Primera fila - Aula y Curso
        row1_frame = ctk.CTkFrame(inscripcion_frame, fg_color="transparent")
        row1_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Seleccionar Aula
        aula_label = ctk.CTkLabel(row1_frame, text="Seleccionar Aula:", font=ctk.CTkFont(size=14))
        aula_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_aula_select_var = ctk.StringVar()
        self.matricula_aula_combo = ctk.CTkComboBox(
            row1_frame,
            values=["Seleccionar aula..."],
            variable=self.matricula_aula_select_var,
            width=250,
            command=self.on_aula_selected
        )
        self.matricula_aula_combo.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        # Buscar Curso (se llena automáticamente según el aula)
        curso_label = ctk.CTkLabel(row1_frame, text="Curso:", font=ctk.CTkFont(size=14))
        curso_label.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_curso_select_var = ctk.StringVar()
        self.matricula_curso_combo = ctk.CTkComboBox(
            row1_frame,
            values=["Seleccione un aula primero"],
            variable=self.matricula_curso_select_var,
            width=200,
            state="disabled"
        )
        self.matricula_curso_combo.grid(row=0, column=3, padx=(0, 20), pady=5)
        
        # Segunda fila - Material y Tipo
        row2_frame = ctk.CTkFrame(inscripcion_frame, fg_color="transparent")
        row2_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Material
        material_label = ctk.CTkLabel(row2_frame, text="Material:", font=ctk.CTkFont(size=14))
        material_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_material_var = ctk.StringVar()
        material_combo = ctk.CTkComboBox(
            row2_frame,
            values=["Libro", "PDF", "Digital"],
            variable=self.matricula_material_var,
            width=150
        )
        material_combo.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        # Tipo Material
        tipo_material_label = ctk.CTkLabel(row2_frame, text="Tipo Material:", font=ctk.CTkFont(size=14))
        tipo_material_label.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_tipo_material_var = ctk.StringVar()
        tipo_material_combo = ctk.CTkComboBox(
            row2_frame,
            values=["Físico", "Digital"],
            variable=self.matricula_tipo_material_var,
            width=150
        )
        tipo_material_combo.grid(row=0, column=3, padx=(0, 20), pady=5)
        
        # Cargar aulas disponibles
        self.load_aulas_for_matricula()
    
    def create_pago_section(self, parent):
        """Crear sección de pago"""
        pago_frame = ctk.CTkFrame(parent, fg_color="#f8f9fa", corner_radius=8)
        pago_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Título de sección
        section_title = ctk.CTkLabel(
            pago_frame,
            text="Pago",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        section_title.pack(pady=(15, 10))
        
        # Fila de campos
        row_frame = ctk.CTkFrame(pago_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Pago
        pago_label = ctk.CTkLabel(row_frame, text="Pago:", font=ctk.CTkFont(size=14))
        pago_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_pago_var = ctk.StringVar()
        pago_entry = ctk.CTkEntry(
            row_frame,
            placeholder_text="Monto",
            textvariable=self.matricula_pago_var,
            width=150
        )
        pago_entry.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        # Método de Pago
        metodo_label = ctk.CTkLabel(row_frame, text="Método de Pago:", font=ctk.CTkFont(size=14))
        metodo_label.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="w")
        
        self.matricula_metodo_pago_var = ctk.StringVar()
        metodo_combo = ctk.CTkComboBox(
            row_frame,
            values=["Efectivo", "Transferencia", "Tarjeta"],
            variable=self.matricula_metodo_pago_var,
            width=150
        )
        metodo_combo.grid(row=0, column=3, padx=(0, 20), pady=5)
        
        # Botón Agregar Pago
        add_pago_btn = ctk.CTkButton(
            row_frame,
            text="Agregar Pago",
            width=150,
            height=30,
            command=self.add_pago,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=12)
        )
        add_pago_btn.grid(row=0, column=4, padx=(0, 20), pady=5)
    
    def create_matricula_final_button(self, parent):
        """Crear botón final para agregar matrícula"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Botón grande de Agregar Matrícula
        add_matricula_btn = ctk.CTkButton(
            button_frame,
            text="AGREGAR MATRÍCULA",
            width=300,
            height=50,
            command=self.add_matricula,
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        add_matricula_btn.pack(pady=20)
    
    # Métodos auxiliares para matrícula
    def show_add_estudiante_dialog(self):
        """Mostrar diálogo para agregar estudiante"""
        messagebox.showinfo("Info", "Funcionalidad de agregar estudiante en desarrollo")
    
    def update_estudiante(self):
        """Actualizar información del estudiante"""
        messagebox.showinfo("Info", "Funcionalidad de actualizar estudiante en desarrollo")
    
    def clear_matricula_form(self):
        """Limpiar formulario de matrícula"""
        self.matricula_estudiante_select_var.set("")
        self.matricula_nombres_var.set("")
        self.matricula_apellidos_var.set("")
        self.matricula_bautismo_var.set("")
        self.matricula_nacimiento_var.set("")
        self.matricula_telefono_var.set("")
        self.matricula_red_var.set("")
        self.matricula_aula_select_var.set("")
        self.matricula_curso_select_var.set("")
        self.matricula_material_var.set("")
        self.matricula_tipo_material_var.set("")
        self.matricula_pago_var.set("")
        self.matricula_metodo_pago_var.set("")
        self.selected_aula_for_matricula = None
        messagebox.showinfo("Info", "Formulario limpiado")
    
    def add_pago(self):
        """Agregar pago"""
        pago = self.matricula_pago_var.get().strip()
        metodo = self.matricula_metodo_pago_var.get()
        
        if not pago or not metodo:
            messagebox.showerror("Error", "Por favor complete el monto y método de pago.")
            return
        
        messagebox.showinfo("Éxito", f"Pago de {pago} ({metodo}) agregado correctamente.")
    
    def add_matricula(self):
        """Agregar matrícula completa"""
        # Validar que hay un ciclo activo
        if not self.active_cicle:
            messagebox.showerror("Error", "Debe tener un ciclo activo para crear matrículas.")
            return
        
        # Validar que hay un aula seleccionada
        if not self.selected_aula_for_matricula:
            messagebox.showerror("Error", "Debe seleccionar un aula para crear la matrícula.")
            return
        
        # Validar campos requeridos
        nombres = self.matricula_nombres_var.get().strip()
        apellidos = self.matricula_apellidos_var.get().strip()
        curso = self.matricula_curso_select_var.get()
        
        if not nombres or not apellidos or not curso:
            messagebox.showerror("Error", "Por favor complete al menos nombres, apellidos y curso.")
            return
        
        # Crear matrícula
        try:
            # Aquí se implementaría la lógica para guardar la matrícula
            aula_name = self.selected_aula_for_matricula.get('name', 'Aula')
            ciclo_name = self.active_cicle.get('cicle', 'Ciclo')
            
            messagebox.showinfo(
                "Éxito", 
                f"Matrícula creada correctamente:\n\n"
                f"Estudiante: {nombres} {apellidos}\n"
                f"Aula: {aula_name}\n"
                f"Curso: {curso}\n"
                f"Ciclo: {ciclo_name}"
            )
            
            # Limpiar formulario
            self.clear_matricula_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear matrícula: {e}")
    
    def previous_consulta_page(self):
        """Ir a la página anterior de consulta"""
        messagebox.showinfo("Info", "Funcionalidad de paginación en desarrollo")
    
    def next_consulta_page(self):
        """Ir a la página siguiente de consulta"""
        messagebox.showinfo("Info", "Funcionalidad de paginación en desarrollo")
    
    def load_aulas_for_matricula(self):
        """Cargar aulas disponibles para matrícula"""
        try:
            if not self.active_cicle:
                self.matricula_aula_combo.configure(values=["No hay ciclo activo"])
                return
            
            # Obtener aulas del ciclo activo
            aulas = self.classroom_repo.get_all_rows()
            aulas_ciclo = [aula for aula in aulas if aula.get("id_cicle") == self.active_cicle.get("id")]
            
            if aulas_ciclo:
                aula_options = [f"{aula.get('name', '')} - {aula.get('course_name', 'Curso')}" for aula in aulas_ciclo]
                self.matricula_aula_combo.configure(values=aula_options)
            else:
                self.matricula_aula_combo.configure(values=["No hay aulas disponibles"])
                
        except Exception as e:
            self.matricula_aula_combo.configure(values=[f"Error: {e}"])
    
    def on_aula_selected(self, selected_aula):
        """Manejar selección de aula"""
        try:
            if not self.active_cicle:
                return
            
            # Obtener aulas del ciclo activo
            aulas = self.classroom_repo.get_all_rows()
            aulas_ciclo = [aula for aula in aulas if aula.get("id_cicle") == self.active_cicle.get("id")]
            
            # Encontrar el aula seleccionada
            selected_aula_data = None
            for aula in aulas_ciclo:
                aula_display = f"{aula.get('name', '')} - {aula.get('course_name', 'Curso')}"
                if aula_display == selected_aula:
                    selected_aula_data = aula
                    break
            
            if selected_aula_data:
                # Habilitar y llenar el combo de curso
                self.matricula_curso_combo.configure(state="normal")
                curso_name = selected_aula_data.get('course_name', 'Curso')
                self.matricula_curso_combo.configure(values=[curso_name])
                self.matricula_curso_combo.set(curso_name)
                
                # Guardar referencia al aula seleccionada
                self.selected_aula_for_matricula = selected_aula_data
            else:
                self.matricula_curso_combo.configure(state="disabled")
                self.matricula_curso_combo.configure(values=["Seleccione un aula válida"])
                self.selected_aula_for_matricula = None
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar aula: {e}")
        
    def show_red_content(self):
        """Mostrar contenido de Red (Gestión de Equipos)"""
        # Título principal
        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="Gestión de Equipos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(side="left")
        
        # Botón para agregar equipo
        add_team_btn = ctk.CTkButton(
            title_frame,
            text="Agregar Equipo",
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_add_team_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=10,
            border_width=2,
            border_color="#1e7e34"
        )
        add_team_btn.pack(side="right", padx=(0, 10), pady=5)
        
        # Frame para filtros
        filters_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        filters_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Título de filtros
        filters_title = ctk.CTkLabel(
            filters_frame,
            text="Filtros de Búsqueda",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        filters_title.pack(pady=(20, 15))
        
        # Fila de filtros
        filters_row = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_row.pack(fill="x", padx=20, pady=(0, 20))
        
        # Filtro por nombre de equipo
        name_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        name_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            name_filter_frame,
            text="Nombre del Equipo:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.team_name_filter = ctk.CTkEntry(
            name_filter_frame,
            placeholder_text="Buscar por nombre...",
            width=200,
            height=35
        )
        self.team_name_filter.pack(pady=(5, 0))
        
        # Filtro por género
        gender_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        gender_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            gender_filter_frame,
            text="Género:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.team_gender_filter = ctk.CTkComboBox(
            gender_filter_frame,
            values=["Todos", "Masculino", "Femenino", "Mixto"],
            width=120,
            height=35
        )
        self.team_gender_filter.set("Todos")
        self.team_gender_filter.pack(pady=(5, 0))
        
        # Filtro por edad mínima
        min_age_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        min_age_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            min_age_filter_frame,
            text="Edad Mínima:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.team_min_age_filter = ctk.CTkEntry(
            min_age_filter_frame,
            placeholder_text="Min",
            width=80,
            height=35
        )
        self.team_min_age_filter.pack(pady=(5, 0))
        
        # Filtro por edad máxima
        max_age_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        max_age_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            max_age_filter_frame,
            text="Edad Máxima:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.team_max_age_filter = ctk.CTkEntry(
            max_age_filter_frame,
            placeholder_text="Max",
            width=80,
            height=35
        )
        self.team_max_age_filter.pack(pady=(5, 0))
        
        # Botones de filtro
        filter_buttons_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        filter_buttons_frame.pack(side="right")
        
        search_btn = ctk.CTkButton(
            filter_buttons_frame,
            text="Buscar",
            width=100,
            height=35,
            command=self.filter_teams,
            fg_color="#1f538d",
            hover_color="#0d47a1"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            filter_buttons_frame,
            text="Limpiar",
            width=100,
            height=35,
            command=self.clear_team_filters,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        clear_btn.pack(side="left")
        
        # Frame para la tabla de equipos
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Título de la tabla
        table_title = ctk.CTkLabel(
            table_frame,
            text="Lista de Equipos",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        table_title.pack(pady=(20, 15))
        
        # Crear tabla de equipos
        self.create_teams_table(table_frame)
        
        # Cargar datos reales de la base de datos
        self.load_teams_from_database()
        
    def show_cursos_content(self):
        """Mostrar contenido de Cursos"""
        # Título principal
        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="Gestión de Cursos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(side="left")
        
        # Botón para agregar curso
        add_course_btn = ctk.CTkButton(
            title_frame,
            text="Nuevo Curso",
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_add_course_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=10,
            border_width=2,
            border_color="#1e7e34"
        )
        add_course_btn.pack(side="right", padx=(0, 10), pady=5)
        
        # Frame para filtros
        filters_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        filters_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Título de filtros
        filters_title = ctk.CTkLabel(
            filters_frame,
            text="Filtros de Búsqueda",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        filters_title.pack(pady=(20, 15))
        
        # Fila de filtros
        filters_row = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_row.pack(fill="x", padx=20, pady=(0, 20))
        
        # Filtro por nombre
        name_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        name_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            name_filter_frame,
            text="Nombre del Curso:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.course_name_filter = ctk.CTkEntry(
            name_filter_frame,
            placeholder_text="Buscar por nombre...",
            width=200,
            height=35
        )
        self.course_name_filter.pack(pady=(5, 0))
        
        # Filtro por nivel
        level_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        level_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            level_filter_frame,
            text="Nivel:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.course_level_filter = ctk.CTkEntry(
            level_filter_frame,
            placeholder_text="Buscar por nivel...",
            width=120,
            height=35
        )
        self.course_level_filter.pack(pady=(5, 0))
        
        # Botones de filtro
        filter_buttons_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        filter_buttons_frame.pack(side="right")
        
        search_btn = ctk.CTkButton(
            filter_buttons_frame,
            text="Buscar",
            width=100,
            height=35,
            command=self.filter_courses,
            fg_color="#1f538d",
            hover_color="#0d47a1"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            filter_buttons_frame,
            text="Limpiar",
            width=100,
            height=35,
            command=self.clear_course_filters,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        clear_btn.pack(side="left")
        
        # Frame para la tabla de cursos
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Título de la tabla
        table_title = ctk.CTkLabel(
            table_frame,
            text="Lista de Cursos",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        table_title.pack(pady=(20, 15))
        
        # Crear tabla de cursos
        self.create_courses_table(table_frame)
        
        # Cargar datos reales de la base de datos
        self.load_courses_from_database()
        
    def show_estudiantes_content(self):
        """Mostrar contenido de Estudiantes"""
        # Título principal
        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="Gestión de Estudiantes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(side="left")
        
        # Botón para agregar estudiante
        add_student_btn = ctk.CTkButton(
            title_frame,
            text="Nuevo Estudiante",
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_add_student_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=10,
            border_width=2,
            border_color="#1e7e34"
        )
        add_student_btn.pack(side="right", padx=(0, 10), pady=5)
        
        # Frame para filtros
        filters_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        filters_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Título de filtros
        filters_title = ctk.CTkLabel(
            filters_frame,
            text="Filtros de Búsqueda",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        filters_title.pack(pady=(20, 15))
        
        # Fila de filtros
        filters_row = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_row.pack(fill="x", padx=20, pady=(0, 20))
        
        # Filtro por nombre
        name_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        name_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            name_filter_frame,
            text="Nombre:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.student_name_filter = ctk.CTkEntry(
            name_filter_frame,
            placeholder_text="Buscar por nombre...",
            width=200,
            height=35
        )
        self.student_name_filter.pack(pady=(5, 0))
        
        # Filtro por teléfono
        phone_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        phone_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            phone_filter_frame,
            text="Teléfono:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.student_phone_filter = ctk.CTkEntry(
            phone_filter_frame,
            placeholder_text="Buscar por teléfono...",
            width=150,
            height=35
        )
        self.student_phone_filter.pack(pady=(5, 0))
        
        # Filtro por equipo
        team_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        team_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            team_filter_frame,
            text="Equipo:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.student_team_filter = ctk.CTkComboBox(
            team_filter_frame,
            values=["Todos"],
            width=120,
            height=35
        )
        self.student_team_filter.set("Todos")
        self.student_team_filter.pack(pady=(5, 0))
        
        # Botones de filtro
        filter_buttons_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        filter_buttons_frame.pack(side="right")
        
        search_btn = ctk.CTkButton(
            filter_buttons_frame,
            text="Buscar",
            width=100,
            height=35,
            command=self.filter_students,
            fg_color="#1f538d",
            hover_color="#0d47a1"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            filter_buttons_frame,
            text="Limpiar",
            width=100,
            height=35,
            command=self.clear_student_filters,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        clear_btn.pack(side="left")
        
        # Frame para la tabla de estudiantes
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Título de la tabla
        table_title = ctk.CTkLabel(
            table_frame,
            text="Lista de Estudiantes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        table_title.pack(pady=(20, 15))
        
        # Crear tabla de estudiantes
        self.create_students_table(table_frame)
        
        # Cargar equipos para el filtro
        self.load_teams_for_student_filter()
        
        # Cargar datos reales de la base de datos
        self.load_students_from_database()
        
    def show_docentes_content(self):
        """Mostrar contenido de Docentes"""
        # Título principal
        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="Gestión de Docentes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(side="left")
        
        # Botón para agregar docente
        add_teacher_btn = ctk.CTkButton(
            title_frame,
            text="Nuevo Docente",
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_add_teacher_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=10,
            border_width=2,
            border_color="#1e7e34"
        )
        add_teacher_btn.pack(side="right", padx=(0, 10), pady=5)
        
        # Frame para filtros
        filters_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        filters_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Título de filtros
        filters_title = ctk.CTkLabel(
            filters_frame,
            text="Filtros de Búsqueda",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        filters_title.pack(pady=(20, 15))
        
        # Fila de filtros
        filters_row = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_row.pack(fill="x", padx=20, pady=(0, 20))
        
        # Filtro por nombre
        name_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        name_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            name_filter_frame,
            text="Nombre:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.teacher_name_filter = ctk.CTkEntry(
            name_filter_frame,
            placeholder_text="Buscar por nombre...",
            width=200,
            height=35
        )
        self.teacher_name_filter.pack(pady=(5, 0))
        
        # Filtro por teléfono
        phone_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        phone_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            phone_filter_frame,
            text="Teléfono:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.teacher_phone_filter = ctk.CTkEntry(
            phone_filter_frame,
            placeholder_text="Buscar por teléfono...",
            width=150,
            height=35
        )
        self.teacher_phone_filter.pack(pady=(5, 0))
        
        # Filtro por equipo
        team_filter_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        team_filter_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            team_filter_frame,
            text="Equipo:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        self.teacher_team_filter = ctk.CTkComboBox(
            team_filter_frame,
            values=["Todos"],
            width=120,
            height=35
        )
        self.teacher_team_filter.set("Todos")
        self.teacher_team_filter.pack(pady=(5, 0))
        
        # Botones de filtro
        filter_buttons_frame = ctk.CTkFrame(filters_row, fg_color="transparent")
        filter_buttons_frame.pack(side="right")
        
        search_btn = ctk.CTkButton(
            filter_buttons_frame,
            text="Buscar",
            width=100,
            height=35,
            command=self.filter_teachers,
            fg_color="#1f538d",
            hover_color="#0d47a1"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            filter_buttons_frame,
            text="Limpiar",
            width=100,
            height=35,
            command=self.clear_teacher_filters,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        clear_btn.pack(side="left")
        
        # Frame para la tabla de docentes
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Título de la tabla
        table_title = ctk.CTkLabel(
            table_frame,
            text="Lista de Docentes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        table_title.pack(pady=(20, 15))
        
        # Crear tabla de docentes
        self.create_teachers_table(table_frame)
        
        # Cargar equipos para el filtro
        self.load_teams_for_teacher_filter()
        
        # Cargar datos reales de la base de datos
        self.load_teachers_from_database()
        
    def show_configuracion_content(self):
        """Mostrar contenido de Configuración"""
        # Limpiar el contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Crear la página de gestión de usuarios con el mismo diseño que las otras páginas
        self.setup_users_page()
        
    def logout(self):
        """Cerrar sesión"""
        result = messagebox.askyesno("Cerrar Sesión", "¿Está seguro de cerrar sesión?")
        if result:
            # Cerrar la ventana actual
            self.parent.destroy()
            
            # Crear nueva ventana de login
            import customtkinter as ctk
            from .login_page import LoginPage
            
            login_window = ctk.CTk()
            login_window.title("Academia Bíblica - Login")
            login_window.geometry("800x600")
            login_window.resizable(True, True)
            
            # Centrar la ventana
            login_window.update_idletasks()
            x = (login_window.winfo_screenwidth() // 2) - (800 // 2)
            y = (login_window.winfo_screenheight() // 2) - (600 // 2)
            login_window.geometry(f"800x600+{x}+{y}")
            
            # Crear la página de login
            login_page = LoginPage(login_window)
            
            # Ejecutar la ventana de login
            login_window.mainloop()
    
    def setup_users_page(self):
        """Configurar la interfaz de gestión de usuarios (como en la imagen)"""
        # Título principal
        title = ctk.CTkLabel(
            self.content_frame,
            text="CONFIGURACIÓN",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(20, 30))
        
        # Sección de usuarios
        self.create_users_section()
        
        # Sección de opciones adicionales
        self.create_additional_options_section()
    
    
    def create_users_section(self):
        """Crear sección de gestión de usuarios (como en la imagen)"""
        # Título de la sección
        users_title = ctk.CTkLabel(
            self.content_frame,
            text="Usuarios",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f538d"
        )
        users_title.pack(pady=(0, 15), anchor="w")
        
        # Frame para filtros
        filters_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filters_frame.pack(fill="x", pady=(0, 15))
        
        # Campo de búsqueda por usuario
        user_label = ctk.CTkLabel(filters_frame, text="Usuario:", font=ctk.CTkFont(size=14))
        user_label.pack(side="left", padx=(0, 10))
        
        self.user_search_var = ctk.StringVar()
        self.user_search_var.trace('w', self.filter_users)
        user_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="Buscar usuario...",
            textvariable=self.user_search_var,
            width=200
        )
        user_entry.pack(side="left", padx=(0, 20))
        
        # Filtro por rol
        role_label = ctk.CTkLabel(filters_frame, text="Rol:", font=ctk.CTkFont(size=14))
        role_label.pack(side="left", padx=(0, 10))
        
        self.role_filter_var = ctk.StringVar()
        self.role_filter_var.set("Todos")
        self.role_filter_var.trace('w', self.filter_users)
        role_combo = ctk.CTkComboBox(
            filters_frame,
            values=["Todos", "Administrador", "Usuario"],
            variable=self.role_filter_var,
            width=150
        )
        role_combo.pack(side="left")
        
        # Frame para la tabla de usuarios
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Crear tabla de usuarios
        self.create_users_table(table_frame)
        
        # Frame para botones de acción
        action_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(10, 15))
        
        # Botón agregar usuario
        self.add_user_btn = ctk.CTkButton(
            action_frame,
            text="Nuevo Usuario",
            width=150,
            height=40,
            command=self.show_create_user_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.add_user_btn.pack(side="left", padx=(0, 10))
        
        # Botón editar usuario
        self.edit_user_btn = ctk.CTkButton(
            action_frame,
            text="Editar",
            width=120,
            height=40,
            command=self.show_edit_user_dialog,
            fg_color="#ffc107",
            hover_color="#e0a800",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.edit_user_btn.pack(side="left", padx=(0, 10))
        
        # Botón eliminar usuario
        self.delete_user_btn = ctk.CTkButton(
            action_frame,
            text="Eliminar",
            width=120,
            height=40,
            command=self.delete_selected_user,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.delete_user_btn.pack(side="left", padx=(0, 10))
        
        # Botón refrescar
        self.refresh_users_btn = ctk.CTkButton(
            action_frame,
            text="Refrescar",
            width=120,
            height=40,
            command=self.load_users,
            fg_color="#17a2b8",
            hover_color="#138496",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.refresh_users_btn.pack(side="right")
        
        # Frame para paginación
        pagination_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        pagination_frame.pack(fill="x", pady=(0, 15))
        
        # Información de paginación
        self.pagination_label = ctk.CTkLabel(
            pagination_frame,
            text="1/10 Páginas",
            font=ctk.CTkFont(size=12)
        )
        self.pagination_label.pack(side="left")
        
        # Botones de paginación
        prev_btn = ctk.CTkButton(
            pagination_frame,
            text="Anterior",
            width=80,
            height=30,
            command=self.previous_users_page,
            font=ctk.CTkFont(size=12)
        )
        prev_btn.pack(side="right", padx=(5, 0))
        
        next_btn = ctk.CTkButton(
            pagination_frame,
            text="Siguiente",
            width=80,
            height=30,
            command=self.next_users_page,
            font=ctk.CTkFont(size=12)
        )
        next_btn.pack(side="right")
        
        # Cargar usuarios
        self.load_users()
    
    def create_users_table(self, parent):
        """Crear tabla de usuarios (como en la imagen)"""
        # Configurar el Treeview
        columns = ("Usuario", "Rol", "Acciones")
        self.users_tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)
        
        # Configurar encabezados
        self.users_tree.heading("Usuario", text="Usuario")
        self.users_tree.heading("Rol", text="Rol")
        self.users_tree.heading("Acciones", text="Acciones")
        
        # Configurar ancho de columnas
        self.users_tree.column("Usuario", width=200, anchor="center")
        self.users_tree.column("Rol", width=150, anchor="center")
        self.users_tree.column("Acciones", width=120, anchor="center")
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.users_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar eventos
        self.users_tree.bind("<Double-1>", self.show_edit_user_dialog)
        self.users_tree.bind("<Button-3>", self.show_context_menu)  # Click derecho
    
    def create_additional_options_section(self):
        """Crear sección de opciones adicionales (como en la imagen)"""
        # Título de la sección
        options_title = ctk.CTkLabel(
            self.content_frame,
            text="Opciones Adicionales",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f538d"
        )
        options_title.pack(pady=(20, 15), anchor="w")
        
        # Frame para botones de opciones
        options_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        options_frame.pack(fill="x")
        
        # Botón Importar BD
        import_btn = ctk.CTkButton(
            options_frame,
            text="Importar BD",
            width=150,
            height=40,
            command=self.import_database,
            fg_color="#17a2b8",
            hover_color="#138496",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        import_btn.pack(side="left", padx=(0, 10))
        
        # Botón Exportar BD
        export_btn = ctk.CTkButton(
            options_frame,
            text="Exportar BD",
            width=150,
            height=40,
            command=self.export_database,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        # Botón Exportar JSON
        export_json_btn = ctk.CTkButton(
            options_frame,
            text="Exportar JSON",
            width=150,
            height=40,
            command=self.export_json,
            fg_color="#ffc107",
            hover_color="#e0a800",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        export_json_btn.pack(side="left")
    
    def load_users(self):
        """Cargar usuarios desde la base de datos"""
        try:
            # Inicializar repositorio de usuarios
            self.user_repo = UserRepository()
            
            # Obtener todos los usuarios
            self.all_users = self.user_repo.get_all_users()
            self.filtered_users = self.all_users.copy()
            self.current_page = 1
            self.users_per_page = 10
            
            # Actualizar tabla
            self.update_users_table()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {e}")
    
    def filter_users(self, *args):
        """Filtrar usuarios según los criterios de búsqueda"""
        try:
            search_text = self.user_search_var.get().lower()
            role_filter = self.role_filter_var.get()
            
            self.filtered_users = []
            
            for user in self.all_users:
                # Filtro por texto de búsqueda
                if search_text and search_text not in user.get("user", "").lower():
                    continue
                
                # Filtro por rol
                if role_filter != "Todos" and user.get("role", "") != role_filter:
                    continue
                
                self.filtered_users.append(user)
            
            self.current_page = 1
            self.update_users_table()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar usuarios: {e}")
    
    def update_users_table(self):
        """Actualizar la tabla de usuarios"""
        try:
            # Limpiar tabla
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Calcular paginación
            total_pages = max(1, (len(self.filtered_users) + self.users_per_page - 1) // self.users_per_page)
            start_idx = (self.current_page - 1) * self.users_per_page
            end_idx = min(start_idx + self.users_per_page, len(self.filtered_users))
            
            # Actualizar etiqueta de paginación
            self.pagination_label.configure(text=f"{self.current_page}/{total_pages} Páginas")
            
            # Agregar usuarios a la tabla
            for i in range(start_idx, end_idx):
                user = self.filtered_users[i]
                username = user.get("user", "")
                role = user.get("role", "")
                
                # Insertar fila
                self.users_tree.insert("", "end", values=(username, role, "Editar | Eliminar"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar tabla: {e}")
    
    def previous_users_page(self):
        """Ir a la página anterior de usuarios"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_users_table()
    
    def next_users_page(self):
        """Ir a la página siguiente de usuarios"""
        total_pages = max(1, (len(self.filtered_users) + self.users_per_page - 1) // self.users_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_users_table()
    
    
    def show_edit_user_dialog(self, event=None):
        """Mostrar diálogo para editar usuario"""
        try:
            # Obtener usuario seleccionado
            selection = self.users_tree.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Por favor seleccione un usuario para editar.")
                return
            
            item = selection[0]
            username = self.users_tree.item(item, "values")[0]  # Usuario está en la columna 0
            
            # Verificar que no sea el usuario admin por defecto
            if username == "admin":
                messagebox.showwarning("Advertencia", "No se puede editar el usuario administrador por defecto.")
                return
            
            # Obtener datos del usuario
            user_data = self.user_repo.get_user_by_username(username)
            if not user_data:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return
            
            # Mostrar diálogo de edición
            self.show_edit_user_form(user_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al editar usuario: {e}")
    
    def delete_selected_user(self):
        """Eliminar usuario seleccionado"""
        try:
            # Obtener usuario seleccionado
            selection = self.users_tree.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Por favor seleccione un usuario para eliminar.")
                return
            
            item = selection[0]
            username = self.users_tree.item(item, "values")[0]  # Usuario está en la columna 0
            
            # Verificar que no sea el usuario admin por defecto
            if username == "admin":
                messagebox.showwarning("Advertencia", "No se puede eliminar el usuario administrador por defecto.")
                return
            
            # Verificar que no sea el usuario actual
            if username == self.current_user.get("user", ""):
                messagebox.showwarning("Advertencia", "No puede eliminar su propio usuario.")
                return
            
            # Eliminar usuario
            self.delete_user(username)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar usuario: {e}")
    
    def show_change_password_dialog(self, username):
        """Mostrar diálogo para cambiar contraseña"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Cambiar Contraseña")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Hacer modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Título
        title = ctk.CTkLabel(
            dialog,
            text=f"Cambiar Contraseña de {username}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=20)
        
        # Frame para campos
        fields_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True, padx=20)
        
        # Nueva contraseña
        new_pass_label = ctk.CTkLabel(fields_frame, text="Nueva Contraseña:", font=ctk.CTkFont(size=14))
        new_pass_label.pack(pady=(0, 5), anchor="w")
        
        new_pass_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese nueva contraseña",
            show="*",
            width=300,
            height=35
        )
        new_pass_entry.pack(pady=(0, 15))
        
        # Confirmar contraseña
        confirm_pass_label = ctk.CTkLabel(fields_frame, text="Confirmar Contraseña:", font=ctk.CTkFont(size=14))
        confirm_pass_label.pack(pady=(0, 5), anchor="w")
        
        confirm_pass_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Confirme la nueva contraseña",
            show="*",
            width=300,
            height=35
        )
        confirm_pass_entry.pack(pady=(0, 20))
        
        # Frame para botones
        buttons_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        def save_password():
            new_pass = new_pass_entry.get()
            confirm_pass = confirm_pass_entry.get()
            
            if not new_pass or not confirm_pass:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return
            
            if new_pass != confirm_pass:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return
            
            if len(new_pass) < 4:
                messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
                return
            
            try:
                # Actualizar contraseña
                rows_affected = self.user_repo.update_user_password(username, new_pass)
                
                if rows_affected > 0:
                    messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la contraseña.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar contraseña: {e}")
        
        def cancel():
            dialog.destroy()
        
        # Botones
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Guardar",
            width=120,
            height=35,
            command=save_password,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=120,
            height=35,
            command=cancel,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        cancel_btn.pack(side="left")
        
        # Enfocar en el primer campo
        new_pass_entry.focus()
    
    def show_edit_user_form(self, user_data):
        """Mostrar formulario para editar usuario"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Editar Usuario")
        dialog.geometry("450x500")
        dialog.resizable(False, False)
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"450x500+{x}+{y}")
        
        # Hacer modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Título
        title = ctk.CTkLabel(
            dialog,
            text="Editar Usuario",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=20)
        
        # Frame para campos
        fields_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True, padx=20)
        
        # Nombre de usuario
        user_label = ctk.CTkLabel(fields_frame, text="Nombre de Usuario:", font=ctk.CTkFont(size=14))
        user_label.pack(pady=(0, 5), anchor="w")
        
        user_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese nombre de usuario",
            width=350,
            height=35
        )
        user_entry.insert(0, user_data.get("user", ""))
        user_entry.pack(pady=(0, 15))
        
        # Rol
        role_label = ctk.CTkLabel(fields_frame, text="Rol:", font=ctk.CTkFont(size=14))
        role_label.pack(pady=(0, 5), anchor="w")
        
        role_var = ctk.StringVar()
        role_var.set(user_data.get("role", "Usuario"))
        role_combo = ctk.CTkComboBox(
            fields_frame,
            values=["Usuario", "Administrador"],
            variable=role_var,
            width=350,
            height=35
        )
        role_combo.pack(pady=(0, 15))
        
        # Separador
        separator = ctk.CTkFrame(fields_frame, height=2, fg_color="#cccccc")
        separator.pack(fill="x", pady=10)
        
        # Título para cambio de contraseña
        pass_title = ctk.CTkLabel(
            fields_frame,
            text="Cambiar Contraseña (opcional):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#666666"
        )
        pass_title.pack(pady=(10, 5), anchor="w")
        
        # Nueva contraseña
        new_pass_label = ctk.CTkLabel(fields_frame, text="Nueva Contraseña:", font=ctk.CTkFont(size=12))
        new_pass_label.pack(pady=(0, 5), anchor="w")
        
        new_pass_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Dejar vacío para no cambiar",
            show="*",
            width=350,
            height=35
        )
        new_pass_entry.pack(pady=(0, 10))
        
        # Confirmar contraseña
        confirm_pass_label = ctk.CTkLabel(fields_frame, text="Confirmar Contraseña:", font=ctk.CTkFont(size=12))
        confirm_pass_label.pack(pady=(0, 5), anchor="w")
        
        confirm_pass_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Confirme la nueva contraseña",
            show="*",
            width=350,
            height=35
        )
        confirm_pass_entry.pack(pady=(0, 20))
        
        # Frame para botones
        buttons_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        def save_changes():
            username = user_entry.get().strip()
            role = role_var.get()
            new_password = new_pass_entry.get()
            confirm_password = confirm_pass_entry.get()
            
            # Validaciones
            if not username:
                messagebox.showerror("Error", "El nombre de usuario es requerido.")
                return
            
            if len(username) < 3:
                messagebox.showerror("Error", "El nombre de usuario debe tener al menos 3 caracteres.")
                return
            
            # Validar contraseña si se proporciona
            if new_password:
                if new_password != confirm_password:
                    messagebox.showerror("Error", "Las contraseñas no coinciden.")
                    return
                
                if len(new_password) < 4:
                    messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
                    return
            
            try:
                # Verificar si el nombre de usuario ya existe (si cambió)
                original_username = user_data.get("user", "")
                if username != original_username and self.user_repo.user_exists(username):
                    messagebox.showerror("Error", "El nombre de usuario ya existe.")
                    return
                
                # Actualizar rol si cambió
                if role != user_data.get("role", ""):
                    self.user_repo.update_user_role(original_username, role)
                
                # Actualizar contraseña si se proporcionó
                if new_password:
                    print(f"Actualizando contraseña para usuario: {original_username}")
                    self.user_repo.update_user_password(original_username, new_password)
                    print("Contraseña actualizada y encriptada correctamente")
                
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
                dialog.destroy()
                
                # Recargar usuarios
                self.load_users()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar usuario: {e}")
        
        def cancel():
            dialog.destroy()
        
        # Botones
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Guardar Cambios",
            width=150,
            height=35,
            command=save_changes,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=150,
            height=35,
            command=cancel,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        cancel_btn.pack(side="left")
        
        # Enfocar en el primer campo
        user_entry.focus()
    
    def show_context_menu(self, event):
        """Mostrar menú contextual para acciones de usuario"""
        try:
            # Obtener elemento seleccionado
            item = self.users_tree.identify_row(event.y)
            if not item:
                return
            
            # Seleccionar el elemento
            self.users_tree.selection_set(item)
            username = self.users_tree.item(item, "values")[0]  # Usuario está en la columna 0
            
            # Crear menú contextual
            context_menu = tk.Menu(self.parent, tearoff=0)
            context_menu.add_command(label="Editar Usuario",
                                   command=self.show_edit_user_dialog)
            context_menu.add_command(label="Eliminar Usuario",
                                   command=lambda: self.delete_user(username))
            
            # Mostrar menú
            context_menu.tk_popup(event.x_root, event.y_root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar menú: {e}")
    
    def show_create_user_dialog(self):
        """Mostrar diálogo para crear nuevo usuario"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Crear Nuevo Usuario")
        dialog.geometry("450x500")
        dialog.resizable(False, False)
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"450x500+{x}+{y}")
        
        # Hacer modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Título
        title = ctk.CTkLabel(
            dialog,
            text="Crear Nuevo Usuario",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=20)
        
        # Frame para campos
        fields_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True, padx=20)
        
        # Nombre de usuario
        user_label = ctk.CTkLabel(fields_frame, text="Nombre de Usuario:", font=ctk.CTkFont(size=14))
        user_label.pack(pady=(0, 5), anchor="w")
        
        user_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese nombre de usuario",
            width=350,
            height=35
        )
        user_entry.pack(pady=(0, 15))
        
        # Rol
        role_label = ctk.CTkLabel(fields_frame, text="Rol:", font=ctk.CTkFont(size=14))
        role_label.pack(pady=(0, 5), anchor="w")
        
        role_var = ctk.StringVar()
        role_var.set("Usuario")
        role_combo = ctk.CTkComboBox(
            fields_frame,
            values=["Usuario", "Administrador"],
            variable=role_var,
            width=350,
            height=35
        )
        role_combo.pack(pady=(0, 15))
        
        # Contraseña
        pass_label = ctk.CTkLabel(fields_frame, text="Contraseña:", font=ctk.CTkFont(size=14))
        pass_label.pack(pady=(0, 5), anchor="w")
        
        pass_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese contraseña",
            show="*",
            width=350,
            height=35
        )
        pass_entry.pack(pady=(0, 15))
        
        # Confirmar contraseña
        confirm_label = ctk.CTkLabel(fields_frame, text="Confirmar Contraseña:", font=ctk.CTkFont(size=14))
        confirm_label.pack(pady=(0, 5), anchor="w")
        
        confirm_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Confirme la contraseña",
            show="*",
            width=350,
            height=35
        )
        confirm_entry.pack(pady=(0, 20))
        
        # Frame para botones (separado del fields_frame)
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 20), padx=20)
        
        def create_user():
            username = user_entry.get().strip()
            role = role_var.get()
            password = pass_entry.get()
            confirm_password = confirm_entry.get()
            
            # Validaciones
            if not username or not role or not password or not confirm_password:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return
            
            if len(username) < 3:
                messagebox.showerror("Error", "El nombre de usuario debe tener al menos 3 caracteres.")
                return
            
            if password != confirm_password:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return
            
            if len(password) < 4:
                messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
                return
            
            try:
                # Verificar si el usuario ya existe
                if self.user_repo.user_exists(username):
                    messagebox.showerror("Error", "El nombre de usuario ya existe.")
                    return
                
                # Crear usuario con encriptación de contraseña
                print(f"Creando usuario: {username} con rol: {role}")
                self.user_repo.create_user(username, role, password)
                print("Usuario creado exitosamente con contraseña encriptada")
                
                messagebox.showinfo("Éxito", "Usuario creado correctamente.\nLa contraseña ha sido encriptada de forma segura.")
                dialog.destroy()
                
                # Recargar usuarios
                self.load_users()
                
            except Exception as e:
                print(f"Error al crear usuario: {e}")
                messagebox.showerror("Error", f"Error al crear usuario: {e}")
        
        def cancel():
            dialog.destroy()
        
        # Botones
        create_btn = ctk.CTkButton(
            buttons_frame,
            text="CREAR USUARIO",
            width=180,
            height=45,
            command=create_user,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        create_btn.pack(side="left", padx=(0, 15))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="CANCELAR",
            width=180,
            height=45,
            command=cancel,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cancel_btn.pack(side="left")
        
        # Enfocar en el primer campo
        user_entry.focus()
    
    def delete_user(self, username):
        """Eliminar usuario"""
        try:
            # Verificar que no sea el usuario admin por defecto
            if username == "admin":
                messagebox.showwarning("Advertencia", "No se puede eliminar el usuario administrador por defecto.")
                return
            
            # Verificar que no sea el usuario actual
            if username == self.current_user.get("user", ""):
                messagebox.showwarning("Advertencia", "No puede eliminar su propio usuario.")
                return
            
            # Confirmar eliminación
            result = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar el usuario '{username}'?\n\nEsta acción no se puede deshacer."
            )
            
            if result:
                # Eliminar usuario
                rows_affected = self.user_repo.delete_user(username)
                
                if rows_affected > 0:
                    messagebox.showinfo("Éxito", f"Usuario '{username}' eliminado correctamente.")
                    # Recargar usuarios
                    self.load_users()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el usuario.")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar usuario: {e}")
    
    def import_database(self):
        """Importar base de datos"""
        messagebox.showinfo("Importar BD", "Funcionalidad de importación en desarrollo.")
    
    def export_database(self):
        """Exportar base de datos"""
        messagebox.showinfo("Exportar BD", "Funcionalidad de exportación en desarrollo.")
    
    def export_json(self):
        """Exportar JSON"""
        messagebox.showinfo("Exportar JSON", "Funcionalidad de exportación JSON en desarrollo.")
    
    
    def create_teams_table(self, parent):
        """Crear tabla de equipos con paginación"""
        # Frame para la tabla
        self.teams_table_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.teams_table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Headers de la tabla
        headers_frame = ctk.CTkFrame(self.teams_table_container, fg_color="#1f538d", height=50)
        headers_frame.pack(fill="x", pady=(0, 5))
        headers_frame.pack_propagate(False)
        
        # Headers
        headers = ["ID", "Nombre", "Género", "Edad Mínima", "Edad Máxima", "Miembros", "Acciones"]
        header_widths = [50, 200, 100, 100, 100, 80, 120]
        
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
                width=width
            )
            header_label.place(x=sum(header_widths[:i]) + i*5, y=15)
        
        # Frame para las filas de datos
        self.teams_rows_frame = ctk.CTkScrollableFrame(
            self.teams_table_container,
            fg_color="#f8f9fa",
            height=450
        )
        self.teams_rows_frame.pack(fill="both", expand=True)
        
        # Frame para paginación
        pagination_frame = ctk.CTkFrame(self.teams_table_container, fg_color="transparent")
        pagination_frame.pack(fill="x", pady=(10, 0))
        
        # Información de paginación
        self.teams_pagination_info = ctk.CTkLabel(
            pagination_frame,
            text="Mostrando 0 de 0 equipos",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        self.teams_pagination_info.pack(side="left")
        
        # Botones de paginación
        pagination_buttons_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        pagination_buttons_frame.pack(side="right")
        
        self.teams_prev_page_btn = ctk.CTkButton(
            pagination_buttons_frame,
            text="Anterior",
            width=100,
            height=30,
            command=self.teams_prev_page,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.teams_prev_page_btn.pack(side="left", padx=(0, 5))
        
        self.teams_next_page_btn = ctk.CTkButton(
            pagination_buttons_frame,
            text="Siguiente",
            width=100,
            height=30,
            command=self.teams_next_page,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.teams_next_page_btn.pack(side="left")
        
        # Variables de paginación
        self.teams_current_page = 1
        self.teams_items_per_page = 10
        self.teams_total_items = 0
        self.filtered_teams = []
        
    def load_teams_from_database(self):
        """Cargar equipos desde la base de datos"""
        try:
            from control.bd.db_connection import Connection
            from control.team_repository import TeamRepository
            
            conn = Connection.connect()
            if conn:
                team_repo = TeamRepository(conn)
                team_repo.create_table()  # Asegurar que la tabla existe
                
                # Obtener todos los equipos
                teams = team_repo.get_all_teams()
                
                # Convertir a formato para la tabla
                self.test_teams = []
                for team in teams:
                    self.test_teams.append({
                        "id": team.id,
                        "name": team.name,
                        "gender": team.gender,
                        "age_start": team.age_start,
                        "age_end": team.age_end,
                        "members": 0  # Por ahora, se puede implementar después
                    })
                
                conn.close()
                
                # Actualizar tabla
                self.update_teams_table()
                
                print(f"Cargados {len(self.test_teams)} equipos desde la base de datos")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al cargar equipos: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar equipos: {str(e)}")
        
    def update_teams_table(self):
        """Actualizar tabla de equipos"""
        # Limpiar filas existentes
        for widget in self.teams_rows_frame.winfo_children():
            widget.destroy()
        
        # Calcular paginación
        start_idx = (self.teams_current_page - 1) * self.teams_items_per_page
        end_idx = start_idx + self.teams_items_per_page
        
        # Obtener equipos para la página actual
        teams_to_show = self.test_teams[start_idx:end_idx]
        
        # Agregar equipos a la tabla
        for team in teams_to_show:
            self.create_team_row(team)
        
        # Actualizar información de paginación
        self.teams_total_items = len(self.test_teams)
        total_pages = (self.teams_total_items + self.teams_items_per_page - 1) // self.teams_items_per_page
        self.teams_pagination_info.configure(text=f"Mostrando {len(teams_to_show)} de {self.teams_total_items} equipos")
        
        # Actualizar botones de paginación
        self.teams_prev_page_btn.configure(state="normal" if self.teams_current_page > 1 else "disabled")
        self.teams_next_page_btn.configure(state="normal" if self.teams_current_page < total_pages else "disabled")
        
    def create_team_row(self, team):
        """Crear fila de equipo en la tabla"""
        row_frame = ctk.CTkFrame(self.teams_rows_frame, fg_color="white", height=40)
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)
        
        # Datos del equipo
        team_data = [
            str(team["id"]),
            team["name"],
            team["gender"],
            str(team["age_start"]),
            str(team["age_end"]),
            str(team["members"])
        ]
        
        # Mostrar datos
        for i, data in enumerate(team_data):
            data_label = ctk.CTkLabel(
                row_frame,
                text=data,
                font=ctk.CTkFont(size=12),
                text_color="#333333",
                width=50 if i == 0 else 200 if i == 1 else 100 if i == 2 else 100 if i == 3 else 100 if i == 4 else 80
            )
            data_label.place(x=sum([50, 200, 100, 100, 100, 80][:i]) + i*5, y=10)
            
            # Botones de acción
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.place(x=sum([50, 200, 100, 100, 100, 80]) + 6*5, y=5)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Editar",
            width=56,
            height=28,
            font=ctk.CTkFont(size=11),
            command=lambda t=team: self.edit_team(t),
            fg_color="#ffc107",
            hover_color="#e0a800"
        )
        edit_btn.pack(side="left", padx=(0, 4))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Eliminar",
            width=56,
            height=28,
            font=ctk.CTkFont(size=11),
            command=lambda t=team: self.delete_team(t),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side="left")
        
    def edit_team(self, team):
        """Editar equipo"""
        self.show_edit_team_dialog(team)
        
    def delete_team(self, team):
        """Eliminar equipo"""
        result = messagebox.askyesno("Confirmar", f"¿Eliminar equipo {team['name']}?")
        if result:
            try:
                from control.bd.db_connection import Connection
                from control.team_repository import TeamRepository
                
                conn = Connection.connect()
                if conn:
                    team_repo = TeamRepository(conn)
                    success = team_repo.delete_team(team['id'])
                    
                    if success:
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Equipo '{team['name']}' eliminado correctamente")
                        self.load_teams_from_database()  # Recargar datos
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el equipo")
                    
                    conn.close()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al eliminar equipo: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar equipo: {str(e)}")
            
    def show_add_team_dialog(self):
        """Mostrar diálogo para agregar equipo"""
        self.show_team_dialog()
        
    def show_edit_team_dialog(self, team):
        """Mostrar diálogo para editar equipo"""
        self.show_team_dialog(team)
        
    def show_team_dialog(self, team=None):
        """Mostrar diálogo para agregar/editar equipo"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Agregar Equipo" if not team else "Editar Equipo")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Centrar la ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Agregar Equipo" if not team else "Editar Equipo",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Campos del formulario
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=30, pady=30)
        
        # Nombre del equipo
        name_label = ctk.CTkLabel(
            fields_frame,
            text="Nombre del Equipo:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        name_label.pack(anchor="w", pady=(0, 8))
        
        name_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese el nombre del equipo (ej: Jóvenes de Cristo)",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        name_entry.pack(fill="x", pady=(0, 25))
        
        # Frame para edades
        age_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        age_frame.pack(fill="x", pady=(0, 25))
        
        # Edad de inicio
        age_start_label = ctk.CTkLabel(
            age_frame,
            text="Edad de Inicio:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        age_start_label.pack(anchor="w", pady=(0, 8))
        
        age_start_entry = ctk.CTkEntry(
            age_frame,
            placeholder_text="Ej: 15",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        age_start_entry.pack(fill="x", pady=(0, 20))
        
        # Edad de fin
        age_end_label = ctk.CTkLabel(
            age_frame,
            text="Edad de Fin:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        age_end_label.pack(anchor="w", pady=(0, 8))
        
        age_end_entry = ctk.CTkEntry(
            age_frame,
            placeholder_text="Ej: 25",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        age_end_entry.pack(fill="x", pady=(0, 25))
        
        # Género
        gender_label = ctk.CTkLabel(
            fields_frame,
            text="Género:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        gender_label.pack(anchor="w", pady=(0, 8))
        
        gender_var = ctk.StringVar(value="Mixto")
        gender_combo = ctk.CTkComboBox(
            fields_frame,
            values=["Mixto", "Masculino", "Femenino"],
            height=45,
            font=ctk.CTkFont(size=14),
            variable=gender_var,
            border_width=2,
            border_color="#1f538d",
            button_color="#1f538d"
        )
        gender_combo.pack(fill="x", pady=(0, 30))
        
        # Llenar campos si es edición
        if team:
            name_entry.insert(0, team['name'])
            age_start_entry.insert(0, str(team['age_start']))
            age_end_entry.insert(0, str(team['age_end']))
            gender_var.set(team['gender'])
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        def save_team():
            """Guardar equipo"""
            name = name_entry.get().strip()
            age_start = age_start_entry.get().strip()
            age_end = age_end_entry.get().strip()
            gender = gender_var.get()
            
            # Validaciones
            if not name:
                messagebox.showerror("Error", "El nombre del equipo es obligatorio")
                return
            
            if not age_start or not age_start.isdigit():
                messagebox.showerror("Error", "La edad de inicio debe ser un número válido")
                return
            
            if not age_end or not age_end.isdigit():
                messagebox.showerror("Error", "La edad de fin debe ser un número válido")
                return
            
            age_start = int(age_start)
            age_end = int(age_end)
            
            if age_start >= age_end:
                messagebox.showerror("Error", "La edad de inicio debe ser menor que la edad de fin")
                return
            
            try:
                from control.bd.db_connection import Connection
                from control.team_repository import TeamRepository
                from model.team import Team
                
                conn = Connection.connect()
                if conn:
                    team_repo = TeamRepository(conn)
                    
                    if team:  # Editar
                        # Crear objeto Team con el ID existente
                        team_obj = Team(
                            id=team['id'],
                            name=name,
                            age_start=age_start,
                            age_end=age_end,
                            gender=gender
                        )
                        success = team_repo.update_team(team_obj)
                        if success:
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Equipo '{name}' actualizado correctamente")
                        else:
                            messagebox.showerror("Error", "No se pudo actualizar el equipo")
                            return
                    else:  # Agregar
                        # Crear objeto Team sin ID
                        team_obj = Team(
                            name=name,
                            age_start=age_start,
                            age_end=age_end,
                            gender=gender
                        )
                        created_team = team_repo.create_team(team_obj)
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Equipo '{name}' agregado correctamente")
                    
                    conn.close()
                    dialog.destroy()
                    self.load_teams_from_database()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al guardar equipo: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar equipo: {str(e)}")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Guardar Equipo",
            width=180,
            height=50,
            command=save_team,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            border_width=2,
            border_color="#1e7e34"
        )
        save_btn.pack(side="right", padx=(15, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=150,
            height=50,
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            border_width=2,
            border_color="#5a6268"
        )
        cancel_btn.pack(side="right")
        
    def filter_teams(self):
        """Filtrar equipos"""
        try:
            from control.bd.db_connection import Connection
            from control.team_repository import TeamRepository
            
            conn = Connection.connect()
            if conn:
                team_repo = TeamRepository(conn)
                
                # Obtener filtros
                name_filter = self.team_name_filter.get().strip()
                gender_filter = self.team_gender_filter.get()
                min_age = self.team_min_age_filter.get().strip()
                max_age = self.team_max_age_filter.get().strip()
                
                # Aplicar filtros
                teams = team_repo.get_all_teams()
                filtered_teams = []
                
                for team in teams:
                    # Filtro por nombre
                    if name_filter and name_filter.lower() not in team.name.lower():
                        continue
                    
                    # Filtro por género
                    if gender_filter != "Todos" and team.gender != gender_filter:
                        continue
                    
                    # Filtro por edad mínima
                    if min_age and min_age.isdigit():
                        if team.age_start < int(min_age):
                            continue
                    
                    # Filtro por edad máxima
                    if max_age and max_age.isdigit():
                        if team.age_end > int(max_age):
                            continue
                    
                    filtered_teams.append(team)
                
                # Convertir a formato para la tabla
                self.test_teams = []
                for team in filtered_teams:
                    self.test_teams.append({
                        "id": team.id,
                        "name": team.name,
                        "gender": team.gender,
                        "age_start": team.age_start,
                        "age_end": team.age_end,
                        "members": 0
                    })
                
                conn.close()
                
                # Actualizar tabla
                self.update_teams_table()
                
                print(f"Filtrados {len(self.test_teams)} equipos")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al filtrar equipos: {str(e)}")
            messagebox.showerror("Error", f"Error al filtrar equipos: {str(e)}")
        
    def clear_team_filters(self):
        """Limpiar filtros de equipos"""
        self.team_name_filter.delete(0, "end")
        self.team_gender_filter.set("Todos")
        self.team_min_age_filter.delete(0, "end")
        self.team_max_age_filter.delete(0, "end")
        
        # Recargar todos los datos
        self.load_teams_from_database()
        
    def teams_prev_page(self):
        """Página anterior de equipos"""
        if self.teams_current_page > 1:
            self.teams_current_page -= 1
            self.update_teams_table()
            
    def teams_next_page(self):
        """Página siguiente de equipos"""
        total_pages = (self.teams_total_items + self.teams_items_per_page - 1) // self.teams_items_per_page
        if self.teams_current_page < total_pages:
            self.teams_current_page += 1
            self.update_teams_table()
    
    # Funciones para Cursos
    def create_courses_table(self, parent):
        """Crear tabla de cursos con paginación"""
        # Frame para la tabla
        self.courses_table_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.courses_table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Headers de la tabla
        headers_frame = ctk.CTkFrame(self.courses_table_container, fg_color="#1f538d", height=50)
        headers_frame.pack(fill="x", pady=(0, 5))
        headers_frame.pack_propagate(False)
        
        # Headers
        headers = ["ID", "Nombre", "Nivel", "Acciones"]
        header_widths = [50, 300, 100, 120]
        
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
                width=width
            )
            header_label.place(x=sum(header_widths[:i]) + i*5, y=15)
        
        # Frame para las filas de datos
        self.courses_rows_frame = ctk.CTkScrollableFrame(
            self.courses_table_container,
            fg_color="#f8f9fa",
            height=450
        )
        self.courses_rows_frame.pack(fill="both", expand=True)
        
        # Frame para paginación
        pagination_frame = ctk.CTkFrame(self.courses_table_container, fg_color="transparent")
        pagination_frame.pack(fill="x", pady=(10, 0))
        
        # Información de paginación
        self.courses_pagination_info = ctk.CTkLabel(
            pagination_frame,
            text="Mostrando 0 de 0 cursos",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        self.courses_pagination_info.pack(side="left")
        
        # Botones de paginación
        pagination_buttons_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        pagination_buttons_frame.pack(side="right")
        
        self.courses_prev_page_btn = ctk.CTkButton(
            pagination_buttons_frame,
            text="Anterior",
            width=100,
            height=30,
            command=self.courses_prev_page,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.courses_prev_page_btn.pack(side="left", padx=(0, 5))
        
        self.courses_next_page_btn = ctk.CTkButton(
            pagination_buttons_frame,
            text="Siguiente",
            width=100,
            height=30,
            command=self.courses_next_page,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.courses_next_page_btn.pack(side="left")
        
        # Variables de paginación
        self.courses_current_page = 1
        self.courses_items_per_page = 10
        self.courses_total_items = 0
        
    def load_courses_from_database(self):
        """Cargar cursos desde la base de datos"""
        try:
            from control.bd.db_connection import Connection
            from control.course_repository import CourseRepository
            
            conn = Connection.connect()
            if conn:
                course_repo = CourseRepository(conn)
                course_repo.create_table()  # Asegurar que la tabla existe
                
                # Obtener todos los cursos
                courses = course_repo.get_all_rows()
                
                # Convertir a formato para la tabla
                self.test_courses = []
                for course in courses:
                    self.test_courses.append({
                        "id": course["id"],
                        "name": course["name"],
                        "level": course["level"],
                        "students": 0  # Por ahora, se puede implementar después
                    })
                
                conn.close()
                
                # Actualizar tabla
                self.update_courses_table()
                
                print(f"Cargados {len(self.test_courses)} cursos desde la base de datos")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al cargar cursos: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar cursos: {str(e)}")
        
    def update_courses_table(self):
        """Actualizar tabla de cursos"""
        # Limpiar filas existentes
        for widget in self.courses_rows_frame.winfo_children():
            widget.destroy()
        
        # Calcular paginación
        start_idx = (self.courses_current_page - 1) * self.courses_items_per_page
        end_idx = start_idx + self.courses_items_per_page
        
        # Obtener cursos para la página actual
        courses_to_show = self.test_courses[start_idx:end_idx]
        
        # Agregar cursos a la tabla
        for course in courses_to_show:
            self.create_course_row(course)
        
        # Actualizar información de paginación
        self.courses_total_items = len(self.test_courses)
        total_pages = (self.courses_total_items + self.courses_items_per_page - 1) // self.courses_items_per_page
        self.courses_pagination_info.configure(text=f"Mostrando {len(courses_to_show)} de {self.courses_total_items} cursos")
        
        # Actualizar botones de paginación
        self.courses_prev_page_btn.configure(state="normal" if self.courses_current_page > 1 else "disabled")
        self.courses_next_page_btn.configure(state="normal" if self.courses_current_page < total_pages else "disabled")
        
    def create_course_row(self, course):
        """Crear fila de curso en la tabla"""
        row_frame = ctk.CTkFrame(self.courses_rows_frame, fg_color="white", height=40)
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)
        
        # Datos del curso
        course_data = [
            str(course["id"]),
            course["name"],
            str(course["level"])
        ]
        
        # Mostrar datos
        for i, data in enumerate(course_data):
            data_label = ctk.CTkLabel(
                row_frame,
                text=data,
                font=ctk.CTkFont(size=12),
                text_color="#333333",
                width=50 if i == 0 else 300 if i == 1 else 100
            )
            data_label.place(x=sum([50, 300, 100][:i]) + i*5, y=10)
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.place(x=sum([50, 300, 100]) + 3*5, y=5)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Editar",
            width=56,
            height=28,
            font=ctk.CTkFont(size=11),
            command=lambda c=course: self.edit_course(c),
            fg_color="#ffc107",
            hover_color="#e0a800"
        )
        edit_btn.pack(side="left", padx=(0, 4))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Eliminar",
            width=56,
            height=28,
            font=ctk.CTkFont(size=11),
            command=lambda c=course: self.delete_course(c),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side="left")
        
    def edit_course(self, course):
        """Editar curso"""
        self.show_edit_course_dialog(course)
        
    def delete_course(self, course):
        """Eliminar curso"""
        result = messagebox.askyesno("Confirmar", f"¿Eliminar curso {course['name']}?")
        if result:
            try:
                from control.bd.db_connection import Connection
                from control.course_repository import CourseRepository
                
                conn = Connection.connect()
                if conn:
                    course_repo = CourseRepository(conn)
                    success = course_repo.delete_row({"id": course['id']})
                    
                    if success:
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Curso '{course['name']}' eliminado correctamente")
                        self.load_courses_from_database()  # Recargar datos
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el curso")
                    
                    conn.close()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al eliminar curso: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar curso: {str(e)}")
            
    def show_add_course_dialog(self):
        """Mostrar diálogo para agregar curso"""
        self.show_course_dialog()
        
    def show_edit_course_dialog(self, course):
        """Mostrar diálogo para editar curso"""
        self.show_course_dialog(course)
        
    def show_course_dialog(self, course=None):
        """Mostrar diálogo para agregar/editar curso"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Agregar Curso" if not course else "Editar Curso")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Centrar la ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Agregar Curso" if not course else "Editar Curso",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        form_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Campos del formulario
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Nombre del curso
        name_label = ctk.CTkLabel(
            fields_frame,
            text="Nombre del Curso:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        name_label.pack(anchor="w", pady=(0, 8))
        
        name_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese el nombre del curso (ej: Teología Sistemática)",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        name_entry.pack(fill="x", pady=(0, 25))
        
        # Nivel del curso
        level_label = ctk.CTkLabel(
            fields_frame,
            text="Nivel del Curso:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        level_label.pack(anchor="w", pady=(0, 8))
        
        level_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ej: 1 (Nivel básico), 2 (Intermedio), 3 (Avanzado)",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        level_entry.pack(fill="x", pady=(0, 30))
        
        # Llenar campos si es edición
        if course:
            name_entry.insert(0, course['name'])
            level_entry.insert(0, str(course['level']))
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(30, 0))
        
        def save_course():
            """Guardar curso"""
            name = name_entry.get().strip()
            level = level_entry.get().strip()
            
            # Validaciones
            if not name:
                messagebox.showerror("Error", "El nombre del curso es obligatorio")
                return
            
            if not level or not level.isdigit():
                messagebox.showerror("Error", "El nivel debe ser un número válido")
                return
            
            level = int(level)
            
            if level < 1 or level > 10:
                messagebox.showerror("Error", "El nivel debe estar entre 1 y 10")
                return
            
            try:
                from control.bd.db_connection import Connection
                from control.course_repository import CourseRepository
                
                conn = Connection.connect()
                if conn:
                    course_repo = CourseRepository(conn)
                    
                    if course:  # Editar
                        try:
                            course_repo.update_row(
                                new_data={"name": name, "level": level},
                                conditions={"id": course['id']}
                            )
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Curso '{name}' actualizado correctamente")
                        except Exception as update_error:
                            print(f"Error al actualizar curso: {str(update_error)}")
                            messagebox.showerror("Error", f"No se pudo actualizar el curso: {str(update_error)}")
                            return
                    else:  # Agregar
                        try:
                            course_repo.insert_row({"name": name, "level": level})
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Curso '{name}' agregado correctamente")
                        except Exception as insert_error:
                            print(f"Error al insertar curso: {str(insert_error)}")
                            messagebox.showerror("Error", f"No se pudo agregar el curso: {str(insert_error)}")
                            return
                    
                    conn.close()
                    dialog.destroy()
                    self.load_courses_from_database()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al guardar curso: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar curso: {str(e)}")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Guardar Curso",
            width=180,
            height=50,
            command=save_course,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            border_width=2,
            border_color="#1e7e34"
        )
        save_btn.pack(side="right", padx=(15, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=150,
            height=50,
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            border_width=2,
            border_color="#5a6268"
        )
        cancel_btn.pack(side="right")
        
    def filter_courses(self):
        """Filtrar cursos"""
        try:
            from control.bd.db_connection import Connection
            from control.course_repository import CourseRepository
            
            conn = Connection.connect()
            if conn:
                course_repo = CourseRepository(conn)
                
                # Obtener filtros
                name_filter = self.course_name_filter.get().strip()
                level_filter = self.course_level_filter.get().strip()
                
                # Aplicar filtros
                courses = course_repo.get_all_rows()
                filtered_courses = []
                
                for course in courses:
                    # Filtro por nombre
                    if name_filter and name_filter.lower() not in course["name"].lower():
                        continue
                    
                    # Filtro por nivel
                    if level_filter and level_filter.isdigit():
                        if course["level"] != int(level_filter):
                            continue
                    
                    filtered_courses.append(course)
                
                # Convertir a formato para la tabla
                self.test_courses = []
                for course in filtered_courses:
                    self.test_courses.append({
                        "id": course["id"],
                        "name": course["name"],
                        "level": course["level"],
                        "students": 0
                    })
                
                conn.close()
                
                # Actualizar tabla
                self.update_courses_table()
                
                print(f"Filtrados {len(self.test_courses)} cursos")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al filtrar cursos: {str(e)}")
            messagebox.showerror("Error", f"Error al filtrar cursos: {str(e)}")
        
    def clear_course_filters(self):
        """Limpiar filtros de cursos"""
        self.course_name_filter.delete(0, "end")
        self.course_level_filter.delete(0, "end")
        
        # Recargar todos los datos
        self.load_courses_from_database()
        
    def courses_prev_page(self):
        """Página anterior de cursos"""
        if self.courses_current_page > 1:
            self.courses_current_page -= 1
            self.update_courses_table()
            
    def courses_next_page(self):
        """Página siguiente de cursos"""
        total_pages = (self.courses_total_items + self.courses_items_per_page - 1) // self.courses_items_per_page
        if self.courses_current_page < total_pages:
            self.courses_current_page += 1
            self.update_courses_table()
    
    # Funciones para Estudiantes
    def create_students_table(self, parent):
        """Crear tabla de estudiantes con paginación"""
        # Frame para la tabla
        self.students_table_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.students_table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Headers de la tabla
        headers_frame = ctk.CTkFrame(self.students_table_container, fg_color="#1f538d", height=50)
        headers_frame.pack(fill="x", pady=(0, 5))
        headers_frame.pack_propagate(False)
        
        # Headers
        headers = ["ID", "Nombre", "Apellido", "Teléfono", "Fecha Bautismo", "Fecha Nacimiento", "ID Equipo", "Acciones"]
        header_widths = [50, 150, 150, 120, 120, 120, 80, 120]
        
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
                width=width
            )
            header_label.place(x=sum(header_widths[:i]) + i*5, y=15)
        
        # Frame para las filas de datos
        self.students_rows_frame = ctk.CTkScrollableFrame(
            self.students_table_container,
            fg_color="#f8f9fa",
            height=450
        )
        self.students_rows_frame.pack(fill="both", expand=True)
        
        # Frame para paginación
        pagination_frame = ctk.CTkFrame(self.students_table_container, fg_color="transparent")
        pagination_frame.pack(fill="x", pady=(10, 0))
        
        # Información de paginación
        self.students_pagination_info = ctk.CTkLabel(
            pagination_frame,
            text="Mostrando 0 de 0 estudiantes",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        self.students_pagination_info.pack(side="left")
        
        # Botones de paginación
        pagination_buttons_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        pagination_buttons_frame.pack(side="right")
        
        self.students_prev_page_btn = ctk.CTkButton(
            pagination_buttons_frame,
            text="Anterior",
            width=100,
            height=30,
            command=self.students_prev_page,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.students_prev_page_btn.pack(side="left", padx=(0, 5))
        
        self.students_next_page_btn = ctk.CTkButton(
            pagination_buttons_frame,
            text="Siguiente",
            width=100,
            height=30,
            command=self.students_next_page,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.students_next_page_btn.pack(side="left")
        
        # Variables de paginación
        self.students_current_page = 1
        self.students_items_per_page = 10
        self.students_total_items = 0
        
    def load_students_from_database(self):
        """Cargar estudiantes desde la base de datos"""
        try:
            from control.bd.db_connection import Connection
            from control.student_repository import StudentRepository
            
            conn = Connection.connect()
            if conn:
                student_repo = StudentRepository(conn)
                student_repo.create_table()  # Asegurar que la tabla existe
                
                # Obtener todos los estudiantes
                students = student_repo.get_all_rows()
                
                # Convertir a formato para la tabla
                self.test_students = []
                for student in students:
                    self.test_students.append({
                        "id": student["id"],
                        "name": student["name"],
                        "lastname": student["lastname"],
                        "phone": student["phone"],
                        "date_baptism": student["date_baptism"],
                        "date_of_birth": student["date_of_birth"],
                        "id_team": student["id_team"]
                    })
                
                conn.close()
                
                # Actualizar tabla
                self.update_students_table()
                
                print(f"Cargados {len(self.test_students)} estudiantes desde la base de datos")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al cargar estudiantes: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")
        
    def update_students_table(self):
        """Actualizar tabla de estudiantes"""
        # Limpiar filas existentes
        for widget in self.students_rows_frame.winfo_children():
            widget.destroy()
        
        # Calcular paginación
        start_idx = (self.students_current_page - 1) * self.students_items_per_page
        end_idx = start_idx + self.students_items_per_page
        
        # Obtener estudiantes para la página actual
        students_to_show = self.test_students[start_idx:end_idx]
        
        # Agregar estudiantes a la tabla
        for student in students_to_show:
            self.create_student_row(student)
        
        # Actualizar información de paginación
        self.students_total_items = len(self.test_students)
        total_pages = (self.students_total_items + self.students_items_per_page - 1) // self.students_items_per_page
        self.students_pagination_info.configure(text=f"Mostrando {len(students_to_show)} de {self.students_total_items} estudiantes")
        
        # Actualizar botones de paginación
        self.students_prev_page_btn.configure(state="normal" if self.students_current_page > 1 else "disabled")
        self.students_next_page_btn.configure(state="normal" if self.students_current_page < total_pages else "disabled")
        
    def create_student_row(self, student):
        """Crear fila de estudiante en la tabla"""
        row_frame = ctk.CTkFrame(self.students_rows_frame, fg_color="white", height=40)
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)
        
        # Datos del estudiante
        student_data = [
            str(student["id"]),
            student["name"],
            student["lastname"],
            student["phone"],
            student["date_baptism"] or "N/A",
            student["date_of_birth"] or "N/A",
            str(student["id_team"])
        ]
        
        # Mostrar datos
        for i, data in enumerate(student_data):
            data_label = ctk.CTkLabel(
                row_frame,
                text=data,
                font=ctk.CTkFont(size=12),
                text_color="#333333",
                width=50 if i == 0 else 150 if i == 1 else 150 if i == 2 else 120 if i == 3 else 120 if i == 4 else 120 if i == 5 else 80
            )
            data_label.place(x=sum([50, 150, 150, 120, 120, 120, 80][:i]) + i*5, y=10)
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.place(x=sum([50, 150, 150, 120, 120, 120, 80]) + 7*5, y=5)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Editar",
            width=56,
            height=28,
            font=ctk.CTkFont(size=11),
            command=lambda s=student: self.edit_student(s),
            fg_color="#ffc107",
            hover_color="#e0a800"
        )
        edit_btn.pack(side="left", padx=(0, 4))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Eliminar",
            width=56,
            height=28,
            font=ctk.CTkFont(size=11),
            command=lambda s=student: self.delete_student(s),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side="left")
        
    def edit_student(self, student):
        """Editar estudiante"""
        self.show_edit_student_dialog(student)
        
    def delete_student(self, student):
        """Eliminar estudiante"""
        result = messagebox.askyesno("Confirmar", f"¿Eliminar estudiante {student['name']}?")
        if result:
            try:
                from control.bd.db_connection import Connection
                from control.student_repository import StudentRepository
                
                conn = Connection.connect()
                if conn:
                    student_repo = StudentRepository(conn)
                    success = student_repo.delete_row({"id": student['id']})
                    
                    if success:
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Estudiante '{student['name']}' eliminado correctamente")
                        self.load_students_from_database()  # Recargar datos
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el estudiante")
                    
                    conn.close()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al eliminar estudiante: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar estudiante: {str(e)}")
            
    def show_add_student_dialog(self):
        """Mostrar diálogo para agregar estudiante"""
        self.show_student_dialog()
        
    def show_edit_student_dialog(self, student):
        """Mostrar diálogo para editar estudiante"""
        self.show_student_dialog(student)
        
    def show_student_dialog(self, student=None):
        """Mostrar diálogo para agregar/editar estudiante"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Agregar Estudiante" if not student else "Editar Estudiante")
        dialog.geometry("700x600")
        dialog.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Centrar la ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"700x600+{x}+{y}")
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Agregar Estudiante" if not student else "Editar Estudiante",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Campos del formulario
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=30, pady=30)
        
        # Nombre del estudiante
        name_label = ctk.CTkLabel(
            fields_frame,
            text="Nombre:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        name_label.pack(anchor="w", pady=(0, 8))
        
        name_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese el nombre del estudiante",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        name_entry.pack(fill="x", pady=(0, 20))
        
        # Apellido del estudiante
        lastname_label = ctk.CTkLabel(
            fields_frame,
            text="Apellido:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        lastname_label.pack(anchor="w", pady=(0, 8))
        
        lastname_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese el apellido del estudiante",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        lastname_entry.pack(fill="x", pady=(0, 20))
        
        # Teléfono del estudiante
        phone_label = ctk.CTkLabel(
            fields_frame,
            text="Teléfono:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        phone_label.pack(anchor="w", pady=(0, 8))
        
        phone_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ej: 555-0123",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        phone_entry.pack(fill="x", pady=(0, 20))
        
        # Fecha de bautismo
        baptism_label = ctk.CTkLabel(
            fields_frame,
            text="Fecha de Bautismo:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        baptism_label.pack(anchor="w", pady=(0, 8))
        
        baptism_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="YYYY-MM-DD (ej: 2020-01-15)",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        baptism_entry.pack(fill="x", pady=(0, 20))
        
        # Fecha de nacimiento
        birth_label = ctk.CTkLabel(
            fields_frame,
            text="Fecha de Nacimiento:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        birth_label.pack(anchor="w", pady=(0, 8))
        
        birth_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="YYYY-MM-DD (ej: 1995-05-20)",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        birth_entry.pack(fill="x", pady=(0, 20))
        
        # Equipo (ComboBox con equipos disponibles)
        team_label = ctk.CTkLabel(
            fields_frame,
            text="Equipo:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        team_label.pack(anchor="w", pady=(0, 8))
        
        # Cargar equipos disponibles
        team_options = []
        try:
            from control.bd.db_connection import Connection
            from control.team_repository import TeamRepository
            
            conn = Connection.connect()
            if conn:
                team_repo = TeamRepository(conn)
                teams = team_repo.get_all_rows()
                team_options = [f"{team['id']} - {team['name']}" for team in teams]
                conn.close()
        except Exception as e:
            print(f"Error al cargar equipos: {str(e)}")
            team_options = ["No hay equipos disponibles"]
        
        team_combo = ctk.CTkComboBox(
            fields_frame,
            values=team_options,
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d",
            button_color="#1f538d"
        )
        team_combo.pack(fill="x", pady=(0, 30))
        
        # Llenar campos si es edición
        if student:
            name_entry.insert(0, student['name'])
            lastname_entry.insert(0, student['lastname'])
            phone_entry.insert(0, student['phone'])
            baptism_entry.insert(0, student['date_baptism'] or "")
            birth_entry.insert(0, student['date_of_birth'] or "")
            # Buscar el equipo correspondiente en el ComboBox
            for i, option in enumerate(team_options):
                if option.startswith(f"{student['id_team']} -"):
                    team_combo.set(option)
                    break
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(30, 0))
        
        def save_student():
            """Guardar estudiante"""
            name = name_entry.get().strip()
            lastname = lastname_entry.get().strip()
            phone = phone_entry.get().strip()
            date_baptism = baptism_entry.get().strip()
            date_of_birth = birth_entry.get().strip()
            team_selection = team_combo.get().strip()
            
            # Validaciones
            if not name:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            if not lastname:
                messagebox.showerror("Error", "El apellido es obligatorio")
                return
            
            if not phone:
                messagebox.showerror("Error", "El teléfono es obligatorio")
                return
            
            if not team_selection or team_selection == "No hay equipos disponibles":
                messagebox.showerror("Error", "Debe seleccionar un equipo")
                return
            
            # Extraer ID del equipo del formato "ID - Nombre"
            try:
                id_team = int(team_selection.split(" - ")[0])
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Formato de equipo inválido")
                return
            
            try:
                from control.bd.db_connection import Connection
                from control.student_repository import StudentRepository
                
                conn = Connection.connect()
                if conn:
                    student_repo = StudentRepository(conn)
                    
                    if student:  # Editar
                        try:
                            student_repo.update_row(
                                new_data={
                                    "name": name,
                                    "lastname": lastname,
                                    "phone": phone,
                                    "date_baptism": date_baptism if date_baptism else None,
                                    "date_of_birth": date_of_birth if date_of_birth else None,
                                    "id_team": id_team
                                },
                                conditions={"id": student['id']}
                            )
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Estudiante '{name}' actualizado correctamente")
                        except Exception as update_error:
                            print(f"Error al actualizar estudiante: {str(update_error)}")
                            messagebox.showerror("Error", f"No se pudo actualizar el estudiante: {str(update_error)}")
                            return
                    else:  # Agregar
                        try:
                            student_repo.insert_row({
                                "name": name,
                                "lastname": lastname,
                                "phone": phone,
                                "date_baptism": date_baptism if date_baptism else None,
                                "date_of_birth": date_of_birth if date_of_birth else None,
                                "id_team": id_team
                            })
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Estudiante '{name}' agregado correctamente")
                        except Exception as insert_error:
                            print(f"Error al insertar estudiante: {str(insert_error)}")
                            messagebox.showerror("Error", f"No se pudo agregar el estudiante: {str(insert_error)}")
                            return
                    
                    conn.close()
                    dialog.destroy()
                    self.load_students_from_database()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al guardar estudiante: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar estudiante: {str(e)}")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Guardar Estudiante",
            width=200,
            height=50,
            command=save_student,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            border_width=2,
            border_color="#1e7e34"
        )
        save_btn.pack(side="right", padx=(15, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=150,
            height=50,
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            border_width=2,
            border_color="#5a6268"
        )
        cancel_btn.pack(side="right")
        
    def filter_students(self):
        """Filtrar estudiantes usando BaseRepository search"""
        try:
            from control.bd.db_connection import Connection
            from control.student_repository import StudentRepository
            
            conn = Connection.connect()
            if conn:
                student_repo = StudentRepository(conn)
                
                # Obtener filtros
                name_filter = self.student_name_filter.get().strip()
                phone_filter = self.student_phone_filter.get().strip()
                team_filter = self.student_team_filter.get()
                
                # Construir diccionario de búsqueda para BaseRepository
                search_criteria = {}
                
                if name_filter:
                    # Buscar en nombre y apellido
                    search_criteria["name"] = name_filter
                    search_criteria["lastname"] = name_filter
                
                if phone_filter:
                    search_criteria["phone"] = phone_filter
                
                # Usar la funcionalidad de búsqueda del BaseRepository
                if search_criteria:
                    students = student_repo.get_all_rows(search_criteria)
                else:
                    students = student_repo.get_all_rows()
                
                # Filtro adicional por equipo si está seleccionado
                if team_filter and team_filter != "Todos":
                    try:
                        team_id = int(team_filter.split(" - ")[0])
                        students = [s for s in students if s["id_team"] == team_id]
                    except (ValueError, IndexError):
                        pass  # Si no se puede parsear el equipo, mostrar todos
                
                # Convertir a formato para la tabla
                self.test_students = []
                for student in students:
                    self.test_students.append({
                        "id": student["id"],
                        "name": student["name"],
                        "lastname": student["lastname"],
                        "phone": student["phone"],
                        "date_baptism": student["date_baptism"],
                        "date_of_birth": student["date_of_birth"],
                        "id_team": student["id_team"]
                    })
                
                conn.close()
                
                # Actualizar tabla
                self.update_students_table()
                
                print(f"Filtrados {len(self.test_students)} estudiantes")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al filtrar estudiantes: {str(e)}")
            messagebox.showerror("Error", f"Error al filtrar estudiantes: {str(e)}")
        
    def clear_student_filters(self):
        """Limpiar filtros de estudiantes"""
        self.student_name_filter.delete(0, "end")
        self.student_phone_filter.delete(0, "end")
        self.student_team_filter.set("Todos")
        
        # Recargar todos los datos
        self.load_students_from_database()
        
    def students_prev_page(self):
        """Página anterior de estudiantes"""
        if self.students_current_page > 1:
            self.students_current_page -= 1
            self.update_students_table()
            
    def students_next_page(self):
        """Página siguiente de estudiantes"""
        total_pages = (self.students_total_items + self.students_items_per_page - 1) // self.students_items_per_page
        if self.students_current_page < total_pages:
            self.students_current_page += 1
            self.update_students_table()
    
    # Funciones para Docentes
    def create_teachers_table(self, parent):
        """Crear tabla de docentes con paginación"""
        # Frame para la tabla
        self.teachers_table_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.teachers_table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Headers de la tabla
        headers_frame = ctk.CTkFrame(self.teachers_table_container, fg_color="#1f538d", height=50)
        headers_frame.pack(fill="x", pady=(0, 5))
        headers_frame.pack_propagate(False)
        
        # Headers
        headers = ["ID", "Nombre", "Apellido", "Teléfono", "Fecha Bautismo", "Fecha Nacimiento", "ID Equipo", "Acciones"]
        header_widths = [50, 150, 150, 120, 120, 120, 80, 120]
        
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
                width=width
            )
            header_label.place(x=sum(header_widths[:i]) + i*5, y=15)
        
        # Frame para las filas de datos
        self.teachers_rows_frame = ctk.CTkScrollableFrame(
            self.teachers_table_container,
            fg_color="#f8f9fa",
            height=450
        )
        self.teachers_rows_frame.pack(fill="both", expand=True)
        
        # Frame para paginación
        pagination_frame = ctk.CTkFrame(self.teachers_table_container, fg_color="transparent")
        pagination_frame.pack(fill="x", pady=(10, 0))
        
        # Información de paginación
        self.teachers_pagination_info = ctk.CTkLabel(
            pagination_frame,
            text="Mostrando 0 de 0 docentes",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        self.teachers_pagination_info.pack(side="left")
        
        # Botones de paginación
        pagination_buttons_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        pagination_buttons_frame.pack(side="right")
        
        self.teachers_prev_page_btn = ctk.CTkButton(
            pagination_buttons_frame,
            text="Anterior",
            width=100,
            height=30,
            command=self.teachers_prev_page,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.teachers_prev_page_btn.pack(side="left", padx=(0, 5))
        
        self.teachers_next_page_btn = ctk.CTkButton(
            pagination_buttons_frame,
            text="Siguiente",
            width=100,
            height=30,
            command=self.teachers_next_page,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.teachers_next_page_btn.pack(side="left")
        
        # Variables de paginación
        self.teachers_current_page = 1
        self.teachers_items_per_page = 10
        self.teachers_total_items = 0
        
    def load_teachers_from_database(self):
        """Cargar docentes desde la base de datos"""
        try:
            from control.bd.db_connection import Connection
            from control.teacher_repository import TeacherRepository
            
            conn = Connection.connect()
            if conn:
                teacher_repo = TeacherRepository(conn)
                teacher_repo.create_table()  # Asegurar que la tabla existe
                
                # Obtener todos los docentes
                teachers = teacher_repo.get_all_rows()
                
                # Convertir a formato para la tabla
                self.test_teachers = []
                for teacher in teachers:
                    self.test_teachers.append({
                        "id": teacher["id"],
                        "name": teacher["name"],
                        "lastname": teacher["lastname"],
                        "phone": teacher["phone"],
                        "date_baptism": teacher["date_baptism"],
                        "date_of_birth": teacher["date_of_birth"],
                        "id_team": teacher["id_team"]
                    })
                
                conn.close()
                
                # Actualizar tabla
                self.update_teachers_table()
                
                print(f"Cargados {len(self.test_teachers)} docentes desde la base de datos")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al cargar docentes: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar docentes: {str(e)}")
        
    def update_teachers_table(self):
        """Actualizar tabla de docentes"""
        # Limpiar filas existentes
        for widget in self.teachers_rows_frame.winfo_children():
            widget.destroy()
        
        # Calcular paginación
        start_idx = (self.teachers_current_page - 1) * self.teachers_items_per_page
        end_idx = start_idx + self.teachers_items_per_page
        
        # Obtener docentes para la página actual
        teachers_to_show = self.test_teachers[start_idx:end_idx]
        
        # Agregar docentes a la tabla
        for teacher in teachers_to_show:
            self.create_teacher_row(teacher)
        
        # Actualizar información de paginación
        self.teachers_total_items = len(self.test_teachers)
        total_pages = (self.teachers_total_items + self.teachers_items_per_page - 1) // self.teachers_items_per_page
        self.teachers_pagination_info.configure(text=f"Mostrando {len(teachers_to_show)} de {self.teachers_total_items} docentes")
        
        # Actualizar botones de paginación
        self.teachers_prev_page_btn.configure(state="normal" if self.teachers_current_page > 1 else "disabled")
        self.teachers_next_page_btn.configure(state="normal" if self.teachers_current_page < total_pages else "disabled")
        
    def create_teacher_row(self, teacher):
        """Crear fila de docente en la tabla"""
        row_frame = ctk.CTkFrame(self.teachers_rows_frame, fg_color="white", height=40)
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)
        
        # Datos del docente
        teacher_data = [
            str(teacher["id"]),
            teacher["name"],
            teacher["lastname"],
            teacher["phone"],
            teacher["date_baptism"] or "N/A",
            teacher["date_of_birth"] or "N/A",
            str(teacher["id_team"])
        ]
        
        # Mostrar datos
        header_widths = [50, 150, 150, 120, 120, 120, 80]
        for i, data in enumerate(teacher_data):
            data_label = ctk.CTkLabel(
                row_frame,
                text=data,
                font=ctk.CTkFont(size=12),
                text_color="#333333",
                width=header_widths[i]
            )
            data_label.place(x=sum(header_widths[:i]) + i*5, y=10)
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.place(x=sum(header_widths) + 7*5, y=5)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Editar",
            width=56,
            height=28,
            font=ctk.CTkFont(size=11),
            command=lambda t=teacher: self.edit_teacher(t),
            fg_color="#ffc107",
            hover_color="#e0a800"
        )
        edit_btn.pack(side="left", padx=(0, 4))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Eliminar",
            width=56,
            height=28,
            font=ctk.CTkFont(size=11),
            command=lambda t=teacher: self.delete_teacher(t),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side="left")
        
    def edit_teacher(self, teacher):
        """Editar docente"""
        self.show_edit_teacher_dialog(teacher)
        
    def delete_teacher(self, teacher):
        """Eliminar docente"""
        result = messagebox.askyesno("Confirmar", f"¿Eliminar docente {teacher['name']}?")
        if result:
            try:
                from control.bd.db_connection import Connection
                from control.teacher_repository import TeacherRepository
                
                conn = Connection.connect()
                if conn:
                    teacher_repo = TeacherRepository(conn)
                    success = teacher_repo.delete_row({"id": teacher['id']})
                    
                    if success:
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Docente '{teacher['name']}' eliminado correctamente")
                        self.load_teachers_from_database()  # Recargar datos
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el docente")
                    
                    conn.close()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al eliminar docente: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar docente: {str(e)}")
            
    def show_add_teacher_dialog(self):
        """Mostrar diálogo para agregar docente"""
        self.show_teacher_dialog()
        
    def show_edit_teacher_dialog(self, teacher):
        """Mostrar diálogo para editar docente"""
        self.show_teacher_dialog(teacher)
        
    def show_teacher_dialog(self, teacher=None):
        """Mostrar diálogo para agregar/editar docente"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Agregar Docente" if not teacher else "Editar Docente")
        dialog.geometry("700x600")
        dialog.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Centrar la ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"700x600+{x}+{y}")
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Agregar Docente" if not teacher else "Editar Docente",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Campos del formulario
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=30, pady=30)
        
        # Nombre del docente
        name_label = ctk.CTkLabel(
            fields_frame,
            text="Nombre:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        name_label.pack(anchor="w", pady=(0, 8))
        
        name_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese el nombre del docente",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        name_entry.pack(fill="x", pady=(0, 20))
        
        # Apellido del docente
        lastname_label = ctk.CTkLabel(
            fields_frame,
            text="Apellido:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        lastname_label.pack(anchor="w", pady=(0, 8))
        
        lastname_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ingrese el apellido del docente",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        lastname_entry.pack(fill="x", pady=(0, 20))
        
        # Teléfono del docente
        phone_label = ctk.CTkLabel(
            fields_frame,
            text="Teléfono:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        phone_label.pack(anchor="w", pady=(0, 8))
        
        phone_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Ej: 555-0123",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        phone_entry.pack(fill="x", pady=(0, 20))
        
        # Fecha de bautismo
        baptism_label = ctk.CTkLabel(
            fields_frame,
            text="Fecha de Bautismo:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        baptism_label.pack(anchor="w", pady=(0, 8))
        
        baptism_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="YYYY-MM-DD (ej: 2020-01-15)",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        baptism_entry.pack(fill="x", pady=(0, 20))
        
        # Fecha de nacimiento
        birth_label = ctk.CTkLabel(
            fields_frame,
            text="Fecha de Nacimiento:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        birth_label.pack(anchor="w", pady=(0, 8))
        
        birth_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="YYYY-MM-DD (ej: 1995-05-20)",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d"
        )
        birth_entry.pack(fill="x", pady=(0, 20))
        
        # Equipo (ComboBox con equipos disponibles)
        team_label = ctk.CTkLabel(
            fields_frame,
            text="Equipo:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        team_label.pack(anchor="w", pady=(0, 8))
        
        # Cargar equipos disponibles
        team_options = []
        try:
            from control.bd.db_connection import Connection
            from control.team_repository import TeamRepository
            
            conn = Connection.connect()
            if conn:
                team_repo = TeamRepository(conn)
                teams = team_repo.get_all_rows()
                team_options = [f"{team['id']} - {team['name']}" for team in teams]
                conn.close()
        except Exception as e:
            print(f"Error al cargar equipos: {str(e)}")
            team_options = ["No hay equipos disponibles"]
        
        team_combo = ctk.CTkComboBox(
            fields_frame,
            values=team_options,
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color="#1f538d",
            button_color="#1f538d"
        )
        team_combo.pack(fill="x", pady=(0, 30))
        
        # Llenar campos si es edición
        if teacher:
            name_entry.insert(0, teacher['name'])
            lastname_entry.insert(0, teacher['lastname'])
            phone_entry.insert(0, teacher['phone'])
            baptism_entry.insert(0, teacher['date_baptism'] or "")
            birth_entry.insert(0, teacher['date_of_birth'] or "")
            # Buscar el equipo correspondiente en el ComboBox
            for i, option in enumerate(team_options):
                if option.startswith(f"{teacher['id_team']} -"):
                    team_combo.set(option)
                    break
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(30, 0))
        
        def save_teacher():
            """Guardar docente"""
            name = name_entry.get().strip()
            lastname = lastname_entry.get().strip()
            phone = phone_entry.get().strip()
            date_baptism = baptism_entry.get().strip()
            date_of_birth = birth_entry.get().strip()
            team_selection = team_combo.get().strip()
            
            # Validaciones
            if not name:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            if not lastname:
                messagebox.showerror("Error", "El apellido es obligatorio")
                return
            
            if not phone:
                messagebox.showerror("Error", "El teléfono es obligatorio")
                return
            
            if not team_selection or team_selection == "No hay equipos disponibles":
                messagebox.showerror("Error", "Debe seleccionar un equipo")
                return
            
            # Extraer ID del equipo del formato "ID - Nombre"
            try:
                id_team = int(team_selection.split(" - ")[0])
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Formato de equipo inválido")
                return
            
            try:
                from control.bd.db_connection import Connection
                from control.teacher_repository import TeacherRepository
                
                conn = Connection.connect()
                if conn:
                    teacher_repo = TeacherRepository(conn)
                    
                    if teacher:  # Editar
                        try:
                            teacher_repo.update_row(
                                new_data={
                                    "name": name,
                                    "lastname": lastname,
                                    "phone": phone,
                                    "date_baptism": date_baptism if date_baptism else None,
                                    "date_of_birth": date_of_birth if date_of_birth else None,
                                    "id_team": id_team
                                },
                                conditions={"id": teacher['id']}
                            )
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Docente '{name}' actualizado correctamente")
                        except Exception as update_error:
                            print(f"Error al actualizar docente: {str(update_error)}")
                            messagebox.showerror("Error", f"No se pudo actualizar el docente: {str(update_error)}")
                            return
                    else:  # Agregar
                        try:
                            teacher_repo.insert_row({
                                "name": name,
                                "lastname": lastname,
                                "phone": phone,
                                "date_baptism": date_baptism if date_baptism else None,
                                "date_of_birth": date_of_birth if date_of_birth else None,
                                "id_team": id_team
                            })
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Docente '{name}' agregado correctamente")
                        except Exception as insert_error:
                            print(f"Error al insertar docente: {str(insert_error)}")
                            messagebox.showerror("Error", f"No se pudo agregar el docente: {str(insert_error)}")
                            return
                    
                    conn.close()
                    dialog.destroy()
                    self.load_teachers_from_database()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al guardar docente: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar docente: {str(e)}")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Guardar Docente",
            width=200,
            height=50,
            command=save_teacher,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            border_width=2,
            border_color="#1e7e34"
        )
        save_btn.pack(side="right", padx=(15, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=150,
            height=50,
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            border_width=2,
            border_color="#5a6268"
        )
        cancel_btn.pack(side="right")
        
    def filter_teachers(self):
        """Filtrar docentes usando BaseRepository search"""
        try:
            from control.bd.db_connection import Connection
            from control.teacher_repository import TeacherRepository
            
            conn = Connection.connect()
            if conn:
                teacher_repo = TeacherRepository(conn)
                
                # Obtener filtros
                name_filter = self.teacher_name_filter.get().strip()
                phone_filter = self.teacher_phone_filter.get().strip()
                team_filter = self.teacher_team_filter.get()
                
                # Construir diccionario de búsqueda para BaseRepository
                search_criteria = {}
                
                if name_filter:
                    # Buscar en nombre y apellido
                    search_criteria["name"] = name_filter
                    search_criteria["lastname"] = name_filter
                
                if phone_filter:
                    search_criteria["phone"] = phone_filter
                
                # Usar la funcionalidad de búsqueda del BaseRepository
                if search_criteria:
                    teachers = teacher_repo.get_all_rows(search_criteria)
                else:
                    teachers = teacher_repo.get_all_rows()
                
                # Filtro adicional por equipo si está seleccionado
                if team_filter and team_filter != "Todos":
                    try:
                        team_id = int(team_filter.split(" - ")[0])
                        teachers = [t for t in teachers if t["id_team"] == team_id]
                    except (ValueError, IndexError):
                        pass  # Si no se puede parsear el equipo, mostrar todos
                
                # Convertir a formato para la tabla
                self.test_teachers = []
                for teacher in teachers:
                    self.test_teachers.append({
                        "id": teacher["id"],
                        "name": teacher["name"],
                        "lastname": teacher["lastname"],
                        "phone": teacher["phone"],
                        "date_baptism": teacher["date_baptism"],
                        "date_of_birth": teacher["date_of_birth"],
                        "id_team": teacher["id_team"]
                    })
                
                conn.close()
                
                # Actualizar tabla
                self.update_teachers_table()
                
                print(f"Filtrados {len(self.test_teachers)} docentes")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al filtrar docentes: {str(e)}")
            messagebox.showerror("Error", f"Error al filtrar docentes: {str(e)}")
        
    def clear_teacher_filters(self):
        """Limpiar filtros de docentes"""
        self.teacher_name_filter.delete(0, "end")
        self.teacher_phone_filter.delete(0, "end")
        self.teacher_team_filter.set("Todos")
        
        # Recargar todos los datos
        self.load_teachers_from_database()
        
    def load_teams_for_student_filter(self):
        """Cargar equipos en el filtro de estudiantes"""
        try:
            from control.bd.db_connection import Connection
            from control.team_repository import TeamRepository
            
            conn = Connection.connect()
            if conn:
                team_repo = TeamRepository(conn)
                teams = team_repo.get_all_rows()
                team_options = ["Todos"] + [f"{team['id']} - {team['name']}" for team in teams]
                self.student_team_filter.configure(values=team_options)
                conn.close()
        except Exception as e:
            print(f"Error al cargar equipos para filtro de estudiantes: {str(e)}")
    
    def load_teams_for_teacher_filter(self):
        """Cargar equipos en el filtro de docentes"""
        try:
            from control.bd.db_connection import Connection
            from control.team_repository import TeamRepository
            
            conn = Connection.connect()
            if conn:
                team_repo = TeamRepository(conn)
                teams = team_repo.get_all_rows()
                team_options = ["Todos"] + [f"{team['id']} - {team['name']}" for team in teams]
                self.teacher_team_filter.configure(values=team_options)
                conn.close()
        except Exception as e:
            print(f"Error al cargar equipos para filtro de docentes: {str(e)}")
        
    def teachers_prev_page(self):
        """Página anterior de docentes"""
        if self.teachers_current_page > 1:
            self.teachers_current_page -= 1
            self.update_teachers_table()
            
    def teachers_next_page(self):
        """Página siguiente de docentes"""
        total_pages = (self.teachers_total_items + self.teachers_items_per_page - 1) // self.teachers_items_per_page
        if self.teachers_current_page < total_pages:
            self.teachers_current_page += 1
            self.update_teachers_table()
