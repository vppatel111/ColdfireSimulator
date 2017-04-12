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

        #TODO: need more testing!!!
    '''
    def __init__(self, l=None, c=None, z=None, s=None, d=None):
        self.label = l
        self.size = z
        self.source = s
        self.dest = d
        self.command = c
        self.s_inc = None # if the source is an EA, is being incremented/decremented in this line?
        self.d_inc = None # the set incrementer method sets these automatically
        self.set_incrementer()
        # self.review() - Temporarily disabling auto-review (Add as a feature)

    def review(self):
        '''
        This method executes the line as python code.
        Returns:    None

        #TODO:      Change command_dict to actual command object that invokes
                    both the command_dict as well as its method command.
        '''
        # execute command:
        if DEBUG and print(self.label, self.command, self.size, self.source, self.dest): pass
        Command(self.command, self.size, self.source, self.dest)
        # if self.source is not None:
        #     s = self.get_source()
        # if self.dest is not None:
        #     d = self.get_dest()

        self.adjust_incrementer()
        # if DEBUG and print("SOURCE: {} , DEST: {}".format(s, d)): pass

    def set_incrementer(self):
        if isinstance(self.source, EffectiveAddress):
            self.s_inc = self.source._inc
        if isinstance(self.dest, EffectiveAddress):
            self.d_inc = self.dest._inc

    def adjust_incrementer(self):
        if isinstance(self.source, EffectiveAddress):
            self.source._inc = self.s_inc
        if isinstance(self.dest, EffectiveAddress):
            self.dest._inc = self.d_inc

class AssemblyFileReader():
    '''
    Reads through the '.s' file and converts the assembly commands into python
    command for later execution.
    #NOTE:  Still a work in progresses as we might need to change a few elements
            when dealing with multiple files.
    #TODO:  -Fix the scale factor parsing.
            -Commenting is not supported yet.
    '''
    def __init__(self, file_name = None):
        self._filename = file_name  # file name
        self._file = []             # file unparsed
        self._line_a = []           # file parsed (assembly)
        self._line_p = dict()       # file parsed (python)
        self._label_dict = dict()   # to organize label to a line number
    #IDEA: potentially use a dictionary if we have multiple files?

    def read_into_list(self, file_name = None):
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
        '''

        if s is None:
            return None

        if s.startswith('-'):
            v = s[1:]
            c = re.compile(r"""
            \(
            %a(?P<register>\d)
            \)
            """, re.VERBOSE)
            i = int(c.match(v).group('register'))
            v = A[i]
            return memory.get_EA(v, False)

        elif s.endswith('+'):
            v = s[:-1]
            c = re.compile(r"""
            \(
            %a(?P<register>\d)
            \)
            """, re.VERBOSE)
            i = int(c.match(v).group('register'))
            v = A[i] # get address register
            return memory.get_EA(v, True) # get effective address

        elif s.startswith('(') and s.endswith(')'):
            v = s[1:-1]
            l = len(v.split(','))
            if l == 3:
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
                return memory.get_EA( A[i], None, offset, scale*factor)
            elif l == 2:
                c = re.compile(r"""
                \(
                (?P<offset>\d),
                %a(?P<address>\d)
                \)
                """, re.VERBOSE)
                offset = int(c.match(s).group('offset'))
                i = int(c.match(s).group('address'))
                return memory.get_EA( A[i], None, offset )
            elif l == 1:
                c = re.compile(r"""
                \(
                %a(?P<address>\d)
                \)
                """, re.VERBOSE)
                i = int(c.match(s).group('address'))
                return memory.get_EA(A[i])

        else:
            if s.startswith('#'):
                v = s[1:]
                if v.startswith('0x'):
                    v = int(v, 16)
                elif v.startswith('0b'):
                    v = int(v, 2)
                elif v.startswith('0o'):
                    v = int(v, 8)
                else:
                    v = int(v)
                return v

            elif s.startswith('%a'):
                return A[int(s[2:])]
            elif s.startswith('%d'):
                return D[int(s[2:])]
            elif s.startswith('0x'):
                v = int(s[2:], 16)
                return memory.get_EA(v)
            elif s.startswith('0b'):
                v = int(s[2:], 2)
                return memory.get_EA(v)
            elif s.startswith('0o'):
                v = int(s[2:], 8)
                return memory.get_EA(v)
        try:
            return int(s)
        except:
            return s

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
