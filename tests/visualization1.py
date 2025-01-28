import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Visualization:
    """Clase para visualizar la evolución de un autómata celular."""

    def __init__(self, cellular_automata):
        """
        Inicializa la visualización para un autómata celular.

        Args:
            cellular_automata: Instancia del autómata celular.
        """
        self.cellular_automata = cellular_automata
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(
            self.cellular_automata.grid,
            cmap="binary",
            interpolation="nearest",
        )
        self.ax.axis("off")  # Oculta los ejes para mayor claridad

    def render(self):
        """Actualiza y muestra la cuadrícula actual."""
        self.im.set_data(self.cellular_automata.grid)
        plt.pause(0.01)

    def animate(self, update_func, interval):
        """
        Crea una animación que actualiza la visualización en intervalos definidos.

        Args:
            update_func (callable): Función para actualizar el estado del autómata.
            interval (float): Intervalo entre actualizaciones (en segundos).
        """
        def update(frame):
            update_func()  # Actualiza el estado del autómata
            self.render()  # Actualiza la visualización

        anim = FuncAnimation(self.fig, update, interval=interval * 1000)
        plt.show()
