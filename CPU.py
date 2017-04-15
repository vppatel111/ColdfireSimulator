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
        self.assembly_code = self.assembler._line_p
        self.parsed_assembly_code = self.assembler._line_a

        self.pc = pc  # Initialize program counter
        self.pc._line = self.assembler._line_p
        self.pc._label_dict = self.assembler._label_dict

    def generate_op_code(self):
        print("Command: ", self.pc._line[self.pc.n].get_dest_address(),
              self.pc._line[self.pc.n].get_source_address())

        op_command_dict = {
                           'add':  "1101 DDD1 10EE EEEE",
                           'adda': "1101 DDD0 10ee eeee",
                           'move': "00XX RRRM MMee eeee",
                           'pea':  "0100 1000 01ee eeee"
        }
        command = op_command_dict[self.parsed_assembly_code[self.pc.n][1]]
        print(command)

    # NOTE: Creates a mem location, even if it is never used.
    def add_memory_monitor(self, address):
        print("add", address)
        address = self.string_to_num(address)
        self.memory_monitor[address] = self.memory.get(address, 4)
        print(memory.get(address, 1), self.memory.get(address, 1))
