Organized way to explain what each component is and system is

## Component
All component name must only have characters of [A-Z][a-z]_
["obj_id", "pos", "size", "color", "font", "font_size", "font_color", "font_align", "text", "text_align",
              "clicked", "movable", "function", "field", "fld_nm", "fld_typ", "fld_dt", "placement_ofs", "child"]

##### obj_id *\<int>*
For grouping bunch of entities into manageable graphics "object"

##### pos *\[int, int]*

##### size *\[int, int]*

##### color *(int, int)*

##### font *\<str>*


## System
Systems should have the same character set as component but all System
name must start with lowercase alphabet (no number or uppercase)

[rect, label, fields, click, move]

##### (sys req) => system name => (sys write)
System description

##### (pos,size,color) => rect => ()
To render a simple rectangle

