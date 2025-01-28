from cellular_automata import CellularAutomata
from cube_visualization import CubeVisualization
from sonification import Sonification
from visualization import Visualization
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time


# Configuración global
MIDI_PORT = "MIDI_OUT 1"  # Puerto MIDI virtual creado con loopMIDI
MIDI_CHANNELS = [0, 1, 2, 3, 4, 5]  # Canales MIDI para las caras
GRID_SIZE = 5  # Tamaño de cada cuadrícula (5x5)
UPDATE_INTERVAL = 0.5  # Intervalo entre actualizaciones (en segundos)

def main():
    """
    Punto de entrada principal del sistema Liquiprism.
    1. Inicializa las caras del cubo (autómatas celulares).
    2. Configura la visualización y la sonificación.
    3. Coordina el ciclo principal del sistema.
    """
    # Inicializar las caras del cubo
    faces = [CellularAutomata(grid_size=GRID_SIZE) for _ in range(6)]
    for face in faces:
        face.randomize()  # Población inicial aleatoria 

     # Inicializar visualización 3D
    visualization = CubeVisualization(faces)

    # Inicializar la sonificación
    sonification = Sonification(midi_port_name=MIDI_PORT, midi_channels=MIDI_CHANNELS)

    # Temporizador para controlar el intervalo de actualizaciones
    last_update_time = time.time()

    try:
        print("Sistema iniciado. Presiona Ctrl + C para salir.")

        running = True

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Controlar la frecuencia de actualizaciones con UPDATE_INTERVAL
            current_time = time.time()
            if current_time - last_update_time >= UPDATE_INTERVAL:
                last_update_time = current_time

                # Actualizar las caras del cubo
                for face_id, face in enumerate(faces):
                    face.update(face_id, faces)

                # Generar eventos MIDI
                sonification.generate_all_midi_events(faces)

            # Renderizar la visualización
            visualization.render()

    except KeyboardInterrupt:
        print("Sistema detenido por el usuario.")
    finally:
        sonification.close()
        pygame.quit()
        print("Recursos liberados. Hasta luego.")

if __name__ == "__main__":
    main()

