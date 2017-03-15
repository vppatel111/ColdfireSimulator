DEBUG = True

class Register():
    '''
    '''
    def __init__(self):
        self._register = dict()

    def add_register(self, index, value = [bytes(0), bytes(0), bytes(0), bytes(0)]):
        if index not in self._register:
            self._register[index] = value

    def get(self, index):
        return self._register.get(index)

    def set(self, index, val, size):
        if index not in self._register:
            pass # TODO: give error
        if size <= 4 and size >= 1:
            b_arr = bytesarray(val)
            for i in range(size):
                self._register[index][i] = b_arr.pop()

D = Register()
A = Register()

for i in range(8):
    D.add_register(i)
    A.add_register(i)

PC = Register()
# source/dest type dictionary
sd_type_dict = {
        '%a': lambda i: A.get(i), # address register
        '%d': lambda i: D.get(i), # data register
        '#' : lambda i: int(i), # immediate
        }
