APP_DIR = "C:/Users/Andrew Shen/Desktop/ProjectEmerald/src2/test1"
PROJECT_FILE = "/project_test_4.dat"

token = {}
with open(APP_DIR+PROJECT_FILE, "r") as fbj:
	fdt = fbj.readlines()
	rd_line = 0

	for ln in fdt:
		line = ln.strip("\n")
		sepr = line[3:].split("$")
		token[line[1]] = {}
		token[line[1]]["type"] = line[0]
		token[line[1]]["val"] = 0
		token[line[1]]["status"] = "NONE"  # NONE|GO|IN|IDLE; node's input status
		if line[0] == "n":  # node
			token[line[1]]["expr"] = sepr[0]
			token[line[1]]["output"] = {}
			token[line[1]]["input"] = {}
			out = sepr[1][:-1].split( "," )  # [:-1] to remove trailing comma
			for w in out:
				key = w.split( ":" )
				token[line[1]]["output"][key[0]] = float( key[1] )
			inp = sepr[2][:-1].split( "," )  # [:-1] to remove trailing comma
			for w in inp:
				key = w.split( ":" )
				token[line[1]]["input"][key[0]] = float( key[1] )
		elif line[0] == "i":  # input
			token[line[1]]["fname"] = sepr[0]
			token[line[1]]["output"] = {}
			out = sepr[1][:-1].split( "," )  # [:-1] to remove trailing comma
			for w in out:
				key = w.split( ":" )
				token[line[1]]["output"][key[0]] = float(key[1])

			with open(APP_DIR+"/"+sepr[0], "r") as fbj:
				inpdt = fbj.readlines()

				token[line[1]]["val"] = inpdt[rd_line].strip("\n")
				token[line[1]]["status"] = "GO"
				rd_line += 1
		elif line[0] == "o":  # output
			token[line[1]]["fname"] = sepr[0]
			token[line[1]]["input"] = {}
			inp = sepr[1][:-1].split( "," )  # [:-1] to remove trailing comma
			for w in inp:
				key = w.split( ":" )
				token[line[1]]["input"][key[0]] = float( key[1] )
		elif line[0] == "b":  # bias (offset)
			pass

t = {"INP":"i", "OUT":"o", "NODE":"n", "BIAS":"b"}
def exec( obj ):
	for k in obj:
		print(k, ":", obj[k])

	run = True
	active_obj = []  # active object

	# for ind in obj:
	# 	if obj[ind]["type"] == t["INP"]:
	# 		for indext in obj[ind]["output"]:
	# 			active_obj.append(indext) if indext not in active_obj else 0

	# for i in active_obj:
	# 	for out in obj[i]["output"]:
	# 		obj[out]["val"] = 1
	# 	rd_ln += 1

	while run:
		for a in active_obj:
			if obj[a]["type"] == t["OUT"]:
				run = False

		for actv in active_obj:
			for idin in obj[actv]["output"]:
				calc = True
				for idext in obj[idin]["input"]:  # going through all the ids of input
					if obj[idext]["status"] != "GO":
						calc = False
					else:
						obj[idin]["status"] = "IN"  # one of the input has status set to GO
				if calc:  # if all input's node are status: GO
					for idext in obj[idin]["input"]:  # summation function
						obj[idin]["val"] += obj[idext]["val"]*obj[idext]["output"][idin]  # value*weight
					# activation function
					obj[idin]["status"] = "GO"
					active_obj.append( idin )
					for idin in active_obj:  # remove dead object in active_obj list
						dead = True  # if it is dead object
						for idext in obj[idin]["output"]:
							if obj[idext]["status"] != "GO":
								dead = False
						if dead:
							active_obj.remove( idin )



		# for k in obj:
		# 	print( k, obj[k] )

		print(active_obj)


exec( token )