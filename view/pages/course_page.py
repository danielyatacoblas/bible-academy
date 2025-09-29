import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from control.course_repository import CourseRepository
from control.bd.db_connection import Connection
from model.course import Course


class CoursePage:
    def __init__(self, parent):
        self.parent = parent
        self.selected_course = None
        self.setup_ui()
        self.load_courses()

    def setup_ui(self):
        """Configurar la interfaz de gestión de cursos"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(
            self.main_frame,
            text="💻 Gestión de Cursos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))

        # Frame para botones de acción
        self.actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(0, 20))

        # Botón agregar curso
        self.add_btn = ctk.CTkButton(
            self.actions_frame,
            text="➕ Nuevo Curso",
            width=150,
            height=40,
            command=self.show_add_course_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        # Botón editar curso
        self.edit_btn = ctk.CTkButton(
            self.actions_frame,
            text="✏️ Editar",
            width=120,
            height=40,
            command=self.show_edit_course_dialog,
            fg_color="#ffc107",
            hover_color="#e0a800",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.edit_btn.pack(side="left", padx=(0, 10))

        # Botón eliminar curso
        self.delete_btn = ctk.CTkButton(
            self.actions_frame,
            text="🗑️ Eliminar",
            width=120,
            height=40,
            command=self.delete_course,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.delete_btn.pack(side="left", padx=(0, 10))

        # Botón refrescar
        self.refresh_btn = ctk.CTkButton(
            self.actions_frame,
            text="🔄 Refrescar",
            width=120,
            height=40,
            command=self.load_courses,
            fg_color="#17a2b8",
            hover_color="#138496",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.refresh_btn.pack(side="right")

        # Frame para la tabla
        self.table_frame = ctk.CTkFrame(self.main_frame)
        self.table_frame.pack(fill="both", expand=True)

        # Crear tabla
        self.create_table()

    def create_table(self):
        """Crear tabla para mostrar cursos"""
        # Configurar estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#ffffff",
                       foreground="#000000",
                       rowheight=25,
                       fieldbackground="#ffffff")
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       font=("Arial", 12, "bold"))

        # Crear Treeview
        columns = ("ID", "Nombre", "Nivel")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre del Curso")
        self.tree.heading("Nivel", text="Nivel")

        # Configurar ancho de columnas
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Nombre", width=300, anchor="w")
        self.tree.column("Nivel", width=150, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind para selección
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_courses(self):
        """Cargar cursos desde la base de datos"""
        try:
            conn = Connection.connect()
            if conn:
                course_repo = CourseRepository(conn)
                courses = course_repo.get_all_rows()
                
                # Limpiar tabla
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Agregar cursos a la tabla
                for course in courses:
                    self.tree.insert("", "end", values=(
                        course["id"],
                        course["name"],
                        course["level"]
                    ))
                
                conn.close()
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cursos: {str(e)}")

    def on_select(self, event):
        """Manejar selección de curso"""
        selection = self.tree.selection()
        if selection:
            self.selected_course = self.tree.item(selection[0])["values"]
        else:
            self.selected_course = None

    def show_add_course_dialog(self):
        """Mostrar diálogo para agregar nuevo curso"""
        self.show_course_dialog("Agregar Curso", None)

    def show_edit_course_dialog(self):
        """Mostrar diálogo para editar curso"""
        if not self.selected_course:
            messagebox.showwarning("Advertencia", "Seleccione un curso para editar")
            return
        
        self.show_course_dialog("Editar Curso", self.selected_course)

    def show_course_dialog(self, title, course_data=None):
        """Mostrar diálogo para agregar/editar curso"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(title)
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()

        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"400x250+{x}+{y}")

        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f538d"
        )
        title_label.pack(pady=(0, 20))

        # Campos del formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 20))

        # Nombre del curso
        name_label = ctk.CTkLabel(form_frame, text="Nombre del Curso:")
        name_label.pack(anchor="w", pady=(0, 5))
        name_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Fundamentos de la Fe", width=300)
        name_entry.pack(fill="x", pady=(0, 10))

        # Nivel del curso
        level_label = ctk.CTkLabel(form_frame, text="Nivel del Curso:")
        level_label.pack(anchor="w", pady=(0, 5))
        level_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 1 (Básico), 2 (Intermedio), 3 (Avanzado)", width=300)
        level_entry.pack(fill="x", pady=(0, 20))

        # Llenar campos si es edición
        if course_data:
            name_entry.insert(0, course_data[1])
            level_entry.insert(0, str(course_data[2]))

        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")

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
                conn = Connection.connect()
                if conn:
                    course_repo = CourseRepository(conn)
                    
                    if course_data:  # Editar
                        course_repo.update_row(
                            {"id": course_data[0]},
                            {"name": name, "level": level}
                        )
                        messagebox.showinfo("Éxito", f"Curso '{name}' actualizado correctamente")
                    else:  # Agregar
                        course_repo.insert_row({
                            "name": name,
                            "level": level
                        })
                        messagebox.showinfo("Éxito", f"Curso '{name}' agregado correctamente")
                    
                    conn.commit()
                    conn.close()
                    dialog.destroy()
                    self.load_courses()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar curso: {str(e)}")

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            width=120,
            height=40,
            command=save_course,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        save_btn.pack(side="right", padx=(10, 0))

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            width=120,
            height=40,
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        cancel_btn.pack(side="right")

    def delete_course(self):
        """Eliminar curso seleccionado"""
        if not self.selected_course:
            messagebox.showwarning("Advertencia", "Seleccione un curso para eliminar")
            return

        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el curso '{self.selected_course[1]}'?"
        )

        if result:
            try:
                conn = Connection.connect()
                if conn:
                    course_repo = CourseRepository(conn)
                    course_repo.delete_row({"id": self.selected_course[0]})
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("Éxito", f"Curso '{self.selected_course[1]}' eliminado correctamente")
                    self.load_courses()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar curso: {str(e)}")