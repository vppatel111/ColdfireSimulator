from commands import *
from registers import *
from memory import *

class Resources():
    '''
    This class contains all the frequently used methods that other classes may
    potentially need.
    '''
    def __init__(cls, cpu):
        cls._cpu = cpu

    def get_source(self, o = None):
        '''
        Returns:    The value stored within the source.
        '''
        if o != None:
            self.source = o
        if isinstance(self.source, EffectiveAddress):
            return self.source.get(self.size)
        elif isinstance(self.source, DataRegister):
            return self.source.get()
        elif isinstance(self.source, AddressRegister):
            return self.source.get()
        else:
            return self.source

    def get_source_address(self, o = None):
        '''
        Returns:    The address stored within the source, only works with
                    effective addresses.
        '''
        if o != None:
            self.source = o
        if isinstance(self.source, EffectiveAddress):  # Push in effective add
            return self.source.get_address(self.size)
        elif isinstance(self.source, AddressRegister):
            return self.source.get_address(self.size)

    def get_dest(self, o = None):
        '''
        Returns:    The value stored within the destination.
        '''
        if o != None:
            self.dest = o
        if isinstance(self.dest, EffectiveAddress):
            return self.dest.get(self.size)
        elif isinstance(self.dest, DataRegister):
            return self.dest.get()
        elif isinstance(self.dest, AddressRegister):
            return self.dest.get()
        else:
            return self.dest

    def set_dest(self, val, size):
        '''
        Returns:        None
        Side effects:   Changes the value of the number stored in the destination.
        NOTE:   This method is mainly used to set the new destination after applying
                the command.
        '''
        if isinstance(self.dest, EffectiveAddress):
            self.dest.set(val, size)
        elif isinstance(self.dest, DataRegister):
            self.dest.set(val, size)
        elif isinstance(self.dest, AddressRegister):
            self.dest.set(val, size)

    def set_source(self, val, size):
        '''
        Returns:        None
        Side effects:   Changes the value of the number stored in the source.
        NOTE:   This method is mainly used to set the new source after applying
                the command.
        '''
        if isinstance(self.source, EffectiveAddress):
            self.source.set(val, size)
        elif isinstance(self.source, DataRegister):
            self.source.set(val, size)
        elif isinstance(self.source, AddressRegister):
            self.source.set(val, size)

    def sign_extend(self, val):
        '''
        Sign extends val then returns new val. The extension only works for
        word sized val.
        '''
        extension_bit = (val >> 15)&1
        if extension_bit == 1 and val <= 0xFFFF:
            val |= 0xFFFF0000
        return val

    def twos_complement(self, val, size):
        '''
        Gets the two's complement of a given value based on a size for sign extension.
        '''
        if (val >> size*8-1)&1 == 1: # the value should be treated as a negative
            count = size*8-1
            pos = 0
            while count > -1:
                if (val>>count)&1 == 1:
                    pos += 1<<count
                count -= 1
            return -1*(count << size*8)+pos
        return val
