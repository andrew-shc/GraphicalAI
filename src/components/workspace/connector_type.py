# Node input/output type specifier

class ConnectorType:
    # Requires at least typing of Matrix and Scalar
    Matrix = 0b10000001  # requires matrix type
    Scalar = 0b10000010  # requires scalar type
    String = 0b00000100  # requires text/string type
    Float  = 0b00001000  # requires float type
    Int    = 0b00010000  # requires integer type
    Bool   = 0b00100000  # requires boolean type (true/false)
    Any    = 0b11000000  # any type


# Matrix: A Square Design
# Scalar: A Circular Design
# String: Green Color
# Float: Blue Color
# Integer: Cyan Color
# Bool: Red Color
# Any (Discrete): Black Color
# Any (Matrix|Scalar): Black Triangle

# Typing Hierarchical
# -- every type can only be compatible by itself --
# -- EXCEPT:
# Any [= ( Any | Matrix | Scalar | String | Float | Int | Bool )
# Matrix | Any [= ( Matrix | ( Any | String | Float | Int | Bool ) )
# Scalar | Any [= ( Scalar | ( Any | String | Float | Int | Bool ) )
# Matrix | Int [= Matrix | ( Int | Bool )
# Scalar | Int [= Matrix | ( Int | Bool )
