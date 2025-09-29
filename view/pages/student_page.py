import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from control.student_repository import StudentRepository
from control.bd.db_connection import Connection
from model.student import Student


class StudentPage:
    def __init__(self, parent):
        self.parent = parent
        self.selected_student = None
        self.setup_ui()
        self.initialize_database()
        self.load_students()

    def setup_ui(self):
        """Configurar la interfaz de gestión de estudiantes"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(
            self.main_frame,
            text="👤 Gestión de Estudiantes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))

        # Frame para botones de acción
        self.actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(0, 20))

        # Botón agregar estudiante
        self.add_btn = ctk.CTkButton(
            self.actions_frame,
            text="➕ Nuevo Estudiante",
            width=150,
            height=40,
            command=self.show_add_student_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        # Botón editar estudiante
        self.edit_btn = ctk.CTkButton(
            self.actions_frame,
            text="✏️ Editar",
            width=120,
            height=40,
            command=self.show_edit_student_dialog,
            fg_color="#ffc107",
            hover_color="#e0a800",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.edit_btn.pack(side="left", padx=(0, 10))

        # Botón eliminar estudiante
        self.delete_btn = ctk.CTkButton(
            self.actions_frame,
            text="🗑️ Eliminar",
            width=120,
            height=40,
            command=self.delete_student,
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
            command=self.load_students,
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
        """Crear tabla para mostrar estudiantes"""
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
        columns = ("ID", "Nombres", "Apellidos", "Teléfono", "Email", "Fecha Nacimiento", "Fecha Bautismo")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombres", text="Nombres")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Fecha Nacimiento", text="Fecha Nacimiento")
        self.tree.heading("Fecha Bautismo", text="Fecha Bautismo")

        # Configurar ancho de columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombres", width=120, anchor="w")
        self.tree.column("Apellidos", width=120, anchor="w")
        self.tree.column("Teléfono", width=100, anchor="center")
        self.tree.column("Email", width=150, anchor="w")
        self.tree.column("Fecha Nacimiento", width=120, anchor="center")
        self.tree.column("Fecha Bautismo", width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind para selección
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def initialize_database(self):
        """Inicializar la base de datos y crear la tabla si no existe"""
        try:
            conn = Connection.connect()
            if conn:
                student_repo = StudentRepository(conn)
                student_repo.create_table()
                conn.close()
                print("Base de datos de estudiantes inicializada correctamente")
            else:
                print("Error: No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {str(e)}")

    def load_students(self):
        """Cargar estudiantes desde la base de datos"""
        try:
            conn = Connection.connect()
            if conn:
                student_repo = StudentRepository(conn)
                students = student_repo.get_all_students()
                
                # Limpiar tabla
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Agregar estudiantes a la tabla
                for student in students:
                    self.tree.insert("", "end", values=(
                        student.id,
                        student.names,
                        student.surnames,
                        student.phone,
                        student.email,
                        student.birth_date,
                        student.baptism_date
                    ))
                
                conn.close()
                print(f"Cargados {len(students)} estudiantes")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al cargar estudiantes: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")

    def on_select(self, event):
        """Manejar selección de estudiante"""
        selection = self.tree.selection()
        if selection:
            self.selected_student = self.tree.item(selection[0])["values"]
        else:
            self.selected_student = None

    def show_add_student_dialog(self):
        """Mostrar diálogo para agregar nuevo estudiante"""
        self.show_student_dialog("Agregar Estudiante", None)

    def show_edit_student_dialog(self):
        """Mostrar diálogo para editar estudiante"""
        if not self.selected_student:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para editar")
            return
        
        self.show_student_dialog("Editar Estudiante", self.selected_student)

    def show_student_dialog(self, title, student_data=None):
        """Mostrar diálogo para agregar/editar estudiante"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(title)
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()

        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")

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

        # Nombres
        names_label = ctk.CTkLabel(form_frame, text="Nombres:")
        names_label.pack(anchor="w", pady=(0, 5))
        names_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Juan Carlos", width=400)
        names_entry.pack(fill="x", pady=(0, 10))

        # Apellidos
        surnames_label = ctk.CTkLabel(form_frame, text="Apellidos:")
        surnames_label.pack(anchor="w", pady=(0, 5))
        surnames_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Pérez García", width=400)
        surnames_entry.pack(fill="x", pady=(0, 10))

        # Teléfono
        phone_label = ctk.CTkLabel(form_frame, text="Teléfono:")
        phone_label.pack(anchor="w", pady=(0, 5))
        phone_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 987654321", width=400)
        phone_entry.pack(fill="x", pady=(0, 10))

        # Email
        email_label = ctk.CTkLabel(form_frame, text="Email:")
        email_label.pack(anchor="w", pady=(0, 5))
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: juan.perez@email.com", width=400)
        email_entry.pack(fill="x", pady=(0, 10))

        # Fecha de nacimiento
        birth_date_label = ctk.CTkLabel(form_frame, text="Fecha de Nacimiento:")
        birth_date_label.pack(anchor="w", pady=(0, 5))
        birth_date_entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", width=400)
        birth_date_entry.pack(fill="x", pady=(0, 10))

        # Fecha de bautismo
        baptism_date_label = ctk.CTkLabel(form_frame, text="Fecha de Bautismo:")
        baptism_date_label.pack(anchor="w", pady=(0, 5))
        baptism_date_entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", width=400)
        baptism_date_entry.pack(fill="x", pady=(0, 20))

        # Llenar campos si es edición
        if student_data:
            names_entry.insert(0, student_data[1])
            surnames_entry.insert(0, student_data[2])
            phone_entry.insert(0, student_data[3])
            email_entry.insert(0, student_data[4])
            birth_date_entry.insert(0, student_data[5])
            baptism_date_entry.insert(0, student_data[6])

        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")

        def save_student():
            """Guardar estudiante"""
            names = names_entry.get().strip()
            surnames = surnames_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            birth_date = birth_date_entry.get().strip()
            baptism_date = baptism_date_entry.get().strip()

            # Validaciones
            if not names:
                messagebox.showerror("Error", "Los nombres son obligatorios")
                return

            if not surnames:
                messagebox.showerror("Error", "Los apellidos son obligatorios")
                return

            if not phone:
                messagebox.showerror("Error", "El teléfono es obligatorio")
                return

            if not email:
                messagebox.showerror("Error", "El email es obligatorio")
                return

            if not birth_date:
                messagebox.showerror("Error", "La fecha de nacimiento es obligatoria")
                return

            if not baptism_date:
                messagebox.showerror("Error", "La fecha de bautismo es obligatoria")
                return

            try:
                # Crear instancia de Student
                if student_data:  # Editar
                    student = Student(
                        id=student_data[0],
                        names=names,
                        surnames=surnames,
                        phone=phone,
                        email=email,
                        birth_date=birth_date,
                        baptism_date=baptism_date
                    )
                else:  # Agregar
                    student = Student(
                        names=names,
                        surnames=surnames,
                        phone=phone,
                        email=email,
                        birth_date=birth_date,
                        baptism_date=baptism_date
                    )

                conn = Connection.connect()
                if conn:
                    student_repo = StudentRepository(conn)
                    
                    if student_data:  # Editar
                        success = student_repo.update_student(student)
                        if success:
                            messagebox.showinfo("Éxito", f"Estudiante '{student.names} {student.surnames}' actualizado correctamente")
                        else:
                            messagebox.showerror("Error", "No se pudo actualizar el estudiante")
                            return
                    else:  # Agregar
                        created_student = student_repo.create_student(student)
                        messagebox.showinfo("Éxito", f"Estudiante '{created_student.names} {created_student.surnames}' agregado correctamente")
                    
                    conn.commit()
                    conn.close()
                    dialog.destroy()
                    self.load_students()  # Refrescar la tabla
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except ValueError as ve:
                messagebox.showerror("Error de Validación", str(ve))
            except Exception as e:
                print(f"Error al guardar estudiante: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar estudiante: {str(e)}")

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            width=120,
            height=40,
            command=save_student,
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

    def delete_student(self):
        """Eliminar estudiante seleccionado"""
        if not self.selected_student:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para eliminar")
            return

        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el estudiante '{self.selected_student[1]} {self.selected_student[2]}'?"
        )

        if result:
            try:
                conn = Connection.connect()
                if conn:
                    student_repo = StudentRepository(conn)
                    success = student_repo.delete_student(self.selected_student[0])
                    
                    if success:
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Estudiante '{self.selected_student[1]} {self.selected_student[2]}' eliminado correctamente")
                        self.load_students()  # Refrescar la tabla
                        self.selected_student = None  # Limpiar selección
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el estudiante")
                    
                    conn.close()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al eliminar estudiante: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar estudiante: {str(e)}")

