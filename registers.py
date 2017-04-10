DEBUG = True

class DataRegister():
    '''
    '''
    def __init__(self):
        self._val = 0

    def get(self):
        # return self.cat_val(self._val)
        return self._val

    def set(self, val, size):
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

    # NOTE: There is still a strong chance that V and C set methods are buggy.
            Especially with negative numbers.
    '''
    def __init__(self):
        self._val = 0

    def get_X(self):
        return (self._val >> 4)&1

    def get_N(self):
        return (self._val >> 3)&1

    def get_Z(self):
        return (self._val >> 2)&1

    def get_V(self):
        return (self._val >> 1)&1

    def get_C(self):
        return (self._val >> 0)&1

    def set(self, X = None, N = None, Z = None, V = None, C = None):
        if X is not None:
            self.assign_X(X)
        if N is not None:
            self.assign_N(N)
        if Z is not None:
            self.assign_Z(Z)
        if V is not None:
            self.assign_V(V)
        if C is not None:
            self.assign_C(C)

    def check_C(self, v, X = None):
        C = (v >> 8*4)&1
        if C == 1:
            C = True
        else:
            C = False
        if X != None:
            X = C
        self.set(X = X, C = C)

    def check_N(self, v):
        if v < 0:   N = True
        else:       N = False
        self.set(N = N)

    def check_Z(self, v):
        if v == 0:  Z = True
        else:       Z = False
        self.set(Z = Z)

    def check_V(self, s, d, r):
        Sm = (s>>35)&1
        Dm = (d>>35)&1
        Rm = (r>>35)&1
        if (Sm == 1 & Dm == 1 & Rm == 0) or (Sm == 0 & Dm == 0 & Rm == 1):
            V = True
        else:
            V = False
        self.set(V = V)

    def assign_X(self, x):
        if x == True:
            self._val |= 0b10000
        else:
            self._val &= 0b01111

    def assign_N(self, n):
        if n == True:
            self._val |= 0b01000
        else:
            self._val &= 0b10111

    def assign_Z(self, z):
        if z == True:
            self._val |= 0b00100
        else:
            self._val &= 0b11011

    def assign_V(self, v):
        if v == True:
            self._val |= 0b00010
        else:
            self._val &= 0b11101

    def assign_C(self, c):
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
        while self.n in self._line:
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
        self.n = self._label_dict[label] - 1 # since exec line will add 1

D = dict()
A = dict()

for i in range(8):
    D[i] = DataRegister()
    A[i] = AddressRegister()

ccr = CCR()
pc = ProgramCounter()
# source/dest type dictionary
sd_type_dict = {
        r'%a': lambda i: A.get(i), # address register
        r'%d': lambda i: D.get(i), # data register
        r'#' : lambda i: int(i), # immediate
        }
