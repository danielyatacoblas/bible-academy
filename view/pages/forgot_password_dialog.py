import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from control.session.user_repository import UserRepository
from view import theme

class ForgotPasswordDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = False
        self.user_data = None
        self.setup_dialog()
        
    def setup_dialog(self):
        """Configurar el diálogo de olvidar contraseña"""
        # Crear ventana de diálogo
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Recuperar Contraseña")
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        
        # Centrar la ventana
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Frame principal con fondo gris claro
        self.main_frame = ctk.CTkFrame(self.dialog, fg_color=theme.BACKGROUND)
        self.main_frame.pack(fill="both", expand=True)
        
        # Título principal
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Modo Administrador",
            font=theme.font(theme.SIZE_TITLE, "bold"),
            text_color=theme.PRIMARY
        )
        self.title_label.pack(pady=(40, 15))
        
        # Descripción
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Ingrese las credenciales de administrador para recuperar el acceso:",
            font=theme.font(theme.SIZE_BODY),
            text_color=theme.TEXT_MUTED
        )
        self.desc_label.pack(pady=(0, 30))
        
        # Campo de usuario administrador
        self.admin_user_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Usuario Administrador",
            width=320,
            height=45,
            font=theme.font(theme.SIZE_BODY),
            corner_radius=8,
            border_width=1,
            border_color=theme.BORDER,
            fg_color=theme.SURFACE
        )
        self.admin_user_entry.pack(pady=(0, 15))
        
        # Campo de contraseña administrador
        self.admin_password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Contraseña Administrador",
            width=320,
            height=45,
            font=theme.font(theme.SIZE_BODY),
            show="*",
            corner_radius=8,
            border_width=1,
            border_color=theme.BORDER,
            fg_color=theme.SURFACE
        )
        self.admin_password_entry.pack(pady=(0, 30))
        
        # Frame para botones
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=(0, 20))
        
        # Solo botón acceder - centrado
        self.access_button = ctk.CTkButton(
            self.buttons_frame,
            text="Acceder",
            width=150,
            height=45,
            font=theme.font(theme.SIZE_SUBTITLE, "bold"),
            command=self.verify_admin_credentials,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            corner_radius=8
        )
        self.access_button.pack(expand=True)
        
        # Centrar la ventana en la pantalla
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"450x350+{x}+{y}")
        
    def verify_admin_credentials(self):
        """Verificar credenciales de administrador contra la base de datos"""
        username = self.admin_user_entry.get().strip()
        password = self.admin_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        try:
            user_repo = UserRepository()

            # Autenticacion real contra la base de datos (Argon2)
            if not user_repo.login(username, password):
                messagebox.showerror(
                    "Error",
                    "Credenciales incorrectas.\n"
                    "Si olvidó su contraseña, contacte al administrador del sistema."
                )
                return

            user_data = user_repo.get_user_by_username(username)
            if not user_data or user_data.get("role") != "Administrador":
                messagebox.showerror(
                    "Acceso denegado",
                    "Solo un usuario administrador puede recuperar el acceso.\n"
                    "Contacte al administrador del sistema."
                )
                return

            # Credenciales validas: informar al llamador (LoginPage)
            self.user_data = user_data
            self.result = True
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")
