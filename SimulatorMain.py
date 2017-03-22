"""
This will be the main file that essentially runs the GUI and starts up
everything.
"""
from GUI import simulator_gui
import tkinter as tk

root = tk.Tk()

Simulator_GUI = simulator_gui(root)
root.mainloop()
