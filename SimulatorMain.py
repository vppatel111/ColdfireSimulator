"""
SimulatorMain.py

This is the main file that essentially runs the GUI and starts up
everything.
"""
from GUI import simulator_gui
import tkinter as tk

root = tk.Tk()  # Create GUI object

Simulator_GUI = simulator_gui(root)  # Start up GUI
root.mainloop()
