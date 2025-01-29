import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class CubeVisualization:
    """Class to visualize a 3D cube using PyOpenGL."""

    def __init__(self, cellular_automata_list):
        """
        Initializes the 3D visualization of the cube.

        Args:
            cellular_automata_list (list): List of CellularAutomata instances (one for each face).
        """
        self.cellular_automata_list = cellular_automata_list
        self.grid_size = cellular_automata_list[0].grid_size

        # Colors for each face of the cube
        self.face_colors = [
            (1, 0, 0),  # Red
            (0, 1, 0),  # Green
            (0, 0, 1),  # Blue
            (1, 1, 0),  # Yellow
            (1, 0, 1),  # Magenta
            (0, 1, 1),  # Cyan
        ]

        # Rotation variables
        self.rotation_x = 0
        self.rotation_y = 0
        
        # Initial configuration for PyGame and OpenGL
        pygame.init()
        pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
        gluPerspective(45, (800 / 600), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -4)

        # OpenGL configuration
        glEnable(GL_DEPTH_TEST)  # Enable depth buffer
        glClearColor(1.0, 1.0, 1.0, 1.0)  # White background

    def draw_face(self, grid, position, rotation, color):
        """
        Draws a face of the cube.

        Args:
            grid (list): Matrix of the face.
            position (tuple): Coordinates (x, y, z) of the face.
            rotation (tuple): Rotation (rx, ry, rz) of the face.
            color (tuple): RGB color of the face.
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
                # Draw the square (filled)
                glColor3f(*color) if cell_state == 1 else glColor3f(1, 1, 1)
                glBegin(GL_QUADS)
                glVertex3f(i * size - 0.5, j * size - 0.5, 0)
                glVertex3f(i * size - 0.5 + size, j * size - 0.5, 0)
                glVertex3f(i * size - 0.5 + size, j * size - 0.5 + size, 0)
                glVertex3f(i * size - 0.5, j * size - 0.5 + size, 0)
                glEnd()

                # Draw the border (black lines)
                glColor3f(0, 0, 0)  # Black
                glLineWidth(2)  # Border thickness
                glBegin(GL_LINE_LOOP)
                glVertex3f(i * size - 0.5, j * size - 0.5, 0)
                glVertex3f(i * size - 0.5 + size, j * size - 0.5, 0)
                glVertex3f(i * size - 0.5 + size, j * size - 0.5 + size, 0)
                glVertex3f(i * size - 0.5, j * size - 0.5 + size, 0)
                glEnd()

        glPopMatrix()

    def draw_cube(self):
        """Draws the complete cube."""
        positions_rotations = [
            ((0, 0, 0.5), (0, 0, 0)),       # Front
            ((0, 0, -0.5), (0, 180, 0)),    # Back
            ((0, 0.5, 0), (-90, 0, 0)),     # Top
            ((0, -0.5, 0), (90, 0, 0)),     # Bottom
            ((-0.5, 0, 0), (0, 90, 0)),     # Left
            ((0.5, 0, 0), (0, -90, 0)),     # Right
        ]

        for face_idx, (position, rotation) in enumerate(positions_rotations):
            grid = self.cellular_automata_list[face_idx].grid
            color = self.face_colors[face_idx]
            self.draw_face(grid, position, rotation, color)

    def render(self):
        """
        Renders the cube, applying automatic rotation.
        """
        # Increment cumulative rotation
        self.rotation_x = (self.rotation_x + 0.1) % 360
        self.rotation_y = (self.rotation_y + 0.1) % 360

        # Clear the buffer and apply cumulative rotations
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        self.draw_cube()
        glPopMatrix()
        pygame.display.flip()
