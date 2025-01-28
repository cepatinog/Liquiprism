from tests.cellular_automata import CellularAutomata
from sonification import Sonification
from visualization import Visualization
import time

def main():
    # Configuración inicial
    midi_port = "MIDI_OUT 1"  # Nombre del puerto MIDI en loopMIDI
    midi_channels = [0, 1, 2, 3, 4, 5]
    sonification = Sonification(midi_port_name=midi_port, midi_channels=midi_channels)

    # Crear seis caras del cubo
    faces = [CellularAutomata(grid_size=5) for _ in range(6)]
    for face in faces:
        face.randomize()

    # Configurar la visualización
    visualization = Visualization(faces)

    # Ciclo principal
    try:
        for _ in range(100):  # Ejemplo: 100 ciclos de actualización
            for face in faces:
                face.update()  # Actualiza las caras del cubo
            sonification.generate_all_midi_events(faces)  # Genera eventos MIDI
            visualization.render()  # Actualiza la visualización
            time.sleep(0.5)  # Pausa entre actualizaciones
    except KeyboardInterrupt:
        print("Detenido por el usuario.")
    finally:
        sonification.close()  # Cierra el puerto MIDI al finalizar

if __name__ == "__main__":
    main()
