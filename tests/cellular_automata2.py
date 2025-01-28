import random

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

    def randomize(self):
        """Llena la cuadrícula con valores aleatorios (0 o 1)."""
        self.grid = [[random.randint(0, 1) for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def display(self):
        """Muestra la cuadrícula en consola."""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def update(self, face_id: int, all_faces: list):
        """
        Actualiza la cuadrícula según las reglas, considerando las conexiones con otras caras.

        Args:
            face_id (int): ID de la cara actual.
            all_faces (list): Lista de todas las caras del cubo.
        """
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Obtener vecinos, incluyendo conexiones entre caras
                neighbors = self._get_neighbors(x, y, face_id, all_faces)

                # Usar la regla para determinar el nuevo estado
                new_grid[x][y] = self.rule_set(self.grid[x][y], neighbors)

        self.grid = new_grid

    def rule_set(self, x: int, y: int) -> int:
        """
        Regla para determinar el estado de una célula en la siguiente iteración.

        Args:
            x (int): Coordenada x de la célula.
            y (int): Coordenada y de la célula.

        Returns:
            int: Nuevo estado de la célula (0 o 1).
        """
        neighbors = self._get_neighbors(x, y)
        alive_neighbors = sum(neighbors)

        if self.grid[x][y] == 1:  # Célula viva
            return 1 if alive_neighbors in (2, 3) else 0
        else:  # Célula muerta
            return 1 if alive_neighbors == 3 else 0
        
    def _get_neighbors(self, x: int, y: int) -> list:
        """Obtiene el estado de los vecinos de una célula."""
        neighbors = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i == x and j == y) or i < 0 or j < 0 or i >= self.grid_size or j >= self.grid_size:
                    continue
                neighbors.append(self.grid[i][j])
        return neighbors    
    
    