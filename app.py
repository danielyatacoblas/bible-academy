import customtkinter as ctk
import tkinter as tk
import sys
import os

# Agregar el directorio raíz al path para importar controladores
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from control.init_database import init_database
from view.pages.login_page import LoginPage

class BibleAcademyApp:

    def __init__(self):
        # Inicializar la base de datos primero
        init_database()
        
        self.root = ctk.CTk()
        self.root.title("Academia Bíblica")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        try:
            self.root.iconbitmap('view/images/iacym.ico')
        except:
            pass 
        
        self.center_window()
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Iniciar con la página de login
        self.show_login()
        
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def show_login(self):
        """Mostrar la página de login"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.login_page = LoginPage(self.root)
        
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BibleAcademyApp()
    app.run()
    