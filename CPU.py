from program_Counter import Program_Counter
from memory import Memory
from registers import Address_Register, Register
from commands import *


class CPU():
    """
    Central processing unit class, depending on it's internal program counter
    it runs code sotred in memory sepecified.
    """
    def __init__(self):
        memory = Memory()  # Initialize memory
        PC = Program_Counter()  # Initialize program counter

        # Initialize registers
        A = Address_Register()
        for i in range(8):
            A.add_register(i)

        D = Register()
        for i in range(8):
            D.add_register(i)
