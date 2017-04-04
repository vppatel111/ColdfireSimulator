DEBUG = True

# NOTE: Does not correctly convert data into bytes and stores them.


def convert_to_bytes(val):
    '''
    Converts any integer to a 32 binary representation and returns it in the
    format: [(MSB)Byte1, Byte2, Byte3, (LSB)Byte4]
    '''
    pass


class Register():
    '''
    Basic register class, can be used for both address and data registers
    as they are extremely similar. Each register stores up to 32 bits of data.

    Idea: To account for address wrapping, we should use inheritance for
    separate data and address registers. OR, add additional functions that
    account for data or address registers.
    '''
    def __init__(self):
        self._register = dict()

    def add_register(self, index, value=[bytes(0), bytes(0),
                                         bytes(0), bytes(0)]):

        if index not in self._register:
            self._register[index] = value

    def get(self, index):
        return self._register.get(index)

    def set(self, index, val, size):
        self._register[index][1] = val
        # if index not in self._register:
        #     pass  # TODO: give error
        #     print("error")
        # if size <= 4 and size >= 1:
        #     # b_arr = bytearray(val)
        #     b_arr = val
        #     for i in range(size):
        #         self._register[index][i] = b_arr.pop()


class Address_Register(Register):
    '''
    Uses inheritance to create address registers that account for address
    wrapping.
    '''
    def __init__(self):
        Register.__init__(self)

    def set(self, index, val, size):
        self._register[index][1] = val
        # if index not in self._register:
        #     pass  # TODO: give error
        # if size == 4:
        #     # b_arr = bytearray(val)
        #     b_arr = val
        #     for i in range(size):
        #         self._register[index][i] = b_arr.pop()
        # elif size == 2:
        #     # b_arr = bytearray([val])
        #     # print(b_arr)
        #     b_arr = val
        #
        #     if b_arr[-1] == 1:  # Check if sign extension necessary.
        #         sign_extend = True
        #     else:
        #         sign_extend = False
        #
        #     for i in range(size):  # Fill up memory
        #         self._register[index][i] = b_arr.pop()
        #
        #     if sign_extend:  # Sign extend accordingly
        #         for i in range(size):
        #             self._register[index][i] = 1
        #     else:
        #         for i in range(size):
        #             self._register[index][i] = 1
        #
        # else:
        #     pass  # TODO: Error


if __name__ == '__main__':  # I'm just going to assume this is DEBUG code.

    D = Register()
    A = Register()

    for i in range(8):
        D.add_register(i)
        A.add_register(i)

    PC = Register()
    # source/dest type dictionary
    sd_type_dict = {
            '%a': lambda i: A.get(i),  # address register
            '%d': lambda i: D.get(i),  # data register
            '#': lambda i: int(i),  # immediate
            }
