class Program_Counter():
    """
    Program counter class, which is simply initialized to the starting address
    for the program and contains functions for incrementing counter, or
    changing program execution
    """
    def __init__(self):
        self.pc = 0

    def set(self, address=0):
        if address >= 0:
            self.pc = address
        else:
            print("Invalid PC address location")

    def get(self):
        return self.pc

    def increment(self, increment_by):
        self.pc += increment_by
