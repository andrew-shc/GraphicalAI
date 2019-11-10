"""
This is where all the custom defined graphic object be used in each *model*

All defined graphic object must have an __repr__() method and a entity with obj_id binded with fld_nm and fld_typ
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

    # to be read by the executor
    def __repr__(self):
        val = self.world.entity_data([self.ent])
        return f"str\x01{val[0]['text']}\x00"

    def create(self, world, oid, pos, rect, fld_nm, fld_typ):
        font = p.font.SysFont("mono", self.font_size)
        dimn = font.size(self.name)

        # *IMPORTANT* graphic object INTERNAL META DATA
        # ALWAYS include at least an obj_id with fld_nm (field name) and fld_typ (field type)
        # to be recognized as a field
        world.create(obj_id=oid, fld_nm=fld_nm, fld_typ=fld_typ, cid=self )

        # title text field
        world.create(obj_id=oid, pos=pos, rect=[dimn[0], rect[1]], font="mono", font_size=self.font_size,
                     font_color=(0, 0, 0), font_align={"x": "center", "y": "center"}, text=self.name, text_align=True,)

        # input field
        targ = world.create(obj_id=oid, pos=[pos[0]+dimn[0], pos[1]], rect=[rect[0]-dimn[0], rect[1]],
                     color=self.backg, at=False, font=self.font, font_size=self.font_size, font_color=self.foreg,
                     font_align=self.font_align, text=self.default, text_align=True, cursor=0)

        self.ent = targ[1]
        self.world = world

