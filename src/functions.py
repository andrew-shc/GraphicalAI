import sys
import pygame as p

# ...in obj:  // main flow
# ...in list(obj.keys())[::-1]:  // invert flow

def _state_acquired( state, req ):  # check if the state is acquired
	try:
		key = state.keys()
		for r in req:
			if r not in key:
				# print("\033[1;31m ERROR: \033[0m", state, "\033[1;31m does not contain keys \033[0m", req, "\033[1;31m to run \033[0m", "<"+sys._getframe().f_back.f_code.co_name+">" )
				return False
		return True
	except AttributeError:
		KeyError("State not fully acquired")

# state: object's state description, req: required state in dictionary
def _state_required( state, req ):  # check if the state has been required
	key = state.keys()
	for k in req:
		if k in key:  # found the same module on the same level: k ~ req
			if req[k] is None:
				pass
			elif type(state[k]) != dict:  # when the requirement has more though the state does not
				print( "\033[1;31m ERROR: \033[0m", state, "\033[1;31m does not contain keys \033[0m", req,
				       "\033[1;31m to run \033[0m", "<"+sys._getframe().f_back.f_code.co_name+">" )
				return False
			else:  # nested requirements
				if _state_required( state[k], req[k]) is False:  # requirements failed below the relative level; propagates
					print( "\033[1;31m ERROR: \033[0m", state, "\033[1;31m does not contain keys \033[0m", req,
					       "\033[1;31m to run \033[0m", "<"+sys._getframe().f_back.f_code.co_name+">" )
					return False
		else:  # no match on the same level
			print( "\033[1;31m ERROR: \033[0m", state, "\033[1;31m does not contain keys \033[0m", req,
			       "\033[1;31m to run \033[0m", "<"+sys._getframe().f_back.f_code.co_name+">" )
			return False
	return True

def _label( surf, text, font, text_size, pos, size, alignX="center", alignY="center", txt_align=True):
	font = p.font.SysFont( font, text_size )
	label = font.render( text, True, (0, 0, 0) )
	dimn = font.size( text )
	pkx = {  # Position Key X
		"left" : pos[0],
		"center": pos[0]+size[0]/2-(dimn[0]/2 if txt_align else 0),
		"right"  : pos[0]+size[0]-(dimn[0] if txt_align else 0),
	}
	pky = {  # Position Key Y
		"top"   : pos[1],
		"center": pos[1]+size[1]/2-(dimn[1]/2 if txt_align else 0),
		"bottom": pos[1]+size[1]-(dimn[1] if txt_align else 0),
	}
	surf.blit( label, (pkx[alignX], pky[alignY]) )
	return dimn

def renderNode( event, obj ):
	for id in obj:
		s = obj[id]  # state
		if _state_acquired( s, ["surf", "pos", "size", "fld_dt", "fld_style", "title"] ):
			p.draw.rect( s["surf"], (225, 255, 255), [s["pos"][0], s["pos"][1], s["size"][0], s["size"][1]] )  # output
			p.draw.rect( s["surf"], (200, 255, 255), [s["pos"][0], s["pos"][1], s["size"][0]/2, s["size"][1]] )  # input
			p.draw.rect( s["surf"], (220, 220, 220), [s["pos"][0], s["pos"][1], s["size"][0], s["size"][1]/4] )  # title

			_label( s["surf"], s["title"], "arial", 15,
			        (s["pos"][0], s["pos"][1]),
			        (s["size"][0], s["size"][1]/4),
			)

			fld = s["fld_dt"]
			sty = s["fld_style"]
			f_no = 0
			for f in fld["fieldI"]:
				p.draw.rect( s["surf"], (0,0,0),
				    ( s["pos"][0]+sty["nd_pad"][0], s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*f_no,
				    sty["nd_sz"], sty["nd_sz"] )
				)  # selectation node

				_label( s["surf"], str(f), "arial", 15,
				    (s["pos"][0]+sty["nd_pad"][0], s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*f_no),
				    (s["size"][0]/2-sty["nd_pad"][0]*2, sty["height"]),
				    alignX="right",
				)

				f_no += 1

			f_no = 0
			for f in fld["fieldO"]:
				p.draw.rect( s["surf"], (0, 0, 0),
				    (s["pos"][0]+s["size"][0]-sty["nd_sz"]-sty["nd_pad"][0],
				     s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*f_no,
				    sty["nd_sz"], sty["nd_sz"])
				)  # selectation node

				_label( s["surf"], str( f ), "arial", 15,
				    (s["pos"][0]+s["size"][0]/2+sty["nd_pad"][0],
				    s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*f_no),
					(s["size"][0], sty["height"]),
				    alignX="left",
				)

				f_no += 1

def renderWire( event, obj ):
	for idin in obj:
		s = obj[idin]
		if _state_acquired( s, ["surf", "pos", "size", "fld_style", "fld_dt"]):
			fld = s["fld_dt"]
			sty = s["fld_style"]
			for fID, fieldI in enumerate(fld["fieldI"]):  # loops internal field input inside [fieldI]
				for idext, f_no in fld["fieldI"][fieldI]:  # loops all the field data has in fieldI
					# pos1: native node, pos2: foreign node
					xs = obj[idext]  # get external output field id
					xfld = xs["fld_dt"]
					xsty = xs["fld_style"]

					pos1 = [s["pos"][0]+sty["nd_pad"][0],
					        s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*fID]
					pos2 = [xs["pos"][0]+xs["size"][0]-xsty["nd_sz"]-xsty["nd_pad"][0],
					        xs["pos"][1]+xs["size"][1]/4+xsty["nd_pad"][1]+(xsty["height"]+xsty["pad"])*f_no]
					p.draw.line(s["surf"], (0, 255, 0), pos1, pos2, 3)
			for fID, fieldO in enumerate(fld["fieldO"]):  # loops internal field output inside [fieldO]
				for idext, f_no in fld["fieldO"][fieldO]:  # loops all the field data has in fieldO
					# pos1: native node, pos2: foreign node
					xs = obj[idext]  # get external input field id
					xfld = xs["fld_dt"]
					xsty = xs["fld_style"]

					pos1 = [s["pos"][0]+s["size"][0]-sty["nd_sz"]-sty["nd_pad"][0],
					        s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*fID]
					pos2 = [xs["pos"][0]+xsty["nd_pad"][0],
					        xs["pos"][1]+xs["size"][1]/4+xsty["nd_pad"][1]+(xsty["height"]+xsty["pad"])*f_no]
					p.draw.line(s["surf"], (0, 255, 0), pos1, pos2, 3)


def renderLabel( event, obj ):
	for id in obj:
		s = obj[id]  # state
		if _state_acquired( s, ["surf", "pos", "size", "label",] ):
			p.draw.rect( s["surf"],
			             (255, 200, 180),
			             [s["pos"][0], s["pos"][1], s["size"][0], s["size"][1]]
			)
			if s["label"]["text"] is not None:
				font = p.font.SysFont( s["label"]["font"], s["label"]["font-size"] )
				txt = font.render( s["label"]["text"], True, (0, 0, 0) )
				dimn = font.size(s["label"]["text"])
				s["surf"].blit(txt, [s["pos"][0]+s["size"][0]/2-dimn[0]/2, s["pos"][1]+s["size"][1]/2-dimn[1]/2])

# TODO: CHNG
def clickNode( event, obj ):  # which node selected
	mOnTrig = False
	mOffTrig = False
	mPos = p.mouse.get_pos()  # [x y]
	for e in event:
		if e.type == p.MOUSEBUTTONDOWN: mOnTrig = True
		elif e.type == p.MOUSEBUTTONUP: mOffTrig = True

	for idin in list(obj.keys())[::-1]:
		s = obj[idin]  # state
		# TODO: Possible speed improvement
		clicked = False
		for idext in obj:
			if _state_acquired( obj[idext], ["clicked",] ):
				if obj[idext]["clicked"] != None:  # another node clicked; prevents multiple nodes clicked
					clicked = True

		if _state_acquired( s, ["clicked", "pos", "size", "fld_dt", "fld_style"] ):
			fld = s["fld_dt"]
			sty = s["fld_style"]
			if len(fld["fieldI"]) != 0:  # there are input fields
				for f_no in range(len(s["fld_dt"]["fieldI"])):
					# pos=each field's selecation node position
					pos = [ s["pos"][0]+sty["nd_pad"][0], s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*f_no ]
					size = [ sty["nd_sz"], sty["nd_sz"] ]
					if mOnTrig and not clicked and \
							pos[0] < mPos[0] < pos[0]+size[0] and \
							pos[1] < mPos[1] < pos[1]+size[1]:  # input
						s["clicked"] = "FIELD"
						fld["selected"]["type"] = "INP"
						fld["selected"]["field"] = f_no
			if len(fld["fieldO"]) != 0:  # there are output fields
				for f_no in range( len( s["fld_dt"]["fieldO"] ) ):
					# pos=each field's selecation node position
					pos = [s["pos"][0]+s["size"][0]-sty["nd_pad"][0]-sty["nd_sz"],
				     s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*f_no]
					size = [sty["nd_sz"], sty["nd_sz"]]
					if mOnTrig and not clicked and \
							pos[0] < mPos[0] < pos[0]+size[0] and \
							pos[1] < mPos[1] < pos[1]+size[1]:  # output
						s["clicked"] = "FIELD"
						fld["selected"]["type"] = "OUT"
						fld["selected"]["field"] = f_no

			if mOffTrig and s["clicked"]:
				s["clicked"] = None
				fld["selected"]["type"] = None
				fld["selected"]["field"] = None


def rectClicked( event, obj ):
	mOnTrig = False
	mOffTrig = False
	mPos = p.mouse.get_pos()  # [x y]
	for e in event:
		if e.type == p.MOUSEBUTTONDOWN: mOnTrig = True
		elif e.type == p.MOUSEBUTTONUP: mOffTrig = True

	for idin in list( obj.keys() )[::-1]:
		s = obj[idin]  # state

		# TODO: Possible speed improvement
		clicked = False
		for idext in obj:
			if _state_acquired( obj[idext], ["clicked", ] ):
				if obj[idext]["clicked"] != None:  # another node clicked; prevents multiple nodes clicked
					clicked = True

		if _state_acquired( s, ["clicked", "pos", "size", ] ):
			if s["pos"][0] < mPos[0] < s["pos"][0]+s["size"][0] and not clicked and \
					s["pos"][1] < mPos[1] < s["pos"][1]+s["size"][1] and mOnTrig:  # main
				s["clicked"] = "MAIN"

			if mOffTrig and s["clicked"]: s["clicked"] = None


def triggerUpdate( event, obj ):
	mOnTrig = False
	mOffTrig = False
	mPos = p.mouse.get_pos()  # [x y]
	for e in event:
		if e.type == p.MOUSEBUTTONDOWN: mOnTrig = True
		elif e.type == p.MOUSEBUTTONUP: mOffTrig = True

	for idin in list( obj.keys() )[::-1]:
		s = obj[idin]  # state

		if _state_acquired( s, ["trigger", "pos", "size", ] ):
			s["trigger"] = None
			if s["pos"][0] < mPos[0] < s["pos"][0]+s["size"][0] and \
					s["pos"][1] < mPos[1] < s["pos"][1]+s["size"][1] and mOnTrig:  # main
				s["trigger"] = "ON"
			elif s["pos"][0] < mPos[0] < s["pos"][0]+s["size"][0] and \
					s["pos"][1] < mPos[1] < s["pos"][1]+s["size"][1] and mOffTrig:  # main
				s["trigger"] = "OFF"


def moveObject( event, obj ):
	for id in list( obj.keys() )[::-1]:
		s = obj[id]  # state
		if _state_acquired( s, ["clicked", "pos", "size", "movable"] ):
			if s["clicked"] == "MAIN" and s["movable"]:
				s["pos"] = [p.mouse.get_pos()[0]-s["size"][0]/2, p.mouse.get_pos()[1]-s["size"][1]/2]


def buttonListener( event, obj ):  # calls the function
	for id in list( obj.keys() )[::-1]:
		s = obj[id]  # state
		if _state_acquired( s, ["clicked", "trigger", "pos", "size", "function"] ):
			if s["clicked"] == "MAIN" and s["trigger"] == "ON":
				s["function"]( event, obj )

# TODO: CHNG
def matchNode( event, obj ):
	mOnTrig = False
	mOffTrig = False
	mPos = p.mouse.get_pos()  # [x y]
	for e in event:
		if e.type == p.MOUSEBUTTONDOWN: mOnTrig = True
		elif e.type == p.MOUSEBUTTONUP: mOffTrig = True

	for idin in list( obj.keys() )[::-1]:
		s = obj[idin]  # state
		# TODO: Possible speed improvement
		clicked = False
		for idext in obj:
			if _state_acquired( obj[idext], ["clicked", ] ):
				if obj[idext]["clicked"] != None:  # another node clicked; prevents multiple nodes clicked
					clicked = True

		if _state_acquired( s, ["clicked", "pos", "size", "fld_dt", "fld_style"] ):
			fld = s["fld_dt"]
			sty = s["fld_style"]

			for f_no in range( len( s["fld_dt"]["fieldI"] ) ):  # check for input fields
				# pos=each field's selecation node position
				pos = [s["pos"][0]+sty["nd_pad"][0],
				       s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*f_no]
				size = [sty["nd_sz"], sty["nd_sz"]]
				if mOffTrig and pos[0] < mPos[0] < pos[0]+size[0] and pos[1] < mPos[1] < pos[1]+size[1]:  # selected field
					for idext in list(obj.keys()):
						idext_s = obj[idext]
						if _state_acquired( idext_s, ["clicked", "fld_dt"] ):
							if idext_s["clicked"] == "FIELD" and idext_s["fld_dt"]["selected"]["type"] == "OUT":
								loc = [ idext, idext_s["fld_dt"]["selected"]["field"] ]  # [idext, field_no ]
								idext_s["fld_dt"]["fieldO"][list(idext_s["fld_dt"]["fieldO"])[ idext_s["fld_dt"]["selected"]["field"]] ].append( [ idin, f_no ] )
								fld["fieldI"][list(fld["fieldI"])[f_no]].append(loc)

			for f_no in range( len( s["fld_dt"]["fieldO"] ) ):  # check for output fields
				# pos=each field's selecation node position
				pos = [s["pos"][0]+s["size"][0]-sty["nd_pad"][0]-sty["nd_sz"],
				       s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*f_no]
				size = [sty["nd_sz"], sty["nd_sz"]]
				if mOffTrig and pos[0] < mPos[0] < pos[0]+size[0] and pos[1] < mPos[1] < pos[1]+size[1]:  # selected field
					for idext in list( obj.keys() ):
						idext_s = obj[idext]
						if _state_acquired( idext, ["clicked", "fld_dt"] ):
							if idext["clicked"] == "FIELD" and idext["fld_dt"]["selected"]["type"] == "IN":
								loc = [ idext, idext_s["fld_dt"]["selected"]["field"] ]  # [idext, field_no ]
								idext_s["fld_dt"]["fieldI"][list(idext_s["fld_dt"]["fieldI"])[ idext_s["fld_dt"]["selected"]["field"]] ].append( [idin, f_no] )
								fld["fieldI"][list( fld["fieldI"] )[f_no]].append( loc )


# TODO: CHNG
def connectNode( event, obj ):  # render wire
	mPos = p.mouse.get_pos()

	for id in list( obj.keys() )[::-1]:
		s = obj[id]  # state
		if _state_acquired( s, ["surf", "clicked", "fld_dt", "fld_style", "pos",] ):
			if s["clicked"] == "FIELD":
				fld = s["fld_dt"]
				sty = s["fld_style"]

				print( fld["selected"]["type"] )
				if fld["selected"]["type"] == "INP":
					p.draw.line( s["surf"], (255, 100, 0), (s["pos"][0]+2,
					    s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*fld["selected"]["field"]),
				        mPos )
				elif fld["selected"]["type"] == "OUT":
					p.draw.line( s["surf"], (255, 100, 0), (s["pos"][0]+s["size"][0]-sty["nd_pad"][0],
				        s["pos"][1]+s["size"][1]/4+sty["nd_pad"][1]+(sty["height"]+sty["pad"])*fld["selected"]["field"]),
					    mPos )


REG_FUNCTIONS = [renderNode, renderLabel, renderWire, matchNode, clickNode, triggerUpdate, moveObject, connectNode, rectClicked, buttonListener]
