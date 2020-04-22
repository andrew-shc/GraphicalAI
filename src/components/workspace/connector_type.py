# Node input/output type specifier

class ConnectorType:
    # Requires at least typing of Matrix and Scalar
    Matrix   = 0b000000001  # requires matrix type (wrapper type)
    Scalar   = 0b000000010  # requires scalar type (wrapper type)
    String   = 0b000000100  # requires text/string type
    Float    = 0b000001000  # requires float type
    Int      = 0b000010000  # requires integer type
    Bool     = 0b000100000  # requires boolean type (true/false)
    Any      = 0b001000000  # any type
    Optional = 0b010000000  # nullable (wrapper type)


# Matrix: A Square Design
# Scalar: A Circular Design
# String: Green Color
# Float: Blue Color
# Integer: Cyan Color
# Bool: Red Color
# Any (Discrete): Black Color
# Any (Matrix|Scalar): Black Triangle
# Optional: Black Circle (for now)

# Typing Hierarchical
# -- every type can only be compatible by itself --
# -- EXCEPT:
# Any [= ( Any | Matrix | Scalar | String | Float | Int | Bool )
# Matrix | Any [= ( Matrix | ( Any | String | Float | Int | Bool ) )
# Scalar | Any [= ( Scalar | ( Any | String | Float | Int | Bool ) )
# Matrix | Int [= Matrix | ( Int | Bool )
# Scalar | Int [= Matrix | ( Int | Bool )
# Optional | ( [Any kind of type] ) [= ( Optional | ( [Any kind of type] ) ) | ( [Any kind of type] )
