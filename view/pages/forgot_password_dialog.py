import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class ForgotPasswordDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = False
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
        self.main_frame = ctk.CTkFrame(self.dialog, fg_color="#f5f5f5")
        self.main_frame.pack(fill="both", expand=True)
        
        # Título principal
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Modo Administrador",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        )
        self.title_label.pack(pady=(40, 15))
        
        # Descripción
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Ingrese las credenciales de administrador para recuperar el acceso:",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        self.desc_label.pack(pady=(0, 30))
        
        # Campo de usuario administrador
        self.admin_user_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Usuario Administrador",
            width=320,
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=1,
            border_color="#dee2e6",
            fg_color="#ffffff"
        )
        self.admin_user_entry.pack(pady=(0, 15))
        
        # Campo de contraseña administrador
        self.admin_password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Contraseña Administrador",
            width=320,
            height=45,
            font=ctk.CTkFont(size=14),
            show="*",
            corner_radius=8,
            border_width=1,
            border_color="#dee2e6",
            fg_color="#ffffff"
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
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.verify_admin_credentials,
            fg_color="#1f538d",
            hover_color="#0d47a1",
            corner_radius=8
        )
        self.access_button.pack(expand=True)
        
        # Centrar la ventana en la pantalla
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"450x350+{x}+{y}")
        
    def verify_admin_credentials(self):
        """Verificar credenciales de administrador"""
        username = self.admin_user_entry.get()
        password = self.admin_password_entry.get()
        
        # Validación hardcodeada: admin/admin (sin base de datos)
        if username == "admin" and password == "admin":
            # Cerrar el diálogo de administrador
            self.dialog.destroy()
            
            # Cerrar también la ventana de login principal
            self.parent.destroy()
            
            # Crear nueva ventana para el dashboard
            import customtkinter as ctk
            dashboard_window = ctk.CTk()
            dashboard_window.title("Academia Bíblica - Dashboard")
            dashboard_window.geometry("1200x800")
            dashboard_window.resizable(True, True)
            
            # Centrar la ventana
            dashboard_window.update_idletasks()
            x = (dashboard_window.winfo_screenwidth() // 2) - (1200 // 2)
            y = (dashboard_window.winfo_screenheight() // 2) - (800 // 2)
            dashboard_window.geometry(f"1200x800+{x}+{y}")
            
            # Crear el dashboard
            from .dashboard_page import DashboardPage
            dashboard = DashboardPage(dashboard_window)
            
            # Ejecutar la ventana del dashboard
            dashboard_window.mainloop()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.\nUse: admin / admin")
