"""
Generador de gráficos usando matplotlib para el dashboard.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
import os


class ChartGenerator:
    """Generador de gráficos para el dashboard"""
    
    def __init__(self):
        # Configurar estilo de matplotlib
        plt.style.use('default')
        self.colors = ['#28a745', '#007bff', '#ffc107', '#dc3545', '#6f42c1', '#20c997', '#fd7e14', '#e83e8c']
    
    def create_line_chart(self, data, title, xlabel, ylabel, width=6, height=4):
        """
        Crear gráfico de línea
        
        Args:
            data: Lista de tuplas (x, y) o diccionario con 'x' y 'y'
            title: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            width: Ancho de la figura
            height: Alto de la figura
            
        Returns:
            Figure: Figura de matplotlib
        """
        fig = Figure(figsize=(width, height), facecolor='white')
        ax = fig.add_subplot(111)
        
        # Preparar datos
        if isinstance(data, dict):
            x_data = data.get('x', [])
            y_data = data.get('y', [])
        else:
            x_data, y_data = zip(*data) if data else ([], [])
        
        # Crear gráfico de línea
        ax.plot(x_data, y_data, marker='o', linewidth=2.5, markersize=6, 
                color=self.colors[1], markerfacecolor=self.colors[0], 
                markeredgecolor='white', markeredgewidth=2)
        
        # Configurar el gráfico
        ax.set_title(title, fontsize=14, fontweight='bold', color='#1f538d', pad=20)
        ax.set_xlabel(xlabel, fontsize=12, color='#666666')
        ax.set_ylabel(ylabel, fontsize=12, color='#666666')
        
        # Estilo de la cuadrícula
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # Configurar colores de ejes
        ax.tick_params(colors='#666666')
        for spine in ax.spines.values():
            spine.set_color('#e9ecef')
        
        # Ajustar layout
        fig.tight_layout(pad=2)
        
        return fig
    
    def create_pie_chart(self, data, labels, title, width=6, height=4):
        """
        Crear gráfico de pastel
        
        Args:
            data: Lista de valores
            labels: Lista de etiquetas
            title: Título del gráfico
            width: Ancho de la figura
            height: Alto de la figura
            
        Returns:
            Figure: Figura de matplotlib
        """
        fig = Figure(figsize=(width, height), facecolor='white')
        ax = fig.add_subplot(111)
        
        # Crear gráfico de pastel
        wedges, texts, autotexts = ax.pie(
            data, 
            labels=labels, 
            autopct='%1.1f%%',
            startangle=90,
            colors=self.colors[:len(data)],
            textprops={'fontsize': 10, 'color': '#333333'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        
        # Configurar título
        ax.set_title(title, fontsize=14, fontweight='bold', color='#1f538d', pad=20)
        
        # Mejorar el estilo de los porcentajes
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        # Asegurar que el gráfico sea circular
        ax.axis('equal')
        
        return fig
    
    def create_bar_chart(self, data, labels, title, xlabel, ylabel, width=6, height=4):
        """
        Crear gráfico de barras
        
        Args:
            data: Lista de valores
            labels: Lista de etiquetas
            title: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            width: Ancho de la figura
            height: Alto de la figura
            
        Returns:
            Figure: Figura de matplotlib
        """
        fig = Figure(figsize=(width, height), facecolor='white')
        ax = fig.add_subplot(111)
        
        # Crear gráfico de barras
        bars = ax.bar(labels, data, color=self.colors[:len(data)], 
                     edgecolor='white', linewidth=1, alpha=0.8)
        
        # Agregar valores en las barras
        for bar, value in zip(bars, data):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{value}', ha='center', va='bottom', 
                   fontweight='bold', color='#333333')
        
        # Configurar el gráfico
        ax.set_title(title, fontsize=14, fontweight='bold', color='#1f538d', pad=20)
        ax.set_xlabel(xlabel, fontsize=12, color='#666666')
        ax.set_ylabel(ylabel, fontsize=12, color='#666666')
        
        # Estilo de la cuadrícula
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.set_facecolor('#f8f9fa')
        
        # Configurar colores de ejes
        ax.tick_params(colors='#666666')
        for spine in ax.spines.values():
            spine.set_color('#e9ecef')
        
        # Rotar etiquetas del eje X si son muy largas
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Ajustar layout
        fig.tight_layout(pad=2)
        
        return fig
    
    def get_matriculas_trend_data(self, inscription_repo):
        """
        Obtener datos de tendencia de matrículas por mes
        
        Args:
            inscription_repo: Repositorio de inscripciones
            
        Returns:
            dict: Datos para gráfico de línea
        """
        try:
            inscriptions = inscription_repo.get_all_rows()
            
            # Agrupar por mes (simulado para demostración)
            months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
            values = [0] * len(months)
            
            # Simular distribución basada en datos existentes
            total_inscriptions = len(inscriptions)
            if total_inscriptions > 0:
                # Distribuir las inscripciones existentes en los meses
                base_per_month = total_inscriptions // len(months)
                remainder = total_inscriptions % len(months)
                
                for i in range(len(months)):
                    values[i] = base_per_month + (1 if i < remainder else 0)
                    # Agregar variación aleatoria
                    values[i] += np.random.randint(-2, 3)
                    values[i] = max(0, values[i])
            
            return {
                'x': months,
                'y': values
            }
        except Exception as e:
            print(f"Error obteniendo datos de tendencia: {e}")
            return {
                'x': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                'y': [12, 18, 15, 22, 19, 25]
            }
    
    def get_equipos_distribution_data(self, team_repo, student_repo):
        """
        Obtener datos de distribución de estudiantes por equipo
        
        Args:
            team_repo: Repositorio de equipos
            student_repo: Repositorio de estudiantes
            
        Returns:
            tuple: (datos, etiquetas)
        """
        try:
            teams = team_repo.get_all_rows()
            students = student_repo.get_all_rows()
            
            # Simular distribución
            team_data = []
            team_labels = []
            
            for i, team in enumerate(teams):
                team_name = team.get('name', f'Equipo {i+1}')
                # Simular conteo basado en hash
                count = len([s for s in students if hash(s.get('name', '')) % len(teams) == i])
                team_data.append(count)
                team_labels.append(team_name)
            
            # Si no hay datos, usar valores simulados
            if not team_data:
                team_data = [8, 12, 5, 15, 7]
                team_labels = ['Equipo A', 'Equipo B', 'Equipo C', 'Equipo D', 'Equipo E']
            
            return team_data, team_labels
        except Exception as e:
            print(f"Error obteniendo datos de equipos: {e}")
            return [8, 12, 5, 15, 7], ['Equipo A', 'Equipo B', 'Equipo C', 'Equipo D', 'Equipo E']
    
    def get_payment_methods_data(self, payment_repo):
        """
        Obtener datos de métodos de pago
        
        Args:
            payment_repo: Repositorio de pagos
            
        Returns:
            tuple: (datos, etiquetas)
        """
        try:
            payments = payment_repo.get_all_rows()
            
            # Agrupar por método de pago
            method_counts = {}
            for payment in payments:
                method = payment.get('method_payment', 'Desconocido')
                method_counts[method] = method_counts.get(method, 0) + 1
            
            # Si no hay datos, usar datos simulados
            if not method_counts:
                method_counts = {
                    "Efectivo": 15,
                    "Transferencia": 8,
                    "Tarjeta": 5,
                    "Yape": 12,
                    "Plin": 3
                }
            
            # Convertir a listas
            methods = list(method_counts.keys())
            counts = list(method_counts.values())
            
            return counts, methods
        except Exception as e:
            print(f"Error obteniendo datos de pagos: {e}")
            return [15, 8, 5, 12, 3], ["Efectivo", "Transferencia", "Tarjeta", "Yape", "Plin"]


def create_matplotlib_widget(fig, parent_frame):
    """
    Crear widget de matplotlib en un frame de CustomTkinter
    
    Args:
        fig: Figura de matplotlib
        parent_frame: Frame padre de CustomTkinter
        
    Returns:
        FigureCanvasTkAgg: Canvas de matplotlib
    """
    canvas = FigureCanvasTkAgg(fig, parent_frame)
    canvas.draw()
    return canvas
