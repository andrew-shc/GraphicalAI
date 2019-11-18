"""
This is where all the custom defined graphic object be used in each *model*

All defined graphic object must have an __repr__() method and a entity with obj_id binded with fld_nm and fld_typ

NOTE: Graphic Object can also be used in the main program
    as the design philophsy for the model.py is a subset of the main program but will still add field data potentially
    confusing the program
"""
import pygame as p


class TextField:
    go_id = 0x0000

    def __init__(self, name, default="", font_align={"x": "center", "y": "center"},
                 backg=(200, 255, 255), foreg=(0,0,0), font="arial", font_size=24):
        self.default = default
        self.backg = backg  # background
        self.foreg = foreg  # foreground (text colour)
        self.font = font
        self.font_size = font_size
        self.font_align = font_align
        self.name = name

        self.ent = None
        self.world = None

    # to read by the people
    def __str__(self):
        return f"Current Input Value: {self.default}"

    # to be read by the executor and the models
    def __repr__(self):
        val = self.world.entity_data([self.ent])
        return f"{val[0]['text']}"

    def create(self, world, oid, pos, rect, fld):
        font = p.font.SysFont("mono", self.font_size)
        dimn = font.size(self.name)

        # *IMPORTANT* graphic object INTERNAL META DATA
        # ALWAYS include at least an obj_id with fld_dt (field data) and cid (constant (graphic object) id)
        # to be recognized as a field
        world.create(obj_id=oid, fld_dt=fld)

        # title text field
        world.create(obj_id=oid, pos=pos, rect=[dimn[0], rect[1]], font="mono", font_size=self.font_size,
                     font_color=(0, 0, 0), font_align={"x": "center", "y": "center"}, text=self.name, text_align=True,)

        # input field
        targ = world.create(obj_id=oid, pos=[pos[0]+dimn[0], pos[1]], rect=[rect[0]-dimn[0], rect[1]],
                     color=self.backg, at=False, font=self.font, font_size=self.font_size, font_color=self.foreg,
                     font_align=self.font_align, text=self.default, text_align=True, cursor=0)

        self.ent = targ[1]
        self.world = world

