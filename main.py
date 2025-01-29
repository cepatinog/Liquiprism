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
GRID_SIZE = 6  # Tamaño de cada cuadrícula (5x5)
UPDATE_INTERVALS = [0.5, 1, 1.5, 2, 2.5, 3]  # Velocidades independientes por cara
ACTIVITY_THRESHOLD = 10 # Umbral para cambiar de regla

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

    # Temporizadores independientes para cada cara
    last_update_times = [time.time()] * len(faces)


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
                        face.perturb(intensity=10)  # Aplica perturbación en todas las caras

            # Controlar la frecuencia de actualizaciones con UPDATE_INTERVAL
            current_time = time.time()
            

            for face_id, face in enumerate(faces):
                # Verificar si es hora de actualizar la cara
                if current_time - last_update_times[face_id] >= UPDATE_INTERVALS[face_id]:
                    
                    last_update_times[face_id] = current_time
                    # Alternar entre Rule Set 1 y 2 según actividad
                    use_stochastic_rule = face.activity_count < ACTIVITY_THRESHOLD
                    face.update(face_id, faces, use_stochastic_rule)
                    

                    #print(f"Actualizando cara {face_id} con {'Rule Set 1' if not use_stochastic_rule else 'Rule Set 2'}")

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

