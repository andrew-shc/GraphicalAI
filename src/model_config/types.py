OCT     = "0o"  # Octal: 0-7
HEX     = "0x"  # Hexadecimal: 0-F
BIN     = "0b"  # Binary: 0, 1
INT     = "0i"  # Integer: 0-9
FLT     = "0f"  # Floating-Point Number: 0-9 w/ decimal

# any type
class Any:
	def __init__(self, dt=None):
		self.DATA = dt

	def __repr__(self):
		return str(self.__class__.__name__)+": "+str(self.DATA)

# any number from float to binary
class Number(Any):
	def __init__(self, dt=None):
		prefix = dt[:2]
		number = dt[2:]
		if type(dt) in [int, float]:
			self.DATA = dt
		elif prefix in [OCT, HEX, BIN, INT, FLT]:
			if prefix == "0o":
				for c in number:
					pass
			self.DATA = dt
		raise ValueError(f"Value {dt} is not number")

	def __repr__(self):
		return str(self.DATA)

# any type that consists of group of another type
class Collections(Any):
	def __init__(self, dt=None):
		prefix = dt[:2]
		number = dt[2:]
		if type(dt) in [int, float]:
			self.DATA = dt
		elif prefix in ["0o", "0x", "0b"]:
			if prefix == "0o":
				pass
			self.DATA = dt
		raise ValueError(f"Value {dt} is not number")

	def __repr__(self):
		return str(self.DATA)


class Integer(Number):
	def __init__(self, dt=None):
		if type(dt) not in [Integer]:
			pass
		self.DATA = dt

	def __repr__(self):
		pass

# a = Number("woah")

print("12345"[2:])