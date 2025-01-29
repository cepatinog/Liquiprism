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
    """Class to model a cellular automaton grid."""

    def __init__(self, grid_size: int):

        """
        Initializes an empty cellular automaton grid.
        
        Args:
            grid_size (int): Grid size (e.g., 10 for a 10x10 grid).
        """


        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.previous_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.activity_count = 0  # Counter for state changes per iteration

    def randomize(self):
        """Fills the grid with random values (0 or 1)."""
        self.grid = [[random.randint(0, 1) for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def display(self):
        """Displays the grid in the console."""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def update(self, face_id: int, all_faces: list, use_stochastic_rule: bool = False):
        """
        Updates the grid according to the rules, considering the connections with other faces.

        Args:
            face_id (int): ID of the current face.
            all_faces (list): List of all cube faces.
        """
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.activity_count = 0

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Get neighbors, including connections between faces
                neighbors = self._get_neighbors(x, y, face_id, all_faces)
                current_state = self.grid[x][y]

                if use_stochastic_rule:
                    new_state = self.rule_set_2(current_state, x, y, neighbors)
                else:
                    new_state = self.rule_set_1(current_state, neighbors)

                if new_state != current_state:
                    self.activity_count += 1
                new_grid[x][y] = new_state

        # Store the current state as the previous state before updating
        self.previous_grid = [row[:] for row in self.grid]
        self.grid = new_grid


    def rule_set_1(self, current_state: int, neighbors: list) -> int:
        """
        Conventional rule to update a cell.

        Args:
            current_state (int): Current state of the cell (0 or 1).
            neighbors (list): List of neighboring states.

        Returns:
            int: New state of the cell (0 or 1).
        """
        alive_neighbors = sum(neighbors)

        if current_state == 1:  # Living cell
            return 1 if alive_neighbors in (2, 3) else 0
        else:  # Dead cell
            return 1 if alive_neighbors == 4 else 0

    def rule_set_2(self, current_state: int, x: int, y: int, neighbors: list) -> int:
        """
        Stochastic rule to update a cell.

        Args:
            x (int): x-coordinate of the cell.
            y (int): y-coordinate of the cell.
            neighbors (list): List of neighboring states.

        Returns:
            int: New state of the cell (0 or 1).
        """
        alive_neighbors = sum(neighbors)
        below_neighbor = self.grid[x + 1][y] if x + 1 < self.grid_size else 0

        if current_state == 1:  # Living cell
            return 1 if alive_neighbors in (2, 3) else 0
        else:  # Dead cell  
            return 1 if below_neighbor == 1 and random.random() < 0.33 else 0
        
    def _get_neighbors(self, x: int, y: int, face_id: int, all_faces: list) -> list:
        """
        Retrieves the neighbors of a cell, including border cells interacting with neighboring faces.

        Args:
            x (int): x-coordinate of the cell.
            y (int): y-coordinate of the cell.
            face_id (int): ID of the current face.
            all_faces (list): List of all cube faces (instances of CellularAutomata).

        Returns:
            list: List of neighboring cell states.
        """
        neighbors = []

        # Validate neighboring faces
        if face_id not in CUBE_NEIGHBORS or not all_faces:
            raise ValueError("CUBE_NEIGHBORS o all_faces están mal configurados.")

        # Get neighbors within the same face
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
                    neighbors.append(self.grid[i][j])

        # Get neighbors from adjacent faces
        for direction, neighbor_face_id in CUBE_NEIGHBORS[face_id].items():
            neighbor_face = all_faces[neighbor_face_id]
            if direction == "up" and x == 0:  # Top border
                neighbors.extend(neighbor_face.grid[-1][y:y+1])  # Last row of the neighboring face
            elif direction == "down" and x == self.grid_size - 1:  # Bottom border
                neighbors.extend(neighbor_face.grid[0][y:y+1])  # First row of the neighboring face
            elif direction == "left" and y == 0:  # Left border
                neighbors.append(neighbor_face.grid[x][-1])  # Last column of the neighboring face
            elif direction == "right" and y == self.grid_size - 1:  # Right border
                neighbors.append(neighbor_face.grid[x][0])  # First column of the neighboring face

        return neighbors    
    
    def perturb(self, intensity=3):
        """
        Applies a perturbation to the system by randomly altering some cells.

        Args:
            intensity (int): Number of cells to be modified.
        """
        for _ in range(intensity):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            self.grid[x][y] = 1 if self.grid[x][y] == 0 else 0  # Invert cell state