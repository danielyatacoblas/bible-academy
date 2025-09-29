#!/usr/bin/env python3
"""
Script para inicializar todas las tablas de la base de datos
"""

import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from control.bd.db_connection import Connection
from control.session.user_repository import UserRepository
from control.student_repository import StudentRepository
from control.teacher_repository import TeacherRepository
from control.team_repository import TeamRepository
from control.course_repository import CourseRepository
from control.classroom_repository import ClassroomRepository
from control.cicle_repository import CicleRepository
from control.inscription_repository import InscriptionRepository
from control.payment_repository import PaymentRepository

def init_database():
    """Inicializar todas las tablas de la base de datos"""
    print("Inicializando base de datos...")
    
    try:
        # Crear conexión
        conn = Connection.connect()
        if not conn:
            print("Error: No se pudo conectar a la base de datos")
            return False
        
        # Crear todas las tablas
        repositories = [
            UserRepository(conn),
            TeamRepository(conn),
            StudentRepository(conn),
            TeacherRepository(conn),
            CourseRepository(conn),
            ClassroomRepository(conn),
            CicleRepository(conn),
            InscriptionRepository(conn),
            PaymentRepository(conn)
        ]
        
        for repo in repositories:
            print(f"Creando tabla {repo.table}...")
            repo.create_table()
        
        # Crear usuario administrador por defecto
        user_repo = UserRepository(conn)
        existing_admin = user_repo.get_row_value({"user": "admin"})
        if not existing_admin:
            print("Creando usuario administrador por defecto...")
            user_repo.create_user("admin", "Administrador", "admin")
            print("Usuario admin creado: admin/admin")
        
        conn.commit()
        conn.close()
        
        print("Base de datos inicializada correctamente")
        return True
        
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        return False

if __name__ == "__main__":
    init_database()
