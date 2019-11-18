
# to remove a set of character from a string
s = "Random Text"
dat = s.translate({ord(i): None for i in 'characters to be removed'})
print(dat)