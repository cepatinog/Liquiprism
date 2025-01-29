from cellular_automata import CellularAutomata
from cube_visualization import CubeVisualization
from sonification import Sonification
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time


# Configuración global
MIDI_PORT = "MIDI_OUT 1"  # Puerto MIDI virtual creado con loopMIDI
MIDI_CHANNELS = [0, 1, 2, 3, 4, 5]  # Canales MIDI para las caras
GRID_SIZE = 5  # Tamaño de cada cuadrícula (5x5)
UPDATE_INTERVALS = [0.5, 1, 1.5, 2, 2.5, 3]  # Velocidades independientes por cara
ACTIVITY_THRESHOLD = 10 # Umbral para cambiar de regla


def main():
    """
    Punto de entrada principal del sistema Liquiprism.
    """
    # Inicializar autómatas celulares
    faces = [CellularAutomata(grid_size=GRID_SIZE) for _ in range(6)]
    for face in faces:
        face.randomize()

    # Inicializar visualización 3D
    visualization = CubeVisualization(faces)

    # Inicializar la sonificación
    sonification = Sonification(midi_port_name=MIDI_PORT, midi_channels=MIDI_CHANNELS)

    # Temporizadores independientes para cada cara
    last_update_times = [time.time()] * len(faces)
    last_midi_time = time.time()  # Controlador de tiempo para MIDI

    try:
        print("Sistema iniciado. Presiona Ctrl + C para salir.")

        running = True

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                # Detectar si se presiona 'P' para perturbar TODAS las caras
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    print("Perturbación manual activada en todas las caras.")
                    for face in faces:
                        face.perturb(intensity=2)  # Intensidad reducida

            #  Control de actualización independiente para cada cara
            current_time = time.time()
            for face_id, face in enumerate(faces):
                if current_time - last_update_times[face_id] >= UPDATE_INTERVALS[face_id]:
                    last_update_times[face_id] = current_time  # Reiniciar temporizador de la cara

                    # 1️ Actualizar el estado de la cara
                    use_stochastic_rule = face.activity_count < ACTIVITY_THRESHOLD
                    face.update(face_id, faces, use_stochastic_rule)

            # 2️ Generar eventos MIDI (sincronizado con actualizaciones de estado)
            if current_time - last_midi_time >= 0.2:  # 200ms entre eventos MIDI
                last_midi_time = current_time
                sonification.generate_all_midi_events(faces)

            # Renderizar la visualización continuamente para una rotación fluida
            visualization.render()

    except KeyboardInterrupt:
        print("Sistema detenido por el usuario.")
    finally:
        sonification.close()
        pygame.quit()
        print("Recursos liberados. Hasta luego.")



if __name__ == "__main__":
    main()

