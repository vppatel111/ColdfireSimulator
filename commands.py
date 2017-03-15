'''
This contains all the commands related to assembly language.
See Coldfire Manual for full details on how commands work.
'''

# dictionary of sizes
size_dict = {
		'l' : 4,
		'w' : 2,
		'b' : 1,
}

class Command():
	'''
	The base command file that contains the common attributes for all the commands
	in Coldfire (ie. all commands contain a source or/and destination)
	'''
	def __init__(self, source = None, dest = None, size = None):
		self._source = source
		self._destination = dest
		self._size = size

	def get_source():
		return self._source

	def get_destination():
		return self._destination

	def get_size():
		return self._size

	def set_source(s):
		self._source = s

	def set_destination(d):
		self._destination = d

	def set_size(s):
		self._size = s

	def get_dest_type(d):
		pass

class Move(Command):
	def __init__(self, s, d, z):
		super().__init__(s, d, z)

class Bra(Command):
	'''
	'''
	def __init__(self, label=None):
		super().__init__(label)
# set of commands that will eventually be a part of our simulation
command_dict = {
		'move': lambda s,d,z: Move(s,d,z)} #'movea',
		# 'bra', 'bne', 'beq', 'ble', 'bge', 'blt', 'bgt', 'bcc', 'bcs', 'bvc', 'bvs', 'bpl', 'bmi',
		# 'add', 'adda', 'addi',
		# 'sub', 'suba', 'subi',
		# 'clr',
		# 'neg',
		# 'asl', 'asr',
		# 'and', 'or', 'eor', 'not',
		# 'cmp', 'cmpa', 'cmpi',
		# }
