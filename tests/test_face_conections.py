from cellular_automata import CellularAutomata

# Crear las caras del cubo
faces = [CellularAutomata(grid_size=5) for _ in range(6)]
for i, face in enumerate(faces):
    face.randomize()

# Simular una actualización
for face_id, face in enumerate(faces):
    face.update(face_id, faces)

# Imprimir el estado de las caras
for i, face in enumerate(faces):
    print(f"Cara {i}:")
    for row in face.grid:
        print(row)
