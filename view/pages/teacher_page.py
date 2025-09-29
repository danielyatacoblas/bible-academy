import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from control.teacher_repository import TeacherRepository
from control.bd.db_connection import Connection
from model.teacher import Teacher


class TeacherPage:
    def __init__(self, parent):
        self.parent = parent
        self.selected_teacher = None
        self.setup_ui()
        self.initialize_database()
        self.load_teachers()

    def setup_ui(self):
        """Configurar la interfaz de gestión de docentes"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(
            self.main_frame,
            text="🎓 Gestión de Docentes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))

        # Frame para botones de acción
        self.actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(0, 20))

        # Botón agregar docente
        self.add_btn = ctk.CTkButton(
            self.actions_frame,
            text="➕ Nuevo Docente",
            width=150,
            height=40,
            command=self.show_add_teacher_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        # Botón editar docente
        self.edit_btn = ctk.CTkButton(
            self.actions_frame,
            text="✏️ Editar",
            width=120,
            height=40,
            command=self.show_edit_teacher_dialog,
            fg_color="#ffc107",
            hover_color="#e0a800",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.edit_btn.pack(side="left", padx=(0, 10))

        # Botón eliminar docente
        self.delete_btn = ctk.CTkButton(
            self.actions_frame,
            text="🗑️ Eliminar",
            width=120,
            height=40,
            command=self.delete_teacher,
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
            command=self.load_teachers,
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
        """Crear tabla para mostrar docentes"""
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
        columns = ("ID", "Nombres", "Apellidos", "Especialidad", "Teléfono", "Email", "Experiencia")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombres", text="Nombres")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Especialidad", text="Especialidad")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Experiencia", text="Experiencia (años)")

        # Configurar ancho de columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombres", width=120, anchor="w")
        self.tree.column("Apellidos", width=120, anchor="w")
        self.tree.column("Especialidad", width=150, anchor="w")
        self.tree.column("Teléfono", width=100, anchor="center")
        self.tree.column("Email", width=150, anchor="w")
        self.tree.column("Experiencia", width=100, anchor="center")

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
                teacher_repo = TeacherRepository(conn)
                teacher_repo.create_table()
                conn.close()
                print("Base de datos de docentes inicializada correctamente")
            else:
                print("Error: No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {str(e)}")

    def load_teachers(self):
        """Cargar docentes desde la base de datos"""
        try:
            conn = Connection.connect()
            if conn:
                teacher_repo = TeacherRepository(conn)
                teachers = teacher_repo.get_all_teachers()
                
                # Limpiar tabla
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Agregar docentes a la tabla
                for teacher in teachers:
                    self.tree.insert("", "end", values=(
                        teacher.id,
                        teacher.names,
                        teacher.surnames,
                        teacher.specialty,
                        teacher.phone,
                        teacher.email,
                        teacher.experience_years
                    ))
                
                conn.close()
                print(f"Cargados {len(teachers)} docentes")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al cargar docentes: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar docentes: {str(e)}")

    def on_select(self, event):
        """Manejar selección de docente"""
        selection = self.tree.selection()
        if selection:
            self.selected_teacher = self.tree.item(selection[0])["values"]
        else:
            self.selected_teacher = None

    def show_add_teacher_dialog(self):
        """Mostrar diálogo para agregar nuevo docente"""
        self.show_teacher_dialog("Agregar Docente", None)

    def show_edit_teacher_dialog(self):
        """Mostrar diálogo para editar docente"""
        if not self.selected_teacher:
            messagebox.showwarning("Advertencia", "Seleccione un docente para editar")
            return
        
        self.show_teacher_dialog("Editar Docente", self.selected_teacher)

    def show_teacher_dialog(self, title, teacher_data=None):
        """Mostrar diálogo para agregar/editar docente"""
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
        names_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: María Elena", width=400)
        names_entry.pack(fill="x", pady=(0, 10))

        # Apellidos
        surnames_label = ctk.CTkLabel(form_frame, text="Apellidos:")
        surnames_label.pack(anchor="w", pady=(0, 5))
        surnames_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: García López", width=400)
        surnames_entry.pack(fill="x", pady=(0, 10))

        # Especialidad
        specialty_label = ctk.CTkLabel(form_frame, text="Especialidad:")
        specialty_label.pack(anchor="w", pady=(0, 5))
        specialty_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Teología Sistemática", width=400)
        specialty_entry.pack(fill="x", pady=(0, 10))

        # Teléfono
        phone_label = ctk.CTkLabel(form_frame, text="Teléfono:")
        phone_label.pack(anchor="w", pady=(0, 5))
        phone_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 987654321", width=400)
        phone_entry.pack(fill="x", pady=(0, 10))

        # Email
        email_label = ctk.CTkLabel(form_frame, text="Email:")
        email_label.pack(anchor="w", pady=(0, 5))
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: maria.garcia@email.com", width=400)
        email_entry.pack(fill="x", pady=(0, 10))

        # Años de experiencia
        experience_label = ctk.CTkLabel(form_frame, text="Años de Experiencia:")
        experience_label.pack(anchor="w", pady=(0, 5))
        experience_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 5", width=400)
        experience_entry.pack(fill="x", pady=(0, 20))

        # Llenar campos si es edición
        if teacher_data:
            names_entry.insert(0, teacher_data[1])
            surnames_entry.insert(0, teacher_data[2])
            specialty_entry.insert(0, teacher_data[3])
            phone_entry.insert(0, teacher_data[4])
            email_entry.insert(0, teacher_data[5])
            experience_entry.insert(0, str(teacher_data[6]))

        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")

        def save_teacher():
            """Guardar docente"""
            names = names_entry.get().strip()
            surnames = surnames_entry.get().strip()
            specialty = specialty_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            experience = experience_entry.get().strip()

            # Validaciones
            if not names:
                messagebox.showerror("Error", "Los nombres son obligatorios")
                return

            if not surnames:
                messagebox.showerror("Error", "Los apellidos son obligatorios")
                return

            if not specialty:
                messagebox.showerror("Error", "La especialidad es obligatoria")
                return

            if not phone:
                messagebox.showerror("Error", "El teléfono es obligatorio")
                return

            if not email:
                messagebox.showerror("Error", "El email es obligatorio")
                return

            if not experience or not experience.isdigit():
                messagebox.showerror("Error", "Los años de experiencia deben ser un número válido")
                return

            try:
                # Crear instancia de Teacher
                if teacher_data:  # Editar
                    teacher = Teacher(
                        id=teacher_data[0],
                        names=names,
                        surnames=surnames,
                        specialty=specialty,
                        phone=phone,
                        email=email,
                        experience_years=int(experience)
                    )
                else:  # Agregar
                    teacher = Teacher(
                        names=names,
                        surnames=surnames,
                        specialty=specialty,
                        phone=phone,
                        email=email,
                        experience_years=int(experience)
                    )

                conn = Connection.connect()
                if conn:
                    teacher_repo = TeacherRepository(conn)
                    
                    if teacher_data:  # Editar
                        success = teacher_repo.update_teacher(teacher)
                        if success:
                            messagebox.showinfo("Éxito", f"Docente '{teacher.names} {teacher.surnames}' actualizado correctamente")
                        else:
                            messagebox.showerror("Error", "No se pudo actualizar el docente")
                            return
                    else:  # Agregar
                        created_teacher = teacher_repo.create_teacher(teacher)
                        messagebox.showinfo("Éxito", f"Docente '{created_teacher.names} {created_teacher.surnames}' agregado correctamente")
                    
                    conn.commit()
                    conn.close()
                    dialog.destroy()
                    self.load_teachers()  # Refrescar la tabla
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except ValueError as ve:
                messagebox.showerror("Error de Validación", str(ve))
            except Exception as e:
                print(f"Error al guardar docente: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar docente: {str(e)}")

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            width=120,
            height=40,
            command=save_teacher,
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

    def delete_teacher(self):
        """Eliminar docente seleccionado"""
        if not self.selected_teacher:
            messagebox.showwarning("Advertencia", "Seleccione un docente para eliminar")
            return

        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el docente '{self.selected_teacher[1]} {self.selected_teacher[2]}'?"
        )

        if result:
            try:
                conn = Connection.connect()
                if conn:
                    teacher_repo = TeacherRepository(conn)
                    success = teacher_repo.delete_teacher(self.selected_teacher[0])
                    
                    if success:
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Docente '{self.selected_teacher[1]} {self.selected_teacher[2]}' eliminado correctamente")
                        self.load_teachers()  # Refrescar la tabla
                        self.selected_teacher = None  # Limpiar selección
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el docente")
                    
                    conn.close()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al eliminar docente: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar docente: {str(e)}")

