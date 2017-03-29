class Memory():
    '''
    Dynamic memory class, this is essentially a large dictionary that can
    be accessed using (mem).add_block(loc, val) and (mem).get_block(loc).
    Where the amount of memory used depends on how much is initialized or
    used during runtime of assembly program.

    Note: Resets after every execution of SimulatorMain.
    '''
    def __init__(self):
        self._mem = dict()

    # TODO: Break up data and store each byte of data separately.
    def add_block(self, loc=None, val=0):
        '''
        Adds given data into memory beginning at loc and stored in 1 byte
        chunks.
        '''
        if loc not in self._mem:
            self._mem[loc] = val

    def get_block(self, loc=None):  # Added
        '''
        Returns the value stored at the requested block.
        '''
        if loc not in self._mem:
            print("Error")  # Requesting memory that hasn't been assigned
            return 0
        else:
            return self._mem[loc]

    def _break_val(self, val):  # Not sure what this does.
        pass

    # DEBUG Feature: Prints current memory location.
    def print_block(self, loc=None):
        '''
        Prints the value at the requested memory location. Assumes that the
        memory has been assigned.
        '''
        if loc is not None:
            print(self._mem[loc])
        else:
            print("0")
