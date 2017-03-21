DEBUG = True

from commands import *
from registers import *
from memory import *

class AssemblyFileReader():
    '''
    '''
    def __init__(self, file_name = None):
        self._filename = file_name  # file name
        self._file = []             # file unparsed
        self._line_a = []           # file parsed (assembly)
        self._line_p = dict()       # file parsed (python)
        self._label_dict = dict()   # to organize label to a line number

    #IDEA: potentially use a dictionary if we have multiple files?

    def read_into_list(self, file_name = None):
        if file_name != None:
            self.file_name = file_name
        with open(self._filename) as f:
            self._file = f.readlines()
            #self._line_a = [line.strip().split() for line in self._line_a]
            for line in self._file:
                line = line.strip().split()
                if self.is_label(line[0]):
                    label = line.pop(0)
                    self._label_dict[label] = self._file.index(line)
                else:
                    label = None
                (command, size) = self.break_command_size(line[0])
                (source, dest) = self.break_source_dest(line[1])
                self._line_a.append((label, command, size, source, dest))
            f.close()
        if DEBUG and print(self._line_a):
            pass
        self.process_line()

    def process_line(self):
        '''
        if the last character of the str is ':' it is a label
        if the first character of the str is '%', it is a register
        '''
        n = 0
        for line in self._line_a:
            (l, c, z, s, d) = line
            s_val = self.parse_source_or_dest(s)
            d_val = self.parse_source_or_dest(d)
            self._line_p[n] = command_dict[c](s_val, d_val, z)
            n += 1
            # if DEBUG and print("source: {}, dest: {}".format(s_val, d_val.get())):
                # pass

    def is_label(self, s):
        if s[-1] == ':':
            return True
        else:
            return False

    def is_command(self, command):
        if command in command_dict:
            return True
        else:
            return False

    def parse_source_or_dest(self, s):
        # if s.startswith('(') and s.endswith(')'):
        #     s = s[1:-1]
        # elif s.startswith('-(') and s.endswith(')'):
        #     s = s[2:-1]
        # elif s.startswith('(') and s.endswith(')+'):
        #     s = s[1:-2]
        for t in sd_type_dict:
            if s.startswith(t):
                v = s.replace(t, '')
                if v.startswith('0x'):
                    v = int(v, 16)
                elif v.startswith('0b'):
                    v = int(v, 2)
                elif v.startswith('0o'):
                    v = int(v, 8)
                else:
                    v = int(v)
                return sd_type_dict[t](v)
            # else:
            #     if s in self._label_dict:
            #         return s
            #     else:
            #         return int(s) # unknown type, flag error?

    def break_command_size(self, s):
        (command, size) = s.lower().split('.')
        if size in size_dict:
            size = size_dict[size]
        else:
            size = None
        if self.is_command(command):
            return command, size
        else:
            pass # raise error

    def break_source_dest(self, s):
        source, dest = [e.strip().lower() for e in s.split(',')]
        return source, dest

assembler = AssemblyFileReader('test.s')
assembler.read_into_list()
