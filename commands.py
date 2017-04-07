'''
This contains all the commands related to assembly language.
See Coldfire Manual for full details on how commands work.
'''
from resources import Resources
DEBUG = True
# dictionary of sizes
size_dict = {
		'l' : 4,
		'w' : 2,
		'b' : 1,
}


class Command(Resources):
	'''
	The base command file that contains the common attributes for all the commands
	in Coldfire (ie. all commands contain a source or/and destination)
	'''
	def __init__(self, c, z, s, d):
		# set of commands that will eventually be a part of our simulation
		self.size = z
		self.source = s
		self.dest = d

		command_dict = {
			'move': 	lambda: self.move(),
			'movea':	lambda: self.movea(),

			'bra':		lambda: self.bra(),
			'bne':		lambda: self.bne(),
			'beq':		lambda: self.beq(),
			'ble':		lambda: self.ble(),
			'bge':		lambda: self.bge(),
			'blt':		lambda: self.blt(),
			'bgt':		lambda: self.bgt(),
			'bcc':		lambda: self.bcc(),
			'bcs':		lambda: self.bcs(),
			'bvc':		lambda: self.bvc(),
			'bvs':		lambda: self.bvs(),
			'bpl':		lambda: self.bpl(),
			'bmi':		lambda: self.bmi(),

			# Extra: Bit tests and do something functions.
			# 'bchg':		lambda: self.bchg(),
			# 'bclr':		lambda: self.bclr(),
			# 'bset':		lambda: self.bset(),
			# 'btst':		lambda: self.btst(),

			'add':		lambda: self.add(),
			'adda':		lambda: self.adda(),
			'addi':		lambda: self.addi(),  # Extra
			'addq':		lambda: self.addi(),  # Extra
			'addx':		lambda: self.addi(),  # Extra

			'sub':		lambda: self.sub(),
			'suba':		lambda: self.suba(),
			'subi':		lambda: self.subi(),

			'clr':		lambda: self.clr(),
			'neg':		lambda: self.neg(),

			'asl':		lambda: self.asl(),
			'asr':		lambda: self.asr(),

			'and':		lambda: self._and(),
			'andi':		lambda: self._and(), # Extra
			'or':		lambda: self._or(),
			'eor':		lambda: self._eor(),
			'not':		lambda: self._not(),

			'cmp':		lambda: self.cmp(),
			'cmpa':		lambda: self.cmpa(),
			'cmpi':		lambda: self.cmpi(),
			}
		if c in command_dict:
			command_dict[c]()

	def move(self):
		s = self.get_source()
		d = self.get_dest()
		z = self.size
		if z == 1:
			d &= 0xffffff00
			s &= 0xff
		elif z == 2:
			d &= 0xffff0000
			s &= 0xffff
		elif z == 4:
			d &= 0x00000000
			s &= 0xffffffff
		self.set_dest(s+d, z)

	def movea(self):
		pass

	def bra(self):
		pass

	def bne(self):
		pass

	def beq(self):
		pass

	def ble(self):
		pass

	def bge(self):
		pass

	def blt(self):
		pass

	def bgt(self):
		pass

	def bcc(self):
		pass

	def bcs(self):
		pass

	def bvs(self):
		pass

	def bpl(self):
		pass

	def bmi(self):
		pass

	def add(self):
		# Adds any source and destination together.
		# BUG: Does not account for overflow etc.
		s = self.get_source()
		d = self.get_dest()
		z = self.size
		if z == 1:
			s &= 0xff
		elif z == 2:
			s &= 0xffff
		elif z == 4:
			s &= 0xffffffff
		self.set_dest(s+d, z)

	def adda(self):
		pass

	def addi(self):
		# Adds any source and destination together.
		# BUG: Does not account for overflow etc.
		# TODO: Errors?
		s = self.get_source()
		d = self.get_dest()
		z = self.size
		if z == 1:
			s &= 0xff
		elif z == 2:
			s &= 0xffff
		elif z == 4:
			s &= 0xffffffff
		self.set_dest(s+d, z)

	def sub(self):
		# Subtracts any source and destination together.
		# BUG: Does not account for overflow etc.
		s = self.get_source()
		d = self.get_dest()
		z = self.size
		if z == 1:
			s &= 0xff
		elif z == 2:
			s &= 0xffff
		elif z == 4:
			s &= 0xffffffff
		self.set_dest(s-d, z)

	def suba(self):
		pass

	def subi(self):
		pass

	def clr(self):
		pass

	def neg(self):
		pass

	def asl(self):
		pass

	def asr(self):
		pass

	def _and(self):
		pass

	def _or(self):
		pass

	def _eor(self):
		pass

	def _not(self):
		pass

	def cmp(self):
		pass

	def cmpa(self):
		pass

	def cmpi(self):
		pass
