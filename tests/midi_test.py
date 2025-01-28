from mido import open_output, Message

# Abre el puerto MIDI_OUT
output_name = "MIDI_OUT 1"  # Asegúrate de que coincide con el nombre en loopMIDI
with open_output(output_name) as outport:
    # Enviar un mensaje de nota
    print(f"Enviando mensaje MIDI a {output_name}...")
    outport.send(Message('note_on', note=60, velocity=64))  # Nota C4
    outport.send(Message('note_off', note=60, velocity=64, time=500))  # Apagar la nota
