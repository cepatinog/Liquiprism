from tests.cellular_automata import CellularAutomata
from tests.visualization1 import Visualization

# Crear un autómata celular con una cuadrícula de 10x10
automata = CellularAutomata(grid_size=10)
automata.randomize()

# Visualizar la cuadrícula inicial
visualization = Visualization(automata)
visualization.animate(automata.update, interval=0.5)
