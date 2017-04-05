from commands import *
from registers import *
from memory import *

class Resources():
    '''
    '''
    def get_source(self, o = None):
        '''
        Returns:    The value stored within the source.
        '''
        if o != None:
            self.source = o
        if isinstance(self.source, EffectiveAddress):
            return self.source.get()
        elif isinstance(self.source, DataRegister):
            return self.source.get()
        elif isinstance(self.source, AddressRegister):
            return self.source.get()
        else:
            return self.source

    def get_dest(self, o = None):
        '''
        Returns:    The value stored within the destination.
        '''
        if o != None:
            self.dest = o
        if isinstance(self.dest, EffectiveAddress):
            return self.dest.get()
        elif isinstance(self.dest, DataRegister):
            return self.dest.get()
        elif isinstance(self.source, AddressRegister):
            return self.dest.get()
        else:
            return self.dest

    def set_dest(self, val, size):
        '''
        Returns:        None
        Side effects:   Changes the value of the number stored in the destination.
        NOTE:   This method is mainly used set the new destination after applying
                the command.
        '''
        if isinstance(self.dest, EffectiveAddress):
            self.dest.set(val)
        elif isinstance(self.dest, DataRegister):
            self.dest.set(val, size)
        elif isinstance(self.dest, AddressRegister):
            self.dest.set(val, size)
