'''
This contains all the commands related to assembly language.
See Coldfire Manual for full details on how commands work.
'''
from resources import Resources
from registers import *
import memory
DEBUG = False
# dictionary of sizes
size_dict = {
			'l': 4,
			'w': 2,
			'b': 1
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
		  'lea':		lambda: self.lea(),
		  'pea':		lambda: self.pea(),

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
		  # 'link':		lambda: self.link(), -- Extra
		  # 'unlk':		lambda: self.unlk(), -- Extra


		  # Extra: Bit tests and do something functions.
		  # 'bchg':		lambda: self.bchg(),
		  # 'bclr':		lambda: self.bclr(),
		  # 'bset':		lambda: self.bset(),
		  # 'btst':		lambda: self.btst(),

		  # Arithmetic Commands
		  'add':		lambda: self.add(),
		  'adda':		lambda: self.adda(),
		  'addi':		lambda: self.addi(),
		  'addq':		lambda: self.addi(),
		  # 'addx':		lambda: self.addi(),  -- Extra

		  'sub':		lambda: self.sub(),
		  'suba':		lambda: self.suba(),
		  'subi':		lambda: self.subi(),
		  'subq':		lambda: self.subq(),
		  # 'subx':		lambda: self.subx(), -- Extra

		  # 'divs':		lambda: self.divs(), -- Extra
		  'divu':		lambda: self.divu(),

		  # 'muls':		lambda: self.muls(),  -- Extra
		  'mulu':		lambda: self.mulu(),

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
		# Move a value.
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
		ccr.set(N = ccr.check_N(s, z), Z = ccr.check_Z(s), V = 0, C = 0)

	def movea(self):
		# Moves an address given at source into an address register.
		if isinstance(self.dest, AddressRegister):
			s = self.get_source()
			d = self.get_dest()
			z = self.size
			if z == 1:
				valid = False
				print("Error: Invalid Size")
			elif z == 2:
				s &= 0xffff
				if s > 65535:  # Negative therefore we must sign extend
					d = 0xffff0000
				else:		   # Otherwise we set 0
					d = 0x00000000
				valid = True
			elif z == 4:
				d &= 0x00000000
				s &= 0xffffffff
				valid = True

			if valid:  # If all checks passed, execute operation
				self.set_dest(s+d, 4)  # Addresses are always longwords
				new_d = self.get_dest()
				# CCR: - - - - -
				ccr.set(X=None, N=None, Z=None, V=None, C=None)
		else:
			print("Error: Invalid Destination")

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
		s = self.get_source()
		d = self.get_dest()

		z = self.size
		if z == 1:
			print("Error: Invalid size")
		elif z == 2:
			print("Error: Invalid Size")
		elif z == 4:
			result = s+d  # Calculate and truncate
			# print("SUPER DUPER RESULT", result)
			self.set_dest(result, z)
			new_d = self.get_dest()
			print(s, d, result)
			# CCR: * * * * *
			ccr.set(
					N = ccr.check_N(new_d),
					Z = ccr.check_Z(new_d),
					V = ccr.check_V(s, d, new_d),
					C = ccr.check_C(result, X = True))

	def adda(self):
		# Adds any source to an address register.
		if isinstance(self.dest, AddressRegister):
			s = self.get_source()
			d = self.get_dest()
			z = self.size
			if z == 1:
				print("Error: Invalid size")
			elif z == 2:
				print("Error: Invalid Size")
			elif z == 4:
				s &= 0xffffffff  # This may be unnecessary
				self.set_dest(s+d, z)

				# CCR: - - - - -
				ccr.set()
		else:
			print("Error: Invalid Destination")

	def addi(self):
		# Adds an immediate value to any source.
		if isinstance(self.dest, DataRegister) and type(self.source) == int:
			s = self.get_source()
			d = self.get_dest()
			z = self.size

			if z == 1:
				print("Error: Invalid size")
			elif z == 2:
				print("Error: Invalid size")
			elif z == 4:
				result = (s+d) # Calculate and truncate
				self.set_dest(result, z)
				new_d = self.get_dest()
				print(s, d, result)
				# CCR: * * * * *
				ccr.set(
						N = ccr.check_N(new_d),
						Z = ccr.check_Z(new_d),
						V = ccr.check_V(s, d, new_d),
						C = ccr.check_C(result, True))

		else:
			print("Error: Invalid Destination")

	def addq(self):
		# Adds an immediate value between 1-8 to the source.
		if type(self.source) == int and self.source >= 0 and self.source <= 7:
			self.addi()
		else:
			raise Exception("Source not an immediate value!")

	def sub(self):
		# Subtracts any source and destination together.
		s = self.get_source()
		d = self.get_dest()

		old_s = self.get_source()  # Used in ccr calculations
		old_d = self.get_dest()

		z = self.size
		if z == 1:
			print("Error: Invalid size")
		elif z == 2:
			print("Error: Invalid Size")
		elif z == 4:
			s &= 0xffffffff

			result = (d-s) & 0xffffffff  # Truncate
			self.set_dest((result), z)
			new_d = self.get_dest()

			# CCR: * * * * *
			ccr.set(X = None,
					N = ccr.check_N(new_d),
					Z = ccr.check_Z(new_d),
					V = ccr.check_V(-1*old_s, old_d, new_d),
					C = ccr.check_C(old_d + -1*old_s, True))

	def suba(self):
		# Subtracts any source and destination address register together.
		if isinstance(self.dest, AddressRegister):

			s = self.get_source()
			d = self.get_dest()

			old_s = self.get_source()
			old_d = self.get_dest()

			z = self.size
			if z == 1:
				print("Error: Invalid size")
			elif z == 2:
				print("Error: Invalid Size")
			elif z == 4:
				s &= 0xffffffff

				result = (d-s) & 0xffffffff  # Truncate
				# print("SUPER DUPER RESULT", result)
				self.set_dest((result), z)
				new_d = self.get_dest()

				# CCR: - - - - -
				ccr.set(X = None,
						N = None,
						Z = None,
						V = None,
						C = None)

		else:
			print("Error: Invalid Destination")

	def subi(self):
		# Subtracts any immediate value from the source.
		if type(self.source) == int:
			self.sub()
		else:
			raise Exception("Source is not an immediate value!")

	def subq(self):
		# Subtracts any immediate value between 1-8 from the source.
		if type(self.source) == int and self.source >= 0 and self.source <= 7:
			self.sub()
		else:
			raise Exception("Source is not an immediate value")

	def clr(self):
		# Clears a number of bits from a data register
		if isinstance(self.source, DataRegister):
			s = self.get_source()
			z = self.size
			if z == 1:
				s &= 0xffffff00
			elif z == 2:
				s &= 0xffff0000
			elif z == 4:
				s &= 0x00000000

			self.set_source(s, z)  # Set source depending on bits cleared.

			# CCR: - 0 1 0 0
			ccr.set(X = None, N = 0, Z = 1, V = 0, C = 0)
		else:
			print("Error: Invalid Source")

	def divu(self):
		# Performs unsigned integer division on the destination by the source
		s = self.get_source()
		d = self.get_dest()
		z = self.size

		old_s = self.get_source()  # Used in ccr calc
		old_d = self.get_dest()

		rem = d % s  # Process remainder
		rem = rem << 16
		rem &= 0xffff0000  # Truncate

		quot = d // s  # Process divisor

		if z == 1:
			valid = False
			print("Error: Invalid Size")
		elif z == 2:  # For words we combine the remaider and quotience
			quot &= 0x0000ffff  # Truncate
			d = (rem | quot)
			valid = True
		elif z == 4:
			d = quot & 0xffffffff  # Truncate
			valid = True

		if valid:
			self.set_dest(d, z)
			new_d = self.get_dest()

			# CCR: - * * * 0
			ccr.set(X = None,
					N = ccr.check_N(new_d),
					Z = ccr.check_Z(new_d),
					V = ccr.check_V(old_s, old_d, new_d),
					C = 0)

	def mulu(self):
		# Multiplies the source and destination together, and the result
		# is stored in the destination.
		s = self.get_source()
		d = self.get_dest()

		result = 0
		if z == 1:
			print("Error: Invalid Size")
			valid = False
		elif z == 2:  # Both are effectively the same however.
			result = s * d
			valid = True
		elif z == 4:
			result = s * d
			result &= 0xffffffff  # Truncate into a longword
			valid = True

		if valid:
			self.set_dest(result, z)
			new_d = self.get_dest()
			# CCR: - * * 0 0
			ccr.set(X = None,
					N = ccr.check_N(new_d),
					Z = ccr.check_Z(new_d),
					V = 0,
					C = 0)

	def neg(self):
		if isinstance(self.source, DataRegister):
			old_s = self.get_source()
			self.set_source(0-old_s, 4)
			s = self.get_source()
			ccr.set(
				N = ccr.check_N(s),
				Z = ccr.check_Z(s),
				V = ccr.check_V(0, s, old_s),
				C = ccr.check_C(s, True)
			)
		else:
			raise Exception("Source not a data register!")


	def asl(self):
		# Shifts a value left by 0-8 bits.
		if isinstance(self.dest, DataRegister):
			s = self.get_source()
			d = self.get_dest()
			z = self.size

			if s >= 0 and s <= 8:  # Bit shift must be 0-8 bits
				d = d << s
				C_bit = d >> 32
				C_bit = C_bit & 0x01  # Take a look at what the last bit was
				d &= 0xffffffff  # Truncate

				self.set_dest(d, z)
				new_d = self.get_dest()  # For ccr calc.

				# CCR: * * * 0 *
				ccr.set(X = C_bit,
						N = ccr.check_N(new_d),
						Z = ccr.check_Z(new_d),
						V = 0,
						C = C_bit)
			else:
				print("Error: Invalid shift")
		else:
			print("Error: Invalid Destination")

	def asr(self):

		# Shifts a value rigt by 0-8 bits
		if isinstance(self.dest, DataRegister):
			s = self.get_source()
			d = self.get_dest()
			z = self.size

			if s >= 0 and s <= 8:  # Bit shift must b 0-8 bits.
				d = d >> s  # NOTE: Not sure if python accounts for sign ext.
				C_bit = d >> s - 1
				C_bit = C_bit & 0x01  # Take a look at what the last bit was
				d &= 0xffffffff  # Truncate

				self.set_dest(d, z)
				new_d = self.get_dest()

				# CCR: * * * 0 *
				ccr.set(X = C_bit,
						N = ccr.check_N(new_d),
						Z = ccr.check_Z(new_d),
						V = 0,
						C = C_bit)

			else:
				print("Error: Invalid shift")
		else:
			print("Error: Invalid Destination")

	def _and(self):

		z = self.size
		if z == 1 or z == 2:
			print("Error: Invalid Size")
		elif z == 4:
			s = self.get_source()
			d = self.get_dest()

			d = s & d  # Take advantage of python
			self.set_dest(d, 4)
			new_d = self.get_dest()  # For ccr calculations

			# CCR: - * * 0 0
			ccr.set(X = None,
					N = ccr.check_N(new_d),
					Z = ccr.check_Z(new_d),
					V = 0,
					C = 0)

	def _andi(self):
		if type(self.source) == int:
			self._and()
		else:
			raise Exception("The source is not an immediate value!")

	def _or(self):

		z = self.size
		if z == 1 or z == 2:
			print("Error: Invalid Size")
		elif z == 4:
			s = self.get_source()
			d = self.get_dest()

			d = s | d  # Take advantage of python
			self.set_dest(d, 4)
			new_d = self.get_dest()  # For ccr calc

			# CCR: * * * 0 0
			ccr.set(X = None,
					N = ccr.check_N(new_d),
					Z = ccr.check_Z(new_d),
					V = 0,
					C = 0)

	def _eor(self):

		if isinstance(self.dest, DataRegister):
			z = self.size
			if z == 1 or z == 2:
				print("Error: Invalid Size")
			elif z == 4:
				s = self.get_source()
				d = self.get_dest()

				d = d ^ s  # Continued python abuse
				self.set_dest(d, 4)
				new_d = self.get_dest()  # Ccr calc

				# CCR: * * * 0 0
				ccr.set(X = None,
						N = ccr.check_N(new_d),
						Z = ccr.check_Z(new_d),
						V = 0,
						C = 0)
		else:
			print("Error: Invalid Source")

	def _not(self):

		z = self.size
		if z == 1 or z == 2:
			print("Error: Invalid Size")
		elif z == 4:
			s = self.get_source()

			s = ~s  # Python abuse
			self.set_source(s, 4)
			new_s = self.get_source()

			# CCR: * * * 0 0
			ccr.set(X = None,
					N = ccr.check_N(new_s),
					Z = ccr.check_Z(new_s),
					V = 0,
					C = 0)

	def cmp(self):
		if isinstance(self.dest, DataRegister):
			s = self.get_source()
			d = self.get_dest()
			z = self.size
			if z == 1:
				s &= 0x000000ff
				d &= 0x000000ff
			elif z == 2:
				s &= 0x0000ffff
				d &= 0x0000ffff
			elif z == 4:
				s &= 0xffffffff
				d &= 0xffffffff

			result = d-s
			# CCR: * * * * *
			ccr.set(X = None,  # Hope ccr functions work
					N = ccr.check_N(result),
					Z = ccr.check_Z(result),
					V = ccr.check_V(result),
					C = ccr.check_C(result, True))

	def cmpa(self):
		if isinstance(self.dest, AddressRegister):
			s = self.get_source()
			d = self.get_dest()
			z = self.size
			if z == 1:
				s &= 0x000000ff
				d &= 0x000000ff
			elif z == 2:
				s &= 0x0000ffff
				d &= 0x0000ffff
			elif z == 4:
				s &= 0xffffffff
				d &= 0xffffffff

			result = d-s
			# CCR: * * * * *
			ccr.set(X = None,  # Hope ccr functions work
					N = ccr.check_N(result),
					Z = ccr.check_Z(result),
					V = ccr.check_V(result),
					C = ccr.check_C(result, True))

	def cmpi(self):
		if type(self.source) == int:
			s = self.get_source()
			d = self.get_dest()
			z = self.size
			if z == 1:
				s &= 0x000000ff
				d &= 0x000000ff
			elif z == 2:
				s &= 0x0000ffff
				d &= 0x0000ffff
			elif z == 4:
				s &= 0xffffffff
				d &= 0xffffffff

			result = d-s
			# CCR: * * * * *
			ccr.set(X = None,  # Hope ccr functions work
					N = ccr.check_N(result),
					Z = ccr.check_Z(result),
					V = ccr.check_V(result),
					C = ccr.check_C(result, True))

	def lea(self):
		# Sets an address register to the specified EffectiveAddress
		s = self.get_source_address()
		self.set_dest(s, 4)

		# CCR: - - - - -

	def pea(self):  # NOTE: A7 or SP is initialized in registers.
		# Pushes an EffectiveAddress onto the top of the stack.
		s = self.get_source_address()
		a = memory.memory.get_EA(A[7])
		a.set(s, 4)
		next_add = A[7].get() - 4
		A[7].set(next_add, 4)

		# CCR: - - - - -
