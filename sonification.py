from mido import Message, open_output
import time

class Sonification:
    """Class to generate and send MIDI messages based on cellular automata."""

    def __init__(self, midi_port_name, midi_channels, max_notes=2, velocity=80):
        """
        Initializes the sonification system.

        Args:
            midi_port_name (str): Name of the MIDI output port.
            midi_channels (list): List of MIDI channels for each face.
            max_notes (int): Maximum number of simultaneous notes per face.
        """
        self.midi_port_name = midi_port_name
        self.midi_channels = midi_channels
        self.max_notes = max_notes
        self.velocity = velocity

        try:
            self.output_port = open_output(midi_port_name)
        except IOError as e:
            raise RuntimeError(f"Could not open MIDI port '{midi_port_name}': {e}")

    def generate_midi_event(self, face_id, active_cells):
        """
        Generates and sends MIDI messages for a specific face of the cube.

        Args:
            face_id (int): Index of the cube face.
            active_cells (list): List of coordinates of active cells [(x, y), ...].
        """
        max_events_per_face = self.max_notes  # Maximum events per face
        # Limit the number of active cells
        active_cells = active_cells[:max_events_per_face]

        for cell in active_cells:
            note = 60 + cell[0] + cell[1]  # Calculate pitch (C4 as a base)
            channel = self.midi_channels[face_id]

            try:
                # Send note on/off messages
                self.output_port.send(Message('note_on', channel=channel, note=note, velocity=self.velocity))
                #time.sleep(0.001)  # Briefly pause before sending note_off
                self.output_port.send(Message('note_off', channel=channel, note=note, velocity=0, time=100))
            except Exception as e:
                print(f"Error sending MIDI message: {e}")

        #print(f"MIDI events sent on face {face_id}: {len(active_cells)}")  # Diagnostic

    def generate_all_midi_events(self, faces):
        """
        Generates and sends MIDI messages for all cube faces.

        Args:
            faces (list): List of CellularAutomata instances.
        """

        total_midi_events = 0  # Counter for generated MIDI events
        for face_id, face in enumerate(faces):
            # Identify cells that changed from OFF → ON
            active_cells = [
                (x, y)
                for x in range(face.grid_size)
                for y in range(face.grid_size)
                if face.previous_grid[x][y] == 0 and face.grid[x][y] == 1
            ]

            # Count events before sending them
            total_midi_events += len(active_cells)
            self.generate_midi_event(face_id, active_cells)
        #print(f"MIDI events sent in this iteration: {total_midi_events}")  # Diagnostic
        
    def close(self):
        """Closes the MIDI port."""
        try:
            self.output_port.close()
        except Exception as e:
            print(f"Error closing MIDI port: {e}")
