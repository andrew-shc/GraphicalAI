Organized way to explain what each component is and system is.
And a way for me, as a maintainer, to reference what each component is
especially in a typeless environment in Python.

## Component
All component name must only have characters of [A-Z][a-z]_  

**obj_id**  *`<uint>`*  
For grouping bunch of entities into manageable graphics "object"

**pos** *`<[uint, uint]>`*

**size** *`<[uint, uint]>`*

**color** *\( 0i-255i, 0i-255i, 0i-255i )*

**font** *\<str>*

**font_size** *\<int>*

**font_color** *\( 0i-255i, 0i-255i, 0i-255i )*

**font_align** *\*

**text** *\*

**text_align** *\*

**clicked** *\*

**movable** *\*

**function** *\*

**field** *\*

**fld_nm** *\*

**fld_typ** *\*

**fld_dt** *\*

**placement_ofs** *\*

**child** *\*

**connectee** *\*

**connect_en** *\*

**#unkown** *\*

**#unkown** *\*

**#unkown** *\*

"font_size", "font_color", "font_align", "text", "text_align",
              "clicked", "movable", "function", "field", "fld_nm", "fld_typ", "fld_dt", "placement_ofs", "child",
              "connectee", "connect_en", "connect_tg"]


## System
Systems should have the same character set as component but all System
name must start with lowercase alphabet (no number or uppercase)

[rect, label, fields, click, move]

##### (sys req) => system name => (sys write)
System description

##### (pos,size,color) => rect => ()
To render a simple rectangle

