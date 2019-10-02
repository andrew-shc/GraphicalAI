import pygame as p


def _id_trnsl_( cmpnt, req):
	ID_MATCH = []
	for c in cmpnt:
		if c not in req: ID_MATCH.append( 0 )
		else: ID_MATCH.append( 1 )
	return ID_MATCH

def _id_match_( id_trans, entity ):
	REQUESTED = True
	for id, c in zip(id_trans, entity):
		if id == 1 and c == -1: REQUESTED = False
	return REQUESTED

def _cmpn_req_( ent, cmpnt, req=None):  # component requested
	CMPNT_UNREG = [] # invalid requested components
	for r in req:
		if r not in cmpnt:
			CMPNT_UNREG.append(r)
	if CMPNT_UNREG != []:
		print( "\033[1;31m ERROR: \033[0m", CMPNT_UNREG, "\033[1;31m are not registered components! \033[0m", )
		return False

	ID_TRANS = _id_trnsl_( cmpnt, req )  # translates requested string components to translated required id
	MATCHED = []  # entity passed the requirement

	for entity in ent:
		if _id_match_(ID_TRANS, entity):
			MATCHED.append(entity)

	return MATCHED

def _merge_data_( eid, container, cmpnt):  # merge ID into data from container and component
	DATA = {}
	for ind, c in enumerate(eid):
		if c != -1: DATA[cmpnt[ind]] = container[ind][c]
	return DATA

def _boilerplate_( ent, cmpnt, cont ):
	res = _cmpn_req_( ent, cmpnt, ["text", ] )
	if res is not False:
		ents = [_merge_data_( e, cont, cmpnt ) for e in res]
		for dt in ents:
			# func()
			pass

# ======= SYSTEMS =======


def label( ent, cmpnt, cont, glbl ):
	res = _cmpn_req_( ent, cmpnt, ["text",])
	if res is not False:
		ents = [_merge_data_( e, cont, cmpnt ) for e in res]
		for dt in ents:
			print(dt)
			print(glbl)

