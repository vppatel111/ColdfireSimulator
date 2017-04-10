'''
This contains all the commands related to assembly language.
See Coldfire Manual for full details on how commands work.
'''
from resources import Resources
from registers import *
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
		  # Data Manipulation Commands
		  'move': 	lambda: self.move(),
		  'movea':	lambda: self.movea(),
		  # 'moveq':	lambda: self.moveq(), -- Extra
		  # 'movem':	lambda: self.movem(), -- Extra
		  # 'move ccr':		lambda: self.move_ccr(), -- Extra

		  # Stack Manipulation/Address Affecting Commands
		  'lea':		lambda: self.lea(),  # Necessary
		  'pea':		lambda: self.pea(),  # Necessary

		  # Branching Commands
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
		  # 'link':		lambda: self.link(),
		  # 'unlk':		lambda: self.unlk(),


		  # Extra: Bit tests and do something functions.
		  # 'bchg':		lambda: self.bchg(),
		  # 'bclr':		lambda: self.bclr(),
		  # 'bset':		lambda: self.bset(),
		  # 'btst':		lambda: self.btst(),

		  # Arithmetic Commands
		  'add':		lambda: self.add(),
		  'adda':		lambda: self.adda(),
		  # 'addi':		lambda: self.addi(),  -- Extra
		  # 'addq':		lambda: self.addi(),  -- Extra
		  # 'addx':		lambda: self.addi(),  -- Extra

		  'sub':		lambda: self.sub(),
		  'suba':		lambda: self.suba(),
		  # 'subi':		lambda: self.subi(), -- Extra
		  # 'subq':		lambda: self.subq(), -- Extra
		  # 'subx':		lambda: self.subx(), -- Extra

		  'divs':		lambda: self.divs(),  # Necessary
		  'divu':		lambda: self.divu(),  # Necessary

		  'muls':		lambda: self.muls(),  # Necessary
		  'mulu':		lambda: self.mulu(),  # Necessary

		  'clr':		lambda: self.clr(),

		  # Logical Commands
		  'asl':		lambda: self.asl(),
		  'asr':		lambda: self.asr(),

		  'and':		lambda: self._and(),
		  # 'andi':		lambda: self._and(), -- Extra

		  'or':		lambda: self._or(),
		  # 'ori':		lambda: self._ori(),
		  'eor':		lambda: self._eor(),
		  # 'eori':		lambda: self._eori(), -- Extra

		  'not':		lambda: self._not(),
		  'neg':		lambda: self.neg(),
		  # 'negx':		lambda: self.neg(), -- Extra

		  'cmp':		lambda: self.cmp(),
		  'cmpa':		lambda: self.cmpa(),
		  'cmpi':		lambda: self.cmpi(),

		  # Miscellaneous Commands
		  # 'tas':		lambda: self._tas(),
		  # 'tst':		lambda: self._tst(),
		  'nop':		lambda: self._nop()
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
		new_d = self.get_dest()
		# CCR: - * * 0 0
		ccr.set(N = ccr.check_N(new_d), Z = ccr.check_Z(new_d), V = 0, C = 0)

	def movea(self):
		pass

	def bra(self):
		# GUARD:
		if not pc.is_valid_label(self.source):
			raise Exception('The label: "{}" does not exist!'.format(self.source))
		# exec command:
		else:
			pc.label_to_line_n(self.source)
		# CCR: - - - - -

	def bne(self):
		# GUARD: None
		# exec command:
		Z = ccr.get_Z()
		if Z == 0:
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def beq(self):
		# GUARD: None
		# exec command:
		Z = ccr.get_Z()
		if Z == 1:
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def ble(self):
		# GUARD = None
		# exec command:
		Z = ccr.get_Z()
		N = ccr.get_N()
		V = ccr.get_V()
		if (Z == 1 or (N == 1 and V == 0) or (N == 0 and V == 1)):
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def bge(self):
		# GUARD = None
		# exec command:
		Z = ccr.get_Z()
		N = ccr.get_N()
		V = ccr.get_V()
		if (Z == 1 or (N == 1 and V == 1) or (N == 0 and V == 0)):
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def blt(self):
		# GUARD = None
		# exec command:
		Z = ccr.get_Z()
		N = ccr.get_N()
		V = ccr.get_V()
		if ((N == 1 and V == 0) or (N == 0 and V == 1)):
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def bgt(self):
		# GUARD = None
		# exec command:
		Z = ccr.get_Z()
		N = ccr.get_N()
		V = ccr.get_V()
		if ((Z == 0 and N == 1 and V == 1) or (Z == 0 and N == 0 and V == 0)):
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def bcc(self):
		# GUARD = None
		# exec command:
		C = ccr.get_C()
		if C == 0:
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def bcs(self):
		# GUARD = None
		# exec command:
		C = ccr.get_C()
		if C == 1:
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def bvs(self):
		# GUARD = None
		# exec command:
		V = ccr.get_V()
		if V == 1:
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def bvc(self):
		# GUARD = None
		# exec command:
		V = ccr.get_V()
		if V == 0:
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def bpl(self):
		# GUARD = None
		# exec command:
		N = ccr.get_N()
		if N == 0:
			self.bra()
		else:
			pass
		# CCR: - - - - -

	def bmi(self):
		# GUARD = None
		# exec command:
		N = ccr.get_N()
		if N == 1:
			self.bra()
		else:
			pass
		# CCR: - - - - -

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
