import random

CUBE_NEIGHBORS = {
    0: {"up": 4, "down": 5, "left": 3, "right": 1},
    1: {"up": 4, "down": 5, "left": 0, "right": 2},
    2: {"up": 4, "down": 5, "left": 1, "right": 3},
    3: {"up": 4, "down": 5, "left": 2, "right": 0},
    4: {"up": 2, "down": 0, "left": 3, "right": 1},
    5: {"up": 0, "down": 2, "left": 3, "right": 1},
}


class CellularAutomata:
    """Clase para modelar una cuadrícula de autómatas celulares."""

    def __init__(self, grid_size: int):

        """
        Inicializa una cuadrícula vacía de autómatas celulares.
        
        Args:
            grid_size (int): Tamaño de la cuadrícula (e.g.m 10 para 10x10)
        """

        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.previous_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.activity_count = 0  # Contador de cambios de estado por iteración

    def randomize(self):
        """Llena la cuadrícula con valores aleatorios (0 o 1)."""
        self.grid = [[random.randint(0, 1) for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def display(self):
        """Muestra la cuadrícula en consola."""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def update(self, face_id: int, all_faces: list, use_stochastic_rule: bool = False):
        """
        Actualiza la cuadrícula según las reglas, considerando las conexiones con otras caras.

        Args:
            face_id (int): ID de la cara actual.
            all_faces (list): Lista de todas las caras del cubo.
        """
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.activity_count = 0

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Obtener vecinos, incluyendo conexiones entre caras
                neighbors = self._get_neighbors(x, y, face_id, all_faces)
                current_state = self.grid[x][y]

                if use_stochastic_rule:
                    new_state = self.rule_set_2(current_state, x, y, neighbors)
                else:
                    new_state = self.rule_set_1(current_state, neighbors)

                if new_state != current_state:
                    self.activity_count += 1
                new_grid[x][y] = new_state

        # Almacenar el estado actual como el estado anterior antes de actualizar
        self.previous_grid = [row[:] for row in self.grid]
        self.grid = new_grid
        
        # print(f"Actualizando cara {face_id}")
        # for row in self.grid:
        #     print(row)
        


    def rule_set_1(self, current_state: int, neighbors: list) -> int:
        """
        Regla convencional para actualizar una célula.

        Args:
            current_state (int): Estado actual de la célula (0 o 1).
            neighbors (list): Lista de estados de los vecinos.

        Returns:
            int: Nuevo estado de la célula (0 o 1).
        """
        alive_neighbors = sum(neighbors)

        if current_state == 1:  # Célula viva
            return 1 if alive_neighbors in (2, 3) else 0
        else:  # Célula muerta
            return 1 if alive_neighbors == 4 else 0

    def rule_set_2(self, current_state: int, x: int, y: int, neighbors: list) -> int:
        """
        Regla estocástica para actualizar una célula.

        Args:
            x (int): Coordenada x de la célula.
            y (int): Coordenada y de la célula.
            neighbors (list): Lista de estados de los vecinos.

        Returns:
            int: Nuevo estado de la célula (0 o 1).
        """
        alive_neighbors = sum(neighbors)
        below_neighbor = self.grid[x + 1][y] if x + 1 < self.grid_size else 0

        if current_state == 1:  # Célula viva
            return 1 if alive_neighbors in (2, 3) else 0
        else:  # Célula muerta
            return 1 if below_neighbor == 1 and random.random() < 0.33 else 0
        
    def _get_neighbors(self, x: int, y: int, face_id: int, all_faces: list) -> list:
        """
        Obtiene los vecinos de una célula, incluyendo los bordes que interactúan con las caras vecinas.

        Args:
            x (int): Coordenada x de la célula.
            y (int): Coordenada y de la célula.
            face_id (int): ID de la cara actual.
            all_faces (list): Lista de todas las caras del cubo (instancias de CellularAutomata).

        Returns:
            list: Lista de estados de los vecinos.
        """
        neighbors = []

        # Validar caras vecinas
        if face_id not in CUBE_NEIGHBORS or not all_faces:
            raise ValueError("CUBE_NEIGHBORS o all_faces están mal configurados.")

        # Obtener vecinos dentro de la misma cara
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
                    neighbors.append(self.grid[i][j])

        # Obtener vecinos de las caras vecinas
        for direction, neighbor_face_id in CUBE_NEIGHBORS[face_id].items():
            neighbor_face = all_faces[neighbor_face_id]
            if direction == "up" and x == 0:  # Borde superior
                neighbors.extend(neighbor_face.grid[-1][y:y+1])  # Última fila de la cara vecina
            elif direction == "down" and x == self.grid_size - 1:  # Borde inferior
                neighbors.extend(neighbor_face.grid[0][y:y+1])  # Primera fila de la cara vecina
            elif direction == "left" and y == 0:  # Borde izquierdo
                neighbors.append(neighbor_face.grid[x][-1])  # Última columna de la cara vecina
            elif direction == "right" and y == self.grid_size - 1:  # Borde derecho
                neighbors.append(neighbor_face.grid[x][0])  # Primera columna de la cara vecina

        return neighbors    
    
    