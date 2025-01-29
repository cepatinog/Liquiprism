# Liquiprism: Cellular Automata-Based Sonification and Visualization System

## Overview
Liquiprism is an interactive system that integrates cellular automata, 3D visualization, and MIDI-based sonification. The system displays a dynamic cube where each face evolves based on cellular automata rules, producing both visual patterns and real-time sound.

## Features
- **Cellular Automata Simulation**: Each cube face operates as an independent cellular automaton.
- **3D Visualization**: Real-time rendering of the cube using OpenGL.
- **MIDI Sonification**: Converts state changes in the automata into MIDI events.
- **Manual Perturbation**: Press `P` to introduce disturbances to the system.
- **Independent Update Intervals**: Each cube face updates at different speeds.

## Requirements
Ensure you have the following dependencies installed:

### **Python Version**
- Python 3.10 or later

### **Dependencies**
You can install all required dependencies using:

```bash
pip install -r requirements.txt
```

Alternatively, manually install:

```bash
pip install pygame PyOpenGL mido
```

**Additional Requirements:**
- **MIDI Output Port**: You need a virtual MIDI port like `loopMIDI` (Windows) or `IAC Driver` (Mac) to send MIDI events to DAWs like Ableton Live.

## Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/cepatinog/liquiprism.git
cd liquiprism
```

2. **Configure the MIDI Output**
- Ensure a virtual MIDI port is created.
- Modify `MIDI_PORT` in `main.py` to match your MIDI device name.

3. **Run the System**
```bash
python main.py
```

## Controls
- **Close the Window**: Click the close button or press `Ctrl + C` in the terminal.
- **Perturb the Automata**: Press `P` to introduce disturbances.

## Project Structure
```
liquiprism/
│── main.py                # Entry point of the system
│── cellular_automata.py   # Cellular automata logic
│── cube_visualization.py  # 3D visualization using OpenGL
│── sonification.py        # MIDI event generation
│── requirements.txt       # Dependencies
└── README.md              # Documentation
```

## Troubleshooting
### **No MIDI Sound?**
- Ensure your DAW is receiving MIDI from the correct virtual port.
- Verify that `MIDI_PORT` in `main.py` matches your MIDI output device.
- Try restarting your DAW after launching `main.py`.

### **Visualization Not Appearing?**
- Make sure PyOpenGL and pygame are installed correctly.
- If running on macOS, try `python3 main.py` instead.

### **Performance Issues?**
- Lower `GRID_SIZE` in `main.py` if rendering is slow.
- Reduce the number of simultaneous MIDI notes in `sonification.py`.

## License
This project is licensed under the MIT License.

---

Enjoy experimenting with Liquiprism! 🚀

