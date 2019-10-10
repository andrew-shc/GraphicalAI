import pygame as p
from src.debugger import *


# ====== SUBROUTINE =====

# returns entity with the only requested components
def _entity_only( self, req ): return self.entity_data( self.entity( req ), _strict=req )

# boilerplate code
def _entity_req( self, req ):
	ind = self.entity( req )
	dat = self.entity_data( ind )
	return dat, ind

# ======= SYSTEMS =======


def label( self, glbl ):
	req = ["pos", "size", "text", "font", "font_size", "font_color", "font_align", "text_align"]
	e_main = self.entity_data( self.entity( req ) )
	for dt in e_main:
		font = p.font.SysFont( dt["font"], dt["font_size"] )
		label = font.render( dt["text"], True, (0, 0, 0) )
		dimn = font.size( dt["text"] )
		pkx = {  # Position Key X
			"left"  :dt["pos"][0],
			"center":dt["pos"][0]+dt["size"][0]/2-(dimn[0]/2 if dt["text_align"] else 0),
			"right" :dt["pos"][0]+dt["size"][0]-(dimn[0] if dt["text_align"] else 0),
		}
		pky = {  # Position Key Y
			"top"   :dt["pos"][1],
			"center":dt["pos"][1]+dt["size"][1]/2-(dimn[1]/2 if dt["text_align"] else 0),
			"bottom":dt["pos"][1]+dt["size"][1]-(dimn[1] if dt["text_align"] else 0),
		}
		glbl["surf"].blit( label, (pkx[dt["font_align"]["x"]], pky[dt["font_align"]["y"]]) )

def rect( self, glbl ):
	req = ["pos", "size", "color", ]
	e_main = self.entity_data( self.entity( req ) )
	for dt in e_main:
		p.draw.rect(glbl["surf"], dt["color"], [dt["pos"][0], dt["pos"][1], dt["size"][0], dt["size"][1]])

def click( self, glbl ):
	req = ["pos", "size", "clicked", ]
	e_main = self.entity_data( self.entity( req ) )

	clicked = False
	e_click = self.entity_data( self.ENTITIES, ["clicked"] ) # check if any other entity has clicked
	for c in e_click:
		if c:
			clicked = True

	for eid, dt in zip(reversed(self.entity(req)), reversed(e_main)):
		if dt["pos"][0] < glbl["event"]["mPos"][0] < dt["pos"][0]+dt["size"][0] and not clicked and \
				dt["pos"][1] < glbl["event"]["mPos"][1] < dt["pos"][1]+dt["size"][1] and glbl["event"]["mTrgOn"]:  # main
			dt["clicked"] = True
			clicked = True
		if glbl["event"]["mTrgOff"] and dt["clicked"]: dt["clicked"] = False
		self.entity_save(eid, dt)

def move( self, glbl ):
	req = ["pos", "clicked", "movable", "placement_ofs"]
	e_main = self.entity_data( self.entity( req ) )
	for eid, dt in zip(reversed(self.entity(req)), reversed(e_main)):
		if dt["movable"]:
			if dt["clicked"] and dt["placement_ofs"] == [None, None]: # first clicked
				dt["placement_ofs"] = [dt["pos"][0]-glbl["event"]["mPos"][0], dt["pos"][1]-glbl["event"]["mPos"][1]]
			elif dt["clicked"]:  # next continues clicked
				dt["pos"] = [dt["placement_ofs"][0]+glbl["event"]["mPos"][0], dt["placement_ofs"][1]+glbl["event"]["mPos"][1]]
			else:  # finish clicking
				dt["placement_ofs"] = [None, None]
		self.entity_save( eid, dt )

def move_child( self, glbl ):
	req = ["pos", "movable", "child"]
	e_main, e_ind = _entity_req( self, req )
	for eid, dt in zip( reversed( e_ind ), reversed( e_main ) ):
		if dt["movable"] and dt["placement_ofs"] != [None, None]:
			e_child, e_indc = _entity_req( self, ["obj_id", "pos"] )
			for eidc, dtc in zip( reversed( e_indc ), reversed( e_child ) ):
				if dtc["obj_id"] == dt["child"]:  # this child entity is part of the master entity
					vector = [(glbl["event"]["mPos"][0]+dt["placement_ofs"][0])-dt["pos"][0],
					           (glbl["event"]["mPos"][1]+dt["placement_ofs"][1])-dt["pos"][1]]
					dtc["pos"][0] += vector[0]
					dtc["pos"][1] += vector[1]
					self.entity_save( eidc, dtc )

# special systems -- for specific purposes

def gen_fields( self, glbl ):
	req = ["obj_id", "pos", "field", ]
	e_main = self.entity_data( self.entity( req ) )
	for dt in e_main:
		e_child = _entity_only( self, ["fld_nm", ] )
		e_missing = []  # fields that are missing
		print(e_child)
		print(dt["field"].keys())

		for f in dt["field"]:
			if f not in e_child:
				e_missing.append(f)

		nd_pd = glbl["fld_sty"]["nd_pad"]
		nd_sz = glbl["fld_sty"]["nd_sz"]

		ind_i, ind_o = 0, 0
		for f in e_missing:  # creating a new entity
			if dt["field"][f] == glbl["node_typ"]["inp"]:
				self.create(obj_id=dt["child"], pos=[dt["pos"][0]+nd_pd,
				                                     dt["pos"][1]+ind_i*(nd_sz+nd_pd)+nd_pd+dt["size"][1]/4+nd_pd],
				            size=[nd_sz, nd_sz], color=(0, 0, 0), fld_nm=f, fld_typ=dt["field"][f], fld_dt=None, clicked=False)
				self.create( obj_id=dt["child"], pos=[dt["pos"][0]+nd_sz+nd_pd*2, dt["pos"][1]+dt["size"][1]/4+nd_pd+nd_pd],
				              size=[dt["size"][0]/2-nd_pd*2, nd_sz], font="mono", font_size=12,
				              font_color=(0, 0, 0),
				              font_align={"x":"left", "y":"center"}, text=f,
				              text_align=True )  # input node text
				ind_i += 1
			elif dt["field"][f] == glbl["node_typ"]["out"]:
				self.create(obj_id=dt["child"], pos=[dt["pos"][0]+dt["size"][0]-nd_pd-nd_sz,
				                                     dt["pos"][1]+ind_o*(nd_sz+nd_pd)+nd_pd+dt["size"][1]/4+nd_pd],
				            size=[nd_sz, nd_sz], color=(0, 0, 0), fld_nm=f, fld_typ=dt["field"][f], fld_dt=None, clicked=False)
				self.create( obj_id=dt["child"], pos=[dt["pos"][0]+dt["size"][0]/2+nd_pd,
				                                      dt["pos"][1]+dt["size"][1]/4+nd_pd+nd_pd],
				             size=[dt["size"][0]/2-nd_sz-nd_pd*2-nd_pd*2, nd_sz], font="mono", font_size=12,
				             font_color=(0, 0, 0),
				             font_align={"x":"right", "y":"center"}, text=f,
				             text_align=True )  # output node text
				ind_o += 1
			elif dt["field"][f] == glbl["node_typ"]["user"]:  # user defined node, uses custom entities
				ind_u = max( ind_i, ind_o )+1
				self.create(obj_id=dt["child"], pos=[dt["pos"][0], dt["pos"][1]+ind_u*(nd_sz+nd_pd)+nd_pd+dt["size"][1]/4+nd_pd],
				            size=[dt["size"][0], 25], color=(0, 0, 0), fld_nm=f, fld_typ=dt["field"][f], fld_dt=None )

# match the nodes
def match_node( self, glbl ):
	req = ["pos", "rect", "clicked", "fld_dt"]
	e_main = self.entity_data( self.entity( req ) )
	selected_node = []  # ID of the node
	typ = None  # type of the selected node
	for eid, dt in zip( self.entity( req ), e_main ):
		if dt["clicked"]:
			selected_node = dt

	for eid, dt in zip( self.entity( req ), e_main ):
		if dt["pos"][0] < glbl["event"]["mPos"][0] < dt["pos"][0]+dt["size"][0] and \
				dt["pos"][1] < glbl["event"]["mPos"][1] < dt["pos"][1]+dt["size"][1] and glbl["event"]["mTrgOff"]:
			pass # selected_node["fld_dt"][]

# render isolated wire (wire connected to the mouse)
def render_iso_wire( self, glbl ):
	req = ["pos", "rect", "clicked", "fld_dt" ]
	e_main = self.entity_data( self.entity( req ) )
	for dt in e_main:
		if dt["clicked"]:
			p.draw.line(glbl["surf"], (255, 150, 0), dt["pos"], glbl["event"]["mPos"], 3)
