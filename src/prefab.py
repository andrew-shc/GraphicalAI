# for storing pre fabricated entities (grouped entities)

def fileInput(): pass
def selectionNode(): pass
def inPut(): pass  # input node
def outPut(): pass  # output node
def userDef(): pass  # user defined variable within software

# Node Enabler: class with a stored attributes for node id to whom to connect
class NdEn:
	BoxInp = "bx/inp"
	BoxOut = "bx/out"

def textField(world, obj_id, pos, rect, size, text, font="arial", font_color=(0, 0, 0), backg=(255,255,255)):
	world.create( obj_id=obj_id, pos=pos, rect=rect, color=backg, at=False, font=font, font_size=size, font_color=font_color,
	              font_align={"x":"center", "y":"center"}, text=text, text_align=True, cursor=0 )

def Node(world, obj_id, pos, rect, color=(0, 0, 0)):
	world.create(obj_id=obj_id, pos=pos, rect=rect, color=color, clicked=False, connectee=[], connect_en=["nodeA"],
	             connect_tg="nodeA" )

def Box(world, obj_id, master_id, pos, rect, text, field):
	world.create( obj_id=obj_id, pos=pos.copy(), rect=[rect[0], rect[1]], color=(150, 200, 255) )  # output area
	world.create( obj_id=obj_id, pos=pos.copy(), rect=[rect[0]/2, rect[1]], color=(170, 220, 255) )  # input area
	world.create( obj_id=obj_id, pos=pos.copy(), rect=[rect[0], rect[1]/4], color=(220, 220, 220) )  # title area

	world.create( obj_id=obj_id, pos=pos.copy(), rect=[rect[0], rect[1]/4], font="mono", font_size=15, font_color=(0, 0, 0),
	              font_align={"x":"center", "y":"center"}, text=text, text_align=True )  # title text

	# master controller entity for the box
	world.create( obj_id=master_id, child=obj_id, pos=pos.copy(), rect=rect, clicked=False, movable=True,
	              placement_ofs=[None, None],  field=field )

def BoxField(world, obj_id, pos, rect, ptxt, stxt, typ, name, x_align, cnct_en, tag):
	# field shape, data, and wires
	world.create( obj_id=obj_id, pos=pos,
	              rect=rect, color=(0, 0, 0), fld_nm=name, fld_typ=typ, fld_dt=None, clicked=False,
	              connectee=[], connect_en=cnct_en, connect_tg=tag)
	# field text
	world.create( obj_id=obj_id, pos=ptxt,
	              rect=stxt, font="mono", font_size=12, font_color=(0, 0, 0), text_align=True,
	              font_align={"x":x_align, "y":"center"}, text=name )

def BoxInpField(world, obj_id, pos, rect, nd_pd, nd_sz, fld_ind, typ, name, cnct_en):
	BoxField(world, obj_id, [pos[0]+nd_pd, pos[1]+fld_ind*(nd_sz+nd_pd)+nd_pd+rect[1]/4+nd_pd], [nd_sz, nd_sz],
	            [pos[0]+nd_sz+nd_pd*2, pos[1]+rect[1]/4+nd_pd+nd_pd], [rect[0]/2-nd_pd*2, nd_sz], typ, name, "left",
	            cnct_en, NdEn.BoxInp)

def BoxOutField(world, obj_id, pos, rect, nd_pd, nd_sz, fld_ind, typ, name, cnct_en):
	BoxField( world, obj_id, [pos[0]+rect[0]-nd_pd-nd_sz, pos[1]+fld_ind*(nd_sz+nd_pd)+nd_pd+rect[1]/4+nd_pd],
	             [nd_sz, nd_sz], [pos[0]+rect[0]/2+nd_pd, pos[1]+rect[1]/4+nd_pd+nd_pd],
	             [rect[0]/2-nd_sz-nd_pd*2-nd_pd*2, nd_sz], typ, name, "right", cnct_en, NdEn.BoxOut )
