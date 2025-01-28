from tests.cellular_automata import CellularAutomata

# Create a 5x5 grid
automata = CellularAutomata(grid_size=5)

automata.randomize()
# Display the initial grid
print("\nInitial grid (randomized):")
automata.display()

# Update the grid
automata.update()
print("\nGrid after update:")
automata.display()

automata = CellularAutomata(grid_size=5)
# Define a manual pattern
automata.grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

print("\nInitial pattern:")
automata.display()

# Update the grid
automata.update()
print("\nGrid after update:")
automata.display()

