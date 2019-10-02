GENERIC = {
		"surf"   : None,
		"clicked": None,  # FIELD|MAIN|NONE
		"movable": True,
		"pos"    : [0, 0],
		"size"   : [0, 0],
		"title"  : "node",
		"fld_style": {
			"pad"   : 2,  # padding between fields
			"height": 20,  # width depends the value inside
			"nd_sz" : 10,  # size of the node (square)
			"nd_pad": [2, 2],  # (x,y) x, the selection node x-padding for the border; y, the padding between nodes
		},
		"fld_dt" : { # field data
			"fieldI"    : {},  # e.g. input1:[[ID, FIELD_NO], [ID, FIELD_NO], [ID, FIELD_NO]]
			"fieldItype": {}, # the type of ui input it should use per field (i.e. DropDown, FileAutoRead)
			"fieldO"    : {},  # e.g. output2:[[ID, FIELD_NO], [ID, FIELD_NO], [ID, FIELD_NO]]
			"fieldOtype": {}, # the type of ui input it should use per field (i.e. DropDown, FileAutoRead)
			"multiple"  : {"inp": False, "out": True},  # if should the input or/and output only have multiple "connections"
			"selected"  : {"type": None, "field": None},  # type : INP|OUT, field: [FIELD_NUMBER]
		},
		"executor": None, # which function to execute with fieldI and fieldO as input and output
}

def InputNode( surf, pos, func, mn_node_size=(200, 100), ):
	state = GENERIC.copy()
	state["surf"] = surf
	state["pos"] = pos
	state["size"] = mn_node_size
	state["executor"] = func
	state["title"] = "InputNode"
	state["fld_dt"] = {
		"fieldI"    :{"input"},
		"fieldItype":{""},
		"fieldO"    :{},
		"fieldOtype":{},
		"multiple"  :{"inp":False, "out":True},
		"selected"  :{"type":None, "field":None},
	}
	return state
