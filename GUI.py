"""
    Additional features to add: -The ability to view registers in different
    formats (eg, decimal, ascii etc)
    - Implement more memory view options such as:
        * Display different types
        * Display a range of values
        * Add more "monitors"

    BUG: - Remember to initialize stack pointer.

"""

from tkinter import *
from unparser import AssemblyFileReader
from CPU import CPU

class simulator_gui:

    def __init__(self, master):

        self.CPU = None

        self.master = master
        master.title("ColdFire Simulator")
        # master.resizeable(width=False, height=False)
        master.geometry('{}x{}'.format(1510, 889))  # width x height
        # master.config(background="#202020")

        self.address_view = "hex"  # Initialize view base
        self.data_view = "hex"
        self.memory_monitor = dict()

        column_offset = 1  # Used to shift the entire right side

        # Text box for code
        self.Code_View_lbl = Text(master, width=100, height=60)
        self.Code_View_lbl.insert(END, "")
        self.Code_View_lbl.grid(row=0, column=0, rowspan=20, pady=20, padx=20)

        # CCR label
        self.CCR_lbl = Label(master, text="CCR", font=("FreeSans", 15))
        self.CCR_lbl.config(anchor="e", justify="right")
        self.CCR_lbl.grid(row=0, column=1+column_offset, sticky=E)

        self.CCR_value_lbl = Label(master, text="0 0 0 0 0",
                                   font=("FreeSans", 15), relief=SUNKEN)
        self.CCR_value_lbl.grid(row=0, column=2+column_offset, padx=20, sticky=W)

        # OP code labels - row 0-3
        self.OP_lbl = Label(master, text="OP Code", font=("FreeSans", 15))
        self.OP_lbl.grid(row=1, column=1+column_offset, columnspan=2)

        self.OP_value_lbl = Label(master, text="0x0", font=("FreeSans", 15),
                                  relief=SUNKEN)
        self.OP_value_lbl.grid(row=2, column=1+column_offset, columnspan=2)

        self.extension1_lbl = Label(master, text="Extension 1:", font=("FreeSans", 15))
        self.extension1_lbl.grid(row=3, column=1+column_offset)

        self.extension1_value_lbl = Label(master, text="0x0",
                                          font=("FreeSans", 15))
        self.extension1_value_lbl.grid(row=3, column=2+column_offset)

        self.extension2_lbl = Label(master, text="Extension 2:", font=("FreeSans", 15))
        self.extension2_lbl.grid(row=4, column=1+column_offset)

        self.extension2_value_lbl = Label(master, text="0x0", font=("FreeSans", 15))
        self.extension2_value_lbl.grid(row=4, column=2+column_offset)

        # Address Register Labels - rows 5-9, cols 1-2,
        # hardcoded constants: spacer = 7th row + offset, columns = 1 or 2
        # Also note spacer is based on counter
        self.addressReg_lbl = Label(master, text="Address Registers:",
                                    font=("FreeSans", 15))
        self.addressReg_lbl.grid(row=5, column=1+column_offset, columnspan=2)

        self.addressRegisters = []
        for _ in range(8):
            self.addressRegisters.append(Label(master, text="0x12345678901234567890123456789012",
                                               font=("FreeSans", 12), padx=10))

        counter = 0
        for label in self.addressRegisters:
            if counter < 4:
                spacer = 6+counter
                label.grid(row=spacer, column=1+column_offset)
            else:
                spacer = 2+counter
                label.grid(row=spacer, column=2+column_offset)
            counter += 1

        self.addressRegisters_value_lbl = []
        for i in range(8):

            if i < 4:
                txt="A"+str(i)+":"
            else:
                txt = ":"+"A"+str(i)

            self.addressRegisters_value_lbl.append(Label(master, text=txt,
                                               font=("FreeSans", 12), padx=10))

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
        # hardcoded constants: spacer = 13th row + offset, columns
        # Also note spacer is based on counter.
        self.dataReg_lbl = Label(master, text="Data Registers:", font=("FreeSans", 12))
        self.dataReg_lbl.grid(row=10, column=1+column_offset, columnspan=2)

        self.dataRegisters = []
        for _ in range(8):
            self.dataRegisters.append(Label(master, text="0x0",
                                            font=("FreeSans", 12)))

        counter = 0
        for label in self.dataRegisters:
            if counter < 4:
                spacer = 11+counter
                label.grid(row=spacer, column=1+column_offset)
            else:
                spacer = 7+counter
                label.grid(row=spacer, column=2+column_offset)
            counter += 1

        self.dataRegisters_value_lbl = []
        for i in range(8):

            if i < 4:
                txt="D"+str(i)+":"
            else:
                txt = ":"+"D"+str(i)

            self.dataRegisters_value_lbl.append(Label(master, text=txt,
                                               font=("FreeSans", 12), padx=10))

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

        # self.memory_display2_list = Listbox(master)
        # self.memory_display2_list.grid(row=16, column=2+column_offset)

        self.add_memory_btn = Button(master, text="Add", command=self.add_monitor)
        self.add_memory_btn.grid(row=17, column=1+column_offset)

        self.remove_memory_btn = Button(master, text="Remove")
        self.remove_memory_btn.grid(row=17, column=2+column_offset)

        # Next/Prev Line Buttons

        self.next_btn = Button(master, text="Next Line", command=self.next_line)
        self.next_btn.grid(row=18, column=1+column_offset)

        self.reset_btn = Button(master, text="Reset", command=self.reset_line)
        self.reset_btn.grid(row=18, column=2+column_offset)

        # Menu bar
        # TODO: Add file choosing ability
        self.menubar = Menu(master)
        self.menubar.add_command(label="Load file", command=self.loadfile)
        self.master.config(menu=self.menubar)

        self.resolution = Menu(self.menubar, tearoff=0)
        self.resolution.add_command(label="1920x1080",
        command=lambda res=1080: self.change_res(res))
        self.resolution.add_command(label="1366x768",
        command=lambda res=768: self.change_res(res))
        self.menubar.add_cascade(label="Screen Resolution",
                                 menu=self.resolution)

        self.dataRegister_menu = Menu(self.menubar, tearoff=0)
        self.dataRegister_menu.add_command(label="View in Bin",
        command=lambda view="bin": self.set_dataRegister_view(view))

        self.dataRegister_menu.add_command(label="View in Hex",
        command=lambda view="hex": self.set_dataRegister_view(view))

        self.dataRegister_menu.add_command(label="View in Dec",
        command=lambda view="dec": self.set_dataRegister_view(view))

        self.menubar.add_cascade(label="Data Register",
                                 menu=self.dataRegister_menu)

        self.addressRegister_menu = Menu(self.menubar, tearoff=0)
        self.addressRegister_menu.add_command(label="View in Bin",
        command=lambda view="bin": self.set_addressRegister_view(view))

        self.addressRegister_menu.add_command(label="View in Hex",
        command=lambda view="hex": self.set_addressRegister_view(view))

        self.addressRegister_menu.add_command(label="View in Dec",
        command=lambda view="dec": self.set_addressRegister_view(view))

        self.menubar.add_cascade(label="Address Register",
                                 menu=self.addressRegister_menu)

        self.theme_menu = Menu(self.menubar, tearoff=0)
        self.theme_menu.add_command(label="Light",
                                    command=lambda t="light": self.set_theme(t))
        self.theme_menu.add_command(label="Dark",
                                    command=lambda t="dark": self.set_theme(t))
        self.menubar.add_cascade(label="Set Theme", menu=self.theme_menu)

        self.menubar.add_command(label="Quit", command=self.master.quit)

        # self.change_res()  # Comment out for not auto-changing.

    def windowsize(self):  # DEBUG Purposes
        print("height", self.master.winfo_height())
        print("width", self.master.winfo_width())

    def set_theme(self, theme):
        if theme == "dark":
            self.master.config(background="#202020")

    def change_res(self, res):

        if res == 768:
            self.master.geometry('{}x{}'.format(1211, 648))  # width x height

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
            self.master.geometry('{}x{}'.format(1510, 889))  # width x height

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
        if lovelyString.startswith('0x'):
            lovelyNum = int(lovelyString, 16)
        elif lovelyString.startswith('0b'):
            lovelyNum = int(lovelyString, 2)
        elif lovelyString.startswith('0o'):
            lovelyNum = int(lovelyString, 8)
        else:
            lovelyNum = int(lovelyString)
        return lovelyNum

    def add_monitor(self):

        def get_input():
            # print(user_input.get())
            address = user_input.get()
            address_list = [a.strip() for a in address.split(',')]
            print(address)

            # if not self.CPU.add_memory_monitor(address):  # TODO: Give error
            #     print("Error: Invalid memory address")
            #
            for address in address_list:
                address = self.string_to_num(address)
                print("add", hex(address))
                self.memory_monitor[address] = self.CPU.memory.memory.get(address, 1)
                print(self.CPU.memory.memory.get(address, 1))

            self.update_mem()
            prompt_monitor.destroy()

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
        self.memory_display_list.delete(0, END)
        self.memory_display2_list.delete(0, END)
        for address in sorted(self.memory_monitor.keys()):
            self.memory_display_list.insert(END,
                                    "{}: {}".format(hex(address), hex(self.CPU.memory.memory.get(address, 1))))

    def update_ccr(self):
        X = self.CPU.ccr.get_X()
        N = self.CPU.ccr.get_N()
        Z = self.CPU.ccr.get_Z()
        V = self.CPU.ccr.get_V()
        C = self.CPU.ccr.get_C()
        self.CCR_value_lbl.config(text="{} {} {} {} {}".format(X, N, Z, V, C))

    def set_dataRegister_view(self, view=None):
        if view is not None:
            self.data_view = view
        else:
            view = self.data_view

        print(self.CPU.D[2].get())

        for i in range(8):
            # print(self.CPU.D[i].get())
            if view == "bin":
                self.dataRegisters[i].config(text=bin(self.CPU.D[i].get()))
            elif view == "hex":
                self.dataRegisters[i].config(text=hex(self.CPU.D[i].get()))
            else:
                self.dataRegisters[i].config(text=self.CPU.D[i].get())

    def set_addressRegister_view(self, view=None):
        if view is not None:
            self.address_view = view
        else:
            view = self.address_view

        for i in range(8):
            # print(self.CPU.A[i].get())
            if view == "bin":
                self.addressRegisters[i].config(
                                text=bin(self.CPU.A[i].get()))
            elif view == "hex":
                self.addressRegisters[i].config(
                                text=hex(self.CPU.A[i].get()))
            else:
                self.addressRegisters[i].config(
                                text=(self.CPU.A[i].get()))

    def reset_line(self):
        self.CPU.pc.n = 0
        # self.CPU.pc.n = 0
        self.Code_View_lbl.tag_remove("current_line", 1.0, "end")
        self.Code_View_lbl.tag_add("current_line", 1.0, 2.0)

    def next_line(self):  # TODO: Constrain next line to max num of lines
        highlight_start = str(self.CPU.pc.n+1) + ".0"
        highlight_end = str(self.CPU.pc.n + 2) + ".0"
        self.CPU.pc.exec_line()
        # self.CPU.pc.n = self.CPU.pc.n
        # changes = self.CPU.check_for_change()
        self.update_mem()
        self.display_register()
        self.update_ccr()
        # if changes:  # If there are changes, display and highlight them
        self.display_register()
        self.Code_View_lbl.tag_remove("current_line", 1.0, "end")
        self.Code_View_lbl.tag_add("current_line", highlight_start,
                                   highlight_end)

    def loadfile(self):
        """
        Loads in a .s file at that is currently in the same directory as
        SimulatorMain.py and displays the text in the Text widget, additionally
        it calls an unparser to process the file.
        """
        self.CPU = CPU('midtermFC1'+'.s')
        # self.CPU = CPU('test.s')

        self.Code_View_lbl.delete(1.0, END)  # Clear text

        highlight_start = 0
        highlight_end = 0
        line_number = 1
        # Formats each line and inserts it
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

                print(str(line_number) + "." + str(highlight_start),
                      str(line_number) + "." + str(highlight_end))

                highlight_end += 2  # Account for formatting

                if not e[1]:  # Check if label was the only instruction
                    self.Code_View_lbl.insert(END, "\n")
                    line_number += 1
                    continue

            else:  # Otherwise we skip over the label
                self.Code_View_lbl.insert(END, "        ")
                highlight_end = 8

            """ Instruction """
            highlight_start = highlight_end
            highlight_end = highlight_start + len(e[1])  # Size of command text

            self.Code_View_lbl.insert(END, e[1])

            self.Code_View_lbl.tag_add("color_tag2",
                                str(line_number) + "." + str(highlight_start),
                                str(line_number) + "." + str(highlight_end))
            self.Code_View_lbl.tag_configure("color_tag2", foreground="blue")

            """ Size """
            if e[2]:
                self.Code_View_lbl.insert(END, ".")

                highlight_start = highlight_end + 1
                highlight_end = highlight_start + 2  # Size of command text

                self.Code_View_lbl.insert(END, e[2])

                self.Code_View_lbl.tag_add("color_tag3",
                                    str(line_number) + "." + str(highlight_start),
                                    str(line_number) + "." + str(highlight_end))
                self.Code_View_lbl.tag_configure("color_tag3", foreground="orange")
            else:
                highlight_end += 1

            self.Code_View_lbl.insert(END, " ")  # Necessary space

            """ Source """
            if e[3]:
                highlight_start = highlight_end
                highlight_end = highlight_start + len(e[3])  # Size of text

                self.Code_View_lbl.insert(END, e[3])

                self.Code_View_lbl.tag_add("color_tag4",
                                str(line_number) + "." + str(highlight_start),
                                str(line_number) + "." + str(highlight_end))
                self.Code_View_lbl.tag_configure("color_tag4", foreground="green")

            """ Destination """
            if e[4]:
                self.Code_View_lbl.insert(END, ", ")  # Necessary comma
                highlight_start = highlight_end + 1
                highlight_end = highlight_start + len(e[4]) + 1  # Size of text

                self.Code_View_lbl.insert(END, e[4])

                self.Code_View_lbl.tag_add("color_tag5",
                                str(line_number) + "." + str(highlight_start),
                                str(line_number) + "." + str(highlight_end))
                self.Code_View_lbl.tag_configure("color_tag5", foreground="blue")

            self.Code_View_lbl.insert(END, "\n")
            line_number += 1

        self.Code_View_lbl.tag_configure("current_line", background="#e9e9e9")
        self.Code_View_lbl.tag_remove("current_line", 1.0, "end")
        self.Code_View_lbl.tag_add("current_line", 1.0, 2.0)

    def display_register(self):
        self.set_dataRegister_view()
        self.set_addressRegister_view()
