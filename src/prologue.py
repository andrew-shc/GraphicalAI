from src.model_config.graphic import *


# TODO: Abolish Mini-Node Render
def node( surf, pos, func, mn_node_size=(200, 100), ):
	return {
		"surf"   : surf,
		"clicked": None,  # FIELD|MAIN|NONE
		"movable": True,
		"pos"    : pos,
		"size"   : [mn_node_size[0], mn_node_size[1]],
		"title"  : "node",
		"fld_style": {
			"pad"   : 2,  # padding between fields
			"height": 20,  # width depends the value inside
			"nd_sz" : 10,  # size of the node (square)
			"nd_pad": [2, 2],  # (x,y) x, the selection node x-padding for the border; y, the padding between nodes
		},
		"fld_dt" : { # field data
			"fieldI"   : {"input1":[], "input2":[]},  # e.g. input1:[[ID, FIELD_NO], [ID, FIELD_NO], [ID, FIELD_NO]]
			"fieldO"   : {"output1":[], "output2":[]},  # e.g. output2:[[ID, FIELD_NO], [ID, FIELD_NO], [ID, FIELD_NO]]
			"multiple" : {"inp": False, "out": True},  # if should the input or/and output only have multiple "connections"
			"selected" : {"type": None, "field": None},  # type : INP|OUT, field: [FIELD_NUMBER]
		},
		"executor": func, # which function to execute with fieldI and fieldO as input and output
	}


def button( surf, pos, size, txt, func, font="arial", font_size=24 ):  # standard button
	return {
		"surf"     :surf,
		"clicked"  :None,  # MAIN|NONE
		"trigger"  :None,  # NONE|ON|OFF
		"movable"  :False,
		"pos"      :pos,
		"size"     :size,
		"label"    : {
			"text"     : txt,
			"font"     : font,
			"font-size": font_size,
		},
		"function" :func,  # run that specific event function
	}
