from sonification import Sonification

# Configurar el puerto MIDI y canales
midi_port = "Python2Midi 1"  # Nombre del puerto en loopMIDI
midi_channels = [0, 1, 2, 3, 4, 5]  # Canales para cada cara del cubo

# Crear instancia de Sonification
sonification = Sonification(midi_port_name=midi_port, midi_channels=midi_channels)

# Simular células activas en una cara
active_cells = [(0, 0), (1, 2), (3, 4)]  # Coordenadas de células activas
face_id = 0  # Cara actual

# Enviar mensajes MIDI para la cara
print(f"Enviando notas para la cara {face_id}...")
sonification.generate_midi_event(face_id, active_cells)

# Cerrar el puerto MIDI
sonification.close()
