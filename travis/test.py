import sys
import os

print("Hello World")
print(sys.version[:6])
if sys.version[:6] == "3.7":
	assert 1
else:
	assert 0