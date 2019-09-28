import sys
import os

print("Hello World")
print(sys.version[:5])
if sys.version[:5] == "3.7.1":
	assert 1
else:
	assert 0