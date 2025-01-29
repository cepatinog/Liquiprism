from cellular_automata import CellularAutomata
from cube_visualization import CubeVisualization
from sonification import Sonification
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

# Global configuration
MIDI_PORT = "MIDI_OUT 1"  # Virtual MIDI port created with loopMIDI
MIDI_CHANNELS = [0, 1, 2, 3, 4, 5]  # MIDI channels for the cube faces
GRID_SIZE = 5  # Size of each grid (5x5)
UPDATE_INTERVALS = [0.5, 1, 1.5, 2, 2.5, 3]  # Independent update speeds for each face
ACTIVITY_THRESHOLD = 10  # Threshold for switching between rule sets
MIDI_EVENT_INTERVAL = 0.2  # Minimum interval between MIDI events

def initialize_system():
    """
    Initializes the main components of the Liquiprism system:
    - Cellular automata
    - 3D visualization
    - MIDI sonification
    """
    faces = [CellularAutomata(grid_size=GRID_SIZE) for _ in range(6)]
    for face in faces:
        face.randomize()

    visualization = CubeVisualization(faces)
    sonification = Sonification(midi_port_name=MIDI_PORT, midi_channels=MIDI_CHANNELS)

    return faces, visualization, sonification

def handle_events(faces):
    """
    Handles user input events:
    - Detects quit events
    - Detects perturbation trigger (key 'P')
    """
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False  # Signal to stop the system
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            print("Shake!")
            for face in faces:
                face.perturb(intensity=5)  # Perturb all faces
    return True

def update_faces(faces, last_update_times, current_time):
    """
    Updates the state of the cube faces based on their individual timers and rules.
    """
    for face_id, face in enumerate(faces):
        if current_time - last_update_times[face_id] >= UPDATE_INTERVALS[face_id]:
            last_update_times[face_id] = current_time  # Reset the timer for the face
            use_stochastic_rule = face.activity_count < ACTIVITY_THRESHOLD
            face.update(face_id, faces, use_stochastic_rule)

def generate_midi_events(sonification, faces, last_midi_time, current_time):
    """
    Generates MIDI events if the minimum time between events has elapsed.
    """
    if current_time - last_midi_time >= MIDI_EVENT_INTERVAL:
        sonification.generate_all_midi_events(faces)
        return current_time
    return last_midi_time

def main():
    """
    Main entry point of the Liquiprism system.
    """
    faces, visualization, sonification = initialize_system()
    last_update_times = [time.time()] * len(faces)
    last_midi_time = time.time()

    try:
        print("System started. Press Ctrl + C to exit.")

        running = True
        while running:
            current_time = time.time()

            # 1. Process user input events
            running = handle_events(faces)

            # 2. Update the state of the faces
            update_faces(faces, last_update_times, current_time)

            # 3. Generate MIDI events
            last_midi_time = generate_midi_events(sonification, faces, last_midi_time, current_time)

            # 4. Render the visualization
            visualization.render()

    except KeyboardInterrupt:
        print("System stopped by user.")
    finally:
        sonification.close()
        pygame.quit()
        print("Resources released. Goodbye.")

if __name__ == "__main__":
    main()
