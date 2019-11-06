Organized way to explain what each component is and system is.
And a way for me, as a maintainer, to reference what each component is
especially in a typeless environment in Python.

## Component
All component name must only have characters of [A-Z][a-z]_  

**`obj_id`**  *`uint`*  
For grouping bunch of entities into manageable graphics "object"

**`pos`** *`[uint, uint]`*  
An object's position `(x, y)` describing where is the object is  
Note: `(0, 0)` is at the top-left corner

**`size`** *`[uint, uint]`*  
Describes an object's rectangular size `(width, height)`

**`color`** *`(0-255,0-255,0-255)`*  
Object's color to display on the screen

**`font`** *`str`*  
Font type to render the text as

**`font_size`** *`uint`*  
Describes how big should the text be

**`font_color`** *`(0-255,0-255,0-255)`*  
Describes what type of color should the font be rendered as

**`font_align`** *`None`*

**`text`** *`str`*
A string of character for displaying text or other manipulative operation

**`text_align`** *`None`*

**`clicked`** *`bool`*

**`movable`** *`bool`*
Describes the object if it is movable

**`function`** *`<callable function>`*
To be called later in use

**`param`** *`[any, ...]`*
Parameters for the function component

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

**`connect_en`** *`[any, ...]`*  
A list of tags that are allowed to be connected (whitelist)

**`connect_tg`** *`any`*  
Connector's tag for identification

**`length`** *`uint`*  

**`width`** *`uint`*  

**`cursor`** *`uint`*  
Cursor's position

**`at`** *`bool`*  
Describe if the user is at the location

**`trigger`** *`str`*  
Describe the type of trigger you want: onclick, offclick, hover

## System
Systems should have the same character set as component but all System
name must start with lowercase alphabet (no number or uppercase)

[rect, label, fields, click, move]

##### `(sys req) => sys nm => (sys wrt)`
sys req: System component requirements  
sys nm: System Name  
sys wrt: System component to write on  

`<req>Name -> ret`

### General Systems

**`() => label => ()`**  
text

**`(pos,size,color) => rect => ()`**  
To render a simple rectangle

**`() => click => ()`**  
text

**`() => move => ()`**  
text

**`() => move_child => ()`**  
text

**`() => connectorWireIso => ()`**  
text

**`() => connectorWireMrg => ()`**  
text

**`() => connectNode => ()`**  
text

**`() => textField => ()`**#TODO  
text

### Special Systems

**`() => genFields => ()`**  
text