from registers import AddressRegister
class EffectiveAddress():
    '''
    An instance of an effective address in memory which is called by the Memory
    class.

    Attributes:
        val (int):  Holds the value contained within the specified address. This
                    value cannot be longer than a byte. By default, all values are 0.

        _address (int): The memory location of the effective address (cannot be
                        longer than a longword).

    #TODO: Add a guard for the val and address so they do not exceed a byte and longword
           respectively.
    '''
    def __init__(self, a, v = 0, is_increment = None, offset = None, sf = None):
        self.val = v
        self._address = a
        self._inc = is_increment
        self._offset = offset
        self._sf = sf

    def get(self, z):
        address = self.get_address(z)
        return memory.get(address, z)

    def set(self, v, z):
        address = self.get_address(z)
        memory.set(address, v, z)

    def get_address(self, z):
        if isinstance(self._address, AddressRegister):
            address = self._address.get()
            if self._inc == False: # decrement address register
                self._address.set(address-z, 4)
                address = self._address.get()
            elif self._inc == True:
                self._address.set(address+z, 4)
            self._inc = None
        else:
            address = self._address
        return address

class Memory():
    '''
    This class handles all the memory components of the Coldfire simulator.

    Attributes:
        _mem (dict):    The _mem  dictionary organizes all the memory locations with
                        an effective address. The key to the dictionary is the memory
                        location while the value is an instance of the effective address
                        class.
    '''
    def __init__(self):
        self._mem = dict()

    def get_EA(self, address, inc = None, offset = None, sf = None):
        if address not in self._mem:
            self._mem[address] = EffectiveAddress(address, is_increment = inc, offset = offset, sf = sf)
        return self._mem[address]

    def get(self, address, size=1):
        v = 0
        for z in range(size):
            if (address+size-z-1) not in self._mem:
                self._mem[address+size-z-1] = EffectiveAddress(address+size-z-1)
            v += self._mem.get(address+size-z-1).val << z*8
        return v

    def set(self, address, val, size):
        b = 0xFF  # one byte
        v = val
        for z in range(size):
            self._mem[address+size-z-1] = EffectiveAddress(address+size-z-1, v & b)
            v >>= 8 # shift by one byte

memory = Memory()
