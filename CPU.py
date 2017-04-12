from memory import memory
# from registers import DataRegister, AddressRegister, CCR
from registers import ccr, D, A, pc
# import registers
from commands import *
from unparser import AssemblyFileReader, line

# from program_counter import Program_Counter


class CPU():
    """
    Central processing unit class, depending on it's internal program counter
    it runs code sorted in memory specified.
    """
    def __init__(self, filename):
        # Read in and store code.
        self.ccr = ccr
        self.memory = memory
        self.D = D
        self.A = A

        print("ccr", self.ccr, "D", self.D, "memory")
        self.assembler = AssemblyFileReader(filename)
        self.assembler.read_into_list()
        self.assembley_code = self.assembler._line_p

        self.pc = pc  # Initialize program counter
        self.pc._line = self.assembler._line_p
        self.pc._label_dict = self.assembler._label_dict

        # for i in range(8):
        #     self.current_dataR_values[i] = 0
        #     self.current_addressR_values[i] = 0

    # NOTE: Creates a mem location, even if it is never used.
    def add_memory_monitor(self, address):
        print("add", address)
        address = self.string_to_num(address)
        self.memory_monitor[address] = self.memory.get(address, 4)
        print(memory.get(address, 1), self.memory.get(address, 1))
