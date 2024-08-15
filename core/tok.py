import enum
import basicTypes as bt


class TokenTypes(enum.Enum):
    """
    Class containing all token types with values to identify them.
    """
    # Basic
    INVALID = -1
    EOF = 0
    INIT = 1
    ATTR = 2
    PROGDECL = 3
    PROGDECLTEXT = 4
    PLACEHOLDER = 5

    # Arithmetic operators
    PLUS = 101
    MINUS = 102
    ASTERISK = 103
    FSLASH = 104
    CARET = 105

    # Assignment and comparison operators
    EQ = 201
    EQEQ = 202
    NOTEQ = 203
    LT = 204
    LTEQ = 205
    GT = 206
    GTEQ = 207

    # Keywords (data types)
    INT = 301
    FLOAT = 302
    STRING = 303
    BOOL = 304
    IDENT = 305
    KEYWD = 340
    # Keywords (others)
    LET = 341
    IF = 342
    ELIF = 343
    ELSE = 344
    WHILE = 345
    FOR = 346
    FUN = 347
    RETURN = 348
    PRINT = 349
    SCAN = 350
    RAISE = 351
    TRUE = 352
    FALSE = 353

    # Other symbols
    LPAREN = 401
    RPAREN = 402
    LFLOBRAC = 403
    RFLOBRAC = 404
    LSQBRAC = 405
    RSQBRAC = 406
    SEMICLN = 407
    COLON = 408
    COMMA = 409

    # Program declarations
    STATIC = 501
    DYNAMIC = 502


class TokenLiterals(enum.Enum):
    """
    Class containing all token literals with literals to identify them.
    """
    # Basic
    EOF = '\0'
    ATTR = '.'
    PROGDECL = '~'
    
    # Arithmetic operators
    PLUS = '+'
    MINUS = '-'
    ASTERISK = '*'
    FSLASH = '/'
    CARET = '^'

    # Assignment and comparison operators
    EQ = '='
    EQEQ = '=='
    NOTEQ = '!='
    LT = '<'
    LTEQ = '<='
    GT = '>'
    GTEQ = '>='

    # Other symbols
    LPAREN = '('
    RPAREN = ')'
    LFLOBRAC = '{'
    RFLOBRAC = '}'
    LSQBRAC = '['
    RSQBRAC = ']'
    SEMICLN = ';'
    COLON = ':'
    COMMA = ','


class Token:
    def __init__(self, typ:TokenTypes, val:bt.BaseForAll, line:int, pos:int, printPos:int, size:int) -> None:
        self.typ = typ
        self.val = val
        self.line = line
        self.pos = pos
        self.printPos = printPos
        self.size = size
    
    def __repr__(self) -> str:
        return f"Token[Typ({self.typ.name}): Val({self.val}): Line({self.line}): Pos({self.pos}): PrintPos({self.printPos}): Size({self.size})]"
    
    def __str__(self) -> str:
        val = '\'' + str(self.val) + '\''
        return f"Type={self.typ.name}: Value={val}: Line={self.line}: PrintPos={self.printPos}: Size={self.size}"
