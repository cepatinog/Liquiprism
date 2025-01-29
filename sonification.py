from mido import Message, open_output
import time

class Sonification:
    """Clase para generar y enviar mensajes MIDI basados en autómatas celulares."""

    def __init__(self, midi_port_name, midi_channels, max_notes=2, velocity=80):
        """
        Inicializa el sistema de sonificación.

        Args:
            midi_port_name (str): Nombre del puerto MIDI de salida.
            midi_channels (list): Lista de canales MIDI para cada cara.
            max_notes (int): Máximo de notas simultáneas por cara.
        """
        self.midi_port_name = midi_port_name
        self.midi_channels = midi_channels
        self.max_notes = max_notes
        self.velocity = velocity

        try:
            self.output_port = open_output(midi_port_name)
        except IOError as e:
            raise RuntimeError(f"No se pudo abrir el puerto MIDI '{midi_port_name}': {e}")

    def generate_midi_event(self, face_id, active_cells):
        """
        Genera y envía mensajes MIDI para una cara específica del cubo.

        Args:
            face_id (int): Índice de la cara del cubo.
            active_cells (list): Lista de coordenadas de células activas [(x, y), ...].
        """
        # Limitar el número de células activas
        active_cells = active_cells[:self.max_notes]

        for cell in active_cells:
            note = 60 + cell[0] + cell[1]  # Calcula el tono (C4 como base)
            channel = self.midi_channels[face_id]

            try:
                # Enviar mensajes de nota on/off
                self.output_port.send(Message('note_on', channel=channel, note=note, velocity=self.velocity))
                #time.sleep(0.05)  # Pausar brevemente antes de enviar note_off
                self.output_port.send(Message('note_off', channel=channel, note=note, velocity=0))
            except Exception as e:
                print(f"Error al enviar mensaje MIDI: {e}")


    def generate_all_midi_events(self, faces):
        """
        Genera y envía mensajes MIDI para todas las caras del cubo.

        Args:
            faces (list): Lista de instancias de CellularAutomata.
        """
        for face_id, face in enumerate(faces):
            # Identificar celdas que cambiaron de OFF → ON
            active_cells = [
                (x, y)
                for x in range(face.grid_size)
                for y in range(face.grid_size)
                if face.previous_grid[x][y] == 0 and face.grid[x][y] == 1
            ]
            self.generate_midi_event(face_id, active_cells)
    
    def close(self):
        """Cierra el puerto MIDI."""
        try:
            self.output_port.close()
        except Exception as e:
            print(f"Error al cerrar el puerto MIDI: {e}")
