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
    def __init__(self):
        self._val = 0

    def auto_assign(self, v, X = None):
        N = Z = V = C = None
        # check for negative
        if v < 0:   N = True
        else:       N = False
        # check for zero
        if v == 0:  Z = True
        else:       Z = False
        # check for overflow

        # check for carry

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

D = dict()
A = dict()

for i in range(8):
    D[i] = DataRegister()
    A[i] = AddressRegister()

PC = AddressRegister()
ccr = CCR()
# source/dest type dictionary
sd_type_dict = {
        r'%a': lambda i: A.get(i), # address register
        r'%d': lambda i: D.get(i), # data register
        r'#' : lambda i: int(i), # immediate
        }
