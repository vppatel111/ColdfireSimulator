import memory
# from registers import DataRegister, AddressRegister, CCR
# from registers import DataRegister, AddressRegister, CCR, ProgramCounter
import registers
from commands import *
from unparser import AssemblyFileReader, line
# from program_counter import Program_Counter


class CPU():
    """
    Central processing unit class, depending on it's internal program counter
    it runs code sorted in memory specified.
    """
    def __init__(self):
        # Read in and store code.
        self.assembler = AssemblyFileReader('test.s')
        self.assembler.read_into_list()
        self.assembley_code = self.assembler._line_p

        self.pc = ProgramCounter(self.assembler._line_p, self.assembler._label_dict)  # Initialize program counter

        self.current_dataR_values = dict()
        self.current_addressR_values = dict()
        self.memory_monitor = dict()

        print("before")
        memory.memory.set(1000, 21, 4)
        print("CPU", memory.memory.get(1000, 4))

        for i in range(8):
            self.current_dataR_values[i] = 0
            self.current_addressR_values[i] = 0

    # NOTE: Creates a mem location, even if it is never used.
    def add_memory_monitor(self, address):
        print("add", address)
        self.memory_monitor[address] = memory.memory.get(int(address), 4)
        print(memory.memory.get(int(address), 1), memory.memory.get(int(address), 1))

    def execute_line(self, line_num):
        """
        Note: Line_num is not zero indexed and the dictionary is.
        """
        # global D
        self.assembler._line_p[line_num - 1].review()

        print("line", line_num-1, registers.D[2].get())

    def check_for_change(self):
        """
        This method looks through all data and address registers and looks for
        a change in values.
        Returns: Dictionary with list of changes in format:
        ('Register Type, #': New Value)
        """
        changes = dict()
        for i in range(8):
            if self.current_dataR_values[i] != registers.D[i].get():
                changes['D' + str(i)] = registers.D[i].get()
                self.current_dataR_values[i] = registers.D[i].get()
            if self.current_addressR_values[i] != registers.A[i].get():
                changes['A' + str(i)] = registers.A[i].get()
                self.current_addressR_values[i] = registers.A[i].get()

        for address in self.memory_monitor:
            self.memory_monitor[address] = memory.memory.get(int(address), 4)
            print("mem_mon", self.memory_monitor[address], memory.memory.get(1000, 4))

        return changes
