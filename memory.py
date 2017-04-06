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
    def __init__(self, a, v = 0):
        self.val = v
        self._address = a
    def get(self, z):
        return memory.get(self._address, z)

    def set(self, v):
        memory.set(self._address, v)

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

    def get(self, address, size=1):
        v = 0
        for z in range(size):
            if (address+size-z-1) not in self._mem:
                self._mem[address+size-z-1] = EffectiveAddress(address)
            v += self._mem.get(address+size-z-1).val << z*8
        return v

    def set(self, address, val):
        b = 0xFF
        v = val
        offset = 0
        while v > 0:
            self._mem[address+offset] = EffectiveAddress(v & b)
            v >>= 8
            offset += 1

memory = Memory()
