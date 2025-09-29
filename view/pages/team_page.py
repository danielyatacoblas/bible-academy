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


class TeamPage:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.load_teams()

    def setup_ui(self):
        """Configurar la interfaz de gestión de equipos"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(
            self.main_frame,
            text="👥 Gestión de Equipos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title.pack(pady=(0, 20))

        # Frame para botones de acción
        self.actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(0, 20))

        # Botón agregar equipo
        self.add_btn = ctk.CTkButton(
            self.actions_frame,
            text="➕ Nuevo Equipo",
            width=150,
            height=40,
            command=self.show_add_team_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        # Botón editar equipo
        self.edit_btn = ctk.CTkButton(
            self.actions_frame,
            text="✏️ Editar",
            width=120,
            height=40,
            command=self.show_edit_team_dialog,
            fg_color="#ffc107",
            hover_color="#e0a800",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.edit_btn.pack(side="left", padx=(0, 10))

        # Botón eliminar equipo
        self.delete_btn = ctk.CTkButton(
            self.actions_frame,
            text="🗑️ Eliminar",
            width=120,
            height=40,
            command=self.delete_team,
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
            command=self.load_teams,
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
        """Crear tabla para mostrar equipos"""
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
        columns = ("ID", "Nombre", "Edad Inicio", "Edad Fin", "Género")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Edad Inicio", text="Edad Inicio")
        self.tree.heading("Edad Fin", text="Edad Fin")
        self.tree.heading("Género", text="Género")

        # Configurar ancho de columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=200, anchor="w")
        self.tree.column("Edad Inicio", width=100, anchor="center")
        self.tree.column("Edad Fin", width=100, anchor="center")
        self.tree.column("Género", width=100, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind para selección
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_teams(self):
        """Cargar equipos desde la base de datos"""
        try:
            conn = Connection.connect()
            if conn:
                team_repo = TeamRepository(conn)
                teams = team_repo.get_all_rows()
                
                # Limpiar tabla
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Agregar equipos a la tabla
                for team in teams:
                    self.tree.insert("", "end", values=(
                        team["id"],
                        team["name"],
                        team["age_start"],
                        team["age_end"],
                        team["gender"]
                    ))
                
                conn.close()
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar equipos: {str(e)}")

    def on_select(self, event):
        """Manejar selección de equipo"""
        selection = self.tree.selection()
        if selection:
            self.selected_team = self.tree.item(selection[0])["values"]
        else:
            self.selected_team = None

    def show_add_team_dialog(self):
        """Mostrar diálogo para agregar nuevo equipo"""
        self.show_team_dialog("Agregar Equipo", None)

    def show_edit_team_dialog(self):
        """Mostrar diálogo para editar equipo"""
        if not self.selected_team:
            messagebox.showwarning("Advertencia", "Seleccione un equipo para editar")
            return
        
        self.show_team_dialog("Editar Equipo", self.selected_team)

    def show_team_dialog(self, title, team_data=None):
        """Mostrar diálogo para agregar/editar equipo"""
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

        # Nombre
        name_label = ctk.CTkLabel(form_frame, text="Nombre del Equipo:")
        name_label.pack(anchor="w", pady=(0, 5))
        name_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Jóvenes", width=300)
        name_entry.pack(fill="x", pady=(0, 10))

        # Edad inicio
        age_start_label = ctk.CTkLabel(form_frame, text="Edad de Inicio:")
        age_start_label.pack(anchor="w", pady=(0, 5))
        age_start_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 15", width=300)
        age_start_entry.pack(fill="x", pady=(0, 10))

        # Edad fin
        age_end_label = ctk.CTkLabel(form_frame, text="Edad de Fin:")
        age_end_label.pack(anchor="w", pady=(0, 5))
        age_end_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 25", width=300)
        age_end_entry.pack(fill="x", pady=(0, 10))

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
        gender_combo.pack(fill="x", pady=(0, 20))

        # Llenar campos si es edición
        if team_data:
            name_entry.insert(0, team_data[1])
            age_start_entry.insert(0, str(team_data[2]))
            age_end_entry.insert(0, str(team_data[3]))
            gender_combo.set(team_data[4])

        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")

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
                conn = Connection.connect()
                if conn:
                    team_repo = TeamRepository(conn)
                    
                    if team_data:  # Editar
                        team_repo.update_row(
                            {"id": team_data[0]},
                            {"name": name, "age_start": age_start, "age_end": age_end, "gender": gender}
                        )
                        messagebox.showinfo("Éxito", f"Equipo '{name}' actualizado correctamente")
                    else:  # Agregar
                        team_repo.insert_row({
                            "name": name,
                            "age_start": age_start,
                            "age_end": age_end,
                            "gender": gender
                        })
                        messagebox.showinfo("Éxito", f"Equipo '{name}' agregado correctamente")
                    
                    conn.commit()
                    conn.close()
                    dialog.destroy()
                    self.load_teams()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar equipo: {str(e)}")

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            width=120,
            height=40,
            command=save_team,
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

    def delete_team(self):
        """Eliminar equipo seleccionado"""
        if not self.selected_team:
            messagebox.showwarning("Advertencia", "Seleccione un equipo para eliminar")
            return

        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el equipo '{self.selected_team[1]}'?"
        )

        if result:
            try:
                conn = Connection.connect()
                if conn:
                    team_repo = TeamRepository(conn)
                    team_repo.delete_row({"id": self.selected_team[0]})
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("Éxito", f"Equipo '{self.selected_team[1]}' eliminado correctamente")
                    self.load_teams()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar equipo: {str(e)}")
