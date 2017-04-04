DEBUG = True

from commands import *
from registers import *
from memory import *

# NOTE: Though I added some functions on top ,there is definitely room for combining
# functions into each other instead of functions calling each other alot
class AssemblyFileReader():
    '''
    Assembler class, contains a series of functions for parsing through files.
        unparse(self) - Reads in and processes entire file, returning formatted
            data that can be stored in memory.
        parse_file(self. file_name) - Reads in and returns an entire file as
            a raw string that can be displayed in a Text widget.

    '''
    def __init__(self, file_name=None):
        self._filename = file_name  # file name
        self._file = []             # file unparsed
        self._line_a = []           # file parsed (assembly)
        self._line_p = dict()       # file parsed (python)
        self._label_dict = dict()   # to organize label to a line number

    # IDEA: potentially use a dictionary if we have multiple files?

    def read_into_list(self, file_name=None):
        if file_name is not None:
            self.file_name = file_name
        with open(self._filename) as f:
            self._file = f.readlines()
            # self._line_a = [line.strip().split() for line in self._line_a]
            for line in self._file:
                line = line.strip().split()
                if self.is_label(line[0]): # BUG: Cannot handly empty lines
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
        # self.process_line() Temporarily disable processing

    def unparse(self):
        """
        Will preform the functionality of read into list and store the output
        in memory starting at 0, unless otherwise specified.
        """
        pass

    def parse_file(self, file_name=None):
        """
        Parses the file and obtains a large raw string that will be put into
        the text widget. Then calls unparser to process file data.
        """
        if file_name is not None:
            self.file_name = file_name
        with open(self._filename) as f:
            self._file_contents = f.read()

        f.close()
        return self._file_contents

    def process_line(self):
        '''
        if the last character of the str is ':' it is a label
        if the first character of the str is '%', it is a register
        '''
        n = 0
        for line in self._line_a:
            (l, c, z, s, d) = line
            s_val = self.get_source_dest(s)
            d_val = self.get_source_dest(d)
            self._line_p[n] = command_dict[c](s_val, d_val, z)
            n += 1
        #if DEBUG and print(self._line_p, '\n', s_val, d_val, z):
        #    pass

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

    def get_source_dest(self, s):
        for t in sd_type_dict:
            if s.startswith(t):
                v = int(s.replace(t, ''))
                return sd_type_dict[t](v)
        else:
            if s in label_dict:
                return s
            else:
                return int(s) # unknown type, flag error?

    def break_command_size(self, s):
        (command, size) = s.lower().split('.')
        if size in size_dict:
            size = size_dict[size]
        else:
            size = None
        if self.is_command(command):
            return command, size
        else:
            pass  # raise error

    def break_source_dest(self, s):
        source, dest = [e.strip().lower() for e in s.split(',')]
        return source, dest


assembler = AssemblyFileReader('test.s')
assembler.read_into_list()
