from tests.cellular_automata import CellularAutomata
from visualization import Visualization

# Crear seis autómatas celulares para representar las caras del cubo
faces = [CellularAutomata(grid_size=5) for _ in range(6)]
for face in faces:
    face.randomize()

# Visualizar las caras del cubo
visualization = Visualization(faces)

# Función de actualización para todas las caras
def update_faces():
    for face in faces:
        face.update()

# Animar la evolución con cambio de caras
visualization.animate(update_faces, interval=0.5)
