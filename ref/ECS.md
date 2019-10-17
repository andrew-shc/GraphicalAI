Organized way to explain what each component is and system is.
And a way for me, as a maintainer, to reference what each component is
especially in a typeless environment in Python.

## Component
All component name must only have characters of [A-Z][a-z]_  

**`obj_id`**  *`uint`*  
For grouping bunch of entities into manageable graphics "object"

**`pos`** *`[uint, uint]`*  

**`size`** *`[uint, uint]`*  

**`color`** *`(0-255,0-255,0-255)`*  

**`font`** *`str`*  

**`font_size`** *`uint`*  

**`font_color`** *`(0-255,0-255,0-255)`*  

**`font_align`** *`None`*

**`text`** *`str`*

**`text_align`** *`None`*

**`clicked`** *`bool`*

**`movable`** *`bool`*

**`function`** *`None`*

**`field`** *`{str:cls_typ,...}`*  
Each field name as `str` has a type value `cls_typ` to signify which
graphical component you want to render it

**`fld_nm`** *`str`*  
Each field's name

**`fld_typ`** *`None`*

**`fld_dt`** *`None`*

**`placement_ofs`** *`[int,int]`*

**`child`** *`uint`*  
Each master entity with `child` component has only one `child`

**`connectee`** *`[uint, ...]`*  
The uint is got form the compact entity ID incrementing upward.

**`connect_en`** *`[any,...]`*

**`connect_tg`** *`any`*

**`unkown`** *`None`*

**`unkown`** *`None`*


## System
Systems should have the same character set as component but all System
name must start with lowercase alphabet (no number or uppercase)

[rect, label, fields, click, move]

##### `(sys req) => sys nm => (sys wrt)`
sys req: System component requirements
sys nm: System Name
sys wrt: System component to write on

**`(pos,size,color) => rect => ()`**  
To render a simple rectangle

**`() =>  => ()`**  
text

**`() =>  => ()`**  
text

**`() =>  => ()`**  
text

**`() =>  => ()`**  
text

**`() =>  => ()`**  
text

**`() =>  => ()`**  
text