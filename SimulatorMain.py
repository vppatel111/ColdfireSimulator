"""
This will be the main file that essentially runs the GUI and starts up
everything.
"""
from GUI import simulator_gui
from memory import Memory
from unparser import AssemblyFileReader
import tkinter as tk
from registers import DataRegister, AddressRegister

root = tk.Tk()  # Create GUI object
memory = Memory()  # Initiates memory

"""
We would parse the entire series of files and store it as a series of lines
which will then either be saved to a temp file (in interest of space) or
a large list (line by line), this will be used by the GUI to display a file.

"""

# Sample memory test code.
# memory.print_block()
# memory.add_block(1, 100)
# memory.print_block(1)
# print("mem1: ", memory.get_block(1))
# print("mem2: ", memory.get_block(3))
# assembler = AssemblyFileReader('test.s')
# assembler.read_into_list()


Simulator_GUI = simulator_gui(root)  # Start up GUI
root.mainloop()
