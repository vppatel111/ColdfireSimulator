from tkinter import *
from unparser import AssemblyFileReader
from CPU import CPU


class simulator_gui:
    """
        Main GUI for the ColdFire Simulator. Initializes all necessary
        components for program execution: GUI and CPU.

        Attributes:
            CPU:            The CPU object that will handle code execution.
            master:         Tkinter object, necessary for GUI execution
            address_view:   Keeps track of user specified base for address reg.
            data_view:      Keeps track of user specified base for data reg.
            memory_monitor: Keeps track of the memory values the user wishes
                            to look at.
            file_name:      The file that is currently being processed.
            resolution:     Keeps track of user specified size of GUI.

            (For all tkinter GUI elements, see below.)

    """

    def __init__(self, master):

        self.CPU = None  # Initialize the CPU

        self.master = master
        master.title("ColdFire Simulator")
        # master.resizeable(width=False, height=False)
        self.master.geometry('{}x{}'.format(1093, 889))  # Width x Height

        self.address_view = "hex"  # Initialize view base
        self.data_view = "hex"
        self.memory_monitor = dict()  # Initialize memory monitors
        self.file_name = ""  # Initialize file name
        self.resolution = 1080  # Initialize resolution

        column_offset = 1  # Used to shift the entire right side after Text

        # Text box for code
        self.Code_View_lbl = Text(master, width=100, height=60)
        self.Code_View_lbl.insert(END, "")
        self.Code_View_lbl.grid(row=0, column=0, rowspan=20, pady=20, padx=20)

        # CCR labels - row 0
        self.CCR_lbl = Label(master, text="CCR", font=("FreeSans", 15))
        self.CCR_lbl.config(anchor="e", justify="right")
        self.CCR_lbl.grid(row=0, column=1+column_offset, sticky=E)

        self.CCR_value_lbl = Label(master, text="0 0 0 0 0",
                                   font=("FreeSans", 15), relief=SUNKEN)
        self.CCR_value_lbl.grid(row=0, column=2+column_offset, padx=20, sticky=W)

        # OP code labels - row 1-4
        self.OP_lbl = Label(master, text="OP Code", font=("FreeSans", 15))
        self.OP_lbl.grid(row=1, column=1+column_offset, columnspan=2)

        self.OP_value_lbl = Label(master, text="0x0", font=("FreeSans", 15),
                                  relief=SUNKEN)
        self.OP_value_lbl.grid(row=2, column=1+column_offset, columnspan=2)

        self.extension1_lbl = Label(master, text="Extension 1:",
                                    font=("FreeSans", 15))
        self.extension1_lbl.grid(row=3, column=1+column_offset)

        self.extension1_value_lbl = Label(master, text="0x0",
                                          font=("FreeSans", 15))
        self.extension1_value_lbl.grid(row=3, column=2+column_offset)

        self.extension2_lbl = Label(master, text="Extension 2:",
                                    font=("FreeSans", 15))
        self.extension2_lbl.grid(row=4, column=1+column_offset)

        self.extension2_value_lbl = Label(master, text="0x0",
                                          font=("FreeSans", 15))
        self.extension2_value_lbl.grid(row=4, column=2+column_offset)

        # Address Register Labels - rows 5-9, cols 1-2,
        # hardcoded constants: spacer = 6th row + offset, columns = 1 or 2
        # Also note spacer is based on counter
        self.addressReg_lbl = Label(master, text="Address Registers:",
                                    font=("FreeSans", 15))
        self.addressReg_lbl.grid(row=5, column=1+column_offset, columnspan=2)

        # Initialize address register labels
        self.addressRegisters = []
        for _ in range(8):
            self.addressRegisters.append(Label(master, text="0x0",
                                               font=("FreeSans", 12), padx=10))

        # Place the address register labels on the grid.
        counter = 0
        for label in self.addressRegisters:
            if counter < 4:
                spacer = 6+counter
                label.grid(row=spacer, column=1+column_offset)
            else:
                spacer = 2+counter
                label.grid(row=spacer, column=2+column_offset)
            counter += 1

        # Initialize address register number labels
        self.addressRegisters_value_lbl = []
        for i in range(8):

            if i < 4:  # Number the labels appropiately
                txt = "A"+str(i)+":"
            else:
                txt = ":"+"A"+str(i)

            self.addressRegisters_value_lbl.append(Label(master, text=txt,
                                               font=("FreeSans", 12), padx=10))

        # Place the address register number labesl on the grid.
        counter = 0
        for label in self.addressRegisters_value_lbl:
            if counter < 4:
                spacer = 6+counter
                label.grid(row=spacer, column=1)
            else:
                spacer = 2+counter
                label.grid(row=spacer, column=2+column_offset+1)
            counter += 1

        # Data Register Labels - rows 10-14, col = 1,2
        # hardcoded constants: spacer = 11th row + offset, columns
        # Also note spacer is based on counter.
        self.dataReg_lbl = Label(master, text="Data Registers:",
                                 font=("FreeSans", 12))
        self.dataReg_lbl.grid(row=10, column=1+column_offset, columnspan=2)

        # Initialize data register labels
        self.dataRegisters = []
        for _ in range(8):
            self.dataRegisters.append(Label(master, text="0x0",
                                            font=("FreeSans", 12)))

        # Place data register labels on the grid
        counter = 0
        for label in self.dataRegisters:
            if counter < 4:
                spacer = 11+counter
                label.grid(row=spacer, column=1+column_offset)
            else:
                spacer = 7+counter
                label.grid(row=spacer, column=2+column_offset)
            counter += 1

        # Initialize data register number labels
        self.dataRegisters_value_lbl = []
        for i in range(8):

            if i < 4:  # Assign appropiate numbering.
                txt = "D"+str(i)+":"
            else:
                txt = ":"+"D"+str(i)

            self.dataRegisters_value_lbl.append(Label(master, text=txt,
                                                font=("FreeSans", 12), padx=10))

        # Place data register number labels on grid.
        counter = 0
        for label in self.dataRegisters_value_lbl:
            if counter < 4:
                spacer = 11+counter
                label.grid(row=spacer, column=1)
            else:
                spacer = 7+counter
                label.grid(row=spacer, column=2+column_offset+1)
            counter += 1

        # Memory Scroll box
        self.memory_display_lbl = Label(master, text="Memory: ",
                                        font=("FreeSans", 12))
        self.memory_display_lbl.grid(row=15, column=1, columnspan=2+column_offset)

        self.memory_display_list = Listbox(master)
        self.memory_display_list.grid(row=16, column=1+column_offset, columnspan=2)

        # Add/Remove memory monitor buttons TODO: Implement remove
        self.add_memory_btn = Button(master, text="Add",
                                     command=self.add_monitor)
        self.add_memory_btn.grid(row=17, column=1+column_offset)

        self.remove_memory_btn = Button(master, text="Remove",
                                        command=self.remove_monitor)
        self.remove_memory_btn.grid(row=17, column=2+column_offset)

        # Next/Prev Line Buttons
        self.next_btn = Button(master, text="Next Line", command=self.next_line)
        self.next_btn.grid(row=18, column=1+column_offset)

        self.reset_btn = Button(master, text="Reset", command=self.reset_line)
        self.reset_btn.grid(row=18, column=2+column_offset)

        # Menu bar
        self.menubar = Menu(master)
        self.menubar.add_command(label="Load file", command=self.loadfile)
        self.master.config(menu=self.menubar)

        # Screen resolution menu
        self.resolution = Menu(self.menubar, tearoff=0)
        self.resolution.add_command(label="1920x1080",
        command=lambda res=1080: self.change_res(res))
        self.resolution.add_command(label="1366x768",
        command=lambda res=768: self.change_res(res))
        self.menubar.add_cascade(label="Screen Resolution",
                                 menu=self.resolution)

        # Data register view menu
        self.dataRegister_menu = Menu(self.menubar, tearoff=0)
        self.dataRegister_menu.add_command(label="View in Bin",
        command=lambda view="bin": self.set_dataRegister_view(view))

        self.dataRegister_menu.add_command(label="View in Hex",
        command=lambda view="hex": self.set_dataRegister_view(view))

        self.dataRegister_menu.add_command(label="View in Dec",
        command=lambda view="dec": self.set_dataRegister_view(view))

        self.menubar.add_cascade(label="Data Register",
                                 menu=self.dataRegister_menu)

        # Address register view menu
        self.addressRegister_menu = Menu(self.menubar, tearoff=0)
        self.addressRegister_menu.add_command(label="View in Bin",
        command=lambda view="bin": self.set_addressRegister_view(view))

        self.addressRegister_menu.add_command(label="View in Hex",
        command=lambda view="hex": self.set_addressRegister_view(view))

        self.addressRegister_menu.add_command(label="View in Dec",
        command=lambda view="dec": self.set_addressRegister_view(view))

        self.menubar.add_cascade(label="Address Register",
                                 menu=self.addressRegister_menu)

        # Theme menu
        self.theme_menu = Menu(self.menubar, tearoff=0)
        self.theme_menu.add_command(label="Light",
                                    command=lambda t="light": self.set_theme(t))
        self.theme_menu.add_command(label="Dark",
                                    command=lambda t="dark": self.set_theme(t))
        self.menubar.add_cascade(label="Set Theme", menu=self.theme_menu)

        # Quit
        self.menubar.add_command(label="Quit", command=self.master.quit)

        # self.change_res()  # Comment out for not auto-changing.

    def windowsize(self):  # DEBUG Purposes
        # Obtains size of GUI.
        print("height", self.master.winfo_height())
        print("width", self.master.winfo_width())

    def set_theme(self, theme):
        """
        Sets the theme of the GUI, by modifying all GUI elements.
        """
        if theme == "dark":
            self.master.config(background="#202020")

            self.Code_View_lbl.config(background="#404040")
            # self.CCR_lbl.config(font=("FreeSans", 10))
            # self.CCR_value_lbl.config(font=("FreeSans", 10))
            # self.OP_lbl.config(font=("FreeSans", 10))
            # self.OP_value_lbl.config(font=("FreeSans", 10))
            # self.extension1_lbl.config(font=("FreeSans", 10))
            # self.extension1_value_lbl.config(font=("FreeSans", 10))
            # self.extension2_lbl.config(font=("FreeSans", 10))
            # self.extension2_value_lbl.config(font=("FreeSans", 10))
            # self.addressReg_lbl.config(font=("FreeSans", 10))
            # self.dataReg_lbl.config(font=("FreeSans", 10))
            #
            # for register in self.addressRegisters:
            #     register.config(font=("FreeSans", 10), padx=10)
            #
            # for register in self.dataRegisters:
            #     register.config(font=("FreeSans", 10), padx=10)
        elif theme == "light":
            self.master.config(background="#E0E0E0")

    def change_res(self, res):
        """
        Changes size of all GUI elements to better fit the size of different
        size screens.
        """

        if res == 768:
            self.resolution = 768
            self.check_window_size()

            self.Code_View_lbl.config(width=80, height=40)
            self.CCR_lbl.config(font=("FreeSans", 10))
            self.CCR_value_lbl.config(font=("FreeSans", 10))
            self.OP_lbl.config(font=("FreeSans", 10))
            self.OP_value_lbl.config(font=("FreeSans", 10))
            self.extension1_lbl.config(font=("FreeSans", 10))
            self.extension1_value_lbl.config(font=("FreeSans", 10))
            self.extension2_lbl.config(font=("FreeSans", 10))
            self.extension2_value_lbl.config(font=("FreeSans", 10))
            self.addressReg_lbl.config(font=("FreeSans", 10))
            self.dataReg_lbl.config(font=("FreeSans", 10))

            for register in self.addressRegisters:
                register.config(font=("FreeSans", 10), padx=10)

            for register in self.dataRegisters:
                register.config(font=("FreeSans", 10), padx=10)

            self.memory_display_lbl.config(font=("FreeSans", 10))

        elif res == 1080:
            self.resolution = 1080
            self.check_window_size()

            self.Code_View_lbl.config(width=100, height=60)
            self.CCR_lbl.config(font=("FreeSans", 15))
            self.CCR_value_lbl.config(font=("FreeSans", 15))
            self.OP_lbl.config(font=("FreeSans", 15))
            self.OP_value_lbl.config(font=("FreeSans", 15))
            self.extension1_lbl.config(font=("FreeSans", 15))
            self.extension1_value_lbl.config(font=("FreeSans", 15))
            self.extension2_lbl.config(font=("FreeSans", 15))
            self.extension2_value_lbl.config(font=("FreeSans", 15))
            self.addressReg_lbl.config(font=("FreeSans", 15))
            self.dataReg_lbl.config(font=("FreeSans", 15))

            for register in self.addressRegisters:
                register.config(font=("FreeSans", 12), padx=10)

            for register in self.dataRegisters:
                register.config(font=("FreeSans", 12), padx=10)

            self.memory_display_lbl.config(font=("FreeSans", 15))

    def string_to_num(self, lovelyString):
        """
        Converts a string in base 2, 10, or 16 into a number
        """
        if lovelyString.startswith('0x'):
            lovelyNum = int(lovelyString, 16)
        elif lovelyString.startswith('0b'):
            lovelyNum = int(lovelyString, 2)
        elif lovelyString.startswith('0o'):
            lovelyNum = int(lovelyString, 8)
        else:
            lovelyNum = int(lovelyString)
        return lovelyNum

    def remove_monitor(self):
        """
        Removes the currently selected memory monitor from the memory monitors.
        """
        # print(self.memory_display_list.get(ACTIVE))
        # Obtains the key for the selected memory monitor from user
        selection = self.memory_display_list.get(ACTIVE)
        selection = selection.strip().split()
        selection = selection[0][:-1]
        selection = self.string_to_num(selection)

        # print(self.memory_monitor)
        self.memory_monitor.pop(selection)
        self.memory_display_list.delete(ACTIVE)
        # print(self.memory_monitor)

    def add_monitor(self):
        """
        Obtains a requested memory monitor from the user and adds it a dict()
        that will be used to update a scroll box with respective values.
        """

        def get_input():
            # Obtain input from the user.
            address = user_input.get()
            address_list = [a.strip() for a in address.split(',')]

            # if not self.CPU.add_memory_monitor(address):  # TODO: Give error
            #     print("Error: Invalid memory address")
            #

            # Allows us to obtain a list of memory values inputted by user, in
            # hex, bin, and dec.
            for address in address_list:
                address = self.string_to_num(address)
                self.memory_monitor[address] = self.CPU.memory.memory.get(address, 1)

            self.update_mem()  # Update the memory display
            prompt_monitor.destroy()

        # Create a top level dialog box.
        prompt_monitor = Toplevel()
        prompt_monitor.geometry('{}x{}'.format(299, 155))
        prompt_monitor.title("Monitor Selection")

        msg = Message(prompt_monitor, text="Enter a valid mem address: ")
        msg.pack()

        user_input = Entry(prompt_monitor)
        user_input.pack()

        button = Button(prompt_monitor, text="Accept", command=get_input)
        button.pack()

        self.update_mem()

    def update_mem(self):
        """
        Based on the monitors as defined by the user, updates the values disp.
        on the GUI with the respective memory values.
        """
        self.memory_display_list.delete(0, END)  # Clear list

        # Parse through the memory "monitors", get and display values.
        for address in sorted(self.memory_monitor.keys()):
            self.memory_display_list.insert(END, "{}: {}".format(hex(address),
                                hex(self.CPU.memory.memory.get(address, 1))))

    def update_ccr(self):
        """
        Update the CCR label with corresponding values.
        """
        X = self.CPU.ccr.get_X()
        N = self.CPU.ccr.get_N()
        Z = self.CPU.ccr.get_Z()
        V = self.CPU.ccr.get_V()
        C = self.CPU.ccr.get_C()
        self.CCR_value_lbl.config(text="{} {} {} {} {}".format(X, N, Z, V, C))

    def check_window_size(self):
        """For hex/dec, 1080: height 889 & width 1093
           For bin height 889 & width 1510

           hex: height 648 & width 1211
           bin: height 648 & width 905

        """
        # print(self.address_view, self.data_view)
        if self.address_view == "bin" or self.data_view == "bin":
            if self.resolution == 768:
                self.master.geometry('{}x{}'.format(1211, 648))
            elif self.resolution == 1080:
                self.master.geometry('{}x{}'.format(1510, 889))
        else:
            if self.resolution == 768:
                self.master.geometry('{}x{}'.format(905, 648))
            elif self.resolution == 1080:
                self.master.geometry('{}x{}'.format(1093, 889))

    def set_dataRegister_view(self, view=None):
        """
        Updates the all data register values.
        """
        if view is not None:
            self.data_view = view
        else:
            view = self.data_view

        for i in range(8):
            # Sets the view base as determined by user.
            if view == "bin":
                self.dataRegisters[i].config(text=bin(self.CPU.D[i].get()))
            elif view == "hex":
                self.dataRegisters[i].config(text=hex(self.CPU.D[i].get()))
            else:
                self.dataRegisters[i].config(text=self.CPU.D[i].get())

        self.check_window_size()

    def set_addressRegister_view(self, view=None):
        """
        Updates the all address register values.
        """
        if view is not None:
            self.address_view = view
        else:
            view = self.address_view

        for i in range(8):
            # Sets view base as determined by user.
            if view == "bin":
                self.addressRegisters[i].config(
                                text=bin(self.CPU.A[i].get()))
            elif view == "hex":
                self.addressRegisters[i].config(
                                text=hex(self.CPU.A[i].get()))
            else:
                self.addressRegisters[i].config(
                                text=(self.CPU.A[i].get()))

        self.check_window_size()

    def reset_line(self):
        """
        Resets program execution.
        """
        self.CPU.pc.n = 0  # Reset program counter

        # Reset all registers and memory
        for i in range(8):
            self.CPU.D[i].set(0, 4)
            self.CPU.A[i].set(0, 4)
        self.CPU.memory.memory.reset_mem()

        self.CPU.A[7].set(0xFFFFF, 4)  # initialize stack pointer

        # Update labels
        self.update_mem()
        self.display_register()

        self.Code_View_lbl.tag_remove("current_line", 1.0, "end")
        self.Code_View_lbl.tag_add("current_line", 1.0, 2.0)

    def next_line(self):  # TODO: Constrain next line to max num of lines
        """
        Executes the next line and updates respective GUI displays.
        """
        self.CPU.pc.exec_line()

        self.update_mem()
        self.display_register()
        self.update_ccr()
        # if changes:  # TODO: If there are changes, display and highlight them
        self.display_register()

        # Move the current line selection cursor.
        highlight_start = str(self.CPU.pc.n + 1) + ".0"
        highlight_end = str(self.CPU.pc.n + 2) + ".0"
        self.Code_View_lbl.tag_remove("current_line", 1.0, "end")
        self.Code_View_lbl.tag_add("current_line", highlight_start,
                                   highlight_end)

    def get_file_dir(self):
        """
        Obtains a requested file name from the user and stores it in a class
        variable: self.file_name
        """
        def get_input():  # Obtains input from a input box

            self.file_name = user_input.get()
            # print(self.file_name)
            prompt_file.destroy()

        prompt_file = Toplevel()  # Create a dialog box.

        prompt_file.geometry('{}x{}'.format(299, 155))
        prompt_file.title("File Selection")

        msg = Message(prompt_file, text="Enter the file name: ")
        msg.pack()

        user_input = Entry(prompt_file)
        user_input.pack()

        button = Button(prompt_file, text="Enter", command=get_input)
        button.pack()

        self.master.wait_window(prompt_file)

    def loadfile(self):
        """
        Loads in a .s file at that is currently in the same directory as
        SimulatorMain.py and displays the text in the Text widget, additionally
        it calls an unparser to process the file.
        """

        # Obtain and load a file requested by the user
        self.get_file_dir()
        file_directory = "AssemblyTest/" + self.file_name
        self.CPU = CPU(file_directory+'.s')

        self.Code_View_lbl.delete(1.0, END)  # Clear text

        # Initialize oru cursors
        highlight_start = 0
        highlight_end = 0
        line_number = 1
        # Formats each line and inserts it into the Text widget
        for e in self.CPU.assembler._line_a:

            """ Label """
            # Add colour for labels
            if e[0]:  # Check for label

                label = e[0] + ": "  # Obtain the label

                # Insert line label
                self.Code_View_lbl.insert(END, label)

                # Determine the size of the label to be printed
                highlight_start = 0
                highlight_end = len(e[0])

                # Add and display the colour tag
                self.Code_View_lbl.tag_add("color_tag",
                            str(line_number) + "." + str(highlight_start),
                            str(line_number) + "." + str(highlight_end + 1))
                self.Code_View_lbl.tag_configure("color_tag", foreground="red")

                # print(str(line_number) + "." + str(highlight_start),
                #      str(line_number) + "." + str(highlight_end))

                highlight_end += 2  # Account for formatting

                if not e[1]:  # Check if label was the only instruction
                    self.Code_View_lbl.insert(END, "\n")
                    line_number += 1
                    continue  # If it was skip the rest of the line processing

            else:  # Otherwise we skip over the label
                self.Code_View_lbl.insert(END, "        ")
                highlight_end = 8

            """ Instruction (Note: Always an instruction)"""
            highlight_start = highlight_end  # Move cursor to start instruction
            highlight_end = highlight_start + len(e[1])  # Size of command text

            self.Code_View_lbl.insert(END, e[1])  # Insert the command

            # Add and display the colour tag
            self.Code_View_lbl.tag_add("color_tag2",
                                str(line_number) + "." + str(highlight_start),
                                str(line_number) + "." + str(highlight_end))
            self.Code_View_lbl.tag_configure("color_tag2", foreground="blue")

            """ Size """
            if e[2]:  # Check for size label
                self.Code_View_lbl.insert(END, ".")

                highlight_start = highlight_end + 1  # Account for period
                highlight_end = highlight_start + 2  # Size of "size" text

                # Inser the size
                self.Code_View_lbl.insert(END, e[2])

                # Add and display the colour tag
                self.Code_View_lbl.tag_add("color_tag3",
                                str(line_number) + "." + str(highlight_start),
                                str(line_number) + "." + str(highlight_end))
                self.Code_View_lbl.tag_configure("color_tag3",
                                                 foreground="orange")
            else:
                highlight_end += 1  # Otherwise we skip over size

            self.Code_View_lbl.insert(END, " ")  # Necessary space

            """ Source """
            if e[3]:  # Check for source label
                highlight_start = highlight_end  # Space already accounted for
                highlight_end = highlight_start + len(e[3])  # Size of text

                # Insert the source and tag it with colour
                self.Code_View_lbl.insert(END, e[3])

                self.Code_View_lbl.tag_add("color_tag4",
                                str(line_number) + "." + str(highlight_start),
                                str(line_number) + "." + str(highlight_end))
                self.Code_View_lbl.tag_configure("color_tag4",
                                                 foreground="green")

            """ Destination """
            if e[4]:  # Check for destination label
                self.Code_View_lbl.insert(END, ", ")  # Necessary comma
                highlight_start = highlight_end + 1
                highlight_end = highlight_start + len(e[4]) + 1  # Size of text

                # Insert the dest and tag it with colourr
                self.Code_View_lbl.insert(END, e[4])
                self.Code_View_lbl.tag_add("color_tag5",
                                str(line_number) + "." + str(highlight_start),
                                str(line_number) + "." + str(highlight_end))
                self.Code_View_lbl.tag_configure("color_tag5",
                                                 foreground="#660033")

            self.Code_View_lbl.insert(END, "\n")
            line_number += 1

        # Also display the current line selection
        self.reset_line()
        self.Code_View_lbl.tag_configure("current_line", background="#e9e9e9")
        self.Code_View_lbl.tag_remove("current_line", 1.0, "end")
        self.Code_View_lbl.tag_add("current_line", 1.0, 2.0)
        self.display_register()

    def display_register(self):
        """
        Calls function that update the data and address registers respectively.
        """
        self.set_dataRegister_view()
        self.set_addressRegister_view()
