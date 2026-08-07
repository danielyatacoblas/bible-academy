import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from control.session.user_repository import UserRepository
from control.bd.db_connection import Connection

class LoginPage:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de login"""
        # Configurar tema claro por defecto
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Configurar fondo claro como en la imagen
        self.parent.configure(bg="#f5f5f5")
        
        # Frame principal con fondo claro
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="#f5f5f5")
        self.main_frame.pack(fill="both", expand=True)
        
        # Frame central para el login (panel claro) - como en la imagen
        self.login_frame = ctk.CTkFrame(
            self.main_frame, 
            width=380, 
            height=480,
            fg_color="#ffffff",
            corner_radius=12
        )
        self.login_frame.pack(expand=True, fill="both")
        self.login_frame.pack_propagate(False)
        
        # Logo/Icono usando la imagen iacym.jpg
        import os
        
        # Crear frame para el logo
        self.logo_frame = ctk.CTkFrame(
            self.login_frame, 
            width=80, 
            height=80, 
            fg_color="#1f538d",
            corner_radius=10
        )
        self.logo_frame.pack(pady=(50, 20))
        self.logo_frame.pack_propagate(False)
        
        # Cargar la imagen del logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "view", "images", "iacym.jpg")
        
        try:
            from PIL import Image, ImageTk
            
            if os.path.exists(logo_path):
                # Cargar y redimensionar la imagen
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
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
                    text_color="white"
                )
                self.logo_text.pack(expand=True)
        except ImportError:
            # Si no hay PIL, usar texto como fallback
            self.logo_text = ctk.CTkLabel(
                self.logo_frame,
                text="AB",
                font=ctk.CTkFont(size=25, weight="bold"),
                text_color="white"
            )
            self.logo_text.pack(expand=True)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.login_frame,
            text="Academia Bíblica",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#1f538d"
        )
        self.title_label.pack(pady=(0, 40))
        
        # Campo de usuario
        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Usuario",
            width=280,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=1,
            border_color="#dee2e6"
        )
        self.username_entry.pack(pady=(0, 15))
        
        # Campo de contraseña
        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Contraseña",
            width=280,
            height=40,
            font=ctk.CTkFont(size=14),
            show="*",
            corner_radius=8,
            border_width=1,
            border_color="#dee2e6"
        )
        self.password_entry.pack(pady=(0, 30))
        
        # Botón de iniciar sesión
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Iniciar Sesión",
            width=280,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.login_attempt,
            fg_color="#6c757d",
            hover_color="#5a6268",
            corner_radius=8
        )
        self.login_button.pack(pady=(0, 20))
        
        # Enlace de olvidar contraseña
        self.forgot_password_label = ctk.CTkLabel(
            self.login_frame,
            text="Olvide mi contraseña",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d",
            cursor="hand2"
        )
        self.forgot_password_label.pack(pady=(0, 30))
        self.forgot_password_label.bind("<Button-1>", self.show_forgot_password_dialog)
        
    def login_attempt(self):
        """Manejar intento de login con autenticación real"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        # Autenticar usuario con la base de datos usando Argon2
        try:
            user_repo = UserRepository()
            if user_repo.login(username, password):
                # Obtener información completa del usuario
                user_data = user_repo.get_user_by_username(username)
                if user_data:
                    messagebox.showinfo("Éxito", f"Bienvenido {username}!")
                    
                    # Cerrar la ventana de login
                    self.parent.destroy()
                    
                    # Crear nueva ventana para el dashboard con información del usuario
                    self.create_dashboard_window(user_data)
                else:
                    messagebox.showerror("Error", "No se pudo obtener información del usuario")
            else:
                messagebox.showerror("Error", "Credenciales incorrectas. Intente nuevamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")
        
    def show_forgot_password_dialog(self, event):
        """Mostrar diálogo de olvidar contraseña"""
        from .forgot_password_dialog import ForgotPasswordDialog
        dialog = ForgotPasswordDialog(self.parent)
        self.parent.wait_window(dialog.dialog)
        
        # Si el diálogo autenticó correctamente contra la base de datos,
        # navegar al dashboard con los datos reales del usuario
        if dialog.result and dialog.user_data:
            # Cerrar la ventana de login
            self.parent.destroy()

            # Crear nueva ventana para el dashboard
            self.create_dashboard_window(dialog.user_data)
    
    def create_dashboard_window(self, user_data=None):
        """Crear nueva ventana para el dashboard"""
        # Crear nueva ventana
        dashboard_window = ctk.CTk()
        dashboard_window.title("Academia Bíblica - Dashboard")
        dashboard_window.geometry("1200x800")
        dashboard_window.resizable(True, True)
        
        # Centrar la ventana
        dashboard_window.update_idletasks()
        x = (dashboard_window.winfo_screenwidth() // 2) - (1200 // 2)
        y = (dashboard_window.winfo_screenheight() // 2) - (800 // 2)
        dashboard_window.geometry(f"1200x800+{x}+{y}")
        
        # Crear el dashboard con información del usuario
        from .dashboard_page import DashboardPage
        dashboard = DashboardPage(dashboard_window, user_data)
        
        # Ejecutar la ventana del dashboard
        dashboard_window.mainloop()
    
    def navigate_to_dashboard(self):
        """Navegar al dashboard"""
        # Limpiar la ventana actual
        self.main_frame.destroy()
        
        # Crear información de usuario por defecto
        default_user_data = {"user": "Usuario", "role": "Usuario"}
        
        # Crear y mostrar el dashboard
        from .dashboard_page import DashboardPage
        dashboard = DashboardPage(self.parent, default_user_data)
