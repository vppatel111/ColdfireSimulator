import re
from commands import *
from registers import *
from memory import *
from resources import Resources

DEBUG = True

class line(Resources):
    '''
    The line object contains and handles all the processing of the assembly line
    code as python code. As such, it holds all the information of a given line.

    Attributes:
        label (str):    Holds the label of the line, if there exists a label, else
                        it is None by default.

        command (str):  The command that is being executed in the line. It is a
                        string so that we can invoke the command using command_dict.

        size (int):     Holds the size of the command being executed (in bytes).
                        ie. If command is being executed as a longword, the size
                        that will be stored is 4. Similarly word has a size of 2.

        source (obj):   The source is either an instance of the effective address
                        class, register class, or an immediate (integer) value.

        destination (obj):  Similar to source, that is, it is an instance of the
                        effective address class, or register class, but cannot be
                        an immediate value.

        s_inc (bool):   Set to None unless the source is an effective address (EA)
                        with a post-increment or pre-decrement option. If the
                        EA is being post-incremented the value is set to True;
                        if it is being pre-decremented the value is set to False.

        d_inc (bool):   Exactly the same principles of s_inc apply to d_inc except
                        that d_inc is specified for the destination rather than
                        the source.

        #TODO: need more testing!!!
    '''
    def __init__(self, l=None, c=None, z=None, s=None, d=None):
        self.label = l
        self.size = z
        self.source = s
        self.dest = d
        self.command = c
        self.s_inc = None # if the source is an EA, is it being incremented/decremented in this line?
        self.d_inc = None # the set incrementer method sets these automatically
        self.set_incrementer()
        # self.review() - Temporarily disabling auto-review (Add as a feature)

    def review(self):
        '''
        This method executes the line as python code.
        Returns:        None
        Side effects:   Creates an instance of the Command class and runs the command.
                        Then resets incrementer if possible.
        '''
        # execute command:
        if DEBUG and print(self.label, self.command, self.size, self.source, self.dest): pass
        Command(self.command, self.size, self.source, self.dest)
        self.adjust_incrementer()

    def set_incrementer(self):
        '''
        Sets the initial value of the incrementer.
        IE. if the source (or destination) is an EA, it will check to see whether
            or not it is being incremented and saves that information into
            s_inc and d_inc respectively.s
        '''
        if isinstance(self.source, EffectiveAddress):
            self.s_inc = self.source._inc
        if isinstance(self.dest, EffectiveAddress):
            self.d_inc = self.dest._inc

    def adjust_incrementer(self):
        '''
        Regarding the source and destination, if either are an EA, reset their
        incrementer as they are disabled during the running of their respective
        commands to avoid multiple incrementations (or decrementations).
        '''
        if isinstance(self.source, EffectiveAddress):
            self.source._inc = self.s_inc
        if isinstance(self.dest, EffectiveAddress):
            self.dest._inc = self.d_inc


class AssemblyFileReader():
    '''
    Reads through the '.s' file and converts the assembly commands into python
    command for later execution. Also stores raw information of each file for
    later use.

    Attributes:
        _filename (str):    Name of the given file.

        _file (list):       A list of strings where each string is the unparsed
                            line in the file.

        _line_a (list):     A list of tuples containing the parsed strings of each line.
                            The tuple is in the format:
                                (label, command, size, source, destination)
                            Where if any of the elements do not exist, it is set to None
                            by default.

        _line_p (dict):     A dictionary containing the pythonic version of the assembly code
                            where the key is the line number. Each line number maps
                            to an instance of the line class.

        _label_dict (dict): A dictionary where the key is a label (if any) which
                            maps to the line number of when the label was "labeled".

    #NOTE:  Still a work in progress as we might need to change a few elements
            when dealing with multiple files.
    #TODO:  -Fix the scale factor parsing.
            -Commenting is not supported yet.
    '''
    def __init__(self, file_name=None):
        self._filename = file_name  # file name
        self._file = []             # file unparsed
        self._line_a = []           # file parsed (assembly)
        self._line_p = dict()       # file parsed (python)
        self._label_dict = dict()   # to organize label to a line number
    # IDEA: potentially use a dictionary if we have multiple files?

    def read_into_list(self, file_name=None):
        '''
        Invokes various methods to seperate, the label, command, size,
        source, and destination into a tuple for further parsing.

        The tuple is stored into _line_a (self) and is blueprinted as follows:
            _line_a[line number] = (label, command, size, source, dest)

        #NOTE:  Under this phase of the program, everything stored into the tuple
                is still a string type
        '''
        c = re.compile(r"""
        \s*                     # skip white space
        ((?P<label>.*)\:)?
        \s*
        ((?P<command>[a-z]+)?(\.(?P<size>[b|w|l]))?
        \s*
        (?P<source>.+?)?        # source group
        \s* (, \s*              # skip white space before/after comma
        (?P<dest>.*)?)?)?       # dest group
        \s*$                    # skip white space until end of line
        """, re.VERBOSE)
        if file_name != None:
            self.file_name = file_name
        with open(self._filename) as f:
            self._file = f.readlines()
            for line in self._file:
                line = line.strip().lower()
                if line == '':
                    continue
                l = c.search(line)
                label = l.group('label')
                command = l.group('command')
                size = l.group('size')
                source = l.group('source')
                dest = l.group('dest')
                # if DEBUG and print([label, command, size, source, dest]): pass
                self._line_a.append((label, command, size, source, dest))
            f.close()
        self.process_line()

    def process_line(self):
        '''
        This method will take everything stored into the tuple and convert the
        strings into their equivalent python objects using the parse functions.
        Line[n] is stored into self._line_p.
        '''
        n = 0 # line number (0 indexed)
        for e in self._line_a:
            (l, c, z, s, d) = e
            if l != None and l not in self._label_dict:
                self._label_dict[l] = n
            if z in size_dict:
                z = size_dict[z]
            s = self.parse_source_or_dest(s, z)
            d = self.parse_source_or_dest(d, z)
            if DEBUG and print(e): pass
            self._line_p[n] = line(l, c, z, s, d)
            n += 1

    def parse_source_or_dest(self, s, z):
        '''
        This method parses the source and destination strings into python objects

        Arguments:
            s (str): The string that must be in either source/destination format
                     which will under go parsing
            z (int): The size of the operation, specifically needed for predecrement
                     and postincrementing registers

        Returns
            s (obj): The pythonic object of that string.
                        ie. '%a0' will return the instance of the AddressRegister
                        class that represents the register a0.

        # NOTE: There is a strong chance that offsetting is still buggy.
        '''

        if s is None: # then this element does not exist, so dont worry about it.
            return None

        if s.startswith('-'): # then assume pre-decrementation is occuring.
            v = s[1:]
            c = re.compile(r"""
            \(
            %a(?P<register>\d)
            \)
            """, re.VERBOSE)
            i = int(c.match(v).group('register'))
            v = A[i] # get address register as an object since the EA will be "dynamic"
            return memory.get_EA(v, False) # set the effective address based off of that register object

        elif s.endswith('+'): # then assume post-incrementation is occuring.
            v = s[:-1]
            c = re.compile(r"""
            \(
            %a(?P<register>\d)
            \)
            """, re.VERBOSE)
            i = int(c.match(v).group('register'))
            v = A[i] # get address register as an object
            return memory.get_EA(v, True) # get effective address based off of the register

        elif s.startswith('(') and s.endswith(')'): # then there are 3 possibilities
            v = s[1:-1]
            l = len(v.split(','))
            if l == 3: # the format is (offset, address register, scale*factor)
                c = re.compile(r"""
                \(
                (?P<offset>\d),
                %a(?P<address>\d),
                (%d(?P<scale>\d)\s*(\*\s*(?P<factor>\d))?)
                \)
                """, re.VERBOSE)
                offset = int(c.match(s).group('offset'))
                i = int(c.match(s).group('address'))
                scale = int(c.match(s).group('scale'))
                factor = int(c.match(s).group('factor'))
                if factor == None:
                    factor = 1
                return memory.get_EA( A[i], None, offset, scale*factor) # get the effective address
            elif l == 2: # the format is (offset, address register)
                c = re.compile(r"""
                \(
                (?P<offset>\d),
                %a(?P<address>\d)
                \)
                """, re.VERBOSE)
                offset = int(c.match(s).group('offset'))
                i = int(c.match(s).group('address'))
                return memory.get_EA( A[i], None, offset )
            elif l == 1: # the format is (address register)
                c = re.compile(r"""
                \(
                %a(?P<address>\d)
                \)
                """, re.VERBOSE)
                i = int(c.match(s).group('address'))
                return memory.get_EA(A[i])

        else:
            if s.startswith('#'): # it is a immediate value
                v = s[1:]
                if v.startswith('0x'): # convert as hex
                    v = int(v, 16)
                elif v.startswith('0b'): # convert as binary
                    v = int(v, 2)
                elif v.startswith('0o'): # convert as octal
                    v = int(v, 8)
                else:
                    v = int(v) # treat as a normal decimal
                return v

            elif s.startswith('%a'): # it is an address register
                return A[int(s[2:])]
            elif s.startswith('%d'): # it is a data register
                return D[int(s[2:])]
            # if it is a raw number, then it is an effective address:
            elif s.startswith('0x'): # hex
                v = int(s[2:], 16)
                return memory.get_EA(v)
            elif s.startswith('0b'): # binary
                v = int(s[2:], 2)
                return memory.get_EA(v)
            elif s.startswith('0o'): # octal
                v = int(s[2:], 8)
                return memory.get_EA(v)
        try:
            return int(s) # try to convert to a decimal integer if possible
        except:
            return s # else it must be a string value -ie. perhaps a label?

# for debugging without using the GUI:
def debugging():
    assembler = AssemblyFileReader('test.s')
    assembler.read_into_list()
    pc._line = assembler._line_p
    pc._label_dict = assembler._label_dict
    while(True):
        if input():
            pc.exec_line()
            for address in memory._mem:
                if type(address) == int:
                    print('address:', hex(address).upper(),
                    'value:', hex(memory.get(address, 1)).upper(),
                    'ccr:', bin(ccr._val)
                    )

# debugging()
