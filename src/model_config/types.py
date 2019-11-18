"""
The 3 basic node types and then the MFHTS Implementation #1
"""
import math


OCT = "0o"  # Octal: 0-7
HEX = "0x"  # Hexadecimal: 0-F
BIN = "0b"  # Binary: 0, 1
INT = "0i"  # Integer: 0-9
FLT = "0f"  # Floating-Point Number: 0-9 w/ decimal


# any type
class Any:
    def __init__(self, dt=None):
        self.DATA = dt

    def __str__(self):
        return str(self.__class__.__name__)+": "+str(self.DATA)


class Void(Any):
    def __init__(self):
        super().__init__(None)

    def __str__(self):
        return "Void"


class Number(Any):
    def __init__(self, n):
        if type(n) in [int, float]:
            super().__init__(n)
        else:
            raise ValueError(f"Error: The class <Number> received an invalid number: {n}")

    def __str__(self):
        return str(self.DATA)

    def __add__(self, other): return self.DATA+other.DATA

    def __sub__(self, other): return self.DATA-other.DATA

    def __mul__(self, other): return self.DATA-other.DATA

    def __truediv__(self, other):
        if other.DATA != 0: return self.DATA/other.DATA
        else: return 0

    def __floordiv__(self, other): return self.DATA//other.DATA

    def ceil(self, other): return math.ceil(self.DATA/other.DATA)

    def __mod__(self, other): return self.DATA%other.DATA

    def __pow__(self, power, modulo=None): return self.DATA**power.DATA

    def __lt__(self, other): return self.DATA < other.DATA

    def __le__(self, other): return self.DATA <= other.DATA

    def __eq__(self, other): return self.DATA == other.DATA

    def __ne__(self, other): return self.DATA != other.DATA

    def __ge__(self, other): return self.DATA >= other.DATA


class Collections(Any):
    def __init__(self, *args):
        super().__init__(args)

    def __len__(self): return len(self.DATA)



def numberTest():
    a = Number(45)
    b = Number(5)
    c = Number(3.9)
    print(a+b)
    print(a-b)
    print(a*b)
    print(a/b)
    print(a/Number(0))
    print(a/c)
    print(a//c)
    print(a.ceil(c))
    print(a%b)
    print(a**b)
    print(a>b)
    print(a>=b)
    print(a==b)
    print(a<=b)
    print(a<b)
    print([0, 0, 0, 1, 1] > [0, 0])

    a += Number(3)

a = Collections(1, 3, 4, 3, 6, 3)
print(len(a))
print()