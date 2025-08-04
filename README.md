# FET Transistor Analysis (N-Channel & P-Channel)

This Python project provides a comprehensive tool to simulate, calculate, and visualize the behavior of **N-channel** and **P-channel** FET (Field Effect Transistor) circuits under different configurations and states.

The tool includes both **command-line** and **graphical user interface (GUI)** modes, allowing users to either interact directly via terminal or use a GUI for visual simulations and input handling. The GUI also includes image processing functionality for enhanced educational or documentation purposes.

---

##  Features

- Analysis of **7 different states** for both N-channel and P-channel FETs.
- Calculation of:
  - Drain current (ID)
  - Gate-source voltage (VGS)
  - Drain-source voltage (VDS)
  - Saturation status of the transistor
- Dual-mode operation:
  - **Command-line** (via `run.py`, `dc_fet.py`, `input_n.py`, `input_p.py`)
  - **Graphical UI** (via `gui_run.py`, `gui_dc_fet.py`, etc.)
- Built-in **image display** for schematic or simulation diagrams.
- Modular code structure for easy extension or integration.

---
##  How to Run

###  1. Install Requirements

Make sure you have Python 3.8+ installed. Then, install dependencies:

```bash
pip install numpy scipy sympy tkinter
```
### 2.Run in Terminal (CLI Mode)
You can analyze both channels using terminal input.

For N-channel:
```bash
python run.py
```
For P-channel (uses dc_fet_pnp.py):
```bash
python dc_fet_pnp.py
```
### 3. Run GUI Mode
```bash
python gui_run.py
```
From there, you can select N-channel or P-channel, enter values, and view visual results including states and diagrams.

### Example Output
A typical output for a P-channel transistor in state 1:
```bash
State 1 with VGS = -1.5 V , ID = 3.21 mA, VDS = -4.8 V 
Status: Saturated
```
### Notes
The image files (state3-4.jpg, state5-6.jpg, etc.) are used inside the GUI for visualization.

The system calculates whether the transistor is operating in the saturation or linear region.

Calculations are based on common FET formulas and implemented using scipy.optimize.fsolve.
