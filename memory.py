class Memory():
    '''
    '''
    def __init__(self):
        self._mem = dict()

    def add_block(self, loc=None, val=0):
        '''
        '''
        if loc not in self._mem:
            self._mem[loc] = val

    def _break_val(self, val):
        pass
