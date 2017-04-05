DEBUG = True

class DataRegister():
    '''
    '''
    def __init__(self):
        self._val = 0

    # def add_register(self, index, value = 0):
    #     if index not in self._register:
    #         self._register[index] = self.split_val(value)

    def split_val(self, val):
        return [(val >> i & 0xff) for i in (0, 8, 16, 24)]

    def cat_val(self, v_arr):
        tmp = v_arr
        val = 0
        for i in (0, 8, 16, 24):
            if tmp != []:
                val += tmp.pop() << i
        return val

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
        # if index not in self._register:
            # pass # TODO: give error
        # if size <= 4 and size >= 1:
        #     b_arr = self.split_val(val)
        #     for i in range(size):
        #         self._val[i] = b_arr.pop()

class AddressRegister(DataRegister):
    def __init__(self):
        super().__init__()

D = dict()
A = dict()

for i in range(8):
    D[i] = DataRegister()
    A[i] = AddressRegister()

PC = AddressRegister()
# source/dest type dictionary
sd_type_dict = {
        r'%a': lambda i: A.get(i), # address register
        r'%d': lambda i: D.get(i), # data register
        r'#' : lambda i: int(i), # immediate
        }
