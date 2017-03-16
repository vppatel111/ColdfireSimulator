"""
    Additional features to add: -The ability to view registers in different
    formats (eg, decimal, ascii etc)
    - Implement more memory view options such as:
        * Display different types
        * Display a range of values
        * Add more "monitors"
"""

from tkinter import *


class simulator_gui:

    def __init__(self, master):

        self.master = master
        master.title("ColdFire Simulator")

        # Text box for code
        self.Code_View_lbl = Text(master)
        self.Code_View_lbl.insert(END, "Test")
        self.Code_View_lbl.grid(row=0, column=0, rowspan=20, pady=20, padx=10)

        # CCR label
        self.CCR_lbl = Label(master, text="CCR")
        self.CCR_lbl.grid(row=0, column=1)

        self.CCR_value_lbl = Label(master, text="1 0 0 1 0")
        self.CCR_value_lbl.grid(row=0, column=2)

        # OP code labels - row 0-3
        self.OP_lbl = Label(master, text="OP Code")
        self.OP_lbl.grid(row=1, column=1, columnspan=2)

        self.OP_value_lbl = Label(master, text="123456789012345")
        self.OP_value_lbl.grid(row=2, column=1, columnspan=2)

        self.extension1_lbl = Label(master, text="Extension 1:")
        self.extension1_lbl.grid(row=3, column=1)

        self.extension1_value_lbl = Label(master, text="123456789012345")
        self.extension1_value_lbl.grid(row=3, column=2)

        self.extension2_lbl = Label(master, text="Extension 2:")
        self.extension2_lbl.grid(row=4, column=1)

        self.extension2_lbl = Label(master, text="123456789012345")
        self.extension2_lbl.grid(row=4, column=2)

        # Address Register Labels - rows 5-9, cols 1-2,
        # hardcoded constants: spacer = 7th row + offset, columns = 1 or 2
        # Also note spacer is based on counter
        self.addressReg_lbl = Label(master, text="Address Registers:")
        self.addressReg_lbl.grid(row=5, column=1, columnspan=2)

        self.addressRegisters = []
        for _ in range(7):
            self.addressRegisters.append(Label(master, text="0x12345678"))

        counter = 0
        for label in self.addressRegisters:
            if counter < 3:
                spacer = 6+counter
                label.grid(row=spacer, column=1)
            else:
                spacer = 3+counter
                label.grid(row=spacer, column=2)
            counter += 1

        self.addressRegisters[6].grid(row=9, column=1)

        # self.addressRegisters[0].config(text="test1")
        # self.addressRegisters[6].config(text="test2")

        # Data Register Labels - rows 10-14, col = 1,2
        # hardcoded constants: spacer = 13th row + offset, columns
        # Also note spacer is based on counter.
        self.dataReg_lbl = Label(master, text="Data Registers:")
        self.dataReg_lbl.grid(row=10, column=1, columnspan=2)

        self.dataRegisters = []
        for _ in range(7):
            self.dataRegisters.append(Label(master, text="0x12345678"))

        counter = 0
        for label in self.dataRegisters:
            if counter < 3:
                spacer = 11+counter
                label.grid(row=spacer, column=1)
            else:
                spacer = 8+counter
                label.grid(row=spacer, column=2)
            counter += 1

        self.dataRegisters[6].grid(row=14, column=1)

        # Memory Scroll box
        self.memory_display_lbl = Label(master, text="Memory: ")
        self.memory_display_lbl.grid(row=15, column=1, columnspan=2)

        self.memory_display_list = Listbox(master)
        self.memory_display_list.grid(row=16, column=1, columnspan=2)
        for item in ["one", "two", "three", "four"]:
            self.memory_display_list.insert(END, item)

        # TODO: Implement change memory view button
        self.add_memory_btn = Button(master, text="Add")
        self.add_memory_btn.grid(row=17, column=1)

        self.remove_memory_btn = Button(master, text="Remove")
        self.remove_memory_btn.grid(row=17, column=2)

        # Next/Prev Line Buttons
        # TODO: Add functionality to buttons as well.
        self.next_btn = Button(master, text="Next Line")
        self.next_btn.grid(row=18, column=1)

        self.prev_btn = Button(master, text="Prev Line")
        self.prev_btn.grid(row=18, column=2)

        # Menu bar
        # TODO: Add additional functionality to "Load file"
        self.menubar = Menu(master)
        self.menubar.add_command(label="Load file")
        self.menubar.add_command(label="Quit", command=master.quit)
        self.master.config(menu=self.menubar)
