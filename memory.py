class EffectiveAddress():
    def __init__(self, a, v = 0):
        self.val = v
        self.address = a
    def get(self):
        return self.val

    def set(self, v):
        memory.set(self.address, v)

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

    def get(self, address):
        if address not in self._mem:
            self._mem[address] = EffectiveAddress(address)
        return self._mem.get(address)

    def set(self, address, val):
        b = 0xFF
        v = val
        offset = 0
        while v > 0:
            self._mem[address+offset] = EffectiveAddress(v & b)
            v >>= 8
            offset += 1

memory = Memory()
