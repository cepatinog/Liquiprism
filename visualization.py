import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Visualization:
    """Clase para visualizar las caras de un cubo de autómatas celulares."""

    def __init__(self, cellular_automata_list):
        """
        Inicializa la visualización para múltiples caras de autómatas celulares.

        Args:
            cellular_automata_list (list): Lista de instancias de autómatas celulares.
        """
        self.cellular_automata_list = cellular_automata_list
        self.current_face_index = 0  # Cara actualmente seleccionada
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(
            self.cellular_automata_list[self.current_face_index].grid,
            cmap="binary",
            interpolation="nearest",
        )
        self.ax.axis("off")  # Oculta los ejes para mayor claridad
        self.fig.canvas.mpl_connect("key_press_event", self._on_key_press)

    def _on_key_press(self, event):
        """
        Cambia de cara al presionar las teclas izquierda o derecha.

        Args:
            event: Evento de teclado capturado por matplotlib.
        """
        if event.key == "left":
            self.current_face_index = (self.current_face_index - 1) % len(self.cellular_automata_list)
        elif event.key == "right":
            self.current_face_index = (self.current_face_index + 1) % len(self.cellular_automata_list)
        self._update_face()

    def _update_face(self):
        """Actualiza la visualización para mostrar la cara seleccionada."""
        self.im.set_data(self.cellular_automata_list[self.current_face_index].grid)
        self.fig.canvas.draw_idle()

    def render(self):
        """Actualiza y muestra la cuadrícula actual."""
        self.im.set_data(self.cellular_automata_list[self.current_face_index].grid)
        plt.pause(0.01)

    def animate(self, update_func, interval):
        """
        Crea una animación que actualiza la visualización en intervalos definidos.

        Args:
            update_func (callable): Función para actualizar el estado de los autómatas.
            interval (float): Intervalo entre actualizaciones (en segundos).
        """
        def update(frame):
            update_func()  # Actualiza el estado de todos los autómatas
            self.render()  # Actualiza la visualización

        anim = FuncAnimation(self.fig, update, interval=interval * 1000)
        plt.show()
