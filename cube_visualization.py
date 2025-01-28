import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class CubeVisualization:
    """Clase para visualizar un cubo 3D usando PyOpenGL."""

    def __init__(self, cellular_automata_list):
        """
        Inicializa la visualización 3D del cubo.

        Args:
            cellular_automata_list (list): Lista de instancias de CellularAutomata (una por cara).
        """
        self.cellular_automata_list = cellular_automata_list
        self.grid_size = cellular_automata_list[0].grid_size

        # Colores para cada cara del cubo
        self.face_colors = [
            (1, 0, 0),  # Rojo
            (0, 1, 0),  # Verde
            (0, 0, 1),  # Azul
            (1, 1, 0),  # Amarillo
            (1, 0, 1),  # Magenta
            (0, 1, 1),  # Cyan
        ]

        # Variables de rotación
        self.rotation_x = 0
        self.rotation_y = 0
        
        # Configuración inicial de PyGame y OpenGL
        pygame.init()
        pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
        gluPerspective(45, (800 / 600), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -4)
        # Configurar el fondo blanco
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Blanco RGBA

    def draw_face(self, grid, position, rotation, color):
        """
        Dibuja una cara del cubo.

        Args:
            grid (list): Matriz de la cara.
            position (tuple): Coordenadas (x, y, z) de la cara.
            rotation (tuple): Rotación (rx, ry, rz) de la cara.
            color (tuple): Color RGB de la cara.
        """
        size = 1 / self.grid_size
        x, y, z = position
        rx, ry, rz = rotation

        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(rx, 1, 0, 0)
        glRotatef(ry, 0, 1, 0)
        glRotatef(rz, 0, 0, 1)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_state = grid[i][j]
                # Dibujar el cuadrado (relleno)
                glColor3f(*color) if cell_state == 1 else glColor3f(1, 1, 1)
                glBegin(GL_QUADS)
                glVertex3f(i * size - 0.5, j * size - 0.5, 0)
                glVertex3f(i * size - 0.5 + size, j * size - 0.5, 0)
                glVertex3f(i * size - 0.5 + size, j * size - 0.5 + size, 0)
                glVertex3f(i * size - 0.5, j * size - 0.5 + size, 0)
                glEnd()

                # Dibujar el borde (líneas negras)
                glColor3f(0, 0, 0)  # Negro
                glLineWidth(2)  # Grosor del borde
                glBegin(GL_LINE_LOOP)
                glVertex3f(i * size - 0.5, j * size - 0.5, 0)
                glVertex3f(i * size - 0.5 + size, j * size - 0.5, 0)
                glVertex3f(i * size - 0.5 + size, j * size - 0.5 + size, 0)
                glVertex3f(i * size - 0.5, j * size - 0.5 + size, 0)
                glEnd()

        glPopMatrix()

    def draw_cube(self):
        """Dibuja el cubo completo."""
        positions_rotations = [
            ((0, 0, 0.5), (0, 0, 0)),       # Frontal
            ((0, 0, -0.5), (0, 180, 0)),    # Posterior
            ((0, 0.5, 0), (-90, 0, 0)),     # Superior
            ((0, -0.5, 0), (90, 0, 0)),     # Inferior
            ((-0.5, 0, 0), (0, 90, 0)),     # Izquierda
            ((0.5, 0, 0), (0, -90, 0)),     # Derecha
        ]

        for face_idx, (position, rotation) in enumerate(positions_rotations):
            grid = self.cellular_automata_list[face_idx].grid
            color = self.face_colors[face_idx]
            self.draw_face(grid, position, rotation, color)

    # def handle_rotation(self, events):
    #     """
    #     Maneja la rotación del cubo basada en las teclas presionadas.

    #     Args:
    #         events (list): Lista de eventos capturados por Pygame.
    #     """
    #     for event in events:
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_LEFT:
    #                 self.rotation_y -= 5  # Rotar a la izquierda
    #             elif event.key == pygame.K_RIGHT:
    #                 self.rotation_y += 5  # Rotar a la derecha
    #             elif event.key == pygame.K_UP:
    #                 self.rotation_x -= 5  # Rotar hacia arriba
    #             elif event.key == pygame.K_DOWN:
    #                 self.rotation_x += 5  # Rotar hacia abajo

    # def render(self, events):
    #     """
    #     Renderiza el cubo, aplicando la rotación acumulada.

    #     Args:
    #         events (list): Lista de eventos capturados por Pygame.
    #     """
    #     self.handle_rotation(events)

    #     # Limpiar el buffer y aplicar las rotaciones
    #     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #     glPushMatrix()
    #     glRotatef(self.rotation_x, 1, 0, 0)
    #     glRotatef(self.rotation_y, 0, 1, 0)

    #     # Dibujar el cubo
    #     self.draw_cube()
    #     glPopMatrix()

    def render(self):
        """
        Renderiza el cubo, aplicando rotación automática.
        """
        # Incrementar la rotación acumulativa
        self.rotation_x += 0.1  # Ajusta este valor para cambiar la velocidad
        self.rotation_y += 0.1

        # Limpiar el buffer y aplicar las rotaciones acumuladas
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        self.draw_cube()
        glPopMatrix()
        pygame.display.flip()