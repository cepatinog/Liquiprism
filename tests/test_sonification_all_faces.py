from tests.cellular_automata import CellularAutomata
from sonification import Sonification
import time

# Configurar el puerto MIDI y canales
midi_port = "Python2Midi 1"  # Nombre del puerto en loopMIDI
midi_channels = [0, 1, 2, 3, 4, 5]  # Canales para cada cara del cubo

# Crear instancia de Sonification
sonification = Sonification(midi_port_name=midi_port, midi_channels=midi_channels)

# Crear seis caras del cubo
faces = [CellularAutomata(grid_size=5) for _ in range(6)]
for face in faces:
    face.randomize()

# Enviar mensajes MIDI para todas las caras
print("Enviando notas para todas las caras del cubo...")
sonification.generate_all_midi_events(faces)



# Actualizar y enviar eventos MIDI en ciclos
for _ in range(5):  # 5 ciclos de actualización
    for face in faces:
        face.update()  # Actualiza la cuadrícula
    sonification.generate_all_midi_events(faces)
    time.sleep(0.5)  # Pausa entre ciclos

# Cerrar el puerto MIDI
sonification.close()
