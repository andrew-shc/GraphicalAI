import yaml
import math

dat = yaml.safe_load(open("test.yaml", "r").read())

print(dat["stuff"]["binary_character"])


def enc(num, base=128):
	if num == 0: return [0]
	place = 1
	val = []
	after_zero = False
	while num%(base**place)//base**(place-1) != 0 or not after_zero or len(val) == 0:
		val.insert(0, num%(base**place)//base**(place-1))
		if val[0] != 0:
			after_zero = True
		place += 1
	return val

def dec(num, base=128):
	val = 0
	for digit, n in enumerate(reversed(num)):
		val += n*base**(digit)
	return val

# print(bytearray([128+i for i in enc(128)])+b"NORMAL")

def bin_trans(s, trns):
	dt = s
	for k in trns: dt=dt.replace(k, trns[k])
	return dt
a=bin_trans(b"Hello World", {b"ll":b"y", b"o":b"x"})

print(enc(217))
print(dec([1, 89]))