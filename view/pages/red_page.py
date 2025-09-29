import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from control.team_repository import TeamRepository
from control.bd.db_connection import Connection
from model.team import Team


class RedPage:
    def __init__(self, parent):
        self.parent = parent
        self.selected_red = None
        self.setup_ui()
        self.initialize_database()
        self.load_redes()

    def setup_ui(self):
        """Configurar la interfaz de gestión de redes"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(
            self.main_frame,
            text="👥 Gestión de Redes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))

        # Frame para botones de acción
        self.actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(0, 20))

        # Botón agregar red
        self.add_btn = ctk.CTkButton(
            self.actions_frame,
            text="➕ Nueva Red",
            width=150,
            height=40,
            command=self.show_add_red_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        # Botón editar red
        self.edit_btn = ctk.CTkButton(
            self.actions_frame,
            text="✏️ Editar",
            width=120,
            height=40,
            command=self.show_edit_red_dialog,
            fg_color="#ffc107",
            hover_color="#e0a800",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.edit_btn.pack(side="left", padx=(0, 10))

        # Botón eliminar red
        self.delete_btn = ctk.CTkButton(
            self.actions_frame,
            text="🗑️ Eliminar",
            width=120,
            height=40,
            command=self.delete_red,
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
            command=self.load_redes,
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
        """Crear tabla para mostrar redes"""
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
        columns = ("ID", "Nombre", "Género", "Edad Mínima", "Edad Máxima", "Miembros")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre de la Red")
        self.tree.heading("Género", text="Género")
        self.tree.heading("Edad Mínima", text="Edad Mínima")
        self.tree.heading("Edad Máxima", text="Edad Máxima")
        self.tree.heading("Miembros", text="Miembros")

        # Configurar ancho de columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=200, anchor="w")
        self.tree.column("Género", width=100, anchor="center")
        self.tree.column("Edad Mínima", width=100, anchor="center")
        self.tree.column("Edad Máxima", width=100, anchor="center")
        self.tree.column("Miembros", width=100, anchor="center")

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
                team_repo = TeamRepository(conn)
                team_repo.create_table()
                conn.close()
                print("Base de datos de redes inicializada correctamente")
            else:
                print("Error: No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {str(e)}")

    def load_redes(self):
        """Cargar redes desde la base de datos"""
        try:
            conn = Connection.connect()
            if conn:
                team_repo = TeamRepository(conn)
                teams = team_repo.get_all_teams()
                
                # Limpiar tabla
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Agregar redes a la tabla
                for team in teams:
                    # Simular número de miembros (en una implementación real vendría de otra tabla)
                    members_count = 0  # Por ahora 0, se puede implementar después
                    
                    self.tree.insert("", "end", values=(
                        team.id,
                        team.name,
                        team.gender,
                        team.age_start,
                        team.age_end,
                        members_count
                    ))
                
                conn.close()
                print(f"Cargadas {len(teams)} redes")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            print(f"Error al cargar redes: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar redes: {str(e)}")

    def on_select(self, event):
        """Manejar selección de red"""
        selection = self.tree.selection()
        if selection:
            self.selected_red = self.tree.item(selection[0])["values"]
        else:
            self.selected_red = None

    def show_add_red_dialog(self):
        """Mostrar diálogo para agregar nueva red"""
        self.show_red_dialog("Agregar Red", None)

    def show_edit_red_dialog(self):
        """Mostrar diálogo para editar red"""
        if not self.selected_red:
            messagebox.showwarning("Advertencia", "Seleccione una red para editar")
            return
        
        self.show_red_dialog("Editar Red", self.selected_red)

    def show_red_dialog(self, title, red_data=None):
        """Mostrar diálogo para agregar/editar red"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()

        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")

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

        # Nombre de la red
        name_label = ctk.CTkLabel(form_frame, text="Nombre de la Red:")
        name_label.pack(anchor="w", pady=(0, 5))
        name_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Jóvenes en Acción", width=300)
        name_entry.pack(fill="x", pady=(0, 10))

        # Género
        gender_label = ctk.CTkLabel(form_frame, text="Género:")
        gender_label.pack(anchor="w", pady=(0, 5))
        gender_var = ctk.StringVar(value="Mixto")
        gender_combo = ctk.CTkComboBox(
            form_frame,
            values=["Mixto", "Masculino", "Femenino"],
            variable=gender_var,
            width=300
        )
        gender_combo.pack(fill="x", pady=(0, 10))

        # Edad mínima
        age_start_label = ctk.CTkLabel(form_frame, text="Edad Mínima:")
        age_start_label.pack(anchor="w", pady=(0, 5))
        age_start_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 15", width=300)
        age_start_entry.pack(fill="x", pady=(0, 10))

        # Edad máxima
        age_end_label = ctk.CTkLabel(form_frame, text="Edad Máxima:")
        age_end_label.pack(anchor="w", pady=(0, 5))
        age_end_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 25", width=300)
        age_end_entry.pack(fill="x", pady=(0, 20))

        # Llenar campos si es edición
        if red_data:
            name_entry.insert(0, red_data[1])
            gender_combo.set(red_data[2])
            age_start_entry.insert(0, str(red_data[3]))
            age_end_entry.insert(0, str(red_data[4]))

        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")

        def save_red():
            """Guardar red"""
            name = name_entry.get().strip()
            gender = gender_var.get()
            age_start = age_start_entry.get().strip()
            age_end = age_end_entry.get().strip()

            # Validaciones
            if not name:
                messagebox.showerror("Error", "El nombre de la red es obligatorio")
                return

            if not age_start or not age_start.isdigit():
                messagebox.showerror("Error", "La edad mínima debe ser un número válido")
                return

            if not age_end or not age_end.isdigit():
                messagebox.showerror("Error", "La edad máxima debe ser un número válido")
                return

            try:
                # Crear instancia de Team (red)
                if red_data:  # Editar
                    team = Team(
                        id=red_data[0],
                        name=name,
                        age_start=int(age_start),
                        age_end=int(age_end),
                        gender=gender
                    )
                else:  # Agregar
                    team = Team(
                        name=name,
                        age_start=int(age_start),
                        age_end=int(age_end),
                        gender=gender
                    )

                conn = Connection.connect()
                if conn:
                    team_repo = TeamRepository(conn)
                    
                    if red_data:  # Editar
                        success = team_repo.update_team(team)
                        if success:
                            messagebox.showinfo("Éxito", f"Red '{team.name}' actualizada correctamente")
                        else:
                            messagebox.showerror("Error", "No se pudo actualizar la red")
                            return
                    else:  # Agregar
                        created_team = team_repo.create_team(team)
                        messagebox.showinfo("Éxito", f"Red '{created_team.name}' agregada correctamente")
                    
                    conn.commit()
                    conn.close()
                    dialog.destroy()
                    self.load_redes()  # Refrescar la tabla
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except ValueError as ve:
                messagebox.showerror("Error de Validación", str(ve))
            except Exception as e:
                print(f"Error al guardar red: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar red: {str(e)}")

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            width=120,
            height=40,
            command=save_red,
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

    def delete_red(self):
        """Eliminar red seleccionada"""
        if not self.selected_red:
            messagebox.showwarning("Advertencia", "Seleccione una red para eliminar")
            return

        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar la red '{self.selected_red[1]}'?"
        )

        if result:
            try:
                conn = Connection.connect()
                if conn:
                    team_repo = TeamRepository(conn)
                    success = team_repo.delete_team(self.selected_red[0])
                    
                    if success:
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Red '{self.selected_red[1]}' eliminada correctamente")
                        self.load_redes()  # Refrescar la tabla
                        self.selected_red = None  # Limpiar selección
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar la red")
                    
                    conn.close()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"Error al eliminar red: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar red: {str(e)}")

