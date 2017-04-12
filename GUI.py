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
        master.geometry('{}x{}'.format(1400, 889))  # width x height

        self.address_view = "hex"  # Initialize view base
        self.data_view = "hex"
        self.screen_resolution = 1080
        self.memory_monitor = dict()

        # Text box for code
        self.Code_View_lbl = Text(master, width=100, height=60)
        self.Code_View_lbl.insert(END, "Test")
        self.Code_View_lbl.grid(row=0, column=0, rowspan=20, pady=20, padx=20)

        # CCR label
        self.CCR_lbl = Label(master, text="CCR", font=("FreeSans", 15))
        self.CCR_lbl.config(anchor="e", justify="right")
        self.CCR_lbl.grid(row=0, column=1, sticky=E)

        self.CCR_value_lbl = Label(master, text="1 0 0 1 0", font=("FreeSans", 15),
                                   relief=SUNKEN)
        self.CCR_value_lbl.grid(row=0, column=2, padx=20, sticky=W)

        # OP code labels - row 0-3
        self.OP_lbl = Label(master, text="OP Code", font=("FreeSans", 15))
        self.OP_lbl.grid(row=1, column=1, columnspan=2)

        self.OP_value_lbl = Label(master, text="123456789012345", font=("FreeSans", 15),
                                  relief=SUNKEN)
        self.OP_value_lbl.grid(row=2, column=1, columnspan=2)

        self.extension1_lbl = Label(master, text="Extension 1:", font=("FreeSans", 15))
        self.extension1_lbl.grid(row=3, column=1)

        self.extension1_value_lbl = Label(master, text="123456789012345",
                                          font=("FreeSans", 15))
        self.extension1_value_lbl.grid(row=3, column=2)

        self.extension2_lbl = Label(master, text="Extension 2:", font=("FreeSans", 15))
        self.extension2_lbl.grid(row=4, column=1)

        self.extension2_value_lbl = Label(master, text="123456789012345", font=("FreeSans", 15))
        self.extension2_value_lbl.grid(row=4, column=2)

        # Address Register Labels - rows 5-9, cols 1-2,
        # hardcoded constants: spacer = 7th row + offset, columns = 1 or 2
        # Also note spacer is based on counter
        self.addressReg_lbl = Label(master, text="Address Registers:",
                                    font=("FreeSans", 15))
        self.addressReg_lbl.grid(row=5, column=1, columnspan=2)

        self.addressRegisters = []
        for _ in range(8):
            self.addressRegisters.append(Label(master, text="0x12345678901234567890123456789012",
                                               font=("FreeSans", 12), padx=10))

        counter = 0
        for label in self.addressRegisters:
            if counter < 4:
                spacer = 6+counter
                label.grid(row=spacer, column=1)
            else:
                spacer = 2+counter
                label.grid(row=spacer, column=2)
            counter += 1

        # self.addressRegisters[6].grid(row=9, column=1)

        # self.addressRegisters[0].config(text="test1")
        # self.addressRegisters[6].config(text="test2")

        # Data Register Labels - rows 10-14, col = 1,2
        # hardcoded constants: spacer = 13th row + offset, columns
        # Also note spacer is based on counter.
        self.dataReg_lbl = Label(master, text="Data Registers:", font=("FreeSans", 12))
        self.dataReg_lbl.grid(row=10, column=1, columnspan=2)

        self.dataRegisters = []
        for _ in range(8):
            self.dataRegisters.append(Label(master, text="0x12345678",
                                            font=("FreeSans", 12)))

        counter = 0
        for label in self.dataRegisters:
            if counter < 4:
                spacer = 11+counter
                label.grid(row=spacer, column=1)
            else:
                spacer = 7+counter
                label.grid(row=spacer, column=2)
            counter += 1

        # self.dataRegisters[6].grid(row=14, column=1)

        # Memory Scroll box
        self.memory_display_lbl = Label(master, text="Memory: ",
                                        font=("FreeSans", 12))
        self.memory_display_lbl.grid(row=15, column=1, columnspan=2)

        self.memory_display_list = Listbox(master)
        self.memory_display_list.grid(row=16, column=1)
        for item in ["one", "two", "three", "four"]:
            self.memory_display_list.insert(END, item)

        self.memory_display2_list = Listbox(master)
        self.memory_display2_list.grid(row=16, column=2)
        for item in ["one", "two", "three", "four"]:
            self.memory_display2_list.insert(END, item)

        self.add_memory_btn = Button(master, text="Add", command=self.add_monitor)
        self.add_memory_btn.grid(row=17, column=1)

        self.remove_memory_btn = Button(master, text="Remove")
        self.remove_memory_btn.grid(row=17, column=2)

        # Next/Prev Line Buttons
        # TODO: Add functionality to buttons as well.
        self.next_btn = Button(master, text="Next Line", command=self.next_line)
        self.next_btn.grid(row=18, column=1)

        self.reset_btn = Button(master, text="Reset", command=self.reset_line)
        self.reset_btn.grid(row=18, column=2)

        # Menu bar
        # TODO: Add additional functionality to "Load file"
        self.menubar = Menu(master)
        self.menubar.add_command(label="Load file", command=self.loadfile)
        self.menubar.add_command(label="Screen Resolution", command=self.change_res)
        self.menubar.add_command(label="Quit", command=self.master.quit)
        self.master.config(menu=self.menubar)

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

        # self.change_res()  # Comment out for not auto-changing.

    def windowsize(self):  # DEBUG Purposes
        print("height", self.master.winfo_height())
        print("width", self.master.winfo_width())

    def change_res(self):
        self.master.geometry('{}x{}'.format(1139, 648))  # width x height
        self.screen_resolution = 720

        self.Code_View_lbl.config(width=80, height=40)
        self.CCR_lbl.config(font=("FreeSans", 10))
        self.CCR_value_lbl.config(font=("FreeSans", 10))
        self.OP_lbl.config(font=("FreeSans", 10))
        self.OP_value_lbl.config(font=("FreeSans", 10))
        # self.extension1_lbl.config(self.master font=("FreeSans", 10))
        self.extension1_value_lbl.config(font=("FreeSans", 10))
        self.extension2_lbl.config(font=("FreeSans", 10))
        self.extension2_lbl.config(font=("FreeSans", 10))
        self.addressReg_lbl.config(font=("FreeSans", 10))

        for register in self.addressRegisters:
            register.config(font=("FreeSans", 10), padx=10)

        for register in self.dataRegisters:
            register.config(font=("FreeSans", 10), padx=10)

        self.memory_display_lbl.config(font=("FreeSans", 10))

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
        self.CPU = CPU('midtermIV'+'.s')
        # assembler.read_into_list()
        file_data = ''
        for e in self.CPU.assembler._file:  # Create a large formatted string to be disp
            if e.strip() != '':
                file_data += e
        self.Code_View_lbl.delete(1.0, END)  # Clear text
        self.Code_View_lbl.insert(END, file_data)  # Insert the file text
        self.Code_View_lbl.tag_configure("current_line", background="#e9e9e9")
        self.Code_View_lbl.tag_remove("current_line", 1.0, "end")
        self.Code_View_lbl.tag_add("current_line", 1.0, 2.0)

    def display_register(self):
        self.set_dataRegister_view()
        self.set_addressRegister_view()
        # for change in changes:
        #     if change[0] == "D":
        #         if self.data_view == "bin":
        #             self.dataRegisters[int(change[1])].config(text=bin(changes[change]))
        #         elif self.data_view == "hex":
        #             self.dataRegisters[int(change[1])].config(text=hex(changes[change]))
        #         else:
        #             self.dataRegisters[int(change[1])].config(text=changes[change])
        #     elif change[0] == "A":
        #         if self.address_view == "bin":
        #             self.addressRegisters[int(change[1])].config(text=bin(changes[change]))
        #         elif self.address_view == "hex":
        #             self.addressRegisters[int(change[1])].config(text=hex(changes[change]))
        #         else:
        #             self.addressRegisters[int(change[1])].config(text=changes[change])
