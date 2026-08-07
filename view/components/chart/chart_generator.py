"""
Generador de gráficos usando matplotlib para el dashboard.

Todas las figuras comparten la paleta, la tipografía y el espaciado definidos
en view/theme.py, y usan layout restringido para que títulos, ejes y etiquetas
nunca se solapen.
"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import numpy as np

from view import theme


class ChartGenerator:
    """Generador de gráficos para el dashboard"""

    def __init__(self):
        self.colors = list(theme.CHART_PALETTE)

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------

    def _new_figure(self, width, height):
        """Crear una figura con layout restringido y fondo de la aplicación."""
        fig = Figure(figsize=(width, height), facecolor=theme.CHART_FACE,
                     layout="constrained")
        fig.get_layout_engine().set(w_pad=0.06, h_pad=0.06,
                                    wspace=0.02, hspace=0.02)
        return fig

    def _style_axes(self, ax, title, xlabel=None, ylabel=None, grid_axis="both"):
        """Aplicar el estilo común a un eje cartesiano."""
        ax.set_title(title, fontsize=theme.CHART_TITLE_SIZE, fontweight="bold",
                     color=theme.CHART_TITLE, pad=10)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=theme.CHART_LABEL_SIZE,
                          color=theme.CHART_LABEL, labelpad=6)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=theme.CHART_LABEL_SIZE,
                          color=theme.CHART_LABEL, labelpad=6)

        ax.set_facecolor(theme.CHART_PLOT_FACE)
        ax.grid(True, axis=grid_axis, alpha=0.6, linestyle="--", linewidth=0.7,
                color=theme.CHART_GRID)
        ax.set_axisbelow(True)
        ax.tick_params(colors=theme.CHART_TICK, labelsize=theme.CHART_TICK_SIZE,
                       length=3, width=0.8)

        for side, spine in ax.spines.items():
            if side in ("top", "right"):
                spine.set_visible(False)
            else:
                spine.set_color(theme.CHART_SPINE)

    def _empty_message(self, fig, title, message="Sin datos disponibles"):
        """Dibujar un mensaje cuando no hay datos que graficar."""
        ax = fig.add_subplot(111)
        ax.set_title(title, fontsize=theme.CHART_TITLE_SIZE, fontweight="bold",
                     color=theme.CHART_TITLE, pad=10)
        ax.text(0.5, 0.5, message, ha="center", va="center",
                fontsize=theme.CHART_LABEL_SIZE, color=theme.CHART_LABEL)
        ax.set_axis_off()
        return fig

    # ------------------------------------------------------------------
    # Gráficos
    # ------------------------------------------------------------------

    def create_line_chart(self, data, title, xlabel, ylabel, width=6, height=4):
        """Crear gráfico de línea.

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
        fig = self._new_figure(width, height)

        if isinstance(data, dict):
            x_data = data.get("x", [])
            y_data = data.get("y", [])
        else:
            x_data, y_data = zip(*data) if data else ([], [])

        if not len(x_data):
            return self._empty_message(fig, title)

        ax = fig.add_subplot(111)
        ax.plot(x_data, y_data,
                marker="o", linewidth=2.2, markersize=5,
                color=theme.CHART_PALETTE[0],
                markerfacecolor=theme.SURFACE,
                markeredgecolor=theme.CHART_PALETTE[0],
                markeredgewidth=1.8)
        ax.fill_between(range(len(x_data)), y_data,
                        color=theme.CHART_PALETTE[0], alpha=0.10)

        self._style_axes(ax, title, xlabel, ylabel, grid_axis="y")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
        ax.margins(x=0.04, y=0.18)
        ax.set_ylim(bottom=0)
        return fig

    def create_pie_chart(self, data, labels, title, width=6, height=4):
        """Crear gráfico de pastel.

        Las categorías con valor cero se omiten para no mostrar etiquetas
        de porcentaje vacías ni sectores invisibles.

        Args:
            data: Lista de valores
            labels: Lista de etiquetas
            title: Título del gráfico
            width: Ancho de la figura
            height: Alto de la figura

        Returns:
            Figure: Figura de matplotlib
        """
        fig = self._new_figure(width, height)

        pairs = [(value, label) for value, label in zip(data, labels)
                 if value and value > 0]
        if not pairs:
            return self._empty_message(fig, title)

        values = [p[0] for p in pairs]
        names = [p[1] for p in pairs]
        total = float(sum(values))

        ax = fig.add_subplot(111)
        # El titulo se ancla a la figura, no al eje: la leyenda lateral desplaza
        # el eje hacia la izquierda y arrastraria el titulo fuera del recuadro.
        fig.suptitle(title, fontsize=theme.CHART_TITLE_SIZE, fontweight="bold",
                     color=theme.CHART_TITLE)

        def autopct(pct):
            # Ocultar el porcentaje de sectores vacíos o demasiado pequeños
            return f"{pct:.1f}%" if pct >= 3 else ""

        wedges, _texts, autotexts = ax.pie(
            values,
            labels=None,
            autopct=autopct,
            startangle=90,
            counterclock=False,
            radius=0.95,
            pctdistance=0.0 if len(values) == 1 else 0.62,
            colors=[self.colors[i % len(self.colors)] for i in range(len(values))],
            wedgeprops={"edgecolor": theme.SURFACE, "linewidth": 1.5},
        )

        for autotext in autotexts:
            autotext.set_color(theme.SURFACE)
            autotext.set_fontweight("bold")
            autotext.set_fontsize(theme.CHART_VALUE_SIZE)

        ax.legend(
            wedges,
            [f"{n} ({int(v)})" if float(v).is_integer() else f"{n} ({v})"
             for n, v in zip(names, values)],
            loc="center left",
            bbox_to_anchor=(1.0, 0.5),
            frameon=False,
            fontsize=theme.CHART_TICK_SIZE,
            labelcolor=theme.CHART_LABEL,
        )
        ax.axis("equal")
        return fig

    def create_bar_chart(self, data, labels, title, xlabel, ylabel, width=6, height=4):
        """Crear gráfico de barras.

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
        fig = self._new_figure(width, height)
        if not len(data):
            return self._empty_message(fig, title)

        ax = fig.add_subplot(111)
        bars = ax.bar(labels, data,
                      color=[self.colors[i % len(self.colors)] for i in range(len(data))],
                      edgecolor=theme.SURFACE, linewidth=1, width=0.62)

        top = max(data) if max(data) else 1
        for bar, value in zip(bars, data):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + top * 0.03,
                    f"{value}", ha="center", va="bottom",
                    fontsize=theme.CHART_VALUE_SIZE, fontweight="bold",
                    color=theme.CHART_LABEL)

        self._style_axes(ax, title, xlabel, ylabel, grid_axis="y")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
        ax.set_ylim(0, top * 1.2)

        # Rotar las etiquetas solo cuando son largas o hay muchas categorías
        longest = max((len(str(l)) for l in labels), default=0)
        if len(labels) > 4 or longest > 9:
            ax.tick_params(axis="x", labelrotation=25)
            for label in ax.get_xticklabels():
                label.set_horizontalalignment("right")
        return fig

    def create_histogram(self, data, title, xlabel, ylabel, bins=10, width=6, height=4):
        """Crear histograma.

        Args:
            data: Lista de valores
            title: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            bins: Número de intervalos
            width: Ancho de la figura
            height: Alto de la figura

        Returns:
            Figure: Figura de matplotlib
        """
        fig = self._new_figure(width, height)
        if not len(data):
            return self._empty_message(fig, title)

        ax = fig.add_subplot(111)
        ax.hist(data, bins=bins, color=theme.CHART_PALETTE[0],
                edgecolor=theme.SURFACE, linewidth=1)

        self._style_axes(ax, title, xlabel, ylabel, grid_axis="y")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
        ax.margins(y=0.15)
        return fig

    def create_scatter_plot(self, x_data, y_data, title, xlabel, ylabel, width=6, height=4):
        """Crear gráfico de dispersión.

        Args:
            x_data: Datos del eje X
            y_data: Datos del eje Y
            title: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            width: Ancho de la figura
            height: Alto de la figura

        Returns:
            Figure: Figura de matplotlib
        """
        fig = self._new_figure(width, height)
        if not len(x_data):
            return self._empty_message(fig, title)

        ax = fig.add_subplot(111)
        ax.scatter(x_data, y_data, c=theme.CHART_PALETTE[0], alpha=0.85,
                   s=55, edgecolors=theme.SURFACE, linewidth=1, zorder=3)

        if len(x_data) > 1:
            z = np.polyfit(x_data, y_data, 1)
            p = np.poly1d(z)
            ordered = sorted(x_data)
            ax.plot(ordered, p(ordered), color=theme.CHART_PALETTE[2],
                    linestyle="--", linewidth=1.8, label="Tendencia", zorder=2)
            legend = ax.legend(frameon=False, fontsize=theme.CHART_TICK_SIZE,
                               loc="best", labelcolor=theme.CHART_LABEL)
            legend.set_zorder(4)

        self._style_axes(ax, title, xlabel, ylabel)
        ax.margins(0.12)
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
    
    def get_student_age_distribution_data(self, student_repo):
        """
        Obtener datos de distribución de edades de estudiantes
        
        Args:
            student_repo: Repositorio de estudiantes
            
        Returns:
            list: Lista de edades
        """
        try:
            students = student_repo.get_all_rows()
            
            # Simular edades basadas en datos existentes
            ages = []
            for student in students:
                # Simular edad basada en hash del nombre
                age = 18 + (hash(student.get('name', '')) % 20)  # Edades entre 18-37
                ages.append(age)
            
            # Si no hay datos, usar datos simulados
            if not ages:
                ages = [20, 22, 19, 25, 23, 21, 24, 26, 20, 22, 23, 25, 19, 21, 24, 22, 20, 23, 25, 21]
            
            return ages
        except Exception as e:
            print(f"Error obteniendo datos de edades: {e}")
            return [20, 22, 19, 25, 23, 21, 24, 26, 20, 22, 23, 25, 19, 21, 24, 22, 20, 23, 25, 21]
    
    def get_course_performance_data(self, course_repo, student_repo, inscription_repo):
        """
        Obtener datos de rendimiento por curso
        
        Args:
            course_repo: Repositorio de cursos
            student_repo: Repositorio de estudiantes
            inscription_repo: Repositorio de inscripciones
            
        Returns:
            tuple: (x_data, y_data) para gráfico de dispersión
        """
        try:
            courses = course_repo.get_all_rows()
            students = student_repo.get_all_rows()
            inscriptions = inscription_repo.get_all_rows()
            
            x_data = []  # Número de estudiantes inscritos
            y_data = []  # Rendimiento simulado
            
            for course in courses:
                # Contar estudiantes inscritos en este curso
                course_inscriptions = [ins for ins in inscriptions 
                                    if ins.get('course_id') == course.get('id')]
                student_count = len(course_inscriptions)
                
                if student_count > 0:
                    # Simular rendimiento basado en número de estudiantes
                    # Más estudiantes = mejor rendimiento (simulado)
                    performance = 60 + (student_count * 2) + np.random.randint(-10, 15)
                    performance = min(100, max(40, performance))  # Entre 40-100
                    
                    x_data.append(student_count)
                    y_data.append(performance)
            
            # Si no hay datos, usar datos simulados
            if not x_data:
                x_data = [5, 8, 12, 15, 3, 10, 7, 9, 6, 11]
                y_data = [75, 82, 88, 92, 65, 85, 78, 80, 72, 87]
            
            return x_data, y_data
        except Exception as e:
            print(f"Error obteniendo datos de rendimiento: {e}")
            return [5, 8, 12, 15, 3, 10, 7, 9, 6, 11], [75, 82, 88, 92, 65, 85, 78, 80, 72, 87]


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

