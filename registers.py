DEBUG = True

class DataRegister():
    '''
    The data register class is meant to simulate a data structure.

    Attributes:
        _val (int): The value stored in the data register. It cannot be longer
                    than a longerword as guaranteed by the set method.
    '''
    def __init__(self):
        self._val = 0

    def get(self):
        '''
        Returns: the data register value
        '''
        return self._val

    def set(self, val, size):
        '''
        Sets the data register value based on the size.
        '''
        if size == 1:
            v = self._val & 0xffffff00
            val &= 0xff
        elif size == 2:
            v = self._val & 0xffff0000
            val &= 0xffff
        elif size == 4:
            v = self._val & 0x00000000
            val &= 0xffffffff
        self._val = v + val


class AddressRegister(DataRegister):
    '''
    Essentially another copy of the data register class but for implmentation
    it is important that they are treated as two seperate entities.

    # NOTE: We may add methods that are exclusive to the address register at
            a later date.
    '''
    def __init__(self):
        super().__init__()


class CCR():
    '''
    A class built to simulate the register that holds all the CCR information.
        Attributes:
            _val (int): The value of the CCR register. Although it is an int,
                        in it's binary format we have the following:
                        0bXNZVC.

            Example:    if _val = 12, then in binary _val = 0b01100 and so
                        X = 0, N = 1, Z = 1, V = 0, C = 0

    # NOTE: There is still a slight chance that V and C set methods are buggy.
            Especially with negative numbers.
    '''
    def __init__(self):
        self._val = 0

    def get_X(self):
        '''
        Returns: The 5th bit value of _val which is the X flag
        '''
        return (self._val >> 4)&1

    def get_N(self):
        '''
        Returns: The 4th bit value of _val which is the N flag
        '''
        return (self._val >> 3)&1

    def get_Z(self):
        '''
        Returns: The 3rd bit value of _val which is the Z flag
        '''
        return (self._val >> 2)&1

    def get_V(self):
        '''
        Returns: The 2nd bit value of _val which is the V flag
        '''
        return (self._val >> 1)&1

    def get_C(self):
        '''
        Returns: The 1st bit value of _val which is the C flag
        '''
        return (self._val >> 0)&1

    def set(self, X = None, N = None, Z = None, V = None, C = None):
        '''
        Sets each flag value that is not 'None' using the assignment methods.
        '''
        if X != None:
            self.assign_X(X)
        if N != None:
            self.assign_N(N)
        if Z != None:
            self.assign_Z(Z)
        if V != None:
            self.assign_V(V)
        if C != None:
            self.assign_C(C)

    def check_C(self, v, X = None):
        '''
        Test for the carry flag and sets it (automatically). If the X argument
        is not None, then it also sets the X flag.
        '''
        C = (v >> 8*4)&1
        print(hex(v), C)
        if X != None:
            X = C
        self.set(X = X, C = C)

    def check_N(self, v, z = 4):
        '''
        Test for negative flag and sets it automatically.
        '''
        N = (v >> z*8-1) & 1
        self.assign_N(N)

    def check_Z(self, v):
        '''
        Test for the zero flag and sets it automatically.
        '''
        if v == 0:  Z = True
        else:       Z = False
        self.assign_Z(Z)

    def check_V(self, s, d, r):
        '''
        Test for the overflow flag and sets it automatically.
        '''
        Sm = (s>>35)&1
        Dm = (d>>35)&1
        Rm = (r>>35)&1
        if (Sm == 1 and Dm == 1 and Rm == 0) or (Sm == 0 and Dm == 0 and Rm == 1):
            V = True
        else:
            V = False
        self.assign_V(V)

    def assign_X(self, x):
        '''
        Sets the X flag
        '''
        if x == True:
            self._val |= 0b10000
        else:
            self._val &= 0b01111

    def assign_N(self, n):
        '''
        Sets the N flag
        '''
        if n == True:
            self._val |= 0b01000
        else:
            self._val &= 0b10111

    def assign_Z(self, z):
        '''
        Sets the Z flag
        '''
        if z == True:
            self._val |= 0b00100
        else:
            self._val &= 0b11011

    def assign_V(self, v):
        '''
        Sets the V flag
        '''
        if v == True:
            self._val |= 0b00010
        else:
            self._val &= 0b11101

    def assign_C(self, c):
        '''
        Sets the C flag
        '''
        if c == True:
            self._val |= 0b00001
        else:
            self._val &= 0b11110

class ProgramCounter():
    '''
    The Program Counter directs the execution of each line in the assembly code.

    Attributes:
        _line (dict):
            The dictionary which holds the object of the line. This dictionary
            is usually a copy of _line_p from the AssemblyFileReader class.

        _label_dict (dict):
            The dictionary which holds the line number of each label. This dictionary
            is usually a copy of _label_dict from the AssemblyFileReader class.

        n (int):
            The line number n that program is currently at.

    # TODO:
        Add functionality with op codes.
    '''
    def __init__(self, line = dict(), label = dict()):
        self._line = line
        self._label_dict = label
        self.n = 0

    def exec_line(self):
        '''
        Executes the given line n, the increments to the next line.
        '''
        if self.n in self._line:
            self._line[self.n].review()
            self.n += 1

    def is_valid_label(self, label):
        '''
        Checks to see if a label exists in _label_dict.
            Returns:
                True - if a label exists
                False - otherwise
        '''
        if label in self._label_dict:
            return True
        else:
            return False

    def label_to_line_n(self, label):
        '''
        Changes n to the line number of the label.
        '''
        self.n = self._label_dict[label] - 1# since exec line will add 1


D = dict()
A = dict()

for i in range(8):
    D[i] = DataRegister() # initialize the data register
    A[i] = AddressRegister() # initialize the address register

A[7].set(0xFFFFF, 4)  # iInitialize stack pointer

ccr = CCR() # initialize the ccr
pc = ProgramCounter() # initialize the pc
